import gradio as gr
import numpy as np
from PIL import Image
import random
import os
import json
from datetime import datetime
# matcher = Matcher()
print(datetime.now())
import shutil

INPUT_DIR = '/media/Zeus/magesh/test_store_crops/'
NOTFIXED_DIR = 'notfixed_2/'
FIXED_DIR = 'fixed_2/'
INVALID_DIR = 'invalid_2/'

'''
Product recognition code
Input -> Image Path. 
Output -> List of Tuples sorted based on TopK. each tuple -> (Image, Score). 
'''
with open("save_image_to_index_mapping_gross.json","r") as f:
    mapping = json.load(f)

with open("cropwise_top1_v6.json", "r") as f:
    results = json.load(f)

def product_recognition(input_img_num, state):


    input_img_path = INPUT_DIR + mapping[str(input_img_num)]
    res = results[input_img_path]
    # out = [(np.asarray(Image.open(os.path.join('/home/interns2022/prodid_endpoint/',res["top"]))),res["score"])]
    return np.asarray(Image.open(os.path.join('/home/interns2022/prodid_endpoint/',res["top"])))


def display_img(input_img_num):
    input_img = Image.open(INPUT_DIR + mapping[str(input_img_num)])
    input_img = np.asarray(input_img)
    return input_img

def fixed_enrollment(input_img_num):
    input_img_path = os.path.join(INPUT_DIR, mapping[str(input_img_num)])
    fixed_img_path = os.path.join(FIXED_DIR, mapping[str(input_img_num)])
    notfixed_img_path = os.path.join(NOTFIXED_DIR, mapping[str(input_img_num)])
    invalid_img_path = os.path.join(INVALID_DIR, mapping[str(input_img_num)])

    fixed_img_dir = '/'.join(fixed_img_path.split('/')[:-1])
    if not os.path.isdir(fixed_img_dir):
        os.makedirs(fixed_img_dir, mode = 0o777)
    if os.path.isfile(notfixed_img_path):
        os.remove(notfixed_img_path)
    if os.path.isfile(invalid_img_path):
        os.remove(invalid_img_path)
    shutil.copy(input_img_path,fixed_img_path)
    return

def notfixed_enrollment(input_img_num):
    input_img_path = os.path.join(INPUT_DIR, mapping[str(input_img_num)])
    fixed_img_path = os.path.join(FIXED_DIR,  mapping[str(input_img_num)])
    notfixed_img_path = os.path.join(NOTFIXED_DIR,  mapping[str(input_img_num)])
    invalid_img_path = os.path.join(INVALID_DIR, mapping[str(input_img_num)])

    notfixed_img_dir = '/'.join(notfixed_img_path.split('/')[:-1])
    if not os.path.isdir(notfixed_img_dir):
        os.makedirs(notfixed_img_dir, mode = 0o777)
    if os.path.isfile(fixed_img_path): 
        os.remove(fixed_img_path)
    if os.path.isfile(invalid_img_path):
        os.remove(invalid_img_path)
    shutil.copy(input_img_path,notfixed_img_path)
    return

def invalid_enrollment(input_img_num):
    input_img_path = os.path.join(INPUT_DIR, mapping[str(input_img_num)])
    fixed_img_path = os.path.join(FIXED_DIR,  mapping[str(input_img_num)])
    notfixed_img_path = os.path.join(NOTFIXED_DIR,  mapping[str(input_img_num)])
    invalid_img_path = os.path.join(INVALID_DIR, mapping[str(input_img_num)])

    invalid_img_dir = '/'.join(invalid_img_path.split('/')[:-1])
    if not os.path.isdir(invalid_img_dir):
        os.makedirs(invalid_img_dir, mode = 0o777)
    if os.path.isfile(fixed_img_path): 
        os.remove(fixed_img_path)
    if os.path.isfile(notfixed_img_path):
        os.remove(notfixed_img_path)
    shutil.copy(input_img_path,invalid_img_path)
    return


def next_num(x, y):
    y ^= 1
    x = str(int(x)+1)
    return [x, y]

def prev_num(x, y):
    y ^= 1
    x = str(int(x)-1)
    return [x, y]

with gr.Blocks() as demo:
    state = gr.State(1)
    gr.Markdown("<h1><center>Product Recognition Demo</center></h1>")
    gr.Markdown("<center>This tool is used to fix the gross mismatches caused due to misenrollment.</center>")
    with gr.Row():
        with gr.Column():
            input_num = gr.Textbox(label = "Image Number")
            message = gr.Checkbox(False, visible = False)
            with gr.Row():
                display = gr.Image(label = "Test Image").style(height = 300, width = 400)
            with gr.Row():
                prev = gr.Button("< Prev")
                next = gr.Button("Next >")
            with gr.Row():
                with gr.Column():  
                    fixed = gr.Button("Fixed", variant = "primary")
                with gr.Column(): 
                    notfixed = gr.Button("Not Fixed", variant = "primary")
                with gr.Column(): 
                    invalid = gr.Button("Invalid Crop")
            
        with gr.Column():
            outputs = gr.Image(label = "Matched Product").style(height = 400, width=500)
    
    input_num.submit(display_img, input_num, display)
    input_num.submit(product_recognition, input_num, outputs)
    input_num.submit(lambda x:x, input_num, state)


    next.click(next_num, [state, message], [state, message])
    prev.click(prev_num, [state, message], [state, message])

    message.change(lambda x:x, state, input_num)
    message.change(display_img, state, display)
    message.change(product_recognition, state, outputs)


    fixed.click(fixed_enrollment, input_num, None)
    notfixed.click(notfixed_enrollment, input_num, None)
    invalid.click(invalid_enrollment, input_num, None)
demo.launch(server_port = 8000)


