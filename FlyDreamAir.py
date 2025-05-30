import pickle
import datetime
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
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
    def __init__(self, customerID, firstName, lastName, contactNumber, email, address, bookings):
        self.customerID = customerID
        self.firstName = firstName
        self.lastName = lastName
        self.contactNumber = contactNumber
        self.email = email
        self.address = address
        self.bookings = bookings

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
    def __init__(self, flightID, bookingID, bookingDate, totalPrice, seatNumber):
        self.flightID = flightID
        self.bookingID = bookingID
        self.bookingDate = bookingDate
        self.totalPrice = totalPrice
        self.seatNumber = seatNumber


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


class InFlightService:
    def __init__(self, serviceID, name, description, price):
        self.serviceID = serviceID
        self.name = name
        self.description = description
        self.price = price

    def list_service_details(self, service_id):

        service_details_list = []

        service_details_list.append(services_list[service_id].serviceID)
        service_details_list.append(services_list[service_id].name)
        service_details_list.append(services_list[service_id].description)
        service_details_list.append(services_list[service_id].price)

        return service_details_list


#---------------------------------Window Classes---------------------------------

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FlyDreamAir")
        self.geometry("1050x630")
        self.frames = {}

        #Data storage to track between frames
        self.matching_flights = []
        self.selected_flight = None

        for F in (MainPage, SeatSelectionPage, FlightResultsPage, ManageFlightsPage, InFlightServicesPage, FoodSelectionPage, DrinkSelectionPage, MyAccountPage, ContactUsPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame("MainPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

        if page_name == "FlightResultsPage" and hasattr(frame, 'load_flights'):
            frame.load_flights()
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

        for label in ["Manage Flight Reservations", "In Flight Services", "My Account", "Contact Us"]:
            btn = ctk.CTkButton(navbar, text=label)
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
        self.date_entry = self.create_styled_entry(input_frame, "Date:")

        search_btn = ctk.CTkButton(search_wrapper, text="Search Flights", fg_color="#7B42F6", text_color="white", font=("Helvetica", 14, "bold"), corner_radius=20, command=lambda: self.submit_flight_search())
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
    
    def submit_flight_search(self):
        from_airport = self.from_entry.get()
        to_airport = self.to_entry.get()
        travel_date = self.date_entry.get()

        matching_flights = []

        #Error handling to confirm all 3 fields have inputs
        if not from_airport or not to_airport or not travel_date:
            error_frame = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=0)
            error_frame.pack(padx=10)

            error_label = ctk.CTkLabel(error_frame, text="Error: All fields (from, to, date) must be provided", font=("Helvetica", 14, "bold"))
            error_label.pack(pady=10, padx=10)

            return matching_flights
        
        try:
            search_date = datetime.datetime.strptime(travel_date, "%Y-%m-%d").date()
        except ValueError:
            error_frame = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=0)
            error_frame.pack(padx=10)

            error_label = ctk.CTkLabel(error_frame, text="Error: Date must be in format YYYY-MM-DD (e.g., 2025-06-15)", font=("Helvetica", 14, "bold"))
            error_label.pack(pady=10, padx=10)
            return matching_flights

        #Converts to uppercase and removes whitespaces to prevent syntax issues
        from_airport = from_airport.upper().strip()
        to_airport = to_airport.upper().strip()

        # Search through all flights
        for flight in flight_list:
            # Check if departure airport matches
            if flight.departureAirport.upper() == from_airport:
                # Check if arrival airport matches
                if flight.arrivalAirport.upper() == to_airport:
                    # Check if date matches
                    if flight.departureTime.date() == search_date:
                        matching_flights.append(flight)

        if len(matching_flights) == 0:
            error_frame = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=0)
            error_frame.pack(padx=10)

            error_label = ctk.CTkLabel(error_frame, text="No Flights are available for this period", font=("Helvetica", 14, "bold"))
            error_label.pack(pady=10, padx=10)

        else:
            self.controller.matching_flights = matching_flights
            self.controller.show_frame("FlightResultsPage")
        return matching_flights


