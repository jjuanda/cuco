import os
import tempfile

from fabric.api import *
from fabric.context_managers import *
from jinja2 import Template

from .SupervisorJob import SupervisorJob



class Kibana(SupervisorJob):
    """docstring for Kibana"""

    def __init__(self, config):
        """ The following configurations are required:
            - name: job name, as used by Supervisor to uniquely identify the job
                e.g. "kibana"    (default: "kibana")

            - config_template: Full path to the template for a config file to be
                used by kibana during its initialization
                e.g. "/home/es/elasticsearch.yml.tpl"

            - cmd_base: Directory containing the kibana binary
                e.g. "/usr/local/Cellar/elasticsearch/2.1.0_1/bin"

            - host: Hostname where Kibana will be bound to
                e.g. "127.0.0.1"      (default: "localhost")

            - port: TCP port where Kibana will be listening to:
                e.g. 5601             (default: 5601)

            - es_host: Host name for the Elasticsearch instance
                e.g. "10.45.23.12"    (default: "localhost")

            - es_port: TCP port for the Elasticsearch instance
                e.g. 1234    (default: 9200)

            - stdout_file: Full path to the file where stdout will be dumped to by
                Supervisor
                e.g. "/home/es/logs/es.out"   (default: <base_dir>/logs/<name>.out)

            - stderr_file: Full path to the file where stderr will be dumped to by
                Supervisor
                e.g. "/home/es/logs/es.out"   (default: <base_dir>/logs/<name>.err)
        """
        super(Kibana, self).__init__(config)

        if 'name' not in self:
            self['name'] = 'kibana'

        if 'port' not in self:
            self['port'] = 5601

        if 'host' not in self:
            self['host'] = 'localhost'

        if 'es_host' not in self:
            self['es_host'] = 'localhost'

        if 'es_port' not in self:
            self['es_port'] = 9200


        envs = {}


    def prepare(self):
        base_dir                  = self.config['base_dir']
        self['log_path']  = os.path.join(base_dir, 'logs')
        self['log_file']  = os.path.join(self['log_path'], 'kibana.log')
        self['pid_file']  = os.path.join(base_dir, 'es.pid')

        for d in ['log_path']:
            local('mkdir -p %s' % self[d])

        if 'stdout_file' not in self:
            self.config['stdout_file'] = os.path.join(self['log_path'], "%s.out" % self['name'])
        if 'stderr_file' not in self:
            self.config['stderr_file'] = os.path.join(self['log_path'], "%s.err" % self['name'])

        handle, config_file = tempfile.mkstemp(prefix='kibana_config')
        print(config_file)

        tpl      = Template(open(self['config_template'], 'r').read())

        self['cmd'] = os.path.join(self['cmd_base'], 'kibana') + \
            " -c %s" % config_file

        os.write(handle, tpl.render(self.config))
        os.close(handle)

        # es_config = os.path.join(temp_path, 'elasticsearch.yml')
        # open(es_config, 'w').write(tpl.render(env))
