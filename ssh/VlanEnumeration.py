import paramiko 
import subprocess
import time

def ssh_command(ip,port,user,passwd,cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)
    remote_conn = client.invoke_shell()
    time.sleep(1)

    output = remote_conn.recv(65535).decode('utf-8')
    results = []
    for i in cmd:
        if len(results) > 0:
                remote_conn.send(i+"\n")
                time.sleep(1)
                output = remote_conn.recv(65535).decode('utf-8')
                results.append(output)
                while "--More--" in results[-1]:
                    remote_conn.send(" \n")
                    time.sleep(1)
                    output = remote_conn.recv(65535).decode('utf-8')
                    results.append(output)
        else:
            remote_conn.send(i+"\n")
            time.sleep(1)
            output =  remote_conn.recv(65535).decode('utf-8')
            results.append(output)
    client.close()

    return results
def getVlans(SwitchDict, user, password):
     for key in SwitchDict:
        print("working on branch: " + key)
        ip = SwitchDict[key]
        port = 22
        cmd = ["sh ip int br | inc Vlan", "sh vlan br "]
        data = ssh_command(ip, port, user, password, cmd)
        lines = data[0].split("\n")
        Vlans = []
        Names = []
        Ips = []
        finalArray = []
        for i in range(1,len(lines)-1):
            ip = lines[i].split()
            Ips.append(ip[1])
            Vlans.append(ip[0][4:])

        for i in range(1,len(data)):
            lines = data[i].split("\n")
            for j in lines:
                j = j.split()
                try:
                    j[0] = int(j[0])
                    Names.append(j[1])
                    if str(j[0]) not in Vlans:
                        Vlans.append(str(j[0]))
                        Ips.append("n/a")
                except:
                    pass

        for i in range(len(Names)):
            print("vlan: " + Vlans[i] + " Name: " + Names[i] + ", gateway: " + Ips[i])

    

if __name__ == '__main__':
    import getpass
    SwitchDict = {#add dictionary of switches here 
    }
    user = input("Username: ")
    password = getpass.getpass()
    getVlans(SwitchDict, user, password)