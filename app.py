from flask import Flask, request, session, redirect, url_for, render_template_string, flash, get_flashed_messages
import os

app = Flask(__name__)
app.secret_key = 'homies-cafe-2026-secret'

# ══════════════════════════════════════════════════════════════
#  CATÁLOGO DE PRODUCTOS
# ══════════════════════════════════════════════════════════════

cafes_calientes = [
    ("Espresso",           7,  "Solo y concentrado, la esencia del buen café."),
    ("Americano",          8,  "Espresso diluido en agua caliente, suave y equilibrado."),
    ("Cortado",            7,  "Espresso con un toque de leche caliente vaporizada."),
    ("Machiatto",          7,  "Espresso marcado con espuma de leche suave."),
    ("Latte",             10,  "Espresso con abundante leche vaporizada."),
    ("Capuccino",          9,  "Partes iguales de espresso, leche y espuma cremosa."),
    ("Chocolate Caliente", 9,  "Chocolate cremoso, intenso y reconfortante."),
    ("Café Mocha",        10,  "Espresso con chocolate y leche vaporizada."),
    ("Vainilla Latte",    12,  "Latte con sirope de vainilla artesanal."),
    ("Matcha Latte",      14,  "Matcha premium con leche vaporizada. Suave y terroso."),
]

cafes_frios = [
    ("Iced Americano",      10, "Americano sobre hielo, refrescante y limpio."),
    ("Affogato",             9, "Espresso sobre helado de vainilla. Caliente y frío a la vez."),
    ("Iced Latte",          12, "Latte frío sobre hielo. Cremoso y clásico."),
    ("Iced Capuccino",      10, "Capuccino frío con hielo y espuma fría."),
    ("Iced Cinnamon",       11, "Latte frío con canela y sirope artesanal."),
    ("Iced Mocha",          11, "Mocha helado, chocolate y café a partes iguales."),
    ("Iced Caramel",        11, "Latte frío con sirope de caramelo artesanal."),
    ("Iced Vainilla Latte", 14, "Vainilla latte sobre hielo, dulce y cremoso."),
    ("Iced Matcha Latte",   16, "Matcha premium frío, leche entera o sin lactosa."),
    ("Iced Coconut Matcha", 13, "Matcha con leche de coco, fresco y tropical."),
]

frappes = [
    ("Frappé Chocolate",   14, "Cremoso, helado e intensamente chocolatoso."),
    ("Frappé Mocha",       14, "Café y chocolate batidos a la perfección."),
    ("Frappé Oreo",        14, "Frappé de vainilla con trozos de Oreo."),
    ("Frappé Caramelo",    14, "Dulce frappé con sirope de caramelo artesanal."),
    ("Frappé Menta",       14, "Fresco, helado y con toque de menta natural."),
    ("BerryMatcha Homies", 15, "Matcha latte con compota de fresas + foto instantánea de regalo ⭐"),
]

postres_artesanales = [
    ("Pionono de Chocolúcuma",   8,  "Bizcocho de chocolate relleno de mousse de lúcuma."),
    ("Crema Volteada",           9,  "Clásico postre peruano, suave y acaramelado."),
    ("Tres Leches de Vainilla",  9,  "Bizcocho esponjoso bañado en tres leches con vainilla."),
    ("Tres Leches de Chocolate", 9,  "Versión chocolatosa de nuestro tres leches estrella."),
    ("Tarta de Manzana",         9,  "Base crocante con manzanas caramelizadas y canela."),
    ("Tarta de Limón",          10,  "Rellena de crema de limón al estilo neoyorquino."),
    ("Torta Moka",              11,  "Torta de café con crema de mantequilla mocha."),
    ("Carrot Cake",             11,  "Queque de zanahoria con frosting de queso crema."),
    ("Torta de Chocolate",      12,  "Intensamente chocolatosa, preparada diariamente."),
    ("Tartaleta de Fresa",      12,  "Base crujiente con crema pastelera y fresas frescas."),
]

postres = [
    ("Cheesecake Maracuyá",  10, "Cremoso cheesecake con coulis de maracuyá fresco."),
    ("Cheesecake Oreo",      10, "Base de Oreo con relleno de queso crema."),
    ("Cheesecake Clásico",   10, "El original. Simple y perfecto."),
    ("NY Cheesecake",        15, "Horneado y decorado con coulis de fresa."),
    ("Torta de Chocolate",   12, "Densa y fudgy, con frosting de ganache."),
    ("Tiramisú",             12, "Clásico italiano con café, mascarpone y cacao."),
    ("Tres Leches Chocolate", 9, "Bizcocho bañado en tres leches con chocolate."),
    ("Tres Leches Vainilla",  9, "Suave y esponjoso, bañado en tres leches."),
    ("Carrot Cake",          11, "Queque de zanahoria con frosting de queso crema."),
]

sandwiches = [
    ("Mixto Simple",                   12, "Pan, queso y jamón. Simple y siempre delicioso."),
    ("Mixto Especial",                 16, "Mixto con ingredientes premium."),
    ("Charsiu",                        18, "Pan ciabatta con chancho glaseado en salsa charsiu y ensalada de cebolla."),
    ("Club Sandwich",                  20, "Triple con pollo, tocino, lechuga, tomate y mayonesa."),
    ("Pollo Deshilachado",             16, "Pan artesanal con pollo deshilachado jugoso y fresco."),
    ("Capresse",                       16, "Pan con tomate, mozzarella fresca y albahaca."),
    ("Pollo Deshilachado con Palta",   18, "Pollo deshilachado con palta fresca en pan artesanal."),
    ("Pollo Deshilachado con Durazno", 20, "Pollo deshilachado con durazno glaseado."),
]

