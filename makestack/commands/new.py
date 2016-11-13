import os
from makestack.helpers import error, generate_file, generate_dir


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
    int pin = 13;

    GPIO.set_pin_mode(pin, GPIO_OUTPUT);
    Timer.set_interval(1000 /* 1000ms = 1sec */, []() {
        GPIO.write((i % 2) ? GPIO_LOW : GPIO_HIGH);
        i++;
    });
}

"""

def main(args):
    path = args.path
    app_name = os.path.basename(path)

    generate_dir(path)
    generate_file(os.path.join(path, 'application.yaml'),
                  APPLICATION_YAML, locals())
    generate_file(os.path.join(path, 'main.cpp'),
                  MAIN_CPP)
