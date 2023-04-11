## About The Project
### Crop-yield-prediction


## Installation

You can install via pip:

```
pip install git+https://github.com/mardonat/crop-yield-prediction.git
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started


Import the modul:
```
from yieldprediction import yieldprediction
```

Import the data using Geopandas
```
[1] line = gpd.read_file('line.shp')
[2] line= line.to_crs('epsg:4326')
[3] poly = gpd.read_file('poly.shp')
[4] poly= poly.to_crs('epsg:4326')
```
Both type(poly) and type(line) must be geodataframes:
```
[1] print(type(poly)==gpd.geodataframe.GeoDataFrame)
[2] True
```
If only yield data have to be created in a grid or if no line is available, a polygon is sufficient as input. The variable 'years' determines the number of years of yield maps. By default 10 is set, so 5 years of multi-annual yield maps are created. The distance between the points in the grid can be changed with the 'raster_resulution'. The smaller the distance, the more points there are in the grid. With the variables 'center' ,'b' and 'bz' the spatial and temporal autocorrelation are changed. 'center' corresponds to the number of different zones that can have high or low yields, b changes the spatial influence of the individual centers and 'bz' varies the temporal variability of the zones.

```
np.random.seed(3) # to use the same random numbers for parametrization
random_yielddata_grid(poly,years=5,raster_resulution=10,center=30,b=1000,bz=0.5)
```
Each data point within the field geometry contains 6 columns. One column contains the geometry, the other 5 columns contain the yield values. They have been standardized to relative yield values. This is a common method to compare yield data between years on a field (Donat et al. (2022)). Here, 100 corresponds to the mean value. Data points with values greater than 100 are data points with yields higher than the mean. Data points with values less than 100 have yields lower than the mean.

```
from mpl_toolkits.axes_grid1 import make_axes_locatable # need that for a nice plot

np.random.seed(3) # just for the same random values for demonstration
random_yielddata1=random_yielddata_grid(poly,years=5,raster_resulution=10,center=30,b=1000,bz=0.5)

fig, ax = plt.subplots(figsize  = (20, 20))
xmin,ymin,xmax,ymax = poly.total_bounds
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="2.5%", pad=-2.5)
cax.tick_params(labelsize=30)

random_yielddata1.plot(ax=ax,cax=cax,column='yield_1',legend=True)
poly.boundary.plot(ax=ax,color='k')

ax.set_xlabel("Eastings",fontsize=26)
ax.set_ylabel("Northings",fontsize=26)
ax.text(xmax +0.005,ymax-0.01, "Relative yield (Year 1)", rotation=90, fontsize=48)
```
<img src="https://github.com/mardonat/crop-yield-prediction/blob/main/tutorials/images/test_usa_field_yield.png" width="600" height="500">
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Marco Donat -  marco.donat@zalf.de

Project Link: [https://github.com/mardonat/crop-yield-prediction.git](https://github.com/mardonat/crop-yield-prediction.git)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
