# UI development python framework -- Tkinter

from tkinter import *
from tkinter import ttk

# Python inbuilt framework -- Time

from time import sleep

# Python based OPCUA framework for Machine to Machine communication protocol

from opcua import Client

# Partial python framework for managing UI user clicks

from functools import partial

#Global variable declarations

global varName, varNode #OPC UA Node Name and Node ID stored globally within framework for client-client communicaiton
varNode=[] # Initialising list with "Null" value
varName=[] # Initialising list with "Null" value
btnids=[]  # Initialising list with "Null" value
btnids1=[] # Initialising list with "Null" value
btnids2=[] # Initialising list with "Null" value
listCondition=["Greater than.","Less than.","Equal to","not Equal to"] # List of preset conditions
listinput=["Enter value","Use input"] # List of preset Input conditions
listaction=["Disconnect input","Disconnect server","Set input"] # List of preset Decisions
serverlist=[] # Initialising list with "Null" value for Server localised name
serverAddress=[] # Initialising list with "Null" value for server address manipulation
abortInput=[] # Initialising list with "Null" value 



#Framework for connecting client services

def testclient(url,port): 

    """ Internal Function -- OPC UA client function for making a communication with the server. 
    Multiple instance of client services can be made using this framework.
    Function takes 2 input argument URL & Port and returns the server Node ID"""

    go="opc.tcp://"+url+":"+port #Binding URL in a OPC UA Webservice format
    global client # Global defining a client for accessing it on other functions
    client=Client(go) #Calling Client function
    
    client.connect()


    print("connected")


    #Queue
    root = client.get_root_node() # Assigning the Client Node ID to a variable
    return root

# Python Tkinter framwork for UI function starts here...

mainwindow=Tk()

# mainwindow.geometry("1600x1000+0+0")
mainwindow.title("OPC-UA Quick-Client") # Defining Title
mainwindow.configure(bg='darkslategray') # Background Colour configuration
lbl_title = Label(mainwindow,text="Welcome to the OPC-UA Quick-Client", fg="white", bg = 'darkslategray').pack # Assigning Title name and UI colour


# Tkinter Framework Functions

def calci(i,dropdown,nodeList,frame,nrow):
    """ Internal Function...
    Function for selection Condition or entering Input
    """
    print(i)
    global varName, varNode,btnids1,btnids,client # Globals
    ids=dropdown.get() #Fetching the row and column of Tkinter UI


    print(ids)
    btnids[i].destroy() #Destroys Tkinter widgets

    if ids=="Set": 
        #Condition 1 apply conditions to the CLient for decision making

        global listCondition, listinput #Globals

        try:

              
            dropdown_con=ttk.Combobox(frame,value=nodeList) # Displays NodeList in a dropdown
            dropdown_con.current(0) #preselects the top one 
            dropdown_con.grid(row=nrow,column=7) #Location on UI tkinter framework
            dropdown_con1=ttk.Combobox(frame,value=listCondition) #List of conditions
            dropdown_con1.current(0) #preselects the top one 
            dropdown_con1.grid(row=nrow,column=8) #Location on UI tkinter framework
            dropdown_in=ttk.Combobox(frame,value=listinput) #List of Output Nodes
            dropdown_in.current(0) #preselects the top one 
            dropdown_in.grid(row=nrow,column=9) #Location on UI tkinter framework

            valueset1=Button(frame,text='set',command=partial(setCondition,i,dropdown_con,dropdown_con1,dropdown_in,frame)) #Widget tkinter button and call a function
            valueset1.grid(row=nrow,column=10) #Location on UI tkinter framework
            btnids1.append(valueset1) #Binds the button configuration in a list


        except Exception as e:
            print(e)
            #Exceptions to disconnect server.
            client.disconnect()



    else:
        
        try:
            # Input data is selected for Node

            dummy=[] #Dummy list
            dropdown_input=ttk.Combobox(frame,value=nodeList) # List of Nodes
            dropdown_input.current(0) #preselects the top one 
            dropdown_input.grid(row=nrow,column=7) #Location on UI tkinter framework

            valueset1=Button(frame,text='set',command=partial(setInput,i,dropdown_input,frame,dummy)) #Widget tkinter button and call a function
            valueset1.grid(row=nrow,column=8) #Location on UI tkinter framework
            dummy.append(valueset1) #Binds the button configuration in a list
            


        except Exception as e:
            print(e)
             #Exceptions to disconnect server.
            client.disconnect()

                
 
