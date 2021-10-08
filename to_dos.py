import unittest
class Test(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        .........
    @classmethod
    def tearDownClass(self):
        ..........

"""
OOPs : Object-Oriented Programming
Since these three methods insert, update, delete have the same definition in every model class then what you can do is you can make a class inheritedClassName which can be inherited in other classes and so you can use the same code.

This will also make your code reusable and will increase code readability as well!

For Example:

'''
Extend the base Model class to add common methods
'''
class inheritedClassName(db.Model):
    __abstract__ = True

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

'''
Vehicle
'''
@dataclass
class Vehicle(inheritedClassName):
    id: int
    license_plate: String
    model: String
    make: String

    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True)
    license_plate = Column(String, unique=True)
    model = Column(String)
    make = Column(String)
    seats = Column(Integer)
This Vehicle(inheritedClassName) syntax tells that you are inheriting the class inheritedClassName in the class Vehicle.


You can group methods from the same module like so:

from flask import (
  Flask,
  request,
  flash,
  redirect,
  render_template,
  ....,
  other_packages_name ,
  url_for,
  flash
)

app.py line 336:
To see what error is being thrown, you may use:

print(sys.exc_info())
For debugging purposes you can use sys.exc_info().You can refer more here

Flash messages could also be useful here if you have a frontend to show.

You can also try using logging to get the best debugging results. I suggest you to please go through the Module-Level Functions here to broaden your knowledge.


SUGGESTION
You can make use of flask-blueprint to properly separating your endpoints. Like - You can arrange endpoints related to actors in one file and endpoints related to movies in another file!


SUGGESTION
You should document the endpoint by use of multiline docstring!
Check the best practices on Python Multiline docstring


"""