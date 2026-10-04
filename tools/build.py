"""Build the three design concepts (all languages) into concepts/<concept>/<lang>/*.html."""
import json, re, html, pathlib, sys, urllib.parse
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from blocks import blocks_of, abridge, faq_pairs

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'concepts'
esc = html.escape

LANGS = ['en', 'de', 'pl', 'es', 'it', 'fr', 'pt', 'ru', 'zh', 'hi', 'ar', 'bn', 'ur', 'id']   # English is the source; other languages fill gaps with AI translations
FULL_AI = {'fr', 'pt', 'ru', 'zh', 'hi', 'ar', 'bn', 'ur', 'id'}   # no original site: every page is AI-translated, marked once in the language picker
LANG_NAME = {'en': 'English', 'de': 'Deutsch', 'pl': 'Polski', 'es': 'Español', 'it': 'Italiano',
             'fr': 'Français', 'pt': 'Português', 'ru': 'Русский', 'zh': '中文', 'hi': 'हिन्दी',
             'ar': 'العربية', 'bn': 'বাংলা', 'ur': 'اردو', 'id': 'Bahasa Indonesia'}
RTL = {'ar', 'ur'}   # written right to left: pages get dir="rtl" and the CSS mirrors
DIR = lambda l: 'rtl' if l in RTL else 'ltr'
KINDS = {'home': 'home', 'basic-faq': 'faq', 'full-faq': 'faq'}  # by English slug, default 'doc'
AI_MARK = ' (AI)'

# Per language: (slug, English slug or None for pages only that language has, menu label, original slug or None if AI-translated).
# Order follows the English menu; language-only pages go last.
SITE = {
 'en': [(s, s, l, s) for s, l in [
  ('home', 'Home'), ('manifesto', 'Manifesto'), ('basic-faq', 'Basic FAQ'), ('full-faq', 'Full FAQ'),
  ('criticism-of-different-pro-life-ideologies', 'Criticism of pro-life ideologies'),
  ('principles-of-the-movement', 'Principles of the movement'), ('suffering-in-detail', 'Suffering in detail'),
  ('cosmic-extinction', 'Cosmic Extinction'), ('history', 'History'), ('join-us', 'Join us'),
  ('social-media-channels', 'Social Media Channels'), ('contact', 'Contact'), ('donate', 'Donate')]],
 'de': [
  ('home', 'home', 'Home', 'home'), ('manifest', 'manifesto', 'Manifest', 'manifest'),
  ('basis-faq', 'basic-faq', 'Basis-FAQ', 'basis-faq'), ('vollstaendiges-faq', 'full-faq', 'Vollständiges FAQ', 'vollständiges-faq'),
  ('kritik-an-pro-life-ideologien', 'criticism-of-different-pro-life-ideologies', 'Kritik an Pro-Life-Ideologien', None),
  ('die-prinzipien-unserer-bewegung', 'principles-of-the-movement', 'Die Prinzipien unserer Bewegung', 'die-prinzipien-unserer-bewegung'),
  ('leid-im-detail', 'suffering-in-detail', 'Leid im Detail', 'leid-im-detail'),
  ('kosmische-extinction', 'cosmic-extinction', 'Kosmische Extinction', None),
  ('geschichte', 'history', 'Geschichte', 'geschichte'), ('aktiv-werden', 'join-us', 'Aktiv werden', 'aktiv-werden'),
  ('social-media', 'social-media-channels', 'Social-Media-Kanäle', None), ('kontakt', 'contact', 'Kontakt', 'kontakt'),
  ('spenden', 'donate', 'Spenden', None), ('ressourcen', None, 'Ressourcen', 'resourcen')],
 'pl': [
  ('home', 'home', 'Home', 'home'), ('komunikat', 'manifesto', 'Komunikat', 'komunikat'),
  ('basic-faq', 'basic-faq', 'Basic FAQ', 'basic-faq'), ('full-faq', 'full-faq', 'Full FAQ', 'full-faq'),
  ('krytyka-ideologii-pro-life', 'criticism-of-different-pro-life-ideologies', 'Krytyka ideologii pro-life', None),
  ('zasady-ruchu', 'principles-of-the-movement', 'Zasady ruchu', 'zasady-ruchu'),
  ('znaczenie-cierpienia', 'suffering-in-detail', 'Znaczenie cierpienia', 'znaczenie-cierpienia'),
  ('kosmiczne-wyginiecie', 'cosmic-extinction', 'Kosmiczne wyginięcie', None),
  ('historia', 'history', 'Historia', 'historia'), ('z-nami', 'join-us', 'Z nami', 'z-nami'),
  ('profile-aktywistyczne', 'social-media-channels', 'Profile aktywistyczne', 'profile-aktywistyczne'),
  ('kontakt', 'contact', 'Kontakt', 'kontakt'), ('darowizny', 'donate', 'Przekaż darowiznę', None),
  ('zasoby', None, 'Zasoby', 'zasoby')],
 'es': [
  ('home', 'home', 'Página inicial', 'página-inicial'), ('manifiesto', 'manifesto', 'Manifiesto', 'manifiesto'),
  ('pmf-basicas', 'basic-faq', 'PMF básicas', 'pmf-básicas'), ('pmf-completas', 'full-faq', 'PMF completas', 'pmf-completas'),
  ('critica-ideologias-provida', 'criticism-of-different-pro-life-ideologies', 'Crítica de las ideologías provida', None),
  ('principios-del-movimiento', 'principles-of-the-movement', 'Principios del movimiento', None),
  ('sufrimiento-en-detalle', 'suffering-in-detail', 'El sufrimiento en detalle', None),
  ('extincion-cosmica', 'cosmic-extinction', 'Extinción cósmica', None),
  ('historia', 'history', 'Historia', 'historia'), ('equipo', 'join-us', 'Equipo', 'equipo'),
  ('redes-sociales', 'social-media-channels', 'Redes sociales', None), ('contacto', 'contact', 'Contacto', 'contacto'),
  ('donar', 'donate', 'Donar', None), ('recursos', None, 'Recursos', 'recursos'), ('mapa-del-sitio', None, 'Mapa del sitio', 'mapa-del-sitio')],
 'it': [
  ('home', 'home', 'Home', 'home'), ('manifesto', 'manifesto', 'Manifesto', 'manifesto'),
  ('faq-di-base', 'basic-faq', 'FAQ di base', 'faq-di-base'), ('faq-completo', 'full-faq', 'FAQ completo', 'faq-completo'),
  ('critica-ideologie-pro-vita', 'criticism-of-different-pro-life-ideologies', 'Critica delle ideologie pro-vita', None),
  ('principi-del-movimento', 'principles-of-the-movement', 'Principi del movimento', 'principi-del-movimento'),
  ('la-sofferenza-nei-dettagli', 'suffering-in-detail', 'La sofferenza nei dettagli', 'la-sofferenza-nei-dettagli'),
  ('estinzione-cosmica', 'cosmic-extinction', 'Estinzione cosmica', None),
  ('storia', 'history', 'Storia', 'storia'), ('unisciti-a-noi', 'join-us', 'Unisciti a noi', 'unisciti-a-noi'),
  ('canali-social', 'social-media-channels', 'Canali social', None), ('contatti', 'contact', 'Contatti', None),
  ('donazioni', 'donate', 'Donazioni', 'donazioni')],
}
# Menu labels of the fully AI-translated languages, in English menu order (slugs stay English).
AI_MENU = {
 'fr': ['Accueil', 'Manifeste', 'FAQ de base', 'FAQ complète', 'Critique des idéologies pro-vie', 'Principes du mouvement',
        'La souffrance en détail', 'Extinction cosmique', 'Histoire', 'Nous rejoindre', 'Réseaux sociaux', 'Contact', 'Faire un don'],
 'pt': ['Início', 'Manifesto', 'FAQ básico', 'FAQ completo', 'Crítica das ideologias pró-vida', 'Princípios do movimento',
        'O sofrimento em detalhe', 'Extinção cósmica', 'História', 'Junte-se a nós', 'Redes sociais', 'Contato', 'Doar'],
 'ru': ['Главная', 'Манифест', 'Основные вопросы', 'Все вопросы', 'Критика идеологий pro-life', 'Принципы движения',
        'Страдание в деталях', 'Космическое вымирание', 'История', 'Присоединяйтесь', 'Соцсети', 'Контакты', 'Пожертвовать'],
 'zh': ['首页', '宣言', '基础问答', '完整问答', '批判各种 pro-life 意识形态', '运动原则', '苦难详述', '宇宙灭绝', '历史',
        '加入我们', '社交媒体', '联系', '捐款'],
 'hi': ['होम', 'घोषणापत्र', 'बुनियादी FAQ', 'पूरा FAQ', 'प्रो-लाइफ़ विचारधाराओं की आलोचना', 'आंदोलन के सिद्धांत',
        'पीड़ा विस्तार से', 'ब्रह्मांडीय विलुप्ति', 'इतिहास', 'हमसे जुड़ें', 'सोशल मीडिया', 'संपर्क', 'दान करें'],
 'ar': ['الرئيسية', 'البيان', 'أسئلة أساسية', 'كل الأسئلة', 'نقد أيديولوجيات pro-life', 'مبادئ الحركة',
        'المعاناة بالتفصيل', 'الانقراض الكوني', 'التاريخ', 'انضم إلينا', 'وسائل التواصل', 'تواصل معنا', 'تبرّع'],
 'bn': ['হোম', 'ইশতেহার', 'প্রাথমিক FAQ', 'সম্পূর্ণ FAQ', 'প্রো-লাইফ মতাদর্শের সমালোচনা', 'আন্দোলনের নীতি',
        'দুঃখভোগ বিস্তারিত', 'মহাজাগতিক বিলুপ্তি', 'ইতিহাস', 'আমাদের সাথে যোগ দিন', 'সোশ্যাল মিডিয়া', 'যোগাযোগ', 'দান করুন'],
 'ur': ['ہوم', 'منشور', 'بنیادی سوالات', 'تمام سوالات', 'پرو لائف نظریات پر تنقید', 'تحریک کے اصول',
        'تکلیف تفصیل سے', 'کائناتی معدومیت', 'تاریخ', 'ہمارے ساتھ شامل ہوں', 'سوشل میڈیا', 'رابطہ', 'عطیہ کریں'],
 'id': ['Beranda', 'Manifesto', 'FAQ dasar', 'FAQ lengkap', 'Kritik ideologi pro-life', 'Prinsip gerakan',
        'Penderitaan secara rinci', 'Kepunahan kosmik', 'Sejarah', 'Bergabung', 'Media sosial', 'Kontak', 'Donasi'],
}
for _l, _labels in AI_MENU.items():
    SITE[_l] = [(s, s, lab, None) for (s, _, _, _), lab in zip(SITE['en'], _labels)]
