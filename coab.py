import streamlit as st
from PIL import Image


def convertToBinary(data):
    newdata = [format(ord(i), '08b') for i in data]
    return newdata

def encodepixels(pix, data):
    datalist = convertToBinary(data)
    lendata = len(datalist)
    image_data = iter(pix)
    for i in range(lendata):
        pix = [value for value in image_data.__next__()[:3] + image_data.__next__()[:3] + image_data.__next__()[:3]]
        for j in range(0, 8):
            if (datalist[i][j] == "0" and pix[j] % 2 != 0):
                pix[j] -= 1
            elif (datalist[i][j] == "1" and pix[j] % 2 == 0):
                if (pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encode_image(new_image, data):
    w = new_image.size[0]
    (x, y) = (0, 0)
    for pixel in encodepixels(new_image.getdata(), data):
        new_image.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

def encode():
    img_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if img_file is not None:
        image = Image.open(img_file)

        data = st.text_input("Enter your secret message:")
        if st.button("Encode"):
            if len(data) == 0:
                st.error('Data is empty')
            else:
                new_image = image.copy()
                encode_image(new_image, data)

                new_img_name = st.text_input("Enter the image name you want to save it as with extension format:")
                st.image(new_image, caption='Encoded Image', use_column_width=True)
                if st.button("Save Image"):
                    new_image.save(new_img_name, str(new_img_name.split(".")[1].upper()))

def decode():
    img_file = st.file_uploader("Upload an image to decode", type=["jpg", "jpeg", "png"])
    if img_file is not None:
        image = Image.open(img_file)

        data = ''
        image_data = iter(image.getdata())
        st.image(image, caption='Image to be decoded', use_column_width=True)
        st.write("The image to be decoded:")
        st.write("\n")

        while True:
            pixels = [value for value in image_data.__next__()[:3] +
                                image_data.__next__()[:3] +
                                image_data.__next__()[:3]]

            binary_string = ''

            for i in pixels[:8]:
                if i % 2 == 0:
                    binary_string += '0'
                else:
                    binary_string += '1'

            data += chr(int(binary_string, 2))
            if pixels[-1] % 2 != 0:
                break

        st.success("The decoded secret message in the input is:  " + data)

# Streamlit UI
st.title("LSB Steganography with Streamlit")
option = st.sidebar.selectbox("Select an option", ["Encode", "Decode"])

if option == "Encode":
    encode()
elif option == "Decode":
    decode()
