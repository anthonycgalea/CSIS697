class myFraction():
    
    def __init__(self, num, denom=0):
        if not denom==0:
            self.num=int(num)
            self.denom=int(denom)
        else:
            splt = num.split(".")
            coeff = int(splt[0])
            self.num=int(splt[1])
            self.denom=10**len(splt[1])
            self.num+=coeff*self.denom
        self.reduceFrac()
            
    def __str__(self):
        return str(self.num) + "/" + str(self.denom)
    
    def gcd(self):
        gcd=1
        for k in range(1, min([abs(self.num), abs(self.denom)])+1):
            if self.num%k==0 and self.denom%k==0:
                gcd=k
        return gcd

    def reduceFrac(self):
        gc = self.gcd()
        if (gc==1):
            return
        else:
            self.num//=gc
            self.denom//=gc
            self.reduceFrac()

    def add(self, frac):
        return myFraction(self.num*frac.denom + frac.num*self.denom, frac.denom*self.denom)
    
    def subtract(self, fracToSubtract):
        return myFraction(self.num*fracToSubtract.denom - fracToSubtract.num*self.denom, fracToSubtract.denom*self.denom)
    
    def multiply(self, frac):
        return myFraction(self.num*frac.num, frac.denom*self.denom)
    
    def divide(self, fracToDivideBy):
        return myFraction(self.num*fracToDivideBy.denom, self.denom*fracToDivideBy.num)