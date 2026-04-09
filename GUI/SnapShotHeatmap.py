import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def generate_cartopy_heatmap(sim_params, grid, title, colourBarLabel=None):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    ax.set_extent([
        sim_params["lon_min"], sim_params["lon_max"],
        sim_params["lat_min"], sim_params["lat_max"]
    ])

    ax.coastlines(resolution="10m", linewidth=1)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.add_feature(cfeature.LAND, facecolor="lightgray")
    ax.add_feature(cfeature.OCEAN)

    vmin = np.nanmin(grid)
    vmax = np.nanmax(grid)

    img = ax.imshow(
        grid,
        origin="lower",
        extent=[
            sim_params["lon_min"], sim_params["lon_max"],
            sim_params["lat_min"], sim_params["lat_max"]
        ],
        cmap="viridis",
        vmin=vmin,
        vmax=vmax,
        transform=ccrs.PlateCarree(),
        alpha=0.9,
    )

    if vmax != vmin:
        levels = np.linspace(vmin, vmax, 8)
        cs = ax.contour(
            grid,
            levels=levels,
            colors="black",
            linewidths=0.4,
            extent=[
                sim_params["lon_min"], sim_params["lon_max"],
                sim_params["lat_min"], sim_params["lat_max"]
            ],
            transform=ccrs.PlateCarree()
        )
        ax.clabel(cs, fontsize=7, inline=True)

    ax.set_title(title)

    return fig