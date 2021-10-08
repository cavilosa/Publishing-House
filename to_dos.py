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
"""