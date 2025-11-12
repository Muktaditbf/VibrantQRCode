import os
import qrcode
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

OUT_DIR = r"C:\Users\rtx\Pictures"
os.makedirs(OUT_DIR, exist_ok=True)

ME_STYLES = {
    "1": ("Classic", (0, 0, 0), (255, 255, 255)),
    "2": ("Navy→Teal", (10, 25, 77), (14, 203, 180)),
    "3": ("Purple→Gold", (88, 24, 69), (255, 193, 7)),
    "4": ("Sunset", (255, 94, 98), (255, 195, 113)),
}

def linear_gradient(size, start_color, end_color):
    w, h = size
    base = Image.new("RGB", size, start_color)
    r1, g1, b1 = start_color
    r2, g2, b2 = end_color
    draw = ImageDraw.Draw(base)
    for x in range(w):
        t = x / (w - 1) if w > 1 else 0
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        draw.line([(x, 0), (x, h)], fill=(r, g, b))
    return base

def make_qr_mask(url, box_size=10, border=4):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("L")
    # mask: 255 where modules are (black), 0 where background
    mask = img.point(lambda p: 255 if p < 128 else 0).convert("L")
    # save debug mask
    try:
        mask.save(os.path.join(OUT_DIR, "debug_qr_mask.png"))
    except Exception:
        pass
    return mask

def draw_center_logo(base_img, size_ratio=0.24):
    w, h = base_img.size
    diameter = int(min(w, h) * size_ratio)
    draw = ImageDraw.Draw(base_img)
    cx, cy = w // 2, h // 2
    circle_box = (
        cx - diameter // 2,
        cy - diameter // 2,
        cx + diameter // 2,
        cy + diameter // 2,
    )
    # white disc
    draw.ellipse(circle_box, fill=(255, 255, 255))

    # load a font (fallback to default)
    font_size = max(10, int(diameter * 0.7))
    font = None
    for fname in ("arial.ttf", "SegoeUIEmoji.ttf", "DejaVuSans.ttf"):
        try:
            font = ImageFont.truetype(fname, font_size)
            break
        except Exception:
            font = None
    if font is None:
        font = ImageFont.load_default()

    text = "f"
    # robust text measurement with fallbacks
    try:
        # Pillow >= 8.0
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except Exception:
        try:
            tw, th = font.getsize(text)
        except Exception:
            tw = int(diameter * 0.6)
            th = int(diameter * 0.6)

    # draw the Facebook-style "f" centered in the white disc
    draw.text((cx - tw // 2, cy - th // 2 - 2), text, fill=(59, 89, 152), font=font)

def save_qr_image(final_img, basename="qrcode_facebook"):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{basename}_{now}.png"
    path = os.path.join(OUT_DIR, filename)
    final_img.save(path)
    return path

def build_colored_qr(url, style_key):
    mask = make_qr_mask(url)
    w, h = mask.size
    name, c1, c2 = ME_STYLES.get(style_key, ME_STYLES["2"])
    if c1 == c2:
        color_img = Image.new("RGB", (w, h), c1)
    else:
        color_img = linear_gradient((w, h), c1, c2)
    bg = Image.new("RGB", (w, h), (255, 255, 255))
    # ensure mask is L and contains 0/255
    mask_l = mask.convert("L")
    colored_qr = Image.composite(color_img, bg, mask_l)
    # save debug colored qr before logo
    try:
        colored_qr.save(os.path.join(OUT_DIR, "debug_colored_qr.png"))
    except Exception:
        pass
    if min(w, h) >= 200:
        draw_center_logo(colored_qr)
    return colored_qr

def main():
    try:
        url = input("Enter the Facebook profile or page URL: ").strip()
    except KeyboardInterrupt:
        print("\nCancelled.")
        return

    if not url:
        print("No URL provided. Exiting.")
        return

    print("\nStyles:")
    for k, v in ME_STYLES.items():
        print(f" {k}) {v[0]}")
    style = input("Choose style (1-4, default 2): ").strip() or "2"
    if style not in ME_STYLES:
        style = "2"

    try:
        final = build_colored_qr(url, style)
        out_path = save_qr_image(final, "facebook_qr")
        print(f"✅ QR code saved to {out_path}")
    except Exception as exc:
        print("Failed to create QR code — debug info saved to your Pictures folder.")
        print("Error:", exc)

if __name__ == "__main__":
    main()