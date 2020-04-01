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
    
To automatically save your jupyter notebook in 'ipynb', 'html', and as a script of the language you are using (e.g. 'py', 'r', ...), create a configuration file for jupyter:

    jupyter notebook --generate-config

And add the following script to the config file just created (in my case, named: .jupyter/jupyter_notebook_config.py):

    import os
    from subprocess import check_call

    c = get_config()

    def post_save(model, os_path, contents_manager):
    """post-save hook for converting notebooks to .py and .html files."""
    	if model['type'] != 'notebook':
            return # only do this for notebooks
    	d, fname = os.path.split(os_path)
        check_call(['ipython', 'nbconvert', '--to', 'script', fname], cwd=d)
        check_call(['ipython', 'nbconvert', '--to', 'html', fname], cwd=d)

    c.FileContentsManager.post_save_hook = post_save

## 3. R

Some packages you may want to add to your R:

     install.packages(c('repr', 'IRdisplay', 'evaluate', 'crayon', 'pbdZMQ', 'devtools', 'uuid', 'digest', 'caret', 'e1071', 'ISLR','rpart','rpart.plot','tree','arules','arulesViz','tidyverse','randomForest'))

To install keras on R:

     install.packages("keras")

     library(keras)

     install_keras(method = "conda")

## 4. Sqlitestudio

To download sqlitestudio, visit:

    https://sqlitestudio.pl/index.rvt?act=download

To install it on ubuntu 18.04, go to the folder where you downloaded the installer and:

    chmod +x InstallSQLiteStudio-3.2.1

    ./InstallSQLiteStudio-3.2.1

To run sqlite studio from the terminal:

    /opt/SQLiteStudio/sqlitestudio
   
## 5. VirtualBox

Since I have a dual boot (I have both Ubuntu and Windows) I required the steps explained in the following forum to make VirtualBox working:

    https://superuser.com/questions/1438279/how-to-sign-a-kernel-module-ubuntu-18-04
    
Summarizing:

In order to get VirtualBox working without simply disabling UEFI Secure Boot, then you'll need to do the following:


1. Create a personal public/private RSA key pair to sign the kernel modules. As recommended in the link below, I chose to store the key/pair in the /root/module-signing/ directory.

    sudo -i
    mkdir /root/module-signing
    cd /root/module-signing
    openssl req -new -x509 -newkey rsa:2048 -keyout MOK.priv -outform DER -out MOK.der -nodes -days 36500 -subj "/CN=YOUR_NAME/"
    chmod 600 MOK.priv 
    
    
2. Use mokutil, a tool to import or delete the machine owner keys (MOK), to import the public key, and then enroll it when the machine is rebooted. The password in this step is a temporary use password you'll only need to remember for a few minutes.

    mokutil --import /root/module-signing/MOK.der
    input password:
    input password again:



3. Reboot the machine. When the bootloader starts, you should see a screen asking you to press a button to enter the MOK manager EFI utility. Note that any external external keyboards won't work in this step. Select Enroll MOK in the first menu, then continue, and then select Yes to enroll the keys, and re-enter the password established in step 2. Then select OK to continue the system boot.

4. Future kernel updates would require the updated kernels to be signed again, so it makes sense to put the signing commands in a script that can be run at a later date as necessary. A sample script /root/module-signing/sign-vbox-modules is given below.

    #!/bin/bash

    for modfile in $(dirname $(modinfo -n vboxdrv))/*.ko; do
        echo "Signing $modfile"
        /usr/src/linux-headers-$(uname -r)/scripts/sign-file sha256 \
                                /root/module-signing/MOK.priv \
                                /root/module-signing/MOK.der "$modfile"
    done

5. Add execution permission, and run the script above as root from the /root/module-signing/ directory.

    sudo -i
    cd /root/module-signing
    chmod 700 /root/module-signing/sign-vbox-modules
    ./sign-vbox-modules
    
6. Load vboxdrv module and launch VirtualBox.

    modprobe vboxdrv 