ORIGINAL = {'en': 'https://www.proextinction.com/{}', 'de': 'https://sites.google.com/view/proextinctionwebsitegerman/{}',
            'pl': 'https://sites.google.com/view/proextinction-website-polish/{}',
            'es': 'https://sites.google.com/view/proextinction-website-spanish/{}',
            'it': 'https://sites.google.com/view/proextinction-website-italian/{}'}
AI = {l: {s for s, _, _, o in SITE[l] if o is None} for l in LANGS}
PAGES = {l: [(s, KINDS.get(e, 'doc')) for s, e, _, _ in SITE[l]] for l in LANGS}
NAV = {l: {s: lab + (AI_MARK if s in AI[l] and l not in FULL_AI else '') for s, _, lab, _ in SITE[l]} for l in LANGS}
CODE = {l: l.upper() + (AI_MARK if l in FULL_AI else '') for l in LANGS}   # picker label, e.g. 'RU (AI)'
EN_OF = {l: {s: e for s, e, _, _ in SITE[l]} for l in LANGS}          # slug -> English slug
OF_EN = {l: {e: s for s, e, _, _ in SITE[l] if e} for l in LANGS}     # English slug -> slug
ORIG = {l: {s: o for s, _, _, o in SITE[l]} for l in LANGS}

def counterpart(lang, slug, other):
    """Slug of the same page in another language, or 'home'."""
    return OF_EN[other].get(EN_OF[lang].get(slug) or '', 'home')

