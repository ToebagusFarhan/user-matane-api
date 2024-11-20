from flask import request, jsonify
from data.db import get_db
from data.models import User
from utils.apiauth import amIAllowed
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import bcrypt
from contextlib import contextmanager

@contextmanager
def get_session():
    db: Session = next(get_db())
    try:
        yield db
    finally:
        db.close()

def login():
    """
    Handle user login request.
    This function processes a login request by extracting the email and hashed password
    from the request JSON payload. It validates the presence of these fields, checks if
    the user exists in the database, and verifies the provided password hash against the
    stored hash using bcrypt.
    Returns:
        Response: A JSON response with the following possible outcomes:
            - 400: If the email or password is not provided.
            - 404: If the user with the provided email does not exist.
            - 401: If the provided password is incorrect.
            - 200: If the login is successful, including user details (excluding sensitive data).
            - 500: If there is a database error.
    Raises:
        SQLAlchemyError: If there is an error querying the database.
    """
    
    # Check if the user is allowed to login
    if not amIAllowed():
        return jsonify(status="fail", message="Unauthorized access"), 403
    
    data = request.get_json()
    
    # Extract the email and hashed password from the request
    email = data.get("email")
    password_hash = data.get("password_hash")  # Assume this is the client-provided hash

    # Validation: Check if email and password are provided
    if not email:
        return jsonify(status="fail", message="Email is required"), 400
    if not password_hash:
        return jsonify(status="fail", message="Password is required"), 400
    
    try:
        with get_session() as db:
            # Check if a user with the provided email exists
            user = db.query(User).filter(User.email == email).first()
            
            if not user:
                return jsonify(status="fail", message="User not found"), 404

            # Verify bcrypt hash of client-provided password
            if not bcrypt.checkpw(password_hash.encode('utf-8'), user.password_hash.encode('utf-8')):
                return jsonify(status="fail", message="Incorrect password"), 401

            # Return success with user details (excluding sensitive data like password)
            return jsonify(status="success", message="Login successful", data={
                "profilelink": user.userprofile_link,
                "useruuid": user.uuid,
                "username": user.username,
                "email": user.email,
                "age": user.age,
                "gender": user.gender,
                "address": user.address
            }), 200

    except SQLAlchemyError as e:
        return jsonify(status="fail", message="Database error", error=str(e)), 500
