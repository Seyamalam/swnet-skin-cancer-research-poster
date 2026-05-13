from pathlib import Path

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parent
IMG = ROOT / "extracted_images"
OUT = ROOT / "SWNet_research_poster.pdf"

PAGE_W, PAGE_H = 24 * inch, 36 * inch
M = 0.62 * inch
G = 0.28 * inch

INK = colors.HexColor("#14213D")
MUTED = colors.HexColor("#536271")
TEAL = colors.HexColor("#008C95")
GREEN = colors.HexColor("#2A9D55")
CORAL = colors.HexColor("#D95D39")
GOLD = colors.HexColor("#E9B44C")
BLUE = colors.HexColor("#355C7D")
PALE = colors.HexColor("#F5F8FA")
LINE = colors.HexColor("#D8E2E8")
WHITE = colors.white


FIGS = {
    "dataset": IMG / "page-06_image-01_aba2f6863522097b.png",
    "transfer": IMG / "page-07_image-01_d76881a5220a615b.jpg",
    "pipeline": IMG / "page-08_image-01_a352bb8b094c358e.jpg",
    "train": IMG / "page-09_image-01_b1fb12060a6afb39.jpg",
    "arch": IMG / "page-11_image-01_a15079069023c922.jpg",
    "features": IMG / "page-12_image-01_6f60ff2f4b44973c.jpg",
    "fusion": IMG / "page-12_image-02_172f69a7fb90266b.png",
    "gradcam": IMG / "page-13_image-01_7a5960687ec09049.jpg",
    "cm": IMG / "page-14_image-01_b5e4d364995fa511.jpg",
    "curve": IMG / "page-15_image-01_da630bdaafd588f1.jpg",
    "pred": IMG / "page-16_image-01_2e769929fb5f4742.jpg",
    "bias": IMG / "page-17_image-01_1be6d351e2f1c9ce.jpg",
    "fair": IMG / "page-19_image-01_c9c2270f942c9bfc.jpg",
    "hair": IMG / "page-20_image-01_f493469a9f926940.jpg",
}


ABSTRACT = (
    "This paper introduces SkinWiseNet (SWNet), a deep convolutional neural network designed for the detection "
    "and automatic classification of potentially malignant skin cancer conditions. SWNet optimizes feature extraction "
    "through multiple pathways, emphasizing network width augmentation to enhance efficiency. The proposed model "
    "addresses potential biases associated with skin conditions, particularly in individuals with darker skin tones or excessive "
    "hair, by incorporating feature fusion to assimilate insights from diverse datasets. Extensive experiments were "
    "conducted using publicly accessible datasets to evaluate SWNet's effectiveness. This study utilized four datasets-"
    "Mnist-HAM10000, ISIC2019, ISIC2020, and Melanoma Skin Cancer-comprising skin cancer images categorized into benign "
    "and malignant classes. Explainable Artificial Intelligence (XAI) techniques, specifically Grad-CAM, were employed "
    "to enhance the interpretability of the model's decisions. Comparative analysis was performed with three pre-existing "
    "deep learning networks-EfficientNet, MobileNet, and Darknet. The results demonstrate SWNet's superiority, achieving "
    "an accuracy of 99.86% and an F1 score of 99.95%, underscoring its efficacy in gradient propagation and feature "
    "capture across various levels. This research highlights the significant potential of SWNet in advancing skin cancer "
    "detection and classification, providing a robust tool for accurate and early diagnosis. The integration of feature fusion "
    "enhances accuracy and mitigates biases associated with hair and skin tones. The outcomes of this study contribute "
    "to improved patient outcomes and healthcare practices, showcasing SWNet's exceptional capabilities in skin cancer "
    "detection and classification."
)


