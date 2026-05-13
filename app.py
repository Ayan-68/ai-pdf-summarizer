from google import genai
from pypdf import PdfReader
import streamlit as st

# Page config
st.set_page_config(
    page_title="AI PDF Summarizer",
    page_icon="📄",
    layout="wide"
)

# Title
st.title("📄 AI PDF Summarizer")

st.markdown("""
Upload a PDF document and generate an AI-powered summary.
""")

# Gemini client
client = genai.Client(
    api_key="YOUR_API_KEY"
)

# Upload PDF
uploaded_file = st.file_uploader(
    "Upload PDF File",
    type=["pdf"]
)

if uploaded_file:

    # Read PDF
    pdf = PdfReader(uploaded_file)

    text = ""

    for page in pdf.pages:

        extracted_text = page.extract_text()

        if extracted_text:
            text += extracted_text

    # Preview text
    st.subheader("📑 Extracted Text Preview")

    st.write(text[:2000])

    # Summary type
    summary_type = st.selectbox(
        "Summary Style",
        [
            "Short Summary",
            "Detailed Summary",
            "Bullet Points"
        ]
    )

    # Generate button
    if st.button("Generate Summary"):

        prompt = f"""
        Generate a {summary_type} for this document.

        Document:
        {text[:12000]}
        """

        with st.spinner("Generating summary..."):

            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt
            )

            summary = response.text.strip()

        st.success("✅ Summary Generated!")

        st.subheader("📝 AI Summary")

        st.write(summary)

        # Download summary
        st.download_button(
            label="⬇ Download Summary",
            data=summary,
            file_name="summary.txt",
            mime="text/plain"
        )