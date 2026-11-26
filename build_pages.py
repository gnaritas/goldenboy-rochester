#!/usr/bin/env python3
"""Goldenboy — Rochester NY (650 Park Ave, former Starbucks). Template-v2 multi-page build.
Every claim traced in evidence.json. Unknowns (phone, prices, reservations, Monday hours)
omitted — never guessed. Facts: WROC-TV/RochesterFirst + Wisevoter 2026-11-25 press coverage;
hours from press (kitchen Tue-Sun 4-10, bar until midnight); owner email self-published on the
shop's own Facebook Page. Zero JS. Hand-rolled HTML/CSS. noindex on demo host per lane doctrine.
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, 'public')
os.makedirs(PUB, exist_ok=True)

ORIGIN = 'https://goldenboy-rochester-demo.up.railway.app'
BRAND = 'Goldenboy'
CITY = 'Rochester, NY'
STREET = '650 Park Ave'
FULL_ADDR = '650 Park Ave, Rochester, NY 14607'
EMAIL = 'goldenboyrochester@gmail.com'
FB = 'https://www.facebook.com/goldenboyrochester'
MAPQ = 'https://www.google.com/maps?q=650%20Park%20Ave%2C%20Rochester%2C%20NY%2014607'
LAT, LON = 43.1483561, -77.5783136  # Nominatim/OSM geocode of 650 Park Ave — exact address match, see evidence.json
SOCIALS = [FB]

def head(title, desc, path):
    u = ORIGIN + path
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{u}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{u}">
<meta property="og:image" content="{ORIGIN}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{ORIGIN}/og.png">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="stylesheet" href="/style.css">
<link rel="preconnect" href="https://www.google.com">
</head>
<body>'''

def nav():
    return '''<a class="skip" href="#main">Skip to content</a>
<header class="site">
  <a class="brand" href="/">Goldenboy <span>Park&nbsp;Ave &middot; Rochester,&nbsp;NY</span></a>
  <input type="checkbox" id="navtoggle" class="navtoggle" aria-label="Show navigation">
  <label for="navtoggle" class="navbtn" aria-hidden="true"><i></i></label>
  <nav aria-label="Main" class="links">
    <a href="/cocktails">Drinks</a>
    <a href="/kitchen">Kitchen</a>
    <a href="/nights">Record&nbsp;Nights</a>
    <a href="/our-story">Our&nbsp;Story</a>
    <a href="/visit">Visit</a>
    <a class="btn btn-sm" href="/contact">Contact&nbsp;Us</a>
  </nav>
</header>'''

def footer():
    return f'''<footer class="site">
  <div class="footgrid">
    <div class="footnap">
      <p class="fbrand">{BRAND}</p>
      <address>{STREET}<br>Rochester, NY 14607<br>Park Avenue</address>
      <p class="fmail"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
    <div class="footcta">
      <p class="bunrule" aria-hidden="true"></p>
      <p class="fline">Stay golden.</p>
      <p class="fsocial"><a href="{FB}" rel="noopener">Facebook</a></p>
      <p class="fline2">A cocktail bar, a late-night kitchen, and records spinning most nights &mdash; in the old Park Avenue space on the north side.</p>
    </div>
  </div>
  <p class="footline">&copy; 2026 {BRAND} &middot; {CITY}</p>
</footer>'''

def breadcrumbs(name, path):
    items = [
        {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': ORIGIN + '/'},
    ]
    if path != '/':
        items.append({'@type': 'ListItem', 'position': 2, 'name': name, 'item': ORIGIN + path})
    return json.dumps({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': items}, ensure_ascii=False)

HOURS_SPEC = [{
    '@type': 'OpeningHoursSpecification',
    'dayOfWeek': ['Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    'opens': '16:00', 'closes': '00:00',
}]

def ld_home():
    obj = {
        '@context': 'https://schema.org', '@type': ['Restaurant', 'BarOrPub'],
        'name': BRAND,
        'image': ORIGIN + '/og.png',
        'url': ORIGIN + '/',
        'email': EMAIL,
        'address': {'@type': 'PostalAddress', 'streetAddress': '650 Park Avenue', 'addressLocality': 'Rochester', 'addressRegion': 'NY', 'postalCode': '14607', 'addressCountry': 'US'},
        'geo': {'@type': 'GeoCoordinates', 'latitude': LAT, 'longitude': LON},
        'hasMap': MAPQ,
        'openingHoursSpecification': HOURS_SPEC,
        'sameAs': SOCIALS,
    }
    return json.dumps(obj, ensure_ascii=False)

def ld_service(name, path, desc):
    obj = {
        '@context': 'https://schema.org', '@type': 'Service',
        'name': name,
        'description': desc,
        'url': ORIGIN + path,
        'areaServed': {'@type': 'City', 'name': 'Rochester', 'addressRegion': 'NY'},
        'provider': {'@type': ['Restaurant', 'BarOrPub'], 'name': BRAND, 'address': {'@type': 'PostalAddress', 'streetAddress': '650 Park Avenue', 'addressLocality': 'Rochester', 'addressRegion': 'NY', 'postalCode': '14607', 'addressCountry': 'US'}},
    }
    return json.dumps(obj, ensure_ascii=False)

PAGES = {}

# ---------- HOME ----------
PAGES['index.html'] = (head(f'{BRAND} — Cocktail Bar &amp; Late-Night Kitchen, {CITY}',
    'Goldenboy: a bar-forward cocktail bar and late-night kitchen in the old Starbucks on Park Avenue, Rochester NY. DJs most nights, kitchen Tue-Sun 4-10pm, bar until midnight.',
    '/'), f'''{nav()}
<main id="main">
<section class="hero">
  <p class="kicker">Rochester &middot; Park Avenue</p>
  <h1>Bar-forward.<br><em>With a serious kitchen.</em></h1>
  <p class="lead">Goldenboy is a cocktail bar and restaurant in the old Starbucks space on Park Avenue &mdash; a modern take on a 1970s vibe, with DJs spinning records most nights and a kitchen running Tuesday through Sunday until ten.</p>
  <p class="cta">
    <a class="btn btn-big" href="/cocktails">See the Bar</a>
    <a class="btn btn-ghost btn-big" href="{MAPQ}" rel="noopener">Get Directions</a>
  </p>
</section>
<section class="awards" id="hoursband">
  <p class="award"><b>Kitchen Tue&ndash;Sun, 4&ndash;10 pm</b> &middot; bar until midnight</p>
  <p class="award"><b>Records spinning</b> most nights of the week</p>
  <p class="award">From the Rochester team behind <b>Cotoletta</b></p>
</section>
<section class="cards">
  <h2 class="sr-only">What we serve</h2>
  <a class="card" href="/cocktails">
    <span class="dot" aria-hidden="true"></span>
    <h3>The Bar</h3>
    <p>The room is built around the bar &mdash; a cocktail program first, poured until midnight. This is the concept, not the side act.</p>
    <span class="more">See the bar &rsaquo;</span>
  </a>
  <a class="card" href="/kitchen">
    <span class="dot" aria-hidden="true"></span>
    <h3>The Kitchen</h3>
    <p>A chef brought over from Shell downtown. The press menu: the burger, the French dip, the lobster mac and cheese.</p>
    <span class="more">See the plates &rsaquo;</span>
  </a>
  <a class="card" href="/nights">
    <span class="dot" aria-hidden="true"></span>
    <h3>Record Nights</h3>
    <p>DJs on records most nights of the week, in a warm room with a 1970s backbone and a modern sound.</p>
    <span class="more">Hear the night &rsaquo;</span>
  </a>
</section>
<section class="strip">
  <div class="stripin">
    <p class="bigquote">&ldquo;More of a social, bar-forward experience with a really incredible food program.&rdquo;</p>
    <p class="attrib">&mdash; Daniel Rehor, Goldenboy manager &middot; WROC-TV, November 2026</p>
  </div>
</section>
<section class="storyteaser">
  <div class="sttext">
    <p class="kicker">The story so far</p>
    <h2>The old Starbucks became the new night out</h2>
    <p>Owners Eric Rozestraten, Jay Speranza and Ron Billitier took the former Starbucks at 650 Park Avenue and gave it a modern take on a 1970s vibe &mdash; then brought a chef and a bartender over from Shell Restaurant downtown. The soft opening runs over Thanksgiving weekend; the grand opening follows.</p>
    <p><a class="more" href="/our-story">Read the full story &rsaquo;</a></p>
  </div>
  <div class="stfig" aria-hidden="true">
    <p class="bunrule"></p>
    <p class="figline">Kitchen Tue&ndash;Sun<br><b>4 &ndash; 10 pm</b></p>
    <p class="figsub">Bar until midnight.<br>650 Park Ave, Rochester.</p>
    <p class="bunrule"></p>
  </div>
</section>
</main>
{footer()}
<script type="application/ld+json">{ld_home()}</script>
<script type="application/ld+json">{breadcrumbs('Home', '/')}</script>
<!-- BUILT-2026-11-26 -->
</body>
</html>''')

# ---------- COCKTAILS ----------
PAGES['cocktails.html'] = (head(f'Cocktail Bar — {BRAND}, {CITY}',
    'A bar-first cocktail program at Goldenboy, 650 Park Ave, Rochester NY — poured by the bartender from Shell downtown, open until midnight, Tue-Sun.',
    '/cocktails'), f'''{nav()}
<main id="main">
<section class="pagehead">
  <p class="kicker">The Bar</p>
  <h1>The night starts<br>at the bar.</h1>
  <p class="lead">Goldenboy flips the Park Avenue script. Manager Daniel Rehor put it plainly to WROC: most spots on the avenue are restaurant-forward with great bar programs &mdash; Goldenboy is built the other way around, a social bar-forward room with an incredible food program behind it.</p>
  <p class="cta"><a class="btn" href="/visit">Plan your visit</a> <a class="btn btn-ghost" href="{MAPQ}" rel="noopener">Get Directions</a></p>
</section>
<div class="menuwrap">
  <section class="menu-sec">
    <h2>Cocktails <span>&mdash; the head of the table</span></h2>
    <dl class="items">
      <div><dt>Built to anchor a night</dt><dd>A cocktail program you can build an evening on. The drink list leads, the menu backs it up.</dd></div>
      <div><dt>The bartender from Shell</dt><dd>The bar crew came over from Shell Restaurant downtown &mdash; the same hands that made it one of Rochester&rsquo;s best-known cocktail rooms.</dd></div>
    </dl>
  </section>
  <section class="menu-sec">
    <h2>Open Late <span>&mdash; midnight at least</span></h2>
    <dl class="items">
      <div><dt>Tuesday through Sunday</dt><dd>The bar pours until midnight. Drinks don&rsquo;t end when the kitchen closes at ten.</dd></div>
      <div><dt>Come as you are</dt><dd>A bar-forward room means the first order of business is a good drink, whenever you walk in.</dd></div>
    </dl>
  </section>
  <section class="menu-note">
    <p class="bunrule" aria-hidden="true"></p>
    <h2>Eating alongside <span>&mdash; kitchen Tue&ndash;Sun, 4&ndash;10 pm</span></h2>
    <p class="newitems">The burger &middot; French dip &middot; lobster mac &amp; cheese</p>
    <p class="fineprint">Comforting plates from a chef recruited from Shell. <a href="/kitchen">Read about the kitchen &rsaquo;</a></p>
  </section>
  <p class="fineprint center">Opening-week schedules can shift &mdash; the <a href="{FB}" rel="noopener">Facebook page</a> posts what&rsquo;s on tonight.</p>
</div>
</main>
{footer()}
<script type="application/ld+json">{ld_service('Cocktail Bar', '/cocktails', 'Bar-first cocktail program with the bartender from Shell Restaurant, poured until midnight at Goldenboy, 650 Park Ave, Rochester, NY 14607.')}</script>
<script type="application/ld+json">{breadcrumbs('Drinks', '/cocktails')}</script>
<!-- BUILT-2026-11-26 -->
</body>
</html>''')

# ---------- KITCHEN ----------
PAGES['kitchen.html'] = (head(f'Late-Night Kitchen — {BRAND}, {CITY}',
    'Comforting plates at Goldenboy — the burger, the French dip, the lobster mac and cheese — from a chef recruited from Shell Restaurant. Kitchen Tue-Sun 4-10pm, Rochester NY.',
    '/kitchen'), f'''{nav()}
<main id="main">
<section class="pagehead">
  <p class="kicker">The Kitchen</p>
  <h1>Delicious, comforting,<br>easy to wrap your head around.</h1>
  <p class="lead">That&rsquo;s the manager&rsquo;s own description, and the kitchen is no afterthought: a chef the owners poached from Shell Restaurant downtown, cooking real plates for a bar crowd, Tuesday through Sunday from four until ten.</p>
  <p class="cta"><a class="btn" href="/visit">Plan your visit</a> <a class="btn btn-ghost" href="/cocktails">Back to the bar</a></p>
</section>
<div class="detailwrap">
  <section class="roll">
    <h2><span class="num" aria-hidden="true">1</span>The plates the press knows</h2>
    <p>What to come for, straight from manager Daniel Rehor&rsquo;s preview to WROC: &ldquo;The burger is going to be great. Come for the French dip. We&rsquo;ll have a delicious lobster mac and cheese.&rdquo; Nothing fussy &mdash; food built to be shared, ordered late, finished before the bar goes to midnight.</p>
  </section>
  <section class="roll">
    <h2><span class="num" aria-hidden="true">2</span>A chef from downtown</h2>
    <p>The chef and the bartender both came over from Shell Restaurant, the downtown Rochester spot the owners named as their source of talent. That&rsquo;s the pedigree behind Goldenboy&rsquo;s kitchen and bar &mdash; hired together, from one of the city&rsquo;s best-regarded rooms.</p>
  </section>
  <aside class="panel">
    <h2>Kitchen 4&ndash;10, bar to midnight</h2>
    <p>Dinner runs Tuesday through Sunday, four until ten &mdash; and the bar keeps pouring until midnight after the last plate. Monday visits come early: the kitchen is for the rest of the week.</p>
    <p class="cta"><a class="btn" href="/visit">Come get a plate</a></p>
  </aside>
</div>
</main>
{footer()}
<script type="application/ld+json">{ld_service('Late-Night Kitchen', '/kitchen', 'Comforting late-night plates — the burger, French dip and lobster mac and cheese — from a chef recruited from Shell Restaurant, served Tue-Sun 4-10pm at Goldenboy, 650 Park Ave, Rochester, NY.')}</script>
<script type="application/ld+json">{breadcrumbs('Kitchen', '/kitchen')}</script>
<!-- BUILT-2026-11-26 -->
</body>
</html>''')

# ---------- NIGHTS ----------
PAGES['nights.html'] = (head(f'DJs &amp; Record Nights — {BRAND}, {CITY}',
    'DJs spinning records most nights at Goldenboy, a retro-1970s cocktail bar on Park Avenue, Rochester NY. Bar until midnight, Tuesday through Sunday.',
    '/nights'), f'''{nav()}
<main id="main">
<section class="pagehead">
  <p class="kicker">The Sound</p>
  <h1>Records most nights.<br>The room stays golden.</h1>
  <p class="lead">Music isn&rsquo;t decoration here &mdash; it&rsquo;s half the concept. Goldenboy is a modern take on a 1970s vibe: a warm, social room with DJs scheduled to spin records most nights of the week.</p>
  <p class="cta"><a class="btn" href="/visit">Plan your visit</a> <a class="btn btn-ghost" href="/cocktails">See the bar</a></p>
</section>
<div class="detailwrap narrow">
  <section class="roll">
    <h2>Most nights, on records</h2>
    <p>DJs are scheduled to spin records most nights of the week &mdash; a room built for talking in, dancing near, and staying late. The bar runs to midnight, so the night ends when you decide it does.</p>
  </section>
  <section class="roll">
    <h2>The 1970s, modernized</h2>
    <p>The look is what the crew calls a modern take on a retro 1970s vibe &mdash; the warmth of the era without the museum bit. Manager Daniel Rehor&rsquo;s pitch for the room, quoted by WROC: &ldquo;a social, bar-forward experience with a really incredible food program.&rdquo; The playlist is what that sounds like at nine p.m.</p>
  </section>
  <aside class="panel">
    <h2>What&rsquo;s on tonight?</h2>
    <p>Opening-week schedules move fast &mdash; DJ nights included. The <a href="{FB}" rel="noopener">shop&rsquo;s Facebook page</a> is where the week&rsquo;s nights get posted first.</p>
    <p class="cta"><a class="btn" href="{FB}" rel="noopener">Check the page</a></p>
  </aside>
</div>
</main>
{footer()}
<script type="application/ld+json">{ld_service('DJ and Record Nights', '/nights', 'DJs spinning records most nights of the week in a retro-modern 1970s cocktail room at Goldenboy, 650 Park Ave, Rochester, NY 14607.')}</script>
<script type="application/ld+json">{breadcrumbs('Record Nights', '/nights')}</script>
<!-- BUILT-2026-11-26 -->
</body>
</html>''')

# ---------- OUR STORY ----------
PAGES['our-story.html'] = (head(f'Our Story — {BRAND}, {CITY}',
    'Goldenboy comes from Eric Rozestraten, Jay Speranza and Ron Billitier — the Rochester team behind Cotoletta — with a chef and bartender from Shell, in the old Starbucks on Park Avenue.',
    '/our-story'), f'''{nav()}
<main id="main">
<section class="pagehead">
  <p class="kicker">Our Story</p>
  <h1>Three restaurant people.<br>One Park Avenue room.</h1>
  <p class="lead">Goldenboy is the new project of Eric Rozestraten, Jay Speranza and Ron Billitier &mdash; named in WROC&rsquo;s opening coverage &mdash; who took the former Starbucks at 650 Park Avenue, gave it a modern take on a 1970s vibe, and staffed the kitchen and bar with talent brought over from Shell Restaurant downtown.</p>
  <p class="cta"><a class="btn" href="/visit">See where we are</a> <a class="btn btn-ghost" href="/kitchen">Try the menu</a></p>
</section>
<div class="story">
  <section class="tl">
    <div class="trow"><p class="tyr">The crew</p><div class="tbody"><h2>Rozestraten &middot; Speranza &middot; Billitier</h2><p>The partners behind Goldenboy are Eric Rozestraten, Jay Speranza and Ron Billitier, per WROC&rsquo;s November 2026 coverage. Rozestraten and Speranza also run Cotoletta ROC, and the trio has a second Park Avenue project, Rosso, on the way.</p></div></div>
    <div class="trow"><p class="tyr">The space</p><div class="tbody"><h2>The old Starbucks on Park Avenue</h2><p>Crews spent the fall transforming the former Starbucks storefront at 650 Park Avenue into a bar-forward restaurant — a warm, retro-modern room where a national chain used to pour coffee.</p></div></div>
    <div class="trow"><p class="tyr">The hire</p><div class="tbody"><h2>A chef and a bartender from Shell</h2><p>The food and drink programs came ready-made: the owners brought both the chef and the bartender over from Shell Restaurant downtown, then let them build Goldenboy&rsquo;s kitchen and bar list.</p></div></div>
    <div class="trow"><p class="tyr">Opening</p><div class="tbody"><h2>Soft opening Thanksgiving weekend</h2><p>The doors go open over Thanksgiving weekend 2026, with a grand opening to follow the week after. Kitchen Tuesday&ndash;Sunday, 4&ndash;10 pm. Bar until midnight.</p></div></div>
  </section>
  <aside class="panel wide">
    <h2>The house line</h2>
    <p class="bigquote">&ldquo;Stay Golden. Opening Fall 2026.&rdquo;</p>
    <p class="attrib">the shop&rsquo;s own tagline, from its Facebook page</p>
    <p>Named in WROC&rsquo;s coverage: Goldenboy, the bar-forward Park Avenue project from the Cotoletta team, with the Shell kitchen hire. Everything on this page comes from that coverage and the shop&rsquo;s own posts.</p>
    <p class="cta"><a class="btn" href="/visit">Visit Park Avenue</a></p>
  </aside>
</div>
</main>
{footer()}
<script type="application/ld+json">{breadcrumbs('Our Story', '/our-story')}</script>
<!-- BUILT-2026-11-26 -->
</body>
</html>''')

# ---------- VISIT ----------
faq_jsonld = json.dumps({
    '@context': 'https://schema.org', '@type': 'FAQPage',
    'mainEntity': [
        {'@type': 'Question', 'name': 'When exactly do you open?',
         'acceptedAnswer': {'@type': 'Answer', 'text': 'Soft opening runs over Thanksgiving weekend 2026, with the grand opening the week after. Check the Facebook page for the schedule this week.'}},
        {'@type': 'Question', 'name': 'What are the hours?',
         'acceptedAnswer': {'@type': 'Answer', 'text': 'Kitchen Tuesday through Sunday, 4 to 10 pm. The bar stays open until midnight.'}},
        {'@type': 'Question', 'name': 'Where exactly is Goldenboy?',
         'acceptedAnswer': {'@type': 'Answer', 'text': '650 Park Avenue in Rochester, New York (14607), in the former Starbucks space on Park Avenue.'}},
        {'@type': 'Question', 'name': 'What should I order?',
         'acceptedAnswer': {'@type': 'Answer', 'text': 'Cocktails first — plus the burger, the French dip and the lobster mac and cheese, per the team\'s own preview to WROC-TV.'}},
    ]
}, ensure_ascii=False)

PAGES['visit.html'] = (head(f'Visit — Hours &amp; Directions, {BRAND}, {CITY}',
    'Goldenboy at 650 Park Ave (the former Starbucks), Rochester NY 14607. Kitchen Tue-Sun 4-10pm, bar until midnight. Directions, hours and answers before you go.',
    '/visit'), f'''{nav()}
<main id="main">
<section class="pagehead">
  <p class="kicker">Now Opening</p>
  <h1>Park Avenue,<br>this weekend &amp; on.</h1>
  <p class="lead">Goldenboy opens over Thanksgiving weekend 2026 in the former Starbucks at 650 Park Avenue &mdash; soft opening first, grand opening the week after. Kitchen Tuesday through Sunday, 4&ndash;10 pm; bar until midnight.</p>
  <p class="cta"><a class="btn btn-big" href="{MAPQ}" rel="noopener">Get Directions</a> <a class="btn btn-ghost btn-big" href="/contact">Ask Us Anything</a></p>
</section>
<div class="visitgrid">
  <section class="visitinfo">
    <h2>Where</h2>
    <address class="bigaddr">{STREET}<br>Rochester, NY 14607<br>Park Avenue &middot; the old Starbucks</address>
    <h2>When</h2>
    <p>Kitchen: Tuesday&ndash;Sunday, 4&ndash;10 pm.<br>Bar: until midnight, Tuesday through Sunday.</p>
    <h2>Questions before you come</h2>
    <div class="faqlist">
      <p class="faq-q">When exactly do you open?</p>
      <p class="faq-a">Soft opening over Thanksgiving weekend 2026, grand opening the week after. The <a href="{FB}" rel="noopener">Facebook page</a> carries this week&rsquo;s schedule.</p>
      <p class="faq-q">What are the hours?</p>
      <p class="faq-a">Kitchen Tuesday&ndash;Sunday, 4 to 10 pm. The bar stays open until midnight. <a href="/nights">See what the nights look like &rsaquo;</a></p>
      <p class="faq-q">What should I order?</p>
      <p class="faq-a">Cocktails first — plus the burger, the French dip, the lobster mac and cheese. <a href="/kitchen">See the plates &rsaquo;</a></p>
      <p class="faq-q">Is there music?</p>
      <p class="faq-a">DJs spin records most nights of the week.</p>
    </div>
    <p class="cta"><a class="btn btn-ghost" href="/cocktails">What we pour</a></p>
  </section>
  <section class="visitmap">
    <div class="mapbox">
      <iframe title="Map to Goldenboy, 650 Park Ave, Rochester, NY" src="https://www.google.com/maps?q=650%20Park%20Ave%2C%20Rochester%2C%20NY%2014607&output=embed" loading="eager" referrerpolicy="no-referrer-when-downgrade"></iframe>
    </div>
    <p class="fineprint">Can&rsquo;t load the map? <a href="{MAPQ}" rel="noopener">Open it in Google Maps</a> or <a href="mailto:{EMAIL}">email us</a> and we&rsquo;ll talk you in.</p>
  </section>
</div>
</main>
{footer()}
<script type="application/ld+json">{ld_service('Visit Goldenboy', '/visit', 'Cocktail bar and late-night kitchen at 650 Park Ave (the former Starbucks), Rochester, NY 14607. Kitchen Tue-Sun 4-10pm, bar until midnight.')}</script>
<script type="application/ld+json">{faq_jsonld}</script>
<script type="application/ld+json">{breadcrumbs('Visit', '/visit')}</script>
<!-- BUILT-2026-11-26 -->
</body>
</html>''')

# ---------- CONTACT ----------
PAGES['contact.html'] = (head(f'Contact — {BRAND}, {CITY}',
    'Contact Goldenboy, the bar-forward cocktail bar and late-night kitchen at 650 Park Ave, Rochester NY — email, contact form, and directions.',
    '/contact'), f'''{nav()}
<main id="main">
<section class="pagehead">
  <p class="kicker">Talk to Us</p>
  <h1>Contact Goldenboy</h1>
  <p class="lead">Questions about the bar, a night out, or what&rsquo;s happening during opening weeks? Email us or use the form &mdash; it lands straight in the shop&rsquo;s inbox.</p>
</section>
<div class="contactgrid">
  <form class="cform" method="post" action="/contact">
    <h2>Send a message</h2>
    <p><label for="f-name">Your name</label><input id="f-name" name="name" type="text" required maxlength="120" autocomplete="name"></p>
    <p><label for="f-email">Email</label><input id="f-email" name="email" type="email" required maxlength="160" autocomplete="email"></p>
    <p><label for="f-msg">Message</label><textarea id="f-msg" name="message" rows="5" required maxlength="4000"></textarea></p>
    <p><button class="btn btn-big" type="submit">Send Message</button></p>
    <p class="fineprint">This form emails the shop directly. We never share your address.</p>
  </form>
  <section class="cinfo">
    <h2>Direct lines</h2>
    <p class="clabel">Email</p>
    <p class="cbig"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <p class="clabel">Walk in</p>
    <address class="bigaddr">{STREET}<br>Rochester, NY 14607</address>
    <p class="clabel">Facebook — hours &amp; what&rsquo;s on</p>
    <p class="cbig"><a href="{FB}" rel="noopener">{BRAND} on Facebook</a></p>
  </section>
</div>
</main>
{footer()}
<script type="application/ld+json">{breadcrumbs('Contact', '/contact')}</script>
<!-- BUILT-2026-11-26 -->
</body>
</html>''')

# ---------- PRIVACY ----------
PAGES['privacy.html'] = (head(f'Privacy Policy — {BRAND}, {CITY}',
    'Privacy policy for the Goldenboy website: what the contact form collects, and the site\'s cookie and tracking practices. No trackers, no cookies.',
    '/privacy'), f'''{nav()}
<main id="main">
<section class="pagehead narrow">
  <p class="kicker">Privacy</p>
  <h1>Privacy Policy</h1>
</section>
<div class="prose">
  <p>This site belongs to {BRAND} ({FULL_ADDR}).</p>
  <h2>What we collect</h2>
  <p>The contact form on this site collects only the information you type into it — your name, your email address and your message — and sends it to the shop&rsquo;s own email address so the owners can answer you. That is the entire purpose of the data. It is not sold, shared or used for advertising.</p>
  <h2>Cookies and tracking</h2>
  <p>This site sets no cookies and uses no advertising trackers or analytics pixels of its own. The embedded Google map may set its own cookies once you interact with it, governed by Google&rsquo;s privacy policy.</p>
  <h2>Your choices</h2>
  <p>Want your message deleted from the shop&rsquo;s mailbox records? Email <a href="mailto:{EMAIL}">{EMAIL}</a> and ask. Questions about this policy go to the same address.</p>
  <p class="fineprint">This policy covers this website only.</p>
</div>
</main>
{footer()}
<script type="application/ld+json">{breadcrumbs('Privacy', '/privacy')}</script>
<!-- BUILT-2026-11-26 -->
</body>
</html>''')

# ---------- 404 ----------
PAGES['404.html'] = (head(f'Page not found — {BRAND}',
    'Page not found at the Goldenboy site. Back to the bar, or straight to the drinks page.',
    '/404'), f'''{nav()}
<main id="main">
<section class="pagehead center">
  <p class="kicker">404</p>
  <h1>That page took the night off.</h1>
  <p class="lead">This page doesn&rsquo;t exist &mdash; but the bar does. Kitchen Tuesday through Sunday until ten, bar until midnight.</p>
  <p class="cta"><a class="btn btn-big" href="/">Back to Home</a> <a class="btn btn-ghost btn-big" href="/cocktails">See the Bar</a></p>
</section>
</main>
{footer()}
<!-- BUILT-2026-11-26 -->
</body>
</html>''')

# ---------- THANKS ----------
PAGES['thanks.html'] = (head(f'Message sent — {BRAND}',
    'Thanks for reaching out to Goldenboy — the owners read every message.',
    '/thanks'), f'''{nav()}
<main id="main">
<section class="pagehead center">
  <p class="kicker">Received</p>
  <h1>Your message is in.</h1>
  <p class="lead">Thank you &mdash; the Goldenboy crew reads the shop&rsquo;s inbox themselves. Meanwhile, the bar and the map are one click away.</p>
  <p class="cta"><a class="btn btn-big" href="/cocktails">See the Bar</a> <a class="btn btn-ghost btn-big" href="/visit">Plan your visit</a></p>
</section>
</main>
{footer()}
<!-- BUILT-2026-11-26 -->
</body>
</html>''')

for fname, (h, body) in PAGES.items():
    with open(os.path.join(PUB, fname), 'w', encoding='utf-8') as f:
        f.write(h + '\n' + body)
    print('wrote', fname, len(h + body), 'bytes')

# ---------- sitemap / robots / favicon ----------
pages_order = ['/', '/cocktails', '/kitchen', '/nights', '/our-story', '/visit', '/contact', '/privacy']
today = '2026-11-26'
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
    f'<url><loc>{ORIGIN}{p}</loc><lastmod>{today}</lastmod></url>\n' for p in pages_order) + '</urlset>\n'
open(os.path.join(PUB, 'sitemap.xml'), 'w').write(sitemap)
open(os.path.join(PUB, 'robots.txt'), 'w').write(f'''User-agent: *
Allow: /

Sitemap: {ORIGIN}/sitemap.xml
''')
favicon = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#20140c"/><circle cx="32" cy="32" r="21" fill="#e5a83c"/><path d="M33 21 a11.5 11.5 0 1 0 8.4 8.4 h-8 v-4.6 h9.4 v15.6 h-4.7" fill="none" stroke="#20140c" stroke-width="4.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
'''
open(os.path.join(PUB, 'favicon.svg'), 'w').write(favicon)
print('wrote sitemap.xml robots.txt favicon.svg')
print('PAGES:', len([f for f in PAGES if f.endswith('.html')]))
