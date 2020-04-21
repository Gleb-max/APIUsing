from sqlalchemy.exc import StatementError
from flask import jsonify, Blueprint, make_response, abort, request
from data.jobs import Job
from data import db_session


blueprint = Blueprint("jobs_api", __name__, template_folder="templates")


@blueprint.route("/api/jobs")
def get_jobs():
    session = db_session.create_session()
    jobs = session.query(Job).all()
    return jsonify(
        {
            "jobs":
                [item.to_dict(only=(
                    "team_leader",
                    "job",
                    "work_size",
                    "collaborators",
                    "start_date",
                    "end_date",
                    "is_finished"
                )) for item in jobs]
        }
    )


@blueprint.route("/api/jobs", methods=["POST"])
def create_job():
    if not request.json:
        return jsonify({"error": "Empty request"})
    elif not all(key in request.json for key in
                 ["team_leader", "job", "work_size"]):
        return jsonify({"error": "Bad request"})
    session = db_session.create_session()
    if session.query(Job).filter(Job.id == request.json.get("id", None)).first():
        return jsonify({"error": "Id already exists"})
    all_fields = {"id", "team_leader", "job", "work_size", "collaborators", "start_date", "end_date", "is_finished"}
    kwargs = {field: request.json[field] for field in all_fields.intersection(set(request.json))}
    job = Job(**kwargs)
    session.add(job)
    try:
        session.commit()
    except StatementError:
        return jsonify({"error": "Wrong arg format"})
    return jsonify({"success": "OK"})


@blueprint.route("/api/jobs/<int:job_id>")
def get_job_by_id(job_id):
    session = db_session.create_session()
    job = session.query(Job).filter(Job.id == job_id).first()
    if not job:
        abort(404)
    return jsonify(
        {
            "job": job.to_dict(only=(
                "team_leader",
                "job",
                "work_size",
                "collaborators",
                "start_date",
                "end_date",
                "is_finished"
            ))
        }
    )


@blueprint.route("/api/jobs/<int:job_id>", methods=["PUT"])
def edit_job_by_id(job_id):
    session = db_session.create_session()
    job = session.query(Job).filter(Job.id == job_id).first()
    if not job:
        abort(404)
    all_fields = {"id", "team_leader", "job", "work_size", "collaborators", "start_date", "end_date", "is_finished"}
    kwargs = {field: request.json[field] for field in all_fields.intersection(set(request.json))}
    for field, kwarg in kwargs.items():
        job.__setattr__(field, kwarg)
        try:
            session.commit()
        except StatementError:
            return jsonify({"error": "Wrong arg format"})
    return jsonify({"success": "OK"})


@blueprint.route("/api/jobs/<int:job_id>", methods=["DELETE"])
def delete_job(job_id):
    session = db_session.create_session()
    job = session.query(Job).get(job_id)
    if not job:
        abort(404)
    session.delete(job)
    session.commit()
    return jsonify({"success": "OK"})


@blueprint.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)
