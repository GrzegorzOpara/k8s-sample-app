from flask import Flask

# Import other modules from your project
from app import create_app
import os

app = create_app(config='default')  # Call the create_app function from app.__init__.py

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
