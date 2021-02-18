#file handling
filename = input("Enter file name:\t")
f = open(filename)
users = int(f.readline())
data = f.readlines()

#initialize adjacency matrix
adjMat = [[0 for k in range(users)] for i in range(users)]

#you cannot be friends with yourself
for k in range(users):
    adjMat[k][k] = -1

#fill adjacency matrix
for line in data:
    friends = line.split(" ")
    adjMat[int(friends[0])][int(friends[1])] = 1
    adjMat[int(friends[1])][int(friends[0])] = 1
while(True):
    #get user input
    inp = input("Enter user id in the range 0 to "+str(len(adjMat) - 1)+" (-1 to quit):\t")

    if (inp == "-1"):
        break
    elif (not (inp.isnumeric())):
        print("Error: Invalid Input")
    else:
        uId = int(inp)
        if (uId >= 0 and uId < users):
            uFriends = adjMat[uId]
            potFriends = []
            for k in range(users):
                if (uFriends[k] == 0):
                    potFriends.append(k)

            maxFriends = -1
            suggested = -1
            for user in potFriends:
                mutFriends = 0
                userMat = adjMat[user]
                for k in range(users):
                    if userMat[k] == 1 and uFriends[k] == 1:
                        mutFriends +=1
                if mutFriends > maxFriends:
                    maxFriends = mutFriends
                    suggested = user
            print("The suggested friend for ",uId, " is ", suggested)
        else:
            print("Error: Invalid Input")
