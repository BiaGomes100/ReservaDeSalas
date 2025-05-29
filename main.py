import os
from flask import Flask
from app.db import db
from app.Models import reserva

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from app.db import db
db.init_app(app)

from app.Models.reserva import routes
app.register_blueprint(routes)

with app.app_context():
    from app.db import db
db.create_all()

if __name__ == "__main__":
    app.run(port=5001, debug=True)