T = {
 'en': dict(menu='Menu', skip='Skip to content', lang='Language', theme='Switch light/dark mode',
  tagline='Together, we end suffering.', sub='The organisation dedicated to ending forced existence and suffering',
  cta1='Join us', cta2='Read the manifesto', mission='Our Mission',
  mission_text='Preventing as much suffering as physically possible, without tradeoffs.',
  effort='Effort', questions='Questions?', questions_text='Contact info@proextinction.com to get more information on the project',
  action='Take action', toc='On this page', abridged='Preview: the long list of channels is left out in this concept. The full list is on the current site:',
  abridged_link='Open the full page', ki='Machine-translated from English (AI).',
  ki_tag='AI', back='Concepts', back_title='Back to the concept overview', progress='Reading progress', home_link='Pro Extinction – home',
  efforts=['Growing the movement to make it possible to prevent billions of years of suffering.',
   'Universal, non-discriminatory help for as many victims as physically possible. For animals, as much extraterrestrial life as possible, and humans.',
   'Purely organised action/activism based. No lamenting at the expense of the victims.',
   'Fully rational, empathetic, atheistic, logical, and fair.'],
  foot='Pro Extinction · Global', page_title='Pro Extinction'),
 'de': dict(menu='Menü', skip='Zum Inhalt springen', lang='Sprache', theme='Hell/Dunkel umschalten',
  tagline='Together, we end suffering.', sub='Die Organisation, die sich für das Ende erzwungener Existenz und erzwungenen Leids einsetzt.',
  cta1='Aktiv werden', cta2='Manifest lesen', mission='Unsere Mission',
  mission_text='Wir zielen darauf ab, ohne Kompromisse, so viel Leid wie möglich zu beenden.',
  effort='Einsatz', questions='Fragen?', questions_text='Kontaktiere info@proextinction.com, um mehr Informationen zu bekommen.',
  action='Mach mit', toc='Auf dieser Seite', abridged='Vorschau: die lange Kanalliste ist in diesem Konzept weggelassen. Die vollständige Liste steht auf der aktuellen Seite:',
  abridged_link='Vollständige Seite öffnen', ki='KI-Übersetzung aus dem Englischen. Die deutsche Originalseite hat diese Seite nicht.',
  ki_tag='AI', back='Konzepte', back_title='Zurück zur Konzeptübersicht', progress='Lesefortschritt', home_link='Pro Extinction – Startseite',
  efforts=['Wir vergrößern die Bewegung, um unzählige Jahre Leid zu verhindern.',
   'Universelle, nicht diskriminierende Hilfe für so viele Opfer wie physisch möglich. Für Tiere, so viel außerirdisches Leben wie möglich und Menschen.',
   'Wir sind strikt handlungsorientiert, anstatt auf Kosten der Opfer nur über das extreme Leid zu klagen.',
   'Wir sind völlig rational, empathisch, atheistisch, logisch und fair.'],
  foot='Pro Extinction · Global · +44 7557095418', page_title='Pro Extinction'),
 'pl': dict(menu='Menu', skip='Przejdź do treści', lang='Język', theme='Przełącz tryb jasny/ciemny',
  tagline='Together, we end suffering.', sub='Organizacja działająca na rzecz położenia kresu przymusowemu istnieniu i cierpieniu',
  cta1='Dołącz', cta2='Przeczytaj komunikat', mission='Nasza misja',
  mission_text='Zapobieganie cierpieniu w jak największym stopniu, bez żadnych kompromisów.',
  effort='Działanie', questions='Pytania?', questions_text='Skontaktuj się z info@proextinction.com, aby uzyskać więcej informacji na temat projektu',
  action='Dołącz', toc='Na tej stronie', abridged='Podgląd: w tym koncepcie pominięto długą listę kanałów. Pełna lista jest na obecnej stronie:',
  abridged_link='Otwórz pełną stronę', ki='Tłumaczenie maszynowe z angielskiego (AI). Polska wersja strony nie ma tej podstrony.',
  ki_tag='AI', back='Koncepty', back_title='Powrót do przeglądu konceptów', progress='Postęp czytania', home_link='Pro Extinction – strona główna',
  efforts=['Rozwój ruchu, aby umożliwić zapobieżenie miliardom lat cierpienia.',
   'Powszechna, niedyskryminująca pomoc dla jak największej liczby ofiar, na ile to fizycznie możliwe. Dla zwierząt, jak największej liczby form życia więcej niż ziemskiego (czyli wszędzie, gdzie życie może zostać zapobiegnięte od zaistnienia cierpienia w kosmosie) oraz dla ludzi.',
   'Działania oparte wyłącznie na zorganizowanym działaniu/aktywizmie. Żadnego użalania się nad losem ofiar.',
   'W pełni racjonalne, empatyczne, ateistyczne, logiczne i sprawiedliwe.'],
  foot='Pro Extinction · Global', page_title='Pro Extinction'),
 'es': dict(menu='Menú', skip='Ir al contenido', lang='Idioma', theme='Cambiar modo claro/oscuro',
  tagline='Together, we end suffering.', sub='Organización dedicada a poner fin a la existencia impuesta y a su sufrimiento',
  cta1='Únete', cta2='Leer el manifiesto', mission='Nuestra misión',
  mission_text='Minimizar al máximo el sufrimiento, sin concesiones.',
  effort='Línea de acción', questions='¿Preguntas?', questions_text='Contacta con info@proextinction.com para obtener más información sobre el proyecto.',
  action='Actúa', toc='En esta página', abridged='Vista previa: este concepto omite la larga lista de canales. La lista completa está en la web actual:',
  abridged_link='Abrir la página completa', ki='Traducción automática del inglés (AI). La web original en español no tiene esta página.',
  ki_tag='AI', back='Conceptos', back_title='Volver a la vista general de conceptos', progress='Progreso de lectura', home_link='Pro Extinction – página inicial',
  efforts=['Impulsar un crecimiento estratégico del movimiento que permita intervenir de forma efectiva sobre las causas estructurales del sufrimiento y prevenir su perpetuación a gran escala.',
   'Promover un alivio universal, no discriminatorio y basado en criterios de sufrimiento, dirigido al mayor número posible de víctimas: animales no humanos, cualquier forma de vida potencialmente sintiente fuera de la Tierra y la humanidad.',
   'Desarrollar un activismo organizado, disciplinado y orientado a resultados, centrado exclusivamente en la reducción del sufrimiento, sin concesiones emocionales ni discursos que lo perpetúen.',
   'Sostener el movimiento sobre principios estrictamente racionales, empáticos y coherentes, libres de dogmas, creencias infundadas o sesgos arbitrarios, con un compromiso firme con la justicia y la lógica.'],
  foot='Pro Extinction · Global · +44 7557095418', page_title='Pro Extinction'),
 'it': dict(menu='Menu', skip='Vai al contenuto', lang='Lingua', theme='Cambia modalità chiara/scura',
  tagline='Together, we end suffering.', sub="L'organizzazione dedicata a porre fine all'esistenza forzata e alla sofferenza.",
  cta1='Unisciti a noi', cta2='Leggi il manifesto', mission='La nostra missione',
  mission_text='Prevenire quanta più sofferenza sia fisicamente possibile, senza compromessi.',
  effort='Obiettivo', questions='Domande?', questions_text='Contatta info@proextinction.com per ottenere più informazioni sul progetto',
  action='Agisci', toc='In questa pagina', abridged="Anteprima: questo concept omette il lungo elenco dei canali. L'elenco completo è sul sito attuale:",
  abridged_link='Apri la pagina completa', ki="Traduzione automatica dall'inglese (AI). Il sito originale in italiano non ha questa pagina.",
  ki_tag='AI', back='Concept', back_title='Torna alla panoramica dei concept', progress='Avanzamento lettura', home_link='Pro Extinction – home',
  efforts=['Crescere il movimento per rendere possibile la prevenzione di miliardi di anni di sofferenza.',
   'Aiuto universale, non-discriminatorio per quante più vittime sia fisicamente possibile. Per gli animali, quanta più vita extraterrestre possibile, e gli umani.',
   'Basato esclusivamente su azioni/attivismo organizzati. Nessun lamento a spese delle vittime.',
   'Pienamente razionale, empatico, ateo, logico, e giusto.'],
  foot='Pro Extinction · Global', page_title='Pro Extinction'),
}
T.update({
 'fr': dict(menu='Menu', skip='Aller au contenu', lang='Langue', theme='Basculer entre mode clair et sombre',
  tagline='Together, we end suffering.', sub="L'organisation qui se consacre à mettre fin à l'existence forcée et à la souffrance",
  cta1='Nous rejoindre', cta2='Lire le manifeste', mission='Notre mission',
  mission_text='Empêcher autant de souffrance que physiquement possible, sans compromis.',
  effort='Engagement', questions='Des questions ?', questions_text="Écrivez à info@proextinction.com pour en savoir plus sur le projet",
  action='Agir', toc='Sur cette page', abridged="Aperçu : ce concept laisse de côté la longue liste des chaînes. La liste complète se trouve sur le site actuel :",
  abridged_link='Ouvrir la page complète', ki="Traduction automatique de l'anglais (AI). Il n'existe pas de site original en français.",
  ki_tag='AI', back='Concepts', back_title="Retour à l'aperçu des concepts", progress='Progression de lecture', home_link='Pro Extinction – accueil',
  efforts=["Faire grandir le mouvement pour rendre possible la prévention de milliards d'années de souffrance.",
   'Une aide universelle et sans discrimination pour autant de victimes que physiquement possible. Pour les animaux, pour autant de vie extraterrestre que possible et pour les humains.',
   "Une action purement organisée, fondée sur l'activisme. Pas de lamentations aux dépens des victimes.",
   'Entièrement rationnel, empathique, athée, logique et juste.'],
  foot='Pro Extinction · Global', page_title='Pro Extinction'),
 'pt': dict(menu='Menu', skip='Ir para o conteúdo', lang='Idioma', theme='Alternar modo claro/escuro',
  tagline='Together, we end suffering.', sub='A organização dedicada a acabar com a existência forçada e o sofrimento',
  cta1='Junte-se a nós', cta2='Ler o manifesto', mission='Nossa missão',
  mission_text='Evitar o máximo de sofrimento fisicamente possível, sem concessões.',
  effort='Frente', questions='Dúvidas?', questions_text='Escreva para info@proextinction.com para saber mais sobre o projeto',
  action='Aja', toc='Nesta página', abridged='Prévia: este conceito deixa de fora a longa lista de canais. A lista completa está no site atual:',
  abridged_link='Abrir a página completa', ki='Tradução automática do inglês (AI). Não existe um site original em português.',
  ki_tag='AI', back='Conceitos', back_title='Voltar à visão geral dos conceitos', progress='Progresso de leitura', home_link='Pro Extinction – início',
  efforts=['Fazer o movimento crescer para tornar possível evitar bilhões de anos de sofrimento.',
   'Ajuda universal e sem discriminação para o maior número de vítimas fisicamente possível. Para animais, para o máximo possível de vida extraterrestre e para humanos.',
   'Ação puramente organizada, baseada em ativismo. Nada de lamentar à custa das vítimas.',
   'Totalmente racional, empático, ateu, lógico e justo.'],
  foot='Pro Extinction · Global', page_title='Pro Extinction'),
 'ru': dict(menu='Меню', skip='Перейти к содержанию', lang='Язык', theme='Переключить светлую/тёмную тему',
  tagline='Together, we end suffering.', sub='Организация, которая стремится положить конец вынужденному существованию и страданию',
  cta1='Присоединиться', cta2='Читать манифест', mission='Наша миссия',
  mission_text='Предотвратить столько страданий, сколько физически возможно, без компромиссов.',
  effort='Направление', questions='Есть вопросы?', questions_text='Пишите на info@proextinction.com, чтобы узнать больше о проекте',
  action='Действуйте', toc='На этой странице', abridged='Превью: в этом концепте длинный список каналов опущен. Полный список есть на текущем сайте:',
  abridged_link='Открыть полную страницу', ki='Машинный перевод с английского (AI). Оригинального сайта на русском языке нет.',
  ki_tag='AI', back='Концепты', back_title='Назад к обзору концептов', progress='Прогресс чтения', home_link='Pro Extinction – главная',
  efforts=['Развивать движение, чтобы сделать возможным предотвращение миллиардов лет страданий.',
   'Всеобщая помощь без дискриминации для стольких жертв, сколько физически возможно. Для животных, для как можно большего числа внеземной жизни и для людей.',
   'Только организованные действия и активизм. Никаких причитаний за счёт жертв.',
   'Полностью рационально, эмпатично, атеистично, логично и справедливо.'],
  foot='Pro Extinction · Global', page_title='Pro Extinction'),
 'zh': dict(menu='菜单', skip='跳到正文', lang='语言', theme='切换浅色/深色模式',
  tagline='Together, we end suffering.', sub='致力于终结被迫存在与苦难的组织',
  cta1='加入我们', cta2='阅读宣言', mission='我们的使命',
  mission_text='在物理上可能的范围内尽量防止苦难，绝不妥协。',
  effort='方向', questions='有疑问？', questions_text='请联系 info@proextinction.com 了解项目详情',
  action='行动起来', toc='本页内容', abridged='预览：此设计方案省略了较长的频道列表。完整列表见现有网站：',
  abridged_link='打开完整页面', ki='由英文机器翻译 (AI)。原网站没有中文版本。',
  ki_tag='AI', back='方案', back_title='返回设计方案总览', progress='阅读进度', home_link='Pro Extinction – 首页',
  efforts=['壮大运动，让防止数十亿年的苦难成为可能。',
   '为物理上可能的最多受害者提供普遍、无差别的帮助。包括动物、尽可能多的地外生命以及人类。',
   '完全以有组织的行动和行动主义为本。不以受害者为代价空发哀叹。',
   '完全理性、富有同理心、无神论、合乎逻辑且公平。'],
  foot='Pro Extinction · Global', page_title='Pro Extinction'),
 'hi': dict(menu='मेनू', skip='सामग्री पर जाएँ', lang='भाषा', theme='लाइट/डार्क मोड बदलें',
  tagline='Together, we end suffering.', sub='वह संगठन जो थोपे गए अस्तित्व और पीड़ा को ख़त्म करने के लिए समर्पित है',
  cta1='हमसे जुड़ें', cta2='घोषणापत्र पढ़ें', mission='हमारा मिशन',
  mission_text='बिना किसी समझौते के, भौतिक रूप से जितनी हो सके उतनी पीड़ा को रोकना।',
  effort='प्रयास', questions='कोई सवाल?', questions_text='परियोजना के बारे में और जानकारी के लिए info@proextinction.com पर संपर्क करें',
  action='कदम उठाएँ', toc='इस पेज पर', abridged='प्रीव्यू: इस कॉन्सेप्ट में चैनलों की लंबी सूची छोड़ दी गई है। पूरी सूची मौजूदा साइट पर है:',
  abridged_link='पूरा पेज खोलें', ki='अंग्रेज़ी से मशीन अनुवाद (AI)। मूल साइट का हिन्दी संस्करण नहीं है।',
  ki_tag='AI', back='कॉन्सेप्ट', back_title='कॉन्सेप्ट की सूची पर वापस जाएँ', progress='पढ़ने की प्रगति', home_link='Pro Extinction – होम',
  efforts=['आंदोलन को बढ़ाना, ताकि अरबों वर्षों की पीड़ा को रोकना संभव हो सके।',
   'भौतिक रूप से जितने संभव हों उतने पीड़ितों के लिए सार्वभौमिक, बिना भेदभाव की मदद। जानवरों के लिए, जितना हो सके उतने पृथ्वी से बाहर के जीवन के लिए, और इंसानों के लिए।',
   'पूरी तरह संगठित कार्रवाई और एक्टिविज़्म पर आधारित। पीड़ितों की कीमत पर कोई विलाप नहीं।',
   'पूरी तरह तार्किक, सहानुभूतिपूर्ण, नास्तिक, विवेकपूर्ण और न्यायसंगत।'],
  foot='Pro Extinction · Global', page_title='Pro Extinction'),
 'ar': dict(menu='القائمة', skip='انتقل إلى المحتوى', lang='اللغة', theme='التبديل بين الوضع الفاتح والداكن',
  tagline='Together, we end suffering.', sub='المنظمة المكرّسة لإنهاء الوجود القسري والمعاناة',
  cta1='انضم إلينا', cta2='اقرأ البيان', mission='مهمتنا',
  mission_text='منع أكبر قدر ممكن فيزيائيًا من المعاناة، دون تنازلات.',
  effort='محور', questions='لديك أسئلة؟', questions_text='راسلنا على info@proextinction.com لمعرفة المزيد عن المشروع',
  action='تحرّك', toc='في هذه الصفحة', abridged='معاينة: يحذف هذا التصميم القائمة الطويلة للقنوات. القائمة الكاملة موجودة على الموقع الحالي:',
  abridged_link='افتح الصفحة كاملة', ki='ترجمة آلية من الإنجليزية (AI). لا توجد نسخة عربية من الموقع الأصلي.',
  ki_tag='AI', back='التصاميم', back_title='العودة إلى نظرة عامة على التصاميم', progress='تقدّم القراءة', home_link='Pro Extinction – الرئيسية',
  efforts=['تنمية الحركة لكي يصبح منع مليارات السنين من المعاناة ممكنًا.',
   'مساعدة شاملة ودون تمييز لأكبر عدد ممكن فيزيائيًا من الضحايا. للحيوانات، ولأكبر قدر ممكن من الحياة خارج الأرض، وللبشر.',
   'عمل منظّم ونشاط ميداني فقط. لا نوح على حساب الضحايا.',
   'عقلانية تامة وتعاطف وإلحاد ومنطق وعدل.'],
  foot='Pro Extinction · Global', page_title='Pro Extinction'),
 'bn': dict(menu='মেনু', skip='মূল বিষয়ে যান', lang='ভাষা', theme='লাইট/ডার্ক মোড বদলান',
  tagline='Together, we end suffering.', sub='যে সংগঠন জোর করে চাপিয়ে দেওয়া অস্তিত্ব আর দুঃখভোগের অবসানে নিবেদিত',
  cta1='আমাদের সাথে যোগ দিন', cta2='ইশতেহার পড়ুন', mission='আমাদের লক্ষ্য',
  mission_text='কোনো আপস ছাড়াই, শারীরিকভাবে যতটা সম্ভব দুঃখভোগ ঠেকানো।',
  effort='প্রচেষ্টা', questions='কোনো প্রশ্ন?', questions_text='প্রকল্প সম্পর্কে আরও জানতে info@proextinction.com-এ যোগাযোগ করুন',
  action='পদক্ষেপ নিন', toc='এই পাতায়', abridged='প্রিভিউ: এই ডিজাইনে চ্যানেলের লম্বা তালিকা বাদ রাখা হয়েছে। পুরো তালিকা বর্তমান সাইটে আছে:',
  abridged_link='পুরো পাতা খুলুন', ki='ইংরেজি থেকে যন্ত্রে অনুবাদ (AI)। মূল সাইটের কোনো বাংলা সংস্করণ নেই।',
  ki_tag='AI', back='ডিজাইন', back_title='ডিজাইনের তালিকায় ফিরে যান', progress='পড়ার অগ্রগতি', home_link='Pro Extinction – হোম',
  efforts=['আন্দোলনকে বড় করা, যাতে কোটি কোটি বছরের দুঃখভোগ ঠেকানো সম্ভব হয়।',
   'শারীরিকভাবে যত বেশি সম্ভব ভুক্তভোগীর জন্য সর্বজনীন, বৈষম্যহীন সাহায্য। প্রাণীদের জন্য, যত বেশি সম্ভব পৃথিবীর বাইরের প্রাণের জন্য, আর মানুষের জন্য।',
   'কেবল সংগঠিত কাজ আর অ্যাক্টিভিজমের ওপর ভিত্তি করে। ভুক্তভোগীদের মূল্যে কোনো বিলাপ নয়।',
   'পুরোপুরি যুক্তিনিষ্ঠ, সহমর্মী, নাস্তিক, যৌক্তিক আর ন্যায্য।'],
  foot='Pro Extinction · Global', page_title='Pro Extinction'),
 'ur': dict(menu='مینو', skip='مواد پر جائیں', lang='زبان', theme='لائٹ/ڈارک موڈ بدلیں',
  tagline='Together, we end suffering.', sub='وہ تنظیم جو زبردستی کے وجود اور تکلیف کو ختم کرنے کے لیے وقف ہے',
  cta1='ہمارے ساتھ شامل ہوں', cta2='منشور پڑھیں', mission='ہمارا مشن',
  mission_text='بغیر کسی سمجھوتے کے، جسمانی طور پر جتنی ممکن ہو اتنی تکلیف کو روکنا۔',
  effort='کوشش', questions='کوئی سوال؟', questions_text='منصوبے کے بارے میں مزید جاننے کے لیے info@proextinction.com پر رابطہ کریں',
  action='قدم اٹھائیں', toc='اس صفحے پر', abridged='پیش نظارہ: اس ڈیزائن میں چینلز کی لمبی فہرست شامل نہیں۔ پوری فہرست موجودہ سائٹ پر ہے:',
  abridged_link='پورا صفحہ کھولیں', ki='انگریزی سے مشینی ترجمہ (AI)۔ اصل سائٹ کا کوئی اردو ورژن نہیں ہے۔',
  ki_tag='AI', back='ڈیزائن', back_title='ڈیزائنز کی فہرست پر واپس جائیں', progress='پڑھنے کی پیش رفت', home_link='Pro Extinction – ہوم',
  efforts=['تحریک کو بڑھانا، تاکہ اربوں سال کی تکلیف کو روکنا ممکن ہو سکے۔',
   'جسمانی طور پر جتنے ممکن ہوں اتنے متاثرین کے لیے عالمگیر، بلا امتیاز مدد۔ جانوروں کے لیے، زمین سے باہر جتنی ممکن ہو اتنی زندگی کے لیے، اور انسانوں کے لیے۔',
   'صرف منظم عمل اور ایکٹیوزم پر مبنی۔ متاثرین کی قیمت پر کوئی ماتم نہیں۔',
   'مکمل طور پر عقلی، ہمدرد، ملحد، منطقی اور منصفانہ۔'],
  foot='Pro Extinction · Global', page_title='Pro Extinction'),
 'id': dict(menu='Menu', skip='Langsung ke isi', lang='Bahasa', theme='Ganti mode terang/gelap',
  tagline='Together, we end suffering.', sub='Organisasi yang berjuang untuk mengakhiri keberadaan yang dipaksakan dan penderitaan',
  cta1='Bergabung', cta2='Baca manifesto', mission='Misi kami',
  mission_text='Mencegah penderitaan sebanyak yang secara fisik mungkin, tanpa kompromi.',
  effort='Upaya', questions='Ada pertanyaan?', questions_text='Hubungi info@proextinction.com untuk informasi lebih lanjut tentang proyek ini',
  action='Bertindak', toc='Di halaman ini', abridged='Pratinjau: konsep ini tidak menampilkan daftar kanal yang panjang. Daftar lengkapnya ada di situs saat ini:',
  abridged_link='Buka halaman lengkap', ki='Terjemahan mesin dari bahasa Inggris (AI). Situs aslinya tidak memiliki versi bahasa Indonesia.',
  ki_tag='AI', back='Konsep', back_title='Kembali ke ringkasan konsep', progress='Kemajuan membaca', home_link='Pro Extinction – beranda',
  efforts=['Membesarkan gerakan agar pencegahan miliaran tahun penderitaan menjadi mungkin.',
   'Bantuan universal tanpa diskriminasi bagi sebanyak mungkin korban yang secara fisik bisa dijangkau. Bagi hewan, bagi sebanyak mungkin kehidupan di luar Bumi, dan bagi manusia.',
   'Murni berbasis aksi dan aktivisme yang terorganisasi. Tidak meratap dengan mengorbankan para korban.',
   'Sepenuhnya rasional, empatik, ateis, logis, dan adil.'],
  foot='Pro Extinction · Global', page_title='Pro Extinction'),
})
DISCORD = 'https://discord.gg/nb2K8y846R'
WHATSAPP = {'en': 'https://chat.whatsapp.com/J9WIHBa7Lqy8MyhlQYLogs', 'it': 'https://chat.whatsapp.com/J9WIHBa7Lqy8MyhlQYLogs',
            'de': 'https://chat.whatsapp.com/Dej17Wh0dvUG7oeauTH3GG', 'pl': 'https://chat.whatsapp.com/Dej17Wh0dvUG7oeauTH3GG',
            'es': 'https://chat.whatsapp.com/Dej17Wh0dvUG7oeauTH3GG'}  # as linked on each original site
