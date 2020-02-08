import argparse
import socket
import time
import os
import multiprocessing as mp

parser = argparse.ArgumentParser(description="Create a logger to listen for messages on a specified port.")
parser.add_argument('port', nargs=1, default=1234, type=int)

def handle_client(conn, address, log_queue, delay_queue):
    name = None
    with conn:
        # Handle messages
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                msg = data.decode('utf-8')
                
                if name is None:
                    name = msg
                    log_queue.put(f'{time.time()} - {name} connected')
                else:
                    msg_time, msg = msg.split()

                    delay_queue.put(time.time() - float(msg_time))
                    log_queue.put(f'{msg_time} | {name} | {msg}')
                    
        except Exception as e:
            # TODO: Better error handling
            print(e)
    log_queue.put(f'{time.time()} - {name} disconnected')



def calculate_delay_metrics(delay_queue, log_queue):
    # Get the number of events per second
    # Min, Max, Median, 90th percentile
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(curr_dir, 'delay_log.txt')

    with open(log_file, 'w') as fp:
    
        while True:
            time.sleep(1)
            
            # TODO: Utilize numpy / pandas
            num_events = delay_queue.qsize()
            events = []
            try:
                total_delay = 0
                for i in range(num_events):
                    delay = delay_queue.get()
                    total_delay += delay
                    events.append(delay)

                if events:
                    events.sort()

                    if len(events) % 2 == 0: 
                        median1 = events[len(events)//2] 
                        median2 = events[len(events)//2 - 1] 
                        median = (median1 + median2)/2
                    else: 
                        median = events[len(events)//2]

                    fp.write(f'{events[0]} {events[-1]} {median} {0.9 * total_delay}\n')
                
            except Exception as e:
                print(e)
    

def print_messages(queue):
    while True:
        msg = queue.get()
        print(msg)


def generate_graph(file_path):
    min_delays = []
    max_delays = []
    median_delays = []
    ninety_delays = []
    
    with open(file_path, 'r') as fp:
        for line in fp:
            min_delay, max_delay, median_delay, ninety_delay = line.split()
            min_delays.append(float(min_delay))
            max_delays.append(float(max_delay))
            median_delays.append(float(median_delay))
            ninety_delays.append(float(ninety_delay))

    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Delay (s)')

    plt.plot(min_delays)
    plt.plot(max_delays)
    plt.plot(median_delays)
    plt.plot(ninety_delays)
    
    plt.show()
    
            
def main():
    # Get the values from the command line
    args = parser.parse_args()
    port = args.port[0]
    host = socket.gethostname()
    host_ip = socket.gethostbyname(host)

    processes = []

    try:
        log_queue = mp.Queue()
        delay_queue = mp.Queue()
        
        log_reader = mp.Process(target=print_messages, args=((log_queue), ))
        processes.append(log_reader)
        log_reader.start()
        
        delay_reader = mp.Process(target=calculate_delay_metrics, args=(delay_queue, log_queue))
        processes.append(delay_reader)
        delay_reader.start()
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            log_queue.put(f'Opening server at {host_ip}:{port}')
            s.bind((host, port))
            s.listen()

            while True:
                conn, address = s.accept()
                p = mp.Process(target=handle_client,
                               args=(conn, address, log_queue, delay_queue))
                processes.append(p)
                p.start()
            
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()
            process.join()
        
        print('\nServer closed. Creating the metrics graph.')

        curr_dir = os.path.dirname(os.path.abspath(__file__))
        log_file = os.path.join(curr_dir, 'delay_log.txt')

        generate_graph(log_file)
        


if __name__ == "__main__":
    main()
