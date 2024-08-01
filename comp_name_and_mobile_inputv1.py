
#Takes the users personal details for the booking 
# and puts it into a list 
final_bookings = []

def fl_name_and_mobile():
    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    mobile = int(input("Enter Mobile"))
    temp_list = []
    temp_list.append(first_name)
    temp_list.append(last_name)
    temp_list.append(mobile)
    print(temp_list)

fl_name_and_mobile()
