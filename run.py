#!/bin/env python
from simplechat import create_app, socketio

app = create_app()

app.debug = True

socketio.run(app)
