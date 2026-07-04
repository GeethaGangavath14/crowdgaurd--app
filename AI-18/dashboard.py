import streamlit as st
import pandas as pd
import time
import streamlit.components.v1 as components
import os
import webbrowser
from prediction_model import predict_crowd, plot_prediction

# === SETTINGS ===
st.set_page_config(page_title="Smart Evacuation Admin", layout="wide")
CROWD_LIMIT = 20
REFRESH_INTERVAL_SEC = 60  # in seconds

# === PAGE TITLE ===
st.title("🚨 Smart Evacuation Admin Dashboard")
st.markdown("---")

# === REFRESH TIMER ===
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()
else:
    elapsed = time.time() - st.session_state.last_refresh
    if elapsed > REFRESH_INTERVAL_SEC:
        st.session_state.last_refresh = time.time()
        st.experimental_rerun()

# === COLUMNS ===
col1, col2 = st.columns(2)

# === COLUMN 1: Heatmap ===
with col1:
    st.header("Crowd Monitoring Heatmap")

    if st.button("Open Live Heatmap in Browser 🌐"):
        html_path = os.path.abspath("templates/heatmap.html")
        webbrowser.open_new_tab(f"file://{html_path}")


    st.subheader("🔴 Live Heatmap Below")
    heatmap_placeholder = st.empty()

# === COLUMN 2: Prediction Graph ===
with col2:
    st.header("Crowd Prediction Graph")

    if st.button("Generate Prediction Graph 📈"):
        plot_prediction()
        st.image('templates/prediction_graph.png', use_column_width=True)

    st.subheader("👥 Live Crowd Count")
    crowd_count_placeholder = st.empty()

st.markdown("---")

# === Predict Future ===
if st.button("Predict Future Crowding 🔮"):
    predictions = predict_crowd()
    st.write(predictions)

st.success("✅ All systems active!")

# === FUNCTIONS ===
def load_heatmap():
    try:
        with open('templates/heatmap.html', 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "<h3>⚠️ Heatmap not available yet.</h3>"

def get_latest_crowd_count():
    try:
        df = pd.read_csv('crowd_data.csv')
        latest_count = df.iloc[-1]['count']
        return int(latest_count)
    except:
        return 0

# === LIVE UPDATE ===
with st.spinner("🔄 Updating heatmap and crowd count..."):
    heatmap_html = load_heatmap()
    components.html(heatmap_html, width=800, height=600, scrolling=True)

    live_count = get_latest_crowd_count()
    if live_count >= CROWD_LIMIT:
        crowd_count_placeholder.error(f"⚠️ Overcrowding Detected! Current Count: {live_count}")
    else:
        crowd_count_placeholder.metric("👥 Current Crowd Count", live_count)