def setInput(i,dropdown_input,frame,dummy,newrow=None):
    """ Internal Function
        Widget button press calls the SetInput function
    """

    global btnids2,varNode,varName, abortInput #Globals
    dummy2=[] 
    if dummy:
        #Conditions for autodisconnecting function loop when the applied condition on UI is statisfied
        c_row=dummy[0].grid_info() #Extracts UI tkinter configuration of the widget
        newrow=c_row.get("row") #Extracts UI tkinter configuration of the widget
        dummy[0].destroy() #Destroy button configuration
        dummy.pop(0) # Removes from List
    ids=dropdown_input.get() # Extracts the select combobox value


    var=(varNode[varName.index(ids)].get_value()) #Variable to store the NodeID 
    print(var)
    varNode[i].set_value(var) #Assigns the input of Node A to Node B

    if not ids in abortInput:
        #COndition to abort refresh loop
        
        valueset1=Button(frame,text='reset',command=partial(resetButton,i,dropdown_input,frame,dummy2)) #Button function
        valueset1.grid(row=newrow,column=8) #UI location
        dummy2.append(valueset1) #Adds to a list of button configuration
        

    if not ids in abortInput:
        #COndition to abort refresh loop
        frame.after(1000,lambda:setInput(i,dropdown_input,frame,dummy,newrow)) #UI function refresh every 1 sec
    
    else:
        #After Abort destorys button and variables
        abortInput.remove(ids)
        dropdown_input.destroy()
 

def resetButton(i,dropdown_input,frame,dummy2):
    """ Internal Function...
    For ResetButton to reapply for condition
    """
    global varName,varNode,abortInput #Globals
    inputType=["Set","Input"] #Initial input condition either Set a condition or apply a output to a node
    

    c_row=dummy2[0].grid_info() #Extracting UI widget configuration to a list
    nrow=c_row.get("row") #Extracting row ID

    ids=dropdown_input.get() #Extract the selected combobox value
    abortInput.append(ids) #Adds to list
    print(dummy2)
    dummy2[0].destroy() #Destroy widget button
  
    dummy2.pop(0) #Removes from list
    print(dummy2)
    print("done")
    dropdown=ttk.Combobox(frame,value=inputType) #Dropdown with a input type manual or device iput
    dropdown.current(0) #Initial input selected
    dropdown.grid(row=nrow,column=5) #UI Location
    valueset=Button(frame,text='set',command=partial(calci,i,dropdown,varName,frame,nrow)) #Button to apply condition and calls function
    valueset.grid(row=nrow,column=7) #UI location
    btnids.append(valueset) #Widget configuration stored in a list



