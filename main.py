import time, threading
import random
from collections import deque


class generate_packet (threading.Thread ):

    def __init__(self,queue,generate_factor):
        threading.Thread.__init__(self )
        self.queue = queue
        self.generate_factor = generate_factor

    def run(self):
        i = 0
        while(1):
            d = random.randrange(1,100,1)/self.generate_factor
            time.sleep(d)

            if not self.queue.isFull():
                i = i + 1
                print(i)
                self.queue.put(i)
            else:
                print("packet discard" )




class bucket (threading.Thread):

    def __init__(self, bucket_capacity, Number_of_token ) :
        threading.Thread.__init__(self)
        self.capacity = bucket_capacity
        self.token = 0
        self.Number_of_token = Number_of_token

    def run(self):
        while (1) :
            time.sleep ( 1.0 / Number_of_token )
            if (self.token < self.capacity) :
                self.token += 1

    def hasToken(self):
        if (self.token):
            self.token -= 1
            return True
        return False

    def getTokenCount(self):
        return self.token



class queue (threading.Thread):

    def __init__(self, queue_size, token_bucket):
        threading.Thread.__init__(self)
        self.size = queue_size
        self.queue = [0] * queue_size
        self.bucket = token_bucket
        self.next = 0

    def put(self, packet_data ):
        if (self.next < len ( self.queue )) :
            self.queue[self.next] = packet_data
            self.next += 1
            return True
        return False

    def pop(self):
        if self.next > 0:
            return_data = self.queue[0]
            self.arrange()
            return return_data
        return -1

    def arrange(self):
        self.next -= 1
        for i in range(len(self.queue) - 1 ):
            self.queue[i] = self.queue[i + 1]

    def run(self):
        while(1):
            if self.bucket.hasToken():
                time.sleep(0.1)

                print(self.pop())

    def isnotEmpty(self):
        return not self.next == 0

    def isFull(self ):
        return self.next == len(self.queue )


generate_factor = 1000.0
Speed = 40000  # 40kbps
packet_size = 4  # 4 byte 
Bucket_size = 1000

Queue_Size = 1000

Number_of_token = Speed / packet_size

token_bucket = bucket(Bucket_size, Number_of_token )

Packet_queue = queue(Queue_Size, token_bucket)


Packet_generator = generate_packet(Packet_queue, generate_factor )

Packet_generator.start()
token_bucket.start()
Packet_queue.start()