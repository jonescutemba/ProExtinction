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