def setCondition(i,dropdown_con,dropdown_con1,dropdown_in,frame):
    """Internal FUnction...
    Applying conditions..
    """
    global btnids1, listaction, serverlist, varNode,varName #Globals
    btnids1[i].destroy() #Destroys the button pressed
    selection=dropdown_in.get() #Gets the value of selected combobox
    tempcondition=dropdown_con1.get() #Gets the value of selected combobox of condition
    c_row=dropdown_in.grid_info() #Fetches the configuration list
    newrow=c_row.get("row") #Fetches the rows configuration
    print(newrow)

    if selection=="Enter value": #FIrst condition
        dropdown_in.destroy() #Destroy the button
        enterInput=Entry(frame) #Input entry widget created on frame for inserting input value
        enterInput.grid(row=newrow,column=9) #UI Location
        dropdown_action=ttk.Combobox(frame,value=listaction) #Combobox for list of actions
       
      
        dropdown_action.current(0) #Selects initial Combobox option
        dropdown_action.grid(row=newrow,column=10) #UI Location
        dummy=[] #Dummy List
        dropdown_address=ttk.Combobox(frame,value=serverlist) #Combobox for list of servers
        dropdown_address.current(0) #Initial server is selected
        dropdown_address.grid(row=newrow,column=11) #UI Location
        #Button widget and calls a function
        valueset1=Button(frame,text='apply',command=partial(afteraction,i,dropdown_action,frame,dummy,dropdown_con,enterInput,tempcondition,newrow,dropdown_address)) 
        valueset1.grid(row=newrow,column=12) #UI location
        dummy.append(valueset1) #Adds button configuration in a dummy list
        
        # valueset1=Button(frame,text='set',command=partial(applyentered_value,i,dropdown_con,enterInput,tempcondition,frame))
        # valueset1.grid(row=newrow,column=11)
    else:
        dropdown_in.destroy() #Destroy button
        dropdownInputlist=ttk.Combobox(frame,value=varName)
        dropdownInputlist.current(0)
        dropdownInputlist.grid(row=newrow,column=9)
        dropdown_action=ttk.Combobox(frame,value=listaction)
       
      
        dropdown_action.current(0)
        dropdown_action.grid(row=newrow,column=10)
        dummy=[]
        dropdown_address=ttk.Combobox(frame,value=serverlist)
        dropdown_address.current(0)
        dropdown_address.grid(row=newrow,column=11)
        #Buttin to apply condition and calls a function
        valueset1=Button(frame,text='apply',command=partial(afteractionInput,i,dropdown_action,frame,dummy,dropdown_con,dropdownInputlist,tempcondition,newrow,dropdown_address))
        valueset1.grid(row=newrow,column=12)
        dummy.append(valueset1)

def afteractionInput(i,dropdown_action,frame,dummy,dropdown_con,dropdownInputlist,tempcondition,newrow,dropdown_address):
    """ Internal Function...
    action after function applied
    """
    global listaction, varName #Globals
    selection=dropdown_action.get() #Extracts the value of combobox
    serverid=dropdown_address.get() #Extracts the value of combobox
    dropdown_address.destroy() 
    dummy[0].destroy()
    dummy.pop(0)
 
    print("next")

    
    # ["Disconnect input","Disconnect server","Set input"]
    if selection=="Disconnect input":
        print("Disconnect input")
        #Calls input disconnect function
        valueset1=Button(frame,text='set',command=partial(applyenteredinput_value,i,dropdown_con,dropdownInputlist,tempcondition,frame,selection,dummy))
        valueset1.grid(row=newrow,column=13)
        dummy.append(valueset1) 
        print("others")
        
    elif selection=="Disconnect server":
        print("Disconnect server123")
        print("others")
        #Calls function to disconnect server
        valueset1=Button(frame,text='set',command=partial(applyenteredinput_value,i,dropdown_con,dropdownInputlist,tempcondition,frame,selection,dummy))
        valueset1.grid(row=newrow,column=13)
        dummy.append(valueset1) 
        
    else:
        print("input")
        #Function called to swap the Node ID of input to change function
        dropdown_toInput=ttk.Combobox(frame,value=varName)
        dropdown_toInput.current(0)
        dropdown_toInput.grid(row=newrow,column=13)
        dropdown_toAssign=ttk.Combobox(frame,value=varName)
        dropdown_toAssign.current(0)
        dropdown_toAssign.grid(row=newrow,column=14)
        valueset1=Button(frame,text='set',command=partial(applyinput,i,dropdown_toInput,dropdown_toAssign,frame,dummy))
        valueset1.grid(row=newrow,column=15)
        dummy.append(valueset1)
        print("set input")

