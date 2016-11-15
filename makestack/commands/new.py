import os
from makestack import api
from makestack.helpers import error, success, generate_file, generate_dir


APPLICATION_YAML = """\
api: 1
name: {{ app_name }}
lang: c++

sources:
  - main.cpp

config:

"""

MAIN_CPP = """\
#include <app.h>

void setup() {
    static int i = 0;
    static int pin = 13;

    GPIO.set_pin_mode(pin, GPIO_OUTPUT_PIN);
    Timer.set_interval(1000 /* 1000ms = 1sec */, []() {
        GPIO.write(pin, (i % 2) ? GPIO_LOW : GPIO_HIGH);
        i++;
    });
}

"""

GITIGNORE = """\
/.config.yaml
"""

def main(args):
    path = args.path
    app_name = os.path.basename(path)

    generate_dir(path)
    generate_file(os.path.join(path, 'application.yaml'),
                  APPLICATION_YAML, locals())
    generate_file(os.path.join(path, 'main.cpp'),
                  MAIN_CPP)
    generate_file(os.path.join(path, '.gitignore'),
                  GITIGNORE)

    if args.register:
        api.invoke('POST', '/apps', params={ 'app_name': app_name })
        success("registered")
