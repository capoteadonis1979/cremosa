#!/usr/bin/env python3
"""Inline Leaflet + fonts into src.html -> index.html (one self-contained file)."""
import base64, pathlib, sys

here = pathlib.Path(__file__).parent
npm = pathlib.Path.home() / "tools/npm"
leaf = npm / "leaflet-1.9.4/package/dist"
outfit = next(npm.glob("fontsource-outfit-*[0-9]")) / "package/files"
dmsans = next(npm.glob("fontsource-dm-sans-*[0-9]")) / "package/files"

def face(family, path, weight):
    b = base64.b64encode(path.read_bytes()).decode()
    return (f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{weight};"
            f"font-display:swap;src:url(data:font/woff2;base64,{b}) format('woff2')}}")

fonts = "\n".join(
    [face("Outfit", outfit / f"outfit-latin-{w}-normal.woff2", w) for w in (700, 800)] +
    [face("DM Sans", dmsans / f"dm-sans-latin-{w}-normal.woff2", w) for w in (400, 500, 700)]
)
src = (here / "src.html").read_text()
out = (src.replace("/*FONTS*/", fonts)
          .replace("/*LEAFLET_CSS*/", (leaf / "leaflet.css").read_text())
          .replace("/*LEAFLET_JS*/", (leaf / "leaflet.js").read_text().replace("</script", "<\\/script")))
dest = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else here / "index.html"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(out)
print(dest, len(out) // 1024, "KB")
