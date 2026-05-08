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
    st.error("API Key tidak ditemukan di Secrets.")
    st.stop()

# --- PERBAIKAN DI SINI: MENGGUNAKAN GEMINI 1.5 FLASH ---
model = genai.GenerativeModel('models/gemini-1.5-flash') 

# --- 3. ANTARMUKA PENGGUNA (UI) ---
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
        if name and logs:
            with st.spinner("AI sedang menganalisis data sesuai rubrik TRACER..."):
                # PROMPT ENGINEERING
                prompt = f"""
                You are a professor assistant. Evaluate this student contribution using TRACER-AI Rubric.
                NAME: {name}
                ROLE: {role}
                LOG: {logs}
                EVIDENCE: {evidence}
                
                Provide:
                1. Scores (0-100) for Transparency, Real-time, and Accountability.
                2. A "Historical Description" analysis.
                3. Identify if this student is a "Free-rider" or not.
                Format result in a clean Table and bullet points.
                """
                try:
                    response = model.generate_content(prompt)
                    st.success(f"Analisis Selesai!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Gagal menghubungi AI: {e}")
        else:
            st.warning("Mohon isi Nama dan Log.")

st.divider()
st.caption("TRACER-AI Framework - Research Prototype 2026")
