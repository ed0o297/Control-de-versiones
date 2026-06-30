from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# ──────────────────────────────────────────────
# Catálogo de productos por categoría (fijo, definido por el negocio)
# ──────────────────────────────────────────────
cafes = [
    ("Espresso", 7),
    ("Americano", 8),
    ("Latte", 10),
    ("Vainilla Latte", 12),
    ("Matcha Latte", 14),
    ("Iced Americano", 10),
    ("Iced Latte", 12),
    ("Iced Vainilla Latte", 14),
    ("Iced Matcha Latte", 16),
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

sandwiches = [
    ("Mixto Simple", 12),
    ("Mixto Especial", 16),
    ("Charsiu", 18),
    ("Club Sandwich", 20),
]

# Diccionario único de productos y precios (catálogo del negocio)
productos = {}
for nombre, precio in cafes + postres + sandwiches:
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

<title>Homies</title>

<style>

*{
margin:0;
padding:0;
box-sizing:border-box;
font-family:Arial,sans-serif;
}

body{
background:#f5f5f5;
}

header{
background:#006241;
color:white;
padding:25px;
text-align:center;
}

nav{
background:#1e3932;
padding:15px;
text-align:center;
}

nav a{
color:white;
text-decoration:none;
margin:15px;
font-weight:bold;
}

.hero{
background:white;
padding:40px;
text-align:center;
}

.hero h1{
font-size:42px;
margin-bottom:10px;
}

.hero p{
font-size:18px;
color:#555;
}

.contenedor{
display:flex;
flex-wrap:wrap;
justify-content:center;
gap:20px;
padding:20px;
}

.card{
background:white;
width:280px;
padding:20px;
border-radius:15px;
box-shadow:0 2px 10px rgba(0,0,0,0.1);
}

.card h3{
color:#006241;
margin-bottom:10px;
}

.card p{
margin-bottom:10px;
}

.precio{
font-weight:bold;
font-size:18px;
margin-bottom:10px;
}

button{
background:#006241;
color:white;
border:none;
padding:10px;
width:100%;
border-radius:8px;
cursor:pointer;
}

button:hover{
background:#004d33;
}

.seccion{
padding:30px;
}

.titulo{
text-align:center;
font-size:32px;
margin-bottom:25px;
color:#1e3932;
}

.carrito{
background:white;
padding:25px;
margin:30px;
border-radius:15px;
box-shadow:0 2px 10px rgba(0,0,0,0.1);
}

.carrito h2{
color:#1e3932;
margin-bottom:20px;
}

.tabla-carrito{
width:100%;
border-collapse:collapse;
margin-top:10px;
}

.tabla-carrito th,
.tabla-carrito td{
text-align:left;
padding:10px;
border-bottom:1px solid #eee;
}

.tabla-carrito th{
background:#f0f0f0;
color:#1e3932;
}

.cantidad-control{
display:flex;
align-items:center;
gap:8px;
}

.btn-cantidad{
width:32px;
height:32px;
padding:0;
font-size:16px;
border-radius:6px;
}

.btn-quitar{
background:#c0392b;
width:auto;
padding:6px 14px;
font-size:13px;
}

.btn-quitar:hover{
background:#922b21;
}

.subtotal{
font-weight:bold;
}

.total-final{
text-align:right;
font-size:22px;
font-weight:bold;
color:#006241;
margin-top:15px;
}

.dashboard{
background:#e8f5e9;
padding:25px;
margin:30px;
border-radius:15px;
}

.dashboard h2{
margin-bottom:15px;
color:#1e3932;
}

.metricas{
display:flex;
flex-wrap:wrap;
gap:20px;
margin-top:15px;
}

.metrica{
background:white;
flex:1;
min-width:180px;
padding:20px;
border-radius:12px;
text-align:center;
box-shadow:0 2px 8px rgba(0,0,0,0.08);
}

.metrica .valor{
font-size:28px;
font-weight:bold;
color:#006241;
}

.metrica .etiqueta{
font-size:14px;
color:#555;
margin-top:5px;
}

.btn-confirmar{
background:#1e3932;
margin-top:15px;
width:auto;
padding:14px 30px;
font-size:16px;
}

.btn-confirmar:hover{
background:#13241f;
}

.mensaje{
background:#d4edda;
color:#155724;
padding:12px 20px;
border-radius:8px;
margin:20px 30px 0 30px;
font-weight:bold;
text-align:center;
}

.vacio{
text-align:center;
color:#888;
padding:20px;
}

footer{
background:#1e3932;
color:white;
text-align:center;
padding:20px;
margin-top:40px;
}

</style>

</head>

<body>

<header>
<h1>☕ Homies</h1>
<p>Cafetería de Especialidad - Lima, Perú</p>
</header>

<nav>
<a href="#cafes">Cafés</a>
<a href="#postres">Postres</a>
<a href="#sandwiches">Sándwiches</a>
<a href="#carrito">Mi Pedido</a>
<a href="#dashboard">Resumen</a>
</nav>

<section class="hero">
<h1>Bienvenido a Homies</h1>
<p>Sabores artesanales, cafés de especialidad y postres preparados diariamente.</p>
</section>

{% if mensaje %}
<div class="mensaje">{{ mensaje }}</div>
{% endif %}

<section class="seccion" id="cafes">
<h2 class="titulo">☕ Cafés</h2>

<div class="contenedor">

{% for nombre, precio in cafes %}
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

<section class="seccion" id="postres">
<h2 class="titulo">🍰 Postres</h2>

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
<h2 class="titulo">🥪 Sándwiches</h2>

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
<p>© 2026 Homies - Proyecto Flask</p>
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
        cafes=cafes,
        postres=postres,
        sandwiches=sandwiches,
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
