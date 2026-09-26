# PrimoHome landing page (UAT)

Public marketing landing page for PrimoHome, deployed via GitHub Pages for UAT.

This is a static copy of `ui/saas-ui/public/landing.html` from the private
[`bookingsystem`](https://github.com/sandeepsmakes/bookingsystem) repo, published
here because GitHub Pages requires a public repo on the free plan.

**Source of truth is `bookingsystem`.** When the landing page changes there,
copy `landing.html` (renamed to `index.html`) and `assets/primohome/` here and
push, rather than editing this repo independently.

The enquiry form posts directly to the backend's ngrok tunnel
(`https://handbag-storage-superjet.ngrok-free.dev/channels/web/enquiry`) —
UAT-only wiring; see issue [#37](https://github.com/sandeepsmakes/bookingsystem/issues/37)
in `bookingsystem` for the real HTTPS/domain plan before go-live.
