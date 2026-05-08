import streamlit as st
import google.generativeai as genai
import os

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="TRACER-AI Framework Dashboard", layout="wide")

# --- 2. KONEKSI API ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ API Key tidak ditemukan di Secrets Streamlit Cloud.")
    st.stop()

# --- 3. PENCARIAN MODEL OTOMATIS (SOLUSI 404) ---
@st.cache_resource
def load_model():
    # Mencoba daftar model yang paling umum didukung
    model_options = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    for m_name in model_options:
        try:
            m = genai.GenerativeModel(m_name)
            # Test kecil untuk memastikan model bisa merespon
            m.generate_content("test", generation_config={"max_output_tokens": 1})
            return m
        except:
            continue
    st.error("Semua model AI gagal dihubungi. Periksa kuota API Key Anda.")
    return None

model = load_model()

# --- 4. ANTARMUKA PENGGUNA (UI) ---
st.title("🛡️ TRACER-AI Framework Dashboard")
st.markdown("### *Transparent, Real-time, Accountable Collaborative Evaluation Record*")
st.caption("Prototype Penelitian R&D - Program Doktor Pendidikan Bahasa Inggris")

st.divider()

col_input, col_display = st.columns([1, 2])

with col_input:
    st.header("📝 Student Portal")
    with st.form("input_form"):
        name = st.text_input("Nama Lengkap Mahasiswa")
        role = st.selectbox("Peran dalam Proyek", ["Lead Writer", "Researcher", "Designer", "Editor", "Coordinator"])
        week = st.selectbox("Minggu Pengerjaan", ["Week 12", "Week 13", "Week 14", "Week 15"])
        logs = st.text_area("Log Aktivitas Mingguan", height=150)
        evidence = st.text_input("Link Bukti/Artifact")
        submitted = st.form_submit_button("Kirim ke TRACER-AI")

with col_display:
    st.header("🔍 Lecturer Dashboard")
    if submitted:
        if name and logs and evidence:
            with st.spinner("AI sedang menganalisis data..."):
                prompt = f"""
                Evaluate this student contribution based on TRACER-AI Rubric:
                NAME: {name} | ROLE: {role} | LOG: {logs} | EVIDENCE: {evidence}
                Provide score (0-100), Category, and Historical Description.
                """
                try:
                    response = model.generate_content(prompt)
                    st.success(f"Analisis Selesai!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Gagal memproses data: {e}")
        else:
            st.warning("Mohon lengkapi Nama, Log, dan Evidence.")

st.divider()
st.caption("TRACER-AI Framework - Research Prototype 2026")
