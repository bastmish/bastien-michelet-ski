# CSS foundations — lot 1

`design-tokens.json` is the authority for semantic palette, typography, spacing,
containers and responsive queries. `compat-*` colors, legacy type sizes and old
responsive conditions preserve the audited appearance; they are not additional
brand choices. Their later visual normalization belongs to lot 2.

`entries.json` declares source order per page family and explicit runtime classes.
Legacy `public/*.css` files remain immutable inputs for unmigrated rules. Extracted
modules here are the editable sources for the newer components; their old public
files remain archived and are no longer loaded by generated HTML.

`python scripts/build.py` renders HTML, then `scripts/css_build.py` compiles two
stylesheets per route: shared tokens and a content-hashed family bundle. No Node
framework or browser is needed for the build. Install `requirements-build.txt`.

The first extraction preserves the cascade exactly. The optimization step removes
only provably unreachable positive-class selectors and superseded declarations.
Unknown selectors and dynamic states are retained. A compatibility bridge preserves
old author priorities while avoiding new `!important` rules; it is not a declaration
that every historical priority has already been redesigned.

No old CSS file is deleted. Do not edit generated `public/assets/css/*` or generated
HTML. Do not change tokens to new visual values during lot 1.
