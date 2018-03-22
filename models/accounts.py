class Account():
    def __init__(self, account_number, firstname, lastname, gender, age, email, city, address, state, employer, balance):
        self.account_number = account_number
        self.firstname = firstname
        self.lastname = lastname
        self.gender  = gender
        self.age = age
        self.email = email
        self.city = city
        self.address = address
        self.state = state
        self.employer = employer
        self.balance = balance
    def tojson(self):
        return {'account_number': self.account_number, 'firstname' : self.firstname,
                'lastname' : self.lastname, 'gender' : self.gender, 'age' : self.age, 'email' : self.email,
                'city' : self.city, 'address' : self.address, 'state' : self.state, 'employer' : self.employer,
                'balance' : self.balance}
