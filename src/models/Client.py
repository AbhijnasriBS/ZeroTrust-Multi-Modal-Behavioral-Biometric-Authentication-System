from common.database import Database
import datetime
import random


class Client(object):

    def __init__(self, _id, password, name, contact_number, gender, email, date_of_birth, account_number=None, date_of_joining=None, money=None, desc=None):
        self._id = _id
        self.password = password
        self.name = name
        self.contact_number = contact_number
        self.gender = gender
        self.date_of_joining = datetime.datetime.utcnow(
        ) if date_of_joining is None else date_of_joining
        self.date_of_birth = date_of_birth
        self.email = email
        self.account_number = random.randint(
            1000000000, 9999999999) if account_number is None else account_number
        self.money = 5000 if money is None else money
        self.desc = desc
        print(self._id, self.password, self.name, self.contact_number, self.gender, self.date_of_birth,
              self.date_of_joining, self.email, self.account_number, self.money, self.desc)

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
            'date_of_joining': self.date_of_joining,
            'date_of_birth': self.date_of_birth,
            'email': self.email,
            'account_number': self.account_number,
            'money': self.money,
            'desc': self.desc
        }

    @classmethod
    def from_id(cls, id):
        data = Database.find_one("Client", {"_id": id})
        if data is not None:
            print(data)
            return cls(**data)

    @classmethod
    def from_name(cls, name):
        data = Database.find_one("Client", {"name": name})
        if data is not None:
            print(data)
            return cls(**data)

    @classmethod
    def from_email(cls, email):
        data = Database.find_one("Client", {"email": email})
        if data is not None:
            print(data)
            x = cls(**data)
            print(x.name)
            return cls(**data)

    @classmethod
    def from_account(cls, account_no):
        data = Database.find_one("Client", {"account_number": int(account_no)})
        if data is not None:
            print(data)
            return cls(**data)

    @staticmethod
    def delete_client(query):
        Database.delete_one_record(collection="Client", query={"name": query})

    @classmethod
    def get_employees(cls):
        clients = Database.find_collection(collection='Client')
        return [cls(**clients) for clients in clients]

    @classmethod
    def all_clients(cls):
        clients = Database.find_collection('Client')
        return [cls(**client) for client in clients]

    @staticmethod
    def update_client_through_id(id, feild, document):
        query = {"_id": id}
        newvalues = {"$set": {feild: document}}
        Database.update('Client', query, newvalues)

    @staticmethod
    def transfer_fund(self_acc, rec_acc, rec_pho, amount, desc):
        from_acc = Client.from_account(self_acc)
        to_acc = Client.from_account(rec_acc)
#        if to_acc.contact_number==rec_pho:
        from_acc.money = from_acc.money-amount
        to_acc.money = to_acc.money+amount
        Client.update_client_through_id(to_acc._id, "money", to_acc.money)
        Client.update_client_through_id(from_acc._id, "money", from_acc.money)
        Client.update_client_through_id(to_acc._id, "desc", desc)
        return "The amount was successfully transferred! Thank you for your patience!"
#        else:
#            return "The receiver's phone number doesn't match"


# Database.initialize()
# clients=Client.all_clients()
# print(clients)

# employee = Employee('EMP1000','password','Vaibhav Bhandari',9945216957,'Male','29-APR-1999')
# employee.save_to_mongo()
