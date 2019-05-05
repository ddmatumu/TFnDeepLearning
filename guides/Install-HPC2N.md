# Installation at HPC2N 
(backup resource in case Google CoLab or your own Jupyter Lab does not work)
## 01. Preparations
- Make sure you have an account in both SUPR and HPC2N. This should already have been taken care of, but otherwise follow 
this guide: [Applying for a user account](https://www.hpc2n.umu.se/documentation/access-and-accounts/users)
- Create a new temporary password: [Set password](https://www.hpc2n.umu.se/access/login#forgotten-password)
- When you have logged in to one of HPC2N's clusters (Abisko and Kebnekaise), you should change your password to something that 
is easier to remember. See how here: [First Time Login / Password Change](https://www.hpc2n.umu.se/access/login#first-login)
## 02. Login to HPC2N's cluster 'Kebnekaise' (with x11 forwarding, enabling you to open GUIs, should you need to). 
### Linux
- ssh -Y yourusername@kebnekaise.hpc2n.umu.se
### Windows
- [Connecting from Windows](https://www.hpc2n.umu.se/documentation/guides/windows-connection)  
### MacOS
- ssh -l username kebnekaise.hpc2n.umu.se 
- If you need to open displays from the remote host on your local machine, then make sure [XQuartz](https://www.xquartz.org/) is installed. 
## 03. Setting up the environment
We recommend using the modules and Python virtualenv, but using Anaconda is also possible. 
### 01. Python and Virtualenv
#### Load some needed modules
- ml GCC/7.3.0-2.30  CUDA/9.2.88  OpenMPI/3.1.1 
- ml Python/3.6.6
- ml TensorFlow/1.12.0-Python-3.6.6
#### Setup your virtual environment
- Create your first virtual environment. Here I call it 'vpyenv', and put it in my pfs, but you can call it anything, of course. Run the following to initialize the environment:
- virtualenv --system-site-packages $HOME/pfs/vpyenv
#### Activate the virtual environment
- Change directory to the environment you created before: cd $HOME/pfs/vpyenv
- And run: source bin/activate
- You can later deactivate it with: deactivate
#### Install some Python packages 
- You can now install python modules like this: pip install --no-cache-dir <python-package> 
-- In our case we have several to install. Please download this file with requirements:[hpc2n-course-req.txt](https://github.com/ddmatumu/TFnDeepLearning/blob/master/hpc2n-course-req.txt). 
- pip install --no-cache-dir -r hpc2n-course-req.txt

ETNLP: 
Download from [ETNLP homepage](https://github.com/vietnlp/etnlp#installation_and_howtouse)
Either git clone or unzip, then enter directory created. 
Go to src/codes under the ETNLP directory. 
python setup.py install
