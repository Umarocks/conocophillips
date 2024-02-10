import chart_studio.plotly as py
import numpy as np           
from scipy.io import netcdf  
from mpl_toolkits.basemap import Basemap
import warnings
import plotly.graph_objs as go
from numpy import pi, sin, cos
from plotly.offline import plot

def degree2radians(degree):
    #convert degrees to radians
    return degree*pi/180

import numpy as np
from netCDF4 import Dataset

def Etopo(lon_area, lat_area, resolution):
    ### Input
    # resolution: resolution of topography for both of longitude and latitude [deg]
    # (Original resolution is 0.0167 deg)
    # lon_area and lat_area: the region of the map which you want like [100, 130], [20, 25]
    ###
    ### Output
    # Mesh type longitude, latitude, and topography data
    ###

    # Read NetCDF data
    data = Dataset("ETOPO1_Ice_g_gdal.grd", "r")

    # Get data
    lon_range = data.variables['x_range'][:]
    lat_range = data.variables['y_range'][:]
    topo_range = data.variables['z_range'][:]
    spacing = data.variables['spacing'][:]
    dimension = data.variables['dimension'][:]
    z = data.variables['z'][:]
    lon_num = dimension[0]
    lat_num = dimension[1]

    # Prepare array
    lon_input = np.zeros(lon_num); lat_input = np.zeros(lat_num)
    for i in range(lon_num):
        lon_input[i] = lon_range[0] + i * spacing[0]
    for i in range(lat_num):
        lat_input[i] = lat_range[0] + i * spacing[1]

    # Create 2D array
    lon, lat = np.meshgrid(lon_input, lat_input)

    # Convert 2D array from 1D array for z value
    topo = np.reshape(z, (lat_num, lon_num))

    # Skip the data for resolution
    if ((resolution < spacing[0]) | (resolution < spacing[1])):
        print('Set the highest resolution')
    else:
        skip = int(resolution/spacing[0])
        lon = lon[::skip,::skip]
        lat = lat[::skip,::skip]
        topo = topo[::skip,::skip]

    topo = topo[::-1]

    # Select the range of map
    range1 = np.where((lon>=lon_area[0]) & (lon<=lon_area[1]))
    lon = lon[range1]; lat = lat[range1]; topo = topo[range1]
    range2 = np.where((lat>=lat_area[0]) & (lat<=lat_area[1]))
    lon = lon[range2]; lat = lat[range2]; topo = topo[range2]

    # Convert 2D again
    lon_num = len(np.unique(lon))
    lat_num = len(np.unique(lat))
    lon = np.reshape(lon, (lat_num, lon_num))
    lat = np.reshape(lat, (lat_num, lon_num))
    topo = np.reshape(topo, (lat_num, lon_num))

    return lon, lat, topo

def mapping_map_to_sphere(lon, lat, radius=1):
    # this function maps the points of coords (lon, lat) to points onto the sphere of radius radius
    lon=np.array(lon, dtype=np.float64)
    lat=np.array(lat, dtype=np.float64)
    lon=degree2radians(lon)
    lat=degree2radians(lat)
    xs=radius*np.cos(lon)*np.cos(lat)
    ys=radius*np.sin(lon)*np.cos(lat)
    zs=radius*np.sin(lat)
    return xs, ys, zs

m = Basemap()

# Functions converting coastline/country polygons to lon/lat traces
def polygons_to_traces(poly_paths, N_poly):
    ''' 
    pos arg 1. (poly_paths): paths to polygons
    pos arg 2. (N_poly): number of polygon to convert
    '''
    # init. plotting list
    lons=[]
    lats=[]

    for i_poly in range(N_poly):
        poly_path = poly_paths[i_poly]
        
        # get the Basemap coordinates of each segment
        coords_cc = np.array(
            [(vertex[0],vertex[1]) 
             for (vertex,code) in poly_path.iter_segments(simplify=False)]
        )
        
        # convert coordinates to lon/lat by 'inverting' the Basemap projection
        lon_cc, lat_cc = m(coords_cc[:,0],coords_cc[:,1], inverse=True)
    
        
        lats.extend(lat_cc.tolist()+[None]) 
        lons.extend(lon_cc.tolist()+[None])
        
       
    return lons, lats

# Function generating coastline lon/lat 
def get_coastline_traces():
    poly_paths = m.drawcoastlines().get_paths() # coastline polygon paths
    N_poly = 91  # use only the 91st biggest coastlines (i.e. no rivers)
    cc_lons, cc_lats= polygons_to_traces(poly_paths, N_poly)
    return cc_lons, cc_lats

# Function generating country lon/lat 
def get_country_traces():
    poly_paths = m.drawcountries().get_paths() # country polygon paths
    N_poly = len(poly_paths)  # use all countries
    country_lons, country_lats= polygons_to_traces(poly_paths, N_poly)
    return country_lons, country_lats

