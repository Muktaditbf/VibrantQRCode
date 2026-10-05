<div align="center">

# 🌈 VibrantQRCode

**Turns any Facebook profile or page link into a colourful, gradient QR code with a centre logo, ready to print or share.**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-8CAAE6?style=for-the-badge&logo=python&logoColor=white)
![qrcode](https://img.shields.io/badge/qrcode-000?style=for-the-badge)

</div>

## ✨ Features
- 🎨 **4 gradient styles:** Classic, Navy→Teal, Purple→Gold and Sunset
- 🛡️ **High error correction (level H)**, so the code still scans with a logo in the middle
- ⚪ **Centre logo badge** drawn on top of the QR code
- 🖼️ Exports a **PNG** with a timestamped filename

## 🚀 Run it
```bash
pip install qrcode pillow
python fb_qr.py
```
1. Paste a Facebook profile or page URL.
2. Pick a style from 1 to 4 (the default is 2).
3. Find the PNG in the output folder.

> ⚠️ The output folder is set by `OUT_DIR` at the top of `fb_qr.py`. Change it to a folder on your machine.

## 👤 Author
**Muktadi** · CSE @ Southeast University · [GitHub](https://github.com/Muktaditbf) · [LinkedIn](https://www.linkedin.com/in/muktadi-mohammad)
