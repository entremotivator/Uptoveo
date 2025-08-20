import streamlit as st
import requests

# ------------------------
# Configuration
# ------------------------
WEBHOOK_URL = "https://your-n8n-instance.com/webhook/segmind"

# ------------------------
# Streamlit UI
# ------------------------
st.title("Send Image & Prompt to n8n Webhook")

prompt = st.text_area("Enter your prompt", "A 3D animated cartoon-style young boy...")
duration = st.text_input("Duration (seconds)", "6")

uploaded_file = st.file_uploader("Upload first frame image", type=["png", "jpg", "jpeg"])
image_url_input = st.text_input("Or enter image URL")

go_fast = st.checkbox("Go Fast", value=True)
prompt_optimizer = st.checkbox("Prompt Optimizer", value=True)

if st.button("Send to n8n"):
    data = {
        "prompt": prompt,
        "duration": duration,
        "go_fast": go_fast,
        "prompt_optimizer": prompt_optimizer
    }

    files = {}
    if uploaded_file:
        files['first_frame_image'] = uploaded_file
    elif image_url_input:
        data['first_frame_image'] = image_url_input

    try:
        if files:
            response = requests.post(WEBHOOK_URL, data=data, files=files)
        else:
            response = requests.post(WEBHOOK_URL, json=data)
        
        if response.status_code == 200:
            st.success("Data sent successfully to n8n!")
        else:
            st.error(f"Error {response.status_code}: {response.text}")

    except Exception as e:
        st.error(f"Failed to send data: {e}")
