import streamlit as st
from PIL import Image
import requests
from haversine import haversine, Unit
import folium
import pandas as pd
import geopandas as gpd
from geopandas import  GeoDataFrame, points_from_xy
from streamlit_folium import folium_static

from utils import get_coords, cal_dist, filtrar_dist, transform_df_map, gen_map, graph_gas_station
from credentials import API_KEY


image = Image.open('gasolinera_img.png')
developer_key = API_KEY

st.sidebar.image(
    image=image,
    caption='Estaciones de gasolina Cercanas',
    width= 256)

app_mode = st.sidebar.selectbox("Estado de la aplicacíon", ['Correr aplicación','Sobre mi'])

if app_mode == 'Correr aplicación':
    
    st.title('App Gasolineras Cercanas')
    st.markdown('Descripción')
    
    df_map = pd.read_csv('data_files/data_set_OK.csv')
    ciudades = list(df_map['Municipio'].unique())
    
    c1,c2,c3,c4,c5 = st.columns((1,6,6,6,1))

    
    locacion = c2.text_input('Locación', 'CC Premium Plaza, Medellin')
    if len(locacion) != 0:
        
        
        respuesta = get_coords(locacion, API_KEY)
        geo_source = (respuesta[1], respuesta[2])
        
        radio = c4.slider('Radio',1,3,1)
        unit = 'Km'
        
        map = gen_map(geo_source, radio)
        
        ciudades_df = transform_df_map(df_map)
        results_df = filtrar_dist(geo_source, ciudades_df, radio, unit)
        gdf_results = GeoDataFrame(results_df, geometry=points_from_xy(results_df['Latitud'],results_df['Longitud']))
        print(gdf_results['Distancia'])
        producto = c3.selectbox('Producto',list(gdf_results['Producto'].unique()))
        
        if c4.button('SHOW MAP'):
            
            graph_gas_station(gdf_results,producto,"usd", unit,map)
            folium_static(map)

        
    
    


elif app_mode == 'Sobre mi':
    
    pass

    

