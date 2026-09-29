import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="Custom Academic Humanizer", page_icon="🎓", layout="wide")

st.title("🎓 Custom Academic Text Humanizer")
st.write("Gemini API එක පාවිච්චි කරලා AI Text එකක් Word Limit නැතුව Natural Humanized Text එකකට හරවගන්න.")

# Sidebar for API Key & Settings
st.sidebar.header("⚙️ Settings")
api_key = st.sidebar.text_input("Gemini API Key එක ඇතුළත් කරන්න:", type="password")

tone = st.sidebar.selectbox(
    "Tone එක තෝරන්න:",
    ["Natural Academic Student", "Conversational & Simple", "Formal Research Paper"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 API Key එක ලබාගැනීමට: [Google AI Studio](https://aistudio.google.com/) වෙත යන්න.")

# Main Input UI
text_input = st.text_area("Humanize කිරීමට අවශ්‍ය AI Text එක මෙතනට Paste කරන්න:", height=250)

if st.button("🚀 Humanize Text Now", type="primary"):
    if not api_key:
        st.error("කරුණාකර Sidebar එකට Gemini API Key එක ඇතුළත් කරන්න!")
    elif not text_input.strip():
        st.warning("කරුණාකර Text එකක් ඇතුළත් කරන්න!")
    else:
        try:
            # Configure Gemini
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")

            with st.spinner("Text එක Humanize වෙමින් පවතී... මොහොතක් රැඳී සිටින්න."):
                # Custom Engineered Prompt
                prompt = f"""
                You are an expert academic editor. Rewrite the following text so that it sounds like it was written by a genuine university student with a {tone} writing style.

                STRICT RULES:
                1. Vary sentence length and structure (mix short and complex sentences naturally).
                2. Use active voice and natural transitions between paragraphs.
                3. Completely eliminate obvious AI words and overused buzzwords (e.g., 'delve', 'testament', 'crucial', 'furthermore', 'moreover', 'multifaceted', 'in conclusion', 'beacon', 'realm').
                4. CRITICAL: ABSOLUTELY DO NOT change, alter, or simplify any technical engineering, scientific, or academic terminology, formulas, or core subject concepts. Keep them 100% accurate.
                5. Maintain original logic, meaning, and key references.

                Text to rewrite:
                {text_input}
                """

                response = model.generate_content(prompt)

                st.subheader("✅ Humanized Output:")
                st.write(response.text)

                # Word count check
                orig_words = len(text_input.split())
                new_words = len(response.text.split())
                st.caption(f"Original Words: {orig_words} | Humanized Words: {new_words}")

        except Exception as e:
            st.error(f"Error එකක් ආවා: {str(e)}")