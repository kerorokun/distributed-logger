# distributed-logger
This is a short project to get started in learning distributed systems. It's a very simple program that simply allows for multiple clients to send messages to a single leader node. Metrics are collected to start playing around with metric collection.

## To run
Running this program requires running both the distributed logger and the node. 
* To run the logger: `python distributed_logger.py <port>`
* To run the node: `python node.py <node name> <ip address> <port>`
    * If you want to use the generator with the node you can run the node as follows: `python python -u generator.py <frequency> | python node.py <node name> <ip address> <port>`
