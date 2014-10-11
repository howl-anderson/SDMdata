Install
===
SDMdata was written in python but also used other library.

Currently there is only one library that setup script cannot install: GDAL.

## Install GDAL
GDAL is a widely used geospatial library. How to install it will depend on user's operation system. see [GDAL office page](http://trac.osgeo.org/gdal/wiki/DownloadingGdalBinaries) for specific information. 

Here, we only introduce two most popular package manage tool: Debian-based APT and redhat-based yum:

1. For APT user:

	sudo apt-get install gdal
	
2. For YUM user:

	sudo yum install gdal 
	
## Install other depend python library
Our `setup.py` is install tools for python library. Just run `./setup.py test` all depends will automatic installed.