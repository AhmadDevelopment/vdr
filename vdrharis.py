import streamlit as st
from gradio_client import Client, file
import tempfile
from PIL import Image
import os
import base64  

def load_image(image_file):
    img = Image.open(image_file)
    return img

# Streamlit app
st.title("Virtual Try-On")
st.write("Upload a user image and a garment image to try on the garment virtually.")

# Upload user image
user_image_file = st.file_uploader("Upload User Image", type=["jpg", "jpeg", "png"])
# Upload garment image
garment_image_file = st.file_uploader("Upload Garment Image", type=["jpg", "jpeg", "png"])

if user_image_file and garment_image_file:
    # Display uploaded images
    st.image(load_image(user_image_file), caption="User Image", use_column_width=True)
    st.image(load_image(garment_image_file), caption="Garment Image", use_column_width=True)

    # Save uploaded images to temporary files
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as user_tempfile:
        user_tempfile.write(user_image_file.getvalue())
        user_tempfile_path = user_tempfile.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as garment_tempfile:
        garment_tempfile.write(garment_image_file.getvalue())
        garment_tempfile_path = garment_tempfile.name

    # Call the Hugging Face API
    client = Client("yisol/IDM-VTON")
    result = client.predict(
        dict={"background": file(user_tempfile_path), "layers": [], "composite": None},
        garm_img=file(garment_tempfile_path),
        garment_des="Virtual Try-On",
        is_checked=True,
        is_checked_crop=False,
        denoise_steps=30,
        seed=42,
        api_name="/tryon"
    )

    # Display result
    result_image_path = result[0]
    result_image = Image.open(result_image_path)
    st.image(result_image, caption="Result", use_column_width=True)

    # Provide a download button for the result image
    st.markdown("### Download Result Image")
    with open(result_image_path, "rb") as img_file:
        b64_result_image = base64.b64encode(img_file.read()).decode()
    st.markdown(f"Download your result image [here](data:image/png;base64,{b64_result_image})")




##
##
##import streamlit as st
##from gradio_client import Client, file
##import tempfile
##from PIL import Image
##
##def load_image(image_file):
##    img = Image.open(image_file)
##    return img
##
### Streamlit app
##st.title("Virtual Try-On")
##st.write("Upload a user image and a garment image to try on the garment virtually.")
##
### Upload user image
##user_image_file = st.file_uploader("Upload User Image", type=["jpg", "jpeg", "png"])
### Upload garment image
##garment_image_file = st.file_uploader("Upload Garment Image", type=["jpg", "jpeg", "png"])
##
##if user_image_file and garment_image_file:
##    # Display uploaded images
##    st.image(load_image(user_image_file), caption="User Image", use_column_width=True)
##    st.image(load_image(garment_image_file), caption="Garment Image", use_column_width=True)
##
##    # Save uploaded images to temporary files
##    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as user_tempfile:
##        user_tempfile.write(user_image_file.getvalue())
##        user_tempfile_path = user_tempfile.name
##
##    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as garment_tempfile:
##        garment_tempfile.write(garment_image_file.getvalue())
##        garment_tempfile_path = garment_tempfile.name
##
##    # Call the Hugging Face API
##    client = Client("yisol/IDM-VTON")
##    result = client.predict(
##        dict={"background": file(user_tempfile_path), "layers": [], "composite": None},
##        garm_img=file(garment_tempfile_path),
##        garment_des="Virtual Try-On",
##        is_checked=True,
##        is_checked_crop=False,
##        denoise_steps=30,
##        seed=42,
##        api_name="/tryon"
##    )
##
##    # Display result
##    result_image_path = result[0]
##    result_image = Image.open(result_image_path)
##    st.image(result_image, caption="Result", use_column_width=True)
##
