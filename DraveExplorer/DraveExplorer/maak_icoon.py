# -*- coding: utf-8 -*-
"""
maak_icoon.py - genereert app.ico (en logo.png als die ontbreekt) voor DraveExplorer.

Als er een eigen 'logo.png' in deze map staat, wordt die gebruikt voor het .ico.
Anders wordt een nette map in de huisstijl getekend.
Draai eenmalig:  python maak_icoon.py
"""
import os
from PIL import Image, ImageDraw

BASIS = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(BASIS, "logo.png")
ICO = os.path.join(BASIS, "app.ico")

BG = (14, 14, 17, 255)
ACCENT = (111, 163, 214, 255)
ACCENT_DIM = (77, 122, 168, 255)
PANEL = (28, 28, 34, 255)


def teken_logo(grootte=256):
    img = Image.new("RGBA", (grootte, grootte), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = grootte / 256.0
    # afgeronde donkere achtergrond
    d.rounded_rectangle([8*s, 8*s, 248*s, 248*s], radius=40*s, fill=BG)
    # maptab
    d.rounded_rectangle([54*s, 74*s, 130*s, 104*s], radius=12*s, fill=ACCENT_DIM)
    # mapbody
    d.rounded_rectangle([46*s, 92*s, 210*s, 196*s], radius=18*s, fill=ACCENT)
    # binnenvlak
    d.rounded_rectangle([62*s, 112*s, 194*s, 180*s], radius=12*s, fill=PANEL)
    # drie "bestand"-streepjes
    for i, y in enumerate((128, 144, 160)):
        breedte = (110 - i*22) * s
        d.rounded_rectangle([78*s, y*s, 78*s+breedte, (y+8)*s],
                            radius=4*s, fill=ACCENT)
    return img


def main():
    if os.path.exists(LOGO):
        bron = Image.open(LOGO).convert("RGBA")
        print("logo.png gebruikt voor het icoon.")
    else:
        bron = teken_logo(256)
        bron.save(LOGO)
        print("logo.png gegenereerd (huisstijl). Vervang gerust door je eigen logo.")
    maten = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    bron.save(ICO, sizes=maten)
    print("app.ico aangemaakt:", ICO)


if __name__ == "__main__":
    main()
