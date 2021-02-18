def hasUpperCase(password): #checks if password contains an uppercase, returns true if it doesn't
    for k in range(len(password)): #loop through password characters
        if (password[k].isupper()): #checks if its uppercase
            return False
    return True

def twoDigits(password): #checks if there are two numbers in the password, returns true if it doesn't
    count = 0
    for k in range(len(password)): #loop through password characters
        if (password[k].isnumeric()): #checks if character is a number
            count+=1 #add one to count
    if count < 2:
        return True
    else:
        return False

def isValidPassword(password): #checks each possible fail option
    if (len(password) < 8):
        return False
    elif (not password.isalnum()):
        return False
    elif (twoDigits(password)):
        return False
    elif (hasUpperCase(password)):
        return False
    else:
        return True

passw = input("Enter a string for password:\t")
if (not isValidPassword(passw)):
    print("invalid password")
else:
    print("valid password")