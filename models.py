from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    points = db.Column(db.Integer, default=0)

class App(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    download_url = db.Column(db.String(200), nullable=False)
    points_required = db.Column(db.Integer, nullable=False)
    icon_path = db.Column(db.String(200), nullable=True)  # 应用图标路径
    screenshot_path = db.Column(db.String(200), nullable=True)  # 应用截图路径