#!/usr/bin/env python3
"""Fast preview builder: one record in records.py -> /p/<slug>/index.html in the site repo.
Usage: python3 build_fast.py <repo_root> [slug ...]"""
import sys, os, json, html, shutil
from urllib.parse import quote
from records import RECORDS, THEMES, CHECKED, NT_PHONE, NT_EMAIL

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
SCHEMA_DAYS = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
E = html.escape


def parse(h):
    h = h.replace(" ", " ").replace(" ", " ").strip()
    if h.lower() == "closed":
        return None
    a, b = [x.strip() for x in h.split("–")]
    mer_b = b.split()[1]

    def tm(s, mer):
        parts = s.split()
        m = parts[1] if len(parts) > 1 else mer
        hh, mm = [int(x) for x in parts[0].split(":")]
        if m == "AM":
            hh = 0 if hh == 12 else hh
        else:
            hh = 12 if hh == 12 else hh + 12
        return hh * 60 + mm

    o, c = tm(a, mer_b), tm(b, mer_b)
    if c <= o:
        c += 1440
    return [o, c]


def fmt(m):
    m = m % 1440
    if m == 0:
        return "midnight"
    h, n = divmod(m, 60)
    s = "am" if h < 12 else "pm"
    h = h % 12 or 12
    return f"{h}{':%02d' % n if n else ''}{s}"


def tel(p):
    d = p.replace(" ", "")
    return "+44" + d[1:]


PHONE_SVG = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1L6.6 10.8z"/></svg>'
PIN_SVG = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg>'

