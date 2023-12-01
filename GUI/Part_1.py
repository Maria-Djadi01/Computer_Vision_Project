import streamlit as st
import sys
import numpy as np
import cv2

sys.path.insert(0, "D:/2M/Vision/Computer_Vision_Project")
from Part_1.filters.laplacian_filter import laplacian_filter
from utils import BGR2HSV, detect_color_object

def preprocess(img, gray=True):
    bytes_data = np.asarray(bytearray(img.read()), dtype=np.uint8)
    if gray:
        img = cv2.imdecode(bytes_data, cv2.IMREAD_GRAYSCALE)
    else:
        img = cv2.imdecode(bytes_data, cv2.IMREAD_COLOR)
    return img


def gray(img):
    img = preprocess(img)
    return img


def none(img):
    img = preprocess(img)
    return img

def laplace_filter(img):
    img = preprocess(img)
    return laplacian_filter(img)

def bgr2hsv(img):
    img = preprocess(img, gray=False)
    return BGR2HSV(img)

def color_detection(img):
    img = preprocess(img, gray=False)
    mask =  detect_color_object(img, (255, 255, 255))
    return mask


st.title("Computer Vision Project")
picture = st.camera_input("Take a picture !")

filters_to_funcs = {
    "No filter": none,
    "Grayscale": gray,
    "Laplacian": laplace_filter,
    "HSV": bgr2hsv,
    "Color Object Detection": color_detection,
}


filters = st.selectbox("...and now, apply a filter!", filters_to_funcs.keys())
# functions = st.selectbox("...and now, apply a filter!", fun_to_funs.keys())

if picture:
    st.image(filters_to_funcs[filters](picture))
    # st.image(fun_to_funs["Color Object Detection"](picture))
