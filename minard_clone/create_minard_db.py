import pandas as pd
with open("data/minard.txt", encoding= "utf-8") as f:
	lines = f.readlines()
	
column_names = lines[2].split()
print(column_names)

patterns_to_be_replaced = {"(", ")", "$", ","}
adjusted_column_names = []
for column_name in column_names:
	for pattern in patterns_to_be_replaced:
		if pattern in column_name:
			column_name = column_name.replace(pattern, "")
	adjusted_column_names.append(column_name)
print(adjusted_column_names)

column_names_city = adjusted_column_names[:3]
column_names_temp = adjusted_column_names[3:7]
column_names_army = adjusted_column_names[7:]
print(column_names_city)
print(column_names_temp)
print(column_names_army)

i = 6
lonc, latc, cities = [], [], []
while i <= 25:
	lon, lat, city = lines[i].split()[:3]
	lonc.append(float(lon))
	latc.append(float(lat))
	cities.append(city)
	i += 1
city_data = (lonc, latc, cities)
city_df = pd.DataFrame()
for column_name, data in zip(column_names_city, city_data):
	city_df[column_name] = data
print(city_df)

