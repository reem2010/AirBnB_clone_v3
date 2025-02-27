#!/usr/bin/python3
"""return json"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states', strict_slashes=False)
def states():
    res_states = list(storage.all(State).values())
    res = []
    for i in res_states:
        res.append(i.to_dict())
    return jsonify(res)


@app_views.route('/states/<state_id>')
def state_id(state_id):
    res_states = list(storage.all(State).values())
    res = None
    for i in res_states:
        if i.id == state_id:
            res = i.to_dict()
    if res is None:
        abort(404)
    return jsonify(res)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def del_stat(state_id):
    res_states = list(storage.all(State).values())
    city = list(storage.all(City).values())
    res = None
    for i in res_states:
        if i.id == state_id:
            res = i
    if res is None:
        abort(404)
    storage.delete(res)
    for i in city:
        if i.state_id == state_id:
            storage.delete(i)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def post_states():
    if not request.json:
        abort(400, "Not a JSON")
    state = request.get_json()
    if "name" not in state:
        abort(400, "Missing name")
    res = State(state).to_dict()
    return jsonify(res), 201


@app_views.route('/states/<state_id>',  methods=['PUT'])
def put_states(state_id):
    res_states = list(storage.all(State).values())
    res = None
    for i in res_states:
        if i.id == state_id:
            res = i
    if res is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    state = request.get_json()
    for key, value in state.items():
        if key == "id" or key == "created_at":
            continue
        if key == "updated_at":
            continue
        setattr(res, key, value)
    storage.save()
    return jsonify(res.to_dict()), 200
