import os
import tempfile

from fabric.api import *
from fabric.context_managers import *
from jinja2 import Template

from .SupervisorJob import SupervisorJob



class ElasticSearch(SupervisorJob):
    """docstring for ElasticSearch"""

    def __init__(self, config):
        """ The following configurations are required:
            - name: job name, as used by Supervisor to uniquely identify the job
                e.g. "elasticsearch"    (default: "elasticsearch")

            - config_template: Full path to the template for a config file to be
                used by elasticsearch during its initialization
                e.g. "/home/es/elasticsearch.yml.tpl"

            - cmd_base: Directory containing the elasticsearch binary
                e.g. "/usr/local/Cellar/elasticsearch/2.1.0_1/bin"

            - host: Hostname where Elasticsearch will be bound to
                e.g. "127.0.0.1"   (default: "127.0.0.1")

            - cluster_name: Cluster name for Elasticsearch
                e.g. "data"

            - stdout_file: Full path to the file where stdout will be dumped to by
                Supervisor
                e.g. "/home/es/logs/es.out"   (default: <base_dir>/logs/<name>.out)

            - stderr_file: Full path to the file where stderr will be dumped to by
                Supervisor
                e.g. "/home/es/logs/es.out"   (default: <base_dir>/logs/<name>.err)
        """
        super(ElasticSearch, self).__init__(config)

        if 'name' not in self:
            self['name'] = 'elasticsearch'

        if 'host' not in self:
            self['host'] = '127.0.0.1'


    def prepare(self):
        base_es                  = self.config['base_dir']
        self.config['log_path']  = os.path.join(base_es, 'logs')
        self.config['data_path'] = os.path.join(base_es, 'data')
        self.config['pid_path']  = os.path.join(base_es, 'es.pid')

        for d in ['log_path', 'data_path']:
            local('mkdir -p %s' % self.config[d])

        if 'stdout_file' not in self:
            self.config['stdout_file'] = os.path.join(self['log_path'], "%s.out" % self['name'])
        if 'stderr_file' not in self:
            self.config['stderr_file'] = os.path.join(self['log_path'], "%s.err" % self['name'])

        temp_path = tempfile.mkdtemp(prefix='es_config')
        print(temp_path)

        self.add_env('ES_HOME', temp_path)

        tpl      = Template(open(self['config_template'], 'r').read())

        es_config = os.path.join(temp_path, 'elasticsearch.yml')
        self['cmd'] = os.path.join(self['cmd_base'], 'elasticsearch') + \
            " -p %s" % self['pid_path']

        open(es_config, 'w').write(tpl.render(self.config))

        # es_config = os.path.join(temp_path, 'elasticsearch.yml')
        # open(es_config, 'w').write(tpl.render(env))
