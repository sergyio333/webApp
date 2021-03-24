from flask import Blueprint, jsonify, request, session
from sqlalchemy import select, delete, join
from .models import cars, brands, models
from .methods import sqlExe, sqlAction, validateFields
from datetime import datetime

# cars Bluebrint (all the routes that are used for the cars model - they use the /api/car prefix)
carRoutes = Blueprint("cars", __name__, url_prefix='/api/car')

@carRoutes.route('/get', methods=["POST"])
def get_cars():
    query = select([cars.c.Id, cars.c.Title, cars.c.Brand_id, cars.c.Model_id, cars.c.DrivedDistance,
                    cars.c.Price, cars.c.Fuel, cars.c.DateCreated])

    get_multiple = True

    if request.get_json().get("id", False):
        id =  request.get_json()["id"]
        query = query.where(cars.c.Id == id)
        get_multiple = False

    elif request.get_json().get("titleFilter", False):
        search_text =  "".join(("%", request.get_json()["titleFilter"], "%"))
        query = query.where(cars.c.Title.like(search_text))
        #x = query.where(cars.c.Title.like(search_text))
        #y = query.where(cars.c.Fuel.like(search_text))
        #query = query.join(x, y)



    result = sqlExe(query, multiple=get_multiple)

    return jsonify(result)

@carRoutes.route('/create', methods=["POST"])
def create_car():
    data = request.get_json()

    if not validateFields(data, ["Title", "Brand_id", "Model_id", "DrivedDistance", "Price", "Fuel"]):
        return jsonify(success=False, message="Invalid form data")

    data = {
        "Title": data["Title"],
        "Brand_id": data["Brand_id"],
        "Model_id": data["Model_id"],
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

    if not validateFields(data, ["Id", "Title", "Brand_id", "Model_id", "DrivedDistance", "Price", "Fuel"]):
        return jsonify(success=False, message="Invalid form data")

    data = {
        "Title": data["Title"],
        "Brand_id": data["Brand_id"],
        "Model_id": data["Model_id"],
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

