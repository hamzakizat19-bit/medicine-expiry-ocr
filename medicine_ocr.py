"""
Lab 12 — «Дәрінің жарамдылық мерзімін анықтау»
EasyOCR көмегімен дәрі қаптамасынан жарамдылық мерзімін оқып,
бүгінгі күнмен салыстырады.

Іске қосу:
    python medicine_ocr.py                     -> medicine.jpg тексереді
    python medicine_ocr.py a.jpg b.jpg c.jpg   -> бірнеше суретті тексереді
"""
import re
import sys
import calendar
from datetime import date

import easyocr

SOON_DAYS = 30  # мерзіміне 30 күн қалса -> EXPIRING SOON

# MM/YYYY (05/2025, 05-2025, 05.2025)
MM_YYYY = re.compile(r'\b(0[1-9]|1[0-2])\s*[/.\-]\s*(20\d{2})\b')
# YYYY-MM-DD (2026-10-28) — мысал суреттегідей формат
YYYY_MM_DD = re.compile(r'\b(20\d{2})\s*[-/.]\s*(0[1-9]|1[0-2])\s*[-/.]\s*(0[1-9]|[12]\d|3[01])\b')
# EXP / EXPIRY / USE BY сөзінен кейінгі мәтін
EXP_WORD = re.compile(r'(EXP\w*|USE\s*BY|BEST\s*BEFORE)', re.IGNORECASE)


def find_date(text):
    """Мәтіннен бірінші күнді табады -> datetime.date немесе None."""
    m = YYYY_MM_DD.search(text)
    if m:
        y, mo, d = map(int, m.groups())
        return date(y, mo, d)
    m = MM_YYYY.search(text)
    if m:
        mo, y = int(m.group(1)), int(m.group(2))
        last_day = calendar.monthrange(y, mo)[1]  # айдың соңғы күні
        return date(y, mo, last_day)
    return None


def extract_expiry(texts):
    """Алдымен EXP сөзінен кейінгі күнді іздейді (MFG күнімен шатастырмау үшін),
    таппаса — барлық мәтіндегі бірінші күнді алады."""
    full_text = " ".join(texts)
    exp = EXP_WORD.search(full_text)
    if exp:
        found = find_date(full_text[exp.end():])
        if found:
            return found
    return find_date(full_text)


def check_status(expiry, today=None):
    today = today or date.today()
    days_left = (expiry - today).days
    if days_left < 0:
        return "EXPIRED", "Мерзімі өтіп кеткен", days_left
    if days_left <= SOON_DAYS:
        return "EXPIRING SOON", "Мерзімі жақында бітеді", days_left
    return "NOT EXPIRED", "Мерзімі өтпеген", days_left


def check_image(reader, image_path):
    texts = reader.readtext(image_path, detail=0)

    print("=" * 45)
    print("Image:", image_path)
    print("Recognized text:")
    for text in texts:
        print("  ", text)

    expiry = extract_expiry(texts)
    if expiry is None:
        print("\nExpiration date not found! / Жарамдылық мерзімі табылмады!")
        return None

    today = date.today()
    status, status_kz, days_left = check_status(expiry, today)

    print("\nToday:", today)
    print("Expiration date:", expiry)
    print(status)
    print("Нәтиже:", status_kz)
    if days_left >= 0:
        print(f"Мерзімнің аяқталуына {days_left} күн қалды")
    else:
        print(f"Мерзімі {-days_left} күн бұрын өтіп кеткен")
    return status


def main():
    images = sys.argv[1:] or ["medicine.jpg"]
    # Step 1: Load OCR model
    reader = easyocr.Reader(['en'], gpu=False)
    for path in images:
        check_image(reader, path)


if __name__ == "__main__":
    main()
