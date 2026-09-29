import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(
    page_title="Academic AI Humanizer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Advanced Custom CSS Styling (Dark Academic Theme)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at top left, #0f172a, #020617);
    }

    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60A5FA 0%, #A78BFA 50%, #F472B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: #94A3B8;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    .custom-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #2563EB 0%, #3B82F6 100%);
        color: #FFFFFF;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 14px 0 rgba(37, 99, 235, 0.39);
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #2563EB 100%);
        box-shadow: 0 6px 20px 0 rgba(37, 99, 235, 0.6);
        transform: translateY(-2px);
        color: #FFFFFF;
    }

    .stTextArea textarea {
        background-color: #0F172A !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        color: #F8FAFC !important;
        font-size: 0.95rem !important;
    }

    .stTextArea textarea:focus {
        border-color: #60A5FA !important;
        box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.2) !important;
    }

    [data-testid="stSidebar"] {
        background-color: #090D16 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    .limit-badge {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
        color: #FBBF24;
        padding: 0.75rem 1rem;
        border-radius: 10px;
        font-size: 0.9rem;
        margin-top: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar Setup
st.sidebar.markdown("<h2 style='color: #F8FAFC;'>🎓 Academic Hub</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

user_api_key = st.sidebar.text_input("🔑 Custom Gemini API Key (Optional):", type="password")

if user_api_key.strip():
    active_api_key = user_api_key.strip()
    is_custom_key = True
    st.sidebar.success("⚡ Custom API Key Active (Unlimited Words)")
else:
    if "GEMINI_API_KEY" in st.secrets:
        active_api_key = st.secrets["GEMINI_API_KEY"]
        is_custom_key = False
        st.sidebar.info("ℹ️ System API Key Active (1,000 Word Limit)")
    else:
        active_api_key = None
        is_custom_key = False
        st.sidebar.warning("⚠️ System Key missing. Please provide an API key.")

with st.sidebar.expander("❓ How to get a FREE API key?"):
    st.markdown("""
    1. Visit **[Google AI Studio](https://aistudio.google.com/)**.
    2. Sign in with your Google Account.
    3. Click **"Get API key"** > **"Create API key"**.
    4. Copy and paste your key in the sidebar field above!
    """)

st.sidebar.markdown("---")
st.sidebar.caption("📌 Designed to eliminate AI patterns in academic essays, reports, and research papers.")

# 4. Hero Header Section
st.markdown("<div class='hero-title'>Academic AI Humanizer & Writing Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>Transform AI-generated text into natural, authentic, and human-sounding academic content</div>", unsafe_allow_html=True)

# 5. Main Content Area
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #F8FAFC; margin-bottom: 1rem;'>📝 Input Content</h3>", unsafe_allow_html=True)
    
    academic_style = st.selectbox(
        "🎯 Select Target Writing Style:",
        ["Academic / Research Paper", "University Student Assignment", "Formal Essay", "Natural & Simple Prose"]
    )
    
    input_text = st.text_area("Paste your AI-generated text below:", height=260, placeholder="Type or paste your content here...")
    
    words = input_text.strip().split() if input_text.strip() else []
    word_count = len(words)
    
    if not is_custom_key:
        st.caption(f"📊 Word Count: **{word_count} / 1000** (Default Free Tier)")
        if word_count > 1000:
            st.markdown("<div class='limit-badge'>⚠️ **1000 Words Limit Exceeded!** The free system key supports up to 1000 words per execution. Enter your free custom API key in the sidebar for unlimited usage.</div>", unsafe_allow_html=True)
    else:
        st.caption(f"📊 Word Count: **{word_count}** (Unlimited Mode - Custom API Key)")

    humanize_btn = st.button("✨ Humanize Text Now")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #F8FAFC; margin-bottom: 1rem;'>✨ Humanized Output</h3>", unsafe_allow_html=True)
    
    if humanize_btn:
        if not input_text.strip():
            st.error("Please enter some text to humanize!")
        elif not is_custom_key and word_count > 1000:
            st.error("Word count exceeds the 1000-word limit. Please add your personal API key in the sidebar.")
        elif not active_api_key:
            st.error("No API Key detected. Please provide a valid Gemini API Key.")
        else:
            with st.spinner("Humanizing your text... Please wait a moment."):
                try:
                    genai.configure(api_key=active_api_key)
                    
                    prompt = f"""
                    You are an expert academic writing editor and humanizer.
                    Rewrite the following text so that it sounds 100% natural, human-written, and appropriate for higher education academic work.
                    
                    Guidelines:
                    - Target Style: {academic_style}
                    - Eliminate obvious robotic AI patterns, cliché transition phrases, and overused buzzwords (e.g., 'delve', 'testament', 'pivotal', 'furthermore', 'moreover', 'beacon', 'realm').
                    - Utilize varied sentence structures, natural flow, active voice, and realistic academic vocabulary.
                    - Preserve all original core technical facts, terminology, formulas, and meaning without oversimplification.
                    
                    Text to rewrite:
                    {input_text}
                    """
                    
                    # Robust Model Call with Fallback
                    try:
                        model = genai.GenerativeModel('gemini-2.0-flash')
                        response = model.generate_content(prompt)
                    except Exception:
                        model = genai.GenerativeModel('gemini-1.5-flash-latest')
                        response = model.generate_content(prompt)
                        
                    st.text_area("Humanized Result:", value=response.text, height=295)
                    st.success("✅ Text successfully humanized!")
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")
    else:
        st.info("Click 'Humanize Text Now' to generate humanized academic content.")
    st.markdown("</div>", unsafe_allow_html=True)

# 6. Video Tutorial Section
st.markdown("---")
st.markdown("<h3 style='color: #F8FAFC;'>🎬 User Guide & Video Tutorial</h3>", unsafe_allow_html=True)
st.write("Watch the video below to learn how to get your free API key and get the best results:")

sample_video_url = "https://www.youtube.com/watch?v=1LrSwbmFPSs&list=RDR2X5_PWVoJ4&index=14"
st.video(sample_video_url)

# Footer
st.markdown("<br><p style='text-align: center; color: #64748B; font-size: 0.85rem;'>🎓 Academic AI Humanizer | Designed for University Students & Researchers</p>", unsafe_allow_html=True)