WHATSAPP.update({l: WHATSAPP['en'] for l in FULL_AI})
EMAIL = 'info@proextinction.com'

CONCEPTS = {
 'a-ember':  dict(name='Ember',  mode='dark',  fonts='family=Source+Serif+4:ital,wght@0,400;0,600;1,400&family=Oswald:wght@500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&family=JetBrains+Mono:wght@400;500'),
 'b-poster': dict(name='Poster', mode='dark',  fonts='family=Oswald:wght@400;600&family=Anton&family=Barlow:wght@400;500;600&family=JetBrains+Mono:wght@400;500'),
}

def linkify(s):
    s = esc(s)
    s = re.sub(r'(https?://[^\s<]+)', lambda m: f'<a href="{m.group(1)}" rel="noopener">{m.group(1)}</a>', s)
    return re.sub(r'\b([\w.+-]+@[\w-]+\.[\w.-]+)\b', r'<a href="mailto:\1">\1</a>', s)

ID_PREFIX = ''   # set by present.py so ids stay unique when all views live in one document

def slug_id(s, used):
    base = re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:40] or 'section'
    i, k = base, 2
    while i in used: i = f'{base}-{k}'; k += 1
    used.add(i); return ID_PREFIX + i

def render_blocks(blocks, used):
    out, toc = [], []
    for b in blocks:
        if b[0] == 'h':
            i = slug_id(b[1], used); toc.append((i, b[1].rstrip(':：')))
            out.append(f'<h2 id="{i}">{esc(b[1].rstrip(":："))}</h2>')
        elif b[0] == 'ul':
            out.append('<ul>' + ''.join(f'<li>{linkify(i)}</li>' for i in b[1]) + '</ul>')
        else:
            out.append(f'<p>{linkify(b[1])}</p>')
    return '\n'.join(out), toc

