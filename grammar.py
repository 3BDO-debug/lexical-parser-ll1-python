from graphviz import Graph
import tokens_scanner as src



outputs = []
iterator = 0
Nodes = []
Parents = [0]
currentnode = 1
connectParent = True


class node:
    parentNode = 0
    value = ""
    Node = 0
    connectParent = True
    def __init__(self,value,Node, parentNode):
        self.Node = Node
        self.parentNode = parentNode
        self.value = value
    def is_statment(self):
        statment = ["if","repeat","assign","read","write"]
        splitted = self.value.split("\n")
        return any((token in statment) for token in splitted)
    def getvalue(self):
        return self.Node
def match(expectedtoken):
    global iterator
    if(outputs[iterator].tokenvalue==expectedtoken)or(outputs[iterator].tokentype==expectedtoken):
        iterator += 1
    else:
       iterator = -1
def program():
    global iterator
    outputs.append(src.token("END","END"))
    stmtsequence()
def stmtsequence():
    global iterator,connectParent
    connectParent = True
    statment()
    connectParent = False
    while ( outputs[iterator].tokenvalue==';'):
        match(";")
        statment()
def statment():
    global iterator,currentnode,connectParen
    if (len(outputs)):
        newnode = node(outputs[iterator].tokenvalue,currentnode, Parents[-1])
        newnode.connectParent =connectParent
        Nodes.append(newnode)
        currentnode = newnode.getvalue() + 1
        Parents.append(newnode.getvalue())
        if (outputs[iterator].tokenvalue=="if"):
            if_stmt()
        elif (outputs[iterator].tokenvalue=="repeat"):
            repeat_stmt()
        elif (outputs[iterator].tokenvalue=="read"):
            read_stmt()
        elif (outputs[iterator].tokenvalue=="write"):
            write_stmt()
        else:
            Nodes[-1].value = "assign\n(" + outputs[iterator].tokenvalue + ")"
            assign_stmt()

        Parents.pop()
def if_stmt():
    global iterator,currentnode
    match("if")
    exp()
    match("then")
    stmtsequence()
    if(outputs[iterator].tokenvalue=="else"):
        match("else")
        stmtsequence()
    match("end")
def repeat_stmt():
    global iterator,currentnode
    match("repeat")
    stmtsequence()
    match("until")
    exp()
def read_stmt():
    global iterator,currentnode
    match("read")
    if(outputs[iterator].tokentype=="ID"):
        Nodes[-1].value = "read\n(" + outputs[iterator].tokenvalue + ")"
        match("ID")
def write_stmt():
    global iterator
    match("write")
    exp()
    return
def assign_stmt():
    global iterator,currentnode
    if(outputs[iterator].tokentype=="ID"):
        match("ID")
    match(":=")
    exp()
    return
def exp():
    global iterator,currentnode
    simple_exp()
    if (outputs[iterator].iscomparison()):
        comparison_exp()
        simple_exp()
        Parents.pop()
    return
def simple_exp():
    global iterator,currentnode
    term()
    nestedOp=0
    while (outputs[iterator].isaddop()):
        addop()
        term()
        nestedOp+=1
    while(nestedOp>0):
        Parents.pop()
        nestedOp-=1
    return
def comparison_exp():
    global iterator,currentnode
    newnode = node("Op\n("+outputs[iterator].tokenvalue+")",currentnode, Parents[-1])
    Nodes.append(newnode)
    Parents.append(newnode.getvalue())
    Nodes[currentnode-2].parentNode = Parents[-1]
    currentnode = newnode.getvalue() + 1
    if(outputs[iterator].tokenvalue=="<"):
        match("<")
    elif(outputs[iterator].tokenvalue=="="):
        match("=")
def addop():
    global iterator,currentnode
    newnode = node("Op\n("+outputs[iterator].tokenvalue+")",currentnode, Parents[-1])
    Nodes.append(newnode)
    Parents.append(newnode.getvalue())
    Nodes[currentnode-2].parentNode = Parents[-1]
    currentnode = newnode.getvalue() + 1
    if(outputs[iterator].tokenvalue=="+"):
        match("+")
    elif(outputs[iterator].tokenvalue=="-"):
        match("-")
def term():
    global iterator,currentnode
    factor()
    nestedOp=0
    while(outputs[iterator].ismulop()):
        mulop()
        factor()
        nestedOp+=1
    while(nestedOp>0):
        Parents.pop()
        nestedOp-=1
def mulop():
    global iterator,currentnode
    newnode = node("Op\n("+outputs[iterator].tokenvalue+")",currentnode, Parents[-1])
    Nodes.append(newnode)
    Parents.append(newnode.getvalue())
    Nodes[currentnode-2].parentNode = Parents[-1]
    currentnode = newnode.getvalue() + 1
    if(outputs[iterator].tokenvalue=="*"):
        match("*")
    elif(outputs[iterator].tokenvalue=="/"):
        match("/")
def factor():
    global iterator,currentnode
    if(outputs[iterator].tokenvalue=="("):
        match("(")
        exp()
        match(")")
    elif(outputs[iterator].is_NUM()):
        newnode = node("const\n("+outputs[iterator].tokenvalue+")",currentnode, Parents[-1])
        Nodes.append(newnode)
        currentnode = newnode.getvalue() + 1
        match("NUM")
    elif(outputs[iterator].is_ID()):
        newnode = node("ID\n("+outputs[iterator].tokenvalue+")",currentnode, Parents[-1])
        Nodes.append(newnode)
        currentnode = newnode.getvalue() + 1
        match("ID")
def generate_tree():
    global iterator,connectParent,currentnode
    dot = Graph(comment='Syntax Tree',format = 'png')
    for Node in Nodes:
        if(Node.is_statment()):
            dot.node(str(Node.Node),Node.value,shape='square')
        else:
            dot.node(str(Node.Node),Node.value)
    for Node in Nodes:
        if(Node.parentNode!=0)and (Node.connectParent):
            dot.edge(str(Node.parentNode),str(Node.Node))
        elif (Node.parentNode!=0):
            dot.edge(str(Node.parentNode),str(Node.Node),style='dashed', color='white')
    for number in range(len(Nodes)):
        for number2 in range(number+1,len(Nodes)):
            if((Nodes[number].parentNode==Nodes[number2].parentNode) and
            (not Nodes[number2].connectParent)and
            Nodes[number2].is_statment() and (Nodes[number].is_statment())):
                dot.edge(str(Nodes[number].Node),str(Nodes[number2].Node),constraint='false')
                break
            elif((Nodes[number].parentNode==Nodes[number2].parentNode) and
            (Nodes[number2].connectParent)and
            Nodes[number2].is_statment() and (Nodes[number].is_statment())):
                break
    dot.render('scans_outputs/tree.gv',view=True)
    while (len(outputs)):
        outputs.pop()
    while (len(Nodes)):
        Nodes.pop()
    iterator = 0
    currentnode = 1
    connectParent = True
    return