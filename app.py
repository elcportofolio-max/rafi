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

# MENGGUNAKAN MODEL YANG BERHASIL DITEST: gemini-2.5-flash
MODEL_NAME = 'models/gemini-2.5-flash'
model = genai.GenerativeModel(MODEL_NAME)

# --- 3. ANTARMUKA PENGGUNA (UI) ---
st.title("🛡️ TRACER-AI Framework Dashboard")
st.markdown("### *Transparent, Real-time, Accountable Collaborative Evaluation Record*")
st.caption("Prototype Penelitian R&D - Program Doktor Pendidikan Bahasa Inggris")

st.divider()

# Membuat dua kolom: Kolom Kiri untuk Input Mahasiswa, Kolom Kanan untuk Hasil AI
col_input, col_display = st.columns([1, 2])

with col_input:
    st.header("📝 Student Portal")
    st.info("Mahasiswa: Masukkan log aktivitas mingguan Anda di sini.")
    with st.form("input_form"):
        st.subheader("Informasi Mahasiswa")
        name = st.text_input("Nama Lengkap Mahasiswa")
        role = st.selectbox("Peran dalam Proyek", ["Lead Writer", "Researcher", "Designer", "Editor", "Coordinator"])
        
        st.subheader("Historical Record (Proses)")
        week = st.selectbox("Minggu Pengerjaan", ["Week 12", "Week 13", "Week 14", "Week 15"])
        logs = st.text_area("Log Aktivitas Mingguan (Jelaskan detail apa yang Anda kerjakan)", height=150)
        evidence = st.text_input("Link Bukti/Artifact (Google Docs/Drive/PDF)")
        
        submitted = st.form_submit_button("Kirim ke TRACER-AI")

with col_display:
    st.header("🔍 Lecturer Dashboard")
    if submitted:
        if name and logs and evidence:
            with st.spinner("AI sedang menganalisis data historis sesuai rubrik TRACER..."):
                # LOGIKA PROMPT (Sesuai Desain Bab 3)
                prompt = f"""
                You are a Senior Professor specializing in Instructional Design and Assessment. 
                Evaluate the following student contribution based on the TRACER-AI Analytic Rubric.

                STUDENT DATA:
                Name: {name}
                Role: {role}
                Timeframe: {week}
                Activity Log: {logs}
                Evidence Artifact: {evidence}

                EVALUATION CRITERIA (TRACER Pillars):
                1. Transparent (T): Clarity of roles and workflow visibility.
                2. Real-time (R): Consistency of progress and responsiveness.
                3. Accountable (A): Alignment between claims and evidence.

                OUTPUT REQUIREMENT:
                1. Provide a SCORE (0-100) for each pillar.
                2. Determine the CATEGORY (Very Good, Good, Fair, or Poor).
                3. Write a 'HISTORICAL DESCRIPTION' summary (max 150 words).
                4. FREE-RIDER DETECTION: Analyze if the student is a genuine contributor or a free-rider.
                
                Please format the response using professional Markdown with a Table for scores.
                """
                
                try:
                    response = model.generate_content(prompt)
                    st.success(f"Analisis untuk {name} Selesai!")
                    st.markdown("---")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Gagal memproses data dengan model {MODEL_NAME}: {e}")
        else:
            st.warning("Mohon lengkapi Nama, Log Aktivitas, dan Link Bukti untuk memulai analisis.")
    else:
        st.info("Dashboard ini akan menampilkan analisis otomatis AI setelah mahasiswa mengirimkan data.")

st.divider()
st.caption("TRACER-AI Framework - Research Prototype 2026 - English Education")
