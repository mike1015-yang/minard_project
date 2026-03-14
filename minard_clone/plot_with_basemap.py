from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pymysql
import pandas as pd

connection = pymysql.connect(
    host = "localhost",
    port = 3306,
    user = "root",
    password = "password",
    database = "minard",
    charset = "utf8mb4"
    )
city_df = pd.read_sql("""select * from cities;""", con = connection)
temp_df = pd.read_sql("""select * from temperatures;""", con = connection)
army_df = pd.read_sql("""select * from army;""", con = connection)

lonc = city_df["lonc"].values
latc = city_df["latc"].values
city_names = city_df["city"].values
rows = army_df.shape[0]
lonps = army_df["lonp"].values
latps = army_df["latp"].values
direction = army_df["direc"].values
survivals = army_df["surviv"].values

fig, axes = plt.subplots(nrows = 2, figsize = (25, 12), gridspec_kw = {"height_ratios" : [4, 1]})
m = Basemap(projection = "lcc", resolution = "i", width = 1000000, height = 400000,
            lon_0 = 31, lat_0 = 55, ax = axes[0])
m.drawcountries()
m.drawrivers()
m.drawparallels(range(54, 58), labels = [True, False, False, False])
m.drawmeridians(range(23, 56, 2), labels = [False, False, False, True])
x, y = m(lonc, latc)
for xi, yi, city_name in zip(x, y, city_names):
    axes[0].annotate(text = city_name, xy = (xi, yi), fontsize = 14, zorder = 2)
x, y = m(lonps, latps)    
for i in range(rows - 1):
    if direction[i] == "A":
        line_color = "tan"
    else:
        line_color = "black"
    start_stop_lons = (x[i], x[i + 1])
    start_stop_lats = (y[i], y[i + 1])
    line_width = survivals[i]
    m.plot(start_stop_lons, start_stop_lats, linewidth = line_width/10000, color = line_color, zorder = 1)
plt.show()


"""temp_celsius = (temp_df["temp"] * 1.25).values
lons = temp_df["lont"].values
fig, ax = plt.subplots()
ax.plot(lons, temp_celsius)
plt.show()"""


"""rows = army_df.shape[0]
lons = army_df["lonp"].values
lats = army_df["latp"].values
survivals = army_df["surviv"].values
direction = army_df["direc"].values
fig, ax = plt.subplots()

plt.show()"""