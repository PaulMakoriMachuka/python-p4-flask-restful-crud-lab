from flask import Flask, request, jsonify
from flask_migrate import Migrate
from server.models import db, Plant

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    Migrate(app, db)

    @app.route("/plants/<int:id>", methods=["GET"])
    def get_plant(id):
        plant = Plant.query.get(id)
        if not plant:
            return {"error": "Plant not found"}, 404
        return jsonify(plant.to_dict()), 200

    @app.route("/plants/<int:id>", methods=["PATCH"])
    def update_plant(id):
        plant = Plant.query.get(id)
        if not plant:
            return {"error": "Plant not found"}, 404

        data = request.json
        if "is_in_stock" in data:
            plant.is_in_stock = data["is_in_stock"]
        db.session.commit()

        return jsonify(plant.to_dict()), 200

    @app.route("/plants/<int:id>", methods=["DELETE"])
    def delete_plant(id):
        plant = Plant.query.get(id)
        if not plant:
            return {"error": "Plant not found"}, 404

        db.session.delete(plant)
        db.session.commit()
        return {"message": "Plant deleted"}, 200

    return app

app = create_app()
