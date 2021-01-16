while(True):
    k = input("Enter the currency in knuts (enter Q to quit):\t") #get input
    if (k == 'Q'): #for quitting
        break
    else:
        k = int(k) #convert input to int
        g = k//493 #get galleons
        k2 = k-g*493 #remove galleons from knut count
        s = k2//29 #get sickles
        k2 = k2 - s*29 #remove sickles from knut count
        print(s,"knuts =",g,"galleons",s,"sickles and",k2,"knuts")