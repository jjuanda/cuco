import os

from fabric.api import *
from fabric.context_managers import *

from .SupervisorJob import SupervisorJob



class RabbitMQ(SupervisorJob):
    """docstring for RabbitMQ"""

    def __init__(self, cmd_base, base_path, ip = "127.0.0.1", port = 5672):
        self.cmd_base    = cmd_base
        self.base_path   = base_path
        self.ip          = ip
        self.port        = port
        
        cmd         = os.path.join(self.cmd_base, 'rabbitmq-server')

        self.mnesia_base = os.path.join(self.base_path, 'db')
        plugins_base     = os.path.join(self.base_path, 'plugins')
        self.log_base    = os.path.join(self.base_path, 'logs')
        
        envs             = {
            
            "RABBITMQ_MNESIA_BASE"          : self.mnesia_base,
            "RABBITMQ_LOG_BASE"             : self.log_base,
            "RABBITMQ_NODE_IP_ADDRESS"      : self.ip,
            "RABBITMQ_NODE_PORT"            : self.port
            # "RABBITMQ_ENABLED_PLUGINS_FILE" : "/etc/rabbitmq/enabled_plugins"
        }



        super(RabbitMQ, self).__init__(envs, self.base_path, cmd, "rabbitmq")
        


    def prepare(self):
        # self.env_vars["RABBITMQ_CONFIG_FILE"] = config_file

        for d in [self.mnesia_base, self.log_base]:
            local('mkdir -p %s' % d)

        # handle, config_file = tempfile.mkstemp(prefix='rabbitmq_config')
        # tpl = Template(open(self.config_template, 'r').read())

        # os.write(handle, tpl.render(
            # ))
