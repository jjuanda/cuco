import os

from fabric.api import *
from fabric.context_managers import *

from .SupervisorJob import SupervisorJob



class ShellCommand(SupervisorJob):
    """docstring for ShellCommand"""

    def __init__(self, config):
        """ The following configurations are required:
            - base_dir: Base directory for the supervisor job
                e.g. "/home/es"

            - cmd: Full command (with args) that supervisor will run
                e.g. "elasticsearch -p /home/es/es.pid"

            - stdout_file: Full path to the file where stdout will be dumped to by
                Supervisor
                e.g. "/home/es/logs/es.out"   (default: <base_dir>/logs/<name>.out)

            - stderr_file: Full path to the file where stderr will be dumped to by
                Supervisor
                e.g. "/home/es/logs/es.out"   (default: <base_dir>/logs/<name>.err)
        """
        if 'name' not in config:
            raise ValueError("An explicit name is required for ShellCommands")

        super(ShellCommand, self).__init__(config)

        self['log_base']    = os.path.join(self['base_dir'], 'logs')

        self['stdout_file'] = os.path.join(self['log_base'], 'stdout.log')
        self['stderr_file'] = os.path.join(self['log_base'], 'stderr.log')



    def prepare(self):
        local('mkdir -p %s' % self['log_base'])
        if 'stdout_file' not in self:
            self.config['stdout_file'] = os.path.join(self['log_path'], "%s.out" % self['name'])
        if 'stderr_file' not in self:
            self.config['stderr_file'] = os.path.join(self['log_path'], "%s.err" % self['name'])

        pass
        # self.env_vars["RABBITMQ_CONFIG_FILE"] = config_file

        # for d in [self.mnesia_base, self.log_base]:
        #     local('mkdir -p %s' % d)

        # handle, config_file = tempfile.mkstemp(prefix='rabbitmq_config')
        # tpl = Template(open(self.config_template, 'r').read())

        # os.write(handle, tpl.render(
            # ))
