#Final Version with all fixes
#This version will be used for the video
#Changed text for the summary page back button
import tkinter as tk
from tkinter import messagebox

# Main application class responsible for managing the entire booking system.
# It handles the initialization, frame creation, and navigation between different pages.
class Go_Bus_Bookings_App(tk.Tk):
    def __init__(self):
        # Initializes the main window and essential variables like booking ID, seat limits, and costs.
        # Justification: The constructor sets up the core of the application, including the overall structure and look.
        super().__init__()
        self.title("Go Bus Bookings")
        self.configure(bg='darkblue')  
        self.booking_id = 1  # Unique ID for each booking
        self.final_bookings = []  # Stores confirmed bookings
        self.temp_bookings = {}  # Temporarily holds booking data before confirmation

        # Adjusted seat limits for one-way trips
        # Justification: Seat limits ensure that bookings do not exceed availability.
        self.seat_limits = {
            "One way from Palmerston North to Auckland": {"Recline": 20, "Bunk": 15},
            "One way from Auckland to Palmerston North": {"Recline": 20, "Bunk": 15},
        }

        # Adjusted costs to include return trips
        # Justification: Separate pricing for one-way and return trips adds flexibility.
        self.costs = {
            "One way from Palmerston North to Auckland": {"Recline": 25, "Bunk": 50},
            "One way from Auckland to Palmerston North": {"Recline": 25, "Bunk": 50},
            "Return from Auckland": {"Recline": 50, "Bunk": 100},
            "Return from Palmerston North": {"Recline": 50, "Bunk": 100}
        }

        self.frames = {}  # Holds references to each page (frame)
        self.create_frames()  # Creates all pages in the application
        self.show_frame("Start_Page")  # Initially displays the start page

    # Creates all frames (pages) in the application and stores them in the frames dictionary.
    # Justification: Preloading frames allows for smooth transitions between pages.
    def create_frames(self):
        for F in (Start_Page, Route_Seat_Page, Confirmation_Page, Summary_Page, AvailableSeatsPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    # Displays the specified frame (page) by bringing it to the front.
    # Justification: Centralized navigation control makes it easy to manage page transitions.
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        self.geometry('')  # Automatically resize window to fit content

    # Adds a new booking to the final bookings list, calculates costs, and updates seat availability.
    # Justification: Encapsulating booking logic ensures consistency and reduces errors.
    def add_booking(self):
        # Create a new booking entry
        booking = {
            "Booking ID": self.booking_id,
            "First Name": self.temp_bookings['First Name'],
            "Last Name": self.temp_bookings['Last Name'],
            "Mobile": self.temp_bookings['Mobile'],
            "Route": self.temp_bookings['Route'],
            "Seats": self.temp_bookings['Seats'],  # Dictionary of seat types and quantities
            "Cost": sum(self.costs[self.temp_bookings['Route']][seat_type] * quantity 
                        for seat_type, quantity in self.temp_bookings['Seats'].items())
        }

        # Calculate and add GST portion to the booking
        gst_portion = booking['Cost'] - (booking['Cost'] / 1.15)
        booking['GST Portion'] = round(gst_portion, 2)

        # Ensure no duplicate booking ID is added
        if not any(b['Booking ID'] == self.booking_id for b in self.final_bookings):
            self.final_bookings.append(booking)
        self.booking_id += 1

        # Update seat limits based on the route and seat types selected
        if "Return" in self.temp_bookings['Route']:
            # Adjust seats for return trips (affects both directions)
            if "Auckland" in self.temp_bookings['Route']:
                self.seat_limits["One way from Auckland to Palmerston North"]["Recline"] -= self.temp_bookings['Seats']['Recline']
                self.seat_limits["One way from Auckland to Palmerston North"]["Bunk"] -= self.temp_bookings['Seats']['Bunk']
                self.seat_limits["One way from Palmerston North to Auckland"]["Recline"] -= self.temp_bookings['Seats']['Recline']
                self.seat_limits["One way from Palmerston North to Auckland"]["Bunk"] -= self.temp_bookings['Seats']['Bunk']
            elif "Palmerston North" in self.temp_bookings['Route']:
                self.seat_limits["One way from Palmerston North to Auckland"]["Recline"] -= self.temp_bookings['Seats']['Recline']
                self.seat_limits["One way from Palmerston North to Auckland"]["Bunk"] -= self.temp_bookings['Seats']['Bunk']
                self.seat_limits["One way from Auckland to Palmerston North"]["Recline"] -= self.temp_bookings['Seats']['Recline']
                self.seat_limits["One way from Auckland to Palmerston North"]["Bunk"] -= self.temp_bookings['Seats']['Bunk']
        else:
            # Adjust seats for one-way trips
            self.seat_limits[self.temp_bookings['Route']]["Recline"] -= self.temp_bookings['Seats']['Recline']
            self.seat_limits[self.temp_bookings['Route']]["Bunk"] -= self.temp_bookings['Seats']['Bunk']

        self.temp_bookings.clear()  # Clear temporary booking data after confirmation
        self.show_frame("Start_Page")  # Return to the start page

    # Clears all temporary bookings and resets fields across all frames.
    # Justification: Ensures that no leftover data is carried into new bookings.
    def clear_all_fields(self):
        self.temp_bookings.clear()
        for frame in self.frames.values():
            if hasattr(frame, 'clear_fields'):
                frame.clear_fields()

    # Displays a summary of all confirmed bookings in the summary page.
    # Justification: Provides the user with an overview of all bookings made so far.
    def display_summary(self, text_widget):
        text_widget.delete(1.0, tk.END)  # Clear the text widget to avoid duplicates
        for booking in self.final_bookings:
            for key, value in booking.items():
                text_widget.insert(tk.END, f"{key}: {value}\n")
            text_widget.insert(tk.END, "\n")

    # Displays the current seat availability for each route and seat type.
    # Justification: Allows users to see available seats before making a booking decision.
    def display_seat_availability(self, text_widget):
        text_widget.delete(1.0, tk.END)
        for route, seats in self.seat_limits.items():
            text_widget.insert(tk.END, f"{route}:\n")
            for seat_type, available in seats.items():
                text_widget.insert(tk.END, f"  {seat_type} Seats Available: {available}\n")
            text_widget.insert(tk.END, "\n")


# Start page class where users enter personal details like name and mobile number.
# Justification: Collecting user information is the first step in the booking process.
class Start_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='darkblue')  # Set the background color to dark blue
        self.controller = controller
        self.create_widgets()

    # Creates the input fields and buttons for the start page.
    # Justification: Clear separation of UI elements improves maintainability.
    def create_widgets(self):
        frame = tk.Frame(self, bg='darkblue')
        frame.pack(pady=10, padx=10)

        # Validation commands for first/last name and mobile number
        validate_name = (self.register(self.validate_name), '%P')
        validate_mobile = (self.register(self.validate_mobile), '%P')

        # First Name entry field
        tk.Label(frame, text="First Name", bg='darkblue', fg='gold', font=('Arial', 18, 'bold')).pack(anchor='w', pady=5)
        self.entry_first_name = tk.Entry(frame, font=('Arial', 18), validate='key', validatecommand=validate_name)
        self.entry_first_name.pack(anchor='w', pady=5)

        # Last Name entry field
        tk.Label(frame, text="Last Name", bg='darkblue', fg='gold', font=('Arial', 18, 'bold')).pack(anchor='w', pady=5)
        self.entry_last_name = tk.Entry(frame, font=('Arial', 18), validate='key', validatecommand=validate_name)
        self.entry_last_name.pack(anchor='w', pady=5)

        # Mobile Number entry field
        tk.Label(frame, text="Mobile Number", bg='darkblue', fg='gold', font=('Arial', 18, 'bold')).pack(anchor='w', pady=5)
        self.entry_mobile = tk.Entry(frame, font=('Arial', 18), validate='key', validatecommand=validate_mobile)
        self.entry_mobile.pack(anchor='w', pady=5)

        # Buttons for form submission, viewing summary, and available seats
        button_frame = tk.Frame(self, bg='darkblue')
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Confirm", command=self.save_and_next, font=('Arial', 18)).pack(side='right', padx=10)
        tk.Button(button_frame, text="Summary", command=lambda: self.controller.show_frame("Summary_Page"), font=('Arial', 18)).pack(side='right', padx=10)
        tk.Button(button_frame, text="View Available Seats", command=lambda: self.controller.show_frame("AvailableSeatsPage"), font=('Arial', 18)).pack(side='right', padx=10)

    # Validates input and saves data before proceeding to the route selection page.
    # Justification: Ensures that only valid data is processed in the booking flow.
    def save_and_next(self):
        first_name = self.entry_first_name.get()
        last_name = self.entry_last_name.get()
        mobile = self.entry_mobile.get()

        # Input validation
        if not first_name or not last_name or not mobile:
            messagebox.showwarning("Input Error", "Please fill in all fields")
            return

        # Store the validated data in temp_bookings
        self.controller.temp_bookings['First Name'] = first_name
        self.controller.temp_bookings['Last Name'] = last_name
        self.controller.temp_bookings['Mobile'] = mobile
        self.controller.show_frame("Route_Seat_Page")

    # Clears the input fields, useful when the user wants to reset the form.
    def clear_fields(self):
        self.entry_first_name.delete(0, tk.END)
        self.entry_last_name.delete(0, tk.END)
        self.entry_mobile.delete(0, tk.END)

    # Validation function to ensure names only contain alphabetic characters.
    def validate_name(self, value_if_allowed):
        if value_if_allowed.isalpha() or value_if_allowed == "":
            return True
        else:
            return False

    # Validation function to ensure the mobile number only contains digits.
    def validate_mobile(self, value_if_allowed):
        if value_if_allowed.isdigit() or value_if_allowed == "":
            return True
        else:
            return False


