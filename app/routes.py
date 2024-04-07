from flask import Flask, jsonify, current_app, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
from app.models import User
from sqlalchemy.exc import IntegrityError
from app import db
import socket

bp = Blueprint('api', __name__)
meta = {"Message": f"app up and running successfully on {socket.gethostname()}. App version: {current_app.config['APP_VERSION']}"}
# Health check

@bp.route("/health")
def home():
    return jsonify(meta)

# Get all users
@bp.route("/user",methods=["GET"])
def get_users():
    users = db.session.query(User).all()
    return jsonify(meta, [user.to_dict() for user in users]), 200

# Get user by id
@bp.route('/user/<int:id>', methods=['GET'])
def get_user_by_id(id):
  # Fetch user by ID from the database
  user = db.session.query(User).filter(User.id == id).first()

  # Check if user exists
  if not user:
    return jsonify(meta, {"error": "User not found"}), 404

  # Return JSON response with user data
  return jsonify(meta, user.to_dict()), 200


@bp.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    # Get user by ID
    user = db.session.query(User).filter_by(id=id).first()

    if not user:
        return jsonify(meta, {'message': 'User not found'}), 404

    # Get data from request (assuming JSON format)
    data = request.get_json()

    # Update user details (check for presence in request data)
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']

    # Commit changes to the database
    db.session.commit()

    return jsonify(meta, {'message': 'User updated successfully'}), 200

@bp.route('/user', methods=['POST'])
def create_user():
  # Get user data from request body
  data = request.get_json()  # Parse JSON data from request

  print(data)

  # Check for required fields (assuming name and email are required)
  if not data or not data.get('name') or not data.get('email'):
    return jsonify(meta, {"error": "Missing required fields"}), 400  # Bad request

  # Create a new user object
  user = User(name=data['name'], email=data['email'])

  # Add user to the database session
  try:
    db.session.add(user)
    db.session.commit()
  except IntegrityError:
    # Handle potential duplicate email or other integrity errors
    return jsonify(meta, {"error": "User creation failed"}), 409  # Conflict

  # Convert user object to a dictionary
  user_data = user.to_dict()

  # Return JSON response with the created user data
  return jsonify(meta, user_data), 201  # Created status code

@bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
  # Get user by ID
  user = db.session.query(User).get(user_id)

  # Check if user exists
  if not user:
    return jsonify(meta ,{"error": "User not found"}), 404  # Not Found

  # Delete the user
  try:
    db.session.delete(user)
    db.session.commit()
  except IntegrityError as e:
    return jsonify(meta, {"error": f"User deletion failed: {e}"}), 409  # Conflict

  # Return a success message (optional)
  return jsonify(meta, {"message": "User deleted successfully"}), 204  # No Content