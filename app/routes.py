from flask import jsonify, current_app, request, Blueprint, make_response
from flask_sqlalchemy import SQLAlchemy
from app.models import User
from sqlalchemy.exc import IntegrityError
from app import db
import socket

bp = Blueprint('bp', __name__)

# Health check
@bp.route("/health")
def home():
    
    return make_response((jsonify({'status': 'healthy'}), 200, {'Content-Type': 'application/json', 'Host': socket.gethostname(), 'Version': current_app.config['APP_VERSION']}))

# Get all users
@bp.route("/user",methods=["GET"])
def get_users():
    users = db.session.query(User).all()
    
    return make_response((jsonify([user.to_dict() for user in users]), 200, {'Content-Type': 'application/json', 'Host': socket.gethostname(), 'Version': current_app.config['APP_VERSION']}))

# Get user by id
@bp.route('/user/<int:id>', methods=['GET'])
def get_user_by_id(id):
  # Fetch user by ID from the database
  
  user = db.session.query(User).filter(User.id == id).first()

  # Check if user exists
  if not user:
    return make_response((jsonify({"error": "User not found"}), 404, {'Content-Type': 'application/json', 'Host': socket.gethostname(), 'Version': current_app.config['APP_VERSION']}))

  # Return JSON response with user data
  return make_response((jsonify(user.to_dict()), 200, {'Content-Type': 'application/json', 'Host': socket.gethostname(), 'Version': current_app.config['APP_VERSION']}))


@bp.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    # Get user by ID
    user = db.session.query(User).filter_by(id=id).first()

    if not user:
        return make_response((jsonify({'error': 'User not found'}), 404, {'Content-Type': 'application/json', 'Host': socket.gethostname(), 'Version': current_app.config['APP_VERSION']}))

    # Get data from request (assuming JSON format)
    data = request.get_json()

    # Update user details (check for presence in request data)
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']

    # Commit changes to the database
    db.session.commit()
    return make_response((jsonify({'message': 'User updated successfully'}), 200, {'Content-Type': 'application/json', 'Host': socket.gethostname(), 'Version': current_app.config['APP_VERSION']}))

@bp.route('/user', methods=['POST'])
def create_user():
  # Get user data from request body
  
  data = request.get_json()  # Parse JSON data from request

  print(data)

  # Check for required fields (assuming name and email are required)
  if not data or not data.get('name') or not data.get('email'):
    return make_response((jsonify({'error': 'missing data.'}), 404, {'Content-Type': 'application/json', 'Host': socket.gethostname(), 'Version': current_app.config['APP_VERSION']}))

  # Create a new user object
  user = User(name=data['name'], email=data['email'])

  # Add user to the database session
  try:
    db.session.add(user)
    db.session.commit()
  except IntegrityError:
    # Handle potential duplicate email or other integrity errors
    return make_response((jsonify({'error': 'user creation failed.'}), 409, {'Content-Type': 'application/json', 'Host': socket.gethostname(), 'Version': current_app.config['APP_VERSION']}))

  # Convert user object to a dictionary
  user_data = user.to_dict()

  # Return JSON response with the created user data
  return make_response((jsonify({'message': 'user created successfully'}), 201, {'Content-Type': 'application/json', 'Host': socket.gethostname(), 'Version': current_app.config['APP_VERSION']}))

@bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
  # Get user by ID
  
  user = db.session.get(User, user_id)

  # Check if user exists
  if not user:
    return make_response((jsonify({'error': 'user not found.'}), 409, {'Content-Type': 'application/json', 'Host': socket.gethostname(), 'Version': current_app.config['APP_VERSION']}))

  # Delete the user
  try:
    db.session.delete(user)
    db.session.commit()
  except IntegrityError as e:
    return make_response((jsonify({"error": f"user deletion failed: {e}"}), 409, {'Content-Type': 'application/json', 'Host': socket.gethostname(), 'Version': current_app.config['APP_VERSION']}))

  # Return a success message (optional)
  return make_response((jsonify({'message': 'user deleted successfully'}), 200, {'Content-Type': 'application/json', 'Host': socket.gethostname(), 'Version': current_app.config['APP_VERSION']}))