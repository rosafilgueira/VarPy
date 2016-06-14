# VarPy: A python library for volcanic and rock physics data analysis


VarPy is an open-source toolbox which provides a
Python framework for analysing volcanology and rock physics
data. It provides several functions, which allow users to define
their own workflows to develop models, analyses and visualisations.
The goal of the VarPy library is to accelerate the uptake
of computational methods by researches in volcanology and rock
physics. 

In this repository you can find:

- Reading material about VarPy Library presented at two conferences: [Slides for the conference EGU2014](https://github.com/rosafilgueira/VarPy/blob/master/VarPy_EGU2014.pdf), [Paper presented at PyHPC2014](https://github.com/rosafilgueira/VarPy/blob/master/pyhpc2014_submission_4.pdf), and [Slides used at the conference PyHPC2014](https://github.com/rosafilgueira/VarPy/blob/master/pyhpc2014-4-VarPy.pdf)

- Source code: [varpy modules and packages](https://github.com/rosafilgueira/VarPy/tree/master/varpy).
Note that the paper [Paper-PyHPC2014](https://github.com/rosafilgueira/VarPy/blob/master/pyhpc2014_submission_4.pdf) contains the complete
structure of the VarPy library (*Section V. VarPy Packages and Modules*).

- Some datasets (Data and Library directories) to work later with VarPy examples (python scripts and notebook)

- Several [python examples](https://github.com/rosafilgueira/VarPy/blob/master/python_scripts) for explaining how to use varpy library 
	- [retrospective analysis 1](https://github.com/rosafilgueira/VarPy/blob/master/python_scripts/varpy_modelworkflow1a.py), [retrospective analysis 2](https://github.com/rosafilgueira/VarPy/blob/master/python_scripts/varpy_modelworkflow2a.py)
	- [single forecast 1](https://github.com/rosafilgueira/VarPy/blob/master/python_scripts/varpy_modelworkflow1b.py), [single forecast 2](https://github.com/rosafilgueira/VarPy/blob/master/python_scripts/varpy_modelworkflow2b.py)
	- [retrospective forecast 1](https://github.com/rosafilgueira/VarPy/blob/master/python_scripts/varpy_modelworkflow1c.py), [retrospective forecast 2](https://github.com/rosafilgueira/VarPy/blob/master/python_scripts/varpy_modelworkflow2c.py)
	- [prospective forecast 1](https://github.com/rosafilgueira/VarPy/blob/master/python_scripts/varpy_modelworkflow1d.py), [retrospective forecast 2](https://github.com/rosafilgueira/VarPy/blob/master/python_scripts/varpy_modelworkflow2d.py) 

- A python [Notebook example](https://github.com/rosafilgueira/VarPy/blob/master/Iceland_Tjornes.ipynb),
which shows how VarPy can facilitate the data exploration and visualization on the Tjornes fracture zone (Iceland).
This example is explained across the reading material provided in this repository (paper and slides). 

For trying a varpy example (python script or notebook):

	1) Clone the VarPy repository in your machine
	2) Add the VarPy repository path into the PYTHONPATH (e.g., export PYTHONPATH=/Users/rosa/VarPy)

	3a) Execute any of the scripts inside the directory 'python_scripts':
                python VarPy_Hierro_Ex1.py
	
	3b) Or execute ipython notebook to open Iceland_Tjornes.ipynb 
