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

## Files

- `poster_tailwind.html` - main Tailwind/CDN poster source.
- `SWNet_tailwind_poster_ratio.pdf` - final PDF export using the poster's natural printed ratio.
- `SWNet_research_poster.pdf` - earlier ReportLab-generated poster version.
- `extracted_images/` - full-quality figures extracted from the source PDF.
- `s12911-025-02889-w.pdf` - source paper.
- `s12911-025-02889-w.txt` - extracted paper text.
- `create_research_poster.py` - earlier Python/ReportLab poster generator.

## Export PDF

On macOS with Google Chrome installed:

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless \
  --disable-gpu \
  --no-pdf-header-footer \
  --print-to-pdf="$PWD/SWNet_tailwind_poster_ratio.pdf" \
  "file://$PWD/poster_tailwind.html"
```

The checked-in `SWNet_tailwind_poster_ratio.pdf` was exported as a single-page PDF sized to the artwork ratio to avoid large empty page margins.

## Notes

The original paper is open access under a Creative Commons Attribution 4.0 International License. The extracted figures are included for academic poster/assignment use with attribution to the original article.

