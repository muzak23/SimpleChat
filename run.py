#!/bin/env python
from simplechat import create_app, socketio

app = create_app()

if __name__ == '__main__':
    app.debug = True
    socketio.run(app)
