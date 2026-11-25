# The Calculus Notebook · Lesson 01

An English undergraduate mathematics learning unit based on the supplied revised content master.

The site is buildless HTML, CSS, and browser JavaScript. All fonts, lesson content, mathematical markup, and SVG diagrams are served locally. No external library or account integration is required for the learning interactions.

## Contents

- Complete mathematical exposition, with optional derivations.
- Twenty-one topic boards with investigations, derivations, and connections to later calculus.
- Ten main problems and two further explorations, each with strategy hints, complete solutions, and a self-review rubric.
- A trigonometric identity reference, source map, and a downloadable text of the lesson.
- Browser-local writing spaces; these do not claim to grade open-ended proofs.

## Build and verify

The checked-in `dist/` directory is ready to serve as a static website. After extracting the ZIP, run `python3 -m http.server 8000 --directory dist` from the extracted folder, then open [http://localhost:8000](http://localhost:8000). To publish to a static host, use `dist/` as the publish directory.

To regenerate content from `source/content-master.md`, run `npm run build`. This requires Python and Pandoc. The generators emit native MathML and preserves the mathematical content of the master, while keeping the internal build specification out of the lesson.

Run `node --test scripts/math.test.mjs` for the domain, branch, coefficient, singular-input, and periodic-model checks. The interactive functions are in `dist/math.js`; presentation and controls are in `dist/labs.js`; navigation and practice are in `dist/app.js`.

Font licence information is retained alongside the fonts in `dist/assets/`.