CSS = r"""
@font-face{font-family:"Archivo NT";src:url("../assets/archivo-var.woff") format("woff");font-weight:400 900;font-stretch:62% 125%;font-style:normal;font-display:swap}
:root{--brand:[[brand]];--on:[[on]];--accent:[[accent]];--aon:[[aon]];--tint:[[tint]];--soft:[[soft]];--ink:#15181D;--mute:#555C66;--line:#D9DDE3}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;text-size-adjust:100%}
body{margin:0;font-family:"Archivo NT",system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;font-size:1.0625rem;line-height:1.5;color:#15181D;color:var(--ink);background:#fff;padding-bottom:84px;-webkit-font-smoothing:antialiased}
a{color:inherit}
svg{flex:none}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
.skip{position:absolute;left:-999px;top:0;background:#fff;color:#000;padding:10px 14px;z-index:10}
.skip:focus{left:8px;top:8px}
a:focus-visible{outline:3px solid #1A73E8;outline-offset:3px}
.pv{background:#101317;color:#fff;font-size:.875rem;line-height:1.4;padding:10px 0}
.pv a{color:#fff;font-weight:700;white-space:nowrap}
.fascia{background:[[brand]];background:var(--brand);color:[[on]];color:var(--on);padding-top:34px}
.name{margin:0;font-weight:800;font-stretch:68%;line-height:.9;letter-spacing:-.01em;font-size:3rem;font-size:clamp(2.75rem,[[vw]]vw,7.5rem);text-wrap:balance;overflow-wrap:anywhere}
.kind{margin:16px 0 0;font-size:1.125rem;line-height:1.35;color:[[soft]];color:var(--soft);max-width:26em}
.sign{background:#fff;color:#15181D;color:var(--ink);border-radius:8px;padding:18px 18px 20px;margin-top:26px}
.status{display:flex;align-items:center;font-weight:800;font-stretch:80%;font-size:1.5rem;line-height:1.15;margin:0}
.dot{width:14px;height:14px;border-radius:50%;background:#9AA1AB;margin-right:10px;flex:none}
.is-open .dot{background:#1E9E57}
.is-shut .dot{background:#C8322B}
.until{margin:4px 0 0 24px;color:#555C66;color:var(--mute)}
.btns{margin-top:16px}
.btn{display:flex;align-items:center;justify-content:center;text-align:center;text-decoration:none;font-weight:700;font-size:1.0625rem;line-height:1.2;padding:15px 16px;border-radius:6px;border:2px solid #15181D;border-color:var(--ink);color:#15181D;color:var(--ink);background:#fff}
.btn svg{margin-right:8px}
.btn+.btn{margin-top:10px}
.btn-main{background:[[accent]];background:var(--accent);border-color:[[accent]];border-color:var(--accent);color:[[aon]];color:var(--aon)}
.num{white-space:nowrap}
.stripe{height:12px;margin-top:28px;background:[[accent]];background:var(--accent)}
.theme-barber .stripe{background:repeating-linear-gradient(135deg,#C8322B 0,#C8322B 14px,#fff 14px,#fff 28px,#2B5BA8 28px,#2B5BA8 42px,#fff 42px,#fff 56px)}
.rate{border-bottom:1px solid #D9DDE3;border-color:var(--line);padding:20px 0}
.rate-in{display:flex;align-items:center}
.score{font-weight:800;font-stretch:75%;font-size:2.75rem;line-height:1;margin-right:14px}
.rate p{margin:0;line-height:1.35}
.rate a{font-weight:700}
.main{padding:6px 0 44px}
.sec{padding-top:32px}
h2{margin:0 0 14px;font-weight:800;font-stretch:75%;font-size:1.875rem;line-height:1.1}
.prices{list-style:none;margin:0;padding:0;border-top:2px solid #15181D;border-color:var(--ink)}
.prices li{display:flex;align-items:center;justify-content:space-between;padding:13px 0;border-bottom:1px solid #D9DDE3;border-bottom-color:var(--line)}
.p-name{font-weight:600;padding-right:14px;line-height:1.3}
.p-time{display:block;font-weight:400;font-size:.9375rem;color:#555C66;color:var(--mute)}
.p-cost{font-weight:800;font-size:1.3125rem;white-space:nowrap}
.after{margin-top:18px}
.hours{width:100%;border-collapse:collapse;border-top:2px solid #15181D;border-top-color:var(--ink)}
.hours th,.hours td{text-align:left;padding:11px 10px;border-bottom:1px solid #D9DDE3;border-bottom-color:var(--line);font-weight:400}
.hours td{text-align:right;white-space:nowrap}
.hours tr.today th,.hours tr.today td{font-weight:800;background:[[tint]];background:var(--tint)}
.note{background:#FFF7CF;border:2px dashed #C9A300;border-radius:6px;padding:14px 16px;font-size:.9688rem;line-height:1.45;color:#3D3200;margin:0}
.note b{display:block;margin-bottom:2px}
.note+.note,.prices+.note,.after+.note{margin-top:18px}
.addr{font-style:normal;font-size:1.1875rem;line-height:1.45;margin:0 0 18px}
.addr b{display:block}
.ft{background:[[tint]];background:var(--tint);color:#3B424C;font-size:.875rem;line-height:1.5;padding:24px 0 28px}
.ft p{margin:0 0 8px}
.ft p:last-child{margin:0}
.bar{position:fixed;left:0;right:0;bottom:0;background:#fff;border-top:1px solid #D9DDE3;padding:10px 12px;padding-bottom:calc(10px + env(safe-area-inset-bottom));display:flex;z-index:5}
.bar .btn{flex:1 1 0;min-width:0;padding:13px 8px}
.bar .btn+.btn{margin:0 0 0 10px}
@media (max-width:359px){.wrap{padding:0 14px}.btn{font-size:1rem;padding-left:10px;padding-right:10px}.status{font-size:1.3125rem}}
@media (min-width:860px){
body{padding-bottom:0;font-size:1.125rem}
.bar{display:none}
.wrap{padding:0 40px}
.fascia{padding-top:60px}
.cols{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(320px,.7fr);column-gap:64px}
.fascia .cols{align-items:end}
.sign{margin-top:0;padding:22px 22px 24px}
.kind{font-size:1.3125rem;margin-top:22px}
.stripe{margin-top:44px;height:14px}
.main .cols{grid-template-areas:"what hours" "photos find";align-items:start}
#what{grid-area:what}#hours{grid-area:hours}#photos{grid-area:photos}#find{grid-area:find}
.sec{padding-top:44px}
#find .btn{display:inline-flex;margin:0 10px 0 0}
}
@media print{.bar,.pv{display:none}body{padding:0}}
"""

JS = r"""(function(){
var H=[[H]],D=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"];
function f(m){m=m%1440;if(m===0)return"midnight";var h=Math.floor(m/60),n=m%60,s=h<12?"am":"pm";h=h%12;if(h===0)h=12;return h+(n?":"+(n<10?"0":"")+n:"")+s}
function now(){var d=new Date();try{var p=new Intl.DateTimeFormat("en-GB",{timeZone:"Europe/London",weekday:"long",hour:"2-digit",minute:"2-digit",hour12:false}).formatToParts(d),o={};for(var i=0;i<p.length;i++){o[p[i].type]=p[i].value}var w=D.indexOf(o.weekday);if(w>-1){return[w,(parseInt(o.hour,10)%24)*60+parseInt(o.minute,10)]}}catch(e){}return[(d.getDay()+6)%7,d.getHours()*60+d.getMinutes()]}
function go(){var n=now(),w=n[0],m=n[1],y=H[(w+6)%7],t=H[w],open=false,txt="",k,q;
var rows=document.querySelectorAll(".hours tr");for(k=0;k<rows.length;k++){rows[k].className=k===w?"today":""}
if(y&&y[1]>1440&&m<y[1]-1440){open=true;txt="Until "+f(y[1])}
else if(t&&m>=t[0]&&m<t[1]){open=true;txt="Until "+f(t[1])+(t[1]>=1440?" tonight":" today")}
else if(t&&m<t[0]){txt="Opens at "+f(t[0])+" today"}
else{for(k=1;k<=7;k++){q=H[(w+k)%7];if(q){txt="Opens at "+f(q[0])+(k===1?" tomorrow":" on "+D[(w+k)%7]);break}}}
document.getElementById("sign").className="sign "+(open?"is-open":"is-shut");
document.getElementById("st").textContent=open?"Open now":"Closed now";
document.getElementById("un").textContent=txt}
go();setInterval(go,60000);
})();"""


def build(r):
    t = THEMES[r["theme"]]
    hrs = [parse(h) for h in r["hours"]]
    name, kind = r["name"], r["kind"]
    full_addr = f'{r["street"]}, {r["area"]} {r["postcode"]}'
    q = quote(f'{name}, {full_addr}')
    dir_url = f'https://www.google.com/maps/dir/?api=1&destination={q}&destination_place_id={r["place_id"]}'
    g_url = f'https://www.google.com/maps/search/?api=1&query={q}&query_place_id={r["place_id"]}'
    url = f'https://nextthreadautomation.co.uk/p/{r["slug"]}/'
    longest = max(len(w) for w in name.split())
    cap = 23.0 if len(name.split()) == 1 else 19.0
    vw = round(min(cap, max(11.0, 86 / (0.47 * longest))), 1)
    street_name = r["street"].split(" ", 1)[1]
    title = f'{name} | {kind} on {street_name}, {r["area"].split(", ")[-1]}'
    has_prices = bool(r.get("prices"))
    desc = (f'{name}, {kind.lower()} at {full_addr}. Opening hours'
            f'{", prices" if has_prices else ""} and directions. Call {r["phone"]}.')
    all_week = all(hrs)

    # what we do
    wants = r.get("wants", "services")
    if has_prices:
        lis = "".join(
            f'<li><span class="p-name">{E(n)}<span class="p-time">{E(tm)}</span></span><span class="p-cost">{E(c)}</span></li>'
            for n, tm, c in r["prices"])
        bk_name, bk_url = r["booking"]
        what = (f'<h2>Prices</h2><ul class="prices">{lis}</ul>'
                f'<div class="after"><a class="btn btn-main" href="{E(bk_url)}" rel="noopener">Book on {E(bk_name)}</a></div>'
                f'<p class="note"><b>Note from NextThread</b>These prices are from your {E(bk_name)} page on {CHECKED}. Tell us if any have changed and we will update them.</p>')
    elif wants == "menu":
        what = ('<h2>Menu</h2><p class="note"><b>Note from NextThread</b>Your menu goes here. '
                'Send us a photo of it and we will add it the same day.</p>')
    else:
        what = ('<h2>Prices</h2><p class="note"><b>Note from NextThread</b>Your services and prices go here. '
                'Send us a photo of your price list and we will add it the same day.</p>')

    rows = "".join(
        f'<tr><th scope="row">{d}</th><td>{("%s to %s" % (fmt(h[0]), fmt(h[1]))) if h else "Closed"}</td></tr>'
        for d, h in zip(DAYS, hrs))

    rate = ""
    if r["rating"] >= 4.5:
        rate = (f'<div class="rate"><div class="wrap rate-in"><span class="score">{r["rating"]:.1f}</span>'
                f'<p>out of 5 on Google, from {r["count"]} reviews.<br>'
                f'<a href="{E(g_url)}" rel="noopener">Read the reviews on Google</a></p></div></div>')

    ld = {
        "@context": "https://schema.org", "@type": r["schema"], "name": name,
        "telephone": tel(r["phone"]), "url": url,
        "address": {"@type": "PostalAddress", "streetAddress": r["street"],
                    "addressLocality": r["area"].split(", ")[-1], "postalCode": r["postcode"], "addressCountry": "GB"},
        "geo": {"@type": "GeoCoordinates", "latitude": r["lat"], "longitude": r["lng"]},
        "openingHours": [f'{SCHEMA_DAYS[i]} {h[0] // 60:02d}:{h[0] % 60:02d}-{(h[1] % 1440) // 60:02d}:{h[1] % 60:02d}'
                         for i, h in enumerate(hrs) if h],
    }
    icon = quote(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="{t["brand"]}"/>'
                 f'<text x="32" y="45" font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="38" text-anchor="middle" fill="{t["on"]}">{E(name.replace("The ", "")[0])}</text></svg>')
    css = CSS.replace("[[vw]]", str(vw))
    for k, v in t.items():
        css = css.replace(f"[[{k}]]", v)
    js = JS.replace("[[H]]", json.dumps(hrs, separators=(",", ":")))
    src = f'Opening hours, phone number and Google rating are from the Google listing for {E(name)} on {CHECKED}.'
    if has_prices:
        src += f' Prices are from its {E(r["booking"][0])} page on the same day.'

    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<!-- a private preview for one business, not a live site: kept out of search engines -->
