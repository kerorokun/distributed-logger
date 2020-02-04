import argparse
import socket

parser = argparse.ArgumentParser()
parser.add_argument('name', nargs=1, default='node', type=str)
parser.add_argument('address', nargs=1, default='localhost', type=str)
parser.add_argument('port', nargs=1, type=int)

def main():
    args = parser.parse_args()
    name = args.name[0]
    host = args.address[0]
    port = args.port[0]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print('Sending message')
        s.connect((host, port))
        s.sendall(str.encode(name))

        while True:
            data = s.recv(1024)
            if not data:
                break
            print(f'Received {repr(data)}')
            pass

if __name__ == "__main__":
    main()
