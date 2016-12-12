.PHONY: build setup server test

# for test
TARGETS ?= test
export MAKESTACK_SERVER_URL = http://localhost:31313
export MAKESTACK_USERNAME   = luke
export MAKESTACK_PASSWORD   = 12345678
export MAKESTACK_CONFIG_DIR = tmp/test/config

pyinstaller:
	git clone --depth 1 https://github.com/pyinstaller/pyinstaller
	cd pyinstaller && python3 setup.py install

setup:
	git clone https://github.com/makestack/server
	cp test/database.yml server/config/database.yml
	mkdir -p tmp/postgres
	initdb tmp/postgres
	gem install foreman
	cd server && bundle install --jobs 2 --without mysql sqlite3

init:
	psql postgres -c "create role makestack_cli with createdb login password '12345678'"
	cd server && RAILS_ENV=development bundle exec rails db:setup

server:
	foreman start -d $(PWD) -f test/Procfile

build: pyinstaller
	pyinstaller --name=makestack --onefile makestack/__main__.py

test:
	PYTHONPATH=. py.test $(TARGETS)

ci-test:
	PYTHONPATH=. py.test --cov=makestack $(TARGETS)

$(VERBOSE).SILENT:
