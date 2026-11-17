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
Unknown selectors and dynamic states are retained. Original priorities remain in their original order. No new `!important` is added.
A trial that moved priorities to cascade layers was rejected after comparative
screenshots showed shifted 1px borders. Layers are therefore not activated in this
lot. Family bundles, ordered entry manifests and explicit tokens provide isolation
without changing priority semantics. Remaining legacy priorities are visible debt,
not hidden behind a replacement priority mechanism.

No old CSS file is deleted. Do not edit generated `public/assets/css/*` or generated
HTML. Do not change tokens to new visual values during lot 1.

`chapters.json` records the approved five-chapter target and transition invariants.
It is a contract only: photographic compatibility rules remain inactive/active
exactly as audited. Their visual removal and transitions require lot 2 approval.

`python scripts/build.py --output-dir /tmp/ski-clean` builds into an empty directory.
Static legacy inputs still live in public/ and are frozen, hash-protected sources.
