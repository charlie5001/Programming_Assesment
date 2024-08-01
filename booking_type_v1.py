


def booking_type():
    user_input = int(input("The following choices are:\n1. One way from Palmerston North to Auckland\n2. One way from Auckland to Palmerston North\n3. Return from Auckland\n4.Return from Palmerston North"))
    if user_input == 1:
        ticket_type = "One way from Palmerston North to Auckland"
    elif user_input == 2:
        ticket_type = "One way from Auckland to Palmerston North"
    elif user_input == 3:
        ticket_type = "Return from Auckland"
    elif user_input == 4:
        ticket_type = "Return from Palmerston North"

        
    