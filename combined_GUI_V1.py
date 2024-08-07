#Trying to use a dictionary instead as the user will  be clicking which one they want combining the information may be faster/shorter
#than appending to a list.

import tkinter as tk
from tkinter import messagebox

# Global variables to store bookings
final_bookings = []
temp_bookings = []
booking_id = 1

# Define costs for different routes and seat types
costs = {
    "One way from Palmerston North to Auckland": {"Recline": 25, "Bunk": 50},
    "One way from Auckland to Palmerston North": {"Recline": 25, "Bunk": 50},
    "Return from Auckland": {"Recline": 50, "Bunk": 100},
    "Return from Palmerston North": {"Recline": 50, "Bunk": 100}
}

# Function to add a booking
def add_booking():
    global booking_id
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    mobile = entry_mobile.get()
    route = selected_route.get()
    seat_type = selected_seat_type.get()
    
    if not first_name or not last_name or not mobile or not route or not seat_type:
        messagebox.showwarning("Input Error", "Please fill in all fields")
        return

    cost = costs[route][seat_type]
    booking = {
        "Booking ID": booking_id,
        "First Name": first_name,
        "Last Name": last_name,
        "Mobile": mobile,
        "Route": route,
        "Seat Type": seat_type,
        "Cost": cost
    }
    
    final_bookings.append(booking)
    booking_id += 1
    display_summary()

# Function to display summary
def display_summary():
    summary_text.delete(1.0, tk.END)
    for booking in final_bookings:
        summary_text.insert(tk.END, f"Booking ID: {booking['Booking ID']}\n")
        summary_text.insert(tk.END, f"First Name: {booking['First Name']}\n")
        summary_text.insert(tk.END, f"Last Name: {booking['Last Name']}\n")
        summary_text.insert(tk.END, f"Mobile: {booking['Mobile']}\n")
        summary_text.insert(tk.END, f"Route: {booking['Route']}\n")
        summary_text.insert(tk.END, f"Seat Type: {booking['Seat Type']}\n")
        summary_text.insert(tk.END, f"Cost: ${booking['Cost']}\n\n")

# Function to clear all fields
def clear_fields():
    entry_first_name.delete(0, tk.END)
    entry_last_name.delete(0, tk.END)
    entry_mobile.delete(0, tk.END)
    selected_route.set(None)
    selected_seat_type.set(None)

# Create the main application window
root = tk.Tk()
root.title("Go Bus Bookings")

# Create and place the widgets
tk.Label(root, text="First Name").grid(row=0, column=0)
entry_first_name = tk.Entry(root)
entry_first_name.grid(row=0, column=1)

tk.Label(root, text="Last Name").grid(row=1, column=0)
entry_last_name = tk.Entry(root)
entry_last_name.grid(row=1, column=1)

tk.Label(root, text="Mobile Number").grid(row=2, column=0)
entry_mobile = tk.Entry(root)
entry_mobile.grid(row=2, column=1)

tk.Label(root, text="Route").grid(row=3, column=0)
routes = [
    "One way from Palmerston North to Auckland",
    "One way from Auckland to Palmerston North",
    "Return from Auckland",
    "Return from Palmerston North"
]
selected_route = tk.StringVar()
for i, route in enumerate(routes):
    tk.Radiobutton(root, text=route, variable=selected_route, value=route).grid(row=3 + i, column=1, sticky='w')

tk.Label(root, text="Seat Type").grid(row=7, column=0)
seat_types = ["Recline", "Bunk"]
selected_seat_type = tk.StringVar()
for i, seat_type in enumerate(seat_types):
    tk.Radiobutton(root, text=seat_type, variable=selected_seat_type, value=seat_type).grid(row=7 + i, column=1, sticky='w')

tk.Button(root, text="Confirm", command=add_booking).grid(row=9, column=1)
tk.Button(root, text="Redo", command=clear_fields).grid(row=9, column=0)

tk.Label(root, text="Summary").grid(row=10, column=0)
summary_text = tk.Text(root, height=10, width=50)
summary_text.grid(row=11, column=0, columnspan=2)

# Run the application
root.mainloop()

