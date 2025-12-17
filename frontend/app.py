import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="Chatbot Kampus Vokasi", layout="wide")
st.title("Chatbot Kampus Vokasi 💬")

# --- Load data ---
txt_path = os.path.join("frontend", "data.txt")
json_path = os.path.join("frontend", "data.json")

txt_content = open(txt_path, "r", encoding="utf-8").read() if os.path.exists(txt_path) else ""
json_content = ""
if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, dict):
            json_content = " ".join([str(v) for v in data.values()])
        elif isinstance(data, list):
            json_content = " ".join([str(v) for item in data for v in (item.values() if isinstance(item, dict) else [item])])

# --- Pilih sumber data ---
option = st.selectbox("Pilih sumber data:", ["TXT", "JSON"])
data_text = txt_content if option == "TXT" else json_content
st.write("Data berhasil dimuat!" if data_text else "Tidak ada data.")

# --- Inisialisasi history ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- Input user ---
user_input = st.text_input("Tanya sesuatu:")

if st.button("Kirim") and user_input.strip():
    if not data_text:
        st.error("Tidak ada data untuk dijadikan konteks.")
    else:
        prompt = f"{data_text}\nUser: {user_input}"
        try:
            res = requests.post(
                "http://127.0.0.1:8000/chat",  # URL backend FastAPI
                json={"prompt": prompt},
                timeout=90
            )
            res.raise_for_status()
            reply = res.json().get("reply", "")
        except requests.exceptions.RequestException as e:
            reply = f"Error API: {e}"

        st.session_state.history.append({"user": user_input, "reply": reply})

# --- Tampilkan chat history ---
for chat in st.session_state.history:
    st.markdown(f"**Kamu:** {chat['user']}")
    st.markdown(f"**Bot:** {chat['reply']}")
    st.markdown("---")
