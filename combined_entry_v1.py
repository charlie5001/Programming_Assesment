#V1
#Combined entry contains the personal details and booking type.

final_bookings = []


def booking_type():
    global final_bookings
    user_input = int(input("The following choices are:\n1. One way from Palmerston North to Auckland\n2. One way from Auckland to Palmerston North\n3. Return from Auckland\n4.Return from Palmerston North"))
    if user_input == 1:
        ticket_type = "One way from Palmerston North to Auckland"
    elif user_input == 2:
        ticket_type = "One way from Auckland to Palmerston North"
    elif user_input == 3:
        ticket_type = "Return from Auckland"
    elif user_input == 4:
        ticket_type = "Return from Palmerston North"
    final_bookings.append(ticket_type)

def fl_name_and_mobile():
    global final_bookings
    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    mobile = int(input("Enter Mobile"))
    temp_list = []
    temp_list.append(first_name)
    temp_list.append(last_name)
    temp_list.append(mobile)
    print(temp_list)
    final_bookings.append(temp_list)


fl_name_and_mobile()
booking_type()
print(final_bookings)
