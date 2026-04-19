
import streamlit as st
import requests
import base64
from PIL import Image
import os

st.set_page_config(
    page_title="Vehicle Damage Detector",
    page_icon="🚗",
    layout="wide"
)

# ============================================
# CONFIG — Update these values
# ============================================
API_URL = os.environ.get(
    "API_URL",
    "https://g4t96in5x2.execute-api.us-east-1.amazonaws.com/prod/analyze"
)

st.title("🚗 Vehicle Damage Detection System")
st.subheader("AI-Powered Insurance Report Generator")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.header("📸 Upload Vehicle Image")
    uploaded_file = st.file_uploader(
        "Choose a car image",
        type=["jpg", "jpeg", "png"]
    )
    if uploaded_file:
        st.image(
            Image.open(uploaded_file),
            caption="Uploaded Image",
            use_column_width=True
        )

with col2:
    st.header("📋 Damage Report")
    if uploaded_file and st.button(
            "🔍 Analyze Damage", type="primary"):
        with st.spinner("Analyzing damage..."):
            img_b64  = base64.b64encode(
                uploaded_file.getvalue()).decode()
            response = requests.post(
                API_URL,
                json={"image": img_b64},
                headers={
                    "Content-Type": "application/json"
                }
            )
            result = response.json()

        if result.get("success"):
            pred = result["prediction"]
            conf = result["confidence"]
            sev  = result["severity"]

            if pred == "damaged":
                st.error("⚠️ DAMAGE DETECTED!")
            else:
                st.success("✅ NO DAMAGE DETECTED!")

            col3, col4, col5 = st.columns(3)
            col3.metric("Prediction", pred.upper())
            col4.metric("Confidence", f"{conf:.1%}")
            col5.metric("Severity",   sev)

            if result.get("damage_labels"):
                st.warning(
                    f"Damage: "
                    f"{', '.join(result['damage_labels'])}"
                )

            st.text_area(
                "Full Report",
                result.get("report_text", ""),
                height=300
            )
            st.caption(
                f"Report ID: {result.get('report_id')}"
            )
        else:
            st.error(f"Error: {result.get('error')}")

st.markdown("---")
st.caption(
    "Powered by AWS SageMaker + Rekognition + Lambda"
)
