
import RobClient
import time

while True:
    rob = RobClient.Client('localhost', 10000)
    print(rob.request('1'), rob.connected)
    time.sleep(2)
    print(rob.request('2'))
    time.sleep(2)
