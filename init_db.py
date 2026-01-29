from app import app
from extensions import db

def init_database():
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")
        print(f"DB Location: {app.config['SQLALCHEMY_DATABASE_URI']}")

if __name__ == '__main__':
    print("Initializing Database...")
    init_database()