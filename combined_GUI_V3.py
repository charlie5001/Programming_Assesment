#Seperate Pages
#New Redo Button
#Summary page logic still in progress.
import tkinter as tk
from tkinter import messagebox

class Go_Bus_Bookings_App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Go Bus Bookings")
        self.geometry("400x400")
        self.booking_id = 1
        self.final_bookings = []
        self.temp_bookings = {}
        self.seat_limits = {
            "One way from Palmerston North to Auckland": {"Recline": 20, "Bunk": 15},
            "One way from Auckland to Palmerston North": {"Recline": 20, "Bunk": 15},
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

    def create_frames(self):
        for F in (Start_Page, Route_Selection_Page, Seat_Type_Page, Confirmation_Page, Summary_Page):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

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

    def clear_all_fields(self):
        self.temp_bookings.clear()
        for frame in self.frames.values():
            if hasattr(frame, 'clear_fields'):
                frame.clear_fields()

    def display_summary(self, text_widget):
        text_widget.delete(1.0, tk.END)
        for booking in self.final_bookings:
            for key, value in booking.items():
                text_widget.insert(tk.END, f"{key}: {value}\n")
            text_widget.insert(tk.END, "\n")

class Start_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="First Name").grid(row=0, column=0)
        self.entry_first_name = tk.Entry(self)
        self.entry_first_name.grid(row=0, column=1)

        tk.Label(self, text="Last Name").grid(row=1, column=0)
        self.entry_last_name = tk.Entry(self)
        self.entry_last_name.grid(row=1, column=1)

        tk.Label(self, text="Mobile Number").grid(row=2, column=0)
        self.entry_mobile = tk.Entry(self)
        self.entry_mobile.grid(row=2, column=1)

        tk.Button(self, text="Confirm", command=self.save_and_next).grid(row=3, column=1)
        tk.Button(self, text="Summary", command=lambda: self.controller.show_frame("Summary_Page")).grid(row=3, column=0)

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

    def clear_fields(self):
        self.entry_first_name.delete(0, tk.END)
        self.entry_last_name.delete(0, tk.END)
        self.entry_mobile.delete(0, tk.END)

class Route_Selection_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Select Route").grid(row=0, column=0)
        self.routes = [
            "One way from Palmerston North to Auckland",
            "One way from Auckland to Palmerston North",
            "Return from Auckland",
            "Return from Palmerston North"
        ]
        self.selected_route = tk.StringVar()
        for i, route in enumerate(self.routes):
            tk.Radiobutton(self, text=route, variable=self.selected_route, value=route).grid(row=i+1, column=0, sticky='w')

        tk.Button(self, text="Confirm", command=self.save_and_next).grid(row=5, column=0)
        tk.Button(self, text="Redo", command=self.redo).grid(row=5, column=1)

        self.recline_label_vars = {}
        self.bunk_label_vars = {}
        for i, route in enumerate(self.controller.seat_limits):
            self.recline_label_vars[route] = tk.StringVar()
            self.bunk_label_vars[route] = tk.StringVar()
            tk.Label(self, textvariable=self.recline_label_vars[route]).grid(row=6 + i, column=0, sticky='w')
            tk.Label(self, textvariable=self.bunk_label_vars[route]).grid(row=8 + i, column=0, sticky='w')

    def save_and_next(self):
        route = self.selected_route.get()
        if not route:
            messagebox.showwarning("Input Error", "Please select a route")
            return

        self.controller.temp_bookings['Route'] = route
        self.controller.show_frame("Seat_Type_Page")

    def redo(self):
        self.controller.clear_all_fields()
        self.controller.show_frame("Start_Page")

    def clear_fields(self):
        self.selected_route.set(None)

    def update_seat_counters(self):
        for route in self.controller.seat_limits:
            self.recline_label_vars[route].set(f"{route} Recline Seats Available: {self.controller.seat_limits[route]['Recline']}")
            self.bunk_label_vars[route].set(f"{route} Bunk Seats Available: {self.controller.seat_limits[route]['Bunk']}")

class Seat_Type_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Select Seat Type").grid(row=0, column=0)
        self.seat_types = ["Recline", "Bunk"]
        self.selected_seat_type = tk.StringVar()
        for i, seat_type in enumerate(self.seat_types):
            tk.Radiobutton(self, text=seat_type, variable=self.selected_seat_type, value=seat_type).grid(row=i+1, column=0, sticky='w')

        tk.Button(self, text="Confirm", command=self.save_and_next).grid(row=3, column=0)
        tk.Button(self, text="Redo", command=self.redo).grid(row=3, column=1)

    def save_and_next(self):
        seat_type = self.selected_seat_type.get()
        if not seat_type:
            messagebox.showwarning("Input Error", "Please select a seat type")
            return

        self.controller.temp_bookings['Seat Type'] = seat_type
        self.controller.show_frame("Confirmation_Page")

    def redo(self):
        self.controller.clear_all_fields()
        self.controller.show_frame("Start_Page")

    def clear_fields(self):
        self.selected_seat_type.set(None)

class Confirmation_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Confirm your booking details").grid(row=0, column=0, columnspan=2)
        self.details_text = tk.Text(self, height=10, width=50)
        self.details_text.grid(row=1, column=0, columnspan=2)

        tk.Button(self, text="Confirm", command=self.confirm_booking).grid(row=2, column=1)
        tk.Button(self, text="Redo", command=self.redo).grid(row=2, column=0)

    def confirm_booking(self):
        self.controller.add_booking()
        self.controller.show_frame("Summary_Page")

    def redo(self):
        self.controller.clear_all_fields()
        self.controller.show_frame("Start_Page")

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.details_text.delete(1.0, tk.END)
        for key, value in self.controller.temp_bookings.items():
            self.details_text.insert(tk.END, f"{key}: {value}\n")
        cost = self.controller.costs[self.controller.temp_bookings['Route']][self.controller.temp_bookings['Seat Type']]
        self.details_text.insert(tk.END, f"Cost: ${cost}\n")

class Summary_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Booking Summary").grid(row=0, column=0)
        self.summary_text = tk.Text(self, height=15, width=50)
        self.summary_text.grid(row=1, column=0, columnspan=2)

        tk.Button(self, text="Redo", command=lambda: self.controller.show_frame("Start_Page")).grid(row=2, column=0)
        tk.Button(self, text="Confirm", command=lambda: self.controller.show_frame("Start_Page")).grid(row=2, column=1)

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.controller.display_summary(self.summary_text)

if __name__ == "__main__":
    app = Go_Bus_Bookings_App()
    app.mainloop()
