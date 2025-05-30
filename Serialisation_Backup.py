
import pickle
import datetime

class Customer:
    def __init__(self, customerID, firstName, lastName, contactNumber, email, address, bookings):
        self.customerID = customerID
        self.firstName = firstName
        self.lastName = lastName
        self.contactNumber = contactNumber
        self.email = email
        self.address = address
        self.bookings = bookings

c1 = Customer(0, "Test", "Customer", "0412345678", "Test@gmail.com", "123 Test lane NSW", [])

customers = [c1]

with open('customers.pkl', 'wb') as f:  # open a text file
    pickle.dump(customers, f) # serialize the list
    f.close()


class InFlightService:
    def __init__(self, serviceID, name, description, price):
        self.serviceID = serviceID
        self.name = name
        self.description = description
        self.price = price

f1 = InFlightService(0, "Pretzels", "Food", 5)
f2 = InFlightService(1, "Mixed Nuts", "Food", 5)
f3 = InFlightService(2, "Salad", "Food", 10)
f4 = InFlightService(3, "Cheese and Crackers", "Food", 6)

d1 = InFlightService(4, "Coffee", "Drink", 4)
d2 = InFlightService(5, "Tea", "Drink", 4)
d3 = InFlightService(6, "Hot Chocolate", "Drink", 4)
d4 = InFlightService(7, "Soft Drinks", "Drink", 4)
d5 = InFlightService(8, "Juice", "Drink", 3)
d6 = InFlightService(9, "Water", "Drink", 1)

services = [f1,f2,f3,f4,d1,d2,d3,d4,d5,d6]

with open('services.pkl', 'wb') as f:  # open a text file
    pickle.dump(services, f) # serialize the list
    f.close()


class Flight:
    def __init__(self, flightID, flightNumber, departureAirport, arrivalAirport, departureTime, arrivalTime, price, status, bookedSeats):
        self.flightID = flightID
        self.flightNumber = flightNumber
        self.departureAirport = departureAirport
        self.arrivalAirport = arrivalAirport
        self.departureTime = departureTime
        self.arrivalTime = arrivalTime
        self.price = price
        self.status = status
        self.bookedSeats = bookedSeats


fl1 = Flight("FL001", "AA1234", "JFK", "LAX", datetime.datetime(2025, 6, 15, 8, 30), datetime.datetime(2025, 6, 15, 11, 45), 450, "On Time", ["A5", "B12", "D7", "F19", "G3", "H28", "I14", "J21"])
fl2 = Flight("FL002", "DL5678", "ATL", "MIA", datetime.datetime(2025, 6, 15, 14, 15), datetime.datetime(2025, 6, 15, 16, 30), 220, "On Time", ["A2", "B18", "C9", "D25", "E6", "F31", "G13", "H4", "I22", "J16", "A29", "C11", "E24"])
fl3 = Flight("FL003", "UA9012", "ORD", "SFO", datetime.datetime(2025, 6, 16, 7, 0), datetime.datetime(2025, 6, 16, 9, 20), 380, "On Time", ["B8", "D15", "F2", "H30", "J7"])
fl4 = Flight("FL004", "SW3456", "DEN", "PHX", datetime.datetime(2025, 6, 16, 12, 45), datetime.datetime(2025, 6, 16, 14, 10), 180, "On Time", ["A17", "C4", "E26", "G10", "I1", "J32", "B23", "D19", "F14", "H6"])
fl5 = Flight("FL005", "JB7890", "BOS", "SEA", datetime.datetime(2025, 6, 17, 9, 15), datetime.datetime(2025, 6, 17, 12, 30), 320, "On Time", ["A11", "B27", "D3", "F20", "G8", "H15", "I25", "J12", "C18"])
fl6 = Flight("FL006", "NK2345", "LAS", "DFW", datetime.datetime(2025, 6, 17, 16, 20), datetime.datetime(2025, 6, 17, 19, 45), 150, "On Time", ["E9", "G24", "I5"])
fl7 = Flight("FL007", "AS6789", "PDX", "ANC", datetime.datetime(2025, 6, 18, 11, 0), datetime.datetime(2025, 6, 18, 15, 30), 280, "On Time", ["A26", "B1", "C13", "D30", "E17", "F4", "G21", "H9", "I28", "J6", "A20", "B15"])
fl8 = Flight("FL008", "F91011", "MCO", "BWI", datetime.datetime(2025, 6, 18, 13, 30), datetime.datetime(2025, 6, 18, 15, 50), 200, "On Time", ["A8", "B22", "C16", "D5", "E29", "F11", "G2", "H25", "I19", "J14", "A32", "B7", "C24", "D18", "E3", "F27", "G12"])
fl9 = Flight("FL009", "B61213", "LGA", "FLL", datetime.datetime(2025, 6, 19, 6, 45), datetime.datetime(2025, 6, 19, 9, 35), 250, "On Time", ["A1", "A23", "B10", "B31", "C6", "C17", "D2", "D28", "E13", "E21", "F8", "F26", "G5", "G18", "H11", "H29", "I4", "I16", "J9", "J22", "A15", "B4", "C25", "D12"])
fl10 = Flight("FL010", "WN1415", "MDW", "HOU", datetime.datetime(2025, 6, 19, 15, 10), datetime.datetime(2025, 6, 19, 17, 25), 140, "On Time", ["A14", "B6", "C21", "D16", "E1", "F23", "G7", "H32", "I18", "J5", "A27", "C3", "E19", "G28", "I9"])

flights = [fl1, fl2, fl3, fl4, fl5, fl6, fl7, fl8, fl9, fl10]

with open('flights.pkl', 'wb') as f:  # open a text file
    pickle.dump(flights, f) # serialize the list
    f.close()