def head_lede(lines, like=None):
    """Title, optional lede, rest. like: English lines that a translation mirrors (decides the structure)."""
    like = like or lines
    title, rest = lines[0], lines[1:]
    lede = None
    from blocks import is_heading
    r = like[1:]
    if len(r) > 1 and len(r[0]) <= 90 and not r[0].endswith('?') \
            and (r[0].endswith('.') or is_heading(r[0])) and is_heading(r[1]) and not r[1].endswith('?'):
        lede, rest = rest[0].rstrip(':：'), rest[1:]
    return title, lede, rest

def doc_body(lang, slug, lines, full_url, like=None):
    t = T[lang]; used = set()
    title, lede, rest = head_lede(lines, like)
    rest_like = like[len(lines) - len(rest):] if like else None
    kind = 'doc'; truncated = False
    if slug in ('social-media-channels',):
        bl = blocks_of(rest, rest_like)[:2]; truncated = True
    else:
        bl = blocks_of(rest, rest_like)
    body, toc = render_blocks(bl, used)
    return title, lede, body, toc, truncated

def faq_body(lang, slug, lines, like=None):
    t = T[lang]
    title, lede, rest = head_lede(lines, like)
    intro, pairs = faq_pairs(rest, like[len(lines) - len(rest):] if like else None)
    shown = pairs
    intro_html = ''.join(f'<p>{linkify(l)}</p>' for l in intro)
    items = []
    for q, a in shown:
        items.append(f'<details><summary>{esc(q)}</summary><div class="a">' + ''.join(f'<p>{linkify(p)}</p>' for p in a) + '</div></details>')
    return title, lede, intro_html + '<div class="faq">' + '\n'.join(items) + '</div>', [], len(shown) < len(pairs)

