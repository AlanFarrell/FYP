import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from scipy.ndimage import gaussian_filter


def generate_cartopy_heatmap(sim_params, grid, title, colourBarLabel=None):
    grid = gaussian_filter(grid, sigma=1.0)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    ax.set_extent([
        sim_params["lon_min"], sim_params["lon_max"],
        sim_params["lat_min"], sim_params["lat_max"]
    ])

    ax.coastlines(resolution="10m", linewidth=1)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.add_feature(cfeature.LAND, facecolor="none", edgecolor="black")
    ax.add_feature(cfeature.OCEAN)

    vmin = np.percentile(grid, 5)
    vmax = np.percentile(grid, 95)

    lon = np.linspace(sim_params["lon_min"], sim_params["lon_max"], grid.shape[1])
    lat = np.linspace(sim_params["lat_min"], sim_params["lat_max"], grid.shape[0])
    Lon, Lat = np.meshgrid(lon, lat)

    img = ax.pcolormesh(
        Lon, Lat, grid,
        cmap="plasma",
        vmin=vmin,
        vmax=vmax,
        shading="nearest",
        transform=ccrs.PlateCarree()
    )

    if vmin != vmax and not np.isnan(vmin) and not np.isnan(vmax):
        levels = np.linspace(vmin, vmax, 6)
        cs = ax.contour(
            Lon, Lat, grid,
            levels=levels,
            colors="black",
            linewidths=0.4,
            alpha=0.6,
            transform=ccrs.PlateCarree()
        )
        ax.clabel(cs, fontsize=7, inline=True, fmt="%.1f")

    cbar = plt.colorbar(img, ax=ax, orientation="vertical", pad=0.02)
    if colourBarLabel:
        cbar.set_label(colourBarLabel)

    ax.set_title(title)
    plt.tight_layout()

    return fig
