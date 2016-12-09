.PHONY: build test

pyinstaller:
	git clone --depth 1 https://github.com/pyinstaller/pyinstaller
	cd pyinstaller && python3 setup.py install && cd ..

build: pyinstaller
	pyinstaller --name=makestack --onefile makestack/__main__.py

test:
	PYTHONPATH=. py.test

$(VERBOSE).SILENT:
