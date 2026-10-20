# Xinyuan Zhou — Academic Homepage

Website: https://zxy6688.github.io/

A small Jekyll academic website derived from al-folio. About, Research, Projects, Honors and CV share the same layouts and content. No frontend framework is required.

## Update content

- `_data/academic.yml`: biography, papers, projects, affiliations, honors, service and news. News uses `paper_id` to reuse the real paper title and link.
- `_data/socials.yml`: email and GitHub username.
- `_pages/`: five pages and the 404 page.
- `_layouts/academic*.liquid` and `_includes/academic/`: shared presentation.
- `assets/css/academic.css`: all website styles.
- `assets/img/prof_pic.jpg`: original portrait; do not replace or alter it. The three original figures are in `assets/img/research/`.
- `/cv/`: complete HTML CV with print styles; use Print to save a PDF.

Keep submission statuses and confirmed dates accurate. The entrance appears once per tab, with keyboard, touch and reduced-motion support.

## Build and check

Use Ruby 3.3 and the committed dependency lockfile:

```sh
bundle install
JEKYLL_ENV=production bundle exec jekyll build
npm ci
npx prettier . --check
bundle exec jekyll serve
```

Check the five pages, images, links, entrance and mobile layout before publishing. Screenshots, logs and reference material belong outside this repository.

## Deployment and recovery

Two branches are required:

- `main`: editable website source.
- `gh-pages`: generated live site. **Do not delete this branch when cleaning old development branches.**

Pull requests run the production build, internal-link check and formatting check. A merge into `main` publishes to `gh-pages`; GitHub Pages then deploys it. In repository Settings → Pages, use **Deploy from a branch → gh-pages → / (root)**.

If the publish branch is accidentally deleted, run Actions → Deploy site → Run workflow on `main`. Once `gh-pages` exists again, restore the Pages source above and wait for the Pages deployment to finish. Verify the public URL rather than relying only on a successful build.

Merged feature branches may be deleted. Git history retains previous versions; no force-push is needed.
