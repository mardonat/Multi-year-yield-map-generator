## About The Project
Multi-year-yield-map-generator  is a tool for random but realistic plant yield modeling. The yield correlates spatially and temporally and can be regulated in its temporal and spatial heterogeneity via individual parameters. It is designed to be used worldwide and to take into account actual working directions.  
This tool can be used to validate and compare methods of yield map filtering, spatial interpolation and management zone creation. 


## Installation

You can install via pip:

```
pip install git+https://github.com/mardonat/Multi-year-yield-map-generator.git
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

Import the modul:
```
from yieldprediction import yieldprediction
```

Import the data using Geopandas (Data can be downloaded in the [tutorial folder](https://github.com/mardonat/Multi-year-yield-map-generator-/tree/main/tutorials))

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
If only yield data have to be created in a grid or if no line is available, a polygon is sufficient as input. The variable 'years' determines the number of years of yield maps. By default 10 is set, so 10 years of multi-annual yield maps are created. The distance between the points in the grid can be changed with the 'raster_resulution'. The smaller the distance, the more points there are in the grid. With the variables 'center' ,'b' and 'bz' the spatial and temporal autocorrelation are changed. 'center' corresponds to the number of different zones that can have high or low yields, b changes the spatial influence of the individual centers and 'bz' varies the temporal variability of the zones.

```
np.random.seed(3) # to use the same random numbers for parametrization
yieldprediction.random_yielddata_grid(poly,years=5,raster_resulution=10,center=30,b=1000,bz=0.5)
```
Each data point within the field geometry contains 6 columns. One column contains the geometry, the other 5 columns contain the yield values. They have been standardized to relative yield values. This is a common method to compare yield data between years on a field (Donat et al. (2022)). Here, 100 corresponds to the mean value. Data points with values greater than 100 are data points with yields higher than the mean. Data points with values less than 100 have yields lower than the mean.

```
from mpl_toolkits.axes_grid1 import make_axes_locatable # need that for a nice plot

np.random.seed(3) # just for the same random values for demonstration
random_yielddata1=yieldprediction.random_yielddata_grid(poly,years=5,raster_resulution=10,center=30,b=1000,bz=0.5)

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
<img src="https://github.com/mardonat/crop-yield-prediction/blob/main/tutorials/images/test_usa_field_yield.png" width="900" height="500">

If you provide a line, yield data can also be generated in lines (similar to real yield data generated by a combine harvester).
```
np.random.seed(3)
yieldprediction.random_yielddata_rows(poly,line,years=5,distance=50, width=10,raster_resulution=10,center=30,b=1000,bz=0.5)
```
'distance' corresponds to the distance between the yield data lines and 'width' determines the number of points within the lines.

```
np.random.seed(9)
random_yielddata1=yieldprediction.random_yielddata_rows(poly,line,years=5,distance=50, width=10,raster_resulution=10,center=30,b=1000,bz=0.5)

fig, ax = plt.subplots(figsize  = (20, 20))
xmin,ymin,xmax,ymax = poly.total_bounds
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="2.5%", pad=-2.5)
cax.tick_params(labelsize=30)

random_yielddata1.plot(ax=ax,cax=cax,column='yield_0',legend=True)
poly.boundary.plot(ax=ax,color='k')

ax.set_xlabel("Eastings",fontsize=26)
ax.set_ylabel("Northings",fontsize=26)
ax.text(xmax +0.005,ymax-0.01, "Relative yield (Year 1)", rotation=90, fontsize=48)
```
<img src="https://github.com/mardonat/crop-yield-prediction/blob/main/tutorials/images/test_usa_field_yield_rows.png" width="900" height="500">


To check the temporal stability we use the standard deviation of all years:

```
##extract yield and geometry column -> if poly is used with severell additional atributes

yield_cols = [col for col in random_yielddata1.columns if col.startswith('geometry') or col.startswith('yield')]
yield_df = random_yielddata1[yield_cols]

#calculation of mean,SD and CV
yield_cols = [col for col in random_yielddata1.columns if col.startswith('yield')]

yield_df1=yield_df.copy()
yield_df1['mean']=yield_df1[yield_cols].mean(axis=1)
yield_df1['SD']=yield_df1[yield_cols].std(axis=1)
yield_df1['CV']=yield_df1['SD']/yield_df1['mean']
yield_gdf=gpd.GeoDataFrame(yield_df1,geometry='geometry')
```
By plotting the column 'SD' we can look at temporal stability of the data points:

```
fig, ax = plt.subplots(figsize  = (20, 20))
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="2.5%", pad=-2.5)
cax.tick_params(labelsize=30)
xmin,ymin,xmax,ymax = poly.total_bounds

yield_gdf.plot(ax=ax,cax=cax,column='SD',cmap='OrRd',legend=True)
poly.boundary.plot(ax=ax,color='k')

ax.set_xlabel("Eastings",fontsize=26)
ax.set_ylabel("Northings",fontsize=26)
ax.text(xmax +0.005,ymax-0.01, "Standard deviation (σ)", rotation=90, fontsize=48)
```
<img src="https://github.com/mardonat/crop-yield-prediction/blob/main/tutorials/images/test_usa_field_yield_SD.png" width="900" height="500">

We can also generate a classified management map with the following classification:
```
+ higher yielding and stable
+ lower yielding and stable
+ unstable
```
For this we only need to set a treshold and filter our gdf:
```
threshold=20
high_stabel=yield_gdf[yield_gdf['SD']<threshold][yield_gdf['mean']>100]
low_stabel=yield_gdf[yield_gdf['SD']<threshold][yield_gdf['mean']<100]
unstabel=yield_gdf[yield_gdf['SD']>threshold]
```
and plot it subsequently:
```
fig, ax = plt.subplots(figsize  = (20, 20))
xmin,ymin,xmax,ymax = poly.total_bounds

poly.boundary.plot(ax=ax,color='k')
high_stabel.plot(ax=ax,color='g',alpha=0.7,markersize=5)
low_stabel.plot(ax=ax,color='r',alpha=0.7,markersize=5)
unstabel.plot(ax=ax,color='b',alpha=0.7,markersize=5)

ax.text( xmax-0.0065,ymax-0.00855,"Yield Classification", fontsize=35)
colors = {'Higher yielding and stable ':'green', 'Lower yielding and stable ':'red', 'Unstabel':'blue'}         
labels = list(colors.keys())
handles = [plt.Rectangle((0,0),0.01,0.01, ls =':',lw = 1, ec='k',color=colors[label]) for label in labels]
plt.legend(handles, labels,loc='lower right',fontsize=30,facecolor='white', framealpha=1)
ax.set_xlabel("Eastings",fontsize=26)
ax.set_ylabel("Northings",fontsize=26)
```

<img src="https://github.com/mardonat/crop-yield-prediction/blob/main/tutorials/images/test_usa_field_yield_classification_new.png" width="700" height="500">

## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Marco Donat -  marco.donat@zalf.de

Project Link: [https://github.com/mardonat/Multi-year-yield-map-generator](https://github.com/mardonat/Multi-year-yield-map-generator)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
