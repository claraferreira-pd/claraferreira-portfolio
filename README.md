# Clara Ferreira — Portfolio

Personal portfolio of Clara Ferreira, Product Designer (fintech, payments and SaaS).

The site is a single self-contained `index.html`: Home, About and the Subscription Management case study, which includes a live, clickable prototype of the billing console. Names and figures inside the prototype are fictional.

## Structure

```
index.html                  built site (open it in a browser, or serve it with GitHub Pages)
scripts/build.py            builds index.html from src/
src/template.html           Home, About, footer, styles and page logic
src/case-billing.html       Subscription Management case study
src/case-billing.css        case study styles
src/prototype/              interactive billing console embedded in the case study
src/img/, src/assets/       photos, screenshots and company logos
```

## Editing

1. Change files in `src/`.
2. Run `python3 scripts/build.py` (Python 3.8+, no dependencies).
3. Commit both your `src/` changes and the rebuilt `index.html`.

## Publishing with GitHub Pages

Settings → Pages → Deploy from a branch → `main` / root. The site is served from `index.html`.
