import datetime

from carson import db


class Appointment(db.Model):
    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)

    repo = db.Column(db.Text)
    commit_sha = db.Column(db.String(40))
    pr_number = db.Column(db.Integer)
    gh_username = db.Column(db.Text)
    base_branch = db.Column(db.Text)

    conditions = db.Column(db.Enum("passed", "any_failed", name="conditions"))
    action = db.Column(db.Enum("merge", "notify_slack", name="actions"))
    processed = db.Column(db.DateTime)

    def __init__(self):
        self.timestamp = datetime.datetime.utcnow()
        self.processed = None

    def write(self):
        db.session.add(self)
        db.session.commit()
