from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
# import pymysql
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:password@localhost:3306/minard"
)
"""connection = pymysql.connect(
    host = "localhost",
    port = 3306,
    user = "root",
    password = "password",
    database = "minard",
    charset = "utf8mb4"
    )"""
city_df = pd.read_sql("""select * from cities;""", con = engine)
temp_df = pd.read_sql("""select * from temperatures;""", con = engine)
army_df = pd.read_sql("""select * from army;""", con = engine)

lonc = city_df["lonc"].values
latc = city_df["latc"].values
city_names = city_df["city"].values
rows = army_df.shape[0]
lonps = army_df["lonp"].values
latps = army_df["latp"].values
direction = army_df["direc"].values
survivals = army_df["surviv"].values
temp_celsius = (temp_df["temp"] * 1.25).astype(int)
lonts = temp_df["lont"].values
annotations = temp_celsius.astype(str).str.cat(temp_df["date"], sep = "°C ")
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

axes[1].plot(lonts, temp_celsius, linestyle = "dashed", color = "black")
for lont, temp_c, annotation in zip(lonts, temp_celsius, annotations):
    axes[1].annotate(annotation, xy = (lont - 0.3, temp_c - 7), fontsize = 16)
axes[1].set_ylim(-50, 10)
axes[1].spines["top"].set_visible(False)
axes[1].spines["right"].set_visible(False)
axes[1].spines["left"].set_visible(False)
axes[1].spines["bottom"].set_visible(False)
axes[1].grid(True, which = "major", axis = "both")
axes[1].set_xticklabels([])
axes[1].set_yticklabels([])
axes[0].set_title("Napolean's disastrous Russian campaign of 1812", loc = "left", fontsize = 30)
plt.tight_layout()
fig.savefig("minard_clone.png")