class myvalidate:
    #data must be filled
    def required(self,frm):
        for f in frm:
            if f=="":
                return False
        return True
    
    # must be digit
    def mustdigit(self,m):
        if(m.isdigit() and len(m)==10):  #String method
            return True
        return False
    
    # must be alphabate
    def mustalpha(self,frm):
        for f in frm:
            if(not (f.isalpha())):
                return False
        return True        
