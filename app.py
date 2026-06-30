from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# ──────────────────────────────────────────────
# Catálogo de productos por categoría (fijo, definido por el negocio)
# ──────────────────────────────────────────────

cafes_calientes = [
    ("Espresso", 7),
    ("Americano", 8),
    ("Cortado", 7),
    ("Machiatto", 7),
    ("Latte", 10),
    ("Capuccino", 9),
    ("Chocolate Caliente", 9),
    ("Café Mocha", 10),
    ("Vainilla Latte", 12),
    ("Matcha Latte", 14),
]

cafes_frios = [
    ("Iced Americano", 10),
    ("Affogato", 9),
    ("Iced Latte", 12),
    ("Iced Capuccino", 10),
    ("Iced Cinnamon", 11),
    ("Iced Mocha", 11),
    ("Iced Caramel", 11),
    ("Iced Vainilla Latte", 14),
    ("Iced Matcha Latte", 16),
    ("Iced Coconut Matcha", 13),
]

frappes = [
    ("Frappé Chocolate", 14),
    ("Frappé Mocha", 14),
    ("Frappé Oreo", 14),
    ("Frappé Caramelo", 14),
    ("Frappé Menta", 14),
    ("BerryMatcha Homies", 15),
]

postres = [
    ("Cheesecake Maracuyá", 10),
    ("Cheesecake Oreo", 10),
    ("Cheesecake Clásico", 10),
    ("NY Cheesecake", 15),
    ("Torta de Chocolate", 12),
    ("Tiramisú", 12),
    ("Tres Leches Chocolate", 9),
    ("Tres Leches Vainilla", 9),
    ("Carrot Cake", 11),
]

postres_artesanales = [
    ("Pionono de Chocolúcuma", 8),
    ("Crema Volteada", 9),
    ("Tres Leches de Vainilla", 9),
    ("Tres Leches de Chocolate", 9),
    ("Tarta de Manzana", 9),
    ("Tarta de Limón", 10),
    ("Torta Moka", 11),
    ("Carrot Cake", 11),
    ("Torta de Chocolate", 12),
    ("Tartaleta de Fresa", 12),
]

sandwiches = [
    ("Mixto Simple", 12),
    ("Mixto Especial", 16),
    ("Charsiu", 18),
    ("Club Sandwich", 20),
    ("Pollo Deshilachado", 16),
    ("Capresse", 16),
    ("Pollo Deshilachado con Palta", 18),
    ("Pollo Deshilachado con Durazno", 20),
]

jugos = [
    ("Jugo de Papaya", 9),
    ("Jugo de Piña", 9),
    ("Jugo de Fresa", 9),
    ("Jugo de Naranja", 9),
    ("Jugo de Mango", 9),
    ("Papaya con Leche", 12),
    ("Fresa con Leche", 12),
    ("Mango con Leche", 12),
]

# Diccionario único de productos y precios (catálogo del negocio)
productos = {}
for nombre, precio in (
    cafes_calientes + cafes_frios + frappes + postres + postres_artesanales
    + sandwiches + jugos
):
    productos[nombre] = precio

# ──────────────────────────────────────────────
# Carrito del cliente: lista de diccionarios {nombre, precio, cantidad}
# Persiste en memoria mientras el servidor esté activo.
# ──────────────────────────────────────────────
carrito = []

# Mensaje de feedback para el usuario tras cada acción sobre su pedido
mensaje = ""