jugos = [
    ("Jugo de Papaya",  9,  "Recién exprimida, natural y refrescante."),
    ("Jugo de Piña",    9,  "Fresca y tropical, exprimida al momento."),
    ("Jugo de Fresa",   9,  "Dulce y aromática, preparada al instante."),
    ("Jugo de Naranja", 9,  "Clásico cítrico, lleno de vitamina C."),
    ("Jugo de Mango",   9,  "Tropical y dulce, del mango más fresco."),
    ("Papaya con Leche", 12, "Cremosa combinación de papaya con leche entera."),
    ("Fresa con Leche",  12, "Fresa fresca batida con leche fría."),
    ("Mango con Leche",  12, "Mango tropical cremoso con leche entera fría."),
]

# Diccionario de precios único
productos = {}
for lista in (cafes_calientes, cafes_frios, frappes, postres_artesanales, postres, sandwiches, jugos):
    for nombre, precio, _ in lista:
        if nombre not in productos:
            productos[nombre] = precio

# ══════════════════════════════════════════════════════════════
#  HELPERS DE SESIÓN (carrito por usuario)
# ══════════════════════════════════════════════════════════════

def get_carrito():
    return list(session.get('carrito', []))

def save_carrito(c):
    session['carrito'] = c
    session.modified = True

def count_carrito():
    return sum(i['cantidad'] for i in get_carrito())

def total_carrito():
    return sum(i['precio'] * i['cantidad'] for i in get_carrito())

# ══════════════════════════════════════════════════════════════
#  URLS DE IMÁGENES (Unsplash)
# ══════════════════════════════════════════════════════════════

IMG = {
    'hero_inicio':    'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=1920&auto=format&fit=crop&q=80',
    'hero_menu':      'https://images.unsplash.com/photo-1442512595331-e89e73853f31?w=1920&auto=format&fit=crop&q=80',
    'hero_nosotros':  'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=1920&auto=format&fit=crop&q=80',
    'hero_contacto':  'https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=1920&auto=format&fit=crop&q=80',
    'cat_caliente':   'https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=1200&auto=format&fit=crop&q=80',
    'cat_frio':       'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=1200&auto=format&fit=crop&q=80',
    'cat_frappe':     'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=1200&auto=format&fit=crop&q=80',
    'cat_postre':     'https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=1200&auto=format&fit=crop&q=80',
    'cat_sandwich':   'https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=1200&auto=format&fit=crop&q=80',
    'cat_jugo':       'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1200&auto=format&fit=crop&q=80',
    'feat_matcha':    'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=600&auto=format&fit=crop&q=80',
    'feat_cake':      'https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=600&auto=format&fit=crop&q=80',
    'feat_sandwich':  'https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=600&auto=format&fit=crop&q=80',
}

# ══════════════════════════════════════════════════════════════
#  CSS COMPARTIDO
# ══════════════════════════════════════════════════════════════

