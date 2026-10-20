# Roadmap · Ideen für später

Ideen, die ausgearbeitet, aber noch nicht entschieden oder umgesetzt sind. Umsetzen erst nach Entscheidung der Owner.
Stand der Plattform-Angaben: Oktober 2026. Preise und Regeln der Plattformen ändern sich oft, vor dem Start neu prüfen.

## 1. Aktivisten-Feed: alle Videos an einem Ort

**Idee:** Eine Seite zeigt die neuesten Videos und Posts der Aktivisten (TikTok, Instagram, X). Unterstützer finden sie schnell,
liken und kommentieren sie, ohne lange in der App zu suchen.

**Was geht und was nicht**
| Teil | Machbar? | Warum |
|---|---|---|
| Liste der neuesten Videos | ja | Aktivisten melden ihre Links (Formular im Discord, Datei im Repo) oder die Liste wird aus den Profilen in `content/social.json` gepflegt |
| Vorschaubild und Titel | ja, beim Bauen | TikTok und X bieten oEmbed ohne Login. Das Build-Skript holt Bild und Titel einmal und speichert sie in `site/`. Der Besucher lädt nichts von fremden Servern |
| Ein Klick öffnet das Video direkt in der App | ja | normaler Link auf das Video; auf dem Handy öffnet er die App genau dort |
| Liken und Kommentieren direkt auf unserer Seite | **nein** | TikTok hat dafür keine Schnittstelle. Instagram erlaubt Kommentare nur unter eigenen Posts eines Business-Kontos, Likes gar nicht. X erlaubt es nur über ein Login jedes Nutzers bei unserer App (kostenpflichtige API, rund 0,015 $ pro Antwort) |
| Videos auf unserer Seite abspielen | nur mit Bruch unserer Regeln | Einbetten lädt Skripte und Cookies von TikTok/Meta/X. Das widerspricht der Datenschutzerklärung und der Content Security Policy |

**Risiko:** Organisiertes Liken nach Liste kann gegen die Regeln der Plattformen gegen künstliche Interaktion verstoßen. Im schlimmsten Fall
werden die Konten der Aktivisten gedrosselt. Deshalb: zum Anschauen und echten Kommentieren einladen, nicht zum "Like-Abarbeiten".

**Vorschlag in Stufen**
1. *Sofort, gratis:* Ein Kanal im Discord oder in der WhatsApp-Gruppe, in dem neue Videos gepostet werden. Kein Code nötig.
2. *Website:* Seite "Unterstützen" mit den Videos der letzten 14 Tage, als Kacheln mit Vorschaubild. Gepflegt über eine Datei
   (`content/feed.json`), aktualisiert per Pull Request oder wöchentlich durch ein Skript. Passt zu den bestehenden Regeln (statisch, nichts von fremden Servern).
3. *Später, optional:* Automatisches Einsammeln der neuen Videos. TikTok erlaubt das nur, wenn jeder Aktivist unserer App selbst Zugriff gibt (Display API).
   Braucht eine App-Prüfung bei TikTok und einen Ort für Zugangsdaten außerhalb des Repos.

**Aufwand:** Stufe 2 etwa 1 bis 2 Tage. Stufe 3 deutlich mehr, plus laufende Pflege.

## 2. Monats-Inspiration: die erfolgreichsten Posts zu Veganismus, Antinatalismus und Efilismus

**Idee:** Einmal im Monat eine Sammlung der beliebtesten TikToks, Instagram-Posts und X-Posts zu diesen Themen.
Die Aktivisten sehen, welche Formate, Aufhänger und Längen gerade funktionieren, und lassen sich davon inspirieren.

**Datenzugang**
| Quelle | Machbar? | Bedingungen |
|---|---|---|
| TikTok Research API | eher nein | nur für Hochschulen und eingetragene gemeinnützige Organisationen (EU), Antrag, keine kommerzielle Nutzung. Pro Extinction ist kein eingetragener Verein |
| TikTok Creative Center (Trend-Seite für Werbende) | ja, von Hand | zeigt beliebte Hashtags und Videos, ohne Schnittstelle |
| Instagram Hashtag-Suche (Graph API) | ja | braucht ein Business- oder Creator-Konto, eine Meta-App mit Prüfung; höchstens 30 Hashtags pro 7 Tage, liefert "Top Media" je Hashtag |
| X Suche (API) | ja, kostet | Abrechnung pro gelesenem Post (rund 0,005 $). 1.000 Posts im Monat kosten etwa 5 $ |
| Scraping (automatisches Auslesen der Seiten) | nicht empfohlen | verstößt gegen die Regeln der Plattformen, wird schnell blockiert (bei der Link-Prüfung im Oktober 2026 antwortete Instagram sofort mit Sperren) |

**Datenschutz:** Die Posts gehören fremden Personen. Nur Links und eigene kurze Beschreibungen weitergeben, keine Kopien der Videos.
Am besten intern (Discord) statt öffentlich auf der Website.

**Vorschlag in Stufen**
1. *Sofort, gratis:* Eine Person sammelt einmal im Monat von Hand 10 Beispiele pro Thema (TikTok Creative Center, Instagram- und X-Suche)
   und lässt eine KI zusammenfassen, warum sie funktionieren (Aufhänger, Länge, Format, Ton). Ergebnis als Beitrag im Discord.
2. *Halbautomatisch:* Instagram Hashtag-Suche und X-Suche per Skript, einmal im Monat (GitHub Actions oder Cloudflare Worker mit Zeitplan).
   TikTok bleibt Handarbeit. Kosten für X ein paar Dollar im Monat.
3. *Später:* Antrag für die TikTok Research API, falls Pro Extinction ein eingetragener Verein wird.

