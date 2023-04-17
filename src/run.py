#!/bin/env python
from simplechat import create_app, socketio

app = create_app()

app.debug = True

if __name__ == '__main__':
    socketio.run(app)