def applyinput(i,dropdown_toInput,dropdown_toAssign,frame,dummy):
    """ Internal Function...
    Internally, calls function
    """
    global varName,varNode
    x1=dropdown_toInput.get()
    x2=dropdown_toAssign.get()
    val1=varNode[varName.index(x1)]
    val2=varNode[varName.index(x2)].get_value()
    print(val2)
    val1.set_value(val2)
    frame.after(1000,lambda:applyinput(i,dropdown_toInput,dropdown_toAssign,frame,dummy)) #Refesh the UI loop


def applyenteredinput_value(i,dropdown_con,dropdownInputlist,tempcondition,frame,selection,dummy):
    """ Internal Function...
    Sets the input value
    """
    #["Greater than.","Less than.","Equal to","not Equal to"]
    global btnids1,varNode,varName,abortInput #Globals
    state=True #Flag for existing loop
    dummy[0].destroy()
    tempinputselect=dropdownInputlist.get()
    tempinputvalue=float(varNode[varName.index(tempinputselect)].get_value())
    ids=dropdown_con.get()
    var=float(varNode[varName.index(ids)].get_value()) #stores values in a variable
    if tempcondition=="Greater than.":
        #Condition 1 greater is selected
        if tempinputvalue<var:
            print("value is greater")
            state=False
            if selection=="Disconnect input":
                print("Disconnect input")
                abortInput.append(ids)
        
            elif selection=="Disconnect server":
                print("Disconnect server")
                stop_server(frame,client) 
            else:
                print("input")
                               
    elif tempcondition=="Less than.":
        #Condition 2 Less than is selected
        if tempinputvalue>var:
            print("value is less than")
            state=False
            if selection=="Disconnect input":
                print("Disconnect input")
                abortInput.append(ids)
        
            elif selection=="Disconnect server":
                print("Disconnect server")
                stop_server(frame,client) 
            else:
                print("input")
    elif tempcondition=="Equal to":
        #Condition 3 Equal to is selected
        if tempinputvalue==var:
            print("value is equal")
            state=False
            stop_server(frame,client)  
    elif tempcondition=="not Equal to":
        #Condition 4 Not equal to is selected
        if tempinputvalue != var:
            print("value is not equal")
            state=False
            stop_server(frame,client)  
    else:
        print("nothing selected")
    if state:
        #Refesh until flag changes
        frame.after(1000,lambda:applyenteredinput_value(i,dropdown_con,dropdownInputlist,tempcondition,frame,selection,dummy))


    
def afteraction(i,dropdown_action,frame,dummy,dropdown_con,enterInput,tempcondition,newrow,dropdown_address):
    """ Internal function...
        
    """
    global listaction #globals
    selection=dropdown_action.get()
    serverid=dropdown_address.get()
    dropdown_address.destroy()
    dummy[0].destroy()
    dummy.pop(0)
    
    
    # ["Disconnect input","Disconnect server","Set input"]
    if selection=="Disconnect input":
        print("Disconnect input")
        
    elif selection=="Disconnect server":
        print("Disconnect server")
    else:
        print("input")

       
    # ["Disconnect input","Disconnect server","Set input"]
    if selection=="Disconnect input":
        print("Disconnect input")
        #enables button and call function
        valueset1=Button(frame,text='set',command=partial(applyentered_value,i,dropdown_con,enterInput,tempcondition,frame,selection,dummy))
        valueset1.grid(row=newrow,column=11)
        dummy.append(valueset1)
        
    elif selection=="Disconnect server":
        print("Disconnect server123")
        #enables button and call function
        valueset1=Button(frame,text='set',command=partial(applyentered_value,i,dropdown_con,enterInput,tempcondition,frame,selection,dummy))
        valueset1.grid(row=newrow,column=11)
        dummy.append(valueset1)
        
    else:
        print("input")
        #enables button and call function
        dropdown_toInput=ttk.Combobox(frame,value=varName)
        dropdown_toInput.current(0)
        dropdown_toInput.grid(row=newrow,column=13)
        dropdown_toAssign=ttk.Combobox(frame,value=varName)
        dropdown_toAssign.current(0)
        dropdown_toAssign.grid(row=newrow,column=14)
        valueset1=Button(frame,text='set',command=partial(applyinputE,i,dropdown_toInput,dropdown_toAssign,frame,dummy,enterInput,tempcondition,dropdown_con))
        valueset1.grid(row=newrow,column=15)
        dummy.append(valueset1)
        print("set input")

