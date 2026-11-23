# Release and handoff checklist

## Included in this local handoff
- [x] CLI improvements and safer validation
- [x] Browser app with responsive layout and ZIP export
- [x] Git ignore rules for local image inputs/outputs and virtual environments
- [x] README rewritten to cover both interfaces
- [x] Unit tests and CI workflow
- [x] Optional Jenkins workflow maintained

## Owner verification before pushing
- [ ] Compare this review package with the latest GitHub checkout before replacing files (package was reconstructed from the publicly visible repository because direct clone access was unavailable)
- [ ] Open `web/index.html` in Chrome, Firefox, and Safari where practical
- [ ] Try PNG transparency, JPEG, WebP, large photographs, corrupt images, and duplicate filenames
- [ ] Verify ZIP extraction in Windows Explorer and macOS Finder
- [ ] Run `python -m unittest discover -s tests -v`
- [ ] Run the CLI on copies of representative real-world images
- [x] MIT license included; review copyright name before publishing
- [ ] Take a real screenshot for README (`docs/screenshot.png`) after browser QA
- [x] GitHub Pages deployment workflow included (`.github/workflows/deploy-pages.yml`)
- [ ] Enable **GitHub Actions** as the Pages source in repository Settings → Pages
- [ ] Run the workflow and verify the live site on the project subpath
- [ ] Add the live demo URL to README and GitHub repository About section
- [ ] Review diff, commit and push manually

## Future improvements, deliberately deferred
- Optional drag-to-reorder or per-image settings
- Before/after comparison slider
- Off-main-thread processing for huge batches
- Browser extension only if there is evidence of frequent right-click or in-page workflows
