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
	cp test/database.yml server/config/database.yml
	cd server
	psql postgres -c "create role makestack_cli with createdb login password '12345678'"
	bundle install --jobs 2
	bundle exec rails db:setup

tmp/postgres:
	mkdir -p $@
	initdb $@

build: pyinstaller
	pyinstaller --name=makestack --onefile makestack/__main__.py

test: server tmp/postgres
	PYTHONPATH=. py.test $(TARGETS)

$(VERBOSE).SILENT:
