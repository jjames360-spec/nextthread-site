# One record per business. Every fact here has a source:
#   name, address, phone, hours, rating, count, place_id, lat/lng: the shop's Google listing, read 28 Nov 2026
#   prices and booking link: the shop's own Booksy page, as shown in web search on 28 Nov 2026
CHECKED = "28 November 2026"

BARBER_HOURS_A = ["9:00 AM – 6:30 PM"] * 5 + ["9:00 AM – 6:00 PM", "10:00 AM – 4:00 PM"]

RECORDS = [
    dict(
        slug="boldmere-barbers", name="Boldmere Barbers", kind="Barbers", theme="barber", schema="BarberShop",
        street="6 Boldmere Road", area="Boldmere, Sutton Coldfield", postcode="B73 5TD",
        phone="07466 756180", rating=5.0, count=81, place_id="ChIJKxi6N86lcEgRzaTzG7I4-ZA",
        lat=52.550143, lng=-1.8418799, hours=BARBER_HOURS_A,
        prices=[("Haircut and styling", "20 min", "£15"), ("Taper fade", "20 min", "£15"),
                ("Skin fade and styling", "30 min", "£17"), ("Skin fade and beard", "40 min", "£28")],
        booking=("Booksy", "https://booksy.com/en-gb/190351_boldmere-barbers_barber_1294958_sutton-coldfield"),
    ),
    dict(
        slug="madrid-cutz", name="Madrid Cutz", kind="Barbers", theme="barber", schema="BarberShop",
        street="17 Boldmere Road", area="Boldmere, Sutton Coldfield", postcode="B73 5UY",
        phone="07424 654505", rating=4.8, count=132, place_id="ChIJi-abRlalcEgRCXmoV5oCNuQ",
        lat=52.5497188, lng=-1.8413972, hours=BARBER_HOURS_A,
        prices=[("Haircut and styling", "15 min", "£15"), ("Taper fade and styling", "20 min", "£15"),
                ("Skin fade and styling", "30 min", "£17")],
        booking=("Booksy", "https://booksy.com/en-gb/58981_madrid-cutz_barber_1294958_sutton-coldfield"),
    ),
    dict(
        slug="emerald-barbers", name="Emerald Barbers", kind="Barbers", theme="barber", schema="BarberShop",
        street="390 Boldmere Road", area="Boldmere, Sutton Coldfield", postcode="B73 5EZ",
        phone="07498 942685", rating=4.9, count=91, place_id="ChIJZZ9-CQClcEgRlbbTJ8fa8TY",
        lat=52.5374638, lng=-1.8362343,
        hours=["9:00 AM – 7:00 PM"] * 5 + ["9:00 AM – 6:00 PM", "10:00 AM – 5:00 PM"],
        prices=[("Haircut and wash style", "20 min", "£13"), ("Skin fade and wash style", "25 min", "£15"),
                ("Emerald's special", "30 min", "£17"), ("Emerald's full service", "40 min", "£26"),
                ("Kids haircut", "20 min", "£12"), ("Kids skin fade", "25 min", "£14"),
                ("O.A.P.", "15 min", "£12")],
        booking=("Booksy", "https://booksy.com/en-gb/146702_emerald-barbers_barber_1294958_sutton-coldfield"),
    ),
    dict(
        slug="fade-garden-barbers", name="Fade Garden Barbers", kind="Barbers", theme="barber", schema="BarberShop",
        street="55 Boldmere Road", area="Boldmere, Sutton Coldfield", postcode="B73 5XA",
        phone="07456 497826", rating=5.0, count=50, place_id="ChIJX43aUmWlcEgROnd4agSUqX8",
        lat=52.5486156, lng=-1.8410406, hours=BARBER_HOURS_A,
    ),
    dict(
        slug="top-fade-barbers", name="Top Fade Barbers", kind="Barbers", theme="barber", schema="BarberShop",
        street="6B Kings Road", area="Sutton Coldfield", postcode="B73 5AF",
        phone="07387 507079", rating=5.0, count=181, place_id="ChIJjWezFUSlcEgROBSQyS8xexw",
        lat=52.5485745, lng=-1.8603041,
        hours=["9:00 AM – 7:00 PM"] * 6 + ["9:00 AM – 5:00 PM"],
    ),
    dict(
        slug="sutton-car-wash", name="Sutton Car Wash", kind="Car wash", theme="carwash", schema="AutoWash",
        street="11 Boldmere Road", area="Boldmere, Sutton Coldfield", postcode="B73 5UY",
        phone="0121 439 4983", rating=4.0, count=178, place_id="ChIJz3zXquSkcEgRx9mzTaKP_Yc",
        lat=52.5498504, lng=-1.8408234,
        hours=["8:00 AM – 6:00 PM"] * 6 + ["9:00 AM – 5:00 PM"],
        wants="services",
    ),
    dict(
        slug="sutton-mobiles", name="Sutton Mobiles", kind="Mobile phone shop", theme="phone", schema="MobilePhoneStore",
        street="24 Boldmere Road", area="Boldmere, Sutton Coldfield", postcode="B73 5TD",
        phone="07496 909895", rating=4.8, count=59, place_id="ChIJfWz6sVKlcEgRVcjQ6crB3bM",
        lat=52.549847, lng=-1.8418742,
        hours=["10:30 AM – 7:00 PM"] * 6 + ["1:00 – 6:00 PM"],
        wants="services",
    ),
    dict(
        slug="gully-junction", name="Gully Junction", kind="Indian restaurant", theme="indian", schema="Restaurant",
        street="18 Boldmere Road", area="Boldmere, Sutton Coldfield", postcode="B73 5TD",
        phone="0121 354 1122", rating=4.6, count=14, place_id="ChIJHYO-IYGlcEgRRZ3aCx3yJpM",
        lat=52.5499245, lng=-1.8419299,
        hours=["9:00 AM – 8:00 PM"] * 4 + ["10:00 AM – 10:00 PM"] * 2 + ["10:00 AM – 9:00 PM"],
        wants="menu",
    ),
    dict(
        slug="the-coffee-cup-boldmere", name="The Coffee Cup", kind="Cafe", theme="cafe", schema="CafeOrCoffeeShop",
        street="19 Boldmere Road", area="Boldmere, Sutton Coldfield", postcode="B73 5UY",
        phone="07344 047180", rating=4.5, count=77, place_id="ChIJfQWQVPukcEgR9V3Oz6xb9OU",
        lat=52.5496776, lng=-1.8413564,
        hours=["8:30 AM – 3:00 PM"] * 4 + ["8:30 AM – 12:00 AM", "8:30 AM – 3:30 PM", "8:30 AM – 2:00 PM"],
        wants="menu",
    ),
    dict(
        slug="serenity-boldmere", name="Serenity", kind="Cafe lounge and cocktail bar", theme="bar", schema="BarOrPub",
        street="118 Boldmere Road", area="Boldmere, Sutton Coldfield", postcode="B73 5UB",
        phone="07411 739080", rating=4.8, count=104, place_id="ChIJD8wh7lWlcEgRBdjYoQMDhZU",
        lat=52.5469978, lng=-1.8410038,
        hours=["10:00 AM – 11:30 PM", "4:00 – 11:30 PM", "12:00 – 11:30 PM", "10:00 AM – 11:30 PM",
               "9:30 AM – 11:30 PM", "9:30 AM – 11:30 PM", "10:00 AM – 11:00 PM"],
        wants="menu",
    ),
]

THEMES = {
    # brand = the shop-front band, on = text on it, accent = the main button, aon = text on the button, tint = soft panel
    "barber":  dict(brand="#14233B", on="#FFFFFF", accent="#C8322B", aon="#FFFFFF", tint="#EEF2F7", soft="#B9C6D8"),
    "cafe":    dict(brand="#1E4A3B", on="#FFFFFF", accent="#F2C14E", aon="#1A1A14", tint="#EFF5F1", soft="#B5CDC2"),
    "carwash": dict(brand="#0B4FB3", on="#FFFFFF", accent="#FFD23F", aon="#10203A", tint="#EAF2FD", soft="#B9D2F5"),
    "phone":   dict(brand="#1B2433", on="#FFFFFF", accent="#FF7A1A", aon="#1A0F04", tint="#F1F3F6", soft="#BFC6D1"),
    "indian":  dict(brand="#4A1230", on="#FFFFFF", accent="#F0A81C", aon="#2A1206", tint="#F7EFF3", soft="#D9BCCB"),
    "bar":     dict(brand="#0F3D3E", on="#FFFFFF", accent="#EDB9A1", aon="#1F1410", tint="#ECF3F3", soft="#B4CFCF"),
}

NT_PHONE = "07856 075882"
NT_EMAIL = "hello@nextthreadautomation.co.uk"
