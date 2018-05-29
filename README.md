# json2gdx
Creates a GAMS (gdx) database file from a json formatted input file. Currently only writes sets and parameters (including scalars) to a gdx file (not equations or variables).

# Requirements
Python 3, GAMS API (high level)

# Use
python3 json2gdx.py --in=inputfilename.json --out=outputfilename.gdx

Output filename is optional, default is 'data.gdx'.

# Structure
The example json file was created with gdx2json and can be read directly with json2gdx to create a GAMS (gdx) file.  The example json file was created from a solution to the ubiquitous 'trnsport.gms' model from the GAMS model library. The user is advised to use gdxdump (from GAMS) in order to view the contents of the newly created gdx file.




