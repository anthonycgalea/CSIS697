border = input("Border character?:\t")[0] #get char input from user
length = int(input("Side length?:\t")) #get length input from user

for k in range(length): #for loop through length
    s = (length-k-1)*" " + border #spacing for first character
    if (k == length-1): #last line, most exclusive
        s+= (length-1)*(" " + border) # repeat char + " "
    elif (k > 0): #all lines except first and last
        s+= (2*k-1)*" " + border #adds spaces between chars then the char
    print(s) #output