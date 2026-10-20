"""Build the portfolio into a single self-contained index.html.

Usage: python3 scripts/build.py
Reads everything from src/ and writes index.html at the repository root.
Images, logos and the Subscription Management prototype are inlined, so the
page has no local file dependencies.
"""
import base64, html, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
OUT = ROOT / "index.html"

MIME = {".webp": "image/webp", ".png": "image/png", ".svg": "image/svg+xml"}

def data_uri(path: Path) -> str:
    raw = path.read_bytes()
    if path.suffix == ".svg":  # strip embedded C2PA metadata to keep logos small
        raw = re.sub(rb"<metadata>.*?</metadata>", b"", raw, flags=re.S)
    return f"data:{MIME[path.suffix]};base64," + base64.b64encode(raw).decode()

img, assets, billing = SRC / "img", SRC / "assets", SRC / "img" / "billing"

PLACEHOLDERS = {
    "ICON": img / "leaf-icon.webp",
    "PORTRAIT": img / "portrait.webp",
    "LEAF": img / "leaf.webp",
    "ABOUT": img / "about.webp",
    "H_PHOTO": img / "photo.webp",
    "H_ILLU": img / "illu.webp",
    "H_HIKE": img / "hike.webp",
    "H_MUSIC": img / "music.webp",
    "UFPB": img / "ufpb.png",
    "LOGO_NOLIMIT": assets / "logo-nolimit.svg",
    "LOGO_FAZPAY": assets / "logo-fazpay.svg",
    "LOGO_INCENTIVE": assets / "logo-incentive.svg",
    "LOGO_DOCK": assets / "logo-dock.svg",
    "LOGO_DEGRAU": assets / "logo-degrau.svg",
    "B_CHANGE": billing / "change.webp",
    "B_DUNNING_DETAIL": billing / "dunning_detail.webp",
    "B_M_LIST": billing / "m_list.webp",
    "B_M_ACCOUNT": billing / "m_account.webp",
    "B_THUMB": billing / "thumb.webp",
    "B_PAYMENT": billing / "payment.webp",
    "B_PLANS": billing / "plans.webp",
}

def main() -> None:
    page = (SRC / "template.html").read_text()
    page = page.replace("{{CASE_CSS}}", (SRC / "case-billing.css").read_text())
    page = page.replace("{{CASE_HTML}}", (SRC / "case-billing.html").read_text())
    for key, path in PLACEHOLDERS.items():
        page = page.replace("{{" + key + "}}", data_uri(path))
    proto = (SRC / "prototype" / "billing-console.html").read_text()
    page = page.replace("{{PROTO_SRC}}", html.escape(proto, quote=False))

    left = re.findall(r"\{\{[A-Z_]+\}\}", page.replace(html.escape(proto, quote=False), ""))
    if left:
        raise SystemExit(f"Unfilled placeholders: {sorted(set(left))}")

    doc = (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
        + page
    )
    # move everything up to the end of </style> into <head>, the rest into <body>
    head_end = doc.index("</style>") + len("</style>")
    doc = doc[:head_end] + "\n</head>\n<body>\n" + doc[head_end:] + "\n</body>\n</html>\n"
    OUT.write_text(doc)
    print(f"Wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KB)")

if __name__ == "__main__":
    main()
