#V4
#Combined entry contains the personal details and booking type, cost.
#Loops
#Adds confimation

final_bookings = []
temp_bookings = []

def booking_type():
    global final_bookings
    user_input = int(input("The following choices are:\n1. One way from Palmerston North to Auckland\n2. One way from Auckland to Palmerston North\n3. Return from Auckland\n4. Return from Palmerston North"))
    if user_input == 1:
        ticket_type = "One way from Palmerston North to Auckland"
    elif user_input == 2:
        ticket_type = "One way from Auckland to Palmerston North"
    elif user_input == 3:
        ticket_type = "Return from Auckland"
    elif user_input == 4:
        ticket_type = "Return from Palmerston North"
    temp_bookings.append(ticket_type)
    return user_input

def fl_name_and_mobile():
    global final_bookings
    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    mobile = int(input("Enter Mobile"))
    temp_bookings.append(first_name)
    temp_bookings.append(last_name)
    temp_bookings.append(mobile)


def cost(x):
    global temp_bookings
    if x == 1:
        cost = 50
    elif x == 2:
        cost = 50
    else: cost = 100
    temp_bookings.append(cost)

def user_input():
    fl_name_and_mobile()
    cost(booking_type())
    
def append_to_final_booking():
    global final_bookings
    global temp_bookings
    final_bookings.append(temp_bookings)
    temp_bookings = []


def confirmation(type, var1):
    if type == "temp_confirm":
        print(var1)
        answer = input("Add  booking?: ")
        if answer == "y":
            return answer


def main():
    global temp_bookings
    while True:
        while True:
            user_input()
            if confirmation("temp_confirm", temp_bookings) == "y":
                append_to_final_booking()
            else: 
                temp_bookings = []
                break
            print(final_bookings)
            print(temp_bookings)

main()