def applyinputE(i,dropdown_toInput,dropdown_toAssign,frame,dummy,enterInput,tempcondition,dropdown_con):
    """ Internal FUnction...
    """
    global varName,varNode
    tempinputvalue=float(enterInput.get()) #type cast entered value
    ids=dropdown_con.get()
    var=float(varNode[varName.index(ids)].get_value()) #extracts and stores data in a variable
    state=True #Flag for existing loop

    if tempcondition=="Greater than.":
        if tempinputvalue<var:  
            state=False 
            #Calls a function   
            assignvalues(dropdown_toInput,dropdown_toAssign,frame)      
           

    if state:
        #Refreshes loop
        frame.after(1000,lambda:applyinputE(i,dropdown_toInput,dropdown_toAssign,frame,dummy,enterInput,tempcondition,dropdown_con))


def assignvalues(dropdown_toInput,dropdown_toAssign,frame):
    """ Internal Function"""
    global varName,varNode
    x1=dropdown_toInput.get()
    x2=dropdown_toAssign.get()
    val1=varNode[varName.index(x1)]
    val2=varNode[varName.index(x2)].get_value()
    print(val2)
    val1.set_value(val2)
    frame.after(1000,lambda:assignvalues(dropdown_toInput,dropdown_toAssign,frame))



def applyentered_value(i,dropdown_con,enterInput,tempcondition,frame,selection,dummy):
    """ Internal Function"""
    #["Greater than.","Less than.","Equal to","not Equal to"]
    global btnids1,varNode,varName,abortInput
    state=True
    dummy[0].destroy()
    tempinputvalue=float(enterInput.get())
    ids=dropdown_con.get()
    var=float(varNode[varName.index(ids)].get_value())
    if tempcondition=="Greater than.":
        if tempinputvalue<var:
            print("value is greater")
            state=False
            if selection=="Disconnect input":
                print("Disconnect input")
                abortInput.append(ids)
        
            elif selection=="Disconnect server":
                print("Disconnect server")
                stop_server(frame,client) 
            else:
                print("input")
                               
    elif tempcondition=="Less than.":
        if tempinputvalue>var:
            print("value is less than")
            state=False
            stop_server(frame,client)  
    elif tempcondition=="Equal to":
        if tempinputvalue==var:
            print("value is equal")
            state=False
            stop_server(frame,client)  
    elif tempcondition=="not Equal to":
        if tempinputvalue != var:
            print("value is not equal")
            state=False
            stop_server(frame,client)  
    else:
        print("nothing selected")
    if state:
        frame.after(1000,lambda:applyentered_value(i,dropdown_con,enterInput,tempcondition,frame,selection,dummy))


def receive(nodeList,nodeID,frame,flag):   
    """ Internal function...

    """


    inputType=["Set","Input"]

    try:

        global client
        global btnids1,btnids
        for i in nodeList: #Creates a list of Node in a parent node
            
            #Check every node progressively
            indexnumber=nodeList.index(i)
            Mylabel=Label(frame,text=i)
            nrow=10+nodeList.index(i)
            Mylabel.grid(row=nrow,column=0)
            
            
            
            if flag:
                dropdown=ttk.Combobox(frame,value=inputType)
                dropdown.current(0)
                dropdown.grid(row=nrow,column=5)
                valueset=Button(frame,text='set',command=partial(calci,nodeList.index(i),dropdown,nodeList,frame,nrow))
                valueset.grid(row=nrow,column=7)
                btnids.append(valueset)
                
                

            i=Text(frame,height=1,width=20)
            i.grid(row=nrow,column=1,columnspan=3)
            i.delete('1.0',END)
            i.insert(END,nodeID[indexnumber].get_value())
        flag=FALSE


        Mylabel.after(1000,lambda:receive(nodeList,nodeID,frame,flag))
    
    except Exception as e:
        print(e)
        client.disconnect()

