from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# ──────────────────────────────────────────────
# Catálogo de productos por categoría
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

# Diccionario único de productos (fuente de verdad para el CRUD y el carrito)
productos = {}
for nombre, precio in cafes + postres + sandwiches:
    productos[nombre] = precio

# Carrito en memoria (persiste mientras el servidor esté activo)
carrito = []

# Mensaje de feedback para el usuario tras cada acción (CRUD)
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
padding:20px;
margin:30px;
border-radius:15px;
box-shadow:0 2px 10px rgba(0,0,0,0.1);
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

.crud{
background:white;
padding:25px;
margin:30px;
border-radius:15px;
box-shadow:0 2px 10px rgba(0,0,0,0.1);
}

.crud h2{
color:#1e3932;
margin-bottom:20px;
}

.crud h3{
color:#006241;
margin-bottom:10px;
margin-top:20px;
}

.crud-form{
display:flex;
flex-wrap:wrap;
gap:10px;
align-items:center;
margin-bottom:10px;
}

.crud-form input[type="text"],
.crud-form input[type="number"]{
padding:10px;
border:1px solid #ccc;
border-radius:8px;
flex:1;
min-width:160px;
}

.crud-form button{
width:auto;
padding:10px 20px;
}

.tabla-productos{
width:100%;
border-collapse:collapse;
margin-top:15px;
}

.tabla-productos th,
.tabla-productos td{
text-align:left;
padding:10px;
border-bottom:1px solid #eee;
}

.tabla-productos th{
background:#f0f0f0;
color:#1e3932;
}

.btn-eliminar{
background:#c0392b;
width:auto;
padding:6px 14px;
font-size:13px;
}

