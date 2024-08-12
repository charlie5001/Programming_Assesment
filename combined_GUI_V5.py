#in the process of making the elements larger, and making the the buttons more aligned to the centre
#the comment above will be removed when this is complete.
import tkinter as tk
from tkinter import messagebox

# Main application class
class Go_Bus_Bookings_App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Go Bus Bookings")
        self.geometry("450x600")  # Increase window size for better spacing
        self.configure(bg='darkblue')  # Set the background color to dark blue
        self.booking_id = 1
        self.final_bookings = []
        self.temp_bookings = {}
        self.seat_limits = {
            "One way from Palmerston North to Auckland": {"Recline": 15, "Bunk": 20},
            "One way from Auckland to Palmerston North": {"Recline": 15, "Bunk": 20},
        }
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
        for F in (Start_Page, Route_Selection_Page, Seat_Type_Page, Confirmation_Page, Summary_Page, AvailableSeatsPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    # Show a specific frame
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    # Add a booking to the final bookings list and update seat availability
    def add_booking(self):
        booking = {
            "Booking ID": self.booking_id,
            "First Name": self.temp_bookings['First Name'],
            "Last Name": self.temp_bookings['Last Name'],
            "Mobile": self.temp_bookings['Mobile'],
            "Route": self.temp_bookings['Route'],
            "Seat Type": self.temp_bookings['Seat Type'],
            "Cost": self.costs[self.temp_bookings['Route']][self.temp_bookings['Seat Type']]
        }
        
        self.final_bookings.append(booking)
        self.booking_id += 1

        if "Return" in self.temp_bookings['Route']:
            if self.temp_bookings['Route'] == "Return from Auckland":
                self.seat_limits["One way from Auckland to Palmerston North"][self.temp_bookings['Seat Type']] -= 1
                self.seat_limits["One way from Palmerston North to Auckland"][self.temp_bookings['Seat Type']] -= 1
            elif self.temp_bookings['Route'] == "Return from Palmerston North":
                self.seat_limits["One way from Palmerston North to Auckland"][self.temp_bookings['Seat Type']] -= 1
                self.seat_limits["One way from Auckland to Palmerston North"][self.temp_bookings['Seat Type']] -= 1
        else:
            self.seat_limits[self.temp_bookings['Route']][self.temp_bookings['Seat Type']] -= 1

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
        text_widget.delete(1.0, tk.END)
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
        tk.Label(self, text="First Name", bg='darkblue', fg='gold', font=('Arial', 18, 'bold')).grid(row=0, column=0, sticky="e", padx=20, pady=10)  # Set the title to gold
        self.entry_first_name = tk.Entry(self, font=('Arial', 18))
        self.entry_first_name.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self, text="Last Name", bg='darkblue', fg='gold', font=('Arial', 18, 'bold')).grid(row=1, column=0, sticky="e", padx=20, pady=10)  # Set the title to gold
        self.entry_last_name = tk.Entry(self, font=('Arial', 18))
        self.entry_last_name.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self, text="Mobile Number", bg='darkblue', fg='gold', font=('Arial', 18, 'bold')).grid(row=2, column=0, sticky="e", padx=20, pady=10)  # Set the title to gold
        self.entry_mobile = tk.Entry(self, font=('Arial', 18))
        self.entry_mobile.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(self, text="Confirm", command=self.save_and_next, font=('Arial', 18)).grid(row=3, column=1, pady=20)
        tk.Button(self, text="Summary", command=lambda: self.controller.show_frame("Summary_Page"), font=('Arial', 18)).grid(row=3, column=0, pady=20)
        tk.Button(self, text="View Available Seats", command=lambda: self.controller.show_frame("AvailableSeatsPage"), font=('Arial', 18)).grid(row=4, column=0, columnspan=2, pady=10)

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
        self.controller.show_frame("Route_Selection_Page")

    # Clear all input fields
    def clear_fields(self):
        self.entry_first_name.delete(0, tk.END)
        self.entry_last_name.delete(0, tk.END)
        self.entry_mobile.delete(0, tk.END)

