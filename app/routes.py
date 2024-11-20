# routes.py
from flask import Blueprint
from app.controller.userController import update_user_by_uuid, get_user_by_uuid, get_all_users, delete_user_by_uuid, delete_user_all, add_personal_data_by_uuid
from app.controller.regisUserController import regis
from app.controller.loginUserController import login


user_routes = Blueprint('user_routes', __name__)

# Get all users
user_routes.route('/users', methods=['GET'])(get_all_users)
# Update user by uuid
user_routes.route('/users/<string:user_uuid>', methods=['PUT'])(update_user_by_uuid)
# Update user personal data by uuid
user_routes.route('/user/personal/<string:user_uuid>', methods=['PUT'])(add_personal_data_by_uuid)
# Get user by uuid
user_routes.route('/users/<string:user_uuid>', methods=['GET'])(get_user_by_uuid)
# Delete user by uuid
user_routes.route('/users/<string:user_uuid>', methods=['DELETE'])(delete_user_by_uuid)

# Register user
user_routes.route('/regis', methods=['POST'])(regis)
# Login user
user_routes.route('/login', methods=['POST'])(login)
# Delete all users(Admin Only)
user_routes.route('/admin/users/delete', methods=['DELETE'])(delete_user_all)