CSS = """
:root {
  --vd: #1B3328;
  --vm: #28503E;
  --vs: #8E9B6D;
  --mr: #6B4226;
  --mc: #B98D63;
  --cr: #FAF6EC;
  --bl: #FFFFFF;
  --tx: #2B2A23;
  --ts: #6B6A5E;
  --sh: 0 6px 24px rgba(27,51,40,0.10);
}

* { margin:0; padding:0; box-sizing:border-box; }

html { scroll-behavior: smooth; }

body {
  background: var(--cr);
  color: var(--tx);
  font-family: 'Work Sans', Arial, sans-serif;
  line-height: 1.6;
}

h1,h2,h3,h4 { font-family: 'Fraunces', Georgia, serif; }

/* ─ NAV ─────────────────────────────── */
.topnav {
  background: var(--vd);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  height: 64px;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 14px rgba(0,0,0,0.22);
}

.nav-logo {
  color: var(--mc);
  font-family: 'Fraunces', serif;
  font-size: 22px;
  font-weight: 700;
  text-decoration: none;
  white-space: nowrap;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 4px;
  overflow-x: auto;
  scrollbar-width: none;
}

.nav-links::-webkit-scrollbar { display: none; }

.nav-links a {
  color: #EDE7DA;
  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
  padding: 7px 16px;
  border-radius: 999px;
  transition: background .2s, color .2s;
  white-space: nowrap;
}

.nav-links a:hover, .nav-links a.active {
  background: var(--mc);
  color: var(--vd);
}

.nav-links .nav-cart {
  background: var(--mr);
  color: white;
  margin-left: 8px;
}

.nav-links .nav-cart:hover { background: #532F19; color: white; }

/* ─ FLASH ────────────────────────────── */
.flash {
  background: #E7EFD9;
  color: var(--vd);
  border-left: 4px solid var(--vs);
  padding: 14px 24px;
  text-align: center;
  font-weight: 600;
  font-size: 15px;
}

/* ─ HERO PRINCIPAL ───────────────────── */
.hero {
  position: relative;
  min-height: 540px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  background-size: cover;
  background-position: center;
  background-color: var(--vd);
}

.hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(155deg, rgba(27,51,40,.75) 0%, rgba(107,66,38,.50) 100%);
}

.hero-content {
  position: relative;
  z-index: 1;
  color: white;
  max-width: 680px;
  padding: 48px 24px;
}

.hero-content .eyebrow {
  display: inline-block;
  font-size: 11px;
  letter-spacing: 4px;
  text-transform: uppercase;
  color: var(--mc);
  font-weight: 700;
  margin-bottom: 14px;
}

.hero-content h1 {
  font-size: 54px;
  line-height: 1.08;
  margin-bottom: 16px;
}

.hero-content p {
  font-size: 18px;
  color: rgba(255,255,255,.85);
  margin-bottom: 30px;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

.btn-hero {
  display: inline-block;
  background: var(--mc);
  color: var(--vd);
  font-weight: 700;
  font-size: 15px;
  padding: 14px 32px;
  border-radius: 999px;
  text-decoration: none;
  transition: background .2s, transform .2s;
  margin: 0 6px;
}

.btn-hero:hover { background: #C9A375; transform: translateY(-2px); }

.btn-hero-outline {
  display: inline-block;
  background: transparent;
  border: 2px solid rgba(255,255,255,.6);
  color: white;
  font-weight: 700;
  font-size: 15px;
  padding: 12px 30px;
  border-radius: 999px;
  text-decoration: none;
  transition: background .2s, border-color .2s;
  margin: 0 6px;
}

.btn-hero-outline:hover { background: rgba(255,255,255,.15); border-color: white; }

/* ─ MINI HERO (páginas interiores) ───── */
.page-hero {
  position: relative;
  min-height: 260px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  background-size: cover;
  background-position: center;
  background-color: var(--vm);
}

.page-hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(27,51,40,.65);
}

.page-hero-content {
  position: relative;
  z-index: 1;
  color: white;
  padding: 48px 24px;
}

.page-hero-content h1 { font-size: 40px; }

.page-hero-content p {
  font-size: 16px;
  color: rgba(255,255,255,.80);
  margin-top: 8px;
}

/* ─ SECTION GENÉRICO ─────────────────── */
.section {
  max-width: 1180px;
  margin: 0 auto;
  padding: 54px 20px 16px;
}

.section-header { text-align: center; margin-bottom: 32px; }

.eyebrow {
  display: inline-block;
  font-size: 11px;
  letter-spacing: 4px;
  text-transform: uppercase;
  color: var(--mr);
  font-weight: 700;
  margin-bottom: 8px;
}

.sec-title {
  font-size: 30px;
  color: var(--vd);
  font-weight: 600;
}

.sec-line {
  width: 56px;
  height: 3px;
  background: var(--mc);
  border-radius: 3px;
  margin: 12px auto 0;
}

/* ─ CATEGORY BANNER ─────────────────── */
.cat-banner {
  position: relative;
  min-height: 130px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  background-size: cover;
  background-position: center;
  background-color: var(--vm);
  border-radius: 16px;
  overflow: hidden;
  margin-top: 40px;
  scroll-margin-top: 120px;
}

.cat-banner::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(27,51,40,.70);
}

.cat-banner-inner {
  position: relative;
  z-index: 1;
  color: white;
  padding: 24px;
}

.cat-banner-inner h2 { font-size: 27px; font-weight: 700; }

.cat-banner-inner p {
  font-size: 13.5px;
  color: rgba(255,255,255,.78);
  margin-top: 4px;
}

/* ─ GRID DE CARDS ───────────────────── */
.grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  padding: 20px 0 10px;
}

.card {
  background: var(--bl);
  width: 255px;
  border-radius: 14px;
  box-shadow: var(--sh);
  border-top: 4px solid var(--mc);
  display: flex;
  flex-direction: column;
  transition: transform .18s, box-shadow .18s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 14px 32px rgba(27,51,40,.16);
}

.card-body {
  padding: 18px 18px 16px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.card h3 { color: var(--vd); font-size: 17px; margin-bottom: 6px; }

.card p { font-size: 13px; color: var(--ts); margin-bottom: 12px; flex-grow: 1; }

.price-badge {
  display: inline-block;
  background: var(--vs);
  color: white;
  font-weight: 700;
  font-size: 13.5px;
  padding: 4px 13px;
  border-radius: 999px;
  margin-bottom: 12px;
  align-self: flex-start;
}

/* ─ BOTONES ─────────────────────────── */
.btn {
  display: inline-block;
  background: var(--mr);
  color: white;
  border: none;
  padding: 10px 16px;
  width: 100%;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
  font-family: 'Work Sans', sans-serif;
  text-align: center;
  text-decoration: none;
  transition: background .2s;
}

.btn:hover { background: #532F19; }
.btn-vd { background: var(--vd); }
.btn-vd:hover { background: #0F2018; }
.btn-mc { background: var(--mc); color: var(--vd); }
.btn-mc:hover { background: #C9A375; color: var(--vd); }
.btn-red { background: #A8442F; }
.btn-red:hover { background: #82331F; }
.btn-sm { width: auto; padding: 6px 14px; font-size: 13px; }
.btn-lg { padding: 14px 36px; font-size: 15px; width: auto; }

.btn-cantidad {
  background: var(--vd);
  color: white;
  width: 30px;
  height: 30px;
  padding: 0;
  font-size: 16px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  transition: background .2s;
  font-family: 'Work Sans', sans-serif;
}

.btn-cantidad:hover { background: #0F2018; }

/* ─ INICIO FEATURED ─────────────────── */
.feat-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  justify-content: center;
  padding: 0 20px;
}

.feat-card {
  background: var(--bl);
  width: 300px;
  border-radius: 16px;
  box-shadow: var(--sh);
  overflow: hidden;
  transition: transform .2s;
}

.feat-card:hover { transform: translateY(-6px); }

.feat-img {
  width: 100%;
  height: 190px;
  object-fit: cover;
}

.feat-body { padding: 20px; }
.feat-body h3 { color: var(--vd); font-size: 20px; margin-bottom: 6px; }
.feat-body p { color: var(--ts); font-size: 14px; margin-bottom: 14px; }
.feat-price { font-size: 24px; font-weight: 700; color: var(--mr); font-family: 'Fraunces', serif; }

/* ─ INICIO WHY US ───────────────────── */
.why-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
  padding: 0 20px;
}

.why-card {
  background: var(--bl);
  width: 270px;
  padding: 28px 22px;
  border-radius: 14px;
  text-align: center;
  box-shadow: var(--sh);
  border-bottom: 3px solid var(--mc);
}

.why-icon { font-size: 38px; margin-bottom: 12px; }
.why-card h3 { color: var(--vd); font-size: 18px; margin-bottom: 8px; }
.why-card p { color: var(--ts); font-size: 14px; }

/* ─ CTA BAND ────────────────────────── */
.cta-band {
  background: var(--vd);
  color: white;
  text-align: center;
  padding: 56px 24px;
  margin-top: 48px;
}

.cta-band h2 { font-size: 34px; margin-bottom: 10px; }

.cta-band p {
  font-size: 16px;
  color: rgba(255,255,255,.72);
  margin-bottom: 26px;
  max-width: 460px;
  margin-left: auto;
  margin-right: auto;
}

/* ─ MENÚ SUB-NAV ────────────────────── */
.sub-nav {
  background: var(--cr);
  border-bottom: 2px solid #E6DFD2;
  padding: 0 20px;
  display: flex;
  gap: 2px;
  overflow-x: auto;
  position: sticky;
  top: 64px;
  z-index: 90;
  scrollbar-width: none;
}

.sub-nav::-webkit-scrollbar { display: none; }

.sub-nav a {
  color: var(--ts);
  text-decoration: none;
  font-size: 13px;
  font-weight: 600;
  padding: 13px 15px;
  white-space: nowrap;
  border-bottom: 3px solid transparent;
  transition: color .2s, border-color .2s;
}

.sub-nav a:hover {
  color: var(--mr);
  border-bottom-color: var(--mr);
}

/* ─ CARRITO BOX ─────────────────────── */
.carrito-box {
  background: var(--bl);
  padding: 28px 24px;
  border-radius: 16px;
  box-shadow: var(--sh);
  border-top: 4px solid var(--vs);
}

.carrito-box h2 { color: var(--vd); margin-bottom: 18px; font-size: 24px; }

.tabla {
  width: 100%;
  border-collapse: collapse;
}

.tabla th, .tabla td {
  text-align: left;
  padding: 10px 10px;
  border-bottom: 1px solid #EDE8DF;
  font-size: 14px;
}

.tabla th {
  background: #F5F0E6;
  color: var(--vd);
  font-size: 11.5px;
  text-transform: uppercase;
  letter-spacing: .5px;
}

.cant-ctrl { display: flex; align-items: center; gap: 8px; }
.cant-num { font-weight: 700; min-width: 22px; text-align: center; }
.sub-bold { font-weight: 700; color: var(--vd); }

.total-line {
  text-align: right;
  font-size: 21px;
  font-weight: 700;
  color: var(--vd);
  margin-top: 16px;
}

.confirm-row {
  text-align: right;
  margin-top: 14px;
}

.vacio { text-align: center; color: var(--ts); padding: 30px; font-size: 15px; }

/* ─ DASHBOARD ───────────────────────── */
.dashboard {
  background: var(--vd);
  padding: 30px 24px;
  border-radius: 16px;
  margin-bottom: 10px;
}

.dashboard h2 { color: white; margin-bottom: 18px; font-size: 22px; }

.metricas { display: flex; flex-wrap: wrap; gap: 14px; }

.metrica {
  background: rgba(255,255,255,.08);
  border: 1px solid rgba(255,255,255,.12);
  flex: 1;
  min-width: 150px;
  padding: 20px;
  border-radius: 12px;
  text-align: center;
}

.metrica .val {
  font-size: 26px;
  font-weight: 700;
  color: var(--mc);
  font-family: 'Fraunces', serif;
}

.metrica .lbl { font-size: 12px; color: #D2CCBE; margin-top: 6px; }

/* ─ NOSOTROS ────────────────────────── */
.story {
  max-width: 780px;
  margin: 0 auto;
  padding: 54px 24px 40px;
  text-align: center;
}

.story h2 { font-size: 32px; color: var(--vd); margin: 10px 0 22px; }
.story p { font-size: 17px; color: var(--ts); line-height: 1.85; margin-bottom: 18px; }

.val-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
  padding: 0 20px 56px;
}

.val-card {
  background: var(--bl);
  width: 230px;
  padding: 28px 20px;
  border-radius: 14px;
  text-align: center;
  box-shadow: var(--sh);
  border-bottom: 3px solid var(--mc);
}

.val-icon { font-size: 34px; margin-bottom: 10px; }
.val-card h3 { color: var(--vd); font-size: 17px; margin-bottom: 6px; }
.val-card p { color: var(--ts); font-size: 13px; }

/* ─ CONTACTO ────────────────────────── */
.contact-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 22px;
  justify-content: center;
  padding: 20px 20px 54px;
  max-width: 980px;
  margin: 0 auto;
}

.contact-card {
  background: var(--bl);
  width: 240px;
  padding: 28px 22px;
  border-radius: 14px;
  text-align: center;
  box-shadow: var(--sh);
}

.contact-icon { font-size: 36px; margin-bottom: 10px; }
.contact-card h3 { color: var(--vd); font-size: 17px; margin-bottom: 10px; }
.contact-card p { color: var(--ts); font-size: 14px; line-height: 1.75; }
.contact-card a { color: var(--mr); text-decoration: none; font-weight: 600; }
.contact-card a:hover { text-decoration: underline; }

.btn-wa {
  display: block;
  width: fit-content;
  background: #25D366;
  color: white;
  padding: 15px 36px;
  border-radius: 999px;
  text-decoration: none;
  font-weight: 700;
  font-size: 16px;
  margin: 0 auto 56px;
  transition: background .2s, transform .2s;
}

.btn-wa:hover { background: #1DA851; transform: translateY(-2px); }

/* ─ FOOTER ──────────────────────────── */
footer {
  background: var(--vd);
  color: #C8C2B5;
  padding: 42px 32px 24px;
}

.footer-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 32px;
  max-width: 1000px;
  margin: 0 auto 30px;
}

.footer-col h4 {
  color: var(--mc);
  font-size: 12px;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  margin-bottom: 12px;
}

.footer-col p, .footer-col a {
  font-size: 13.5px;
  color: #A09A8E;
  line-height: 1.85;
  text-decoration: none;
  display: block;
}

.footer-col a:hover { color: var(--mc); }
.footer-logo { font-family: 'Fraunces', serif; font-size: 26px; color: white; margin-bottom: 6px; }
.footer-sub { font-size: 13px; color: #7A7470; margin-bottom: 10px; }

.footer-bottom {
  border-top: 1px solid rgba(255,255,255,.08);
  padding-top: 18px;
  text-align: center;
  font-size: 12.5px;
  color: #5E5A52;
  max-width: 1000px;
  margin: 0 auto;
}

/* ─ FLOAT CART ──────────────────────── */
.float-cart {
  position: fixed;
  bottom: 26px;
  right: 26px;
  background: var(--mr);
  color: white;
  border-radius: 999px;
  padding: 13px 20px;
  font-size: 14px;
  font-weight: 700;
  text-decoration: none;
  font-family: 'Work Sans', sans-serif;
  box-shadow: 0 6px 20px rgba(107,66,38,.42);
  z-index: 200;
  transition: background .2s, transform .2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.float-cart:hover { background: #532F19; transform: scale(1.06); }

.cart-badge {
  background: white;
  color: var(--mr);
  border-radius: 999px;
  padding: 2px 8px;
  font-size: 12.5px;
}

/* ─ UTIL CLASES ─────────────────────── */
.center { text-align: center; }
.mt-sm  { margin-top: 20px; }
.mt-md  { margin-top: 36px; }
.mt-lg  { margin-top: 54px; }

/* ─ RESPONSIVE ──────────────────────── */
@media (max-width: 640px) {
  .hero-content h1 { font-size: 36px; }
  .page-hero-content h1 { font-size: 28px; }
  .topnav { padding: 0 16px; }
  .nav-logo { font-size: 18px; }
  .card  { width: 100%; max-width: 320px; }
  .feat-card { width: 100%; max-width: 340px; }
  .why-card  { width: 100%; max-width: 300px; }
  .tabla th, .tabla td { padding: 7px 5px; font-size: 12.5px; }
  .confirm-row { text-align: center; }
}
"""

