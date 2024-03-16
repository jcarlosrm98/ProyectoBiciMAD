import pandas as pd
import requests as req
import ast
import itertools
from fuzzywuzzy import fuzz
from geopy.distance import geodesic
import argparse

def obtener_argumentos():
    parser = argparse.ArgumentParser(description='Obtener estación de origen y destino')
    parser.add_argument('--origen', required=True, help='Estación de origen')
    parser.add_argument('--destino', required=True, help='Estación de destino')
    parser.add_argument('--distancia', action='store_true', help='Mostrar distancia entre origen y destino')
    return parser.parse_args()

def main(origen, destino, mostrar_distancia):
    est_bicimad = pd.read_csv("C:/IronHack/proyectos/ih_datamadpt0124_project_m1-main/data/bicimad_stations.csv", sep="\t")
    est_bicimad["geometry.coordinates"] = est_bicimad["geometry.coordinates"].apply(ast.literal_eval)
    est_bicimad['Latitudes'] = est_bicimad['geometry.coordinates'].apply(lambda x: x[1])
    est_bicimad["Longitudes"] = est_bicimad["geometry.coordinates"].apply(lambda x: x[0])
    est_bicimad.pop("geometry.type")
    est_bicimad.pop("Unnamed: 0")
    est_bicimad.pop("geometry.coordinates")
    est_bicimad.pop("free_bases")
    est_bicimad.pop("total_bases")
    est_bicimad.pop("number")
    df_bicimad = est_bicimad.rename(columns={"name":"location", "light":"ocupation","no_available": "availability", "dock_bikes":"bikes","reservations_count":"reservations"})
    df_bicimad['location'] = df_bicimad['location'].apply(lambda x: x.split('-')[-1])
    
    url = "https://datos.madrid.es/egob/catalogo/202311-0-colegios-publicos.json"
    res = req.get(url)
    name_colegios = res.json()["@graph"]
    data_coles = pd.json_normalize(name_colegios)
    data_coles.pop("organization.accesibility")
    data_coles.pop("organization.schedule")
    data_coles.pop("organization.services")
    data_coles.pop("address.postal-code")
    data_coles.pop("address.locality")
    data_coles.pop("address.area.@id")
    data_coles.pop("address.district.@id")
    data_coles.pop("relation")
    data_coles.pop("id")
    data_coles.pop("@type")
    data_coles.pop("@id")
    data_coles.pop("organization.organization-name")
    df_coles = data_coles.rename(columns={"title":"Place of interest", "address.street-address": "Place Address","location.latitude": "Latitude", "location.longitude":"Longitude","organization.organization-desc":"Type of place"})
    df_coles['Type of place'] = df_coles['Type of place'].apply(lambda x: x.split('B')[0]).apply(lambda x: x.split('- Pr')[0])

    df_bicimad["fuzzy"] = df_bicimad["location"].apply(lambda x: fuzz.partial_ratio(x, origen))
    df_bicimad_max = df_bicimad.nlargest(3, "fuzzy")
    
    df_coles["fuzzy"] = df_coles["Place of interest"].apply(lambda x: fuzz.partial_ratio(x, destino))
    df_coles_max = df_coles.nlargest(1, "fuzzy")

    station = pd.DataFrame()
    station_found = False

    for index, row in df_bicimad_max.iterrows():
        if (row["ocupation"] == 3 or row["reservations"] > row["bikes"] or row["bikes"] == 0 or
            row["availability"] != 0 or row["activate"] == 0):
            print("Estación inactiva o sin bicicletas disponibles, esta ubicación sí posee bicicletas:")
            next_station_index = index + 1
            
            if next_station_index < len(df_bicimad_max):
                next_station = df_bicimad_max.iloc[next_station_index]
                
                if (next_station["ocupation"] != 3 and next_station["reservations"] <= next_station["bikes"] and
                    next_station["bikes"] != 0 and next_station["availability"] == 0 and next_station["activate"] == 1):
                    station = pd.concat([row.to_frame().transpose(), next_station.to_frame().transpose()], axis=1)
                    station_found = True
                    break
                
        elif (row["ocupation"] != 3 and row["reservations"] <= row["bikes"] and
              row["bikes"] != 0 and row["availability"] == 0 and row["activate"] == 1):
            station = row.to_frame().transpose()
            station_found = True
            break

    if not station_found:
        print("No hay bicicletas disponibles cerca")
        station = pd.DataFrame(["No se encontró ninguna estación válida"])

    origen_bicimad = (df_bicimad_max["Latitudes"].iloc[0], df_bicimad_max["Longitudes"].iloc[0])
    destino_coles = (df_coles_max["Latitude"].iloc[0], df_coles_max["Longitude"].iloc[0])
    distance = geodesic(origen_bicimad, destino_coles).kilometers

    if mostrar_distancia:
        print(f"La distancia entre el origen y el destino es: {distance:.2f} kilómetros.")
    
    if "id" in station.columns:
        columns = ["id", "ocupation", "activate", "availability", "Latitudes", "Longitudes", "fuzzy"]
        origen_df = station.drop(columns=columns)
    else:
        origen_df = None 

    columns2 = ["Latitude", "Longitude", "fuzzy"]
    destino_df = df_coles_max.drop(columns=columns2)
    if origen_df is None:
        print("No hay bicis disponibles para tu origen, busca otra ubicación")
    else:
        final_df = pd.concat([origen_df.reset_index(drop=True), destino_df.reset_index(drop=True)], axis=1)
        print(final_df)

if __name__ == "__main__":
    args = obtener_argumentos()
    main(args.origen, args.destino, args.distancia)
