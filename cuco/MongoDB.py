import os
import tempfile

from fabric.api import *
from fabric.context_managers import *
from jinja2 import Template

from .SupervisorJob import SupervisorJob



class MongoDB(SupervisorJob):
    """docstring for MongoDB"""

    def __init__(self, config):
        """ The following configurations are required:
            - name: job name, as used by Supervisor to uniquely identify the job
                e.g. "db"    (default: "mongodb")

            - config_template: Full path to the template for a config file to be
                used by mongodb during its initialization
                e.g. "/home/db/mongod.conf.tpl"

            - cmd_base: Directory containing the mongodb binary
                e.g. "/usr/local/bin"

            - host: Hostname where mongodb will be bound to
                e.g. "127.0.0.1"      (default: "localhost")

            - port: TCP port where mongodb will be listening to:
                e.g. 5601             (default: 27017)

            - stdout_file: Full path to the file where stdout will be dumped to by
                Supervisor
                e.g. "/home/es/logs/es.out"   (default: <base_dir>/logs/<name>.out)

            - stderr_file: Full path to the file where stderr will be dumped to by
                Supervisor
                e.g. "/home/es/logs/es.out"   (default: <base_dir>/logs/<name>.err)
        """
        super(MongoDB, self).__init__(config)

        if 'name' not in self:
            self['name'] = 'mongodb'

        if 'host' not in self:
            self['host'] = 'localhost'

        if 'port' not in self:
            self['port'] = 27017



    def prepare(self):
        base_dir                  = self.config['base_dir']

        self['log_path']        = os.path.join(base_dir, 'logs')
        self['log_file']        = os.path.join(self['log_path'], "mongod.log")
        self['storage_path']    = os.path.join(base_dir, 'data')
        self['pid_path']        = os.path.join(base_dir, 'mongod.pid')

        for d in ['log_path', 'storage_path']:
            local('mkdir -p %s' % self[d])

        if 'stdout_file' not in self:
            self.config['stdout_file'] = os.path.join(self['log_path'], "%s.out" % self['name'])
        if 'stderr_file' not in self:
            self.config['stderr_file'] = os.path.join(self['log_path'], "%s.err" % self['name'])


        handle, config_file = tempfile.mkstemp(prefix='mongod_config')
        print(config_file)

        tpl      = Template(open(self['config_template'], 'r').read())

        self['cmd'] = os.path.join(self['cmd_base'], 'mongod') + " --config %s" % config_file

        os.write(handle, tpl.render(self.config))

        os.close(handle)
