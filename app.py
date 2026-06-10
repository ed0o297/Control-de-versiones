from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Café Limeño</title>

<style>

body{
font-family:Arial,sans-serif;
margin:0;
background:#f5f5f5;
}

header{
background:#4b2e2e;
color:white;
padding:30px;
text-align:center;
}

section{
padding:20px;
max-width:1000px;
margin:auto;
}

.card{
background:white;
padding:15px;
margin:10px 0;
border-radius:10px;
box-shadow:0 0 10px rgba(0,0,0,.1);
}

form{
background:white;
padding:20px;
border-radius:10px;
}

input{
width:100%;
padding:10px;
margin-bottom:10px;
}

button{
background:#6f4e37;
color:white;
border:none;
padding:12px;
cursor:pointer;
width:100%;
}

.mensaje{
background:#d4edda;
padding:10px;
margin-bottom:15px;
border-radius:5px;
}

</style>
</head>

<body>

<header>
<h1>☕ Café Limeño</h1>
<p>Cafetería de especialidad - Lima, Perú</p>
</header>

<section>

<h2>☕ Cafés de Especialidad</h2>

<div class="card">
<h3>Flat White</h3>
<p>Espresso doble con leche texturizada. Suave y equilibrado.</p>
</div>

<div class="card">
<h3>Cappuccino</h3>
<p>Espresso, leche vaporizada y espuma cremosa.</p>
</div>

<div class="card">
<h3>V60 Peruano</h3>
<p>Café filtrado de granos de Cajamarca con notas frutales.</p>
</div>

<h2>🥪 Sándwiches</h2>

<div class="card">
<h3>Sándwich de Pollo</h3>
<p>Pollo deshilachado, lechuga fresca y mayonesa artesanal.</p>
</div>

<div class="card">
<h3>Sándwich Caprese</h3>
<p>Mozzarella, tomate y pesto.</p>
</div>

<h2>🍰 Postres</h2>

<div class="card">
<h3>Torta de Chocolate</h3>
<p>Bizcocho húmedo con ganache de chocolate.</p>
</div>

<div class="card">
<h3>Cheesecake de Maracuyá</h3>
<p>Cheesecake artesanal con cobertura de maracuyá.</p>
</div>

<h2>📝 Registro de Pedido</h2>

{% if mensaje %}
<div class="mensaje">
{{ mensaje }}
</div>
{% endif %}

<form method="POST">

<input type="text"
name="cliente"
placeholder="Nombre del cliente"
required>

<input type="text"
name="producto"
placeholder="Producto solicitado"
required>

<button type="submit">
Guardar Pedido
</button>

</form>

</section>

</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def inicio():

    mensaje = ""

    if request.method == "POST":

        cliente = request.form["cliente"]
        producto = request.form["producto"]

        with open("pedidos.txt","a",encoding="utf-8") as archivo:
            archivo.write(f"{cliente},{producto}\\n")

        mensaje = "Pedido registrado correctamente."

    return render_template_string(
        HTML,
        mensaje=mensaje
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)