**Aufwand:** Stufe 1 etwa 1 bis 2 Stunden im Monat. Stufe 2 etwa 2 bis 3 Tage einmalig.

## Was die Owner vorher entscheiden müssen
1. Ob überhaupt etwas Automatisches läuft: Zugangsdaten (API-Schlüssel) dürfen nicht ins Repo (`AGENTS.md`), sie bräuchten einen geschützten Ort
   (GitHub Secrets oder Cloudflare), und jemand muss sie verwalten.
2. Öffentlich auf der Website oder nur intern (Discord)?
3. Ob die Datenschutzerklärung angepasst werden muss (nur nötig, wenn die Website Daten von fremden Servern lädt oder Besucherdaten verarbeitet).

## 3. Entwicklungs-Branch `develop` und Vorschau auf dev.proextinction.com

**Idee:** Neue Änderungen gehen zuerst auf `develop` und sind auf dev.proextinction.com zu sehen. Auf `main` (die echte Seite) kommt nur, was über `develop` geprüft wurde.

- **Branch:** `develop` aus dem heutigen `main` anlegen (kann die KI).
- **Nur Jonas und James mergen:** GitHub → *Settings* → *Rules* → *Rulesets* für `main` und `develop`: nur per Pull Request, `check` muss grün sein, kein Löschen, kein Force-Push, Merge nur für die Org-Owner (Bypass-Liste).
  Privates Repo: braucht GitHub Team (rund 4 $ pro Person und Monat), öffentliches Repo: gratis.
- **Auf `main` nur von `develop`:** keine Einstellung bei GitHub. Lösung: kleine Prüfung im Workflow, die rot wird, wenn ein Pull Request auf `main` nicht von `develop` kommt; im Ruleset als Pflicht-Check eintragen.
- **dev.proextinction.com:** zweiter Cloudflare Worker (z. B. `proextinction-dev`), gleiches Repo, Production-Branch `develop`, Custom Domain `dev.proextinction.com`.
  Empfohlen: per Cloudflare Access nur für eure E-Mail-Adressen sichtbar (bis 50 Personen gratis).
- **Suchmaschinen:** Die Dev-Seite muss gesperrt bleiben (sonst doppelte und ungeprüfte Inhalte bei Google). Der Build braucht dafür einen Schalter, der `develop` immer auf "noindex" setzt.
- **Regeln für die KI:** `AGENTS.md` anpassen (Pull Requests auf `develop`, nur `develop` auf `main`). Das ändert ein Owner selbst.
- **Offene Pull Requests** danach auf `develop` umstellen.

**Stand:** besprochen, noch nicht entschieden.

## 4. Suchmaschinen und Domain

- **Erledigt:** Website für Suchmaschinen freigeschaltet (`INDEXABLE = True`, Oktober 2026).
- **Google zeigt noch den alten Stand** (alte Google-Sites-Seite, "keine Informationen verfügbar"). Wird mit dem nächsten Besuch von Google neu eingelesen.
- **Google Search Console:** Domain `proextinction.com` bestätigen (TXT-Eintrag in Cloudflare DNS), Sitemap `https://proextinction.com/sitemap.xml` einreichen,
  `https://proextinction.com/en/` per *URL-Prüfung* → *Indexierung beantragen*. Optional dasselbe in den Bing Webmaster Tools.
- **www auf die Domain ohne www umleiten:** www liefert heute eine eigene Kopie aus. Cloudflare → *Rules* → *Redirect Rules*: Hostname `www.proextinction.com`
  → `https://proextinction.com${http.request.uri.path}`, 301, Query-String behalten.
- Zuständig: James (Cloudflare-Konto) oder Jonas mit Zugang (siehe 5).

## 5. Cloudflare-Zugang für Jonas

- Kein geteiltes Passwort: James lädt Jonas ein (*Manage Account* → *Members* → *Invite*).
- Rollen: "Administrator Read Only" (nur ansehen) oder "Administrator" (alles einstellen, Abrechnung bleibt bei James).
- Nur für die Domain: domain-bezogene Rolle (z. B. "Domain Administrator", Scope nur `proextinction.com`), falls der Tarif sie anbietet.
- Nur für den Worker geht nicht: Workers-Rechte gelten für alle Workers im Konto.
- Falls James im Konto auch anderes hat: eigenes Cloudflare-Konto nur für Pro Extinction, Domain und Worker dorthin umziehen, beide Administrator.
- Jonas: Zwei-Faktor-Anmeldung einschalten.

## 6. Weitere offene Punkte (warten auf Entscheidung der Owner)

- **Quiz vor der WhatsApp-Gruppe:** Absage-Text um "Sorry, you didn't make it" ergänzen? (Heute: freundlicher Text plus "You can still help: share our website!")
- **PR #7 (Cloudflare Workers):** schließen, nur die Doku behalten oder nur den Sicherheitsabschnitt aus `HOSTING.md` entfernen (er sollte vor einem öffentlichen Repo weg).
- **Vorschau-Builds bei Pull Requests** schlagen bei Cloudflare immer fehl (die echte Seite aus `main` geht). Ursache in den Worker-Einstellungen bei Cloudflare suchen.
- **`CODEOWNERS`:** James (`idoinejd`) eintragen, sobald er die Einladung als Org-Owner angenommen hat.
- **Datenschutzerklärung kürzen** (Abschnitte "Kontakt per E-Mail", "Deine Rechte"): nur nach Bestätigung.
- **Cartoon-Bild im FAQ** (Bild 31, moralische Subjektivität): unscharf hinter einem Klick wie die Bilder bei "Suffering in detail"?
- **Dependabot PR #1** (actions/checkout 4.2.2 → 7.0.1): prüfen und mergen oder schließen.
- **Repo öffentlich oder GitHub Team:** nötig für Rulesets (siehe 3).
