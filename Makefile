.PHONY: build test

# for test
export MAKESTACK_SERVER_URL = http://localhost:31313
export MAKESTACK_USERNAME   = luke
export MAKESTACK_PASSWORD   = 12345678
export MAKESTACK_CONFIG_DIR = tmp/test/config

pyinstaller:
	git clone --depth 1 https://github.com/pyinstaller/pyinstaller
	cd pyinstaller && python3 setup.py install

server:
	git clone https://github.com/makestack/server
	cd server
	bundle install --jobs 2
	bundle exec rails db:migrate

build: pyinstaller
	pyinstaller --name=makestack --onefile makestack/__main__.py

test: server
	PYTHONPATH=. py.test

$(VERBOSE).SILENT:
