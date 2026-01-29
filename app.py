import os
from flask import Flask, make_response, request
from flask_mail import Mail
from flask_login import LoginManager
from dotenv import load_dotenv
from sqlalchemy import text

from extensions import db
from models import AdminUsers

from routes_admin import admin_bp
from routes_public import public_bp

load_dotenv()

app = Flask(__name__)

#--DB CONFIG
db_url = os.getenv('DATABASE_URL', 'sqlite:///whiztech.db')

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
}

#--MAIL CONFIG
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER_BR')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT_BR'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS_BR') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL_BR') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME_BR')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_SMTP_KEY_BR')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_SENDER_G')
app.config['SECRET_KEY'] = os.getenv('PK')

#--PLUGINS
mail = Mail(app)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin.login'

@login_manager.user_loader
def load_user(user_id):
    return AdminUsers.query.get(int(user_id))

app.register_blueprint(public_bp)
app.register_blueprint(admin_bp)

@app.route('/setup-device/<token>')
def setup_device(token):
    psst = os.getenv('DK')
    if token == psst:
        resp = make_response("Device Authorized. You may now access /admin/login")
        resp.set_cookie('whiztech_auth_token', psst, max_age=31536000, httponly=True, secure=True)
        return resp
    return "Invalid Token", 403

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False') == 'True'
    app.run(debug=debug_mode)