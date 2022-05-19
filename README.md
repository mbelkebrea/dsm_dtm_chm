# Calculate DSM and DEM rasters from 3D point clouds

Small program that uses pdal in python to convert 3D point clouds to dsm and dem raster files with the same mission boundaries and row/column count.

## Installation
Download and save in a project directory the files calculate_dsm_dem.py, ground_filter.json, get_missionbounds.json and requirements_pdal_env.txt. 
Important: all files need to be in the same directory.

Package requirements for calculate_dsm_dem.py are listed in the requirements_pdal_env.txt file. 
The easiest way to run calculate_dsm_dem.py is to firest create a new python environment using the requirements_pdal_env.txt file. 
To create a new environment navigate to the directory containing the requirements_pdal_env.txt and use either conda or virtual envrionment and pip:

1) _conda create --name new_env_name --file requirements_pdal_env.txt_
2) create and switch to a new virtual environment, then do _pip install -r requirements_pdal_env.txt_

## Usage
In the Anaconda prompt, navigate to the directory containing calculate_dsm_dem.py and activate the new envrionment (e.g. using _conda activate new_env_name_), then execute the program with: _python calculate_dsm_dem.py_

The program expects to find the following files and folder structure in the active working directory: <br>
  \inputs <br>
  \outputs_dsm <br>
  \outputs_dem <br>
  ground_filter.json <br>
  get_missionbounds.json <br>

All 3D point cloud files need to be in format .las and stored in the inputs folder. If the program can't find any .las files in inputs or the inputs folder itself doesn't exist, it will raise an error. If the outputs folders don't exists they will be automatically created by the program.
  
When executed, calculate_dsm_dem.py will iterate through all .las files stored in \inputs and calculate dsm and dem rasters for each .las file which are then stored 
in the outpus folders. Several parameters can be modified inside the .py file to optimize the dsm and dem calculation (a parameter list will soon be added to the README.txt)
  