def sitenav(lang, slug):
    t = T[lang]; cur = ' aria-current="page"'
    items = ''.join('<li><a href="%s.html"%s>%s</a></li>' % (s_, cur if s_ == slug else '', esc(NAV[lang][s_])) for s_, _ in PAGES[lang])
    return f'<nav class="sitenav" id="sitenav" aria-label="Main"><ul>{items}</ul></nav>'

def lang_select(lang, url):
    """Language picker. url(other_lang) gives each option's target; site.js / present.js navigate on change."""
    t = T[lang]
    opts = ''.join(f'<option value="{url(l)}" lang="{l}"{" selected" if l == lang else ""}>{CODE[l]} · {LANG_NAME[l]}</option>' for l in LANGS)
    return f'<label class="lang-wrap"><span class="lang" aria-hidden="true">{CODE[lang]}</span><select class="lang-select" aria-label="{t["lang"]}">{opts}</select></label>'

def header(c, lang, slug, ctx):
    t = T[lang]
    picker = lang_select(lang, lambda l: f'../{l}/{counterpart(lang, slug, l)}.html')
    return f'''<a class="skip" href="#main">{t["skip"]}</a>
<div class="progress" aria-hidden="true"><i></i></div>
<header class="top">
  <div class="lead">
    <a class="brand" href="home.html" aria-label="{t["home_link"]}"><span class="logo" role="img" aria-label="Pro Extinction logo"></span><span class="wordmark">PRO EXTINCTION</span></a>
    <a class="back" href="../../index.html" title="{t["back_title"]}"><span aria-hidden="true">←</span><span class="back-t">{t["back"]}</span></a>
  </div>
  <div class="tools">
    {picker}
    <button class="theme" type="button" aria-label="{t["theme"]}" title="{t["theme"]}"><span></span></button>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="sitenav"><span class="bars" aria-hidden="true"></span><span class="menu-t">{t["menu"]}</span></button>
  </div>
</header>'''

