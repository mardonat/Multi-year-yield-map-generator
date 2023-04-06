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
yieldprediction.random_yielddata_grid(poly,years=5,raster_resulution=10, center=20,b=60,bz=10)
```



## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Marco Donat -  marco.donat@zalf.de

Project Link: [https://github.com/mardonat/crop-yield-prediction.git](https://github.com/mardonat/crop-yield-prediction.git)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
