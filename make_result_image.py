"""results.txt -> results.png (есепке салатын терминал скриншоты)."""
from PIL import Image, ImageDraw, ImageFont


def mono(size):
    for name in ("consola.ttf", "cour.ttf", "DejaVuSansMono.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


lines = open("results.txt", encoding="utf-8-sig").read().splitlines()
font = mono(18)
line_h = 24
width = 820
img = Image.new("RGB", (width, 40 + line_h * (len(lines) + 2)), (30, 30, 30))
draw = ImageDraw.Draw(img)
draw.text((16, 12), "> python medicine_ocr.py medicine.jpg ... medicine_5.jpg", fill=(120, 200, 255), font=font)
y = 12 + line_h * 2
colors = {"EXPIRED": (255, 100, 100), "NOT EXPIRED": (110, 220, 110), "EXPIRING SOON": (255, 200, 80)}
for line in lines:
    color = colors.get(line.strip(), (225, 225, 225))
    draw.text((16, y), line, fill=color, font=font)
    y += line_h
img.save("results.png")
print("saved results.png", img.size)