# ══════════════════════════════════════════════════════════════
#  COMPONENTES HTML COMPARTIDOS
# ══════════════════════════════════════════════════════════════

def make_nav(active='inicio'):
    count = count_carrito()
    pages = [
        ('inicio',   '/',          'Inicio'),
        ('menu',     '/menu',      'Menú'),
        ('nosotros', '/nosotros',  'Nosotros'),
        ('contacto', '/contacto',  'Contacto'),
    ]
    links = ''
    for key, href, label in pages:
        cls = 'active' if key == active else ''
        links += f'<a href="{href}" class="{cls}">{label}</a>'
    cart_label = f'🛒 Mi Pedido ({count})' if count > 0 else '🛒 Mi Pedido'
    links += f'<a href="/menu#carrito" class="nav-cart">{cart_label}</a>'
    return f'<nav class="topnav"><a href="/" class="nav-logo">☕ Homies</a><div class="nav-links">{links}</div></nav>'


FOOTER_HTML = '''
<footer>
  <div class="footer-grid">
    <div class="footer-col">
      <div class="footer-logo">☕ Homies</div>
      <p class="footer-sub">Café y Pastelería · Lima, Perú</p>
      <p>Abrimos todos los días<br>8:00 am – 9:00 pm</p>
    </div>
    <div class="footer-col">
      <h4>Visítanos</h4>
      <p>Blvd. Las Droseras 126</p>
      <p>Espalda del Banco de la Nación</p>
      <p>Paradero Celima, Lima</p>
    </div>
    <div class="footer-col">
      <h4>Menú</h4>
      <a href="/menu#cat-caliente">Cafés Calientes</a>
      <a href="/menu#cat-frio">Cafés Fríos</a>
      <a href="/menu#cat-postre">Postres</a>
      <a href="/menu#cat-sandwich">Sándwiches</a>
      <a href="/menu#cat-jugo">Jugos</a>
    </div>
    <div class="footer-col">
      <h4>Contacto</h4>
      <a href="tel:+51910022587">📞 910 022 587</a>
      <a href="tel:+51935656320">📱 935 656 320</a>
      <a href="#">Instagram: Homiescafe.pe</a>
    </div>
  </div>
  <div class="footer-bottom">
    <p>© 2026 Homies Café y Pastelería · Todos los derechos reservados</p>
  </div>
</footer>'''