def mainOLD():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with netcdf.netcdf_file('ETOPO_2022_v1_60s_N90W180_geoid.nc', 'r') as f:
            lon = f.variables['lon'][::]       # copy longitude as list
            lat = f.variables['lat'][::-1]     # invert the latitude vector -> South to North
            olr = f.variables['olr'][0,::-1,:] # olr= outgoing longwave radiation
        f.fp   

    # Shift 'lon' from [0,360] to [-180,180]
    tmp_lon = np.array([lon[n]-360 if l>=180 else lon[n] 
                    for n,l in enumerate(lon)])  # => [0,180]U[-180,2.5]

    i_east, = np.where(tmp_lon>=0)  # indices of east lon
    i_west, = np.where(tmp_lon<0)   # indices of west lon
    lon = np.hstack((tmp_lon[i_west], tmp_lon[i_east]))  # stack the 2 halves

    # Correspondingly, shift the olr array
    olr_ground = np.array(olr)
    olr = np.hstack((olr_ground[:,i_west], olr_ground[:,i_east]))

    # Get list of of coastline, country, and state lon/lat 

    cc_lons, cc_lats=get_coastline_traces()
    country_lons, country_lats=get_country_traces()

    #concatenate the lon/lat for coastlines and country boundaries:
    lons=cc_lons+[None]+country_lons
    lats=cc_lats+[None]+country_lats

    xs, ys, zs=mapping_map_to_sphere(lons, lats, radius=1.01)# here the radius is slightly greater than 1 
                                                         #to ensure lines visibility; otherwise (with radius=1)
                                                         # some lines are hidden by contours colors

    boundaries=dict(type='scatter3d',
               x=xs,
               y=ys,
               z=zs,
               mode='lines',
               line=dict(color='black', width=1)
              )
    
    colorscale=[[0.0, '#313695'],
        [0.07692307692307693, '#3a67af'],
        [0.15384615384615385, '#5994c5'],
        [0.23076923076923078, '#84bbd8'],
        [0.3076923076923077, '#afdbea'],
        [0.38461538461538464, '#d8eff5'],
        [0.46153846153846156, '#d6ffe1'],
        [0.5384615384615384, '#fef4ac'],
        [0.6153846153846154, '#fed987'],
        [0.6923076923076923, '#fdb264'],
        [0.7692307692307693, '#f78249'],
        [0.8461538461538461, '#e75435'],
        [0.9230769230769231, '#cc2727'],
        [1.0, '#a50026']]

    clons=np.array(lon.tolist()+[180], dtype=np.float64)
    clats=np.array(lat, dtype=np.float64)
    clons, clats=np.meshgrid(clons, clats)

    XS, YS, ZS=mapping_map_to_sphere(clons, clats)

    nrows, ncolumns=clons.shape
    OLR=np.zeros(clons.shape, dtype=np.float64)
    OLR[:, :ncolumns-1]=np.copy(np.array(olr,  dtype=np.float64))
    OLR[:, ncolumns-1]=np.copy(olr[:, 0])

    text=[['lon: '+'{:.2f}'.format(clons[i,j])+'<br>lat: '+'{:.2f}'.format(clats[i, j])+
        '<br>W: '+'{:.2f}'.format(OLR[i][j]) for j in range(ncolumns)] for i in range(nrows)]

    sphere=dict(type='surface',
            x=XS, 
            y=YS, 
            z=ZS,
            colorscale=colorscale,
            surfacecolor=OLR,
            cmin=-20, 
            cmax=20,
            colorbar=dict(thickness=20, len=0.75, ticklen=4, title= 'W/m²'),
            text=text,
            hoverinfo='text')

    noaxis=dict(showbackground=False,
            showgrid=False,
            showline=False,
            showticklabels=False,
            ticks='',
            title='',
            zeroline=False)

    layout3d=dict(title='Outgoing Longwave Radiation Anomalies<br>Dec 2017-Jan 2018',
              font=dict(family='Balto', size=14),
              width=800, 
              height=800,
              scene=dict(xaxis=noaxis, 
                         yaxis=noaxis, 
                         zaxis=noaxis,
                         aspectratio=dict(x=1,
                                          y=1,
                                          z=1),
                         camera=dict(eye=dict(x=1.15, 
                                     y=1.15, 
                                     z=1.15)
                                    )
            ),
            paper_bgcolor='rgba(235,235,235, 0.9)'  
           )
             
    fig=dict(data=[sphere, boundaries], layout=layout3d)
    py.sign_in('empet', 'api_key')
    py.iplot(fig, filename='radiation-map2sphere')

def main():
    # Import topography data
    # Select the area you want
    resolution = 0.8
    lon_area = [-180., 180.]
    lat_area = [-90., 90.]
    # Get mesh-shape topography data
    lon_topo, lat_topo, topo = Etopo(lon_area, lat_area, resolution)
    xs, ys, zs = mapping_map_to_sphere(lon_topo, lat_topo)

    Ctopo = [[0, 'rgb(0, 0, 70)'],[0.2, 'rgb(0,90,150)'], 
          [0.4, 'rgb(150,180,230)'], [0.5, 'rgb(210,230,250)'],
          [0.50001, 'rgb(0,120,0)'], [0.57, 'rgb(220,180,130)'], 
          [0.65, 'rgb(120,100,0)'], [0.75, 'rgb(80,70,0)'], 
          [0.9, 'rgb(200,200,200)'], [1.0, 'rgb(255,255,255)']]
    cmin = -8000
    cmax = 8000

    topo_sphere=dict(type='surface',
        x=xs,
        y=ys,
        z=zs,
        colorscale=Ctopo,
        surfacecolor=topo,
        cmin=cmin,
        cmax=cmax)
    
    noaxis=dict(showbackground=False,
        showgrid=False,
        showline=False,
        showticklabels=False,
        ticks='',
        title='',
        zeroline=False)
    

    titlecolor = 'white'
    bgcolor = 'black'

    layout = go.Layout(
    autosize=False, width=1200, height=800,
    title = '3D spherical topography map',
    titlefont = dict(family='Courier New', color=titlecolor),
    showlegend = False,
    scene = dict(
        xaxis = noaxis,
        yaxis = noaxis,
        zaxis = noaxis,
        aspectmode='manual',
        aspectratio=go.layout.scene.Aspectratio(
        x=1, y=1, z=1)),
    paper_bgcolor = bgcolor,
    plot_bgcolor = bgcolor)

    
    plot_data=[topo_sphere]
    fig = go.Figure(data=plot_data, layout=layout)
    plot(fig, validate = False, filename='SphericalTopography.html',
    auto_open=True)

if __name__ == "__main__":
    main()