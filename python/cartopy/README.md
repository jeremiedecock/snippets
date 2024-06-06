## Libraries to plot cartographic data on top of Matplotlib

Currently, there are 2 main libraries for this task:

- https://matplotlib.org/basemap/users/intro.html
- https://scitools.org.uk/cartopy/

but basemap is a "dead" project:

    "The Cartopy project will replace Basemap, but it hasn’t yet implemented all
    of Basemap’s features. All new software development should try to use
    Cartopy whenever possible, and existing software should start the process
    of switching over to use Cartopy. All maintenance and development efforts
    should be focused on Cartopy."
    
    (src: https://matplotlib.org/basemap/users/intro.html#cartopy-new-management-and-eol-announcement)

## Install

```
apt install libgeos-dev
pip install cartopy
```

## Glossary (TODO)

- GIS softwares
- shapely: a python library
- pyshp (https://github.com/GeospatialPython/pyshp)
- fiona (http://toblerity.org/fiona/)
- geopandas (http://geopandas.org/)
- netCDF format
- Basemap
- Cartopy
- PyNGL (http://www.pyngl.ucar.edu/): an alternative to Basemap
- CDAT (https://pcmdi.llnl.gov/?software/cdat/support/vcs/vcs.html): an alternative to Basemap
- PyNIO (http://www.pyngl.ucar.edu/Nio.shtml): is a Python package that allows read and/or write access to a variety of data formats using an interface modeled on netCDF
- PROJ (https://proj4.org/): a C library to transform coordinates (used by basemap)
- Generic Mapping Tools (GMT) (http://gmt.soest.hawaii.edu/): an open source collection of about 80 command-line tools for manipulating geographic and Cartesian data sets. Provides Shoreline, river and political boundary datasets used by Basemap.
- GSHHG (http://www.soest.hawaii.edu/pwessel/gshhg/):  We present a high-resolution geography data set amalgamated from three data bases in the public domain: World Vector Shorelines (WVS), CIA World Data Bank II (WDBII), Atlas of the Cryosphere (AC). Used by GMT.
- ESRI shapefiles.
- MaxMind GeoIP (https://www.maxmind.com/fr/geoip2-services-and-databases): converts an IP address to a geographical data
- https://epsg.io/ (https://github.com/klokantech/epsg.io)

## Useful documentation:

- https://matplotlib.org/basemap/users/intro.html
- https://scitools.org.uk/cartopy/docs/v0.15/gallery.html
- https://github.com/SciTools/cartopy/issues/384
- https://stackoverflow.com/questions/35707514/download-data-from-natural-earth-and-openstreetmap-for-cartopy
- http://www.naturalearthdata.com/downloads/
- http://www.fabienpoulard.info/post/2011/01/24/Interroger-OpenStreetMap-en-Python-avec-OsmApi
- http://fabienpoulard.info/post/2012/12/23/Extraction-de-donn%C3%A9es-d-OpenStreetMap-hors-ligne
- https://github.com/grdscarabe/osm-utils/blob/master/osm2json-transportation.py
- https://wiki.openstreetmap.org/wiki/FR:Osmosis
- https://wiki.openstreetmap.org/wiki/Osmapi
- http://osmapi.metaodi.ch/
- http://michelleful.github.io/code-blog/2015/04/27/osm-data/
- http://nbviewer.jupyter.org/gist/pelson/8912530
- https://scitools.org.uk/cartopy/docs/v0.15/examples/tube_stations.html
- http://www.xavierdupre.fr/app/papierstat/helpsphinx/notebooks/enedis_cartes.html
- http://www.net-analysis.com/blog/cartopyintro.html
- http://darribas.org/gds_scipy16/ipynb_md/02_geovisualization.html
- https://ocefpaf.github.io/python4oceanographers/blog/2015/02/02/cartopy_folium_shapefile/
- http://earthpy.org/tag/cartopy.html
- https://govhack-toolkit.readthedocs.io/technical/geographic-data/
- https://scitools.org.uk/cartopy/docs/v0.13/matplotlib/advanced_plotting.html
- http://andykee.com/visualizing-strava-tracks-with-python.html
- https://scitools.org.uk/cartopy/docs/latest/matplotlib/intro.html
- https://stackoverflow.com/questions/tagged/cartopy?page=3&sort=newest&pagesize=15
