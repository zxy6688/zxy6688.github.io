This refresh replaces the template-heavy landing page with a restrained English academic homepage, using the owner's final v2 specification and preserving the original portrait unchanged. It retains Jekyll/al-folio and the existing deployment workflow. **Review only: do not merge or deploy without the owner's approval.**

## Implementation

- `_data/academic.yml` is the shared content source for Home, Honors, and the print-friendly English CV. It includes the frozen biography, six research areas, exactly three preprints, affiliations, programs, awards, service, and five news items.
- `_layouts/academic*.liquid` and `_includes/academic/` render a lightweight, accessible layout; `assets/css/academic.css` provides a 968px content column, restrained blue links, fine rules, consistent typography, and responsive reflow.
- Original `assets/img/prof_pic.jpg` is reused directly. Its SHA-256 is unchanged; no face crop, image editing, or generated substitute. See [asset provenance](ASSETS.md).
- Three original arXiv figures are displayed at a consistent 8:5 ratio with `object-fit: contain`. Author lists are complete, with Xinyuan Zhou bolded in the second, third, and sixth positions.
- Template pages/collections and remote demo posts are excluded from generated output; source history is retained. Actual output HTML routes are only Home, Honors, CV, and 404. Placeholder social accounts and example CV links are removed.
- No dependency upgrade, framework migration, production branch update, deployment change, or fabricated Scholar URL. The existing example PDF is replaced in navigation by a real HTML CV generated from the verified content.

## Repository audit

- Starting commit: `ad15609f47476809d3604d9aa3ae814c70282b03`.
- Existing theme: al-folio source tree; Docker configuration documents v0.16.3. The repository has no theme release tag, so this is not claimed as a verified exact theme revision.
- Jekyll: **4.4.1**, pinned in the existing `Gemfile.lock`; CI Ruby: **3.3.5**. Local validation used Ruby **3.3.8**, Bundler **4.0.4**, and the unchanged dependency lock.
- Original homepage: `_pages/about.md` → `_layouts/about.liquid`; portrait: `profile.image: prof_pic.jpg`.
- Original publications: `_bibliography/papers.bib` (Einstein examples); news: `_news/announcement_*.md` (template examples). The new visible content is in `_data/academic.yml`.
- `.github/workflows/deploy.yml` builds PRs with `JEKYLL_ENV=production bundle exec jekyll build`, then PurgeCSS. Its deploy step excludes `pull_request` events and deploys `_site` to `gh-pages` only on the existing non-PR path. This workflow was not changed.

## Visual comparison

Both reference and existing sites were actually opened in Chrome at desktop and mobile widths before editing. The reference's entry overlay was dismissed to inspect the page. Captures include the biography, affiliations, news, publications, and footer.

Visible design choices carried forward:

1. Generous outer margins and an orderly central reading column.
2. A compact identity/photo introduction with clear typographic hierarchy.
3. Fine gray rules and vertical whitespace separating research and experience.
4. Repeated left-image/right-text publication rows and small text links.
5. Compact affiliations and date-led news rows.
6. Minimal decoration and natural mobile text wrapping.

Differences required by the owner's specification: right-aligned original portrait on desktop; a sans-serif hierarchy; no entry overlay; no three-layer research framework; publications before affiliations; three separately stated municipal Special Prizes; a normal-flow footer that does not cover text. On phones the portrait and biography stack, as do publication images and text; navigation wraps into its own row.

| Evidence         | Desktop                                                                                           | Mobile                                                                                                             |
| ---------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Reference        | [Full page](screenshots/reference-desktop.png)                                                    | [Full page](screenshots/reference-mobile.png), [top](screenshots/reference-mobile-top.png)                         |
| Original         | [Full page](screenshots/original-desktop.png)                                                     | [Full page](screenshots/original-mobile.png), [top](screenshots/original-mobile-top.png)                           |
| New homepage     | [1440px](screenshots/new-1440-full.png), [hero](screenshots/new-1440-hero.png)                    | [390px](screenshots/new-390-full.png), [375px](screenshots/new-375-full.png), [hero](screenshots/new-390-hero.png) |
| New publications | [Desktop](screenshots/new-1440-research.png)                                                      | [Mobile](screenshots/new-390-research.png)                                                                         |
| New honors       | [Homepage section](screenshots/new-1440-honors.png), [complete page](screenshots/honors-1440.png) | [Complete page](screenshots/honors-390.png)                                                                        |
| Tablet           | [768px](screenshots/new-768-full.png)                                                             | —                                                                                                                  |
| English CV       | [Desktop](screenshots/cv-1440.png)                                                                | [Mobile](screenshots/cv-390.png)                                                                                   |