# Route and Seat Selection Page class where users select a route and number of seats.
# Justification: Separating this logic into its own page ensures clear organization of the booking process.
class Route_Seat_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='darkblue')  # Set the background color to dark blue
        self.controller = controller
        self.create_widgets()

    # Create widgets for route selection and seat input
    def create_widgets(self):
        frame = tk.Frame(self, bg='darkblue')
        frame.pack(pady=10, padx=10)

        # Route selection options
        tk.Label(frame, text="Select Route", bg='darkblue', fg='gold', font=('Arial', 18, 'bold')).pack(anchor='w', pady=5)
        self.routes = [
            "One way from Palmerston North to Auckland",
            "One way from Auckland to Palmerston North",
            "Return from Auckland",
            "Return from Palmerston North"
        ]
        self.selected_route = tk.StringVar()
        for route in self.routes:
            tk.Radiobutton(frame, text=route, variable=self.selected_route, value=route, font=('Arial', 16), bg='darkblue', fg='gold').pack(anchor='w', pady=5)

        # Validation for seat numbers (only digits allowed)
        validate_seat_number = (self.register(self.validate_seat_number), '%P')

        # Seat number input fields
        tk.Label(frame, text="Enter number of seats:", bg='darkblue', fg='gold', font=('Arial', 18, 'bold')).pack(anchor='w', pady=10)
        
        tk.Label(frame, text="Recline", bg='darkblue', fg='gold', font=('Arial', 16)).pack(anchor='w', pady=5)
        self.entry_recline = tk.Entry(frame, font=('Arial', 16), validate='key', validatecommand=validate_seat_number)
        self.entry_recline.pack(anchor='w', pady=5)

        tk.Label(frame, text="Bunk", bg='darkblue', fg='gold', font=('Arial', 16)).pack(anchor='w', pady=5)
        self.entry_bunk = tk.Entry(frame, font=('Arial', 16), validate='key', validatecommand=validate_seat_number)
        self.entry_bunk.pack(anchor='w', pady=5)

        # Buttons for confirming and resetting seat selection
        button_frame = tk.Frame(self, bg='darkblue')
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Confirm", command=self.save_and_next, font=('Arial', 18)).pack(side='right', padx=10)
        tk.Button(button_frame, text="Redo", command=self.redo, font=('Arial', 18)).pack(side='right', padx=10)

    # Validation function to ensure seat numbers only contain numeric digits.
    def validate_seat_number(self, value_if_allowed):
        if value_if_allowed.isdigit() or value_if_allowed == "":
            return True
        else:
            return False

    # Save the selected route and seat numbers and proceed to the next page
    # Save the selected route and seat numbers and proceed to the next page
    def save_and_next(self):
        route = self.selected_route.get()
        recline_seats = self.entry_recline.get()
        bunk_seats = self.entry_bunk.get()

        # Ensure route and seat numbers are provided
        if not route or (not recline_seats and not bunk_seats):
            messagebox.showwarning("Input Error", "Please select a route and enter seat numbers")
            return

        # Convert seat numbers to integers and validate that they are greater than zero
        try:
            recline_seats = int(recline_seats) if recline_seats else 0
            bunk_seats = int(bunk_seats) if bunk_seats else 0
            if recline_seats <= 0 and bunk_seats <= 0:
                raise ValueError("Seats must be greater than zero")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter valid seat numbers greater than zero")
            return

        # Check seat availability
        if "Return" in route:
            # Check for return routes by verifying the seat count for both corresponding one-way routes
            if (recline_seats > self.controller.seat_limits["One way from Palmerston North to Auckland"]['Recline'] or
                recline_seats > self.controller.seat_limits["One way from Auckland to Palmerston North"]['Recline'] or
                bunk_seats > self.controller.seat_limits["One way from Palmerston North to Auckland"]['Bunk'] or
                bunk_seats > self.controller.seat_limits["One way from Auckland to Palmerston North"]['Bunk']):
                messagebox.showwarning("Seat Availability", "Not enough seats available for a return trip")
                return
        else:
            # Check seat availability for one-way routes
            if recline_seats > self.controller.seat_limits[route]['Recline'] or bunk_seats > self.controller.seat_limits[route]['Bunk']:
                messagebox.showwarning("Seat Availability", "Not enough seats available")
                return

        # Store route and seat selection in temp_bookings
        self.controller.temp_bookings['Route'] = route
        self.controller.temp_bookings['Seats'] = {'Recline': recline_seats, 'Bunk': bunk_seats}
        self.controller.show_frame("Confirmation_Page")


    # Reset all fields and return to the start page
    def redo(self):
        self.controller.clear_all_fields()
        self.controller.show_frame("Start_Page")

    # Clear the selected route and seat numbers
    def clear_fields(self):
        self.selected_route.set(None)
        self.entry_recline.delete(0, tk.END)
        self.entry_bunk.delete(0, tk.END)

