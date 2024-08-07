import streamlit as st
import os
from PIL import Image
from utils import utils
# from prototype import PrototypeGenerator
from prototype import design_description, design_generation
from dotenv import load_dotenv
import base64
import requests
from pathlib import Path

load_dotenv()

# API_KEY = os.getenv('OPENAI_API_KEY')

# page config
st.set_page_config(
    page_title="Lyzr - Generate Better Prototypes",
    layout="centered",
    initial_sidebar_state="auto",
    page_icon="./logo/lyzr-logo-cut.png"
)

# style the app
st.markdown("""
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    [data-testid="stSidebar"][aria-expanded="true"]{                                                                                    
           min-width: 450px;
           max-width: 450px;
       }
    </style>
    """, unsafe_allow_html=True)

# Streamlit app interface
image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)
st.title('Prototype Generator')
st.markdown(
    'A tool that uses AI to enhance your existing design and generate better prototypes.')

img_dir = 'Image'
os.makedirs(img_dir, exist_ok=True)

API_KEY = st.text_input(label="OpenAI API Key", type='password')
if API_KEY:

    img = st.file_uploader('Upload your design', type=['png', 'jpeg'])


    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    #
    # path_of_image = utils.get_files_in_directory(directory='Image')
    # # Path to your image
    # image_path = Path(path_of_image[0])
    #
    # # Getting the base64 string
    # base64_image = encode_image(image_path)

    if img:
        utils.save_uploaded_file(directory=img_dir, uploaded_file=img)
        # prototype = PrototypeGenerator(api_key=API_KEY)
        # img_path = utils.get_files_in_directory(directory=img_dir)
        # prototype.generate(image_path=img_path[0])
        path_of_image = utils.get_files_in_directory(directory='Image')
        image_path = Path(path_of_image[0])
        base64_image = encode_image(image_path)
        descr = design_description(base64Image=base64_image, api_key=API_KEY)
        st.markdown('---')
        st.subheader('Existing Design')
        st.image(img)
        st.markdown('---')
        prompt_for_new_design = descr["choices"][0]["message"]["content"]
        img_url = design_generation(prompt=prompt_for_new_design)
        # st.write(img_url)
        st.subheader('New Design')
        st.image(img_url)

    else:
        utils.remove_existing_files(directory=img_dir)

