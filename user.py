from flask_sqlalchemy import SQLAlchemy




class User:
    def __init__(self, app):
        self.db=SQLAlchemy(app)
    
    id=self.db.Column(db.Integer, primary_key=True)
    name=self.db.Column(db.String(50))
    username=self.db.Column(db.String(50))
    email=self.db.Column(db.String(20))
    password=self.db.Column(db.String(20))


    def __repr__(self):
        return(f'{self.name} | {self.username} | {self.email}')