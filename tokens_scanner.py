reservedwords = ['if','then','else','end','repeat','until','read','write']
specialsymbols = [':=','+','-','*','/','=','<', '(',')',';']
class token:
    tokenvalue=""
    tokentype=""
    def __init__(self, tokenvalue, tokentype):
        self.tokentype = tokentype
        self.tokenvalue = tokenvalue
    def is_ID(self):
        if(self.tokentype=="ID"):
            return True
        else:
            return False
    def is_NUM(self):
        if(self.tokentype=="NUM"):
            return True
        else:
            return False
    def is_reservedword(self):
        if(self.tokentype=="reserved words"):
            return True
        else:
            return False
    def is_terminator(self):
        if(self.tokenvalue==";"):
            return True
        else:
            return False
    def iscomparison(self):
        if((self.tokenvalue=='<')or(self.tokenvalue=='=')):
            return True
        else:
            return False
    def isaddop(self):
        if((self.tokenvalue=='+')or(self.tokenvalue=='-')):
            return True
        else:
            return False
    def ismulop(self):
        if((self.tokenvalue=='*')or(self.tokenvalue=='/')):
            return True
        else:
            return False
def scanner(given_lines):
    lines = [s.rstrip() for s in given_lines]
    lines = [s.lstrip() for s in lines]
    lines = [s.strip() for s in lines]
    outputs = []
    currentstate='start'
    currenttoken=""
    for line in lines:
        for char in (line+' '):
            if(char.isalnum)or (char in reservedwords):
                if(currentstate=='start'):
                    if(char=='{'):
                        currentstate='Incomment'
                    elif(char==':'):
                         currentstate='inassign'
                         currenttoken+=(char)
                    elif((char.isdigit())or (char=='-')):
                         currentstate='Innum'
                         currenttoken+=(char)
                    elif(char.isalpha()):
                         currentstate='Inid'
                         currenttoken+=(char)
                    elif(char in specialsymbols):
                        currentstate='start'
                        mytoken = token(char,"special symbols")
                        outputs.append(mytoken)
                elif(currentstate=='Incomment'):
                    if(char=='}'):
                        currentstate='start'
                elif(currentstate=='inassign'):
                    if(char=='='):
                        currenttoken+=(char)
                        currenttoken=''.join(currenttoken)
                        mytoken = token(currenttoken,"special symbols")
                        outputs.append(mytoken)
                        currenttoken=""
                        currentstate='start'
                elif(currentstate=='Innum'):
                    if(char.isdigit()): 
                         currenttoken+=(char)
                    else:
                        currenttoken=''.join(currenttoken)
                        mytoken = token(currenttoken,"NUM")
                        outputs.append(mytoken)
                        currenttoken=""
                        currentstate='start'
                        if(char in specialsymbols):
                            currentstate='start'
                            mytoken = token(char,"special symbols")
                            outputs.append(mytoken)
                elif(currentstate=='Inid'):
                    if(char.isdigit() or char.isalpha()): 
                         currenttoken+=(char)
                    else:
                        currenttoken=''.join(currenttoken)
                        if(currenttoken in reservedwords):
                            mytoken = token(currenttoken,"reserved words")
                            outputs.append(mytoken)
                        else:
                            mytoken = token(currenttoken,"ID")
                            outputs.append(mytoken)
                        currenttoken=""
                        currentstate='start'
                        if(char==':'):
                            currentstate='inassign'
                            currenttoken +=char
                        elif(char in specialsymbols):
                            currentstate='start'
                            mytoken = token(char,"special symbols")
                            outputs.append(mytoken)
                elif(char in specialsymbols):
                        currentstate='start'
                        mytoken = token(char,"special symbols")
                        outputs.append(mytoken) 
    for tok in outputs:
        print("Token value", tok.tokentype)
        print('Token type', tok.tokenvalue)
    return outputs


