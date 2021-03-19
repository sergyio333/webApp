from flask import Blueprint, jsonify, request
from sqlalchemy import select, delete
from .models import cars
from .methods import sqlExe, sqlAction, validateFields
from datetime import datetime

# cars Bluebrint (all the routes that are used for the cars model - they use the /api/car prefix)
carRoutes = Blueprint("cars", __name__, url_prefix='/api/car')

@carRoutes.route('/get', methods=["POST"])
def get_cars():
    query = select([cars.c.Id, cars.c.Title, cars.c.Brand, cars.c.Model, cars.c.DrivedDistance,
                    cars.c.Price, cars.c.Fuel, cars.c.DateCreated])
    get_multiple = True

    if request.get_json().get("id", False):
        id =  request.get_json()["id"]
        query = query.where(cars.c.Id == id)
        get_multiple = False

    elif request.get_json().get("titleFilter", False):
        search_text =  "".join(("%", request.get_json()["titleFilter"], "%"))
        query = query.where(cars.c.Title.like(search_text))

    result = sqlExe(query, multiple=get_multiple)

    return jsonify(result)

@carRoutes.route('/create', methods=["POST"])
def create_car():
    data = request.get_json()

    if not validateFields(data, ["Title", "Brand", "Model", "DrivedDistance", "Price", "Fuel"]):
        return jsonify(success=False, message="Invalid form data")

    data = {
        "Title": data["Title"],
        "Brand": data["Brand"],
        "Model": data["Model"],
        "DrivedDistance": data["DrivedDistance"],
        "Price": data["Price"],
        "Fuel": data["Fuel"],
        "DateCreated": datetime.utcnow()
    }
    
    query = cars.insert().values(data)
    result = sqlAction(query)

    return jsonify(success=True)

@carRoutes.route('/modify/<id>', methods=["POST"])
def modify_car(id):
    data = request.get_json()

    if not validateFields(data, ["Id", "Title", "Brand", "Model", "DrivedDistance", "Price", "Fuel"]):
        return jsonify(success=False, message="Invalid form data")

    data = {
        "Title": data["Title"],
        "Brand": data["Brand"],
        "Model": data["Model"],
        "DrivedDistance": data["DrivedDistance"],
        "Price": data["Price"],
        "Fuel": data["Fuel"]
    }
    query = cars.update().values(data).where(cars.c.Id==id)
    result = sqlAction(query)

    return jsonify(success=True)

@carRoutes.route('/delete/<id>', methods=["POST"])
def delete_car(id):
    
    query = delete(cars).where(cars.c.Id == id)
    result = sqlAction(query)

    return jsonify(success=True)

