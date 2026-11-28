from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from records import RECORDS, THEMES, NT_PHONE, NT_EMAIL

R = {r["slug"]: r for r in RECORDS}
# visiting order, with what to check, and Sunday hours
ORDER = [
 ("the-coffee-cup-boldmere", "8:30am to 2pm", "4.5 from 77 Google reviews",
  "Ask first if they already have a website. One listing site showed a website link I could not open."),
 ("madrid-cutz", "10am to 4pm", "4.8 from 132 Google reviews. Their Booksy prices are on the page.", ""),
 ("sutton-car-wash", "9am to 5pm", "178 Google reviews",
  "Their Google score is 4.0, so the page leaves the score off."),
 ("boldmere-barbers", "10am to 4pm", "5.0 from 81 Google reviews. Their Booksy prices are on the page.", ""),
 ("gully-junction", "10am to 9pm", "4.6 from 14 Google reviews",
  "Google calls it an Indian restaurant. Check that is how they describe it."),
 ("fade-garden-barbers", "10am to 4pm", "5.0 from 50 Google reviews",
  "Booking sites still show Kings Barbers Club at number 55. Check the sign says Fade Garden."),
 ("serenity-boldmere", "10am to 11pm", "4.8 from 104 Google reviews", ""),
 ("emerald-barbers", "10am to 5pm", "4.9 from 91 Google reviews. Their Booksy prices are on the page.",
  "390 Boldmere Road is the far end, near Chester Road. Drive."),
 ("top-fade-barbers", "9am to 5pm", "5.0 from 181 Google reviews", "Kings Road, not Boldmere Road. Drive."),
 ("sutton-mobiles", "1pm to 6pm", "4.8 from 59 Google reviews", "Opens at 1pm, so it is last."),
]
if __name__ == "__main__":
    W, H = A4
    c = canvas.Canvas("boldmere-cards-29-nov.pdf", pagesize=A4)
    c.setTitle("NextThread cards: Boldmere visits, Sunday 29 November 2026")
    c.setAuthor("NextThread")
    cw, ch = 90 * mm, 54 * mm
    mx, my = (W - 2 * cw) / 2, (H - 5 * ch) / 2
    for i, (slug, *_r) in enumerate(ORDER):
        r = R[slug]; t = THEMES[r["theme"]]
        col, row = i % 2, i // 2
        x, y = mx + col * cw, H - my - (row + 1) * ch
        # cut line
        c.setStrokeColor(HexColor("#9AA1AB")); c.setLineWidth(0.4); c.setDash(2, 2); c.rect(x, y, cw, ch); c.setDash()
        # name band
        pad = 5 * mm; band = 11 * mm
        c.setFillColor(HexColor(t["brand"])); c.rect(x + 0.3, y + ch - band, cw - 0.6, band - 0.3, stroke=0, fill=1)
        c.setFillColor(white); c.setFont("Helvetica-Bold", 13); c.drawString(x + pad, y + ch - band + 3.6 * mm, r["name"])
        c.setFont("Helvetica", 7); c.drawRightString(x + cw - pad, y + ch - band + 3.9 * mm, f"{i + 1} of 10")
        # QR
        url = f"https://nextthreadautomation.co.uk/p/{slug}/"
        size = 29 * mm
        w = qr.QrCodeWidget(url, barLevel="M")
        b = w.getBounds(); bw, bh = b[2] - b[0], b[3] - b[1]
        d = Drawing(size, size, transform=[size / bw, 0, 0, size / bh, 0, 0]); d.add(w)
        qx, qy = x + cw - pad - size + 1.5 * mm, y + 9.5 * mm
        renderPDF.draw(d, c, qx, qy)
        # text
        tx = x + pad; ty = y + ch - band - 7.5 * mm
        c.setFillColor(black)
        c.setFont("Helvetica-Bold", 10.5); c.drawString(tx, ty, "Your website preview")
        c.drawString(tx, ty - 4.6 * mm, "is ready.")
        c.setFont("Helvetica", 8.5)
        c.drawString(tx, ty - 10.2 * mm, "Scan the code to see it")
        c.drawString(tx, ty - 14 * mm, "on your phone.")
        c.setFont("Helvetica", 7.2)
        c.drawString(tx, ty - 19.2 * mm, "£349 if you order by Wed 16 December.")
        c.drawString(tx, ty - 22.4 * mm, "You pay the day it goes live.")
        c.setFont("Helvetica-Bold", 8.5); c.drawString(tx, y + 9.4 * mm, f"NextThread  {NT_PHONE}")
        c.setFont("Helvetica", 6.6); c.drawString(tx, y + 6.0 * mm, NT_EMAIL)
        c.setFont("Helvetica", 5.6); c.setFillColor(HexColor("#444444"))
        c.drawString(tx, y + 2.9 * mm, url.replace("https://", ""))
    c.showPage()

    # page 2: run sheet
    P = ParagraphStyle("p", fontName="Helvetica", fontSize=8.2, leading=10.4)
    PB = ParagraphStyle("pb", parent=P, fontName="Helvetica-Bold")
    c.setFont("Helvetica-Bold", 16); c.drawString(15 * mm, H - 20 * mm, "Sunday 29 November: 10 visits in Boldmere")
    c.setFont("Helvetica", 9.5)
    c.drawString(15 * mm, H - 26.5 * mm, "Start at 11am at The Coffee Cup. Stops 1 to 7 are a walk down Boldmere Road. Drive to 8 and 9, then come back for 10.")
    rows = [[Paragraph(h, PB) for h in ["", "Shop", "Open Sunday", "A true thing to mention", "Check first", "Result"]]]
    for i, (slug, sun, fact, check) in enumerate(ORDER):
        r = R[slug]
        rows.append([Paragraph(str(i + 1), PB),
                     Paragraph(f'<b>{r["name"]}</b><br/>{r["street"]}, {r["postcode"]}<br/>{r["phone"]}', P),
                     Paragraph(sun, P), Paragraph(fact, P), Paragraph(check, P), ""])
    tb = Table(rows, colWidths=[7 * mm, 43 * mm, 21 * mm, 40 * mm, 47 * mm, 22 * mm], repeatRows=1)
    tb.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, 0), 1, black),
                            ("LINEBELOW", (0, 1), (-1, -1), 0.4, HexColor("#9AA1AB")),
                            ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                            ("LEFTPADDING", (0, 0), (-1, -1), 2), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    tw, th = tb.wrapOn(c, W - 30 * mm, H)
    tb.drawOn(c, 15 * mm, H - 32 * mm - th)
    yb = H - 32 * mm - th - 9 * mm
    c.setFont("Helvetica-Bold", 9.5); c.drawString(15 * mm, yb, "Result: write Yes, Maybe, No or Owner out. If the owner is out, ask for their name and the best number.")
    c.setFont("Helvetica", 9); c.drawString(15 * mm, yb - 5.5 * mm, "Every page shows the shop's Google opening hours and phone number as they were on 28 November. Ask the owner to check them.")
    c.showPage(); c.save()
    print("ok", th / mm)
