from datetime import datetime
from extensions import db

class Task(db.Model):
    __tablename__ = "tasks"

    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_datetime = db.Column(db.DateTime)
    creation_datetime = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(
        db.Enum("To Do", "In-Progress", "Done", "Cancelled", name="task_status"),
        default="To Do"
    )
    priority = db.Column(
        db.Enum("Low", "Medium", "High", "Critical", name="task_priority"),
        default="Medium"
    )
    assigned_to = db.Column(db.String(100), db.ForeignKey("users.id"))
    assigned_by = db.Column(db.String(100), db.ForeignKey("users.id"))

    # Relationships for easier access
    assignee = db.relationship("User", foreign_keys=[assigned_to], backref="assigned_tasks")
    assigner = db.relationship("User", foreign_keys=[assigned_by], backref="created_tasks")
