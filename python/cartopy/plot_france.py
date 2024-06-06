import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

COORDINATES_TO_PLOT = [
    (2.3522, 48.8566),  # Paris
    (3.0588, 50.6347),  # Lille
    (5.3698, 43.2965),  # Marseille
    (1.4442, 43.6047),  # Montpellier
    (-1.5536, 47.2184),  # Nantes
    (-0.5792, 44.8378),  # Bordeaux
    (3.8767, 43.6116),  # Toulouse
    (7.2650, 43.7102),  # Nice
    (4.8357, 45.7640),  # Lyon
    (6.1296, 49.6116),  # Strasbourg
]

def plot_map():
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    
    # Set the extent (x0, x1, y0, y1) of the map in the given coordinate system.
    ax.set_extent([-5.266007882805498, 9.6624992762358, 41.303, 51.12421275782688], crs=ccrs.PlateCarree())
    
    # ax.add_feature(cfeature.LAND)
    # ax.add_feature(cfeature.OCEAN)
    ax.coastlines(resolution='10m')  # '50m'

    # Add France's boundaries with higher resolution
    borders = cfeature.NaturalEarthFeature(category='cultural',
                                           name='admin_0_boundary_lines_land',
                                           scale='10m', facecolor='none')

    #ax.add_feature(cfeature.COASTLINE)
    #ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(borders, edgecolor='black', linestyle=':')
    # ax.add_feature(cfeature.LAKES, alpha=0.5)
    # ax.add_feature(cfeature.RIVERS)

    # Plot the coordinates
    for lon, lat in COORDINATES_TO_PLOT:
        ax.scatter(lon, lat, transform=ccrs.PlateCarree(), color='red')

    # Add gridlines
    ax.gridlines(draw_labels=True)

    # Save the figure
    plt.savefig("france.svg", format='svg')
    plt.show()

plot_map()