

class SupervisorJob(object):
    """docstring for SupervisorJob"""

    def __init__(self, env_vars, base_dir, cmd, name):
        super(SupervisorJob, self).__init__()
        
        self.env_vars = env_vars
        self.base_dir = base_dir
        self.cmd      = cmd
        self.name     = name

    def prepare(self):
        raise NotImplementedError("base class")

    def get_env_str(self):
        return ", ".join([k + "=\"" + str(v) + "\"" for k,v in self.env_vars.items()])