<meta name="robots" content="noindex, nofollow, noarchive">
<meta name="color-scheme" content="only light">
<meta name="format-detection" content="telephone=no">
<meta name="theme-color" content="{t['brand']}">
<meta property="og:type" content="website">
<meta property="og:title" content="{E(name)}, {E(r['area'])}">
<meta property="og:description" content="{E(kind)} at {E(r['street'])}. Opening hours and directions.">
<meta property="og:url" content="{url}">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,{icon}">
<link rel="preload" href="../assets/archivo-var.woff" as="font" type="font/woff" crossorigin>
<style>{css}</style>
</head>
<body class="theme-{r['theme']}">
<a class="skip" href="#main">Skip to the page</a>
<div class="pv" role="note" aria-label="Preview notice"><div class="wrap">Website preview for {E(name)}, made by NextThread. To make it live, call <a href="tel:{tel(NT_PHONE)}">{NT_PHONE}</a>.</div></div>
<header class="fascia">
  <div class="wrap cols">
    <div>
      <h1 class="name">{E(name)}</h1>
      <p class="kind">{E(kind)} at {E(r['street'])}, {E(r['area'])}</p>
    </div>
    <div class="sign" id="sign">
      <p class="status"><span class="dot"></span><span id="st">{'Open 7 days a week' if all_week else 'Opening hours'}</span></p>
      <p class="until" id="un">Hours for each day are below</p>
      <div class="btns">
        <a class="btn btn-main" href="tel:{tel(r['phone'])}">{PHONE_SVG}<span>Call <span class="num">{r['phone']}</span></span></a>
        <a class="btn" href="{E(dir_url)}" rel="noopener">{PIN_SVG}Get directions</a>
      </div>
    </div>
  </div>
  <div class="stripe"></div>
</header>
{rate}
<main class="main" id="main">
  <div class="wrap cols">
    <section class="sec" id="what">{what}</section>
    <section class="sec" id="hours"><h2>Opening hours</h2><table class="hours"><tbody>{rows}</tbody></table></section>
    <section class="sec" id="photos"><h2>Photos</h2><p class="note"><b>Note from NextThread</b>Your photos go here. Send us 3 to 6 from your phone and we will add them the same day.</p></section>
    <section class="sec" id="find"><h2>Find us</h2>
      <address class="addr"><b>{E(name)}</b>{E(r['street'])}<br>{E(r['area'])}<br>{E(r['postcode'])}</address>
      <a class="btn" href="{E(dir_url)}" rel="noopener">{PIN_SVG}Get directions</a>
      <a class="btn" href="tel:{tel(r['phone'])}">{PHONE_SVG}<span>Call <span class="num">{r['phone']}</span></span></a>
    </section>
  </div>
</main>
<footer class="ft"><div class="wrap">
  <p>{E(name)}, {E(full_addr)}.</p>
  <p>{src}</p>
  <p>Website preview by NextThread. This is not a live website yet. {NT_PHONE}, {NT_EMAIL}</p>
</div></footer>
<div class="bar">
  <a class="btn btn-main" href="tel:{tel(r['phone'])}">{PHONE_SVG}Call</a>
  <a class="btn" href="{E(dir_url)}" rel="noopener">{PIN_SVG}Directions</a>
</div>
<script type="application/ld+json">{json.dumps(ld, separators=(",", ":"))}</script>
<script>{js}</script>
</body>
</html>
"""


if __name__ == "__main__":
    root = sys.argv[1]
    only = set(sys.argv[2:])
    os.makedirs(os.path.join(root, "p", "assets"), exist_ok=True)
    font = os.path.join(root, "p", "assets", "archivo-var.woff")
    if not os.path.exists(font):
        shutil.copy(os.path.join(root, "p", "adapt-drainage-services", "archivo-var.woff"), font)
    for r in RECORDS:
        if only and r["slug"] not in only:
            continue
        d = os.path.join(root, "p", r["slug"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(build(r))
        print("built", r["slug"])
