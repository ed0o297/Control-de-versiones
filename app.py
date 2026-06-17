from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

productos = {
    "Espresso": 7,
    "Americano": 8,
    "Latte": 10,
    "Vainilla Latte": 12,
    "Matcha Latte": 14,
    "Iced Americano": 10,
    "Iced Latte": 12,
    "Iced Vainilla Latte": 14,
    "Iced Matcha Latte": 16,

    "Cheesecake Maracuyá": 10,
    "Cheesecake Oreo": 10,
    "Cheesecake Clásico": 10,
    "NY Cheesecake": 15,
    "Torta de Chocolate": 12,
    "Tiramisú": 12,
    "Tres Leches Chocolate": 9,
    "Tres Leches Vainilla": 9,
    "Carrot Cake": 11,

    "Mixto Simple": 12,
    "Mixto Especial": 16,
    "Charsiu": 18,
    "Club Sandwich": 20
}

carrito = []

HTML = """

<!DOCTYPE html>
<html lang="es">
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>Café Limeño</title>

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
padding:20px;
margin:30px;
border-radius:15px;
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
<h1>☕ Café Limeño</h1>
<p>Cafetería de Especialidad - Lima, Perú</p>
</header>

<nav>
<a href="#cafes">Cafés</a>
<a href="#postres">Postres</a>
<a href="#sandwiches">Sándwiches</a>
<a href="#carrito">Carrito</a>
<a href="#dashboard">Dashboard</a>
</nav>

<section class="hero">
<h1>Bienvenido a Café Limeño</h1>
<p>Sabores artesanales, cafés de especialidad y postres preparados diariamente.</p>
</section>

<section class="seccion" id="cafes">
<h2 class="titulo">☕ Cafés</h2>

<div class="contenedor">

{% for nombre, precio in cafes %}
<div class="card">
<h3>{{ nombre }}</h3>
<p>Café de especialidad preparado por nuestros baristas.</p>
<div class="precio">S/{{ precio }}</div>

<form method="POST">
<input type="hidden" name="producto" value="{{ nombre }}">
<button type="submit">Agregar al carrito</button>
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
<input type="hidden" name="producto" value="{{ nombre }}">
<button type="submit">Agregar al carrito</button>
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
<input type="hidden" name="producto" value="{{ nombre }}">
<button type="submit">Agregar al carrito</button>
</form>

</div>
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

<p><strong>Productos agregados:</strong> {{ cantidad }}</p>

<p><strong>Total acumulado:</strong> S/{{ total }}</p>

{% if ultimo %}
<p><strong>Último producto agregado:</strong> {{ ultimo }}</p>
{% endif %}

</div>

</section>

<!-- PEGAR AQUÍ EL CRUD -->

<section class="dashboard">

<h2>⚙️ CRUD Productos</h2>

<h3>Crear Producto</h3>

<form method="POST">

<input type="text"
name="nuevo_nombre"
placeholder="Nombre del producto"
required>

<input type="number"
name="nuevo_precio"
placeholder="Precio"
required>

<button name="accion" value="crear">
Crear Producto
</button>

</form>

<br>

<h3>Editar Precio</h3>

<form method="POST">

<input type="text"
name="editar_nombre"
placeholder="Nombre exacto del producto"
required>

<input type="number"
name="editar_precio"
placeholder="Nuevo precio"
required>

<button name="accion" value="editar">
Actualizar Precio
</button>

</form>

<br>

<h3>Productos Registrados</h3>

<ul>

{% for nombre, precio in productos.items() %}

<li>

{{ nombre }} - S/{{ precio }}

<form method="POST" style="display:inline;">

<input type="hidden"
name="nombre_producto"
value="{{ nombre }}">

<button name="accion" value="eliminar">
Eliminar
</button>

</form>

</li>

{% endfor %}

</ul>

</section>


<footer>
<p>© 2026 Café Limeño - Proyecto Flask</p>
</footer>

</body>
</html>

"""

@app.route("/", methods=["GET", "POST"])
def inicio():

    global carrito

    if request.method == "POST":

    accion = request.form.get("accion")

    if accion == "crear":

        nombre = request.form["nuevo_nombre"]

        precio = int(request.form["nuevo_precio"])

        productos[nombre] = precio

    elif accion == "editar":

        nombre = request.form["editar_nombre"]

        nuevo_precio = int(request.form["editar_precio"])

        if nombre in productos:
            productos[nombre] = nuevo_precio

    elif accion == "eliminar":

        nombre = request.form["nombre_producto"]

        if nombre in productos:
            del productos[nombre]

    else:

        nombre = request.form["producto"]

        precio = productos[nombre]

        carrito.append((nombre, precio))

    total = sum(item[1] for item in carrito)

    cafes = [
        ("Espresso",7),
        ("Americano",8),
        ("Latte",10),
        ("Vainilla Latte",12),
        ("Matcha Latte",14),
        ("Iced Americano",10),
        ("Iced Latte",12),
        ("Iced Vainilla Latte",14),
        ("Iced Matcha Latte",16)
    ]

    postres = [
        ("Cheesecake Maracuyá",10),
        ("Cheesecake Oreo",10),
        ("Cheesecake Clásico",10),
        ("NY Cheesecake",15),
        ("Torta de Chocolate",12),
        ("Tiramisú",12),
        ("Tres Leches Chocolate",9),
        ("Tres Leches Vainilla",9),
        ("Carrot Cake",11)
    ]

    sandwiches = [
        ("Mixto Simple",12),
        ("Mixto Especial",16),
        ("Charsiu",18),
        ("Club Sandwich",20)
    ]

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
    productos=productos
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)