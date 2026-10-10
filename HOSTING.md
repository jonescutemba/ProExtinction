# Hosting the new site on Cloudflare Pages

A one-time setup of about 10 minutes, done in the Cloudflare account that already holds `proextinction.com`.
It's free, and there is no server or software to maintain. Cloudflare serves the finished files from the `site/` folder of the GitHub repository.
Every change pushed to GitHub goes live automatically, and you can roll back any change yourself.

## 1. Give Cloudflare access to the repository
Cloudflare needs permission to read the GitHub repository. Only the repository's owner can grant it.
- **Recommended:** move the repository into a free GitHub organisation for Pro Extinction (github.com → *Your organizations* → *New organization* → Free), with both of us as owners. Then neither the code nor the domain depends on one person. GitHub redirects the old links automatically.
- **Otherwise:** the current owner approves the Cloudflare GitHub app for this repository when Cloudflare asks in step 2.

## 2. Create the Pages project
1. Cloudflare dashboard → **Workers & Pages** → **Create** → **Pages** → **Connect to Git** (or *Import an existing Git repository*).
2. Choose **GitHub**, sign in and allow access to the `proextinction` repository only.
3. Settings:
   | Field | Value |
   |---|---|
   | Project name | `proextinction` |
   | Production branch | `main` |
   | Framework preset | **None** |
   | Build command | *leave empty* |
   | Build output directory | `site` |
4. **Save and Deploy.** After about a minute the site is online at `https://proextinction.pages.dev`.

## 3. Connect the domain
1. In the Pages project → **Custom domains** → **Set up a custom domain** → `proextinction.com`. Then add a second one: `www.proextinction.com`.
2. Cloudflare offers to replace the old DNS records that point to Google Sites (the `A` records and the `CNAME` for `www` → `ghs.googlehosted.com`). Accept.
   **Leave the `MX` and `TXT` records alone.** They are for email, and email keeps working as before.
3. Send `www` to the address without www: **Rules** → **Redirect Rules** → **Create rule** → template **"Redirect from WWW to root"** → Deploy.
4. After a few minutes `https://proextinction.com` shows the new site, with HTTPS done by Cloudflare.

## 4. Afterwards
- **Changes:** anyone with write access to the repository can change the site, with or without the help of AI. Each push to `main` goes live within a minute or two.
- **Previews:** a push to any other branch gets its own preview address (`<branch>.proextinction.pages.dev`). The live site doesn't change until that branch is merged into `main`.
- **Undo:** Pages project → **Deployments** → open an older deployment → **Rollback to this deployment**.
- **The old Google Site** stays where it is at its `sites.google.com` address. Old English links like `proextinction.com/manifesto` forward to the new pages.
- **Search engines:** the site starts hidden from Google on purpose, until the legal notice and privacy policy are filled in. That is switched on in the code, not in Cloudflare (see `DEPLOY.md`). Once it is switched on:
  - Cloudflare → **Caching** → **Configuration** → turn on **Crawler Hints**. It tells Bing and other search engines about changes right away (IndexNow), free.
  - Add the site to **Google Search Console** (search.google.com/search-console, *Domain* property; Cloudflare can add the verification record for you) and submit `https://proextinction.com/sitemap.xml`. The same for **Bing Webmaster Tools**, which can import it from Search Console.