class FlightResultsPage(ctk.CTkFrame):
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

        # Navbar
        navbar = ctk.CTkFrame(self, height=50, fg_color="#ffffff")
        navbar.pack(fill="x")

        ctk.CTkLabel(navbar, text="FlyDreamAir", font=("Helvetica", 20)).pack(side="left", padx=20)
        ctk.CTkLabel(navbar, text="Available Flights", font=("Helvetica", 18)).place(relx=0.5, rely=0.5, anchor="center")

        # Create scrollable frame for flight results
        self.content_frame = ctk.CTkScrollableFrame(self, fg_color="#ffffff")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Back button at bottom
        back_btn = ctk.CTkButton(self, text="Back", command=lambda: controller.show_frame("MainPage"))
        back_btn.pack(pady=10)

        # Create headers
        headers_frame = ctk.CTkFrame(self.content_frame, fg_color="#f0f0f0")
        headers_frame.pack(fill="x", pady=(0, 10))

        headers = ["Flight Number", "Route", "Departure Time", "Price", "Select"]
        for col, header in enumerate(headers):
            header_label = ctk.CTkLabel(headers_frame, text=header, font=("Helvetica", 14, "bold"))
            header_label.grid(row=0, column=col, padx=10, pady=10, sticky="ew")
        
        # Configure column weights for proper spacing
        for i in range(len(headers)):
            headers_frame.grid_columnconfigure(i, weight=1)

        # Load flights when frame is shown
        self.load_flights()


    def load_flights(self):

        # Display flights
        for i, flight in enumerate(self.controller.matching_flights):
            flight_frame = ctk.CTkFrame(self.content_frame, fg_color="#ffffff", border_width=1)
            flight_frame.pack(fill="x", pady=2)

            # Flight Number
            flight_num = getattr(flight, 'flightNumber', f'FL{i+1}')
            flight_label = ctk.CTkLabel(flight_frame, text=str(flight_num))
            flight_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
            
            # Route
            from_airport = getattr(flight, 'departureAirport', 'N/A')
            to_airport = getattr(flight, 'arrivalAirport', 'N/A')
            route_text = f"{from_airport} -> {to_airport}"
            route_label = ctk.CTkLabel(flight_frame, text=route_text)
            route_label.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
            
            # Departure Time
            departure_time = getattr(flight, 'departureTime', 'N/A')
            time_label = ctk.CTkLabel(flight_frame, text=str(departure_time))
            time_label.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
            
            # Price
            price = getattr(flight, 'price', 'N/A')
            price_label = ctk.CTkLabel(flight_frame, text=f"${price}")
            price_label.grid(row=0, column=3, padx=10, pady=10, sticky="ew")
            
            # Select Button
            select_btn = ctk.CTkButton(flight_frame, text="Select", width=80, command=lambda f=flight: self.select_flight(f))
            select_btn.grid(row=0, column=4, padx=10, pady=10, sticky="ew")
            
            # Configure column weights
            for j in range(5):
                flight_frame.grid_columnconfigure(j, weight=1)

    def select_flight(self, flight):
        self.controller.selected_flight = flight
        self.controller.show_frame("SeatSelectionPage")


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

        # Navbar
        navbar = ctk.CTkFrame(self, height=50, fg_color="#ffffff")
        navbar.pack(fill="x")

        ctk.CTkLabel(navbar, text="FlyDreamAir", font=("Helvetica", 20)).pack(side="left", padx=20)
        ctk.CTkLabel(navbar, text="Manage Flights", font=("Helvetica", 18)).place(relx=0.5, rely=0.5, anchor="center")

        # Create scrollable frame for flight results
        self.content_frame = ctk.CTkScrollableFrame(self, fg_color="#ffffff")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Back button at bottom
        back_btn = ctk.CTkButton(self, text="Back", command=lambda: controller.show_frame("MainPage"))
        back_btn.pack(pady=10)

        # Create headers
        headers_frame = ctk.CTkFrame(self.content_frame, fg_color="#f0f0f0")
        headers_frame.pack(fill="x", pady=(0, 10))

        headers = ["Flight Number", "Route", "Departure Time", "Price", "Seat", "Select"]
        for col, header in enumerate(headers):
            header_label = ctk.CTkLabel(headers_frame, text=header, font=("Helvetica", 14, "bold"))
            header_label.grid(row=0, column=col, padx=5, pady=10, sticky="ew")
        
        # Configure column weights for proper spacing
        for i in range(len(headers)):
            headers_frame.grid_columnconfigure(i, weight=1)

        # Load flights when frame is shown
        self.load_flights()


    def load_flights(self):

        # Display flights
        for i, flight in enumerate(customer_list[0].bookings):
            flight_frame = ctk.CTkFrame(self.content_frame, fg_color="#ffffff", border_width=1)
            flight_frame.pack(fill="x", pady=2)

            # Flight Number
            flight_num = getattr(flight, 'flightID', f'FL{i+1}')
            flight_label = ctk.CTkLabel(flight_frame, text=str(flight_num))
            flight_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
            
            # Route
            from_airport = getattr(flight, 'departureAirport', 'N/A')
            to_airport = getattr(flight, 'arrivalAirport', 'N/A')
            route_text = f"{from_airport} -> {to_airport}"
            route_label = ctk.CTkLabel(flight_frame, text=route_text)
            route_label.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
            
            # Departure Time
            departure_time = getattr(flight, 'departureTime', 'N/A')
            time_label = ctk.CTkLabel(flight_frame, text=str(departure_time))
            time_label.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
            
            # Price
            price = getattr(flight, 'totalPrice', 'N/A')
            price_label = ctk.CTkLabel(flight_frame, text=f"${price}")
            price_label.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

            # Seat
            seat = getattr(flight, 'seatNumber', 'N/A')
            price_label = ctk.CTkLabel(flight_frame, text=str(seat))
            price_label.grid(row=0, column=3, padx=10, pady=10, sticky="ew")
            
            # Select Button
            select_btn = ctk.CTkButton(flight_frame, text="Select", width=80, command=lambda f=flight: self.select_flight(f))
            select_btn.grid(row=0, column=4, padx=10, pady=10, sticky="ew")
            
            # Configure column weights
            for j in range(5):
                flight_frame.grid_columnconfigure(j, weight=1)

    def select_flight(self, flight):
        self.controller.selected_flight = flight
        self.controller.show_frame("SeatSelectionPage")


class SeatSelectionPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#83c1fc")
        
        self.controller = controller

        navbar = ctk.CTkFrame(self, height=50, fg_color="#ffffff")
        navbar.pack(fill="x")

        ctk.CTkLabel(navbar, text="FlyDreamAir", font=("Helvetica", 20)).pack(side="left", padx=20)
        ctk.CTkLabel(navbar, text="Seat Selection", font=("Helvetica", 18)).place(relx=0.5, rely=0.5, anchor="center")

        self.seat_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        self.seat_frame.pack(padx=20, pady=10)

        self.seats = {}
        self.cols = 32
        self.cols_labels = ['A','B','C','D','E','F','G','H','J']

        submit_btn = ctk.CTkButton(self, text="Submit", command=self.submit_booking)
        submit_btn.pack(pady=20)

        back_btn = ctk.CTkButton(self, text="Back", command=lambda: controller.show_frame("MainPage"))
        back_btn.pack(pady=20)

        self.selected_seats = set()
        
        # Load seats when frame is first shown
        self.load_seats()

    def load_seats(self):
        """Load and display seats based on current selected flight"""
        # Clear existing seats

        #print(self.controller.selected_flight.bookedSeats)

        for widget in self.seat_frame.winfo_children():
            widget.destroy()
        
        # Get booked seats from selected flight in the App class
        if hasattr(self.controller, 'selected_flight') and self.controller.selected_flight and hasattr(self.controller.selected_flight, 'bookedSeats'):
            unavailable_seats = set(self.controller.selected_flight.bookedSeats)
            print(unavailable_seats)
        else:
            unavailable_seats = set()

        # Add column headers
        for r in range(self.cols):
            col_label = ctk.CTkLabel(self.seat_frame, text=str(r+1), font=("Helvetica", 12, "bold"))
            col_label.grid(row=0, column=r+1, padx=3, pady=(3, 8))

        # Add row labels (letters) on the left and seat buttons
        for c_idx, c in enumerate(self.cols_labels):
            # Add extra padding for row spacing
            extra_pady = 0
            if c_idx == 2:
                extra_pady = 15
            elif c_idx == 5:
                extra_pady = 15
            
            # Add row label on the left
            row_label = ctk.CTkLabel(self.seat_frame, text=c, font=("Helvetica", 12, "bold"))
            row_label.grid(row=c_idx+1, column=0, padx=(3, 8), pady=(3, 3 + extra_pady))
            
            # Add seat buttons
            for r in range(self.cols):
                seat_id = f"{c}{r+1}"
                btn = ctk.CTkButton(self.seat_frame, text="", width=25, height=25, corner_radius=5)
                
                btn.grid(row=c_idx+1, column=r+1, padx=3, pady=(3, 3 + extra_pady))

                if seat_id in unavailable_seats:
                    btn.configure(fg_color="red", hover_color="#ff4d4d", state="disabled")
                else:
                    btn.configure(fg_color="gray", hover_color="#b3b3b3")
                    btn.configure(command=lambda s=seat_id: self.toggle_seat(s))
                self.seats[seat_id] = btn
    
    #Override tkraise to refresh frame when page is loaded
    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.load_seats()

    def toggle_seat(self, seat_id):
        btn = self.seats[seat_id]
        if seat_id in self.selected_seats:
            btn.configure(fg_color="gray")
            self.selected_seats.remove(seat_id)
        else:
            btn.configure(fg_color="blue")
            self.selected_seats.add(seat_id)

    def submit_booking(self):
        if not self.selected_seats:
            error_frame = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=0)
            error_frame.pack(padx=10)

            error_label = ctk.CTkLabel(error_frame, text="No Seats Selected", font=("Helvetica", 14, "bold"))
            error_label.pack(pady=10, padx=10)
            return

        selected_flight = self.controller.selected_flight

        # Update the flight's booked seats
        if hasattr(selected_flight, 'bookedSeats'):
            selected_flight.bookedSeats.extend(list(self.selected_seats))
        
        
        for seat in self.selected_seats:
            booking = Booking(selected_flight.flightID, len(booking_list), datetime.datetime.today().strftime('%Y-%m-%d'), selected_flight.price, seat)
            booking_list.append(booking)
            customer_list[0].bookings.append(booking)

        with open('customers.pkl', 'wb') as f:  # open a text file
            pickle.dump(customer_list, f) # serialize the list
            f.close()
        
        with open('bookings.pkl', 'wb') as f:  # open a text file
            pickle.dump(booking_list, f) # serialize the list
            f.close()

        with open('flights.pkl', 'wb') as f:  # open a text file
            pickle.dump(flight_list, f) # serialize the list
            f.close()
        
        # Navigate to confirmation page or back to main page
        self.controller.show_frame("MainPage")


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

        #Load in food and drink option images
        food_pil = Image.open("assets/food_image.jpg")
        food_pil = food_pil.resize((180, 370))
        self.food_image = CTkImage(light_image=food_pil, dark_image=food_pil, size=(180, 370))

        drink_pil = Image.open("assets/drink_image.jpg")
        drink_pil = drink_pil.resize((180, 370))
        self.drink_image = CTkImage(light_image=drink_pil, dark_image=drink_pil, size=(180, 370))

        button_frame = ctk.CTkFrame(self, fg_color="#83c1fc")
        button_frame.pack(pady=50)

        food_btn = ctk.CTkButton(button_frame, image=self.food_image, text="Food Menu", compound="top", width=180, height=370, font=("Helvetica", 16), command=lambda: controller.show_frame("FoodSelectionPage"))
        food_btn.pack(side="left", padx=20)

        drink_btn = ctk.CTkButton(button_frame, image=self.drink_image, text="Drink Menu", compound="top", width=180, height=370, font=("Helvetica", 16), command=lambda: controller.show_frame("DrinkSelectionPage"))
        drink_btn.pack(side="left", padx=20)

        back_btn = ctk.CTkButton(self, text="Back", command=lambda: controller.show_frame("MainPage"), bg_color="#83c1fc")
        back_btn.pack(pady=20)


