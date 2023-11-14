# This file is meant to graph a route(s) after an order of locations
# has been determined.
# by: Huanlin Dai

import contextily as cx
import folium
import geopandas
import matplotlib
import networkx as nx
import osmnx as ox
import pandas as pd

# from geodatasets import get_path
# from shapely.geometry import LineString


def find_bbox(coords):
    """
    Given a list of coordinates (longitude and latitude),
    find a bounding box that contains all the points of interest.
    This function helps reduce the number of nodes and edges in a
    osmnx graph to reduce computational complexity/time.
    Parameters:
        coords : pd.DataFrame
    Returns:
        n, s, e, w : float
    """
    if len(coords) == 0:
        raise ValueError("find_bbox :: no coords inputted")
    n, s, e, w = [
        coords["Latitude"].iloc[0],
        coords["Latitude"].iloc[0],
        coords["Longitude"].iloc[0],
        coords["Longitude"].iloc[0],
    ]
    for i in range(len(coords)):
        longitude = coords["Longitude"].iloc[i]
        latitude = coords["Latitude"].iloc[i]
        n, s, e, w = [
            max(latitude, n),
            min(latitude, s),
            max(longitude, e),
            min(longitude, w),
        ]
    return n, s, e, w


def osmnx_to_latlon(graph, routes):
    """
    given a route created by osmnx (node numbers), create a list of x, y
    coordinates to draw on folium

    Parameters:
        graph : osmnx graph
        routes : list of osmnx routes (routes are usually lists of nodes)
    Returns:
        list of (lat, lon) coordinates
    """
    final_route = []
    for route in routes:
        for point in route:
            final_route.append(
                (graph.nodes[point]["y"], graph.nodes[point]["x"])
            )
    return final_route


def calc_routes(graph, coords):
    """
    Takes in a graph and a set of coordinates
    (w/ columns "Longitude" and "Latitude")
    and returns the set of shortest routes between each coordinate

    Parameters:
        graph : osmnx graph
        coords : dataframe
    Returns:
        routes: list of routes

    """
    routes = []
    for i in range(len(coords) - 1):
        start_node = ox.nearest_nodes(
            graph, coords.iloc[i]["Longitude"], coords.iloc[i]["Latitude"]
        )
        end_node = ox.nearest_nodes(
            graph,
            coords.iloc[i + 1]["Longitude"],
            coords.iloc[i + 1]["Latitude"],
        )
        routes.append(
            nx.shortest_path(graph, start_node, end_node, weight="length")
        )

    return osmnx_to_latlon(graph, routes)


def add_markers(f_map, route_data, color):
    """
    given a folium map, route data (includes location names), and a color (str),
    draw markers on the given map

    Parameters:
        f_map : folium map
        route_data : pd.DataFrame
        color : str (e.g., "red", "blue")
    """

    # icon_size = 100
    for i in range(len(route_data)):
        y, x = route_data[["Latitude", "Longitude"]].iloc[i]
        folium.Marker(
            (y, x), popup=route_data["Name"][i], icon=folium.Icon(color=color)
        ).add_to(f_map)
        # icon_size = 40
    return None


if __name__ == "__main__":

    place = "Galveston, Texas, USA"  # location = [29.30135, -94.7977]

    feu_galveston = pd.read_csv("../data/FUE_Galveston.csv")
    route_1_data = pd.read_csv("../data/route1.csv")
    route_2_data = pd.read_csv("../data/route2.csv")
    coords1 = route_1_data[["Longitude", "Latitude"]]
    coords2 = route_2_data[["Longitude", "Latitude"]]

    n1, s1, e1, w1 = find_bbox(coords1)
    n2, s2, e2, w2 = find_bbox(coords2)

    graph = ox.graph_from_place(place, network_type="drive")

    galv_graph1 = ox.truncate.truncate_graph_bbox(
        graph,
        n1,
        s1,
        e1,
        w1,
        truncate_by_edge=False,
        retain_all=False,
        quadrat_width=0.05,
        min_num=3,
    )
    galv_graph2 = ox.truncate.truncate_graph_bbox(
        graph,
        n2,
        s2,
        e2,
        w2,
        truncate_by_edge=False,
        retain_all=False,
        quadrat_width=0.05,
        min_num=3,
    )

    route_1 = calc_routes(galv_graph1, coords1)
    route_2 = calc_routes(galv_graph2, coords2)

    map = folium.Map(location=place, tiles="OpenStreetMap", zoom_start=11)
    add_markers(map, route_1_data, "blue")
    add_markers(map, route_2_data, "red")
    folium.PolyLine(locations=route_1, color="blue").add_to(map)
    folium.PolyLine(locations=route_2, color="red").add_to(map)

    map.save("../output/route.html")
