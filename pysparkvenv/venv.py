import os
from pyspark import SparkContext, SparkConf, SparkFiles

class SparkContextVenv(SparkContext):
    def __init__(self,app_name, virtual_env_tarball_file=None, venv_name=None, python_path='/usr/bin/python2.7', env_variables_dict=None):

        assert os.path.isfile(python_path)

        if virtual_env_tarball_file:
            assert os.path.isfile(virtual_env_tarball_file)
            self.virtual_env_tarball_file = virtual_env_tarball_file
            if not venv_name:
                self.venv_name = os.path.basename(virtual_env_tarball_file).split('.')[0] #this assumes that the name of the tarball is the same of the folder stored inside
            else:
                self.venv_name = venv_name
        else:
            self.virtual_env_tarball_file = None
            self.venv_name = None


        self.python_path = python_path
        self.sc = None

        os.environ['PYSPARK_PYTHON'] = self.python_path
        conf = SparkConf()
        self.env_variables_dict = env_variables_dict
        if env_variables_dict:
            for key, value in env_variables_dict.iteritems():
                print 'setting env: {} with value: {}'.format(key, value)
                conf.setExecutorEnv(key=key, value=value)
        super(SparkContextVenv, self).__init__(appName=app_name, conf=conf)
        if self.virtual_env_tarball_file:
            self.addFile(self.virtual_env_tarball_file)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

def virtualenv(venv_name):
  def wrap(f):
    def wrapped_f(*args, **kwargs):
        venv_location = SparkFiles.get(venv_name)
        print 'called wrapped_f for virtual env in {}'.format(venv_location)
        activate_env="%s/bin/activate_this.py" % venv_location
        execfile(activate_env, dict(__file__=activate_env))

        import sys
        numpy_mods = [item for item in sys.modules if ('numpy' in item or 'scipy' in item)]
        for mod in numpy_mods:
            sys.modules.pop(mod)

        return f(*args, **kwargs)
    return wrapped_f
  return wrap

