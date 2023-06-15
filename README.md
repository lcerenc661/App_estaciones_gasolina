
# App "Estaciones de gasolina cercanas"

App desarrollada en python usando folium, pandas, hereplatform  APIy desplegada en streamlit con ayuda de docker.

El dataset tomado para esta APP se adquirió de datos abiertos Colombia:  

        https://www.datos.gov.co


Esta App localiza las estaciones de gasolina que se encuentren en un rango de 1 a 3 km (según especifique el usuario), especificando la gasolinera más económica y la más costosa según el tipo de combustible (también especificado según el usuario). En la versión actual solo contiene datos de estaciones en Medellín, Itagüí, Bello, Sabaneta, Rionegro y Envigado.



## Despliegue

Obtener la API KEY de hereplatform: 
Registraser en Here platform, crear un pryecto y generar la API KEY con permisos para realizar geocoding, esta se debe ingresar en el archivos credentials.py

```bash
    https://www.here.com/platform

```
Para correr la App se debe correr el contenedor de docker, esto se puede realizar con el siguiente comando en la terminal linux:

```bash
 docker run --name gas_app -it  -p 80:8501 gas_station_app
```




## Files

#### --app.py :
Archivo desde donde se corre la aplicación.

#### --utils.py :
Archivo donde se encuentran las funciones para correr en app.py.

#### --credentials.py :
EN este archivo se debe ubicar la API KEY de Here para realizar el geocoding de las ubicaciones.

#### --dockerfile :
Archivo con la imagen de docker para ejecutar el contenedor en cualquier ambiente.

#### --DIRECTORIO notebooks_desarrollo :
Contienen los notebooks en los cuales se desarrollo y probo el codigo que despues se orgnanizo en los archivos utils.py y app.py.

#### --DIRECTORIO data_files :
Contienen el data set crudo => "dataset_precios_combustibles.xlsx" y el data set tratado listo para ser usado en la app => "data_set_OK.csv".


