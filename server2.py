from flask import render_template
import config

# obtener la instancia de la aplicación
connex_app = config.connex_app

# leer el archivo swagger.yml para configurar los endpoints
connex_app.add_api('swagger.yml')

# crear una ruta de url dentro de la aplicación para root
@connex_app.route('/')
def home():
    """
    Ésta función responde en el navegado con la url:
    localhost:5000

    :return:    con la plantilla renderizada home.html
    """
    return render_template('home.html')

# si se está ejecutando en modo standalone, entonces ejecutar la aplicación
if __name__ == '__main__':
    connex_app.run(host='0.0.0.0', port=5000, debug=True)
