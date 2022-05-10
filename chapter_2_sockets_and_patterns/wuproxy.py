# Weather proxy device
#
# Author: Lev Givon <let(at)columbia(dot)edu>

import zmq

context = zmq.Context()

# This is where the wheather server sits
frontend = context.socket(zmq.SUB)
frontend.connect("tcp://192.168.55.210:5556")

# This is our public endpoint for subscribers
backend = context.socket(zmq.PUB)
backend.bind("tcp://10.1.1.0:8100")

# Subscribe on enverything
frontend.setsockopt(zmq.SUBSCRIBE, b"")

# Shun messages out to our own subscribers
while True:
    # Process all parts of the message
    message = frontend.recv_multipart()
    backend.send_multipart(message)