BASE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }} · Homies Café</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700&family=Work+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{{ css|safe }}</style>
</head>
<body>
{{ nav|safe }}
{% for msg in messages %}<div class="flash">{{ msg }}</div>{% endfor %}
{{ body|safe }}
{{ footer|safe }}
{% if cart_count > 0 %}
<a href="/menu#carrito" class="float-cart">🛒 <span class="cart-badge">{{ cart_count }}</span></a>
{% endif %}
</body>
</html>"""


def render_page(title, active, body):
    messages = get_flashed_messages()
    return render_template_string(
        BASE,
        title=title,
        css=CSS,
        nav=make_nav(active),
        messages=messages,
        body=body,
        footer=FOOTER_HTML,
        cart_count=count_carrito(),
    )

# ══════════════════════════════════════════════════════════════
#  HELPERS DE CONSTRUCCIÓN HTML
# ══════════════════════════════════════════════════════════════

def product_card(nombre, precio, desc):
    nom_safe = nombre.replace('"', '&quot;')
    return f'''<div class="card"><div class="card-body">
      <h3>{nombre}</h3><p>{desc}</p>
      <div class="price-badge">S/{precio}</div>
      <form method="POST" action="/menu">
        <input type="hidden" name="accion" value="agregar">
        <input type="hidden" name="producto" value="{nom_safe}">
        <button type="submit" class="btn">+ Agregar al pedido</button>
      </form>
    </div></div>'''


def product_grid(items):
    return '<div class="grid">' + ''.join(product_card(n, p, d) for n, p, d in items) + '</div>'


def cat_banner(bid, icon, title, subtitle, img_key):
    url = IMG[img_key]
    return f'''<div class="cat-banner" id="{bid}" style="background-image:url('{url}')">
      <div class="cat-banner-inner">
        <h2>{icon} {title}</h2>
        <p>{subtitle}</p>
      </div>
    </div>'''


def build_carrito_html(carrito, total):
    if not carrito:
        return '<p class="vacio">Tu pedido está vacío. ¡Agrega algo desde el menú! ☝️</p>'
    rows = ''
    for item in carrito:
        sub = item['precio'] * item['cantidad']
        n = item['nombre'].replace('"', '&quot;')
        rows += f'''<tr>
          <td><strong>{item["nombre"]}</strong></td>
          <td>S/{item["precio"]}</td>
          <td><div class="cant-ctrl">
            <form method="POST" action="/menu" style="display:inline">
              <input type="hidden" name="accion" value="disminuir">
              <input type="hidden" name="producto" value="{n}">
              <button type="submit" class="btn-cantidad">−</button>
            </form>
            <span class="cant-num">{item["cantidad"]}</span>
            <form method="POST" action="/menu" style="display:inline">
              <input type="hidden" name="accion" value="aumentar">
              <input type="hidden" name="producto" value="{n}">
              <button type="submit" class="btn-cantidad">+</button>
            </form>
          </div></td>
          <td class="sub-bold">S/{sub}</td>
          <td><form method="POST" action="/menu" style="display:inline">
            <input type="hidden" name="accion" value="quitar">
            <input type="hidden" name="producto" value="{n}">
            <button type="submit" class="btn btn-red btn-sm">Quitar</button>
          </form></td>
        </tr>'''
    return f'''<table class="tabla">
      <tr><th>Producto</th><th>Precio unit.</th><th>Cantidad</th><th>Subtotal</th><th></th></tr>
      {rows}
    </table>
    <div class="total-line">Total a pagar: S/{total}</div>
    <div class="confirm-row">
      <form method="POST" action="/menu">
        <input type="hidden" name="accion" value="confirmar">
        <button type="submit" class="btn btn-vd btn-lg">✅ Confirmar pedido</button>
      </form>
    </div>'''


def build_dashboard_html(carrito, total):
    items   = len(carrito)
    units   = sum(i['cantidad'] for i in carrito)
    ultimo  = carrito[-1]['nombre'] if carrito else '—'
    return f'''<div class="dashboard">
      <h2>📊 Resumen de tu pedido</h2>
      <div class="metricas">
        <div class="metrica"><div class="val">{items}</div><div class="lbl">Productos distintos</div></div>
        <div class="metrica"><div class="val">{units}</div><div class="lbl">Unidades totales</div></div>
        <div class="metrica"><div class="val">S/{total}</div><div class="lbl">Total a pagar</div></div>
        <div class="metrica"><div class="val" style="font-size:16px;line-height:1.3;padding-top:2px;">{ultimo}</div><div class="lbl">Último agregado</div></div>
      </div>
    </div>'''

# ══════════════════════════════════════════════════════════════
#  PÁGINAS
# ══════════════════════════════════════════════════════════════

def page_inicio():
    img = IMG['hero_inicio']
    return f'''
    <div class="hero" style="background-image:url('{img}')">
      <div class="hero-content">
        <span class="eyebrow">Café y Pastelería · Lima, Perú</span>
        <h1>Un lugar para sentirte como en casa</h1>
        <p>Cafés de especialidad, postres artesanales y sándwiches preparados con amor cada día.</p>
        <a href="/menu" class="btn-hero">Ver menú completo</a>
        <a href="/nosotros" class="btn-hero-outline">Nuestra historia</a>
      </div>
    </div>

    <div class="section mt-md">
      <div class="section-header">
        <span class="eyebrow">Lo más pedido</span>
        <h2 class="sec-title">Los favoritos de Homies</h2>
        <div class="sec-line"></div>
      </div>
      <div class="feat-grid">
        <div class="feat-card">
          <img src="{IMG['feat_matcha']}" alt="BerryMatcha Homies" class="feat-img">
          <div class="feat-body">
            <h3>BerryMatcha Homies ⭐</h3>
            <p>Matcha latte con compota de fresas y foto instantánea de regalo. El hit de la temporada.</p>
            <div class="feat-price">S/15</div>
          </div>
        </div>
        <div class="feat-card">
          <img src="{IMG['feat_cake']}" alt="Tartaleta de Fresa" class="feat-img">
          <div class="feat-body">
            <h3>Tartaleta de Fresa</h3>
            <p>Base crujiente con crema pastelera y fresas frescas. Hecha a mano diariamente por nuestros pasteleros.</p>
            <div class="feat-price">S/12</div>
          </div>
        </div>
        <div class="feat-card">
          <img src="{IMG['feat_sandwich']}" alt="Club Sándwich" class="feat-img">
          <div class="feat-body">
            <h3>Club Sándwich</h3>
            <p>Triple de pollo, tocino, lechuga, tomate y mayonesa artesanal. El clásico de Homies.</p>
            <div class="feat-price">S/20</div>
          </div>
        </div>
      </div>
    </div>

    <div class="section mt-lg">
      <div class="section-header">
        <span class="eyebrow">Por qué elegirnos</span>
        <h2 class="sec-title">La experiencia Homies</h2>
        <div class="sec-line"></div>
      </div>
      <div class="why-grid">
        <div class="why-card">
          <div class="why-icon">☕</div>
          <h3>Café de especialidad</h3>
          <p>Granos seleccionados y baristas apasionados que cuidan cada taza desde el primer grano hasta la última gota.</p>
        </div>
        <div class="why-card">
          <div class="why-icon">🍰</div>
          <h3>Pastelería artesanal</h3>
          <p>Postres preparados diariamente con ingredientes frescos por nuestro equipo de pastelería.</p>
        </div>
        <div class="why-card">
          <div class="why-icon">🏡</div>
          <h3>Ambiente acogedor</h3>
          <p>Un espacio pensado para que te sientas como en casa, ideal para trabajar, reunirte o simplemente relajarte.</p>
        </div>
      </div>
    </div>

    <div class="cta-band">
      <h2>¿Tienes ganas de pedir algo?</h2>
      <p>Explora nuestro menú completo y arma tu pedido favorito en segundos.</p>
      <a href="/menu" class="btn btn-mc btn-lg">Ver menú completo →</a>
    </div>
    '''


def page_menu():
    carrito = get_carrito()
    total   = total_carrito()
    img     = IMG['hero_menu']
    return f'''
    <div class="page-hero" style="background-image:url('{img}')">
      <div class="page-hero-content">
        <h1>☕ Nuestro Menú</h1>
        <p>Cafés, postres, sándwiches y jugos — todo hecho con amor</p>
      </div>
    </div>

    <nav class="sub-nav">
      <a href="#cat-caliente">☕ Calientes</a>
      <a href="#cat-frio">🧊 Fríos</a>
      <a href="#cat-frappe">🥤 Frappés</a>
      <a href="#cat-art">🥧 Postres Artesanales</a>
      <a href="#cat-postre">🍰 Más Postres</a>
      <a href="#cat-sandwich">🥪 Sándwiches</a>
      <a href="#cat-jugo">🍹 Jugos</a>
      <a href="#carrito">🛒 Mi Pedido</a>
    </nav>

    <div style="max-width:1180px; margin:0 auto; padding:0 20px 10px;">
      {cat_banner('cat-caliente','☕','Cafés Calientes','Leche entera o sin lactosa · preparados por nuestros baristas','cat_caliente')}
      {product_grid(cafes_calientes)}

      {cat_banner('cat-frio','🧊','Cafés Fríos','Refrescantes, sobre hielo · leche entera o sin lactosa','cat_frio')}
      {product_grid(cafes_frios)}

      {cat_banner('cat-frappe','🥤','Frappés','Batidos, helados y cremosos · el antídoto perfecto para el calor','cat_frappe')}
      {product_grid(frappes)}

      {cat_banner('cat-art','🥧','Postres Artesanales','Los favoritos de la casa · hechos a mano diariamente','cat_postre')}
      {product_grid(postres_artesanales)}

      {cat_banner('cat-postre','🍰','Más Postres','Cheesecakes, tiramisú y nuestros clásicos de siempre','cat_postre')}
      {product_grid(postres)}

      {cat_banner('cat-sandwich','🥪','Sándwiches de la Casa','Preparados al momento con ingredientes frescos','cat_sandwich')}
      {product_grid(sandwiches)}

      {cat_banner('cat-jugo','🍹','Jugos','Naturales, recién exprimidos · sin conservantes','cat_jugo')}
      <div style="text-align:center; margin:18px 0 4px;">
        <span style="font-size:16px; font-weight:700; color:var(--mr); font-family:Fraunces,serif;">Jugos Clásicos · S/9</span>
      </div>
      {product_grid(jugos[:5])}
      <div style="text-align:center; margin:14px 0 4px;">
        <span style="font-size:16px; font-weight:700; color:var(--mr); font-family:Fraunces,serif;">Con Leche · S/12</span>
      </div>
      {product_grid(jugos[5:])}
    </div>

    <div id="carrito" style="max-width:900px; margin:40px auto 20px; padding:0 20px; scroll-margin-top:120px;">
      <div class="carrito-box">
        <h2>🛒 Mi Pedido</h2>
        {build_carrito_html(carrito, total)}
      </div>
    </div>

    <div style="max-width:1180px; margin:20px auto 40px; padding:0 20px;">
      {build_dashboard_html(carrito, total)}
    </div>
    '''


def page_nosotros():
    img = IMG['hero_nosotros']
    return f'''
    <div class="page-hero" style="background-image:url('{img}')">
      <div class="page-hero-content">
        <h1>Sobre Nosotros</h1>
        <p>Conoce la historia detrás de Homies</p>
      </div>
    </div>

    <div class="story">
      <span class="eyebrow">Nuestra historia</span>
      <h2>Nació el 8 de marzo de 2024</h2>
      <p>Homies Café nació con el sueño de crear un espacio acogedor donde cada detalle cuente una historia. Desde el primer día, apostamos por la calidad de cada ingrediente, la dedicación de nuestro equipo y el calor de un lugar que se siente como casa.</p>
      <p>Nuestra pasión por la pastelería y la cocina artesanal se refleja en cada plato: desde los postres más dulces hasta los sabores más reconfortantes. Cada torta, cada café y cada sándwich es preparado con el mismo amor y cuidado de siempre.</p>
      <p style="font-weight:700; color:var(--vd); font-size:19px;">¡Bienvenidos! Disfruten de una experiencia única, llena de sabor y buenos momentos.</p>
    </div>

    <div class="center mt-sm">
      <span class="eyebrow">Nuestros valores</span>
      <h2 style="font-size:28px; color:var(--vd); margin:10px 0 30px;">Lo que nos define</h2>
    </div>

    <div class="val-grid">
      <div class="val-card">
        <div class="val-icon">☕</div>
        <h3>Calidad</h3>
        <p>Ingredientes frescos y bien seleccionados en cada producto que preparamos.</p>
      </div>
      <div class="val-card">
        <div class="val-icon">🏡</div>
        <h3>Calidez</h3>
        <p>Cada visita debe sentirse como volver a casa. Nuestro espacio fue diseñado para eso.</p>
      </div>
      <div class="val-card">
        <div class="val-icon">🎨</div>
        <h3>Creatividad</h3>
        <p>Combinamos sabores peruanos con tendencias internacionales en nuestra carta.</p>
      </div>
      <div class="val-card">
        <div class="val-icon">❤️</div>
        <h3>Pasión</h3>
        <p>Cada taza de café y cada postre son elaborados con genuina pasión por lo que hacemos.</p>
      </div>
    </div>

    <div class="cta-band">
      <h2>¿Tienes ganas de visitarnos?</h2>
      <p>Estamos esperándote con la mejor carta de Lima y un ambiente que te hará sentir en casa.</p>
      <a href="/contacto" class="btn btn-mc btn-lg">¿Dónde estamos? →</a>
    </div>
    '''


def page_contacto():
    img = IMG['hero_contacto']
    return f'''
    <div class="page-hero" style="background-image:url('{img}')">
      <div class="page-hero-content">
        <h1>📍 Contáctanos</h1>
        <p>Estamos en Lima, esperándote con el café listo</p>
      </div>
    </div>

    <div class="center" style="padding:54px 0 0;">
      <span class="eyebrow">¿Cómo llegar?</span>
      <h2 style="font-size:28px; color:var(--vd); margin:10px 0 32px;">Encuéntranos</h2>
    </div>

    <div class="contact-grid">
      <div class="contact-card">
        <div class="contact-icon">📍</div>
        <h3>Dirección</h3>
        <p>Blvd. Las Droseras 126<br>Espalda del Banco de la Nación<br>Paradero Celima, Lima</p>
      </div>
      <div class="contact-card">
        <div class="contact-icon">🕐</div>
        <h3>Horario</h3>
        <p>Lunes a Viernes<br>8:00 am – 9:00 pm<br><br>Sábados y Domingos<br>8:00 am – 10:00 pm</p>
      </div>
      <div class="contact-card">
        <div class="contact-icon">📞</div>
        <h3>Teléfonos</h3>
        <p>
          <a href="tel:+51910022587">910 022 587</a><br>
          <a href="tel:+51935656320">935 656 320</a>
        </p>
      </div>
      <div class="contact-card">
        <div class="contact-icon">📱</div>
        <h3>Redes Sociales</h3>
        <p>
          <a href="#">Pastelería Homies</a><br>
          <a href="#">Homies Café</a><br>
          <a href="#">Homiescafe.pe</a>
        </p>
      </div>
    </div>

    <div class="center">
      <a href="https://wa.me/51910022587" target="_blank" class="btn-wa">💬 Escribirnos por WhatsApp</a>
    </div>

    <div class="cta-band">
      <h2>¿Listo para pedir?</h2>
      <p>Explora nuestro menú completo y arma tu pedido favorito.</p>
      <a href="/menu" class="btn btn-mc btn-lg">Ver menú →</a>
    </div>
    '''

# ══════════════════════════════════════════════════════════════
#  RUTAS FLASK
# ══════════════════════════════════════════════════════════════

@app.route('/')
def inicio():
    return render_page('Inicio', 'inicio', page_inicio())


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        carrito = get_carrito()
        accion  = request.form.get('accion', '')
        nombre  = request.form.get('producto', '')
        item    = next((i for i in carrito if i['nombre'] == nombre), None)

        if accion == 'agregar':
            if nombre not in productos:
                flash('⚠️ Ese producto ya no está disponible.')
            elif item:
                item['cantidad'] += 1
                flash(f"🛒 Una unidad más de '{nombre}'.")
            else:
                carrito.append({'nombre': nombre, 'precio': productos[nombre], 'cantidad': 1})
                flash(f"🛒 '{nombre}' agregado a tu pedido.")

        elif accion == 'aumentar':
            if item:
                item['cantidad'] += 1
                flash(f"➕ Cantidad de '{nombre}' aumentada.")

        elif accion == 'disminuir':
            if item:
                item['cantidad'] -= 1
                if item['cantidad'] <= 0:
                    carrito = [i for i in carrito if i['nombre'] != nombre]
                    flash(f"➖ '{nombre}' removido del pedido.")
                else:
                    flash(f"➖ Cantidad de '{nombre}' reducida.")

        elif accion == 'quitar':
            carrito = [i for i in carrito if i['nombre'] != nombre]
            flash(f"🗑️ '{nombre}' quitado del pedido.")

        elif accion == 'confirmar':
            if carrito:
                t = sum(i['precio'] * i['cantidad'] for i in carrito)
                flash(f"✅ ¡Pedido confirmado por S/{t}! En breve lo preparamos 🎉")
                carrito = []
            else:
                flash('⚠️ Tu pedido está vacío. ¡Agrega algo primero!')

        save_carrito(carrito)
        return redirect(url_for('menu'))

    return render_page('Menú', 'menu', page_menu())


@app.route('/nosotros')
def nosotros():
    return render_page('Nosotros', 'nosotros', page_nosotros())


@app.route('/contacto')
def contacto():
    return render_page('Contacto', 'contacto', page_contacto())


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
