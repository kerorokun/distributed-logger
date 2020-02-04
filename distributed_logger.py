import argparse
import socket

import multiprocessing as mp

parser = argparse.ArgumentParser(description="Create a logger to listen for messages on a specified port.")
parser.add_argument('port', nargs=1, default=1234, type=int)

def handle_client(conn, address, queue):
    with conn:
        # Handle messages
        queue.put(f'{address} | Node connected')
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)

def print_messages(queue):
    while True:
        msg = queue.get()
        print(msg)
            
def main():
    # Get the values from the command line
    args = parser.parse_args()
    port = args.port[0]
    host = socket.gethostname()
    host_ip = socket.gethostbyname(host)

    processes = []

    try:
        process_queue = mp.Queue()
        reader = mp.Process(target=print_messages, args=((process_queue), ))
        processes.append(reader)
        reader.start()
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            process_queue.put(f'Opening server at {host_ip}:{port}')
            s.bind((host, port))
            s.listen()

            while True:
                conn, address = s.accept()
                p = mp.Process(target=handle_client, args=(conn, address, process_queue))
                processes.append(p)
                p.start()
            
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()
            process.join()
        
        print('\nServer closed')

        


if __name__ == "__main__":
    main()
