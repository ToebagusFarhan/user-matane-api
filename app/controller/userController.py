from flask import request, jsonify
from app.data.db import get_db
from app.data.storage import upload_blob_to_folder, generate_presigned_url_for_profile
from app.data.models import User
from app.utils.apiauth import amIAllowed
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
import tempfile
import os


# Context manager to get a database session
@contextmanager
def get_session():
    db: Session = next(get_db())
    try:
        yield db
    finally:
        db.close()

def get_all_users():
    if not amIAllowed():
        return jsonify(status="fail", message="Unauthorized"), 403

    with get_session() as db:
        users = db.query(User).all()
        response_users = [{"uuid": user.uuid, "name": user.username, "email": user.email} for user in users]
        return jsonify(status="success", data={"users": response_users}), 200

def get_user_by_uuid(user_uuid):
    if not amIAllowed():
        return jsonify(status="fail", message="Unauthorized"), 403

    with get_session() as db:
        user = db.query(User).filter(User.uuid == user_uuid).first()
        if user:
            return jsonify(status="success", data={"user": {"id": user.uuid, "name": user.username, "email": user.email}}), 200
        return jsonify(status="fail", message="User not found"), 404

def add_personal_data_by_uuid(user_uuid):
    if not amIAllowed():
        return jsonify(status="fail", message="Unauthorized"), 403

    with get_session() as db:
        data = request.get_json()
        user = db.query(User).filter(User.uuid == user_uuid).first()

        if not user:
            return jsonify(status="fail", message="User not found"), 404

        user.age = data.get("age")
        user.gender = data.get("gender")
        user.address = data.get("address")
        try:
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            return jsonify(status="fail", message="User personal data update failed", error=str(e)), 500

        return jsonify(status="success", message="User personal data updated successfully", data={"userId": user.uuid, "user age": user.age, "user gender": user.gender, "user address": user.address}), 200

def update_userProfile_by_uuid(user_uuid):
    if not amIAllowed():
        return jsonify(status="fail", message="Unauthorized"), 403

    # Check if the user exists in the database
    with get_session() as db:
        user = db.query(User).filter(User.uuid == user_uuid).first()
        if not user:
            return jsonify(status="fail", message="User not found"), 404

    # Check if an image is provided in the request
    if 'image' not in request.files:
        return jsonify(status="fail", message="No image file found in request"), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify(status="fail", message="No file selected for upload"), 400

    # Use user_uuid as the filename, preserving the file extension
    file_extension = os.path.splitext(image_file.filename)[1]
    filename = f"{user_uuid}{file_extension}"

    try:
        # Use tempfile to create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            temp_path = temp_file.name
            image_file.save(temp_path)

        # Upload to Cloud Storage
        destination_folder_name = "userProfile"
        upload_blob_to_folder(temp_path, destination_folder_name, filename)

        # Generate a presigned URL
        presigned_url = generate_presigned_url_for_profile(filename)

        # Clean up the temporary file
        os.remove(temp_path)

        return jsonify(status="success", message="Image uploaded successfully", url=presigned_url), 201
    except Exception as e:
        return jsonify(status="fail", message=f"An error occurred: {str(e)}"), 500
    
    
def update_user_by_uuid(user_uuid):
    if not amIAllowed():
        return jsonify(status="fail", message="Unauthorized"), 403

    with get_session() as db:
        data = request.get_json()
        user = db.query(User).filter(User.uuid == user_uuid).first()

        if not user:
            return jsonify(status="fail", message="User update failed. User ID not found"), 404
        if not data.get("name"):
            return jsonify(status="fail", message="User update failed. Name is required"), 400

        user.username = data.get("name")
        user.email = data.get("email")
        try:
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            return jsonify(status="fail", message="User update failed", error=str(e)), 500

        return jsonify(status="success", message="User updated successfully", data={"userId": user.uuid, "name": user.username}), 200

def delete_user_by_uuid(user_uuid):
    if not amIAllowed():
        return jsonify(status="fail", message="Unauthorized"), 403

    with get_session() as db:
        user = db.query(User).filter(User.uuid == user_uuid).first()

        if not user:
            return jsonify(status="fail", message="User deletion failed. User ID not found"), 404

        try:
            db.delete(user)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            return jsonify(status="fail", message="User deletion failed", error=str(e)), 500

        return jsonify(status="success", message="User deleted successfully"), 200

def delete_user_all():
    if not amIAllowed():
        return jsonify(status="fail", message="Unauthorized"), 403

    data = request.get_json()
    if data.get("secret_key") != "iwakpeyek":
        return jsonify(status="fail", message="User deletion failed. You Don't have access"), 403
    with get_session() as db:
        db.query(User).delete()
        db.commit()
    return jsonify(status="success", message="All users deleted successfully"), 200
