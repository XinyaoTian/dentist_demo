from flask import Flask
from config import Config

application = Flask(__name__)
application.config.from_object(Config)
if __name__ == '__main__':
    application.run(host='0.0.0.0',port=5000,debug=False)

from app import routes