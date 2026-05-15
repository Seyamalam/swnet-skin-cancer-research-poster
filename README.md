# SWNet Skin Cancer Research Poster

High-quality research poster for:

**Towards unbiased skin cancer classification using deep feature fusion**  
Ali Atshan Abdulredah, Mohammed A. Fadhel, Laith Alzubaidi, Ye Duan, Monji Kherallah, and Faiza Charfi  
*BMC Medical Informatics and Decision Making* (2025) 25:48  
DOI: `10.1186/s12911-025-02889-w`

Created by **team Huntrix** as part of a Machine Learning assignment.

Team members:
- Touhidul Alam Seyam
- Shafiul Azam Mahin
- Afrin Sultana Niharika
- Chandnin Barua Jowthi

## GitHub Pages

This repository is GitHub Pages ready. The poster entry point is:

- `index.html`

After enabling Pages from the repository settings with source `main` / root, the poster will be available at:

```text
https://seyamalam.github.io/swnet-skin-cancer-research-poster/
```

## Files

- `index.html` - main Tailwind/CDN poster source.
- `assets/pdfs/SWNet_tailwind_poster_ratio.pdf` - final PDF export using the poster's natural printed ratio.
- `assets/pdfs/SWNet_research_poster.pdf` - earlier ReportLab-generated poster version.
- `assets/images/` - full-quality figures extracted from the source PDF.
- `assets/source/s12911-025-02889-w.pdf` - source paper.
- `assets/source/s12911-025-02889-w.txt` - extracted paper text.
- `assets/source/extracted_images_full_quality.zip` - zipped extracted images.
- `create_research_poster.py` - earlier Python/ReportLab poster generator.

## Export PDF

On macOS with Google Chrome installed:

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless \
  --disable-gpu \
  --no-pdf-header-footer \
  --print-to-pdf="$PWD/assets/pdfs/SWNet_tailwind_poster_ratio.pdf" \
  "file://$PWD/index.html"
```

The checked-in `assets/pdfs/SWNet_tailwind_poster_ratio.pdf` was exported as a single-page PDF sized to the artwork ratio to avoid large empty page margins.

Current poster export size: `130 x 130 in` as a single-page square PDF generated from `index.html`.

## Notes

The original paper is open access under a Creative Commons Attribution 4.0 International License. The extracted figures are included for academic poster/assignment use with attribution to the original article.
