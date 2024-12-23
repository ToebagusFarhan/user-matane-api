# routes.py
from flask import Blueprint
from app.controller.userController import update_user_by_uuid, get_user_by_uuid, get_all_users, delete_user_by_uuid, delete_user_all, add_personal_data_by_uuid, update_userProfile_by_uuid, get_user_image_by_uuid
from app.controller.regisUserController import regis
from app.controller.loginUserController import login


user_routes = Blueprint('user_routes', __name__)

# Get all users
user_routes.route('/users', methods=['GET'])(get_all_users)
# Update user by uuid
user_routes.route('/user/<string:user_uuid>', methods=['PUT'])(update_user_by_uuid)
# Update user personal data by uuid
user_routes.route('/user/personal/<string:user_uuid>', methods=['PUT'])(add_personal_data_by_uuid)
# Get user by uuid
user_routes.route('/user/<string:user_uuid>', methods=['GET'])(get_user_by_uuid)
# Delete user by uuid
user_routes.route('/user/<string:user_uuid>', methods=['DELETE'])(delete_user_by_uuid)

# Upload user profile picture
user_routes.route('/user/profile/<string:user_uuid>', methods=['POST'])(update_userProfile_by_uuid)
# Get user profile picture
user_routes.route('/user/profile/<string:user_uuid>', methods=['GET'])(get_user_image_by_uuid)


# Register user
user_routes.route('/regis', methods=['POST','GET'])(regis)
# Login user
user_routes.route('/login', methods=['POST', 'GET'])(login)
# Delete all users(Admin Only)
user_routes.route('/admin/users/delete', methods=['DELETE'])(delete_user_all)

