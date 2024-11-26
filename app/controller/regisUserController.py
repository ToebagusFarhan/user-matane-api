# regisUser.py
from flask import request, jsonify, render_template
from uuid import uuid4
from app.data.db import get_db
from app.data.models import User
from app.utils.apiauth import amIAllowed
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import bcrypt
from contextlib import contextmanager
import re

@contextmanager
def get_session():
    db: Session = next(get_db())
    try:
        yield db
    finally:
        db.close()

def regis():
    """
    Registers a new user in the database.
    This function handles the registration of a new user by receiving user data from a JSON request,
    hashing the provided password, and storing the user information in the database. It also performs
    basic validation to ensure that the username and email are provided.
    Returns:
        Response: A JSON response indicating the success or failure of the user registration process.
        - On success: Returns a JSON response with status "success", a message, and the new user's ID and username.
        - On failure: Returns a JSON response with status "fail" and an appropriate error message, along with an HTTP status code.
    """
    if not amIAllowed():
        return render_template("error/401.html"), 401
    data = request.get_json()
    uuid = str(uuid4())
    # Hash the client-provided password hash using bcrypt
    password_hashed = bcrypt.hashpw(data.get("password_hash").encode("utf-8"), bcrypt.gensalt())
    
    new_user = User(
        uuid=uuid,
        username=data.get("name"),
        email=data.get("email"),
        password_hash=password_hashed,
    )
    
    if not new_user.username:
        return jsonify(status="fail", message="User creation failed. Name is required"), 400
    
    if not new_user.email:
        return jsonify(status="fail", message="User creation failed. Email is required"), 400
    
    # Validate email format
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, new_user.email):
        return jsonify(status="fail", message="User creation failed. Invalid email format"), 400
    
    with get_session() as db:
        existing_user = db.query(User).filter(User.email == data.get("email")).first()
        if existing_user:
            return jsonify(status="fail", message="User creation failed. Email already exists"), 400
        
        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        except SQLAlchemyError as e:
            db.rollback()
            return jsonify(status="fail", message="User creation failed. Database error", error=str(e)), 500
    
    return jsonify(status="success", message="User added successfully", data={"userId": new_user.uuid, "username": new_user.username}), 201