HTML = """
<!DOCTYPE html>
<html lang="es">
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>Homies Café y Pastelería</title>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,500&family=Work+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>

:root{
  --verde-oscuro:#1B3328;
  --verde-medio:#28503E;
  --verde-salvia:#8E9B6D;
  --marron:#6B4226;
  --marron-claro:#B98D63;
  --crema:#FAF6EC;
  --crema-card:#FFFFFF;
  --texto:#2B2A23;
  --texto-suave:#6B6A5E;
  --sombra:0 8px 24px rgba(27,51,40,0.08);
}

*{
  margin:0;
  padding:0;
  box-sizing:border-box;
}

body{
  background:var(--crema);
  color:var(--texto);
  font-family:'Work Sans', Arial, sans-serif;
  line-height:1.5;
}

h1,h2,h3{
  font-family:'Fraunces', Georgia, serif;
}

/* ---------- HEADER ---------- */
header{
  background:linear-gradient(135deg, var(--verde-oscuro), var(--verde-medio));
  color:#fff;
  padding:34px 25px 28px;
  text-align:center;
  position:relative;
}

header::after{
  content:"";
  display:block;
  width:70px;
  height:3px;
  background:var(--marron-claro);
  margin:14px auto 0;
  border-radius:3px;
}

header h1{
  font-size:46px;
  font-weight:700;
  letter-spacing:0.5px;
}

header p{
  margin-top:6px;
  font-size:14px;
  letter-spacing:3px;
  text-transform:uppercase;
  color:var(--marron-claro);
  font-weight:600;
}

/* ---------- NAV ---------- */
nav{
  background:var(--verde-oscuro);
  padding:12px 16px;
  display:flex;
  gap:8px;
  overflow-x:auto;
  white-space:nowrap;
  position:sticky;
  top:0;
  z-index:50;
  border-top:1px solid rgba(255,255,255,0.08);
  scrollbar-width:thin;
}

nav a{
  color:#EDE7DA;
  text-decoration:none;
  font-weight:600;
  font-size:13.5px;
  padding:8px 16px;
  border-radius:999px;
  transition:background 0.2s ease, color 0.2s ease;
  flex-shrink:0;
}

nav a:hover{
  background:var(--marron-claro);
  color:var(--verde-oscuro);
}

/* ---------- HERO ---------- */
.hero{
  background:linear-gradient(180deg, var(--verde-salvia) 0%, var(--crema) 100%);
  padding:54px 24px 44px;
  text-align:center;
}

.hero h1{
  font-size:38px;
  color:var(--verde-oscuro);
  margin-bottom:12px;
}

.hero p{
  font-size:17px;
  color:var(--texto-suave);
  max-width:520px;
  margin:0 auto;
}

/* ---------- MENSAJE FLASH ---------- */
.mensaje{
  background:#E7EFD9;
  color:var(--verde-oscuro);
  border-left:4px solid var(--verde-salvia);
  padding:12px 20px;
  border-radius:8px;
  margin:20px auto 0;
  max-width:700px;
  font-weight:600;
  text-align:center;
}

/* ---------- SECCIONES ---------- */
.seccion{
  padding:46px 20px 10px;
  max-width:1180px;
  margin:0 auto;
}

.seccion-header{
  text-align:center;
  margin-bottom:32px;
}

.eyebrow{
  display:inline-block;
  font-size:12px;
  letter-spacing:3px;
  text-transform:uppercase;
  color:var(--marron);
  font-weight:700;
  margin-bottom:6px;
}

.titulo{
  font-size:30px;
  color:var(--verde-oscuro);
  font-weight:600;
}

.titulo-linea{
  width:54px;
  height:3px;
  background:var(--marron-claro);
  border-radius:3px;
  margin:14px auto 0;
}

.subseccion-titulo{
  font-size:21px;
  color:var(--marron);
  font-weight:600;
  text-align:center;
  margin:36px 0 20px;
  position:relative;
}

.subseccion-titulo:first-of-type{
  margin-top:0;
}

/* ---------- GRID DE PRODUCTOS ---------- */
.contenedor{
  display:flex;
  flex-wrap:wrap;
  justify-content:center;
  gap:20px;
  padding:6px 0 10px;
}

.card{
  background:var(--crema-card);
  width:255px;
  padding:22px 20px 20px;
  border-radius:14px;
  box-shadow:var(--sombra);
  border-top:4px solid var(--marron-claro);
  transition:transform 0.18s ease, box-shadow 0.18s ease;
  display:flex;
  flex-direction:column;
}

.card:hover{
  transform:translateY(-4px);
  box-shadow:0 14px 28px rgba(27,51,40,0.14);
}

.card h3{
  color:var(--verde-oscuro);
  font-size:18px;
  margin-bottom:8px;
}

.card p{
  font-size:13.5px;
  color:var(--texto-suave);
  margin-bottom:14px;
  flex-grow:1;
}

.precio{
  display:inline-block;
  align-self:flex-start;
  background:var(--verde-salvia);
  color:#fff;
  font-weight:700;
  font-size:14px;
  padding:5px 14px;
  border-radius:999px;
  margin-bottom:14px;
}

button{
  background:var(--marron);
  color:white;
  border:none;
  padding:11px;
  width:100%;
  border-radius:8px;
  cursor:pointer;
  font-weight:600;
  font-size:14px;
  transition:background 0.2s ease;
}

button:hover{
  background:#532F19;
}

/* ---------- CARRITO ---------- */
.carrito{
  background:var(--crema-card);
  padding:28px 24px;
  margin:30px auto;
  max-width:900px;
  border-radius:16px;
  box-shadow:var(--sombra);
  border-top:4px solid var(--verde-salvia);
}

.carrito h2{
  color:var(--verde-oscuro);
  margin-bottom:18px;
  font-size:24px;
}

.tabla-carrito{
  width:100%;
  border-collapse:collapse;
  margin-top:10px;
}

.tabla-carrito th,
.tabla-carrito td{
  text-align:left;
  padding:11px 10px;
  border-bottom:1px solid #EFEAE0;
  font-size:14px;
}

.tabla-carrito th{
  background:#F2EFE5;
  color:var(--verde-oscuro);
  text-transform:uppercase;
  font-size:12px;
  letter-spacing:0.5px;
}

.cantidad-control{
  display:flex;
  align-items:center;
  gap:8px;
}

.btn-cantidad{
  width:30px;
  height:30px;
  padding:0;
  font-size:16px;
  border-radius:6px;
}

.btn-quitar{
  background:#A8442F;
  width:auto;
  padding:6px 14px;
  font-size:12.5px;
}

.btn-quitar:hover{
  background:#82331F;
}

.subtotal{
  font-weight:700;
  color:var(--verde-oscuro);
}

.total-final{
  text-align:right;
  font-size:21px;
  font-weight:700;
  color:var(--verde-oscuro);
  margin-top:16px;
}

.btn-confirmar{
  background:var(--verde-oscuro);
  margin-top:16px;
  width:auto;
  padding:14px 32px;
  font-size:15px;
  float:right;
}

.btn-confirmar:hover{
  background:#0F2018;
}

.vacio{
  text-align:center;
  color:var(--texto-suave);
  padding:24px;
  font-size:14.5px;
}

/* ---------- DASHBOARD ---------- */
.dashboard{
  background:var(--verde-oscuro);
  padding:30px 24px;
  margin:30px auto 0;
  max-width:1180px;
  border-radius:16px;
}

.dashboard h2{
  margin-bottom:18px;
  color:#fff;
  font-size:22px;
}

.metricas{
  display:flex;
  flex-wrap:wrap;
  gap:18px;
}

.metrica{
  background:rgba(255,255,255,0.06);
  border:1px solid rgba(255,255,255,0.12);
  flex:1;
  min-width:180px;
  padding:20px;
  border-radius:12px;
  text-align:center;
}

.metrica .valor{
  font-size:27px;
  font-weight:700;
  color:var(--marron-claro);
  font-family:'Fraunces', serif;
}

.metrica .etiqueta{
  font-size:13px;
  color:#D8D3C5;
  margin-top:6px;
}

/* ---------- FOOTER ---------- */
footer{
  background:var(--verde-oscuro);
  color:#D8D3C5;
  text-align:center;
  padding:26px;
  margin-top:50px;
  border-top:3px solid var(--marron-claro);
  font-size:13.5px;
}

/* ---------- RESPONSIVE ---------- */
@media (max-width:600px){
  header h1{font-size:34px;}
  .hero h1{font-size:28px;}
  .titulo{font-size:24px;}
  .card{width:100%;max-width:320px;}
  .btn-confirmar{float:none;width:100%;}
  .total-final{text-align:center;}
}

</style>

</head>

<body>

<header>
<h1>☕ Homies</h1>
<p>Café y Pastelería</p>
</header>

<nav>
<a href="#cafes-calientes">Cafés Calientes</a>
<a href="#cafes-frios">Cafés Fríos</a>
<a href="#frappes">Frappés</a>
<a href="#postres-artesanales">Postres Artesanales</a>
<a href="#postres">Más Postres</a>
<a href="#sandwiches">Sándwiches</a>
<a href="#jugos">Jugos</a>
<a href="#carrito">Mi Pedido</a>
<a href="#dashboard">Resumen</a>
</nav>

<section class="hero">
<h1>Bienvenido a Homies</h1>
<p>Sabores artesanales, cafés de especialidad y postres preparados diariamente, en un espacio cálido pensado para ti.</p>
</section>

{% if mensaje %}
<div class="mensaje">{{ mensaje }}</div>
{% endif %}

<section class="seccion" id="cafes-calientes">
<div class="seccion-header">
<span class="eyebrow">Recién preparados</span>
<h2 class="titulo">☕ Cafés Calientes</h2>
<div class="titulo-linea"></div>
</div>

<div class="contenedor">

{% for nombre, precio in cafes_calientes %}
<div class="card">
<h3>{{ nombre }}</h3>
<p>Café de especialidad preparado por nuestros baristas.</p>
<div class="precio">S/{{ precio }}</div>

<form method="POST">
<input type="hidden" name="accion" value="agregar">
<input type="hidden" name="producto" value="{{ nombre }}">
<button type="submit">Agregar al pedido</button>
</form>

</div>
{% endfor %}

</div>
</section>

<section class="seccion" id="cafes-frios">
<div class="seccion-header">
<span class="eyebrow">Para refrescarte</span>
<h2 class="titulo">🧊 Cafés Fríos</h2>
<div class="titulo-linea"></div>
</div>

<div class="contenedor">

{% for nombre, precio in cafes_frios %}
<div class="card">
<h3>{{ nombre }}</h3>
<p>Preparado con hielo y leche entera o sin lactosa, a elección.</p>
<div class="precio">S/{{ precio }}</div>

<form method="POST">
<input type="hidden" name="accion" value="agregar">
<input type="hidden" name="producto" value="{{ nombre }}">
<button type="submit">Agregar al pedido</button>
</form>

</div>
{% endfor %}

</div>
</section>

<section class="seccion" id="frappes">
<div class="seccion-header">
<span class="eyebrow">Helados y cremosos</span>
<h2 class="titulo">🥤 Frappés</h2>
<div class="titulo-linea"></div>
</div>

<div class="contenedor">

{% for nombre, precio in frappes %}
<div class="card">
<h3>{{ nombre }}</h3>
<p>Bebida fría y cremosa, batida hasta lograr la textura perfecta.</p>
<div class="precio">S/{{ precio }}</div>

<form method="POST">
<input type="hidden" name="accion" value="agregar">
<input type="hidden" name="producto" value="{{ nombre }}">
<button type="submit">Agregar al pedido</button>
</form>

</div>
{% endfor %}

</div>
</section>

<section class="seccion" id="postres-artesanales">
<div class="seccion-header">
<span class="eyebrow">Los favoritos de la casa</span>
<h2 class="titulo">🥧 Postres Artesanales</h2>
<div class="titulo-linea"></div>
</div>

<div class="contenedor">

{% for nombre, precio in postres_artesanales %}
<div class="card">
<h3>{{ nombre }}</h3>
<p>Hecho a mano por nuestro equipo de pastelería.</p>
<div class="precio">S/{{ precio }}</div>

<form method="POST">
<input type="hidden" name="accion" value="agregar">
<input type="hidden" name="producto" value="{{ nombre }}">
<button type="submit">Agregar al pedido</button>
</form>

</div>
{% endfor %}

</div>
</section>

<section class="seccion" id="postres">
<div class="seccion-header">
<span class="eyebrow">Dulces clásicos</span>
<h2 class="titulo">🍰 Más Postres</h2>
<div class="titulo-linea"></div>
</div>

<div class="contenedor">

{% for nombre, precio in postres %}
<div class="card">
<h3>{{ nombre }}</h3>
<p>Postre artesanal preparado diariamente.</p>
<div class="precio">S/{{ precio }}</div>

<form method="POST">
<input type="hidden" name="accion" value="agregar">
<input type="hidden" name="producto" value="{{ nombre }}">
<button type="submit">Agregar al pedido</button>
</form>

</div>
{% endfor %}

</div>
</section>

<section class="seccion" id="sandwiches">
<div class="seccion-header">
<span class="eyebrow">Sándwiches de la casa</span>
<h2 class="titulo">🥪 Sándwiches</h2>
<div class="titulo-linea"></div>
</div>

<div class="contenedor">

{% for nombre, precio in sandwiches %}
<div class="card">
<h3>{{ nombre }}</h3>
<p>Preparado al momento con ingredientes frescos.</p>
<div class="precio">S/{{ precio }}</div>

<form method="POST">
<input type="hidden" name="accion" value="agregar">
<input type="hidden" name="producto" value="{{ nombre }}">
<button type="submit">Agregar al pedido</button>
</form>

</div>
{% endfor %}

</div>
</section>

<section class="seccion" id="jugos">
<div class="seccion-header">
<span class="eyebrow">Naturales, recién exprimidos</span>
<h2 class="titulo">🍹 Jugos</h2>
<div class="titulo-linea"></div>
</div>

<h3 class="subseccion-titulo">Jugos Clásicos</h3>
<div class="contenedor">

{% for nombre, precio in jugos[:5] %}
<div class="card">
<h3>{{ nombre }}</h3>
<p>Fruta natural recién exprimida.</p>
<div class="precio">S/{{ precio }}</div>

<form method="POST">
<input type="hidden" name="accion" value="agregar">
<input type="hidden" name="producto" value="{{ nombre }}">
<button type="submit">Agregar al pedido</button>
</form>

</div>
{% endfor %}

</div>

<h3 class="subseccion-titulo">Con Leche</h3>
<div class="contenedor">

{% for nombre, precio in jugos[5:] %}
<div class="card">
<h3>{{ nombre }}</h3>
<p>Fruta natural combinada con leche entera.</p>
<div class="precio">S/{{ precio }}</div>

<form method="POST">
<input type="hidden" name="accion" value="agregar">
<input type="hidden" name="producto" value="{{ nombre }}">
<button type="submit">Agregar al pedido</button>
</form>

</div>
{% endfor %}

</div>
</section>

<section id="carrito">

<div class="carrito">

<h2>🛒 Mi Pedido</h2>

{% if carrito %}

<table class="tabla-carrito">
<tr>
<th>Producto</th>
<th>Precio unit.</th>
<th>Cantidad</th>
<th>Subtotal</th>
<th></th>
</tr>

{% for item in carrito %}
<tr>
<td>{{ item.nombre }}</td>
<td>S/{{ item.precio }}</td>
<td>
<div class="cantidad-control">

<form method="POST" style="display:inline;">
<input type="hidden" name="accion" value="disminuir">
<input type="hidden" name="producto" value="{{ item.nombre }}">
<button type="submit" class="btn-cantidad">−</button>
</form>

<span>{{ item.cantidad }}</span>

<form method="POST" style="display:inline;">
<input type="hidden" name="accion" value="aumentar">
<input type="hidden" name="producto" value="{{ item.nombre }}">
<button type="submit" class="btn-cantidad">+</button>
</form>

</div>
</td>
<td class="subtotal">S/{{ item.precio * item.cantidad }}</td>
<td>
<form method="POST" style="display:inline;">
<input type="hidden" name="accion" value="quitar">
<input type="hidden" name="producto" value="{{ item.nombre }}">
<button type="submit" class="btn-quitar">Quitar</button>
</form>
</td>
</tr>
{% endfor %}

</table>

<div class="total-final">Total a pagar: S/{{ total }}</div>

<form method="POST">
<input type="hidden" name="accion" value="confirmar">
<button type="submit" class="btn-confirmar">Confirmar pedido</button>
</form>

{% else %}

<p class="vacio">Tu pedido está vacío. Agrega productos desde el menú.</p>

{% endif %}

</div>

</section>

<section id="dashboard">

<div class="dashboard">

<h2>📊 Resumen de tu pedido</h2>

<div class="metricas">

<div class="metrica">
<div class="valor">{{ cantidad_items }}</div>
<div class="etiqueta">Productos distintos</div>
</div>

<div class="metrica">
<div class="valor">{{ cantidad_total }}</div>
<div class="etiqueta">Unidades en tu pedido</div>
</div>

<div class="metrica">
<div class="valor">S/{{ total }}</div>
<div class="etiqueta">Total a pagar</div>
</div>

<div class="metrica">
<div class="valor">{{ ultimo if ultimo else "—" }}</div>
<div class="etiqueta">Último producto agregado</div>
</div>

</div>

</div>

</section>

<footer>
<p>© 2026 Homies Café y Pastelería · Blvd. Las Droseras 126, Lima</p>
</footer>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def inicio():
    global carrito, mensaje

    mensaje = ""

    if request.method == "POST":
        accion = request.form.get("accion")
        nombre = request.form.get("producto", "")

        # Buscar si el producto ya está en el carrito
        item_existente = next((i for i in carrito if i["nombre"] == nombre), None)

        if accion == "agregar":
            if nombre not in productos:
                mensaje = "⚠️ Ese producto ya no está disponible."
            elif item_existente:
                item_existente["cantidad"] += 1
                mensaje = f"🛒 Se agregó otra unidad de '{nombre}' a tu pedido."
            else:
                carrito.append({
                    "nombre": nombre,
                    "precio": productos[nombre],
                    "cantidad": 1,
                })
                mensaje = f"🛒 '{nombre}' agregado a tu pedido."

        elif accion == "aumentar":
            if item_existente:
                item_existente["cantidad"] += 1
                mensaje = f"➕ Se aumentó la cantidad de '{nombre}'."

        elif accion == "disminuir":
            if item_existente:
                item_existente["cantidad"] -= 1
                if item_existente["cantidad"] <= 0:
                    carrito = [i for i in carrito if i["nombre"] != nombre]
                    mensaje = f"➖ '{nombre}' fue removido de tu pedido."
                else:
                    mensaje = f"➖ Se disminuyó la cantidad de '{nombre}'."

        elif accion == "quitar":
            if item_existente:
                carrito = [i for i in carrito if i["nombre"] != nombre]
                mensaje = f"🗑️ '{nombre}' fue quitado de tu pedido."

        elif accion == "confirmar":
            if carrito:
                total_confirmado = sum(i["precio"] * i["cantidad"] for i in carrito)
                mensaje = f"✅ ¡Pedido confirmado! Total: S/{total_confirmado}. Pronto lo estaremos preparando."
                carrito = []
            else:
                mensaje = "⚠️ Tu pedido está vacío, agrega productos antes de confirmar."

    total = sum(i["precio"] * i["cantidad"] for i in carrito)
    cantidad_items = len(carrito)
    cantidad_total = sum(i["cantidad"] for i in carrito)
    ultimo = carrito[-1]["nombre"] if carrito else ""

    return render_template_string(
        HTML,
        cafes_calientes=cafes_calientes,
        cafes_frios=cafes_frios,
        frappes=frappes,
        postres=postres,
        postres_artesanales=postres_artesanales,
        sandwiches=sandwiches,
        jugos=jugos,
        carrito=carrito,
        total=total,
        cantidad_items=cantidad_items,
        cantidad_total=cantidad_total,
        ultimo=ultimo,
        mensaje=mensaje,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
