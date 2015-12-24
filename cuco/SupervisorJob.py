from jinja2 import Template


class SupervisorJob(object):
    """docstring for SupervisorJob"""

    def __init__(self, config):
        """ Specify the configuration options for a job.
            'config' must be a dictionary containing the following keys:
            - env_vars: dict containing the key/value pairs to be specified as
                environment variables
                e.g. {"ES_HOME" : "/home/es"}

            - name: job name, as used by Supervisor to uniquely identify the job
                e.g. "elasticsearch"

            - base_dir: Base directory for the supervisor job
                e.g. "/home/es"

            - cmd: Full command (with args) that supervisor will run
                e.g. "elasticsearch -p /home/es/es.pid"

            - stdout_file: Full path to the file where stdout will be dumped to by
                Supervisor
                e.g. "/home/es/logs/es.out"

            - stderr_file: Full path to the file where stderr will be dumped to by
                Supervisor
                e.g. "/home/es/logs/es.err"

        """
        super(SupervisorJob, self).__init__()

        self.config = config
        self['env_vars'] = config.get('env_vars', {})

        # self.env_vars    = env_vars
        # self.base_dir    = base_dir
        # self.cmd         = cmd
        # self.name        = name
        # self.stdout_file = stdout_file
        # self.stderr_file = stderr_file

    def prepare(self):
        raise NotImplementedError("base class")

    def __getitem__(self, k):
        return self.config[k]

    def __setitem__(self, k, v):
        self.config[k] = v

    def __contains__(self, k):
        return k in self.config

    def add_env(self, k, v):
        self['env_vars'][k] = v

    def as_supervisor_program(self):
        config = """[program:{{program_name}}]
command     = {{cmd}}
directory   = {{base_dir}}
autostart   = true
autorestart = true
stopsignal  = KILL
killasgroup = true
stopasgroup = true
environment = {{env}}
stdout_logfile = {{stdout}}
stderr_logfile = {{stderr}}


"""

        env = Template(config)

        return env.render({
            "program_name" : self.config['name'],
            "base_dir"     : self.config['base_dir'],
            "env"          : self.get_env_str(),
            "cmd"          : self.config['cmd'],
            "stdout"       : self.config['stdout_file'],
            "stderr"       : self.config['stderr_file'],
        })

    def as_exports(self):
        res = ""
        for k, v in self['env_vars'].items():
            res += "export %s=%s\n" % (k, v)
        return res

    def get_env_str(self):
        return ", ".join([k + "=\"" + str(v) + "\"" for k,v in self['env_vars'].items()])
