# DEPLOY — goldenboy-rochester (Goldenboy, Rochester NY)

Built 2026-11-25 on card t_4efaf504. Banked (built + deployed, NOT yet pitched) — recipient window closed (America/New_York 23:00 at deploy-finish), send parked to 2026-11-28 (Sat) 07:30 EST.

## What shipped
Template v2 vitrine (10 files: index, cocktails, kitchen, nights, our-story, visit, contact, privacy + thanks + 404; sitemap carries 8 locs), hand-rolled espresso-ink/marigold-gold design — retro-1970s cocktail bar, unique art direction, zero JS, no sibling look-alike.

- Generators: `build_pages.py` (pages), `make_og.py` (og.png 1200×630, marigold sunburst + "Stay Golden.").
- Facts only from card-body sources: 650 Park Ave (press+GBP), soft open Thanksgiving weekend 11-27/29 with grand opening to follow, retro-1970s modern, DJs on vinyl most nights, chef + bartender recruited from Shell, press menu items named with NO prices on-site (prices not verified), manager Daniel Rehor quote on cocktails/kitchen/nights, owners Eric Rozestraten / Jay Speranza / Ron Billitier named on index + our-story. NO phone number anywhere on the site (never verified — CTAs mail goldenboyrochester@gmail.com).
- JSON-LD: index = Restaurant+BarOrPub with geo 43.1483561,-77.5783136 (Nominatim-geocoded 650 Park Ave), hours, hasMap, sameAs FB; Service nodes on 4 detail pages; FAQPage on visit; BreadcrumbList on every page; priceRange omitted (nothing verified to anchor it).
- Keyless Maps embed on visit page. noindex meta on every route incl. 404/thanks (demo rule) + X-Robots-Tag verified live — see checks.
- Contact form → server.js Brevo v3 HTTP API relay (htmlContent/textContent) → jarvis+websites lane box; 303 → /thanks.
- Pixel: GET /open?t=<token> → 200 image/gif 43B; pixel.gif byte-identical with sibling lineage. favicon.svg present.

## Checks (all PASS, executed 2026-11-25)
- tidy clean all pages; `_verify.py public <origin>` 0 flags.
- Live 200-walk on goldenboy-rochester-demo.up.railway.app: html pages 200 with titles + correct content-types, /open 200 image/gif, missing path 404, X-Robots-Tag: noindex on pages.
- Contact form live POST: 303 → /thanks and the lane mailbox received the relayed CONTACT message (IMAP read-back, unique token sweep-token-gb1).
- Render sweep DOM (render_sweep.py): pages × {390,768,1280} — 20/20 gates, overflow_px=0 everywhere, header visible on all shots, map iframe exactly 1 on /visit, 404 renders as real page, console clean apart from the intentional 404 resource line. 22 pngs + vision-results.json in `shots/` (durable copy under this dir).
- Vision sign-off: OG image clean (all texts legible, sunburst motif judged intentional); index_desktop NO DEFECTS; contact_desktop: 2 low-res claims FALSE, 1 REAL defect (info-column heading offset vs form card inner heading line) → fixed via cinfo padding-top, redeployed, re-sweep PASS, re-vision ALIGNED + NO DEFECTS. OpenRouter batch battery on the sweep shots produced leads adjudicated against native full-res reads — per-shot verdicts recorded in shots/vision-results.json; no unresolved lead.

## Deploy topology
- Repo: `github.com/gnaritas/goldenboy-rochester` (public, no secrets). HEAD d1970a1.
- Railway: service `goldenboy-rochester` id `f8036504-9bfd-4e6a-a66d-0681c6c3e22e` CO-HOSTED inside dead-shell project **the-plain-bar** `604a72a9-09eb-4169-920d-e64619651640` (account project cap; sibling capitol-locksmith-demo service shares the project — teardown of this site = GraphQL serviceDelete ONLY, never project delete).
- Domain: goldenboy-rochester-demo.up.railway.app; canonical/og:url/sitemap/robots pin the live -demo host (production token re-pinned, _verify sitemap-vs-origin tripwire clean).
- Env: BREVO_API_KEY set from secrets via xkeysib-onward extraction.
- lane.db: deploys + services rows written through sites_agency_state.py; `export` + `verify` all five files IDENTICAL, rc 0.

## Pitch state (send pending in-window)
- Staged trio at projects/websites/: `_pitch_goldenboy-rochester.md` (106 core words, 2 links + 1 pixel img), `.envelope.json`, `_pitch_goldenboy-rochester.send.py` — clone of the proven jeyas specimen (arm-coin pre-assert: sha256%2=1 → v7 "Website demo for Goldenboy"; giacobbe no-redirect HAS-SITE probes on goldenboyrochester.com/.net/.us + goldenboybar.com; MX google.com; registry guard email+alias clean; envelope-resume guard; ASCII-stem IMAP read-back; registry append AT send + recount; lane.db events mirror at physical line; pilot row v7/brand_new nudge 2026-12-04 mature 2026-12-11).
- Dry-run (--check-only) PASS today. FB email re-check is warning-class only: anonymous FB reads are login-gated intermittently (page throttled after ~10 anonymous fetches today) — an anonymous miss cannot distinguish gated from removed; the 2026-11-25 logged-out provenance read stands and a dead gmail address reveals itself as a bounce.
- Offer: founder bundle $249 + $39/mo 31-day trial on live Stripe link plink_1UfHjNLvO6Vx44saQoPtWrFV (buy.stripe.com/6oU14o98pcpZgrU7UT3ks0a) + utm_content/client_reference_id goldenboy-rochester-t1. No new Stripe object.
- Recipient tz seeded America/New_York (source 650 Park Ave); send day 2026-11-28 (Thanksgiving 11-26/27 pair skipped per ladder convention; weekend pitch sends proven legitimate — 6 in-window precedent).
- Homonyms excluded: Golden Boy Adelaide AU, Golden Boy LA, boxing @goldenboy — registry carries zero hits; aliases city-tied.

## Teardown bar (GARBAGE RULE)
If owner opts out or the ladder dies: serviceDelete f8036504-9bfd-4e6a-a66d-0681c6c3e22e (NOT project delete — shell hosts capitol-locksmith), gh repo delete gnaritas/goldenboy-rochester, rm sites tree, sites_agency_state.py delete deploy+service, export.
