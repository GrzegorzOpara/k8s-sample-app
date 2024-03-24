from flask import Flask, jsonify, request

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.exc import IntegrityError

import socket
import os

from dotenv import load_dotenv


# Env varibales
load_dotenv()

app = Flask(__name__)

# SQLAlchemy
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("POSTGRES_CONN_STRING")
db.init_app(app)

# Model
class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }

with app.app_context():
    db.create_all()

hostname = {"Message": f"app up and running successfully on {socket.gethostname()}"}

# Health check
@app.route("/health")
def home():
    return jsonify(hostname)

# Get all users
@app.route("/user",methods=["GET"])
def get_users():
    users = db.session.query(User).all()
    return jsonify(hostname, [user.to_dict() for user in users]), 200

# Get user by id
@app.route('/user/<int:id>', methods=['GET'])
def get_user_by_id(id):
  # Fetch user by ID from the database
  user = db.session.query(User).filter(User.id == id).first()

  # Check if user exists
  if not user:
    return jsonify(hostname, {"error": "User not found"}), 404

  # Return JSON response with user data
  return jsonify(hostname, user.to_dict()), 200

@app.route('/user', methods=['POST'])
def create_user():
  # Get user data from request body
  data = request.get_json()  # Parse JSON data from request

  print(data)

  # Check for required fields (assuming name and email are required)
  if not data or not data.get('name') or not data.get('email'):
    return jsonify(hostname, {"error": "Missing required fields"}), 400  # Bad request

  # Create a new user object
  user = User(name=data['name'], email=data['email'])

  # Add user to the database session
  try:
    db.session.add(user)
    db.session.commit()
  except IntegrityError:
    # Handle potential duplicate email or other integrity errors
    return jsonify(hostname, {"error": "User creation failed"}), 409  # Conflict

  # Convert user object to a dictionary
  user_data = user.to_dict()

  # Return JSON response with the created user data
  return jsonify(hostname, user_data), 201  # Created status code

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
  # Get user by ID
  user = db.session.query(User).get(user_id)

  # Check if user exists
  if not user:
    return jsonify(hostname ,{"error": "User not found"}), 404  # Not Found

  # Delete the user
  try:
    db.session.delete(user)
    db.session.commit()
  except IntegrityError as e:
    return jsonify(hostname, {"error": f"User deletion failed: {e}"}), 409  # Conflict

  # Return a success message (optional)
  return jsonify(hostname, {"message": "User deleted successfully"}), 204  # No Content



if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=8080) 