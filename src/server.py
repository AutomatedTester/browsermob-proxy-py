from subprocess import Popen, PIPE, STDOUT
import socket
import time

from client import Client


class Server(object):

    def __init__(self, path, options={}):
        self.path = path
        self.port = options['port'] if options.has_key('port') else 8080
        self.command = ['sh', path, '--port=%s' % self.port]

    def start(self):
        self.process = Popen(self.command, stdout=PIPE, stderr=STDOUT)
        count = 0
        while not self._is_listening():
            time.sleep(0.1)
            count += 1
            if count == 30:
                raise Exception("Can't connect to Browsermob-Proxy")

        

    def stop(self):
        try:
            if self.process:
                self.process.kill()
                self.process.wait()
        except AttributeError:
            # kill may not be available under windows environment
            pass

    @property
    def url(self):
        return "http://localhost:%d" % self.port

    @property
    def create_proxy(self):
        client = Client(self.url)
        return client

    def _is_listening(self):
        try:
            socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_.settimeout(1)
            socket_.connect(("localhost", self.port))
            socket_.close()
            return True
        except socket.error:
            return False

