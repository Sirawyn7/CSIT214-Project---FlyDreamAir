import pickle
import datetime
import customtkinter as ctk
from customtkinter import CTkImage
import os
from PIL import Image, ImageTk
import random

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
        self.geometry("1050x630")
        self.frames = {}
        for F in (MainPage, SeatSelectionPage, ManageFlightsPage, InFlightServicesPage, MyAccountPage, ContactUsPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame("MainPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
#---------------------------------Page Classes---------------------------------

class MainPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        # Load and display background image
        image_path = "assets/plane.jpg"
        pil_image = Image.open(image_path)
        pil_image = pil_image.resize((1050, 630))  # resize to desired size

        self.bg_image = CTkImage(light_image=pil_image, dark_image=pil_image, size=(1050, 630))

        bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.controller = controller

        navbar = ctk.CTkFrame(self, height=50, fg_color="#ffffff")
        navbar.pack(fill="x")

        ctk.CTkLabel(navbar, text="FlyDreamAir", font=("Helvetica", 20)).pack(side="left", padx=20)

        for label in ["Book Flights", "Manage Flight Reservations", "In Flight Services", "My Account", "Contact Us"]:
            btn = ctk.CTkButton(navbar, text=label)
            if label == "Book Flights":
                btn.configure(command=lambda: controller.show_frame("SeatSelectionPage"))
            if label == "Manage Flight Reservations":
                btn.configure(command=lambda: controller.show_frame("ManageFlightsPage"))
            if label == "In Flight Services":
                btn.configure(command=lambda: controller.show_frame("InFlightServicesPage"))
            if label == "My Account":
                btn.configure(command=lambda: controller.show_frame("MyAccountPage"))
            if label == "Contact Us":
                btn.configure(command=lambda: controller.show_frame("ContactUsPage"))
            btn.pack(side="left", padx=15, pady=5)

        #Search bar
        search_wrapper = ctk.CTkFrame(self, fg_color="#ffffff", bg_color="#0f2f80", corner_radius=50)
        search_wrapper.pack(pady=40, padx=20)

        input_frame = ctk.CTkFrame(search_wrapper, fg_color="#ffffff", corner_radius=0)
        input_frame.grid(row=0, column=0, sticky="w", padx=(20, 10), pady=10)

        self.from_entry = self.create_styled_entry(input_frame, "From:")
        self.to_entry = self.create_styled_entry(input_frame, "To:")
        self.when_entry = self.create_styled_entry(input_frame, "When:")

        search_btn = ctk.CTkButton(search_wrapper, text="Search Flights", fg_color="#7B42F6", text_color="white", font=("Helvetica", 14, "bold"), corner_radius=20)
        search_btn.grid(row=0, column=1, sticky="e", padx=(10, 20), pady=10)

        # Configure grid columns for proper spacing
        search_wrapper.grid_columnconfigure(0, weight=1)
        search_wrapper.grid_columnconfigure(1, weight=0)

    def create_styled_entry(self, parent, label):
        frame = ctk.CTkFrame(parent, fg_color="#E5E5E5", corner_radius=20)
        frame.grid(row=0, column=len(parent.winfo_children()), padx=15, pady=10)
        ctk.CTkLabel(frame, text=label, font=("Helvetica", 14, "bold")).pack(side="left", padx=10, pady=3)
        entry = ctk.CTkEntry(frame, width=120)
        entry.pack(side="left", padx=10)
        return entry


class FlightBookingPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        # Load and display background image
        image_path = "assets/plane.jpg"
        pil_image = Image.open(image_path)
        pil_image = pil_image.resize((1050, 630))  # resize to desired size

        self.bg_image = CTkImage(light_image=pil_image, dark_image=pil_image, size=(1050, 630))

        bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.controller = controller

        navbar = ctk.CTkFrame(self, height=50, fg_color="#ffffff")
        navbar.pack(fill="x")

        ctk.CTkLabel(navbar, text="FlyDreamAir", font=("Helvetica", 20)).pack(side="left", padx=20)
        ctk.CTkLabel(navbar, text="Flight Booking", font=("Helvetica", 18)).place(relx=0.5, rely=0.5, anchor="center")

        seat_frame = ctk.CTkFrame(self)
        seat_frame.pack(padx=20, pady=10)

        back_btn = ctk.CTkButton(self, text="Back", command=lambda: controller.show_frame("MainPage"))
        back_btn.pack(pady=20)


class ManageFlightsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        # Load and display background image
        image_path = "assets/plane.jpg"
        pil_image = Image.open(image_path)
        pil_image = pil_image.resize((1050, 630))  # resize to desired size

        self.bg_image = CTkImage(light_image=pil_image, dark_image=pil_image, size=(1050, 630))

        bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.controller = controller

        navbar = ctk.CTkFrame(self, height=50, fg_color="#ffffff")
        navbar.pack(fill="x")

        ctk.CTkLabel(navbar, text="FlyDreamAir", font=("Helvetica", 20)).pack(side="left", padx=20)
        ctk.CTkLabel(navbar, text="Manage Flights", font=("Helvetica", 18)).place(relx=0.5, rely=0.5, anchor="center")

        seat_frame = ctk.CTkFrame(self)
        seat_frame.pack(padx=20, pady=10)

        back_btn = ctk.CTkButton(self, text="Back", command=lambda: controller.show_frame("MainPage"))
        back_btn.pack(pady=20)


class SeatSelectionPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#83c1fc")
        
        self.controller = controller

        navbar = ctk.CTkFrame(self, height=50, fg_color="#ffffff")
        navbar.pack(fill="x")

        ctk.CTkLabel(navbar, text="FlyDreamAir", font=("Helvetica", 20)).pack(side="left", padx=20)
        ctk.CTkLabel(navbar, text="Seat Selection", font=("Helvetica", 18)).place(relx=0.5, rely=0.5, anchor="center")

        seat_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        seat_frame.pack(padx=20, pady=10)

        self.seats = {}
        cols = 32
        cols_labels = ['A','B','C','D','E','F','G','H','J']

        unavailable_seats = set(random.sample([f"{r+1}{c}" for r in range(cols) for c in cols_labels], k=int(cols*len(cols_labels)*0.15)))

        for r in range(cols):
            #Add column labels above
            col_label = ctk.CTkLabel(seat_frame, text=str(r+1), font=("Helvetica", 12, "bold"))
            col_label.grid(row=0, column=r+1, padx=3, pady=(3, 8))

        # Add row labels (letters) on the left and seat buttons
        for c_idx, c in enumerate(cols_labels):
            # Add extra padding for row spacing
            extra_pady = 0
            if c_idx == 2:
                extra_pady = 15
            elif c_idx == 5:
                extra_pady = 15
            
            # Add row label on the left
            row_label = ctk.CTkLabel(seat_frame, text=c, font=("Helvetica", 12, "bold"))
            row_label.grid(row=c_idx+1, column=0, padx=(3, 8), pady=(3, 3 + extra_pady))
            
            # Add seat buttons
            for r in range(cols):
                seat_id = f"{r+1}{c}"
                btn = ctk.CTkButton(seat_frame, text="", width=25, height=25, corner_radius=5)
                
                btn.grid(row=c_idx+1, column=r+1, padx=3, pady=(3, 3 + extra_pady))

                if seat_id in unavailable_seats:
                    btn.configure(fg_color="red", hover_color="#ff4d4d", state="disabled")
                else:
                    btn.configure(fg_color="gray", hover_color="#b3b3b3")
                    btn.configure(command=lambda s=seat_id: self.toggle_seat(s))
                self.seats[seat_id] = btn

        back_btn = ctk.CTkButton(self, text="Back", command=lambda: controller.show_frame("MainPage"))
        back_btn.pack(pady=20)

        self.selected_seats = set()

    def toggle_seat(self, seat_id):
        btn = self.seats[seat_id]
        if seat_id in self.selected_seats:
            btn.configure(fg_color="gray")
            self.selected_seats.remove(seat_id)
        else:
            btn.configure(fg_color="blue")
            self.selected_seats.add(seat_id)


class InFlightServicesPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        # Load and display background image
        image_path = "assets/plane.jpg"
        pil_image = Image.open(image_path)
        pil_image = pil_image.resize((1050, 630))  # resize to desired size

        self.bg_image = CTkImage(light_image=pil_image, dark_image=pil_image, size=(1050, 630))

        bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.controller = controller

        navbar = ctk.CTkFrame(self, height=50, fg_color="#ffffff")
        navbar.pack(fill="x")

        ctk.CTkLabel(navbar, text="FlyDreamAir", font=("Helvetica", 20)).pack(side="left", padx=20)
        ctk.CTkLabel(navbar, text="In Flight Services", font=("Helvetica", 18)).place(relx=0.5, rely=0.5, anchor="center")

        seat_frame = ctk.CTkFrame(self)
        seat_frame.pack(padx=20, pady=10)

        back_btn = ctk.CTkButton(self, text="Back", command=lambda: controller.show_frame("MainPage"))
        back_btn.pack(pady=20)


class MyAccountPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        # Load and display background image
        image_path = "assets/plane.jpg"
        pil_image = Image.open(image_path)
        pil_image = pil_image.resize((1050, 630))  # resize to desired size

        self.bg_image = CTkImage(light_image=pil_image, dark_image=pil_image, size=(1050, 630))

        bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.controller = controller

        navbar = ctk.CTkFrame(self, height=50, fg_color="#ffffff")
        navbar.pack(fill="x")

        ctk.CTkLabel(navbar, text="FlyDreamAir", font=("Helvetica", 20)).pack(side="left", padx=20)
        ctk.CTkLabel(navbar, text="My Account", font=("Helvetica", 18)).place(relx=0.5, rely=0.5, anchor="center")

        account_frame = ctk.CTkFrame(self, fg_color="#ffffff")

        labels = ["Customer ID:", "Name:", "Contact Number:", "Email:", "Address:"]
        values = customer_list[0].list_customer_details(0)
        adjusted_values = []
        #Combine first and last names into 1 value in list
        for index, value in enumerate(values):
            if index == 1:
                adjusted_values.append(f"{values[1]} {values[2]}")
            elif index == 2:
                pass
            else:
                adjusted_values.append(value)

        for i in range(len(adjusted_values)):
            label = ctk.CTkLabel(account_frame, text=labels[i], font=("Helvetica", 14, "bold"))
            value = ctk.CTkLabel(account_frame, text=adjusted_values[i], font=("Helvetica", 14))
            label.grid(row=i, column=0, padx=10, pady=10)
            value.grid(row=i, column=1, padx=10, pady=10)

        account_frame.pack(padx=20, pady=10)

        back_btn = ctk.CTkButton(self, text="Back", bg_color="#3574e0", command=lambda: controller.show_frame("MainPage"))
        back_btn.pack(pady=20)


class ContactUsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        # Load and display background image
        image_path = "assets/plane.jpg"
        pil_image = Image.open(image_path)
        pil_image = pil_image.resize((1050, 630))  # resize to desired size

        self.bg_image = CTkImage(light_image=pil_image, dark_image=pil_image, size=(1050, 630))

        bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.controller = controller

        navbar = ctk.CTkFrame(self, height=50, fg_color="#ffffff")
        navbar.pack(fill="x")

        ctk.CTkLabel(navbar, text="FlyDreamAir", font=("Helvetica", 20)).pack(side="left", padx=20)
        ctk.CTkLabel(navbar, text="Contact Us", font=("Helvetica", 18)).place(relx=0.5, rely=0.5, anchor="center")
        
        content_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        

        #Define Labels & Values
        labels = ["Email:", "Phone:", "Address:", "X:", "Facebook:", "Instagram:"]
        values = ["info@flydreamair.com", "+61 1234 5678", "FlyDreamAir Customer Relations P.O. Box 12345, Fake St, NSW, 2500", "@FlyDreamAir", "facebook.com/flydreamair", "@flydreamair_official"]

        for i in range(len(labels)):
            label = ctk.CTkLabel(content_frame, text=labels[i], font=("Helvetica", 14, "bold"))
            value = ctk.CTkLabel(content_frame, text=values[i], font=("Helvetica", 14))
            label.grid(row=i, column=0, padx=10, pady=10)
            value.grid(row=i, column=1, padx=10, pady=10)

        content_frame.pack(padx=20, pady=30)
        

        back_btn = ctk.CTkButton(self, text="Back", bg_color="#599efd", command=lambda: controller.show_frame("MainPage"))
        back_btn.pack(pady=20)

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
