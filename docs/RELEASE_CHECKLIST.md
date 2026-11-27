# Release checklist

## Done
- [x] CLI with input validation and safe defaults
- [x] Responsive browser app with ZIP export
- [x] `.gitignore` rules for local image inputs/outputs and virtual environments
- [x] README covering both the browser app and the CLI
- [x] Unit tests and CI workflow (`.github/workflows/tests.yml`)
- [x] GitHub Pages deployment (`.github/workflows/deploy-pages.yml`) with a live demo
- [x] README screenshot (`docs/screenshot.png`)
- [x] Optional Jenkins pipeline (`Jenkinsfile`)
- [x] MIT license

## Manual test matrix (before each release)
- [ ] Open `web/index.html` in Chrome, Firefox and Safari
- [ ] Try PNG with transparency, JPEG, WebP, large photographs, corrupt files and duplicate file names
- [ ] Verify ZIP extraction in Windows Explorer and macOS Finder
- [ ] Run `python -m unittest discover -s tests -v`
- [ ] Run the CLI on copies of representative real-world images

## Roadmap
- Drag-to-reorder and per-image settings
- Before/after comparison slider
- Off-main-thread (Web Worker) processing for very large batches
- A browser extension, only if there is clear demand for right-click or in-page workflows
