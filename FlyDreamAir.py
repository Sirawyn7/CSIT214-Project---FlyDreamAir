import pickle
import datetime

"""
FlyDreamAir is a major airline which covers both international and domestic routes with a 
large fleet of aircrafts. The airline has a large network of travel agencies and customers 
across the world. FlyDream is planning to digitalize its business processes and operations, 
and has identified three potential projects:  

•   Project 1: develop an IT software system to manage customers and allow them 
    to book flights, manage flight reservations, seat selections, purchasing in-flight 
    services such as food and drinks. 
"""

#To sort a list of objects based on the attributes:
# orig_list.sort(key=lambda x: x.attribute_name)
#---------------------------------Classes---------------------------------

class Customer:
    def __init__(self, customerID, firstName, lastName, contactNumber, email, address):
        self.customerID = customerID
        self.firstName = firstName
        self.lastName = lastName
        self.contactNumber = contactNumber
        self.email = email
        self.address = address

    #Method to list customer details
    def list_customer_details(self, customer_id):
        print(f"Account number: {customer_list[customer_id].customerID}")
        print(f"Name: {customer_list[customer_id].firstName} {customer_list[customer_id].lastName}")
        print(f"Contact Number: {customer_list[customer_id].contactNumber}")
        print(f"Email: {customer_list[customer_id].email}")
        print(f"Address: {customer_list[customer_id].address}")
        print()

class Booking:
    def __init__(self, bookingID, bookingDate, status, totalPrice, seatNumber):
        self.bookingID = bookingID
        self.bookingDate = bookingDate
        self.status = status
        self.totalPrice = totalPrice
        self.seatNumber = seatNumber

class Flight:
    def __init__(self, flightID, flightNumber, departureAirport, arrivalAirport, departureTime, arrivalTime, status, availableSeats):
        self.flightID = flightID
        self.flightNumber = flightNumber
        self.departureAirport = departureAirport
        self.arrivalAirport = arrivalAirport
        self.departureTime = departureTime
        self.arrivalTime = arrivalTime
        self.status = status
        self.availableSeats = availableSeats

class InFlightService:
    def __init__(self, serviceID, name, description, price, availableOnRoute):
        self.serviceID = serviceID
        self.name = name
        self.description = description
        self.price = price
        self.availableOnRoute = availableOnRoute

class Seat:
    def __init__(self, seatNumber, seatClass, price, isAvailable):
        self.seatNumber = seatNumber
        self.seatClass = seatClass
        self.price = price
        self.isAvailable = isAvailable

class Payment:
    def __init__(self, paymentID, amount, paymentDate, paymentMethod, status):
        self.paymentID = paymentID
        self.amount = amount
        self.paymentDate = paymentDate
        self.paymentMethod = paymentMethod
        self.status = status

#---------------------------------Data Deserialisation---------------------------------


customer_list = []

#Read data from file
try:
    with open('customers.pkl', 'rb') as f:
        customer_list = pickle.load(f) # deserialize into object using load()
except:
    pass

#---------------------------------Main---------------------------------

if __name__ == "__main__":

    new_customer = "Yes"

    while True:
        #Default to customer creation if no customers on file
        if len(customer_list) > 0: 
            new_customer = input("Are you a new customer? yes/no ").title()

        #Create new customer
        if new_customer == "Yes":
            customer_id = len(customer_list)
            fname = input("What is your first name? ")
            lname = input("What is your last name? ")
            cnum = int(input("What is your contact number? "))
            email = input("What is your email? ")
            addr = input("What is your address? ")
            cust = Customer(customer_id, fname, lname, cnum, email, addr)

            customer_list.append(cust)
            customer_list.sort(key=lambda x: x.customerID)
            print("Account succesfully created")
            print(f"Your account ID is {customer_id}")
            print()
            break

        #Confirm customer account number
        elif new_customer == "No":
            while True:
                customer_id = int(input("Please enter your account number: "))
                if customer_id + 1 > len(customer_list):
                    print("This account does not exist")
                else:
                    break
                break
            break

        #Invalid input handling
        else:
            print("Invalid option")

    #Loop to display menu
    while True:
        print()
        print("Menu")
        print("1. My Account")
        print("2. Bookings")
        print("3. Upcoming Flights")
        print("4. Quit")
        user_choice = int(input("Enter Choice: "))
        print()

        #My Account
        if user_choice == 1:
            print("Your account details are:")
            customer_list[customer_id].list_customer_details(customer_id)

            print("Menu")
            print("1. Update account details")
            print("2. Return to main menu")
            user_choice = int(input("Enter Choice: "))
            print()

        #Bookings
        if user_choice == 2:
            pass

        #Upcoming Flights
        if user_choice == 3:
            pass

        #Quit
        if user_choice == 4:

            #---------------------------------Data Serialisation---------------------------------

            #Sort list based on object attributes
            customer_list.sort(key=lambda x: x.customerID)

            #Write customer list to file
            with open('customers.pkl', 'wb') as f:
                pickle.dump(customer_list, f)
                f.close()
            break