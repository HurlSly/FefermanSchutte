class Ordinal:
    def __init__(self, decomp):
        decomp.sort(reverse = True)
        
        for i in range(len(decomp) - 1):
            if decomp[i] == decomp[i+1]:
                if decomp[i][0] < decomp[i+1][0]:
                    decomp[i][0] = decomp[i+1][0]
                    decomp[i][1] = decomp[i+1][1]
                elif decomp[i+1][0] < decomp[i][0]:
                    decomp[i+1][0] = decomp[i][0]
                    decomp[i+1][1] = decomp[i][1]
                    
        self.Decomp = decomp
        
    def __len__(self):
        return len(self.Decomp)
    
    def __lt__(self, b):
        if len(self) == 0 and len(b) > 0:
            return True
        
        if len(self) > 0 and len(b) == 0:
            return False
        
        if len(self) == 0 and len(b) == 0:
            return False
        
        i = 0
        while i < len(self) and i < len(b) and self.Decomp[i] == b.Decomp[i]:
            i += 1
            
        if i == len(self):
            return len(self) < len(b)
        
        if i == len(b):
            return False
        
        (alpha, beta) = self.Decomp[i]
        (gamma, delta) = b.Decomp[i]
        
        if alpha == gamma:
            return beta < delta
        
        elif alpha < gamma:
            return beta < Phi(gamma, delta)
        
        else:
            return Phi(alpha, beta) < delta
        
    def __eq__(self, b):
        if len(self) != len(b):
            return False
        
        if len(self) == 1:
            (a, c) = self.Decomp[0]
            (r, s) = b.Decomp[0]
            
            if a == r:
                return c == s
            
            elif a < r:
                return c == b
            
            else: 
                return s == self
                    
        for (x, y) in zip(self.Decomp, b.Decomp):
            if x != y:
                return False
        
        return True
    
    def __le__(self, b):
        return self == b or self < b
    
    def __repr__(self):
        if len(self.Decomp) == 0:
            return "0"

        if len(self) == 1:
            if self.IsOne():
                return "1"
            else:
                return "Phi(%s, %s)" % (self.Decomp[0][0], self.Decomp[0][1])
        
        out = ""

        i = 0
        while i < len(self):
            if i > 0:
                out += " + "
                
            n = 1
            while i + n < len(self) and self.Decomp[i + n] == self.Decomp[i]:
                n += 1
            
            current = Ordinal([self.Decomp[i]])
                
            if n > 1:
                if current.IsOne():
                    out += "%d" % n
                else:
                    out += "%s*%d" % (current, n)
                    
            else:
                out += "%s" % current
                
            i += n
        
        return out
    
    def IsZero(self):
        return len(self) == 0
    
    def IsOne(self):
        if len(self) != 1:
            return False
        
        return self.Decomp[0][0].IsZero() and self.Decomp[0][1].IsZero()
    
    def IsLimit(self):
        if self.IsZero():
            return False
        
        return not(Ordinal([self.Decomp[-1]]).IsOne())
    
    def FundamentalSequence(self, n):
        if self.IsZero():
            return self
        
        zero = Ordinal([])
        
        (a, b) = self.Decomp[-1]
        
        if a.IsZero():
            if b.IsZero():
                return Ordinal(self.Decomp[:-1])
            
            elif b.IsLimit():
                return Ordinal(self.Decomp[:-1] + [[a, b.FundamentalSequence(n)]])
            
            else:
                return Ordinal(self.Decomp[:-1] + [[a, b.FundamentalSequence(n)]] * n)
            
        elif a.IsLimit():
            if b.IsZero():
                return Ordinal(self.Decomp[:-1] + [[a.FundamentalSequence(n), zero]])
            
            elif b.IsLimit():
                return Ordinal(self.Decomp[:-1] + [[a, b.FundamentalSequence(n)]])
            
            else:
                return Ordinal(self.Decomp[:-1] + [[a.FundamentalSequence(n), b]])
            
        else:
            alpha = a.FundamentalSequence(n)
            
            if b.IsZero():
                current = zero
                for i in range(n - 1):
                    current = Phi(alpha, current)
                
                return Ordinal(self.Decomp[:-1] + [[alpha, current]])
            
            elif b.IsLimit():
                return Ordinal(self.Decomp[:-1] + [[a, b.FundamentalSequence(n)]])
            
            else:
                beta = b.FundamentalSequence(n)
                
                courant = Ordinal([[a, beta], [zero, zero]])
                for i in range(n - 1):
                    courant = Phi(alpha, courant)

                return Ordinal(self.Decomp[:-1] + [[alpha, courant]])
        
def Phi(a ,b):
    return Ordinal([[a ,b]])

def FeffermanShutte(n):
    zero = Ordinal([])
    
    current = zero
    for i in range(n):
        current = Phi(current, zero)
        
    t = n
    
    print(current)
    while not current.IsZero():
        current = current.FundamentalSequence(t)
        t += 1
        if t % 1==0:
            print ("%d: %s" % (t, current))
    
    print("---")
    return t
    
def main():
    print(FeffermanShutte(2))
    
main()
        