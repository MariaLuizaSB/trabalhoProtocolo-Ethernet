import socket
import threading

def handle_tcp(sock, address):
    data_payload = 2048  # The maximum amount of data to be received at once
    try:
        while True:
            print("Waiting to receive TCP message from client")
            data = sock.recv(data_payload)
            if not data:
                break
            print("Received TCP data from %s: %s" % (address, data.decode('utf-8')))
            sock.sendall(data)
            print("Sent TCP response to %s: %s" % (address, data.decode('utf-8')))
    except Exception as e:
        print("TCP Connection error:", e)
    finally:
        print("Closing TCP connection with %s" % str(address))
        sock.close()

def handle_udp(sock):
    data_payload = 2048  # The maximum amount of data to be received at once
    try:
        while True:
            print("Waiting to receive UDP message from client")
            data, address = sock.recvfrom(data_payload)
            print("Received UDP data from %s: %s" % (address, data.decode('utf-8')))
            sock.sendto(data, address)
            print("Sent UDP response to %s: %s" % (address, data.decode('utf-8')))
    except Exception as e:
        print("UDP Connection error:", e)
    finally:
        print("Closing UDP socket")
        sock.close()

def server(protocol, host='localhost', tcp_port=8082, udp_port=8083):
    if protocol.lower() == 'tcp':
        # Create TCP socket
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_sock.bind((host, tcp_port))
        tcp_sock.listen(5)

        print("Starting up echo server on TCP port %s" % tcp_port)

        try:
            while True:
                print("Waiting for incoming connections...")
                tcp_client, tcp_address = tcp_sock.accept()
                print("Accepted TCP connection from:", tcp_address)
                tcp_thread = threading.Thread(target=handle_tcp, args=(tcp_client, tcp_address))
                tcp_thread.start()
        except KeyboardInterrupt:
            print("Keyboard Interrupt. Closing server.")
        finally:
            print("Closing TCP socket")
            tcp_sock.close()
    
    elif protocol.lower() == 'udp':
        # Create UDP socket
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_sock.bind((host, udp_port))

        print("Starting up echo server on UDP port %s" % udp_port)

        try:
            while True:
                print("Waiting for incoming UDP messages...")
                udp_thread = threading.Thread(target=handle_udp, args=(udp_sock,))
                udp_thread.start()
        except KeyboardInterrupt:
            print("Keyboard Interrupt. Closing server.")
        finally:
            print("Closing UDP socket")
            udp_sock.close()
    
    else:
        print("Invalid protocol. Please choose 'tcp' or 'udp'.")

# Ask user for protocol choice
protocol_choice = input("Choose protocol (TCP/UDP): ").strip().lower()
if protocol_choice in ['tcp', 'udp']:
    server(protocol_choice)
else:
    print("Invalid protocol choice.")
