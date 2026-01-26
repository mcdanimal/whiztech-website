from datetime import datetime, timezone
from extensions import db

class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'

    id = db.Column(db.Integer, primary_key=True)
    customer_lname = db.Column(db.String(50), nullable=False)
    customer_fname = db.Column(db.String(50), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    service_type = db.Column(db.String(50))
    details = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Request {self.id}>'