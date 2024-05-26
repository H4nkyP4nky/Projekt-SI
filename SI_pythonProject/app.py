from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()


class EmptyTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
