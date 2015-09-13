import tempfile
import os

from jinja2 import Template
from fabric.api import *
from fabric.context_managers import *


class SupervisorApp(object):
    """docstring for SupervisorApp"""

    def __init__(self, log_file="logs/supervisord.log", pidfile="supervisord.pid", http_port=9920):
        super(SupervisorApp, self).__init__()

        self.log_file  = log_file
        self.http_port = http_port
        self.pidfile   = pidfile
        self.jobs      = []
        
    def add(self, job):
        self.jobs.append(job)

    def run(self):
        handle, config_file = tempfile.mkstemp(prefix='supervisord_config')
        print("Starting job:")
        print(" - Config: %s" % config_file)

        config = """[supervisord]
logfile          = {{log_file}}
logfile_maxbytes = 50MB
logfile_backups  = 10
loglevel         = info
pidfile          = {{pidfile}}
nodaemon         = True
minfds           = 1024
minprocs         = 200
umask            = 022
identifier       = supervisor
directory        = /tmp
nocleanup        = true
childlogdir      = /tmp


[inet_http_server]
port     = 0.0.0.0:{{http_port}}
username = user
password = pass


"""

        env = Template(config)

        os.write(handle, env.render({
            "log_file"  : self.log_file,
            "http_port" : self.http_port,
            "pidfile"   : self.pidfile
        }))

        for job in self.jobs:
            job.prepare()

            config = """[program:{{program_name}}]
command     = {{cmd}}
directory   = {{base_dir}}
autostart   = true
autorestart = true
stopsignal  = KILL
killasgroup = true
stopasgroup = true
environment = {{env}}


"""

            env = Template(config)

            os.write(handle, env.render({
                "program_name" : job.name,
                "base_dir"     : job.base_dir,
                "env"          : job.get_env_str(),
                "cmd"          : job.cmd
            }))


        os.close(handle)

        local("supervisord -c %s" % config_file)

