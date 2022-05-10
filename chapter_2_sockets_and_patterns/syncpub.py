#
#  Synchronized publisher
#
import zmq

#  We wait for 10 subcribers
SUBSCRIBERS_EXPECTED = 10


def main():
    context = zmq.Context()

    # Socket to talk to clients
    publisher = context.socket(zmq.PUB)
    # Set SNDHWM, so we don't drop messages for slow subcribers
    publisher.sndhwm = 1100000
    publisher.bind("tcp://*:5561")

    # Socket to receive signals
    syncservice = context.socket(zmq.REP)
    syncservice.bind("tcp://*:5562")

    # Get synchronization from suscribers
    subscribers = 0
    while subscribers < SUBSCRIBERS_EXPECTED:
        # wait for synchronization request
        msg = syncservice.recv()
        # send synchronization reply
        syncservice.send(b"")
        subscribers += 1
        print(f"+1 subcriber ({subscribers} / {SUBSCRIBERS_EXPECTED}) ")

    # Now broadcast exactly 1 updates followed by END
    for i in range(1000000):
        publisher.send(b"Rhubarb")

    publisher.send(b"END")


if __name__ == "__main__":
    main()
