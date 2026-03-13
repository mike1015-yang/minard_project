from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

m = Basemap(projection = "lcc", resolution = "i", width = 1000000, height = 400000,
            lon_0 = 31, lat_0 = 55)
lons = [24.0, 37.6]
lats = [55.0, 55.8]
m.drawcountries()
m.drawrivers()
m.drawparallels(range(54, 58), labels = [True, False, False, False])
m.drawmeridians(range(23, 56, 2), labels = [False, False, False, True])
xi, yi = m(lons, lats)
m.scatter(xi, yi)
plt.show()