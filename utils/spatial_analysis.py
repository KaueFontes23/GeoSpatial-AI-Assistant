def generate_spatial_summary(gdf):

    summary = {}

    summary["total_features"] = len(gdf)

    summary["geometry_types"] = (
        gdf.geometry.geom_type.unique().tolist()
    )

    try:

        summary["total_area"] = round(
            gdf.geometry.area.sum(),
            2
        )

    except:
        summary["total_area"] = "Unavailable"

    try:

        centroids = gdf.geometry.centroid

        summary["average_latitude"] = round(
            centroids.y.mean(),
            4
        )

        summary["average_longitude"] = round(
            centroids.x.mean(),
            4
        )

    except:

        summary["average_latitude"] = "Unavailable"
        summary["average_longitude"] = "Unavailable"

    return summary