"""CSS module of NirmatAI WebApp."""

import streamlit as st


def local_css(css_text: str) -> None:
    """Injects local CSS into a Streamlit app.

    Parameters:
    css_text (str): The CSS code as a string to be injected into the app.
    """
    st.markdown(f"<style>{css_text}</style>", unsafe_allow_html=True)

custom_css = """
/* Smooth animated wave background in lilac tones for main container */
body {
    background: linear-gradient(120deg, #fff2cc, #fffcdc);
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
}

@keyframes gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Input fields without shadow, clean look */
input[type="text"], input[type="password"] {
    background-color: #F0F0F5;
    border: none;
    border-radius: 10px;
    padding: 10px;
    font-size: 16px;
    margin-bottom: 10px;
    width: 100%;
    box-sizing: border-box;
}

input[type="text"]:focus, input[type="password"]:focus {
    outline: none;
    background-color: #e8e8f0;
}

/* File uploader with a clean, shadow-free style */
div.stFileUploader {
    background-color: #F7F7FA;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
}

/* DataFrame style */
div.stDataFrame {
    border-radius: 15px;
    background-color: #fff;
    padding: 10px;
    margin-bottom: 20px;
}

/* Heading styles with modern font and no shadow */
h1, h2, h3 {
    font-family: 'Roboto', sans-serif;
    color: #235371;
    margin: 10px 15px 20px 10px;
}

/* Download link style */
.download-link {
    color: #4CAF50;
    font-size: 14px;
}

/* Button styles */
button {
    background-color: #1e4863 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    font-size: 16px !important;
}

button:hover {
    background-color: #45a049 !important;
}

/* Logo styles without shadow */
.stLogo {
    width: 100px; /* Adjust the logo size */
    height: 100px; /* Adjust the logo size */
    padding: 5px 5px 5px 5px; /* Adjust padding */
    margin: 8px 12px 12px 8px;
    border-radius: 8px; /* Optional rounded corners */
}

.stExpander {
    font-family: 'Roboto', sans-serif;
    font-size: 20px;
    color: #235371;
    margin: 10px 15px 15px 10px;
}
"""