# Page where users select their route
class Route_Selection_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='darkblue')  # Set the background color to dark blue
        self.controller = controller
        self.create_widgets()

    # Create widgets for route selection
    def create_widgets(self):
        tk.Label(self, text="Select Route", bg='darkblue', fg='gold', font=('Arial', 18, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)  # Set the title to gold
        self.routes = [
            "One way from Palmerston North to Auckland",
            "One way from Auckland to Palmerston North",
            "Return from Auckland",
            "Return from Palmerston North"
        ]
        self.selected_route = tk.StringVar()
        for i, route in enumerate(self.routes):
            tk.Radiobutton(self, text=route, variable=self.selected_route, value=route, font=('Arial', 16)).grid(row=i+1, column=0, columnspan=2, sticky='w', padx=20, pady=5)

        tk.Button(self, text="Confirm", command=self.save_and_next, font=('Arial', 18)).grid(row=5, column=1, pady=20)
        tk.Button(self, text="Redo", command=self.redo, font=('Arial', 18)).grid(row=5, column=0, pady=20)

        self.recline_label_vars = {}
        self.bunk_label_vars = {}
        for i, route in enumerate(self.controller.seat_limits):
            self.recline_label_vars[route] = tk.StringVar()
            self.bunk_label_vars[route] = tk.StringVar()
            tk.Label(self, textvariable=self.recline_label_vars[route], bg='darkblue', fg='gold', font=('Arial', 16)).grid(row=6 + i, column=0, columnspan=2, sticky='w', padx=20)  # Set the title to gold
            tk.Label(self, textvariable=self.bunk_label_vars[route], bg='darkblue', fg='gold', font=('Arial', 16)).grid(row=8 + i, column=0, columnspan=2, sticky='w', padx=20)  # Set the title to gold

    # Save the selected route and proceed to the next page
    def save_and_next(self):
        route = self.selected_route.get()
        if not route:
            messagebox.showwarning("Input Error", "Please select a route")
            return

        self.controller.temp_bookings['Route'] = route
        self.controller.show_frame("Seat_Type_Page")

    # Reset all fields and return to the start page
    def redo(self):
        self.controller.clear_all_fields()
        self.controller.show_frame("Start_Page")

    # Clear the selected route
    def clear_fields(self):
        self.selected_route.set(None)

    # Update seat availability labels
    def update_seat_counters(self):
        for route in self.controller.seat_limits:
            self.recline_label_vars[route].set(f"{route} Recline Seats Available: {self.controller.seat_limits[route]['Recline']}")
            self.bunk_label_vars[route].set(f"{route} Bunk Seats Available: {self.controller.seat_limits[route]['Bunk']}")

# Page where users select their seat type
class Seat_Type_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='darkblue')  # Set the background color to dark blue
        self.controller = controller
        self.create_widgets()

    # Create widgets for seat type selection
    def create_widgets(self):
        tk.Label(self, text="Select Seat Type", bg='darkblue', fg='gold', font=('Arial', 18, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)  # Set the title to gold
        self.seat_types = ["Recline", "Bunk"]
        self.selected_seat_type = tk.StringVar()
        for i, seat_type in enumerate(self.seat_types):
            tk.Radiobutton(self, text=seat_type, variable=self.selected_seat_type, value=seat_type, font=('Arial', 16)).grid(row=i+1, column=0, columnspan=2, sticky='w', padx=20, pady=5)

        tk.Button(self, text="Confirm", command=self.save_and_next, font=('Arial', 18)).grid(row=3, column=1, pady=20)
        tk.Button(self, text="Redo", command=self.redo, font=('Arial', 18)).grid(row=3, column=0, pady=20)

    # Save the selected seat type and proceed to the next page
    def save_and_next(self):
        seat_type = self.selected_seat_type.get()
        if not seat_type:
            messagebox.showwarning("Input Error", "Please select a seat type")
            return

        self.controller.temp_bookings['Seat Type'] = seat_type
        self.controller.show_frame("Confirmation_Page")

    # Reset all fields and return to the start page
    def redo(self):
        self.controller.clear_all_fields()
        self.controller.show_frame("Start_Page")

    # Clear the selected seat type
    def clear_fields(self):
        self.selected_seat_type.set(None)

# Page where users confirm their booking details
class Confirmation_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='darkblue')  # Set the background color to dark blue
        self.controller = controller
        self.create_widgets()

    # Create widgets for confirmation page
    def create_widgets(self):
        tk.Label(self, text="Confirm your booking details", bg='darkblue', fg='gold', font=('Arial', 18, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)  # Set the title to gold
        self.details_text = tk.Text(self, height=10, width=40, font=('Arial', 16))
        self.details_text.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

        tk.Button(self, text="Confirm", command=self.confirm_booking, font=('Arial', 18)).grid(row=2, column=1, pady=20)
        tk.Button(self, text="Redo", command=self.redo, font=('Arial', 18)).grid(row=2, column=0, pady=20)

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
            self.details_text.insert(tk.END, f"{key}: {value}\n")
        cost = self.controller.costs[self.controller.temp_bookings['Route']][self.controller.temp_bookings['Seat Type']]
        self.details_text.insert(tk.END, f"Cost: ${cost}\n")

# Page displaying a summary of all bookings
class Summary_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='darkblue')  # Set the background color to dark blue
        self.controller = controller
        self.create_widgets()

    # Create widgets for summary page
    def create_widgets(self):
        tk.Label(self, text="Booking Summary", bg='darkblue', fg='gold', font=('Arial', 18, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)  # Set the title to gold
        self.summary_text = tk.Text(self, height=15, width=40, font=('Arial', 16))
        self.summary_text.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

        tk.Button(self, text="Redo", command=lambda: self.controller.show_frame("Start_Page"), font=('Arial', 18)).grid(row=2, column=0, pady=20)
        tk.Button(self, text="Confirm", command=lambda: self.controller.show_frame("Start_Page"), font=('Arial', 18)).grid(row=2, column=1, pady=20)

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
        tk.Label(self, text="Available Seats", bg='darkblue', fg='gold', font=('Arial', 18, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)  # Set the title to gold
        self.seats_text = tk.Text(self, height=15, width=40, font=('Arial', 16))
        self.seats_text.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

        tk.Button(self, text="Back", command=lambda: self.controller.show_frame("Start_Page"), font=('Arial', 18)).grid(row=2, column=0, columnspan=2, pady=20)

    # Display the seat availability
    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.controller.display_seat_availability(self.seats_text)

if __name__ == "__main__":
    app = Go_Bus_Bookings_App()
    app.mainloop()
