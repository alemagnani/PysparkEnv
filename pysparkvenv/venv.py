import os
from pyspark import SparkContext, SparkConf, SparkFiles

class SparkContextVenv(SparkContext):
    def __init__(self,app_name, virtual_env_tarball_file, venv_name=None, python_path='/usr/bin/python2.7'):
        assert os.path.isfile(virtual_env_tarball_file)
        assert os.path.isfile(python_path)
        self.virtual_env_tarball_file = virtual_env_tarball_file
        self.python_path = python_path
        self.sc = None
        if not venv_name:
            self.venv_name = os.path.basename(virtual_env_tarball_file).split('.')[0] #this assumes that the name of the tarball is the same of the folder stored inside
        else:
            self.venv_name = venv_name

        os.environ['PYSPARK_PYTHON'] = self.python_path
        conf = SparkConf()
        super(SparkContextVenv, self).__init__(appName=app_name, conf=conf)
        self.addFile(self.virtual_env_tarball_file)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

def virtualenv(venv_name):
  def wrap(f):
    def wrapped_f(*args, **kwargs):
        print 'called wrapped_f'
        venv_location = SparkFiles.get(venv_name)
        activate_env="%s/bin/activate_this.py" % venv_location
        execfile(activate_env, dict(__file__=activate_env))
        return f(*args, **kwargs)
    return wrapped_f
  return wrap
