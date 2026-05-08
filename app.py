import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="TRACER-AI Diagnostic", layout="wide")

st.title("🛡️ TRACER-AI Diagnostic Mode")

# 1. Cek Koneksi Secrets
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ Secrets tidak terbaca di Streamlit Cloud!")
else:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    st.success("✅ API Key ditemukan di Secrets.")

    # 2. Test Koneksi Langsung ke Model Terbaru
    st.subheader("Test Koneksi AI")
    if st.button("Klik untuk Test Koneksi"):
        try:
            # Kita paksa pakai 1.5 Flash karena ini yang paling stabil untuk Free Tier
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content("Hello, are you active?")
            st.balloons()
            st.write("### 🚀 BERHASIL! AI Merespon:")
            st.info(response.text)
            st.write("Sekarang Anda bisa memasukkan kembali kode Dashboard TRACER-AI yang lengkap.")
        except Exception as e:
            st.error("⚠️ Error Asli dari Google detected:")
            st.code(str(e)) # Ini akan memunculkan kode error yang sebenarnya
            st.info("Jika muncul 'API_KEY_INVALID', berarti kunci Anda salah salin.")
            st.info("Jika muncul 'User location not supported', berarti server Streamlit butuh VPN (tapi jarang terjadi).")

st.divider()
st.caption("TRACER-AI Framework Tool Diagnostic")
