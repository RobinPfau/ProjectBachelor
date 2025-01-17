WINDOWS:

#Install Python version <=3.12 and add to path:
https://www.python.org/downloads/

#Install Git https://github.com/git-for-windows/git/releases/download/v2.47.1.windows.1/Git-2.47.1-64-bit.exe

#create folder for project

#in Linux, tkinter needs to be installed:
sudo apt-get install python3-tk

#(optional)create new Virtual environment in your folder:
python -m venv venv

#activate:
venv\scripts\activate

#install projectBachelor:
pip install git+https://github.com/RobinPfau/ProjectBachelor

#run app:
str8ts


___________________________

#if no git installed (not recommended)
#download and unpack next to venv from https://github.com/RobinPfau/ProjectBachelor
pip install setuptools

#in venv run:
python setup.py sdist bdist_wheel

#install app:
pip install .

#run app
str8ts

___________________________

should work on other os aswell
