PKGNAME = llm_server
VERSION = $(shell python -c "import pkg_resources; print(pkg_resources.require('llm_server')[0].version)")
SOURCES = $(shell find $(PKGNAME) -not \( -name 'version.py' \) -name "*.py" -type f)


.PHONY: clean


clean:
	find . -name "*.pyi" -type f -delete
	find . -name "__pycache__" -type d -exec rm -rf "{}" \;
	rm -rf build .coverage

wheel: dist/$(PKGNAME)-$(VERSION)-py3-none-any.whl
dist/$(PKGNAME)-${VERSION}-py3-none-any.whl: $(SOURCES)
	pip wheel -w dist --no-deps .
