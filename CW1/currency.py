while(True):
    k = input("Enter the currency in knuts (enter Q to quit):\t")
    if (k == 'Q'):
        break
    else:
        k = int(k)
        g = k//493
        k2 = k-g*493
        s = k2//29
        k2 = k2 - s*29
        print(s,"knuts =",g,"galleons",s,"sickles and",k2,"knuts")