import streamlit as st
from utils import extract_resume_text
from analyzer import analyze_resume
from pdf_generator import create_pdf

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Resume Intelligence",
    page_icon="🟡",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #000000, #111111, #1a1a1a);
    color: white;
}

/* Hero Card */
.hero-card {
    border: 2px solid #FFD700;
    border-radius: 25px;
    padding: 50px;
    text-align: center;
    margin-bottom: 30px;
    background: linear-gradient(135deg, #000000, #1a1a1a);
    box-shadow: 0px 0px 25px rgba(255,215,0,0.25);
}

/* Upload Box */
[data-testid="stFileUploader"] {
    border: 2px solid #FFD700 !important;
    border-radius: 15px;
    padding: 12px;
    background-color: rgba(255,215,0,0.05);
    box-shadow: 0px 0px 12px rgba(255,215,0,0.25);
}

/* Role Input */
.stTextInput input {
    border: 2px solid #FFD700 !important;
    border-radius: 12px;
    background-color: #111111 !important;
    color: white !important;
    box-shadow: 0px 0px 12px rgba(255,215,0,0.25);
}

/* Labels */
label {
    color: #FFD700 !important;
    font-weight: bold !important;
}

/* Button */
div.stButton > button {
    width: 100%;
    height: 60px;
    border-radius: 15px;
    border: none;
    font-size: 20px;
    font-weight: bold;
    background: linear-gradient(90deg,#FFD700,#FFC107);
    color: black;
}

div.stButton > button:hover {
    box-shadow: 0px 0px 20px #FFD700;
    transform: scale(1.02);
}

/* Tabs */
button[data-baseweb="tab"] {
    background-color: #111111;
    color: white;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #FFD700;
    border-bottom: 2px solid #FFD700;
}

/* Footer */
.footer-text {
    text-align: center;
    color: #F3F4F6;
    font-size: 18px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HERO SECTION
# =========================

st.markdown("""
<div class="hero-card">

<h1 style="color:#FFD700;">
RESUME INTELLIGENCE
</h1>
            
<h3 style="color:white;">
Professional Resume Analysis
</h3>

<p style="color:#d1d5db;font-size:18px;">
Upload your resume and receive ATS scoring, resume improvement suggestions,
and role-specific interview questions.
</p>

</div>
""", unsafe_allow_html=True)

# =========================
# INPUT SECTION
# =========================

col1, col2 = st.columns([2,1])

with col1:
    uploaded_file = st.file_uploader(
        "📄 Upload Resume",
        type=["pdf"]
    )

with col2:
    job_role = st.text_input(
        "🎯 Target Job Role",
        placeholder="Data Analyst"
    )

st.markdown("---")

# =========================
# ANALYSIS
# =========================

if uploaded_file:

    st.success("✅ Resume uploaded successfully!")

    resume_text = extract_resume_text(uploaded_file)

    analyze_btn = st.button(
        "🚀 Analyze Resume",
        use_container_width=True
    )

    if analyze_btn:

        with st.spinner("🔍 Gemini is analyzing your resume..."):

            result = analyze_resume(
                resume_text,
                job_role
            )

        st.markdown("---")

        tab1, tab2 = st.tabs(
            [
                "📄 Analysis",
                "📑 Resume Text"
            ]
        )

        with tab1:
            st.subheader("Resume Analysis")
            st.markdown(result)

        with tab2:
            st.subheader("Extracted Resume")

            st.text_area(
                "Resume Content",
                resume_text,
                height=400
            )
        st.markdown("---")

        pdf = create_pdf(
            result,
            job_role if job_role else "General"
        )

        st.download_button(
            label="📥 Download PDF Report",
            data=pdf,
            file_name="Resume_Intelligence_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

# =========================
# FOOTER
# =========================

st.markdown("---")

st.markdown(
    """
    <div class="footer-text">
        Developed by Koushik Mangalagiri
    </div>
    """,
    unsafe_allow_html=True
)
