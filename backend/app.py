from app_instance import app
from db_instance import db

with app.app_context():
    import models
    db.create_all()
    models.User.create_if_no_admin()

import routes

