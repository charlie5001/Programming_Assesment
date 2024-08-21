#adding the gst portion to the summary
#This Version does not contain the fix for the double appened
import tkinter as tk
from tkinter import messagebox

# Main application class
class Go_Bus_Bookings_App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Go Bus Bookings")
        self.configure(bg='darkblue')  # Set the background color to dark blue
        self.booking_id = 1
        self.final_bookings = []
        self.temp_bookings = {}

        # Adjusted seat limits to include only one-way trips
        self.seat_limits = {
            "One way from Palmerston North to Auckland": {"Recline": 20, "Bunk": 15},
            "One way from Auckland to Palmerston North": {"Recline": 20, "Bunk": 15},
        }

        # Adjusted costs to include return trips
        self.costs = {
            "One way from Palmerston North to Auckland": {"Recline": 25, "Bunk": 50},
            "One way from Auckland to Palmerston North": {"Recline": 25, "Bunk": 50},
            "Return from Auckland": {"Recline": 50, "Bunk": 100},
            "Return from Palmerston North": {"Recline": 50, "Bunk": 100}
        }

        self.frames = {}
        self.create_frames()
        self.show_frame("Start_Page")

    # Create frames for each page and add them to the dictionary of frames
    def create_frames(self):
        for F in (Start_Page, Route_Seat_Page, Confirmation_Page, Summary_Page, AvailableSeatsPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    # Show a specific frame
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        self.geometry('')  # Automatically resize window

    # Add a booking to the final bookings list and update seat availability
    def add_booking(self):
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
        gst_portion = booking['Cost'] - (booking['Cost'] / 1.15)
        booking['GST Portion'] = round(gst_portion, 2)

        # Ensure no duplicate booking ID is added
        if not any(b['Booking ID'] == self.booking_id for b in self.final_bookings):
            self.final_bookings.append(booking)
        self.booking_id += 1

        # Update seat limits
        if "Return" in self.temp_bookings['Route']:
            # Subtract seats from both one-way routes
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
            # Subtract seats from the selected one-way route
            self.seat_limits[self.temp_bookings['Route']]["Recline"] -= self.temp_bookings['Seats']['Recline']
            self.seat_limits[self.temp_bookings['Route']]["Bunk"] -= self.temp_bookings['Seats']['Bunk']

        self.temp_bookings.clear()
        self.show_frame("Start_Page")

    # Clear all fields in the temporary bookings and reset all frames
    def clear_all_fields(self):
        self.temp_bookings.clear()
        for frame in self.frames.values():
            if hasattr(frame, 'clear_fields'):
                frame.clear_fields()

    # Display the summary of all bookings
    def display_summary(self, text_widget):
        text_widget.delete(1.0, tk.END)  # Clear the text widget to avoid duplicates
        for booking in self.final_bookings:
            for key, value in booking.items():
                text_widget.insert(tk.END, f"{key}: {value}\n")
            text_widget.insert(tk.END, "\n")

    # Display the seat availability
    def display_seat_availability(self, text_widget):
        text_widget.delete(1.0, tk.END)
        for route, seats in self.seat_limits.items():
            text_widget.insert(tk.END, f"{route}:\n")
            for seat_type, available in seats.items():
                text_widget.insert(tk.END, f"  {seat_type} Seats Available: {available}\n")
            text_widget.insert(tk.END, "\n")

# Start page where users enter their personal details
class Start_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='darkblue')  # Set the background color to dark blue
        self.controller = controller
        self.create_widgets()

    # Create widgets for the start page
    def create_widgets(self):
        frame = tk.Frame(self, bg='darkblue')
        frame.pack(pady=10, padx=10)

        # Validation commands for first/last name and mobile number
        validate_name = (self.register(self.validate_name), '%P')
        validate_mobile = (self.register(self.validate_mobile), '%P')

        tk.Label(frame, text="First Name", bg='darkblue', fg='gold', font=('Arial', 18, 'bold')).pack(anchor='w', pady=5)
        self.entry_first_name = tk.Entry(frame, font=('Arial', 18), validate='key', validatecommand=validate_name)
        self.entry_first_name.pack(anchor='w', pady=5)

        tk.Label(frame, text="Last Name", bg='darkblue', fg='gold', font=('Arial', 18, 'bold')).pack(anchor='w', pady=5)
        self.entry_last_name = tk.Entry(frame, font=('Arial', 18), validate='key', validatecommand=validate_name)
        self.entry_last_name.pack(anchor='w', pady=5)

        tk.Label(frame, text="Mobile Number", bg='darkblue', fg='gold', font=('Arial', 18, 'bold')).pack(anchor='w', pady=5)
        self.entry_mobile = tk.Entry(frame, font=('Arial', 18), validate='key', validatecommand=validate_mobile)
        self.entry_mobile.pack(anchor='w', pady=5)

        button_frame = tk.Frame(self, bg='darkblue')
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Confirm", command=self.save_and_next, font=('Arial', 18)).pack(side='right', padx=10)
        tk.Button(button_frame, text="Summary", command=lambda: self.controller.show_frame("Summary_Page"), font=('Arial', 18)).pack(side='right', padx=10)
        tk.Button(button_frame, text="View Available Seats", command=lambda: self.controller.show_frame("AvailableSeatsPage"), font=('Arial', 18)).pack(side='right', padx=10)

    # Save the entered details and proceed to the next page
    def save_and_next(self):
        first_name = self.entry_first_name.get()
        last_name = self.entry_last_name.get()
        mobile = self.entry_mobile.get()

        if not first_name or not last_name or not mobile:
            messagebox.showwarning("Input Error", "Please fill in all fields")
            return

        self.controller.temp_bookings['First Name'] = first_name
        self.controller.temp_bookings['Last Name'] = last_name
        self.controller.temp_bookings['Mobile'] = mobile
        self.controller.show_frame("Route_Seat_Page")

    # Clear all input fields
    def clear_fields(self):
        self.entry_first_name.delete(0, tk.END)
        self.entry_last_name.delete(0, tk.END)
        self.entry_mobile.delete(0, tk.END)

    # Validation function for name (only letters allowed)
    def validate_name(self, value_if_allowed):
        if value_if_allowed.isalpha() or value_if_allowed == "":
            return True
        else:
            return False

    # Validation function for mobile (only digits allowed)
    def validate_mobile(self, value_if_allowed):
        if value_if_allowed.isdigit() or value_if_allowed == "":
            return True
        else:
            return False

