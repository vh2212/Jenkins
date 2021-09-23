import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = os.path.abspath(os.path.dirname(__file__))

# crear la instancia de conexión de la aplicación
connex_app = connexion.App(__name__, specification_dir=basedir)

# obtener la instancia de la aplicación bajo el que corre flask
app = connex_app.app

# configurar la parte de SQLAlchemy de la instancia de la aplicación
sqlite_url = "sqlite:///" + os.path.join(basedir, "people.db")
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# crear la instancia de base de datos de SQLAlchemy
db = SQLAlchemy(app)

# inicializar Marshmallow
ma = Marshmallow(app)
