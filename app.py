# import os
# from flask import Flask, render_template
# from routes import predictions, scheduling
# from dotenv import load_dotenv
#
# # Load environment variables
# load_dotenv()
# ROOT_PATH = os.getenv("ROOT_PATH")
# DB_PATH = os.path.join(ROOT_PATH, "database", "database2.db")
#
# # Explicitly set the template folder
# TEMPLATES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
# app = Flask(__name__, template_folder=TEMPLATES_PATH)
#
# app.config['SECRET_KEY'] = 'energy_optimization_secret_key'
# app.config['DB_PATH'] = DB_PATH
#
# # Register blueprints
# app.register_blueprint(predictions.bp)
# app.register_blueprint(scheduling.bp)
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
# if __name__ == '__main__':
#     app.run(debug=True)


# Updated app.py
from flask import Flask, render_template
from routes import predictions, scheduling
import os
from dotenv import load_dotenv
from models.database import init_app

# Load environment variables
load_dotenv()
ROOT_PATH = os.getenv("ROOT_PATH")
DB_PATH = os.path.join(ROOT_PATH, "database", "database2.db")


def create_app():
    # Explicitly set the template folder path
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TEMPLATES_PATH = os.path.join(BASE_DIR, 'templates')

    app = Flask(__name__, template_folder=TEMPLATES_PATH)
    app.config['SECRET_KEY'] = 'energy_optimization_secret_key'
    app.config['DB_PATH'] = DB_PATH

    # Initialize database connection
    init_app(app)

    # Register blueprints
    app.register_blueprint(predictions.bp)
    app.register_blueprint(scheduling.bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