# Confirmation Page class where users review and confirm their booking details.
# Justification: A final review step reduces the risk of errors before committing the booking.
class Confirmation_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='darkblue')
        self.controller = controller
        self.create_widgets()

    # Creates the text area for displaying booking details and confirmation buttons.
    def create_widgets(self):
        frame = tk.Frame(self, bg='darkblue')
        frame.pack(pady=10, padx=10)

        tk.Label(frame, text="Confirm your booking details", bg='darkblue', fg='gold', font=('Arial', 18, 'bold')).pack(anchor='w', pady=10)
        self.details_text = tk.Text(frame, height=10, width=50, font=('Arial', 16))
        self.details_text.pack(anchor='w', pady=10)

        button_frame = tk.Frame(self, bg='darkblue')
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Confirm", command=self.confirm_booking, font=('Arial', 18)).pack(side='right', padx=10)
        tk.Button(button_frame, text="Redo", command=self.redo, font=('Arial', 18)).pack(side='right', padx=10)

    # Adds the booking to the final list and transitions to the summary page.
    def confirm_booking(self):
        self.controller.add_booking()
        self.controller.show_frame("Summary_Page")

    # Resets all fields and returns to the start page.
    def redo(self):
        self.controller.clear_all_fields()
        self.controller.show_frame("Start_Page")

    # Displays the booking details for final confirmation.
    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.details_text.delete(1.0, tk.END)
        for key, value in self.controller.temp_bookings.items():
            if key == "Seats":
                self.details_text.insert(tk.END, f"{key}:\n")
                for seat_type, quantity in value.items():
                    self.details_text.insert(tk.END, f"  {seat_type}: {quantity}\n")
            else:
                self.details_text.insert(tk.END, f"{key}: {value}\n")
        cost = sum(self.controller.costs[self.controller.temp_bookings['Route']][seat_type] * quantity 
                   for seat_type, quantity in self.controller.temp_bookings['Seats'].items())
        gst_portion = cost - (cost / 1.15)
        self.details_text.insert(tk.END, f"Total Cost: ${cost}\n")
        self.details_text.insert(tk.END, f"GST Portion: ${round(gst_portion, 2)}\n")