def footer(lang):
    t = T[lang]
    return f'''<section class="cta" aria-label="{t["action"]}">
  <hr class="slash">
  <h2>{t["action"]}</h2>
  <p class="cta-sub">{t["tagline"]}</p>
  <p class="cta-links"><a class="btn primary" href="{DISCORD}" rel="noopener">Discord</a><a class="btn" href="{WHATSAPP[lang]}" rel="noopener">WhatsApp</a><a class="btn" href="mailto:{EMAIL}">{EMAIL}</a></p>
</section>
<footer class="foot"><p class="mono">{t["foot"]}</p></footer>'''

def page_main(lang, slug, kind, href=lambda s: s + '.html'):
    """Title and <main> content of one page (shared by the multi-page prototype and the single-file presentation)."""
    t = T[lang]
    ki = slug in AI[lang]
    if kind == 'home':
        return NAV[lang]['home'], home_main(lang, href), 'home'
    lines = json.loads((ROOT / 'content' / lang / f'{slug}.json').read_text(encoding='utf-8'))
    like = json.loads((ROOT / 'content' / 'en' / f'{EN_OF[lang][slug]}.json').read_text(encoding='utf-8')) if ki else None
    if kind == 'faq': title, lede, body, toc, truncated = faq_body(lang, slug, lines, like)
    else:
        title, lede, body, toc, truncated = doc_body(lang, EN_OF[lang][slug], lines, '', like)
    if ki: orig = ORIGINAL['en'].format(EN_OF[lang][slug])
    else: orig = ORIGINAL[lang].format(urllib.parse.quote(ORIG[lang][slug]))
    notes = ''
    if ki: notes += f'<p class="note ki"><span class="tag">{t["ki_tag"]}</span> {t["ki"]}</p>'
    if truncated: notes += f'<p class="note">{t["abridged"]} <a href="{orig}" rel="noopener">{t["abridged_link"]}</a></p>'
    toc_html = ''
    if len(toc) > 1:
        toc_html = f'<nav class="toc" aria-label="{t["toc"]}"><p class="mono">{t["toc"]}</p><ol>' + ''.join(f'<li><a href="#{i}">{esc(n)}</a></li>' for i, n in toc) + '</ol></nav>'
    lede_html = f'<p class="lede">{esc(lede)}</p>' if lede else ''
    main = f'<article class="doc"><header class="doc-head"><p class="mono kicker">{esc(NAV[lang][slug])}</p><h1>{esc(title)}</h1>{lede_html}<hr class="slash"></header>{toc_html}<div class="prose">{notes}{body}</div></article>'
    return title, main, 'page'

