# PysparkEnv
Helper classes to run Pyspark with a virtual environment

When running code on Pyspark that depends on multiple libraries it could be hard to ship all the libraries using the SparkContext.
This code ships a tarball containing a venv to all the nodes and then sets the env on the node to use it.
This makes is easier to use PySpark with a virtual environment.

Example:
```python
local_location_venvtarball = '/tmp/venv.tar.gz' # available only local no need to have it on the nodes
venv_name = 'venv' # name of the venv when unzipped
with SparkVirtualEnvContext('applecation_name', virtual_env_tarball_file=local_location_venvtarball, venv_name=venv_name) as sc: #
        
        @virtualenv(sc.venv_name) #enable the venv on the node
        def computation(data):
            import sklearn  #the import statements need to be inside the method decorated with "virtualenv"
            return 1
       
        result = sc.parallelize([ 1, 2, 3 ,4]).map(computation).count()
```