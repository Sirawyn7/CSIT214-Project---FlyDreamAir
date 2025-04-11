import pickle
import datetime
import customtkinter as ctk

"""
FlyDreamAir is a major airline which covers both international and domestic routes with a 
large fleet of aircrafts. The airline has a large network of travel agencies and customers 
across the world. FlyDream is planning to digitalize its business processes and operations, 
and has identified three potential projects:  

•   Project 1: develop an IT software system to manage customers and allow them 
    to book flights, manage flight reservations, seat selections, purchasing in-flight 
    services such as food and drinks. 
"""

#---------------------------------Data Classes---------------------------------

class Customer:
    def __init__(self, customerID, firstName, lastName, contactNumber, email, address):
        self.customerID = customerID
        self.firstName = firstName
        self.lastName = lastName
        self.contactNumber = contactNumber
        self.email = email
        self.address = address

    def list_customer_details(self, customer_id):

        customer_details_list = []

        customer_details_list.append(customer_list[customer_id].customerID)
        customer_details_list.append(customer_list[customer_id].firstName)
        customer_details_list.append(customer_list[customer_id].lastName)
        customer_details_list.append(customer_list[customer_id].contactNumber)
        customer_details_list.append(customer_list[customer_id].email)
        customer_details_list.append(customer_list[customer_id].address)

        return customer_details_list


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


#---------------------------------Window Classes---------------------------------

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FlyDreamAir")
        self.geometry("600x400")
        
        # Show initial screen
        self.show_login_screen()


    #Clears window to make way for new content
    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()


    def show_login_screen(self):
        self.clear_window()

        label = ctk.CTkLabel(self, text="Login Screen", font=("Helvetica", 20))
        label.pack(pady=20)

        label = ctk.CTkLabel(self, text="Do you have an existing account?", font=("Helvetica", 20))
        label.pack(pady=16)

        existing_account_button = ctk.CTkButton(self, text="Yes", command=self.show_account_login_screen)
        existing_account_button.pack(pady=10)

        new_account_button = ctk.CTkButton(self, text="No", command=self.show_create_account_screen)
        new_account_button.pack(pady=10)

    
    def show_account_login_screen(self):
        self.clear_window()

        label = ctk.CTkLabel(self, text="Login Screen", font=("Helvetica", 20))
        label.pack(pady=20)

        label = ctk.CTkLabel(self, text="Do you have an existing account?", font=("Helvetica", 20))
        label.pack(pady=16)

        self.user_entry = ctk.CTkEntry(self, width=300, placeholder_text="Type here...")
        self.user_entry.pack(pady=10, padx=10)

        attempt_login = ctk.CTkButton(self, text="Submit", command=self.attempt_login)
        attempt_login.pack(pady=10, padx=10)

    def attempt_login(self):

        user_input = int(self.user_entry.get())

        if user_input + 1 > len(customer_list):
            self.show_login_screen()
        else:
            self.show_home_screen()
    
    
    def show_create_account_screen(self):
        pass


    def show_home_screen(self):
        self.clear_window()
        
        label = ctk.CTkLabel(self, text="Home Screen", font=("Helvetica", 20))
        label.pack(pady=20)

        account_button = ctk.CTkButton(self, text="My Account", command=self.show_my_account)
        account_button.pack(pady=10)
        
        settings_button = ctk.CTkButton(self, text="Settings", command=self.show_settings_screen)
        settings_button.pack(pady=10)
        
        about_button = ctk.CTkButton(self, text="About", command=self.show_about_screen)
        about_button.pack(pady=10)


    def show_my_account(self):
        self.clear_window()

        label = ctk.CTkLabel(self, text="My Account", font=("Helvetica", 20))
        label.pack(pady=20)

        account_details = customer_list[customer_id].list_customer_details(customer_id)

        account_details_string = f"Customer ID: {account_details[0]}\nName: {account_details[1]} {account_details[2]}\nContact Number: {account_details[3]}\nEmail: {account_details[4]}\nAddress: {account_details[5]}"
    
        label = ctk.CTkLabel(self, text=account_details_string, justify="center")
        label.pack(pady=20, padx=20)

        update_account_button = ctk.CTkButton(self, text="Update Account Details", command=self.show_update_account_screen)
        update_account_button.pack(pady=10)

        home_button = ctk.CTkButton(self, text="Back to Home", command=self.show_home_screen)
        home_button.pack(pady=10)


    def show_update_account_screen(self):
        self.clear_window()
        
        label = ctk.CTkLabel(self, text="Please Confirm Your Details", font=("Helvetica", 20))
        label.pack(pady=20)
        
        home_button = ctk.CTkButton(self, text="Back to Home", command=self.show_home_screen)
        home_button.pack(pady=10)


    def show_settings_screen(self):
        self.clear_window()
        
        label = ctk.CTkLabel(self, text="Settings Screen", font=("Helvetica", 20))
        label.pack(pady=20)
        
        home_button = ctk.CTkButton(self, text="Back to Home", command=self.show_home_screen)
        home_button.pack(pady=10)
    

    def show_about_screen(self):
        self.clear_window()
        
        label = ctk.CTkLabel(self, text="About Screen", font=("Helvetica", 20))
        label.pack(pady=20)
        
        home_button = ctk.CTkButton(self, text="Back to Home", command=self.show_home_screen)
        home_button.pack(pady=10)


#---------------------------------Data Deserialisation---------------------------------


customer_list = []
customer_id = 0

#Read data from file
try:
    with open('customers.pkl', 'rb') as f:
        customer_list = pickle.load(f) # deserialize into object using load()
except:
    pass

#Sort customer list based on customerID
customer_list.sort(key=lambda x: x.customerID)
#---------------------------------Main---------------------------------

if __name__ == "__main__":

    #Create app window
    app = App()
    app.mainloop()