def page_html(c, lang, slug, kind):
    t = T[lang]; cdef = CONCEPTS[c]
    title, main, body_class = page_main(lang, slug, kind)
    return f'''<!doctype html>
<html lang="{lang}" dir="{DIR(lang)}" data-concept="{c}" data-default="{cdef["mode"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} – Pro Extinction · {cdef["name"]}</title>
<meta name="robots" content="noindex">
<script>(function(){{var d=document.documentElement,m=null;try{{m=new URLSearchParams(location.search).get('theme')||localStorage.getItem('pe-theme')}}catch(e){{}}
if(m!=='light'&&m!=='dark'){{m=window.matchMedia&&matchMedia('(prefers-color-scheme: light)').matches?'light':(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches?'dark':d.dataset.default)}}d.dataset.theme=m}})()</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{cdef["fonts"]}&display=swap">
<link rel="stylesheet" href="../style.css">
</head>
<body class="{body_class}">
{header(c, lang, slug, None)}
<div class="shell">
{sitenav(lang, slug)}
<main id="main">
{main}
</main>
</div>
{footer(lang)}
<script src="../../assets/site.js" defer></script>
</body>
</html>
'''

def home_main(lang, href=lambda s: s + '.html'):
    t = T[lang]
    ki = f'<p class="note ki"><span class="tag">{t["ki_tag"]}</span> {t["ki"]}</p>' if lang in FULL_AI else ''
    efforts = ''.join(f'<li><span class="num mono">{i+1:02d}</span><p class="eff-label mono">{t["effort"]} {i+1}</p><p>{esc(x)}</p></li>' for i, x in enumerate(t['efforts']))
    return f'''<section class="hero">
  {HERO_LOGO}
  <h1 class="wordmark">PRO EXTINCTION</h1>
  <p class="hero-tag">{t["tagline"]}</p>
  <p class="hero-sub">{esc(t["sub"])}</p>
  <p class="hero-cta"><a class="btn primary" href="{href(OF_EN[lang]['join-us'])}">{t["cta1"]}</a><a class="btn" href="{href(OF_EN[lang]['manifesto'])}">{t["cta2"]}</a></p>
</section>
<section class="mission"><hr class="slash"><p class="mono kicker">{t["mission"]}</p><blockquote>{esc(t["mission_text"])}</blockquote></section>
<section class="efforts"><ol>{efforts}</ol></section>
<section class="questions"><h2>{t["questions"]}</h2><p>{linkify(t["questions_text"])}</p>{ki}</section>'''

def _svg_uri(name):
    svg = (OUT / 'assets' / f'{name}.svg').read_text(encoding='utf-8').replace('currentColor', '#000')
    return 'data:image/svg+xml,' + urllib.parse.quote(svg, safe="/:=' ")

def logo_css():
    """Static logo (header) plus the three layers of the animated hero logo: snake, cut gap, slash."""
    return (f'.logo{{--logo:url("{_svg_uri("logo")}");-webkit-mask:var(--logo) center/contain no-repeat;mask:var(--logo) center/contain no-repeat;background:currentColor;display:inline-block}}\n'
            f':root{{--logo-snake:url("{_svg_uri("logo-snake")}");--logo-cut:url("{_svg_uri("logo-cut")}");--logo-slash:url("{_svg_uri("logo-slash")}")}}\n')

HERO_LOGO = ('<span class="hero-logo" role="img" aria-label="Pro Extinction logo">'
             '<span class="lg lg-snake"></span><span class="lg lg-cut"></span><span class="lg lg-slash"></span></span>')

def build():
    css_base = (ROOT / 'tools/css/base.css').read_text(encoding='utf-8')
    for c in CONCEPTS:
        css = css_base + '\n' + (ROOT / 'brand' / c / 'tokens.css').read_text(encoding='utf-8') + '\n' + (ROOT / f'tools/css/{c[0]}.css').read_text(encoding='utf-8') + '\n' + logo_css()
        (OUT / c).mkdir(parents=True, exist_ok=True)
        (OUT / c / 'style.css').write_text(css, encoding='utf-8')
        for lang in LANGS:
            d = OUT / c / lang; d.mkdir(exist_ok=True)
            for slug, kind in PAGES[lang]:
                (d / f'{slug}.html').write_text(page_html(c, lang, slug, kind), encoding='utf-8')
    n = sum(len(PAGES[l]) for l in PAGES) * len(CONCEPTS)
    print('built', n, 'pages')

if __name__ == '__main__': build()

INDEX = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pro Extinction – design concepts</title><meta name="robots" content="noindex">
<style>:root{color-scheme:dark light;--bg:#0d0809;--text:#dcd8d8;--muted:#9a9292;--line:#2c2224;--accent:#e8484d}
@media (prefers-color-scheme:light){:root{--bg:#f4f0ea;--text:#151011;--muted:#5e5656;--line:#cfc6ba;--accent:#a30f14}}
body{margin:0;background:var(--bg);color:var(--text);font:1.05rem/1.6 Georgia,serif;padding:clamp(1.2rem,5vw,3rem);max-width:56rem;margin-inline:auto}
h1{font:600 clamp(2rem,6vw,3.4rem)/1 "Arial Narrow",Impact,sans-serif;text-transform:uppercase;margin:0 0 .5rem}
p{color:var(--muted)}li{border-top:1px solid var(--line);padding:1.2rem 0;list-style:none}ul{padding:0;margin:2rem 0}
h2{font:600 1.5rem "Arial Narrow",Impact,sans-serif;text-transform:uppercase;margin:0 0 .3rem}a{color:var(--accent);margin-right:1.2rem}</style></head>
<body><h1>Pro Extinction – design concepts</h1>
<p>Two directions for the redesign. All have a light/dark switch (button top right) and 14 languages. Pages and languages marked (AI) are machine-translated from English.</p>
<ul>
<li><h2>A · Ember</h2><p>Angular, editorial, asymmetric. Red/black/silver, serif body text.</p>%s</li>
<li><h2>B · Poster</h2><p>Angular, centred, loud. Red/black/silver, sans-serif body text.</p>%s</li>
</ul></body></html>
'''
LINKS = lambda c: ''.join(f'<a href="{c}/{l}/home.html" lang="{l}">{LANG_NAME[l]}{AI_MARK if l in FULL_AI else ""}</a>' for l in LANGS)
(OUT / 'index.html').write_text(INDEX % tuple(LINKS(c) for c in CONCEPTS), encoding='utf-8')
