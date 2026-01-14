from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Parent(db.Model):
  __tablename__ = "parents"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)

  # Relationship with backref
  children = db.relationship("Child", backref="parent") 

class Child(db.Model):
  __tablename__ = "children"
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)

  # Foreign Key
  parent_id = db.Column(db.Integer, db.ForeignKey("parents.id"))
  

nicole = Parent(name = "Nicole")

a = Parent(name='Maria') 
b = Child(name='Wallace')
print(a)
print(b)
a.Child = b
b.Parent = a
print(a.Child)
print(b.Parent)