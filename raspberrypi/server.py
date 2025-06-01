from tkinter import *
import socket
host = ' '
port = 5560

storedValue = "Hello, can you hear me loud and clear?"

def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("socket created")
    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
    print("Socket binding complete")
    return s

def setupConnection():
    s.listen(1)
    connection, address = s.accept()
    print("connected to: " + address[0] + ":" + str(address[1]))
    return connection

def dataTransfer(connection, command_input):
    while True:
        #receiving dataMessage
        data = connection.recv(1024)
        data = data.decode('utf-8')

        dataMessage = data.split(' ', 1)
        command = dataMessage[0]

        connection.sendall(str.encode(command_input))
        print("Data has been sent!")

        
if __name__== "__main__":
    gui = Tk()
    connection = setupConnection()
    s = setupServer()
    
    gui.configure(background="grey")
    
    gui.title("Direction Input")
    
    gui.geometry("370x250")
    
    up_btn = Button(text="up", width=5, height=5, command=dataTransfer(connection, "UP"))
    down_btn = Button(text="down", width=5, height=5, command=dataTransfer(connection, "DOWN"))
    left_btn = Button(text="left", width=5, height=5, command=dataTransfer(connection, "LEFT"))
    right_btn = Button(text="right", width=5, height=5, command=dataTransfer(connection, "RIGHT"))
    stop_btn = Button(text="stop", width=5, height=5, command=dataTransfer(connection, "STOP"))
    
    up_btn.grid(row=0, column=1, padx=5, pady=5)
    left_btn.grid(row=1, column=0, padx=5,pady=5)
    right_btn.grid(row=1, column=2, padx=5, pady=5)
    down_btn.grid(row=1, column=1, padx=5, pady=5)
    stop_btn.grid(row=0, column=3, padx=5, pady=5)

    gui.mainloop()
