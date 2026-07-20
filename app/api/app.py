"""Tasks API — the backend tier of the capstone.

A deliberately small Flask + SQLAlchemy service: the point of this
project is the infrastructure around it (Kubernetes, Terraform, CI/CD,
monitoring), not the app itself. It talks to Postgres in-cluster via
DATABASE_URL and falls back to SQLite so it runs anywhere with zero
setup (local dev, CI).
"""

import os

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, nullable=False, default=False)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "done": self.done}


def create_app(database_url: str | None = None) -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url or os.environ.get(
        "DATABASE_URL", "sqlite:///local.db"
    )
    db.init_app(app)
    with app.app_context():
        db.create_all()

    @app.get("/healthz")
    def healthz():
        # Liveness only — no DB round-trip, so a slow database doesn't
        # get the pod restarted.
        return jsonify(status="ok")

    @app.get("/readyz")
    def readyz():
        # Readiness includes the DB: if Postgres is unreachable, drop
        # out of the Service endpoints instead of serving 500s.
        try:
            db.session.execute(text("SELECT 1"))
        except Exception:
            return jsonify(status="degraded"), 503
        return jsonify(status="ready")

    @app.get("/api/tasks")
    def list_tasks():
        tasks = Task.query.order_by(Task.id).all()
        return jsonify([t.to_dict() for t in tasks])

    @app.post("/api/tasks")
    def create_task():
        payload = request.get_json(silent=True) or {}
        title = str(payload.get("title", "")).strip()
        if not title:
            return jsonify(error="title is required"), 400
        task = Task(title=title, done=bool(payload.get("done", False)))
        db.session.add(task)
        db.session.commit()
        return jsonify(task.to_dict()), 201

    return app
