# -*- coding: utf-8 -*-
"""The ownCloud Marketplace screenshot, drawn with PIL. No screen capture.

1400 x 700, the 2:1 shape the marketplace asks for. The chat text is the
real answer the assistant gave during the test on 2026-09-14, shortened to fit.
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'screenshots')
os.makedirs(OUT, exist_ok=True)

W, H = 1400, 700
BG = (246, 246, 247)
INK = (17, 17, 20)
GREY = (110, 112, 120)
LINE = (223, 225, 229)
NAVY = (4, 30, 66)          # ownCloud header
BLUE = (37, 99, 235)
BUBBLE = (241, 243, 247)
F = r'C:\Windows\Fonts'


def font(size, bold=False):
    return ImageFont.truetype(os.path.join(F, 'segoeuib.ttf' if bold else 'segoeui.ttf'), size)


def wrap(draw, text, fnt, width):
    lines, cur = [], ''
    for word in text.split(' '):
        test = (cur + ' ' + word).strip()
        if draw.textlength(test, font=fnt) <= width:
            cur = test
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, lh=None):
    lh = lh or int(fnt.size * 1.45)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


canvas = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(canvas)

# Headline
d.text((70, 52), 'Your ownCloud answers questions', font=font(44, True), fill=INK)
d.text((70, 112), 'The Asyntai assistant sits on every page and answers from your own content.', font=font(22), fill=GREY)

# Card: a slice of the ownCloud Files view with the chat open
CX, CY, CW, CH = 70, 176, 1260, 480
shadow = Image.new('RGBA', (CW + 80, CH + 80), (0, 0, 0, 0))
ImageDraw.Draw(shadow).rounded_rectangle([40, 48, CW + 40, CH + 48], 16, fill=(0, 0, 0, 55))
shadow = shadow.filter(ImageFilter.GaussianBlur(20))
canvas.paste(shadow, (CX - 40, CY - 40), shadow)

card = Image.new('RGB', (CW, CH), (255, 255, 255))
c = ImageDraw.Draw(card)

# ownCloud top bar
c.rectangle([0, 0, CW, 54], fill=NAVY)
c.text((22, 15), 'Files', font=font(20), fill=(255, 255, 255))
c.text((CW // 2 - 48, 15), 'ownCloud', font=font(20, True), fill=(255, 255, 255))
c.text((CW - 90, 17), 'admin', font=font(17), fill=(220, 226, 236))

# left navigation
c.rectangle([0, 54, 230, CH], fill=(250, 250, 250))
c.line([230, 54, 230, CH], fill=LINE, width=1)
for i, item in enumerate(['All files', 'Favorites', 'Shared with you', 'Shared with others', 'Shared by link', 'Tags', 'Deleted files']):
    c.text((28, 78 + i * 40), item, font=font(17), fill=INK if i == 0 else GREY)

# file rows
c.text((262, 72), 'Name', font=font(15), fill=GREY)
c.text((760, 72), 'Size', font=font(15), fill=GREY)
c.text((850, 72), 'Modified', font=font(15), fill=GREY)
rows = [('Documents', '36 KB', '2 hours ago'), ('Photos', '663 KB', '2 hours ago'),
        ('Handbook.pdf', '1.2 MB', 'yesterday'), ('Travel policy.docx', '48 KB', '3 days ago'),
        ('ownCloud Manual.pdf', '4.9 MB', '2 hours ago')]
y = 104
for name, size, when in rows:
    c.rectangle([248, y, 262 + 22, y + 22], fill=(74, 118, 190) if not '.' in name else (150, 150, 155))
    c.text((300, y), name, font=font(17), fill=INK)
    c.text((760, y), size, font=font(15), fill=GREY)
    c.text((850, y), when, font=font(15), fill=GREY)
    c.line([248, y + 44, 980, y + 44], fill=LINE, width=1)
    y += 52

# chat panel
PX, PY, PW, PH = CW - 400, 74, 372, CH - 96
pshadow = Image.new('RGBA', (PW + 60, PH + 60), (0, 0, 0, 0))
ImageDraw.Draw(pshadow).rounded_rectangle([30, 34, PW + 30, PH + 34], 14, fill=(0, 0, 0, 45))
pshadow = pshadow.filter(ImageFilter.GaussianBlur(14))
card.paste(pshadow, (PX - 30, PY - 30), pshadow)
c.rounded_rectangle([PX, PY, PX + PW, PY + PH], 14, fill=(255, 255, 255), outline=LINE)
c.ellipse([PX + 18, PY + 16, PX + 46, PY + 44], fill=BLUE)
c.text((PX + 58, PY + 18), 'AI Assistant', font=font(18, True), fill=INK)
c.ellipse([PX + PW - 30, PY + 26, PX + PW - 22, PY + 34], fill=(52, 199, 89))
c.line([PX, PY + 60, PX + PW, PY + 60], fill=LINE, width=1)

# visitor question
q = 'How do I share a folder with someone outside the company?'
qf = font(15)
ql = wrap(c, q, qf, 230)
qh = len(ql) * 22 + 18
c.rounded_rectangle([PX + PW - 262, PY + 76, PX + PW - 14, PY + 76 + qh], 12, fill=BLUE)
yy = PY + 85
for line in ql:
    c.text((PX + PW - 250, yy), line, font=qf, fill=(255, 255, 255))
    yy += 22

# assistant answer, from the handbook
a = ('Open Files, hover the folder and click the share icon. Choose "Public link", set an expiry '
     'date and a password, then send the link. External people need no ownCloud account.')
af = font(15)
al = wrap(c, a, af, 300)
ah = len(al) * 22 + 18
top = PY + 76 + qh + 14
c.rounded_rectangle([PX + 14, top, PX + PW - 30, top + ah], 12, fill=BUBBLE)
yy = top + 9
for line in al:
    c.text((PX + 26, yy), line, font=af, fill=INK)
    yy += 22

# input row
c.line([PX, PY + PH - 54, PX + PW, PY + PH - 54], fill=LINE, width=1)
c.rounded_rectangle([PX + 16, PY + PH - 42, PX + PW - 58, PY + PH - 12], 15, outline=LINE, fill=(250, 250, 250))
c.text((PX + 30, PY + PH - 36), 'Write your message…', font=font(15), fill=GREY)
c.ellipse([PX + PW - 48, PY + PH - 44, PX + PW - 14, PY + PH - 10], fill=BLUE)
c.polygon([(PX + PW - 31, PY + PH - 36), (PX + PW - 24, PY + PH - 27), (PX + PW - 31, PY + PH - 18)], fill=(255, 255, 255))

mask = Image.new('L', (CW, CH), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, CW - 1, CH - 1], 16, fill=255)
canvas.paste(card, (CX, CY), mask)

path = os.path.join(OUT, 'chat.png')
canvas.save(path)
print(path, canvas.size)