## Validation

- **PASS**: `npx prettier . --check` and `git diff --check`. The repository-wide formatter required two pre-existing, format-only cleanups in `CUSTOMIZE.md` and `_includes/head.liquid`; neither changes the new page behavior. See [format check](format-check.log).
- **PASS**: production Jekyll build with the existing Gemfile and lockfile. See [build log](build.log). An initial attempt exposed an unused template notebook requiring local nbconvert; demo notebooks, HTML, and Plotly examples were excluded from output as part of template cleanup. No dependency or deployment rewrite was needed.
- **PASS**: PurgeCSS with the repository configuration, processing 13 stylesheets. The Windows CLI had an ESM drive-path issue; the same package's API was used with `require('./purgecss.config.js')` and its outputs written to the configured directory. Browser verification was repeated after purging.
- **PASS**: [browser verification](verification.json), run with `python docs/homepage-refresh/verify.py` against the actual `_site` output at 1440×900, 768×1024, 390×844, and 375×812. No horizontal overflow, broken images, or page errors. Local navigation, research anchor, mailto, keyboard skip link, full author lists, three paper entries, and portrait proportions passed.
- Six public arXiv/PDF endpoints returned HTTP 200. GitHub profile and repository existence were verified through GitHub API responses (HTTP 200); direct webpage HEAD attempts timed out. Details are recorded in [external link checks](external-links.json). The public reading-notes repository was also successfully accessed via the web tool. Mailto points to the owner's existing public address; mailbox deliverability was not tested.
- No automated test can replace the owner's final visual/content approval. Screenshots are provided for that review.

## Acceptance checklist

- [x] Existing repository, data sources, version evidence, and deployment path recorded above; original screenshots retained.
- [x] Reference, original, and new desktop/mobile screenshots attached, including publication layouts.
- [x] Correct identity, school, unchanged portrait, three biography paragraphs, and exact six research directions; no welcome barrier.
- [x] Exactly three preprints; titles and author order verified on the linked arXiv records. CHI submission labels follow the owner's specification and do not claim acceptance. SLATE targets COLING 2027 without claiming active COLING review.
- [x] Tsinghua **Institute for Network Sciences and Cyberspace**, BNU × USTC, and BNU security internship displayed as three compact entries.
- [x] Zeng Xianzi program and mentor; FinPilot **Mar 2026–May 2027, Ongoing**; technology-anxiety project **Mar 2024–May 2025, Completed; Outstanding Project Completion**.
- [x] Three independent 2025 Beijing Municipal Special Prizes; 2025 Beijing Regional innovation First Prize; 2026 Beijing innovation First Prize; **2026 municipal Challenge Cup Main Track Third Prize**. Complete remaining honors are on Honors and CV.
- [x] Service roles use confirmed dates, including Class President **Sep 2025–Oct 2026**; no “Former” label.
- [x] No template publications, blog/books/teaching pages, example identities, or placeholder navigation in generated HTML.
- [x] Real contact address; real CV route; no fabricated PDF, Scholar, or code link. Local links verified; external evidence attached.
- [x] Desktop, tablet, and both phone widths checked; images and long titles/authors reflow correctly.
- [x] Actual production build completed; browser verification covers the generated and purged output.
- [x] Independent branch with review evidence. No merge or production deployment performed.

## Items for owner review

- Approve the visual result and print-friendly English CV. No genuine existing PDF CV or verified Scholar profile was found; those downloadable/profile links are intentionally absent.
- Publication submission states are reproduced from the final v2 specification. Confirm only if there has been a newer decision; no active COLING review or acceptance is inferred.
- All three Special Prizes remain stated as confirmed by the owner. Additional certificate links for the two AI Applications prizes are optional follow-up; none are invented. Additional campus gold awards are not aggregated without corroboration.
- Project descriptions were shortened from the specification/existing real homepage without adding results, numbers, funding, or new appointments. The optional future IJHCI sentence was omitted to keep attention on public work.
