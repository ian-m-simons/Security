#############################
#Port Scanner               #
#written by Ian Simons      #
#20260414                   #
#############################

import socket

down = '\033[31mv\033[0m'
error = '\033[91mERROR\033[0m'
up = '\033[32m^\033[0m'
InputPrompt = '\033[94m>\033[0m'
reset = '\033[0m'
def inputIP():
    ipAddress = input(f"[{InputPrompt}] Please enter the IP address you would like to scan> ")
    #todo add IP address validation
    return ipAddress

def setTimeout():
    change = input(f"[{InputPrompt}] default timeout is 1 second, would you like to change timeout?(1=yes/2=no)> ")
    try:
        change = float(change)
    except:
        print(f"[{error}] Invalid input, exiting program")
        exit()
    if change == 1:
        timeout = input(f"[{InputPrompt}] Please enter new timeout in seconds>")
        try: 
            timeout = float(timeout)
            return timeout
        except:
            print(f"[{error}] Invalid input, exiting program")
            exit()
    elif change == 2: 
        return 1.0
    else:
        print(f"[{error}] Invalid selection, exiting program")
        exit()

def setPortList():
    print("[*] select port options \n[*] 1) User provided range\n[*] 2) User provided list\n[*] 3) Default list of commonly used ports")
    port_option = input(f"[{InputPrompt}] > ")
    portList = []
    try:
        port_option = int(port_option)
    except:
        print(f"[{error}] Invalid input, exiting program")
        exit()
    if port_option == 1:
        start = input(f"[{InputPrompt}] Please enter the starting port> ")
        end = input(f"[{InputPrompt}] Please enter the ending port> ")
        try:
            start = int(start)
            end = int(end)
        except:
            print(f"[{error}] Invalid input, exiting program")
            exit()
        for i in range(start, end+1 , 1):
            portList.append(i)
    elif port_option == 2:
        stringPortList = input(f"[{InputPrompt}] Please enter a comma separated list of ports (no spaces)> ")
        portList = stringPortList.split(",")
        for i in range(len(portList)):
            portList[i] = int(portList[i]) 
    elif port_option == 3:
        portList = [20,21,22,23,25,53,67,68,80,110,123,143,443,445,3389]
    else:
        print(f"[{error}] Invalid option, exiting program")
        exit()
    return portList


def scanPorts(ipAddress, timeout, portList):
    print(f"[*] beginning scan of {ipAddress}, timeout set to {timeout}")
    for i in portList:
        server_address = (ipAddress,i)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(timeout)
        try:
            client_socket.connect(server_address)

            print(f"[{up}] port {i} open")

            client_socket.close()
        except:
            print(f"[{down}] port {i} appears to be closed")
    

def main():
    while True:
        ipAddress = inputIP()
        timeout = setTimeout()
        portList = setPortList()
        scanPorts(ipAddress, timeout, portList)
        again = input(f"[{InputPrompt}] Perform another scan?(1=yes/2=no)> ")
        try:
            again = int(again)
        except:
            print(f"[{error}] Invalid input, exiting program")
            exit()
        if again == 1:
            pass
        elif again == 2:
            print("[*] exiting")
            exit()
        else:
            print(f"[{error}] Invalid option, exiting program")
            exit()

if __name__ == '__main__':
    main()