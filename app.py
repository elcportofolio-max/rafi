import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="TRACER-AI Model Scanner", layout="wide")
st.title("🛡️ TRACER-AI: Model Scanner Mode")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("API Key belum terpasang di Secrets.")
else:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)

    st.subheader("1. Daftar Model yang Tersedia untuk API Key Anda:")
    try:
        # Perintah untuk melihat model apa saja yang didukung oleh Kunci Anda
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        st.write("Silakan pilih salah satu model di bawah ini untuk ditest:")
        selected_model_name = st.selectbox("Pilih Model:", available_models)

        if st.button("Test Model yang Dipilih"):
            model = genai.GenerativeModel(selected_model_name)
            response = model.generate_content("Hello, this is a test.")
            st.success(f"✅ BERHASIL! Model '{selected_model_name}' merespon.")
            st.info(f"AI Say: {response.text}")
            st.warning(f"Gunakan nama '{selected_model_name}' di kode final Anda nanti.")
            
    except Exception as e:
        st.error("⚠️ Gagal mengambil daftar model:")
        st.code(str(e))

st.divider()
st.caption("TRACER-AI Diagnostic System 2026")
