import argparse
import socket

parser = argparse.ArgumentParser(description="Create a logger to listen for messages on a specified port.")
parser.add_argument('port', nargs=1, default=1234, type=int)

def main():
    # Get the values from the command line
    args = parser.parse_args()
    port = args.port[0]
    host = socket.gethostname()
    host_ip = socket.gethostbyname(host)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f'Opening server at {host_ip}:{port}')
            s.bind((host, port))
            s.listen()

            conn, address = s.accept()
            with conn:
                print(f'{address} | Node connected')
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)
    except KeyboardInterrupt:
        print('\nServer closed')

        


if __name__ == "__main__":
    main()
