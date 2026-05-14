import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from utils.ai_analysis import analyze_geospatial_data

st.set_page_config(
    page_title="GeoSpatial AI Assistant",
    page_icon="",
    layout="wide"
)

st.title("GeoSpatial AI Assistant")
st.write("AI-powered assistant for geospatial data analysis.")

uploaded_file = st.file_uploader(
    "Upload a GeoJSON file",
    type=["geojson", "json"]
)

if uploaded_file:
    st.success("File uploaded successfully!")

    gdf = gpd.read_file(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(gdf.drop(columns="geometry", errors="ignore").head())

    st.subheader("Dataset Information")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Features", len(gdf))
    col2.metric("Columns", len(gdf.columns))
    col3.metric("Geometry Type", str(gdf.geometry.geom_type.iloc[0]))

    st.subheader("Interactive Map")

    center = [
        gdf.geometry.centroid.y.mean(),
        gdf.geometry.centroid.x.mean()
    ]

    m = folium.Map(location=center, zoom_start=12)

    folium.GeoJson(gdf).add_to(m)

    st_folium(m, width=1000, height=500)

    st.subheader("Ask AI about the dataset")

user_question = st.text_input(
    "Ask a geospatial question"
)

if user_question:

    with st.spinner("Analyzing geospatial data..."):

        data_summary = gdf.drop(
            columns="geometry",
            errors="ignore"
        ).to_string()

        ai_response = analyze_geospatial_data(
            data_summary,
            user_question
        )

        st.subheader("AI Response")

        st.write(ai_response)