def para(c, text, x, y, w, h, size=18, color=INK, leading=None, bold=False, align=0):
    style = ParagraphStyle(
        "p",
        fontName="Helvetica-Bold" if bold else "Helvetica",
        fontSize=size,
        leading=leading or size * 1.22,
        textColor=color,
        alignment=align,
        spaceAfter=0,
        spaceBefore=0,
    )
    p = Paragraph(text, style)
    _, used_h = p.wrap(w, h)
    p.drawOn(c, x, y + h - used_h)
    return used_h


def rounded(c, x, y, w, h, fill=WHITE, stroke=LINE, r=9, lw=1):
    c.setLineWidth(lw)
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.roundRect(x, y, w, h, r, stroke=1, fill=1)


def band(c, x, y, w, h, color, label):
    c.setFillColor(color)
    c.roundRect(x, y + h - 24, 124, 24, 7, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(x + 62, y + h - 17, label.upper())


def heading(c, text, x, y, w, color=INK):
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(x, y, text)
    c.setStrokeColor(color)
    c.setLineWidth(2)
    c.line(x, y - 7, x + min(w, 210), y - 7)


def image_fit(c, path, x, y, w, h, bg=WHITE, stroke=LINE, r=7, pad=8, caption=None):
    rounded(c, x, y, w, h, bg, stroke, r)
    im = Image.open(path)
    iw, ih = im.size
    max_w = w - 2 * pad
    max_h = h - 2 * pad - (22 if caption else 0)
    scale = min(max_w / iw, max_h / ih)
    dw, dh = iw * scale, ih * scale
    ix = x + (w - dw) / 2
    iy = y + pad + (max_h - dh) / 2 + (18 if caption else 0)
    c.drawImage(ImageReader(str(path)), ix, iy, dw, dh, preserveAspectRatio=True, mask="auto")
    if caption:
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 10)
        c.drawCentredString(x + w / 2, y + 8, caption)


def image_cover(c, path, x, y, w, h, bg=WHITE, stroke=LINE, r=7, pad=8, caption=None):
    rounded(c, x, y, w, h, bg, stroke, r)
    im = Image.open(path)
    iw, ih = im.size
    max_w = w - 2 * pad
    max_h = h - 2 * pad - (22 if caption else 0)
    scale = max(max_w / iw, max_h / ih)
    crop_w, crop_h = int(max_w / scale), int(max_h / scale)
    left = max(0, int((iw - crop_w) / 2))
    top = max(0, int((ih - crop_h) / 2))
    crop = im.crop((left, top, min(iw, left + crop_w), min(ih, top + crop_h)))
    c.drawImage(ImageReader(crop), x + pad, y + pad + (18 if caption else 0), max_w, max_h, preserveAspectRatio=False, mask="auto")
    if caption:
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 10)
        c.drawCentredString(x + w / 2, y + 8, caption)


def stat(c, x, y, w, h, value, label, color):
    rounded(c, x, y, w, h, colors.HexColor("#FFFFFF"), colors.HexColor("#DDE8ED"), 8)
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(x + w / 2, y + h * 0.48, value)
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(x + w / 2, y + 17, label.upper())


def pill(c, x, y, text, color):
    pad = 10
    w = stringWidth(text, "Helvetica-Bold", 10) + 2 * pad
    c.setFillColor(color)
    c.roundRect(x, y, w, 20, 10, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x + pad, y + 6, text)
    return w


def section(c, x, y, w, h, title, color=INK):
    rounded(c, x, y, w, h)
    heading(c, title, x + 14, y + h - 30, w - 28, color)


def bullets(c, items, x, y, w, size=10.5, leading=13, color=INK, dot=TEAL, gap=30):
    yy = y
    for item in items:
        c.setFillColor(dot)
        c.circle(x + 4, yy + leading - 7, 2.7, stroke=0, fill=1)
        used = para(c, item, x + 13, yy, w - 13, 0.55 * inch, size=size, color=color, leading=leading)
        yy -= max(gap, used + 7)
    return yy


def aspect_h(path, w, max_h=None):
    im = Image.open(path)
    iw, ih = im.size
    h = w * ih / iw
    return min(h, max_h) if max_h else h


