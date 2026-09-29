import streamlit as st
import google.generativeai as genai

# 1. Page Configuration (Academic & Clean Theme)
st.set_page_config(
    page_title="Academic AI Humanizer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (CSS) for Academic UI
st.markdown("""
<style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 700;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        text-align: center;
        margin-bottom: 1.8rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #2563EB;
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.6rem;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
        color: white;
    }
    .warning-box {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 0.9rem;
        border-radius: 8px;
        border-left: 5px solid #F59E0B;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# 2. Sidebar Settings & API Key Management
st.sidebar.title("🎓 Academic Hub")
st.sidebar.markdown("---")

# User Custom API Key Input
user_api_key = st.sidebar.text_input("🔑 ඔබේ Gemini API Key එක ඇතුළත් කරන්න (Optional):", type="password")

# Key & Limit Selection Logic
if user_api_key.strip():
    active_api_key = user_api_key.strip()
    is_custom_key = True
    st.sidebar.success("✅ ඔබේම API Key එක සක්‍රීයයි! (Unlimited Words)")
else:
    # Uses Developer's System Key from Streamlit Secrets
    if "GEMINI_API_KEY" in st.secrets:
        active_api_key = st.secrets["GEMINI_API_KEY"]
        is_custom_key = False
        st.sidebar.info("ℹ️ System API Key එක සක්‍රීයයි (වචන 1,000 සීමාවක් සහිතව)")
    else:
        active_api_key = None
        is_custom_key = False
        st.sidebar.warning("⚠️ System Key එකක් සෙට් කර නැත. කරුණාකර API Key එකක් ඇතුළත් කරන්න.")

# Guide to Get Free API Key
with st.sidebar.expander("❓ නොමිලේ API Key එකක් සාදාගන්නේ කෙසේද?"):
    st.markdown("""
    1. **[Google AI Studio](https://aistudio.google.com/)** වෙත යන්න.
    2. ඔබේ Google Account එකෙන් Sign In වෙන්න.
    3. **"Get API key"** ක්ලික් කර **"Create API key"** ලබාගන්න.
    4. ලැබුණු Key එක මෙහි Sidebar එකේ ඇති කොටුවට Paste කරන්න!
    """)

st.sidebar.markdown("---")
st.sidebar.caption("📌 Tip: Assignment / Thesis වල AI detection අඩු කිරීමට මෙය උපකාරී වේ.")

# 3. Main Application Interface
st.markdown("<div class='main-title'>🎓 Academic AI Humanizer & Writing Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>AI මගින් ලියන ලද ලිපි ස්වාභාවික, Academic සහ Human Tone එකකට පරිවර්තනය කරන්න</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Input AI Content")
    
    academic_style = st.selectbox(
        "🎯 Writing Style එක තෝරන්න:",
        ["Academic / Research Paper", "University Student Assignment", "Formal Essay", "Natural & Simple English"]
    )
    
    input_text = st.text_area("මෙහි ඔබේ AI Text එක Paste කරන්න:", height=280, placeholder="Enter text here...")
    
    # Calculate Word Count
    words = input_text.strip().split() if input_text.strip() else []
    word_count = len(words)
    
    # Check Word Limit
    if not is_custom_key:
        st.caption(f"📊 වචන ගණන: **{word_count} / 1000** (Default System Key)")
        if word_count > 1000:
            st.markdown("<div class='warning-box'>⚠️ **වචන 1000 සීමාව පැන ඇත!** System Key එකෙන් වචන 1000ක් දක්වා පමණක් Humanize කළ හැක. කරුණාකර Sidebar එකෙන් ඔබේම නොමිලේ API Key එකක් එක් කරන්න.</div>", unsafe_allow_html=True)
    else:
        st.caption(f"📊 වචන ගණන: **{word_count}** (Unlimited Mode - Custom API Key)")

    humanize_btn = st.button("✨ Humanize Text")

with col2:
    st.subheader("✨ Humanized Academic Result")
    
    if humanize_btn:
        if not input_text.strip():
            st.error("කරුණාකර Humanize කිරීමට Text එකක් ඇතුළත් කරන්න!")
        elif not is_custom_key and word_count > 1000:
            st.error("වචන 1000 සීමාව පැන ඇත. කරුණාකර Sidebar එකෙන් ඔබේම API Key එකක් ඇතුළත් කරන්න.")
        elif not active_api_key:
            st.error("API Key එකක් නොමැත. කරුණාකර Sidebar එකෙන් API Key එකක් ලබාදෙන්න.")
        else:
            with st.spinner("AI Text එක Humanize කරමින් පවතී... කරුණාකර රැඳී සිටින්න."):
                try:
                    genai.configure(api_key=active_api_key)
                    
                    # Using Gemini 1.5 Flash Model
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    prompt = f"""
                    You are an expert academic writing assistant and humanizer.
                    Your task is to rewrite the following text so that it sounds 100% natural, human-written, and suitable for academic/university work.
                    
                    Instructions:
                    - Target Style: {academic_style}
                    - Remove robotic AI patterns, cliché transitions, and repetitive AI jargon (e.g., 'delve', 'testament', 'pivotal', 'furthermore', 'moreover').
                    - Use natural sentence structure, active voice, clear flow, and authentic vocabulary.
                    - Preserve all original core facts, figures, and technical meaning.
                    
                    Text to rewrite:
                    {input_text}
                    """
                    
                    response = model.generate_content(prompt)
                    result_text = response.text
                    
                    st.text_area("Humanized Output:", value=result_text, height=280)
                    st.success("✅ සාර්ථකව Humanize කර අවසන්!")
                    
                except Exception as e:
                    st.error(f"Error එකක් සිදුවිය: {e}")

# 4. Video Tutorial / Guide Section at the Bottom
st.markdown("---")
st.subheader("🎬 App එක සහ API Key එක පාවිච්චි කරන හැටි (Video Tutorial)")
st.write("මෙම App එකෙන් නිවැරදිව ප්‍රයෝජන ගන්නා ආකාරය පහත Video එකෙන් නරඹන්න:")

# Video Container (You can replace this URL with your AI Video URL later)
sample_video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
st.video(sample_video_url)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #6B7280; font-size: 0.9rem;'>🎓 Academic AI Humanizer | Designed for University Students & Researchers</p>", unsafe_allow_html=True)