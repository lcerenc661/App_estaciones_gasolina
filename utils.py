import requests
from haversine import haversine, Unit
import folium
import pandas as pd
import geopandas as gpd
from geopandas import  GeoDataFrame, points_from_xy



#Geocoding de la ubicación, obtenemos coordenas (lat,lon)
def get_coords(address,api_key_geocoding):
    
    url_get = f'https://geocode.search.hereapi.com/v1/geocode?q={address}&apiKey={api_key_geocoding}'
    
    try:
        response = requests.get(url=url_get).json()
        clean_address = response['items'][0]['title']
        coord_lat = response['items'][0]['position']['lat']
        coord_lng = response['items'][0]['position']['lng']
        
        results = [clean_address, coord_lat, coord_lng]
    except:
        
        results = ['Not Found', 'NA', 'NA']
    
    return results


#Calcula distancia entre dos puntos
def cal_dist(geo_source, point2, unit):
    
    if unit =='Km':
        distance = haversine(geo_source, point2, Unit.KILOMETERS)
    elif unit == 'm':
        distance = haversine(geo_source, point2, Unit.METERS)
    elif unit == 'miles':
        distance = haversine(geo_source, point2, Unit.MILES)
        
    return round(distance,2)


#Generamos df con las distancias hasta el centroide, ordenadas en ascendente.
def filtrar_dist(geo_source, df, radio, unit):
    
    distancia = []
    source = []
    
    for i in range(len(df)):
        distancia.append(cal_dist(geo_source,df['Coordenadas'][i],unit))
        source.append(geo_source)
        
    new_df = df.copy(deep=True)
    new_df['Fuente'] = source
    new_df['Distancia'] = distancia
    new_df = new_df[new_df['Distancia']<=radio]
    new_df = new_df.reset_index()
    new_df = new_df.drop(columns='index')
    
    return new_df.sort_values(by='Distancia', ascending=True)


#Generamos un nuevo df con la nueva columna "Coordenadas"
def transform_df_map(df):
    
    coordenadas = []
    
    for i in range(len(df)):
        
        try: 
            
            coord = float(df['Latitud'][i]), (float(df['Longitud'][i]))
            coordenadas.append(coord)
            
        except :
            
            coordenadas.append('Vacio')
            
    df['Coordenadas'] = coordenadas
    df = df[df['Coordenadas']!='Vacio'] 
    df = df.reset_index()
    df = df.drop(columns = 'index')
    new_df = df.copy()
    
    return new_df


#Generamos el mapa en folium, señalando el centroide y el radio a validar
def gen_map(geo_source, radio):
    
    m = folium.Map([geo_source[0], geo_source[1]], zoom_start=15)

    folium.Circle(
        radius=int(radio)*1000,
        location=[geo_source[0], geo_source[1]],
        color='green',
        fill='green').add_to(m)

    folium.Marker(
        location=[geo_source[0], geo_source[1]],
        icon = folium.Icon(
            color='black',
            icon_color='white',
            icon='home',
            prefix='glyphicon'
            ),
        popup="<b>Centro</b>"
        ).add_to(m)

    return m


#Graficamos las gasolineras segun el producto seleccionado, marcando la gasolinera con precio max(rojo) y min(verde)
def graph_gas_station(gdf,tipo_producto,icono, unit,mapa):
    
    df_nuevo = gdf[gdf['Producto']==tipo_producto]
    df_nuevo.reset_index(inplace=True)
    df_nuevo.drop(columns='index', inplace=True)


    for i in range(len(df_nuevo)):
        
        if int(df_nuevo['Precio'][i]) == int(df_nuevo['Precio'].min()):
            
            html =  f"""<b>MARCA:</b> {df_nuevo.Bandera[i]} <br>
                    <b>NOMBRE:</b> {df_nuevo.Nombre_comercial[i]} <br>
                    <b>PRODUCTO:</b> {df_nuevo.Producto[i]} <br>
                    <b>PRECIO:</b> {df_nuevo.Precio[i]} <br>
                    <b>DISTANCIA:</b> {df_nuevo.Distancia[i]} <br>
                    <b>UNIDAD:</b> {unit} <br>
                    <b>DIRECCION:</b> {df_nuevo.Direccion[i]} <br>"""
            iframe = folium.IFrame(html=html, figsize=(6,3))
            popup = folium.Popup(iframe)
            
            folium.Marker(location=[float(df_nuevo['Latitud'][i]), float(df_nuevo['Longitud'][i])],
                        icon = folium.Icon(
                            color='darkgreen',
                            icon_color='white',
                            icon=icono,
                            prefix='glyphicon'),
                        popup=popup).add_to(mapa)
        
        elif int(df_nuevo['Precio'][i]) == int(df_nuevo['Precio'].max()):
            
            html =  f"""<b>MARCA:</b> {df_nuevo.Bandera[i]} <br>
                    <b>NOMBRE:</b> {df_nuevo.Nombre_comercial[i]} <br>
                    <b>PRODUCTO:</b> {df_nuevo.Producto[i]} <br>
                    <b>PRECIO:</b> {df_nuevo.Precio[i]} <br>
                    <b>DISTANCIA:</b> {df_nuevo.Distancia[i]} <br>
                    <b>UNIDAD:</b> {unit} <br>
                    <b>DIRECCION:</b> {df_nuevo.Direccion[i]} <br>"""
            iframe = folium.IFrame(html=html, figsize=(6,3))
            popup = folium.Popup(iframe)
            
            folium.Marker(location=[float(df_nuevo['Latitud'][i]), float(df_nuevo['Longitud'][i])],
                        icon = folium.Icon(
                            color='darkred',
                            icon_color='white',
                            icon=icono,
                            prefix='glyphicon'),
                        popup=popup).add_to(mapa)
        
        else:
            
            html =  f"""<b>MARCA:</b> {df_nuevo.Bandera[i]} <br>
                    <b>NOMBRE:</b> {df_nuevo.Nombre_comercial[i]} <br>
                    <b>PRODUCTO:</b> {df_nuevo.Producto[i]} <br>
                    <b>PRECIO:</b> {df_nuevo.Precio[i]} <br>
                    <b>DISTANCIA:</b> {df_nuevo.Distancia[i]} <br>
                    <b>UNIDAD:</b> {unit} <br>
                    <b>DIRECCION:</b> {df_nuevo.Direccion[i]} <br>"""
            iframe = folium.IFrame(html=html, figsize=(6,3))
            popup = folium.Popup(iframe)
            
            folium.Marker(location=[float(df_nuevo['Latitud'][i]), float(df_nuevo['Longitud'][i])],
                        icon = folium.Icon(
                            color='orange',
                            icon_color='white',
                            icon=icono,
                            prefix='glyphicon'),
                        popup=popup).add_to(mapa)
            
    return

