import rpyc
from rpyc.utils.server import ThreadedServer
import datetime

date_time = datetime.datetime.now()

class MonitorService(rpyc.Service):
    def on_connect(self, conn):
        print(f'connected on {date_time}')

    def on_disconnect(self, conn):
        print(f'connected on {date_time}')


if __name__ == '__main__':
    t = ThreadedServer(MonitorService, port=8100)
    t.start()