class FoodSelectionPage(ctk.CTkFrame):
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
        ctk.CTkLabel(navbar, text="In Flight Food Booking", font=("Helvetica", 18)).place(relx=0.5, rely=0.5, anchor="center")

        food_frame = ctk.CTkFrame(self, fg_color="#ffffff")

        food_index = []

        for i in range(len(services_list)):
            if services_list[i].description == "Food":
                food_index.append(i)
                food_name = ctk.CTkLabel(food_frame, text=services_list[i].name, font=("Helvetica", 14, "bold"))
                food_price = ctk.CTkLabel(food_frame, text=f"${services_list[i].price}", font=("Helvetica", 14))
                food_index[i] = ctk.CTkEntry(food_frame, placeholder_text="Quantity")
                food_name.grid(row=i, column=0, padx=10, pady=10)
                food_price.grid(row=i, column=1, padx=10, pady=10)
                food_index[i].grid(row=i, column=2, padx=10, pady=10)
        
        submit_btn = ctk.CTkButton(food_frame, text="Submit", command=lambda: self.submit_food_order(food_index))
        submit_btn.grid(pady=20, column=1)

        food_frame.pack(padx=20, pady=10)

        back_btn = ctk.CTkButton(self, text="Back", command=lambda: controller.show_frame("InFlightServicesPage"))
        back_btn.pack(pady=20)

    def submit_food_order(self, food_index):
        for i in range(len(food_index)):
            print(food_index[i].get())


