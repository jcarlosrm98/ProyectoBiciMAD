# Proyecto BiciMAD

En este repositorio encontrarás un código escrito en *Python* para comprobar la disponibilidad de bicicletas de **BiciMAD** proporcionando un origen y un destino que da el usuario y que devuelve la estación más cercana disponible, un destino centrándose en la búsqueda de colegios públicos en Madrid y la distancia a la que se encuentran ambos puntos.

## Status

Ironhack Data Analytics Project. Beta version.

## Technology stack

Este código está generado en *Python* para poder ser utilizado en la terminal y utiliza diversas librerías para funcionar:
1) *"Pandas"* para obtener y devolver DataFrames.
2) *"Requests"* para obtener el .json de los colegios públicos.
3) *"FuzzyWuzzy"* para obtener una comparación entre las estaciones de **BiciMAD** y la busqueda del origen.
4) *"Geodesic"* para calcular la distancia entre los puntos de origen y destino.
5) *"Folium"* para crear un mapa interactivo que dibuje una línea entre ambos puntos.
6) *"ArgParse"* para poder ejecutar el código a través de la terminal.

## Uso y funcionamiento

Para poder ejecutar el código, es necesario abrir la terminal y pegar el siguiente comando: "python bicimad_argparse.py --origen "origen" --destino "destino" --distancia" indicando el origen y el destino que desee el usuario dentro de las comillas.

La terminal devolverá entonces una tabla con los datos obtenidos. Los datos se dividen en dos categorias:
1) **Origen:** Devuelve los datos de la localización, el nombre de la calle, las bicicletas disponibles y las reservas realizadas.
2) **Destino:** Devuelve los datos de la dirección, el nombre del colegio, el tipo de lugar y la distancia entre los puntos.

Si la estación de origen se encuentra inactiva o sin bicicletas disponibles, el código buscará entre las ubicaciones más cercanas a la estación buscada. Si encuentra alguna que contenga bicicletas, devolverá ésta en su lugar. Si no encuentra ninguna estación cercana disponible, devovlerá una tabla indicando que no existen bicicletas cercanas en la ubicación proporcionada.

## Resources

- Estaciones BiciMAD: Dentro del repositorio.
- Colegios Públicos Madrid: [Link.](https://datos.madrid.es/egob/catalogo/202311-0-colegios-publicos.json)
