# PysparkEnv
Helper classes to run Pyspark with a virtual environment

When running code on Pyspark that depends on multiple libraries it could be hard to ship all the libraries using the SparkContext.
Moreover with multiple users on a cluster, there might be conflicts between versions of libraries required by each user.

This code ships a tarball containing a venv to all the nodes and then sets the env on the node to use it.
This makes is easier to use PySpark with a virtual environment.

Example:
```python
from pysparkvenv import SparkContextVenv, virtualenv
venvtarball_file = '/tmp/venv.tar.gz' # available only local no need to have it on the nodes
venv_name = 'venv' # name of the venv when unzipped

env_variables_dict = {'LD_LIBRARY_PATH': '/home/user/lib'} # if env variables need to be set on the nodes

with SparkContextVenv('application_name', virtual_env_tarball_file=venvtarball_file, venv_name=venv_name, env_variables_dict=env_variables_dict) as sc: #
        
        @virtualenv(sc.venv_name) #enable the venv on the node
        def computation(data):
            import sklearn  #the import statements need to be inside the method decorated with "virtualenv"
            return 1
       
        result = sc.parallelize([ 1, 2, 3 ,4]).map(computation).count()
```