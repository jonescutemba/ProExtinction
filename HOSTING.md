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
- **Search engines:** the site starts hidden from Google on purpose, until we decide to go public. That is switched on in the code, not in Cloudflare (see `DEPLOY.md`). Once it is switched on:
  - Cloudflare → **Caching** → **Configuration** → turn on **Crawler Hints**. It tells Bing and other search engines about changes right away (IndexNow), free.
  - Add the site to **Google Search Console** (search.google.com/search-console, *Domain* property; Cloudflare can add the verification record for you) and submit `https://proextinction.com/sitemap.xml`. The same for **Bing Webmaster Tools**, which can import it from Search Console.

## 5. Account and domain security (5 minutes, recommended)
The website itself has no login, database or forms, so the main way to attack it is through the accounts behind it.
- **Two-factor login** on the Cloudflare account and on every GitHub account with access. For the GitHub organisation: *Settings* → *Authentication security* → **Require two-factor authentication**.
- **DNSSEC:** Cloudflare → the domain → **DNS** → **Settings** → **Enable DNSSEC**. It stops others from faking the domain's DNS answers. If the domain is registered at Cloudflare, that's all; otherwise copy the DS record it shows to the registrar.
- **DMARC (email spoofing):** the domain has SPF but no DMARC, so anyone can send mail that claims to come from `@proextinction.com`. Add a DNS record of type `TXT`, name `_dmarc`:
  - if nobody sends email *from* the domain (Cloudflare Email Routing only forwards incoming mail): `v=DMARC1; p=reject;`
  - if someone does send from `info@proextinction.com` (e.g. "send as" in Gmail): start with `v=DMARC1; p=none;` and fix SPF for that sender first.

## 6. Who can publish: owners and contributors
Goal: the two of us are owners. Other people (and their AI tools) can change the site and propose changes, but nothing goes live until one of us merges it.
All of this is free and set up once in GitHub, in the organisation from step 1.

**People**
- Organisation → *People*: both of us **Owner**. Everyone else **Member** (they get no rights to settings).
- Organisation → *Teams* → *New team*: `owners` (both of us) and `contributors`. Repository → *Settings* → *Collaborators and teams*: `owners` **Admin**, `contributors` **Write**.
  Write lets people push branches and open pull requests, not change settings. Occasional helpers need no access at all: they fork the repository and open a pull request from their fork.
- Replace the names in `.github/CODEOWNERS` with `@<organisation>/owners`.

**Protect `main`** (Repository → *Settings* → *Rules* → *Rulesets* → *New branch ruleset*)
| Setting | Value |
|---|---|
| Name / Enforcement | `main is live` / **Active** |
| Target branches | *Include default branch* |
| Restrict deletions, Block force pushes | on |
| Require a pull request before merging | on, **1** approval, **Require review from Code Owners**, *Dismiss stale approvals when new commits are pushed* on, *Require conversation resolution* on |
| Require status checks to pass | on, add **`check`**, *Require branches to be up to date* on |
| Bypass list | *Repository admin*, mode **For pull requests only**. Then an owner still needs a pull request and a green `check`, but can merge their own without waiting for the other owner. Remove it if you want every change seen by both of us. |

**GitHub Actions** (Repository → *Settings* → *Actions* → *General*)
- *Fork pull request workflows from outside collaborators*: **Require approval for all external contributors**.
- *Workflow permissions*: **Read repository contents**, and leave *Allow GitHub Actions to create and approve pull requests* **off**.

**Cloudflare previews**
Every pushed branch gets a public preview address (`<branch>.proextinction.pages.dev`, hidden from search engines). That is handy for review, but anyone with the link can see unreviewed changes. To keep previews private: Pages project → *Settings* → *General* → **Enable access policy** (Cloudflare Access, free, only the e-mail addresses you allow). Or turn previews off: *Settings* → *Builds & deployments* → *Preview branch control* → **None**.

**AI agents**
They work like any contributor, on branches and through pull requests, with the rules in `AGENTS.md`. Never give an agent an owner's token, and don't install apps that can merge or push to `main`.
