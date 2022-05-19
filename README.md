# Calculate DSM and DEM rasters from 3D point clouds

Small program that uses pdal in python to convert 3D point clouds to dsm and dem raster files with the same mission boundaries and row/column count.

## Installation
Download and save in a project directory the files calculate_dsm_dem.py, ground_filter.json, missionbounds.json and requirements_pdal_env.txt. 
Important: all files need to be in the same directory.

Package requirements for calculate_dsm_dem.py are listed in the requirements_pdal_env.txt file. 
The easiest way to run calculate_dsm_dem.py is to firest create a new python environment using the requirements_pdal_env.txt file. 
To create a new envrionment use either conda or virtual envrionment and pip:

1) conda create --name <env> --file requirements_pdal_env.txt
2) create and switch to a new virtual environment, then do pip install -r requirements_pdal_env.txt

## Usage
The program expects to find the following files and folder structure in the active working directory:
  \inputs
  \outputs_dsm
  \outputs_dem
  ground_filter.json
  missionbounds.json

All 3D point cloud files need to be in format .las and stored in the inputs folder. If the program can't find any .las files in inputs or the inputs folder itself doesn't exist, 
it will raise an error. If the outputs folders don't exists they will be automatically created by the program.
  
When executed, calculate_dsm_dem.py will iterate through all .las files stored in \inputs and calculate dsm and dem rasters for each .las file which are stored 
in the outpus folders. Several parameters can be modified inside the .py file to optimize the dsm and dem calculation (a parameter list will soon be added to the README.txt)
  
