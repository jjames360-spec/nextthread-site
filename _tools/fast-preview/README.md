# Fast preview builder

Builds a simple one-page preview for a local shop from a few facts, and a sheet of
leave-behind cards with a QR code for each preview. This folder starts with an
underscore, so GitHub Pages does not publish it.

- `records.py`: one record per shop (name, address, phone, opening hours, Google rating,
  place id, and prices where the shop publishes them), plus the colour themes.
  Every fact must come from a source. Never guess.
- `build_fast.py`: `python3 build_fast.py <repo root> [slug ...]` writes `/p/<slug>/index.html`.
- `cards.py`: `python3 cards.py` writes an A4 PDF, 10 cards a page plus a visit sheet.
  Edit `ORDER` in it for each new batch. Needs reportlab.

Each preview is noindex, carries a "Website preview" strip, and shows yellow
"Note from NextThread" boxes where the shop's own prices, menu and photos will go.
The Google rating is shown only when it is 4.5 or higher.
