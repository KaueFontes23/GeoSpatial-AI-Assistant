import streamlit as st
import geopandas as gpd
import folium
import streamlit.components.v1 as components
import base64
import html
import textwrap
from streamlit_folium import st_folium
from utils.ai_analysis import analyze_geospatial_data
from utils.spatial_analysis import generate_spatial_summary




def load_css():

    with open("styles/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

st.set_page_config(
    page_title="GeoSpatial AI Assistant",
    page_icon="assets/icon.png",
    layout="wide"
)

load_css()

def get_base64_image(image_path):

    with open(image_path, "rb") as img_file:

        return base64.b64encode(
            img_file.read()
        ).decode()

with open("assets/logo.png", "rb") as image_file:
    logo_base64 = base64.b64encode(
        image_file.read()
    ).decode()

components.html(f"""
<div class="hero-card">

    <img
        src="data:image/png;base64,{logo_base64}"
        class="hero-logo"
    >

    <div class="hero-text">

        <h2>
            Helping you with
            <span id="changing-text">
                ArcGIS workflows
            </span>
        </h2>

        <p>
            Start by uploading your GeoJSON file on the left sidebar.
        </p>

    </div>

</div>

<style>

.hero-card {{
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 28px;

    width: 100%;
    height: 180px;
    box-sizing: border-box;

    backdrop-filter: blur(14px);
    border-radius: 24px;

    padding: 10px 38px;
    padding-top: 42px;

    font-family: Arial, sans-serif;
}}

.hero-logo {{
    width: 360px;
    height: auto;
    object-fit: contain;
    opacity: 0.96;
    filter: drop-shadow(0 0 20px rgba(57,255,136,0.15));
}}

.hero-text {{
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

.hero-text h2 {{
    color: rgba(57, 255, 136, 0.72);
    font-size: 24px;
    margin: 0 0 10px 0;
}}

.hero-text p {{
    color: #9ca3af;
    font-size: 15px;
    margin: 0;
}}

</style>

<script>

const words = [
    "ArcGIS workflows",
    "interactive maps",
    "GeoJSON files",
    "spatial analysis",
    "GIS automation",
    "AI geospatial insights"
];

let index = 0;

setInterval(() => {{
    index = (index + 1) % words.length;
    document.getElementById("changing-text").innerText = words[index];
}}, 1800);

</script>
""", height=220)


with st.sidebar:

    st.markdown("""
    <div class="sidebar-header">
        <h2>GeoSpatial AI</h2>
        <p>Geospatial intelligence workspace</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### Dataset")

    uploaded_file = st.file_uploader(
        "Upload GeoJSON file",
        type=["geojson", "json"]
    )

    st.markdown("---")

    st.markdown("### AI Engine")

    st.markdown("""
    <div class="sidebar-pill">Spatial Analysis</div>
    <div class="sidebar-pill">AI Insights</div>
    <div class="sidebar-pill">GIS Automation</div>
    <div class="sidebar-pill">ArcGIS Concepts</div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div class="sidebar-footer">
        GeoSpatial AI Assistant<br>
        <span>by Kauê Fontes</span>
    </div>
    """, unsafe_allow_html=True)

if uploaded_file:

    st.success("File uploaded successfully!")

    gdf = gpd.read_file(uploaded_file)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="card-title">Total Features</div>
            <div class="card-value">{len(gdf)}</div>
            <div class="card-positive">Spatial records loaded</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="card-title">Columns</div>
            <div class="card-value">{len(gdf.columns)}</div>
            <div class="card-positive">Dataset attributes</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        geometry_type = str(gdf.geometry.geom_type.iloc[0])
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="card-title">Geometry Type</div>
            <div class="card-value">{geometry_type}</div>
            <div class="card-positive">GIS layer detected</div>
        </div>
        """, unsafe_allow_html=True)

        with col4:
            st.markdown("""
        <div class="dashboard-card">
            <div class="card-title">AI Engine</div>
            <div class="card-value">Ready</div>
            <div class="card-positive">OpenAI pipeline connected</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## Interactive Map")

    center = [
        gdf.geometry.centroid.y.mean(),
        gdf.geometry.centroid.x.mean()
    ]

    m = folium.Map(
        location=center,
        zoom_start=12,
        tiles="CartoDB dark_matter"
    )

    folium.GeoJson(
        gdf,
        name="GeoJSON Layer"
    ).add_to(m)

    st_folium(
        m,
        width=1200,
        height=520
    )
    
    st.subheader("Spatial Analysis")

    spatial_summary = generate_spatial_summary(gdf)

    st.json(spatial_summary)

    st.subheader("Ask AI about the dataset")

    user_question = st.text_input("Ask a geospatial question")

    if user_question:

        with st.spinner("Analyzing geospatial data..."):

            data_summary = gdf.drop(
                columns="geometry",
                errors="ignore"
            ).head(10).to_string()

            ai_response = analyze_geospatial_data(
                data_summary,
                user_question
            )

        safe_response = html.escape(ai_response)

        ai_card = f"""
    <div style="background: rgba(5, 8, 12, 0.95); border: 1px solid rgba(57,255,136,0.22); border-radius: 22px; padding: 24px; margin-top: 20px; box-shadow: 0 0 30px rgba(57,255,136,0.08);">
        <div style="color: rgba(57,255,136,0.9); font-size: 20px; font-weight: 700; margin-bottom: 16px;">
            AI Spatial Insights
        </div>
        <div style="color: rgba(57,255,136,0.78); font-size: 15px; line-height: 1.7; white-space: pre-wrap; font-family: Arial, sans-serif;">
            {safe_response}
        </div>
    </div>
    """

        st.markdown(ai_card, unsafe_allow_html=True)