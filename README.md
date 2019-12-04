SOME USEFUL COMMANDS
====================

## 1. Conda

To install, visit https://docs.conda.io/en/latest/miniconda.html and download the package that fits your operative system, then (in case of MacOSX):

    bash Miniconda2-latest-MacOSX-x86_64.sh

To update:

    conda update conda

To keep conda activated when you open a new terminal, add this line to your .bashrc file:

    export PATH=/home/nicolo/miniconda3/bin/:$PATH

To list all the installed packages:

    conda list

To install new packages:

    conda install <package>

To create a python2 environment:

    conda create -n py2 python=2
   
    conda activate py2

To go back to 'base' environment:

    conda deactivate

To create an environment with r:

    conda create -n Estadistica --channel r r-base

    conda activate Estadistica

To install a Jupyter notebook on conda:

    conda install jupyter

To install m2-base:

    conda install -c msys2 m2-base

## 2. Jupyter

To launch jupyter:

    jupyter console

To open a jupyter notebook, enter the directory where your notebook is stored and use the following command:

    jupyter notebook

To see the list of jupyter notebooks open:

    jupyter notebook list
    
To install R kernel on Jupyter (reference: https://irkernel.github.io/installation/):
    
    install.packages('IRkernel')
    
    IRkernel::installspec()

or, to install for all the users of the system: 

    IRkernel::installspec(user = FALSE)
    

