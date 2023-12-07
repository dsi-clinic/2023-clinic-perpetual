# Output Directory

* `feasibilityfile.csv` : Feasibility Analysis output csv file. 
* `map_bikes.html` : (code/bike_conversions.py output) folium map with bike-accessible points
* `map_trucks_and_bikes.html` : (code/bike_conversions.py output) folium map with all points
* `map_trucks.html` : (code/bike_conversions.py output) folium map with truck-accessible points

* `data/` : contains intermediary/resulting data output by code
    * `converted_bike_dists_galv.csv` : distance matrix for converted bike points
    * `converted_bike_service_pts.csv` : dataframe for converted bike points
    * `converted_truck_dists_galv.csv` : distance matrix for converted truck points
    * `converted_truck_service_pts.csv` : dataframe for converted truck points
    * `extracted_supp_info_dict.csv` : dataframe storing supplementary info dictionary for all points
* `routes/` : (output?) contains route data outputs after `output/data/` data through routing algorithms