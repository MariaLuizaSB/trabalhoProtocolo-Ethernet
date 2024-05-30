# Dupla: Maria Luiza e Samuel Macário

import socket

def client(protocol, host='localhost', port=8082):
    try:
        if protocol.lower() == 'tcp':
            # TCP protocol
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif protocol.lower() == 'udp':
            # UDP protocol
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            print("Invalid protocol. Please choose 'tcp' or 'udp'.")
            return

        server_address = (host, port)
        print("Connecting to %s port %s" % server_address)
        sock.connect(server_address)

        if protocol.lower() == 'tcp':
            # Send and receive TCP data
            message = "Test message. This will be echoed"
            print("Sending %s" % message)
            sock.sendall(message.encode('utf-8'))

            amount_received = 0
            amount_expected = len(message)
            while amount_received < amount_expected:
                data = sock.recv(16)
                amount_received += len(data)
                print("Received: %s" % data)
        else:
            # For UDP, we don't establish a connection, just send a message
            message = "Test message. This will be echoed"
            print("Sending %s" % message)
            sock.sendto(message.encode('utf-8'), server_address)

            # UDP is connectionless, so we need to receive the response explicitly
            data, server = sock.recvfrom(4096)
            print("Received: %s" % data)

    except socket.error as e:
        print("Socket error: %s" % str(e))
    except Exception as e:
        print("Other exception: %s" % str(e))
    finally:
        print("Closing connection to the server")
        sock.close()

# Ask user for protocol choice
protocol_choice = input("Choose protocol (TCP/UDP): ").strip().lower()
if protocol_choice in ['tcp', 'udp']:
    client(protocol_choice)
else:
    print("Invalid protocol choice.")