class DrinkSelectionPage(ctk.CTkFrame):
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
        ctk.CTkLabel(navbar, text="In Flight Drink Booking", font=("Helvetica", 18)).place(relx=0.5, rely=0.5, anchor="center")

        drink_frame = ctk.CTkFrame(self, fg_color="#ffffff")

        drink_index = []

        for i in range(len(services_list)):
            if services_list[i].description == "Drink":
                drink_index.append(i)
                print(i)
                drink_name = ctk.CTkLabel(drink_frame, text=services_list[i].name, font=("Helvetica", 14, "bold"))
                drink_price = ctk.CTkLabel(drink_frame, text=f"${services_list[i].price}", font=("Helvetica", 14))
                drink_index[len(drink_index) - 1] = ctk.CTkEntry(drink_frame, placeholder_text="Quantity")
                drink_name.grid(row=i, column=0, padx=10, pady=10)
                drink_price.grid(row=i, column=1, padx=10, pady=10)
                drink_index[len(drink_index) - 1].grid(row=i, column=2, padx=10, pady=10)

        submit_btn = ctk.CTkButton(drink_frame, text="Submit", command=lambda: self.submit_drink_order(drink_index))
        submit_btn.grid(pady=20, column=1)

        drink_frame.pack(padx=20, pady=10)

        back_btn = ctk.CTkButton(self, text="Back", command=lambda: controller.show_frame("InFlightServicesPage"))
        back_btn.pack(pady=20)

    def submit_drink_order(self, drink_index):
        for i in range(len(drink_index)):
            print(drink_index[i].get())


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

services_list = []
customer_list = []
flight_list = []
booking_list = []
customer_id = 0

#Read customer data
try:
    with open('customers.pkl', 'rb') as f:
        customer_list = pickle.load(f) # deserialize into object using load()
except:
    pass

#Sort customer list based on customerID
customer_list.sort(key=lambda x: x.customerID)

#Read in flight service data
try:
    with open('services.pkl', 'rb') as f:
        services_list = pickle.load(f) # deserialize into object using load()
except:
    pass

#Sort serivces list based on serviceID
services_list.sort(key=lambda x: x.serviceID)

#Read in flights data
try:
    with open('flights.pkl', 'rb') as f:
        flight_list = pickle.load(f) # deserialize into object using load()
except:
    pass

#Sort customer list based on customerID
flight_list.sort(key=lambda x: x.flightID)

#Read in booking data
try:
    with open('bookings.pkl', 'rb') as f:
        booking_list = pickle.load(f) # deserialize into object using load()
except:
    pass

#Sort customer list based on customerID
booking_list.sort(key=lambda x: x.bookingID)

#---------------------------------Main---------------------------------

if __name__ == "__main__":

    #Create app window
    app = App()
    app.mainloop()
