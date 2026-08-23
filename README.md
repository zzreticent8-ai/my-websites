# The GreenHouseSheShed Stories — Website

Static site for Kim Wild's children's book series, *The GreenHouseSheShed Stories* (thegreenhousesheshed.com).

Plain HTML/CSS/JS — no build step, no framework. Open `index.html` directly or serve the folder with any static host.

## Pages

- `index.html` — Home
- `books.html` — All 7 books (Magic Series + Discover Adventure Series)
- `about.html` — About Kim Wild + the real GreenHouseSheShed story
- `contact.html` — Contact form + social links

## Adding the real photos & cover art

The site ships with styled placeholder covers (title + icon on a gradient) so it looks finished immediately. Drop real image files into `assets/images/` using these **exact filenames** and they'll swap in automatically — no code changes needed:

| File | Used for |
|---|---|
| `assets/images/author-kim-wild.jpg` | Author headshot (Home + About) |
| `assets/images/covers/book-1-the-magical-world.jpg` | Book 1 — The Magical World in The GreenHouseSheShed |
| `assets/images/covers/book-2-miss-bluebeary.jpg` | Book 2 — Miss Bluebeary Moves In Next Door |
| `assets/images/covers/book-3-nighttime-magic.jpg` | Book 3 — Nighttime Magic in The GreenHouseSheShed |
| `assets/images/covers/book-4-musical-magic.jpg` | Book 4 — Musical Magic and Sunny Friends |
| `assets/images/covers/book-5-where-fairies-fly.jpg` | Book 5 — Where Fairies Fly and Magic Lives |
| `assets/images/covers/book-6-adventure-alley.jpg` | Book 6 — Adventure Alley |
| `assets/images/covers/book-7-wayfinder-trail.jpg` | Book 7 — Wayfinder Trail |

Recommended: square (1:1) JPGs for covers, at least 800×800px. Portrait (4:5) for the author photo.

## Contact / newsletter forms

Both forms currently fall back to opening the visitor's email client (`mailto:hello@thegreenhousesheshed.com`) since there's no backend wired up. To capture submissions for real, swap in a form service such as Formspree, Mailchimp, or ConvertKit:

1. Replace the placeholder email in `assets/js/main.js`, or
2. Point the `<form>` tags in `index.html` / `contact.html` at your provider's endpoint and remove the JS `preventDefault()` handler for that form.

## Deployment

Any static host works — Hostinger file manager/FTP, GitHub Pages, Netlify, Vercel, etc. Just upload the whole folder (keeping the `assets/` structure intact).