# Combined Route and Seat Selection Page
class Route_Seat_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='darkblue')  # Set the background color to dark blue
        self.controller = controller
        self.create_widgets()

    # Create widgets for route selection and seat input
    def create_widgets(self):
        frame = tk.Frame(self, bg='darkblue')
        frame.pack(pady=10, padx=10)

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

        tk.Label(frame, text="Enter number of seats:", bg='darkblue', fg='gold', font=('Arial', 18, 'bold')).pack(anchor='w', pady=10)

        tk.Label(frame, text="Recline", bg='darkblue', fg='gold', font=('Arial', 16)).pack(anchor='w', pady=5)
        self.entry_recline = tk.Entry(frame, font=('Arial', 16))
        self.entry_recline.pack(anchor='w', pady=5)

        tk.Label(frame, text="Bunk", bg='darkblue', fg='gold', font=('Arial', 16)).pack(anchor='w', pady=5)
        self.entry_bunk = tk.Entry(frame, font=('Arial', 16))
        self.entry_bunk.pack(anchor='w', pady=5)

        button_frame = tk.Frame(self, bg='darkblue')
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Confirm", command=self.save_and_next, font=('Arial', 18)).pack(side='right', padx=10)
        tk.Button(button_frame, text="Redo", command=self.redo, font=('Arial', 18)).pack(side='right', padx=10)

    # Save the selected route and seat numbers and proceed to the next page
    def save_and_next(self):
        route = self.selected_route.get()
        recline_seats = self.entry_recline.get()
        bunk_seats = self.entry_bunk.get()

        if not route or (not recline_seats and not bunk_seats):
            messagebox.showwarning("Input Error", "Please select a route and enter seat numbers")
            return

        # Convert seat numbers to integers
        try:
            recline_seats = int(recline_seats) if recline_seats else 0
            bunk_seats = int(bunk_seats) if bunk_seats else 0
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter valid numbers for seats")
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

# Page where users confirm their booking details
class Confirmation_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='darkblue')  # Set the background color to dark blue
        self.controller = controller
        self.create_widgets()

    # Create widgets for confirmation page
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

    # Confirm the booking and proceed to the summary page
    def confirm_booking(self):
        self.controller.add_booking()
        self.controller.show_frame("Summary_Page")

    # Reset all fields and return to the start page
    def redo(self):
        self.controller.clear_all_fields()
        self.controller.show_frame("Start_Page")

    # Display the booking details for confirmation
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
# Page displaying a summary of all bookings
class Summary_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='darkblue')  # Set the background color to dark blue
        self.controller = controller
        self.create_widgets()

    # Create widgets for summary page
    def create_widgets(self):
        frame = tk.Frame(self, bg='darkblue')
        frame.pack(pady=10, padx=10)

        tk.Label(frame, text="Booking Summary", bg='darkblue', fg='gold', font=('Arial', 18, 'bold')).pack(anchor='w', pady=10)

        self.summary_text = tk.Text(frame, height=15, width=50, font=('Arial', 16))
        self.summary_text.pack(anchor='w', pady=10)

        button_frame = tk.Frame(self, bg='darkblue')
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Redo", command=lambda: self.controller.show_frame("Start_Page"), font=('Arial', 18)).pack(side='right', padx=10)
        tk.Button(button_frame, text="Confirm", command=lambda: self.controller.show_frame("Start_Page"), font=('Arial', 18)).pack(side='right', padx=10)

    # Display the booking summary
    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.controller.display_summary(self.summary_text)

# Page displaying available seats for each route and seat type
class AvailableSeatsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='darkblue')  # Set the background color to dark blue
        self.controller = controller
        self.create_widgets()

    # Create widgets for available seats page
    def create_widgets(self):
        frame = tk.Frame(self, bg='darkblue')
        frame.pack(pady=10, padx=10)

        tk.Label(frame, text="Available Seats", bg='darkblue', fg='gold', font=('Arial', 18, 'bold')).pack(anchor='w', pady=10)

        self.seats_text = tk.Text(frame, height=15, width=50, font=('Arial', 16))
        self.seats_text.pack(anchor='w', pady=10)

        button_frame = tk.Frame(self, bg='darkblue')
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Back", command=lambda: self.controller.show_frame("Start_Page"), font=('Arial', 18)).pack(padx=10)

    # Display the seat availability (only one-way routes)
    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.controller.display_seat_availability(self.seats_text)

if __name__ == "__main__":
    app = Go_Bus_Bookings_App()
    app.mainloop()
