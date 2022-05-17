import pdal
import json
import os
import re
import os

# Check if inputs folder exists, if not raise exception.

if not os.path.isdir("inputs"):
    raise Exception("No 'inputs' folder found."
    " Please create an 'inputs' folder in the current working directory and add the .las files that are to be processed."
    " Current working directory: %s" % os.getcwd())

# Check if output folders exist, if not they are created.
f_list = ["output_dsm", "output_dem"]
for f in f_list:
    if not os.path.isdir(f):
        os.makedirs(f)
        print("created folder: ", f)
    else:
        print(f, "folder exists.")

# Read las files from inputs folder that should be converted into dem and dsm.
# Raise exception if no .las files in inputs folder.
path = "inputs"
las_file_list = []
for f in os.listdir(path):
    if f.endswith(".las"):
        las_file_list.append(f)
print(las_file_list)

if len(las_file_list) == 0:
    raise Exception("'inputs' folder contains no files with ending .las."
    " Please add to 'inputs' folder .las files that are to be processed.")

# open json file with the pipeline that holds all the stages (processes)
# that should be applied to the las files via pdal
json_filename = "get_missionbounds"
with open ("%s.json" % json_filename, "r") as read_file:
    filter_dict = json.load(read_file)

    # Iterate through files in las_file_list and create dem for each file
    i = 0
    bounds = []
    for file in las_file_list:
        # update the input and output filename in the pipeline and rewrite it as json file
        filter_dict["pipeline"][0]["filename"] = "1point_clouds/input_part/%s" % file
        json_format = json.dumps(filter_dict, indent=4)

        # pass the json file to the pdal pipeline and process the las files
        pipeline = pdal.Pipeline(json_format)
        count = pipeline.execute()
        metadata = pipeline.metadata

        bound_index = [metadata.find("maxx"), metadata.find("maxy"), metadata.find("maxz"), metadata.find("minx"), metadata.find("miny"), metadata.find("minz")]
        minx_string = str(metadata[bound_index[3]:bound_index[4]])
        maxx_string = str(metadata[bound_index[0]:bound_index[1]])
        miny_string = str(metadata[bound_index[4]:bound_index[5]])
        maxy_string = str(metadata[bound_index[1]:bound_index[2]])

        minx = re.search('([0-9]+)(.)([0-9]+)', minx_string).group()
        maxx = re.search('([0-9]+)(.)([0-9]+)', maxx_string).group()
        miny = re.search('([0-9]+)(.)([0-9]+)', miny_string).group()
        maxy = re.search('([0-9]+)(.)([0-9]+)', maxy_string).group()
        bound = "([%s, %s], [%s, %s])" % (minx, maxx, miny, maxy)
        bounds.append(bound)
        print(bounds)

# open json file with the pipeline that holds all the stages (processes)
# that should be applied to the las files via pdal
json_filename = "ground_filter"
with open ("%s.json" % json_filename, "r") as read_file:
    filter_dict = json.load(read_file)
    # Iterate through files in las_file_list and create dem for each file
    i = 0
    for file in las_file_list:
        # update the input and output filename in the pipeline and rewrite it as json file

        # reading pointcloud file
        filter_dict["pipeline"][0]["filename"] = "1point_clouds/input_part/%s" % file
        # setting parameters for morphological filter (smrf)
        filter_dict["pipeline"][5]["slope"] = 0.05
        filter_dict["pipeline"][5]["window"] = 17
        filter_dict["pipeline"][5]["threshold"] = 0.35
        filter_dict["pipeline"][5]["scalar"] = 0.9
        filter_dict["pipeline"][5]["cell"] = 0.4
        #writitng dsm.tif
        filter_dict["pipeline"][6]["filename"] = "2dsm/%s2_pdal_dsm.tiff" % file[:16]
        filter_dict["pipeline"][6]["output_type"] = "mean"
        filter_dict["pipeline"][6]["resolution"] = "0.05"
        # writing dem.tif
        print(file[:16])
        filter_dict["pipeline"][8]["filename"] = "3dem/%s2_pdal_dem.tiff" % file[:16]
        filter_dict["pipeline"][8]["output_type"] = "mean"
        filter_dict["pipeline"][8]["resolution"] = "0.05"
        filter_dict["pipeline"][8]["bounds"] = bounds[i]

        print("bound pipeline 2: ")
        print(bounds[i])

        # transform dictionary to json file to pass it to the pdal pipeline
        json_format = json.dumps(filter_dict, indent=4)

        # pass the json file to the pdal pipeline and process the las files
        pipeline = pdal.Pipeline(json_format)
        count = pipeline.execute()
        arrays = pipeline.arrays
        metadata = pipeline.metadata

        i += 1
        # print(arrays[:2])

        # transform json file back to dictionary so it can be modified
        filter_dict = json.loads(json_format)

        # activate in case one wants to save the json file with the updated filename
        # with open("%s_%s" % (json_filename, str(i)), "w") as outfile:
        #     json.dump(filter_dict, outfile)
