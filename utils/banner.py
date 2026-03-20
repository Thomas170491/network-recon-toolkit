import socket 

def grab_banner(target :str , port :int ) -> str  :
    try :
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s :
            s.settimeout(1) # Make customable later
            s.connect((target,port))

            #Send basic request
            s.sendall(b"HEAD / HTTP/1.1\r\nHost: example.com\r\n\r\n")

            banner = s.recv(1024)
            return banner.decode(errors= 'ignore').split("\n")[0]




    except Exception:
        return "Unknown service"