# Summary Page class to display all confirmed bookings.
# Justification: Giving users a final overview ensures transparency and accuracy in the booking process.
class Summary_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='darkblue')
        self.controller = controller
        self.create_widgets()

    # Creates the text area for displaying booking summaries and navigation buttons.
    def create_widgets(self):
        frame = tk.Frame(self, bg='darkblue')
        frame.pack(pady=10, padx=10)

        tk.Label(frame, text="Booking Summary", bg='darkblue', fg='gold', font=('Arial', 18, 'bold')).pack(anchor='w', pady=10)
        self.summary_text = tk.Text(frame, height=15, width=50, font=('Arial', 16))
        self.summary_text.pack(anchor='w', pady=10)

        button_frame = tk.Frame(self, bg='darkblue')
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Confirm", command=lambda: self.controller.show_frame("Start_Page"), font=('Arial', 18)).pack(side='right', padx=10)
        tk.Button(button_frame, text="Back", command=lambda: self.controller.show_frame("Start_Page"), font=('Arial', 18)).pack(side='right', padx=10)

    # Populates the summary text area with all confirmed bookings.
    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.controller.display_summary(self.summary_text)


# Available Seats Page class to display seat availability for all routes.
# Justification: Providing seat availability information helps users make informed booking decisions.
class AvailableSeatsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='darkblue')
        self.controller = controller
        self.create_widgets()

    # Creates the text area for displaying available seats and navigation button.
    def create_widgets(self):
        frame = tk.Frame(self, bg='darkblue')
        frame.pack(pady=10, padx=10)

        tk.Label(frame, text="Available Seats", bg='darkblue', fg='gold', font=('Arial', 18, 'bold')).pack(anchor='w', pady=10)
        self.seats_text = tk.Text(frame, height=15, width=50, font=('Arial', 16))
        self.seats_text.pack(anchor='w', pady=10)

        button_frame = tk.Frame(self, bg='darkblue')
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Back", command=lambda: self.controller.show_frame("Start_Page"), font=('Arial', 18)).pack(padx=10)

    # Populates the available seats text area with up-to-date data.
    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.controller.display_seat_availability(self.seats_text)

# Will run the main loop
if __name__ == "__main__":
    app = Go_Bus_Bookings_App()
    app.mainloop()
