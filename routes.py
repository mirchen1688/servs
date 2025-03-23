from flask import Blueprint, request, jsonify
from .models import db, User, App
from flask import request, jsonify, abort

main = Blueprint('main', __name__)


@main.route('/download_app', methods=['POST'])
def download_app():
    if not request.headers.get('Authorization'):
        abort(401)  # Unauthorized

    user_id = request.headers.get('Authorization')
    app_id = request.json.get('app_id')

    # 检查用户是否有权限下载应用
    user = User.query.get(user_id)
    if not user or not user.has_enough_points(app_id):
        abort(403)  # Forbidden

    # 允许下载应用
    return jsonify({"message": "App downloaded successfully"})

@main.route('/add_app', methods=['POST'])
def add_app():
    data = request.json
    new_app = App(
        name=data['name'],
        description=data.get('description', ''),
        download_url=data['download_url'],
        points_required=data['points_required'],
        icon_path=data.get('icon_path', ''),
        screenshot_path=data.get('screenshot_path', '')
    )
    db.session.add(new_app)
    db.session.commit()
    return jsonify({"message": "App added successfully"}), 201

@main.route('/apps', methods=['GET'])
def get_apps():
    apps = App.query.all()
    return jsonify([{
        "id": app.id,
        "name": app.name,
        "description": app.description,
        "download_url": app.download_url,
        "points_required": app.points_required,
        "icon_path": app.icon_path,
        "screenshot_path": app.screenshot_path
    } for app in apps])

@main.route('/delete_app/<int:app_id>', methods=['DELETE'])
def delete_app(app_id):
    app = App.query.get_or_404(app_id)
    db.session.delete(app)
    db.session.commit()
    return jsonify({"message": "App deleted successfully"}), 200