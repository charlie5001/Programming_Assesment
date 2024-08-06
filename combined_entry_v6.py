#V5
#Combined entry contains the personal details and booking type, cost.
#Loops
#Adds confimation
#Removes seats after comnfirming booking
#Has a booking ID to be able to Identify different bookings when there are multiple.

final_bookings = []
temp_bookings = []
a_to_p_bunk = 15
a_to_p_recline = 20
p_to_a_bunk = 15
p_to_a_recline = 20


def destination():
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

def ticket_type():
    user_input = int(input("1. Recline $25 eachway \n 2. Bunk $50 eachway\n"))
    if user_input == 1:
        ticket_type = "Recline"
    elif user_input == 2:
        ticket_type = "Bunk"
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


def cost(x, y):
    global temp_bookings
    if y == 1:
        if x == 1:
            cost = 25
        elif x == 2:
            cost=25
        else: cost=50
        


    if y == 2:
        if x == 1:
            cost = 50
        elif x == 2:
            cost = 50
        else: cost = 100
    temp_bookings.append(cost)

def user_input():
    fl_name_and_mobile()
    cost(destination(), ticket_type())
    
def append_to_final_booking(booking_id):
    global final_bookings
    global temp_bookings

    set_seats()
    temp_bookings.append(booking_id)
    final_bookings.append(temp_bookings)
    temp_bookings = []


def set_seats():
    global a_to_p_bunk
    global a_to_p_recline
    global p_to_a_bunk
    global p_to_a_recline
    if temp_bookings[4] == "Bunk":
        if temp_bookings[3] == "Return from Palmerston North" or temp_bookings[3] == "Return from Auckland":
            p_to_a_bunk = p_to_a_bunk - 1
            a_to_p_bunk = a_to_p_bunk - 1

        elif temp_bookings[3] == "One way from Palmerston North to Auckland":
            p_to_a_bunk = p_to_a_bunk - 1
        else:
            a_to_p_bunk = a_to_p_bunk - 1
    else:
        if temp_bookings[3] == "Return from Palmeston North" or temp_bookings[3] == "Return from Auckland":
            p_to_a_recline = p_to_a_recline - 1
            a_to_p_recline = a_to_p_recline - 1

        elif temp_bookings[3] == "One way from Palmerston North to Auckland":
            p_to_a_recline = p_to_a_recline - 1
        else:
            a_to_p_recline = a_to_p_recline - 1     


def confirmation(type, var1):
    if type == "temp_confirm":
        print(var1)
        answer = input("Add  booking?: ")
        return answer


def main():
    global final_bookings
    global temp_bookings

    booking_id = 0
    while True:

        user_input()
        if confirmation("temp_confirm", temp_bookings) == "y":
            booking_id = booking_id + 1
            append_to_final_booking(booking_id)

        else: 
            temp_bookings = []
            break
        print(final_bookings)
        print(temp_bookings)
        print(p_to_a_recline, p_to_a_bunk, a_to_p_recline, a_to_p_bunk)

main()
