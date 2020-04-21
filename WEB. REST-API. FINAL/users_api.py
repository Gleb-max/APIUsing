from sqlalchemy.exc import StatementError
from flask import jsonify, Blueprint, make_response, abort, request
from data.users import User
from data import db_session


blueprint = Blueprint("users_api", __name__, template_folder="templates")


@blueprint.route("/api/users")
def get_users():
    session = db_session.create_session()
    users = session.query(User).all()
    return jsonify(
        {
            "users":
                [item.to_dict(only=(
                    "surname",
                    "name",
                    "age",
                    "position",
                    "speciality",
                    "address",
                    "email",
                    "city_from",
                )) for item in users]
        }
    )


@blueprint.route("/api/users", methods=["POST"])
def create_user():
    if not request.json:
        return jsonify({"error": "Empty request"})
    elif not all(key in request.json for key in
                 ["city_from", "surname", "name", "age", "email", "hashed_password"]):
        return jsonify({"error": "Bad request"})
    session = db_session.create_session()
    if session.query(User).filter(User.id == request.json.get("id", None)).first():
        return jsonify({"error": "Id already exists"})
    all_fields = {"city_from", "surname", "name", "age", "position", "speciality", "address", "email", "hashed_password"}
    kwargs = {field: request.json[field] for field in all_fields.intersection(set(request.json))}
    user = User(**kwargs)
    session.add(user)
    try:
        session.commit()
    except StatementError:
        return jsonify({"error": "Wrong arg format"})
    return jsonify({"success": "OK"})


@blueprint.route("/api/users/<int:user_id>")
def get_user_by_id(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        abort(404)
    return jsonify(
        {
            "user": user.to_dict(only=(
                "surname",
                "name",
                "age",
                "position",
                "speciality",
                "address",
                "email",
                "city_from",
            ))
        }
    )


@blueprint.route("/api/users/<int:user_id>", methods=["PUT"])
def edit_user_by_id(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        abort(404)
    all_fields = {"city_from", "surname", "name", "age", "position", "speciality", "address", "email", "hashed_password"}
    kwargs = {field: request.json[field] for field in all_fields.intersection(set(request.json))}
    for field, kwarg in kwargs.items():
        user.__setattr__(field, kwarg)
        try:
            session.commit()
        except StatementError:
            return jsonify({"error": "Wrong arg format"})
    return jsonify({"success": "OK"})


@blueprint.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404)
    session.delete(user)
    session.commit()
    return jsonify({"success": "OK"})


@blueprint.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)