def flow_card(c, x, top, w, h, title, color=INK):
    section(c, x, top - h, w, h, title, color)
    return top - h


def make():
    c = canvas.Canvas(str(OUT), pagesize=(PAGE_W, PAGE_H))
    c.setTitle("Towards unbiased skin cancer classification using deep feature fusion - Research Poster")

    c.setFillColor(colors.HexColor("#FBFCFD"))
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    header_h = 3.45 * inch
    c.setFillColor(INK)
    c.rect(0, PAGE_H - header_h, PAGE_W, header_h, stroke=0, fill=1)
    c.setFillColor(TEAL)
    c.rect(0, PAGE_H - header_h, PAGE_W, 0.16 * inch, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(PAGE_W * 0.69, PAGE_H - header_h, PAGE_W * 0.31, 0.16 * inch, stroke=0, fill=1)

    para(
        c,
        "Towards Unbiased Skin Cancer Classification<br/>Using Deep Feature Fusion",
        M,
        PAGE_H - 2.04 * inch,
        PAGE_W - 2 * M,
        1.38 * inch,
        size=40,
        color=WHITE,
        leading=44,
        bold=True,
    )
    para(
        c,
        "Ali Atshan Abdulredah | Mohammed A. Fadhel | Laith Alzubaidi | Ye Duan | Monji Kherallah | Faiza Charfi",
        M,
        PAGE_H - 2.67 * inch,
        PAGE_W - 2 * M,
        0.35 * inch,
        size=13.5,
        color=colors.HexColor("#DDEAF0"),
    )
    para(
        c,
        "BMC Medical Informatics and Decision Making (2025) 25:48 | DOI: 10.1186/s12911-025-02889-w",
        M,
        PAGE_H - 2.95 * inch,
        PAGE_W - 2 * M,
        0.25 * inch,
        size=11.5,
        color=colors.HexColor("#B9C9D3"),
    )
    x = M
    for txt, col in [
        ("SWNet CNN", TEAL),
        ("Feature fusion", GREEN),
        ("Grad-CAM XAI", CORAL),
        ("Bias mitigation", GOLD),
    ]:
        x += pill(c, x, PAGE_H - 3.18 * inch, txt, col) + 10

    top = PAGE_H - header_h - 0.35 * inch
    bottom = M

    # Abstract band
    abstract_h = 3.1 * inch
    rounded(c, M, top - abstract_h, PAGE_W - 2 * M, abstract_h)
    heading(c, "Abstract", M + 18, top - 38, PAGE_W - 2 * M - 36, TEAL)
    para(
        c,
        ABSTRACT,
        M + 18,
        top - abstract_h + 24,
        PAGE_W - 2 * M - 36,
        abstract_h - 78,
        size=12.2,
        color=INK,
        leading=15,
    )

    grid_top = top - abstract_h - G
    col_w = (PAGE_W - 2 * M - 2 * G) / 3
    x1 = M
    x2 = M + col_w + G
    x3 = M + 2 * (col_w + G)

    # Column 1: framing and setup
    y = grid_top
    h = 1.7 * inch
    section(c, x1, y - h, col_w, h, "Problem", TEAL)
    para(c, "Manual skin cancer screening is expert-dependent and can be affected by visual confounders such as skin tone, hair, imaging artifacts, and lesion variability. The study asks whether a widened CNN with feature fusion can improve classification while keeping predictions inspectable.", x1 + 14, y - h + 16, col_w - 28, h - 58, size=10.6, leading=13)

    y -= h + G
    h = 2.25 * inch
    section(c, x1, y - h, col_w, h, "Research Questions", BLUE)
    bullets(c, [
        "Can a custom CNN outperform EfficientNet, MobileNet, and Darknet for benign/malignant classification?",
        "Can multi-level feature fusion reduce shortcuts from artifacts, hair, and skin-tone variation?",
        "Can Grad-CAM make model attention transparent enough for clinical review?",
    ], x1 + 18, y - 76, col_w - 36, size=10.1, leading=12.5, dot=BLUE, gap=34)

    y -= h + G
    h = 2.75 * inch
    section(c, x1, y - h, col_w, h, "Contributions", GREEN)
    bullets(c, [
        "Built <b>SWNet</b>, a 113-layer CNN with width expansion and global average pooling.",
        "Added concatenation stages to fuse feature maps across multiple network levels.",
        "Benchmarked against EfficientNet, MobileNet, and Darknet.",
        "Used Grad-CAM XAI to visualize prediction evidence.",
        "Discussed feature fusion as a strategy for hair and skin-tone bias mitigation.",
    ], x1 + 18, y - 76, col_w - 36, size=9.8, leading=12.2, dot=GREEN, gap=29)

    y -= h + G
    text_h = 1.25 * inch
    img_h = aspect_h(FIGS["dataset"], col_w - 28)
    h = 58 + text_h + img_h + 44
    section(c, x1, y - h, col_w, h, "Datasets + Setup", CORAL)
    para(c, "<b>Datasets:</b> Mnist-HAM10000, ISIC2019, ISIC2019-2020, Melanoma Skin Cancer.<br/><b>Classes:</b> benign/malignant. <b>Input:</b> 224 x 224 RGB.<br/><b>Training:</b> SGD, lr=0.001, 100 epochs, 80/20 split, MATLAB R2023a.", x1 + 14, y - 130, col_w - 28, text_h, size=9.7, leading=12)
    image_fit(c, FIGS["dataset"], x1 + 14, y - h + 14, col_w - 28, img_h + 30, caption="Representative benign/malignant samples")

    y -= h + G
    h = y - bottom
    section(c, x1, bottom, col_w, h, "References + Source", INK)
    para(
        c,
        "<b>Primary paper:</b> Abdulredah AA, Fadhel MA, Alzubaidi L, Duan Y, Kherallah M, Charfi F. Towards unbiased skin cancer classification using deep feature fusion. <i>BMC Medical Informatics and Decision Making</i>. 2025;25:48.<br/><br/>"
        "<b>Selected cited works:</b><br/>"
        "[28] Tahir M et al. DSCC_Net: multi-classification deep learning models for diagnosing skin cancer using dermoscopic images. <i>Cancers</i>. 2023;15:2179.<br/>"
        "[30] Waheed S et al. Melanoma skin cancer classification based on CNN deep learning algorithms. <i>Malays J Fundam Appl Sci</i>. 2023;19:299-305.<br/>"
        "[31] Dahdouh Y et al. Deep learning and reinforcement learning in healthcare: skin cancer classification. <i>Int J Electr Comput Eng Syst</i>. 2023;14(5):557-564.<br/>"
        "[37] MobileNet: lightweight CNNs for mobile inference.<br/>[42] EfficientNet: compound scaling of CNN depth, width, and resolution.<br/>[43] Darknet: CNN family used in YOLO-style recognition.<br/>[54] Zhang H, Ogasawara K. Grad-CAM-based explainable AI for medical imaging.<br/><br/>"
        "<b>Data sources:</b> Kaggle HAM10000, ISIC2019, ISIC2019-2020 melanoma dataset, and Melanoma Skin Cancer dataset.",
        x1 + 14,
        bottom + 18,
        col_w - 28,
        h - 58,
        size=8.9,
        leading=11,
    )

    # Column 2: method and images with natural heights
    y = grid_top
    h = 1.55 * inch
    section(c, x2, y - h, col_w, h, "Method Summary", TEAL)
    para(c, "SWNet widens feature extraction through multiple convolutional pathways. Features are concatenated at stages, normalized with BN, activated with ReLU, globally pooled, regularized with dropout, and classified with Softmax.", x2 + 14, y - h + 16, col_w - 28, h - 58, size=10.4, leading=12.8)

    y -= h + G
    img_h = aspect_h(FIGS["arch"], col_w - 28, max_h=5.0 * inch)
    h = img_h + 58
    section(c, x2, y - h, col_w, h, "SWNet Architecture", GREEN)
    image_fit(c, FIGS["arch"], x2 + 14, y - h + 14, col_w - 28, img_h + 30, caption="Widened multi-path CNN")

    y -= h + G
    img_h = aspect_h(FIGS["pipeline"], col_w - 28, max_h=4.25 * inch)
    h = img_h + 58
    section(c, x2, y - h, col_w, h, "Classification Pipeline", BLUE)
    image_fit(c, FIGS["pipeline"], x2 + 14, y - h + 14, col_w - 28, img_h + 30, caption="Preprocess, train, classify, evaluate")

    y -= h + G
    img_h = aspect_h(FIGS["fusion"], col_w - 28, max_h=1.85 * inch)
    h = img_h + 1.15 * inch + 58
    section(c, x2, y - h, col_w, h, "Feature Fusion + XAI", CORAL)
    image_fit(c, FIGS["fusion"], x2 + 14, y - h + h - img_h - 56, col_w - 28, img_h + 30, caption="Fusion structure")
    para(c, "Feature fusion combines information from multiple sources and model levels to reduce overfitting and expose the classifier to broader lesion variation. Grad-CAM highlights the regions that most influence each predicted class.", x2 + 14, y - h + 16, col_w - 28, 0.82 * inch, size=9.8, leading=12)

    y -= h + G
    img_h = aspect_h(FIGS["gradcam"], col_w - 28, max_h=3.5 * inch)
    h = img_h + 58
    section(c, x2, y - h, col_w, h, "Grad-CAM Explanations", INK)
    image_fit(c, FIGS["gradcam"], x2 + 14, y - h + 14, col_w - 28, img_h + 30, caption="Model attention across selected layers")

    y -= h + G
    h = y - bottom
    section(c, x2, bottom, col_w, h, "Architecture Details", INK)
    bullets(c, [
        "Input layer crops/resizes images to 224 x 224 x 3.",
        "Thirty-three 3 x 3 convolution layers; 9,368,192 convolution kernels.",
        "Batch normalization between convolution and ReLU layers.",
        "Four concatenation blocks merge parallel feature streams.",
        "Global average pooling plus three fully connected layers.",
        "Dropout reduces overfitting before the final Softmax classifier.",
    ], x2 + 18, bottom + h - 76, col_w - 36, size=9.5, leading=11.8, dot=INK, gap=30)
    image_fit(c, FIGS["transfer"], x2 + 14, bottom + 16, col_w - 28, min(2.0 * inch, h - 265), caption="Transfer-learning baselines")

    # Column 3: results, bias, conclusion
    y = grid_top
    h = 1.95 * inch
    section(c, x3, y - h, col_w, h, "Headline Results", GREEN)
    stat_w = (col_w - 42) / 2
    stat(c, x3 + 14, y - 88, stat_w, 50, "99.86%", "Accuracy", TEAL)
    stat(c, x3 + 28 + stat_w, y - 88, stat_w, 50, "99.95%", "F1 score", GREEN)
    stat(c, x3 + 14, y - 146, stat_w, 50, "100%", "Precision", CORAL)
    stat(c, x3 + 28 + stat_w, y - 146, stat_w, 50, "20 ms", "Recognition", GOLD)
    para(c, "Peak result reported on the Melanoma Skin Cancer dataset.", x3 + 14, y - h + 12, col_w - 28, 0.2 * inch, size=8.8, color=MUTED, leading=10)

    y -= h + G
    h = 2.75 * inch
    section(c, x3, y - h, col_w, h, "Baseline + Robustness", BLUE)
    rows = [("Model", "Acc.", "F1"), ("EfficientNet", "91.88", "86.39"), ("MobileNet", "93.20", "92.23"), ("Darknet", "94.44", "92.17"), ("SWNet", "99.86", "99.95")]
    tx, ty = x3 + 14, y - 70
    widths = [col_w * 0.47, col_w * 0.21, col_w * 0.21]
    for ri, row in enumerate(rows):
        rh = 22
        c.setFillColor(INK if ri == 0 else (colors.HexColor("#EAF7F5") if row[0] == "SWNet" else WHITE))
        c.rect(tx, ty - ri * rh, sum(widths), rh, stroke=0, fill=1)
        c.setStrokeColor(LINE)
        c.rect(tx, ty - ri * rh, sum(widths), rh, stroke=1, fill=0)
        xx = tx
        for ci, val in enumerate(row):
            c.setFillColor(WHITE if ri == 0 else INK)
            c.setFont("Helvetica-Bold" if ri == 0 or row[0] == "SWNet" else "Helvetica", 9.4)
            c.drawString(xx + 6, ty - ri * rh + 7, val)
            xx += widths[ci]
    para(c, "<b>Cross-dataset caveat:</b> HAM10000 reaches 81.93% accuracy but only 43.79% F1; ISIC2019-2020 reaches 91.09% accuracy and 89.70% F1.", x3 + 14, y - h + 15, col_w - 28, 0.5 * inch, size=9.1, leading=11)

    y -= h + G
    img_h = 2.0 * inch
    h = img_h + 58
    section(c, x3, y - h, col_w, h, "Training Evidence", TEAL)
    image_fit(c, FIGS["cm"], x3 + 14, y - h + 14, (col_w - 38) / 2, img_h + 30, caption="Confusion matrix")
    image_fit(c, FIGS["curve"], x3 + 24 + (col_w - 38) / 2, y - h + 14, (col_w - 38) / 2, img_h + 30, caption="Training curves")

    y -= h + G
    img_h = aspect_h(FIGS["pred"], col_w - 28, max_h=3.05 * inch)
    h = img_h + 58
    section(c, x3, y - h, col_w, h, "Predictions + XAI", BLUE)
    image_fit(c, FIGS["pred"], x3 + 14, y - h + 14, col_w - 28, img_h + 30, caption="Predicted samples with explainable AI overlays")

    y -= h + G
    img_h = aspect_h(FIGS["hair"], col_w - 28, max_h=3.55 * inch)
    h = img_h + 1.25 * inch + 58
    section(c, x3, y - h, col_w, h, "Bias Mitigation", CORAL)
    para(c, "The study identifies risks from microscope artifacts, dark backgrounds, underrepresented skin types, and hair coverage. Feature fusion is framed as a way to broaden model exposure and reduce shortcut learning.", x3 + 14, y - h + h - 118, col_w - 28, 0.65 * inch, size=9.6, leading=11.8)
    image_fit(c, FIGS["hair"], x3 + 14, y - h + 14, col_w - 28, img_h + 30, caption="Hair-related bias challenge")

    y -= h + G
    h = y - bottom
    section(c, x3, bottom, col_w, h, "Limitations + Conclusion", GOLD)
    para(
        c,
        "<b>Limitations:</b> large image storage/processing cost; tuning complexity as datasets scale; dependence on preprocessing; low F1 on imbalanced datasets; need for real-world clinical validation.<br/><br/>"
        "<b>Future work:</b> use clinically collected datasets, improve underrepresented classes, test alternative architectures, optimize for real-time deployment, and run longitudinal evaluation.<br/><br/>"
        "<b>Conclusion:</b> SWNet is a promising architecture with strong reported performance on one dataset and useful XAI support, but its practical value depends on robust validation across broader, demographically balanced clinical data.",
        x3 + 14,
        bottom + 18,
        col_w - 28,
        h - 58,
        size=9.6,
        leading=12,
    )
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 9)
    c.drawString(M, 22, "Poster generated from the open-access article and extracted native PDF figures.")

    c.showPage()
    c.save()


if __name__ == "__main__":
    make()
    print(OUT)
