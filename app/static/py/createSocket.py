import socket

def UDPSocket(port, timeout=1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", port))
    sock.settimeout(timeout)
    return sock

def TCPSocket(ip, port, timeout=1, host="192.168.1.3"):
    sock =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        # sock.bind((host, port))
        sock.connect((ip, int(port)))
        return True, sock
    except:
        return False, None