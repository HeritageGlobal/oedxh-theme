.PHONY: build build-tokens build-scss copy-assets validate clean

build: build-tokens build-scss copy-assets validate

build-tokens:
	npx paragon build-tokens --source ./paragon/tokens --build-dir ./paragon/build --themes light

build-scss:
	mkdir -p dist
	npx paragon build-scss --corePath ./paragon/core.scss --themesPath ./paragon/build/themes --outDir ./dist --defaultThemeVariants light

copy-assets:
	mkdir -p dist/paragon/images
	cp logo.svg logo-trademark.svg logo-white.svg favicon.ico dist/
	cp paragon/images/card-imagecap-fallback.png dist/paragon/images/

# Cheap sanity check, not a substitute for testing against real MFEs
# (see docs/RELEASE-CHECKLIST.md): confirms every generated CSS file has
# balanced braces and that the font-family fix documented in
# docs/TOKEN-MAP.md hasn't regressed (no orphaned default Paragon font
# names bleeding through a partially-overridden array token -- see
# docs/TOKEN-MAP.md "Array token overrides" for why this can happen).
validate:
	@for f in dist/core.css dist/light.css; do \
		open=$$(grep -o '{' $$f | wc -l); \
		close=$$(grep -o '}' $$f | wc -l); \
		if [ "$$open" != "$$close" ]; then \
			echo "FAIL: $$f has unbalanced braces ($$open open, $$close close)"; exit 1; \
		fi; \
	done
	@if grep -q "Apple Color Emoji" dist/core.css && ! grep -q "Jost.*Apple Color Emoji" dist/core.css; then \
		echo "FAIL: dist/core.css has default Paragon sans-serif fallback fonts without the Jost brand font -- array override may have regressed, see docs/TOKEN-MAP.md"; exit 1; \
	fi
	@echo "validate: OK"

clean:
	rm -rf dist paragon/build
