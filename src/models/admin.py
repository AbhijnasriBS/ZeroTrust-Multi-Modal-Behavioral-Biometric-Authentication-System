import uuid
import datetime
from common.database import Database
import random


class Admin(object):

    def __init__(self, _id, password, name, contact_number, gender, email, date_of_birth):
        self._id = _id
        self.password = password
        self.name = name
        self.contact_number = contact_number
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.email = email

    def save_to_mongo(self):
        Database.insert(collection='Client',
                        data=self.json())

    def json(self):
        return {
            '_id': self._id,
            'name': self.name,
            'password': self.password,
            'contact_number': self.contact_number,
            'gender': self.gender,
            'date_of_birth': self.date_of_birth,
            'email': self.email,
        }

    @classmethod
    def from_id(cls, name):
        data = Database.find_one("Admin", {"name": name})
        if data is not None:
            print(data)
            return cls(**data)

    @staticmethod
    def delete_admin(query):
        Database.delete_one_record(collection="Admin", query={"name": query})

    @classmethod
    def get_employees(cls):
        clients = Database.find_collection(collection='Admin')
        return [cls(**clients) for clients in clients]

    @classmethod
    def all_admins(cls):
        clients = Database.find_collection('Admin')
        return [cls(**client) for client in clients]


Database.initialize()
clients = Admin.all_admins()
print(clients)

# employee = Employee('EMP1000','password','Vaibhav Bhandari',9945216957,'Male','29-APR-1999')
# employee.save_to_mongo()
