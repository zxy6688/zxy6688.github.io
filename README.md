# Xinyuan Zhou — Academic Homepage

Personal academic website: https://zxy6688.github.io/

Built with the existing Jekyll / al-folio setup. Home, Honors, and CV share one content source; no frontend framework or JavaScript is needed for these pages.

## Maintaining the website

- Edit `_data/academic.yml` for the biography, research interests, three preprints, affiliations, projects, awards, service, and news. All three pages update together.
- Edit `_data/socials.yml` for the public email address and GitHub username.
- Keep the original portrait at `assets/img/prof_pic.jpg` unchanged. The three original paper figures are in `assets/img/research/`; source URLs are recorded next to their entries in the content data.
- Page entries live in `_pages/`; `academic*.liquid` layouts and `_includes/academic/` provide the shared presentation. Styles are in `assets/css/academic.css`.
- `/cv/` is an English HTML CV with print styles. Use the browser's Print command to save it as a PDF. No placeholder CV or Scholar profile is linked.

## Build and deploy

Use the repository's existing Ruby dependencies and lockfile:

```sh
bundle install
JEKYLL_ENV=production bundle exec jekyll build
npm ci
npx prettier . --check
```

The existing Docker Compose setup is also available. GitHub Actions runs the production build and CSS cleanup. Pull requests are checked without deployment; merging into `main` publishes the generated site through `gh-pages` and GitHub Pages.

Keep development screenshots, logs, reference websites, and temporary reports outside this repository. Preserve accurate preprint/submission labels and confirmed dates when updating content.
