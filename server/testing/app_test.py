import json
import pytest
from app import app, db
from server.models import Plant

class TestPlant:
    def setup_method(self):
        """Run before every test."""
        with app.app_context():
            # Reset the database
            db.drop_all()
            db.create_all()

            # Seed with a plant
            plant = Plant(
                name="Live Oak",
                image="https://www.nwf.org/-/media/NEW-WEBSITE/Shared-Folder/Wildlife/Plants-and-Fungi/plant_southern-live-oak_600x300.ashx",
                price=250.00,
                is_in_stock=True
            )
            db.session.add(plant)
            db.session.commit()

    def test_plant_by_id_get_route(self):
        '''has a resource available at "/plants/<int:id>".'''
        response = app.test_client().get('/plants/1')
        assert response.status_code == 200

    def test_plant_by_id_get_route_returns_one_plant(self):
        '''returns JSON representing one Plant object at "/plants/<int:id>".'''
        response = app.test_client().get('/plants/1')
        data = json.loads(response.data.decode())

        assert type(data) == dict
        assert data["id"] == 1
        assert data["name"] == "Live Oak"

    def test_plant_by_id_patch_route_updates_is_in_stock(self):
        '''returns JSON representing updated Plant object with "is_in_stock" = False at "/plants/<int:id>".'''
        response = app.test_client().patch(
            '/plants/1',
            json={"is_in_stock": False}
        )
        data = json.loads(response.data.decode())

        assert response.status_code == 200
        assert data["is_in_stock"] is False

    def test_plant_by_id_delete_route_deletes_plant(self):
        '''deletes the Plant object at "/plants/<int:id>".'''
        response = app.test_client().delete('/plants/1')
        assert response.status_code == 200

        # check it's gone
        with app.app_context():
            plant = Plant.query.filter_by(id=1).first()
            assert plant is None