def browse_name(node):
    """ Internal function...
        THis function extracts the list of node available in a server. 
        By applying a proper if condition this can used to extract selective node type from server"""
    global varName, varNode
    for childId in node.get_children(): #iterates through every single node of parent class
        ch = client.get_node(childId) #gets the child node ID
        
      
        if str(ch.get_node_class()) == 'NodeClass.Object': #IF object node recursive as a parent node
            browse_name(ch)
        elif str(ch.get_node_class()) == 'NodeClass.Variable' and 'ns=' in str(ch): #Looks for variable node with namespace
            try:
                app=str(ch.get_browse_name()).replace("QualifiedName(","")
               
                
            
                papp=app.replace(')','')
                

                #print(ch.get_value(),"and",papp)

                
                
                varName.append(papp) #stores node name in a list
                varNode.append(ch) #stores node ID in a list
                #print(varNode[0].get_value())
              
                
                
            except ua.uaerrors._auto.BadWaitingForInitialData:
                pass
    
    return varName,varNode

def stop_server(frame,client):
    """Internal function..."""
    #server disconnection
    client.disconnect()
    print("Server disconnected")
    frame.destroy()


def start_server(top,xyz,e1,e2):
    """Internal function"""
    #initiating server
    global serverAddress
    y=e1.get()
    z=e2.get()
    top.destroy()
    x=y+":"+z #OPC UA URL
    serverAddress.append(x)
    frame=LabelFrame(mainwindow,text=xyz,padx=5,pady=5)
    frame.pack(padx=15,pady=15)
    New3=Label(frame, text=x).grid(row=2,column=0)
    Dis_one=Button(frame,text="DisConnect",width=20,command=lambda:stop_server(frame,client))
    Dis_one.grid(row=6,column=0)
    
    # Displays.insert('1.0',x)
      
    root=testclient(y,z)
    nodeList,nodeID=browse_name(root)
    flag=True
    receive(nodeList,nodeID,frame,flag)

 

def stop():
    """Internal function"""
    global client
    client.disconnect()
    print("Disconencted from server")


def start(top,e2):
    """Internal function"""
    global serverlist
    xyz=e2.get()
    serverlist.append(xyz)
    top.destroy()
    top=Tk()
    Displays=Text(top,height=1,width=20)
    Displays.grid(row=0,column=0,columnspan=3)
    Displays.insert('1.0',xyz)

    e1=Entry(top)
    e1.grid(row=4,column=2)   
    New1=Label(top, text="server").grid(row=4,column=0)
    e2=Entry(top)
    e2.grid(row=5,column=2)  
    New2=Label(top, text="PortNumber").grid(row=5,column=0)

    one=Button(top,text="Connect",width=20,command=lambda:start_server(top,xyz,e1,e2))
    one.grid(row=6,column=4)
    



def create_new():
    """Internal function...
    Initial framework without client instance"""

    top=Tk()
    e2 =Entry(top)
    e2.grid(row=4,column=2)

    
    
    #Button press
    New1=Label(top, text="Device Name",width=20).grid(row=4,column=0)

    one=Button(top,text="Create",width=20,command=lambda:start(top,e2))
    one.grid(row=4,column=4)


#Tkinter framework menus
my_menu =Menu(mainwindow)
mainwindow.config(menu=my_menu)
file_menu=Menu(my_menu)
my_menu.add_cascade(label="File",menu=file_menu)
file_menu.add_command(label="New Tool",command=create_new)
file_menu.add_separator()
file_menu.add_cascade(label="Exit",command=mainwindow.quit)


mainwindow.mainloop()

#Tkinter framework ends