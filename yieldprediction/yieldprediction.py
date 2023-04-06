#!/usr/bin/env python
# coding: utf-8

import geopandas as gpd
import numpy as np

from pyproj import CRS
from pyproj.aoi import AreaOfInterest
from pyproj.database import query_utm_crs_info
from shapely.geometry import Point, LineString, MultiLineString, Polygon


def random_yielddata_grid(poly,years=10,raster_resulution=10, center=20,b=60,bz=10):
    """ 
    """
    
    poly= poly.to_crs('epsg:4326')
    
    ##find correct EPSG for calculation in meter
    utm_crs_list = query_utm_crs_info(datum_name="WGS 84",area_of_interest=AreaOfInterest(
                west_lon_degree=poly.bounds.values[0][0],
                south_lat_degree=poly.bounds.values[0][1],
                east_lon_degree=poly.bounds.values[0][2],
                north_lat_degree=poly.bounds.values[0][3]))
    
    EPSG = CRS.from_epsg(utm_crs_list[0].code)
    poly=poly.to_crs('{}'.format(EPSG))
    
    
    #bbbox, 
    bbox = poly.geometry.total_bounds
    xmin, ymin, xmax, ymax = bbox
    xres, yres = raster_resulution,raster_resulution  # Breite und Höhe jeder Zelle
    xcoords = np.arange(np.floor(xmin), np.ceil(xmax)+xres, xres)
    ycoords = np.arange(np.floor(ymin), np.ceil(ymax)+yres, yres)
    coords = np.stack(np.meshgrid(xcoords, ycoords), axis=-1).reshape(-1, 2)
    
    
    b = b/np.max((len(ycoords),len(xcoords))) #Bandbreite räumlich -> teilen durch maximum, damit normalisiert
     
    Z = np.zeros((len(ycoords),len(xcoords),years))

    sum_wv,sum_w = np.zeros_like(Z),np.zeros_like(Z)
    for i in range(center): 
        cy,cx,cz = np.random.randint(Z.shape[0]),np.random.randint(Z.shape[1]),np.random.randint(Z.shape[2])
        v = np.random.uniform()  

        mg = np.meshgrid(np.arange(Z.shape[0]) ,np.arange(Z.shape[1])  ,np.arange(Z.shape[2]), indexing="ij" )
        mg = np.stack(mg,-1)
        
        c=np.array((cy,cx,cz))
        w = np.linalg.norm((mg-c)/np.array((b,b,bz)),axis=3)

        w = np.exp(-w)

        sum_wv += w*v
        sum_w += w
        maps=sum_wv/sum_w
        maps=maps/np.mean(maps)*100 # standartisieren
        
        gdf_points = gpd.GeoDataFrame(geometry=gpd.points_from_xy(coords[:,0],coords[:,1]),)
        

        for i in range(maps.shape[2]):
            gdf_points["yield_"+str(2000+i)] = maps[:,:,i].ravel()
        gdf_points=gdf_points.set_crs('{}'.format(EPSG))
        gdf_points

        gdf_yield = gpd.sjoin(gdf_points,poly)
        gdf_yield = gdf_yield.drop('index_right', axis=1)
        
        gdf_yield=gdf_yield.to_crs('epsg:4326')

    return gdf_yield


def enlarge_line(line, distance_meter=200):
    
    enlarged_lines = []
    for index, row in line.iterrows():
        
        points = list(row.geometry.coords)

        dx = points[1][0] - points[0][0]
        dy = points[1][1] - points[0][1]

        factor = distance_meter / (dx**2 + dy**2)**0.5

        points = [ Point(points[0][0] - factor*dx, points[0][1] - factor*dy),
                    Point(points[1][0] + factor*dx, points[1][1] + factor*dy)]

        enlarged_line = LineString(points)
        enlarged_lines.append(enlarged_line)

    long_line = gpd.GeoDataFrame(geometry=enlarged_lines)

    return long_line

def random_yielddata_rows(poly,line,distance=30, width=3,years=5,raster_resulution=6,center=10,b=1000,bz=1):
    
    poly= poly.to_crs('epsg:4326')
    
    ##find correct EPSG for calculation in meter
    utm_crs_list = query_utm_crs_info(datum_name="WGS 84",area_of_interest=AreaOfInterest(
                west_lon_degree=poly.bounds.values[0][0],
                south_lat_degree=poly.bounds.values[0][1],
                east_lon_degree=poly.bounds.values[0][2],
                north_lat_degree=poly.bounds.values[0][3]))
    
    EPSG = CRS.from_epsg(utm_crs_list[0].code)
    
    poly=poly.to_crs('{}'.format(EPSG))
    line=line.to_crs('{}'.format(EPSG))
    
    enlarged_line=enlarge_line(line,distance_meter=2000)
    
    lines_copied=[]
    for i in range(-5000,5000,distance):
        lines_copied.append(enlarged_line.iloc[0][0].offset_curve(i))

    lines_copied_poly=MultiLineString(lines_copied).buffer(width)
    gdf_poly=gpd.GeoDataFrame( geometry=[lines_copied_poly])
    gdf_poly=gdf_poly.set_crs('{}'.format(EPSG))
    
    
    random_yielddata=random_yielddata_grid(poly,years,raster_resulution,center,b,bz)
    
    
    random_yielddata=random_yielddata.to_crs('{}'.format(EPSG))
    points_within = gpd.sjoin(random_yielddata,gdf_poly)
    points_within=points_within.to_crs('epsg:4326')
    
    return points_within
