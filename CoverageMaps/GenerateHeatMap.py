import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from scipy.ndimage import gaussian_filter

from config import SimulationConfig

def generate_heatmap(grid, title, colourBarLabel=None):
    grid = gaussian_filter(grid, sigma=1.0)

    mean_val = np.mean(grid)
    min_val = np.min(grid)
    max_val = np.max(grid)

    plt.figure(figsize=(10, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.set_extent([
        SimulationConfig.LON_MIN, SimulationConfig.LON_MAX,
        SimulationConfig.LAT_MIN, SimulationConfig.LAT_MAX
    ])

    ax.coastlines(resolution="10m", linewidth=1)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.add_feature(cfeature.LAND, facecolor="lightgray")
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.LAND, facecolor="none", edgecolor="black")

    vmin = np.percentile(grid, 5)
    vmax = np.percentile(grid, 95)

    lon = np.linspace(SimulationConfig.LON_MIN, SimulationConfig.LON_MAX, grid.shape[1])
    lat = np.linspace(SimulationConfig.LAT_MIN, SimulationConfig.LAT_MAX, grid.shape[0])
    Lon, Lat = np.meshgrid(lon, lat)

    img = ax.pcolormesh(
        Lon, Lat, grid,
        cmap="plasma",
        vmin=vmin,
        vmax=vmax,
        shading="nearest",
        transform=ccrs.PlateCarree()
    )

    #if contours were [0,0,0,0] system would crash -> this block solves this issue
    if vmin == vmax or np.isnan(vmin) or np.isnan(vmax):
        contour_levels = None
    else:
        contour_levels = np.linspace(vmin, vmax, 6)
    #----------------------------------------------------------------------------

    if contour_levels is not None:
        cs = ax.contour(
            Lon, Lat, grid,
            levels=contour_levels,
            colors='black',
            linewidths=0.4,
            alpha=0.6,
            transform=ccrs.PlateCarree()
        )

        ax.clabel(cs, inline=True, fontsize=6, fmt="%.1f")


    stats_text = (f"Max:  {max_val:.2f}\n"
                  f"Min:  {min_val:.2f}\n"
                  f"Mean: {mean_val:.2f}")

    plt.gcf().text(0.82, 0.25, stats_text, fontsize=10, bbox=dict(facecolor='white', alpha=0.8))

    plt.colorbar(img, ax=ax, label=colourBarLabel)
    plt.title(title)
    plt.tight_layout()
    plt.show()