"""Тест үшін дәрі қаптамасының суреттерін жасайды (EXP: MM/YYYY)."""
from PIL import Image, ImageDraw, ImageFont

SAMPLES = {
    "medicine.jpg": ["PARACETAMOL 500 mg", "LOT B99414", "MFG: 03/2024", "EXP: 05/2025"],
    "medicine_2.jpg": ["IBUPROFEN 200 mg", "LOT A12345", "MFG: 12/2024", "EXP: 12/2026"],
    "medicine_3.jpg": ["AMOXICILLIN 250 mg", "LOT C77881", "MFG: 08/2025", "EXP: 08/2027"],
    # PDF-тегі мысал сияқты YYYY-MM-DD форматы
    "medicine_4.jpg": ["(01) 00307663074806", "EXP 2026-10-28", "LOT B99414"],
    # мерзіміне 30 күннен аз қалған -> EXPIRING SOON
    "medicine_5.jpg": ["ASPIRIN 100 mg", "LOT D55012", "MFG: 11/2024", "EXP: 11/2026"],
}


def load_font(size):
    for name in ("arialbd.ttf", "arial.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def make(path, lines):
    img = Image.new("RGB", (900, 420), (245, 242, 230))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 900, 70], fill=(60, 70, 160))
    font = load_font(48)
    y = 100
    for line in lines:
        draw.text((60, y), line, fill=(20, 20, 20), font=font)
        y += 75
    img.save(path, quality=95)
    print("saved", path)


if __name__ == "__main__":
    for file_name, text_lines in SAMPLES.items():
        make(file_name, text_lines)
