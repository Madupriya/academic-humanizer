import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(
    page_title="Academic AI Humanizer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Advanced Custom CSS & HTML Front-End Styling
st.markdown("""
<style>
    /* Global Styles & Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Background Accent */
    .stApp {
        background: radial-gradient(circle at top left, #0f172a, #020617);
    }

    /* Main Title with Vibrant Gradient */
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

    /* Glassmorphism Card Wrapper */
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

    /* Primary Action Button Customization */
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

    /* Input & Textarea Customization */
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

    /* Sidebar Aesthetic Customization */
    [data-testid="stSidebar"] {
        background-color: #090D16 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Custom Warning/Info Badges */
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

user_api_key = st.sidebar.text_input("🔑 ඔබේ Gemini API Key එක (Optional):", type="password")

if user_api_key.strip():
    active_api_key = user_api_key.strip()
    is_custom_key = True
    st.sidebar.success("⚡ ඔබේම API Key එක සක්‍රීයයි (Unlimited Words)")
else:
    if "GEMINI_API_KEY" in st.secrets:
        active_api_key = st.secrets["GEMINI_API_KEY"]
        is_custom_key = False
        st.sidebar.info("ℹ️ System Key එක සක්‍රීයයි (වචන 1,000 සීමාව)")
    else:
        active_api_key = None
        is_custom_key = False
        st.sidebar.warning("⚠️ System Key එක සෙට් කර නැත. Key එකක් ඇතුළත් කරන්න.")

with st.sidebar.expander("❓ නොමිලේ API Key එකක් හදාගන්නේ කොහොමද?"):
    st.markdown("""
    1. **[Google AI Studio](https://aistudio.google.com/)** වෙත යන්න.
    2. Google Account එකෙන් Sign In වෙන්න.
    3. **"Get API key"** > **"Create API key"** ලබාගන්න.
    4. Key එක මෙහි Sidebar එකට Paste කරන්න!
    """)

st.sidebar.markdown("---")
st.sidebar.caption("📌 Tip: Assignments & Research Papers වල AI pattern අයින් කිරීමට උපකාරී වේ.")

# 4. Hero Header Section
st.markdown("<div class='hero-title'>Academic AI Humanizer & Writing Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>AI මගින් ලියන ලද ලිපි Natural, Academic සහ Genuine Human Tone එකකට පරිවර්තනය කරන්න</div>", unsafe_allow_html=True)

# 5. Main Application Body with Columns
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #F8FAFC; margin-bottom: 1rem;'>📝 Input AI Content</h3>", unsafe_allow_html=True)
    
    academic_style = st.selectbox(
        "🎯 Writing Style එක තෝරන්න:",
        ["Academic / Research Paper", "University Student Assignment", "Formal Essay", "Natural & Simple English"]
    )
    
    input_text = st.text_area("මෙහි ඔබේ AI Text එක Paste කරන්න:", height=260, placeholder="Type or paste your AI-generated text here...")
    
    words = input_text.strip().split() if input_text.strip() else []
    word_count = len(words)
    
    if not is_custom_key:
        st.caption(f"📊 වචන ගණන: **{word_count} / 1000** (Default System Key)")
        if word_count > 1000:
            st.markdown("<div class='limit-badge'>⚠️ **වචන 1000 සීමාව පැන ඇත!** System Key එකෙන් වචන 1000ක් දක්වා පමණක් Humanize කළ හැක. Sidebar එකෙන් ඔබේම API Key එකක් ඇතුළත් කරන්න.</div>", unsafe_allow_html=True)
    else:
        st.caption(f"📊 වචන ගණන: **{word_count}** (Unlimited Mode - Custom Key)")

    humanize_btn = st.button("✨ Humanize Text Now")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #F8FAFC; margin-bottom: 1rem;'>✨ Humanized Output</h3>", unsafe_allow_html=True)
    
    if humanize_btn:
        if not input_text.strip():
            st.error("කරුණාකර Humanize කිරීමට Text එකක් ඇතුළත් කරන්න!")
        elif not is_custom_key and word_count > 1000:
            st.error("වචන 1000 සීමාව පැන ඇත. කරුණාකර Sidebar එකෙන් ඔබේම API Key එකක් ඇතුළත් කරන්න.")
        elif not active_api_key:
            st.error("API Key එකක් නොමැත. කරුණාකර Sidebar එකෙන් API Key එකක් ලබාදෙන්න.")
        else:
            with st.spinner("Text එක Humanize වෙමින් පවතී... මොහොතක් රැඳී සිටින්න."):
                try:
                    genai.configure(api_key=active_api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    prompt = f"""
                    You are an expert academic writing assistant and humanizer.
                    Rewrite the following text so that it sounds 100% natural, human-written, and suitable for university work.
                    
                    Instructions:
                    - Target Style: {academic_style}
                    - Remove robotic AI patterns, cliché transitions, and repetitive AI jargon (e.g., 'delve', 'testament', 'pivotal', 'furthermore', 'moreover').
                    - Use natural sentence structure, active voice, clear flow, and authentic vocabulary.
                    - Preserve all original core facts, figures, and technical meaning.
                    
                    Text to rewrite:
                    {input_text}
                    """
                    
                    response = model.generate_content(prompt)
                    st.text_area("Humanized Result:", value=response.text, height=295)
                    st.success("✅ සාර්ථකව Humanize කර අවසන්!")
                    
                except Exception as e:
                    st.error(f"Error එකක් සිදුවිය: {e}")
    else:
        st.info("Humanized Text එක මෙතනින් ලබාගැනීමට වම් පැත්තේ බටන් එක ඔබන්න.")
    st.markdown("</div>", unsafe_allow_html=True)

# 6. Video Tutorial Section at Bottom
st.markdown("---")
st.markdown("<h3 style='color: #F8FAFC;'>🎬 Guide & Video Tutorial</h3>", unsafe_allow_html=True)
st.write("App එක නිවැරදිව පාවිච්චි කරන ආකාරය පහත Video එකෙන් බලන්න:")

sample_video_url = "https://www.youtube.com/watch?v=dQw4w9XcQ"
st.video(sample_video_url)

# Footer
st.markdown("<br><p style='text-align: center; color: #64748B; font-size: 0.85rem;'>🎓 Academic AI Humanizer | Designed for University Students & Researchers</p>", unsafe_allow_html=True)