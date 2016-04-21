import os
import platform
import socket
import subprocess
import time

from .client import Client
from .exceptions import ProxyServerError


class RemoteServer(object):

    def __init__(self, host, port):
        """
        Initialises a RemoteServer object

        :param host: The host of the proxy server.
        :param port: The port of the proxy server.
        """
        self.host = host
        self.port = port

    @property
    def url(self):
        """
        Gets the url that the proxy is running on. This is not the URL clients
        should connect to.
        """
        return "http://%s:%d" % (self.host, self.port)

    def create_proxy(self, params=None):
        """
        Gets a client class that allow to set all the proxy details that you
        may need to.

        :param dict params: Dictionary where you can specify params
            like httpProxy and httpsProxy
        """
        params = params if params is not None else {}
        client = Client(self.url[7:], params)
        return client

    def _is_listening(self):
        try:
            socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_.settimeout(1)
            socket_.connect((self.host, self.port))
            socket_.close()
            return True
        except socket.error:
            return False


class Server(RemoteServer):

    def __init__(self, path='browsermob-proxy', options=None):
        """
        Initialises a Server object

        :param str path: Path to the browsermob proxy batch file
        :param dict options: Dictionary that can hold the port.
            More items will be added in the future.
            This defaults to an empty dictionary
        """
        options = options if options is not None else {}

        path_var_sep = ':'
        if platform.system() == 'Windows':
            path_var_sep = ';'
            if not path.endswith('.bat'):
                path += '.bat'

        exec_not_on_path = True
        for directory in os.environ['PATH'].split(path_var_sep):
            if(os.path.isfile(os.path.join(directory, path))):
                exec_not_on_path = False
                break

        if not os.path.isfile(path) and exec_not_on_path:
            raise ProxyServerError("Browsermob-Proxy binary couldn't be found "
                                   "in path provided: %s" % path)

        self.path = path
        self.host = 'localhost'
        self.port = options.get('port', 8080)
        self.process = None

        if platform.system() == 'Darwin':
            self.command = ['sh']
        else:
            self.command = []
        self.command += [path, '--port=%s' % self.port]

    def start(self, options=None):
        """
        This will start the browsermob proxy and then wait until it can
        interact with it

        :param dict options: Dictionary that can hold the path and filename
            of the log file with resp. keys of `log_path` and `log_file`
        """
        if options is None:
            options = {}
        log_path = options.get('log_path', os.getcwd())
        log_file = options.get('log_file', 'server.log')
        retry_sleep = options.get('retry_sleep', 0.5)
        retry_count = options.get('retry_count', 60)
        log_path_name = os.path.join(log_path, log_file)
        self.log_file = open(log_path_name, 'w')

        self.process = subprocess.Popen(self.command,
                                        stdout=self.log_file,
                                        stderr=subprocess.STDOUT)
        count = 0
        while not self._is_listening():
            if self.process.poll():
                message = (
                    "The Browsermob-Proxy server process failed to start. "
                    "Check {0}"
                    "for a helpful error message.".format(self.log_file))

                raise ProxyServerError(message)
            time.sleep(retry_sleep)
            count += 1
            if count == retry_count:
                self.stop()
                raise ProxyServerError("Can't connect to Browsermob-Proxy")

    def stop(self):
        """
        This will stop the process running the proxy
        """
        if self.process.poll() is not None:
            return

        try:
            self.process.kill()
            self.process.wait()
        except AttributeError:
            # kill may not be available under windows environment
            pass

        self.log_file.close()
