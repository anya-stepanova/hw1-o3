import argparse
import numpy as np
import json
from scipy.io import netcdf
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('longitude', metavar='LON', type=float, help='Longitude, deg')
parser.add_argument('latitude',  metavar='LAT', type=float, help='Latitude, deg')

if __name__ == "__main__":
    args = parser.parse_args()
    print(args.longitude, args.latitude)
    

with netcdf.netcdf_file('MSR-2.nc', mmap=False) as netcdf_file:
    variables = netcdf_file.variables

lat_index = np.searchsorted(variables['latitude'].data, args.latitude)
lon_index = np.searchsorted(variables['longitude'].data, args.longitude)

conc = variables['Average_O3_column'][:, lat_index, lon_index]
time = [i for i in range(516)]

conc_jan = conc[0::12]
conc_jul = conc[6::12]


text = {
  "coordinates": [args.longitude, args.latitude],
  "jan": {
    "min": float(conc_jan.min()),
    "max": float(conc_jan.max()),
    "mean": np.mean(conc_jan)
  },
  "jul": {
    "min": float(conc_jul.min()),
    "max": float(conc_jul.max()),
    "mean": np.mean(conc_jul)
  },
  "all": {
    "min": float(conc.min()),
    "max": float(conc.max()),
    "mean": np.mean(conc)
  }
}
with open('ozon.json', 'w') as f:
    json.dump(text, f)
    

plt.figure(figsize=(20, 10))
plt.plot(time, conc, label='All interval')
plt.plot(time[0::12], conc_jan, label='January')
plt.plot(time[6::12], conc_jul, label='July')
plt.legend()
plt.grid()
plt.xlabel("time")
plt.ylabel("ozone concentration")
plt.savefig('ozon.png')
