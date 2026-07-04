import streamlit as st
import qrcode
from io import BytesIO

def generate_qr_code():
    form_link = "http://localhost:8501/Register%20Mobile%20Number"
    img = qrcode.make(form_link)

    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    st.image(buffer, caption="Scan this QR to register!", width=300)
