import tkinter as tk
from tkinter import messagebox

class GoBusBookingsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Go Bus Bookings")
        self.geometry("400x400")
        self.booking_id = 1
        self.final_bookings = []
        self.temp_bookings = {}
        self.frames = {}

        self.create_frames()
        self.show_frame(StartPage)

    def create_frames(self):
        for F in (StartPage, RouteSelectionPage, SeatTypePage, ConfirmationPage, SummaryPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_class):
        frame = self.frames[page_class.__name__]
        frame.tkraise()

    def add_booking(self):
        self.temp_bookings['Booking ID'] = self.booking_id
        self.final_bookings.append(self.temp_bookings.copy())
        self.booking_id += 1
        self.temp_bookings.clear()
        self.show_frame(SummaryPage)

    def display_summary(self, text_widget):
        text_widget.delete(1.0, tk.END)
        for booking in self.final_bookings:
            for key, value in booking.items():
                text_widget.insert(tk.END, f"{key}: {value}\n")
            text_widget.insert(tk.END, "\n")

class StartPage(tk.Frame):
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
        tk.Button(self, text="Summary", command=lambda: self.controller.show_frame(SummaryPage)).grid(row=3, column=0)

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
        self.controller.show_frame(RouteSelectionPage)

class RouteSelectionPage(tk.Frame):
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
        tk.Button(self, text="Redo", command=lambda: self.controller.show_frame(StartPage)).grid(row=5, column=1)

    def save_and_next(self):
        route = self.selected_route.get()
        if not route:
            messagebox.showwarning("Input Error", "Please select a route")
            return

        self.controller.temp_bookings['Route'] = route
        self.controller.show_frame(SeatTypePage)

class SeatTypePage(tk.Frame):
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
        tk.Button(self, text="Redo", command=lambda: self.controller.show_frame(StartPage)).grid(row=3, column=1)

    def save_and_next(self):
        seat_type = self.selected_seat_type.get()
        if not seat_type:
            messagebox.showwarning("Input Error", "Please select a seat type")
            return

        self.controller.temp_bookings['Seat Type'] = seat_type
        self.controller.show_frame(ConfirmationPage)

class ConfirmationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Confirm your booking details").grid(row=0, column=0, columnspan=2)
        self.details_text = tk.Text(self, height=10, width=50)
        self.details_text.grid(row=1, column=0, columnspan=2)

        tk.Button(self, text="Confirm", command=self.confirm_booking).grid(row=2, column=1)
        tk.Button(self, text="Redo", command=lambda: self.controller.show_frame(StartPage)).grid(row=2, column=0)

    def confirm_booking(self):
        route = self.controller.temp_bookings['Route']
        seat_type = self.controller.temp_bookings['Seat Type']
        cost = costs[route][seat_type]
        self.controller.temp_bookings['Cost'] = cost
        self.controller.add_booking()

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.details_text.delete(1.0, tk.END)
        for key, value in self.controller.temp_bookings.items():
            self.details_text.insert(tk.END, f"{key}: {value}\n")

class SummaryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Booking Summary").grid(row=0, column=0)
        self.summary_text = tk.Text(self, height=15, width=50)
        self.summary_text.grid(row=1, column=0, columnspan=2)

        tk.Button(self, text="Redo", command=lambda: self.controller.show_frame(StartPage)).grid(row=2, column=0)
        tk.Button(self, text="Confirm", command=lambda: self.controller.show_frame(StartPage)).grid(row=2, column=1)

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.controller.display_summary(self.summary_text)

if __name__ == "__main__":
    costs = {
        "One way from Palmerston North to Auckland": {"Recline": 25, "Bunk": 50},
        "One way from Auckland to Palmerston North": {"Recline": 25, "Bunk": 50},
        "Return from Auckland": {"Recline": 50, "Bunk": 100},
        "Return from Palmerston North": {"Recline": 50, "Bunk": 100}
    }

    app = GoBusBookingsApp()
    app.mainloop()
