#!/usr/bin/env python3
import sys
sys.path.append("../")
from flaskr import create_app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0')
