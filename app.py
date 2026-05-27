# Importamos Flask
from flask import Flask, render_template

# Creamos la aplicación Flask
app = Flask(__name__)

# Creamos una ruta principal
@app.route("/")
def inicio():

    # Renderizamos index.html
    return render_template("index.html")

# Ejecutamos el servidor
if __name__ == "__main__":
    app.run(debug=True)