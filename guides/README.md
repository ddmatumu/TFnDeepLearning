
# I. Installation:
## 1. Install Jupyter Lab:
### 1.1. For Unix/Linux users: choose *ONE* of following options.
#### 01. Anaconda (recommended, read more [here](https://www.anaconda.com/) if you haven't used Anaconda before.)
Create a new python environment called *tf_n_dl* (or activate your current in-use environment)
> conda create -n tf_n_dl python=3.6<br>
> conda activate tf_n_dl<br>
> conda install -c conda-forge jupyterlab
#### 02. pip (directly to your default python environment)
> pip install jupyterlab
#### 03. pipenv (read more [here](https://github.com/pypa/pipenv))
> pipenv install jupyterlab<br>
> pipenv shell
### 1.2. For Windows users: see this instructions. 

## 2. Starting JupyterLab
Active your python environment and simply type this following command using the console:
> jupyter lab --ip=127.0.0.1

JupyterLab will open automatically in the browser with an interface resembling the one below.

![](https://cdn-images-1.medium.com/max/800/1*xo8LGAaxdBCKFQVFb8ZQ3g.png)

** Read more about Jupyter Lab and its advantages at this 
[link](https://towardsdatascience.com/jupyter-lab-evolution-of-the-jupyter-notebook-5297cacde6b?fbclid=IwAR3O0QkkhCwK1BBJM6akHOhcdM_ZtvgcrHzCYrJj3dJ3IvVS3gk6TSziuTk).

## 3. Install required packages:
1. In the menu of *Jupyter Lab*, click File -> New -> Terminal. Make sure your current active python environment is *tf_n_dl* (the ENV name will appear at the beginning of the command prompt).
2. Clone the github repo of this course:
> git clone https://github.com/ddmatumu/TFnDeepLearning.git
3. Go to the repo and install requirements:
> cd TFnDeepLearning; pip install -r requirements.txt

## 4. Install for HPC2N (console):

# II. Test required packages:
 
## 1. With *Jupyter Lab*:
1. On the *Jupyter Lab*, open `codes/Tests/Test_Packages.jpnb`
2. Run the import packages section to see if all packages are installed properly:

3. Congratulation, you're done with the installation part.

## 2. With console on HPC2N:
1. <putting here testing script>