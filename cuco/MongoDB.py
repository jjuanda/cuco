import os
import tempfile

from fabric.api import *
from fabric.context_managers import *
from jinja2 import Template

from .SupervisorJob import SupervisorJob



class MongoDB(SupervisorJob):
    """docstring for MongoDB"""

    def __init__(self, config_template, cmd_base, base_path, host = "localhost", port = 27017):
        self.config_template = config_template
        self.cmd_base        = cmd_base
        self.base_path       = base_path
        self.host            = host
        self.port            = port
        
        
        
        self.log_path        = os.path.join(self.base_path, 'logs')
        self.storage_path    = os.path.join(self.base_path, 'data')
        self.pid_path        = os.path.join(self.base_path, 'mongod.pid')

        envs = {}

        super(MongoDB, self).__init__(envs, self.base_path, None, "mongodb")

    def prepare(self):
        for d in [self.log_path, self.storage_path]:
            local('mkdir -p %s' % d)

        handle, config_file = tempfile.mkstemp(prefix='mongod_config')
        print(config_file)

        tpl      = Template(open(self.config_template, 'r').read())

        self.cmd = os.path.join(self.cmd_base, 'mongod') + " --config %s" % config_file

        env = {
            'log_path'     : os.path.join(self.log_path, "mongod.log"),
            'storage_path' : self.storage_path,
            'pid_path'     : self.pid_path,
            'mongo_host'   : self.host,
            'mongo_port'   : self.port
        }
        os.write(handle, tpl.render(env))

        os.close(handle)