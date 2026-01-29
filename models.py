from datetime import datetime, timezone
from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

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
    
class SecurityLog(db.Model):
    __tablename__ = 'security_logs'

    id = db.Column(db.Integer, primary_key=True)
    risk_lvl = db.Column(db.String(25))
    result = db.Column(db.String(25))
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(255))
    endpoint = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    details = db.Column(db.String(255))

    def __repr__(self):
        return f'<SecurityLog {self.ip_address}'
    
class AdminUsers(UserMixin, db.Model):
    __tablename__ = 'admin_users'

    id = db.Column(db.Integer, primary_key=True)
    admin_username = db.Column(db.String(64), unique=True, nullable=False)
    admin_password_hash = db.Column(db.String(256))
    
    def set_password(self, password):
        self.admin_password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.admin_password_hash, password)
