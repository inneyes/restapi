from flask import Flask, request,jsonify
import json

app = Flask(__name__)

countries = [
    {"id":'1',"name":"Thailand","capital":"Bangkok"},
    {"id":'2',"name":"Korea","capital":"Seoul"},
    {"id":'3',"name":"USA","capital":"LA"},
]

def _find_next_id(id: int):
    return next((x for x in countries if x['id'] == id), None)

#GET
@app.route('/country', methods=['GET'])
def get_country():
    return jsonify(countries)

#GET by id
@app.route('/country/<id>', methods=['GET'])
def get_country_id(id):
    data = _find_next_id(id)
    return jsonify(data)


#POST
@app.route('/country', methods=['POST'])
def post_country():
    id = request.form.get('id')
    name = request.form.get('name')
    capital = request.form.get('capital')

    new_data = {
        "id": id,
        "name": name,
        "capital": capital
    }

    if (_find_next_id(id)):
        return {"error": 'Bad Request'}, id
    else:
        countries.append(new_data)
        return jsonify(countries)


#PUT
@app.route('/country/<id>', methods=['PUT'])
def put_country(id):
    global countries
    name = request.form.get('name')
    capital = request.form.get('capital')

    update_data = {
        "name": name,
        "capital": capital
    }

    for country in countries:
        if id == country.get("id"):
            country["name"] = str(name)
            country['capital'] = str(capital)
            return jsonify(countries)
        else:
            return "error", 404


#PATCH
@app.route('/country/<id>', methods=["PATCH"])
def patch_country(id: int):
    country = _find_next_id(id)
    if country is None:
        return jsonify({'error':'Country not found!'}),404

    updated_country = json.loads(request.data)
    country.update(updated_country)
    return jsonify(countries)




#DELETE
@app.route('/country/<id>', methods = ['DELETE'])
def delete_country(id):

    data = _find_next_id(id)
    if not data:
        return {"error": "Country not found"}, 404
    else:
        countries.remove(data[0]) 
        return "Country deleted succuessfully" ,200

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