.btn-eliminar:hover{
background:#922b21;
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
<a href="#carrito">Carrito</a>
<a href="#dashboard">Dashboard</a>
<a href="#crud">Administrar</a>
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
{% if nombre in productos %}
<div class="card">
<h3>{{ nombre }}</h3>
<p>Café de especialidad preparado por nuestros baristas.</p>
<div class="precio">S/{{ productos[nombre] }}</div>

<form method="POST">
<input type="hidden" name="producto" value="{{ nombre }}">
<button type="submit">Agregar al carrito</button>
</form>

</div>
{% endif %}
{% endfor %}

</div>
</section>

<section class="seccion" id="postres">
<h2 class="titulo">🍰 Postres</h2>

<div class="contenedor">

{% for nombre, precio in postres %}
{% if nombre in productos %}
<div class="card">
<h3>{{ nombre }}</h3>
<p>Postre artesanal preparado diariamente.</p>
<div class="precio">S/{{ productos[nombre] }}</div>

<form method="POST">
<input type="hidden" name="producto" value="{{ nombre }}">
<button type="submit">Agregar al carrito</button>
</form>

</div>
{% endif %}
{% endfor %}

</div>
</section>

<section class="seccion" id="sandwiches">
<h2 class="titulo">🥪 Sándwiches</h2>

<div class="contenedor">

{% for nombre, precio in sandwiches %}
{% if nombre in productos %}
<div class="card">
<h3>{{ nombre }}</h3>
<p>Preparado al momento con ingredientes frescos.</p>
<div class="precio">S/{{ productos[nombre] }}</div>

<form method="POST">
<input type="hidden" name="producto" value="{{ nombre }}">
<button type="submit">Agregar al carrito</button>
</form>

</div>
{% endif %}
{% endfor %}

</div>
</section>

<section id="carrito">

<div class="carrito">

<h2>🛒 Carrito</h2>

{% if carrito %}

<ul>

{% for item in carrito %}
<li>{{ item[0] }} - S/{{ item[1] }}</li>
{% endfor %}

</ul>

<h3>Total: S/{{ total }}</h3>

{% else %}

<p>No hay productos agregados.</p>

{% endif %}

</div>

</section>

<section id="dashboard">

<div class="dashboard">

<h2>📊 Dashboard</h2>

<div class="metricas">

<div class="metrica">
<div class="valor">{{ cantidad }}</div>
<div class="etiqueta">Productos en el carrito</div>
</div>

<div class="metrica">
<div class="valor">S/{{ total }}</div>
<div class="etiqueta">Total acumulado</div>
</div>

<div class="metrica">
<div class="valor">{{ ultimo if ultimo else "—" }}</div>
<div class="etiqueta">Último producto agregado</div>
</div>

<div class="metrica">
<div class="valor">{{ total_productos }}</div>
<div class="etiqueta">Productos en catálogo</div>
</div>

</div>

</div>

</section>

<section id="crud">

<div class="crud">

<h2>⚙️ Administración de Productos (CRUD)</h2>

<h3>➕ Crear producto</h3>

<form method="POST" class="crud-form">
<input type="text" name="nuevo_nombre" placeholder="Nombre del producto" required>
<input type="number" name="nuevo_precio" placeholder="Precio (S/)" min="1" required>
<button name="accion" value="crear">Crear</button>
</form>

<h3>✏️ Editar precio</h3>

<form method="POST" class="crud-form">
<input type="text" name="editar_nombre" placeholder="Nombre exacto del producto" required>
<input type="number" name="editar_precio" placeholder="Nuevo precio (S/)" min="1" required>
<button name="accion" value="editar">Actualizar</button>
</form>

<h3>📋 Productos registrados</h3>

<table class="tabla-productos">
<tr>
<th>Producto</th>
<th>Precio</th>
<th></th>
</tr>

{% for nombre, precio in productos.items() %}
<tr>
<td>{{ nombre }}</td>
<td>S/{{ precio }}</td>
<td>
<form method="POST" style="display:inline;">
<input type="hidden" name="nombre_producto" value="{{ nombre }}">
<button name="accion" value="eliminar" class="btn-eliminar">Eliminar</button>
</form>
</td>
</tr>
{% endfor %}

</table>

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
    global carrito, productos, mensaje

    mensaje = ""

    if request.method == "POST":
        accion = request.form.get("accion")

        if accion == "crear":
            nombre = request.form.get("nuevo_nombre", "").strip()
            precio_raw = request.form.get("nuevo_precio", "")

            if not nombre:
                mensaje = "⚠️ El nombre del producto no puede estar vacío."
            elif nombre in productos:
                mensaje = f"⚠️ El producto '{nombre}' ya existe."
            else:
                try:
                    precio = int(precio_raw)
                    if precio <= 0:
                        mensaje = "⚠️ El precio debe ser mayor a 0."
                    else:
                        productos[nombre] = precio
                        mensaje = f"✅ Producto '{nombre}' creado correctamente."
                except ValueError:
                    mensaje = "⚠️ El precio debe ser un número válido."

        elif accion == "editar":
            nombre = request.form.get("editar_nombre", "").strip()
            precio_raw = request.form.get("editar_precio", "")

            if nombre not in productos:
                mensaje = f"⚠️ El producto '{nombre}' no existe."
            else:
                try:
                    nuevo_precio = int(precio_raw)
                    if nuevo_precio <= 0:
                        mensaje = "⚠️ El precio debe ser mayor a 0."
                    else:
                        productos[nombre] = nuevo_precio
                        mensaje = f"✅ Precio de '{nombre}' actualizado a S/{nuevo_precio}."
                except ValueError:
                    mensaje = "⚠️ El precio debe ser un número válido."

        elif accion == "eliminar":
            nombre = request.form.get("nombre_producto", "")
            if nombre in productos:
                del productos[nombre]
                # Quitar del carrito también los items de ese producto eliminado
                carrito = [item for item in carrito if item[0] != nombre]
                mensaje = f"🗑️ Producto '{nombre}' eliminado."
            else:
                mensaje = f"⚠️ El producto '{nombre}' no existe."

        else:
            # Agregar producto al carrito
            nombre = request.form.get("producto", "")
            if nombre in productos:
                precio = productos[nombre]
                carrito.append((nombre, precio))
                mensaje = f"🛒 '{nombre}' agregado al carrito."
            else:
                mensaje = "⚠️ Ese producto ya no está disponible."

    total = sum(item[1] for item in carrito)
    ultimo = carrito[-1][0] if carrito else ""

    return render_template_string(
        HTML,
        cafes=cafes,
        postres=postres,
        sandwiches=sandwiches,
        carrito=carrito,
        total=total,
        cantidad=len(carrito),
        ultimo=ultimo,
        productos=productos,
        total_productos=len(productos),
        mensaje=mensaje,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
