from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()



class Account(db.Model):
    __tablename__='account'
    username=db.Column(db.String,primary_key=True)
    password=db.Column(db.String)
    email=db.Column(db.String)