import os

from fabric.api import *
from fabric.context_managers import *

from .SupervisorJob import SupervisorJob



class RabbitMQ(SupervisorJob):
    """docstring for RabbitMQ"""

    def __init__(self, config):
        """ The following configurations are required:
            - name: job name, as used by Supervisor to uniquely identify the job
                e.g. "mq"    (default: "rabbitmq")


            - cmd_base: Directory containing the RabbitMQ binary
                e.g. "/usr/local/bin"

            - ip: Hostname where RabbitMQ will be bound to
                e.g. "127.0.0.1"      (default: "127.0.0.1")

            - port: TCP port where RabbitMQ will be listening to:
                e.g. 5601             (default: 5672)

            - stdout_file: Full path to the file where stdout will be dumped to by
                Supervisor
                e.g. "/home/es/logs/es.out"   (default: <base_dir>/logs/<name>.out)

            - stderr_file: Full path to the file where stderr will be dumped to by
                Supervisor
                e.g. "/home/es/logs/es.out"   (default: <base_dir>/logs/<name>.err)
        """
        super(RabbitMQ, self).__init__(config)

        if 'name' not in self:
            self['name'] = 'rabbitmq'

        if 'ip' not in self:
            self['ip'] = '127.0.0.1'

        if 'port' not in self:
            self['port'] = 5672





    def prepare(self):
        base_dir                  = self.config['base_dir']

        self['mnesia_base']  = os.path.join(base_dir, 'db')
        self['plugins_base'] = os.path.join(base_dir, 'plugins')
        self['log_path']     = os.path.join(base_dir, 'logs')

        for d in ['log_path', 'mnesia_base']:
            local('mkdir -p %s' % self[d])

        if 'stdout_file' not in self:
            self.config['stdout_file'] = os.path.join(self['log_path'], "%s.out" % self['name'])
        if 'stderr_file' not in self:
            self.config['stderr_file'] = os.path.join(self['log_path'], "%s.err" % self['name'])


        # self.env_vars["RABBITMQ_CONFIG_FILE"] = config_file

        self.add_env("RABBITMQ_MNESIA_BASE", self['mnesia_base']),
        self.add_env("RABBITMQ_LOG_BASE", self['log_path']),
        self.add_env("RABBITMQ_NODE_IP_ADDRESS", self['ip']),
        self.add_env("RABBITMQ_NODE_PORT", self['port'])
            # "RABBITMQ_ENABLED_PLUGINS_FILE" : "/etc/rabbitmq/enabled_plugins"


        self['cmd'] = os.path.join(self['cmd_base'], 'rabbitmq-server')

        # handle, config_file = tempfile.mkstemp(prefix='rabbitmq_config')
        # tpl = Template(open(self.config_template, 'r').read())

        # os.write(handle, tpl.render(
            # ))
