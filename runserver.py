from backend.factory import create_app
from backend.config import Config
import os

if __name__ == '__main__':
        app = create_app(Config)
        app.run(port=5000, host="0.0.0.0", use_reloader=True)