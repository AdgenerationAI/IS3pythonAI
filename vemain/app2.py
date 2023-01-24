from flask import Flask, request, render_template
from googletrans import Translator
import base64
import os
import io
import numpy as np
import torch
from diffusers import StableDiffusionPipeline
from torch import autocast

MODEL_ID = "CompVis/stable-diffusion-v1-4"
DEVICE = "cpu"
YOUR_TOKEN = "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"

pipe = StableDiffusionPipeline.from_pretrained(MODEL_ID, use_auth_token=YOUR_TOKEN)
pipe = pipe.to(DEVICE)

app = Flask(__name__)

def doGet():
    message = request.form["form"]
    messageList = message.strip().split(",")
    return messageList

def translate(messageList):
    translator = Translator()
    translatedList = []
    for m in messageList:
        tm = translator.translate(m, dest="en")
        translatedList.append(tm.text)
    translatedWord = ",".join(translatedList)
    return translatedWord

def generateImage(translatedWord):
    image = []
    prompt = [translatedWord] * 2

    def null_safety(images, **kwargs):
        return images, False

    pipe.safety_checker = null_safety

    with autocast(DEVICE):
        images = pipe(prompt, guidance_scale=7.5).images
        images.extend(pipe(prompt, guidance_scale=7.5).images)
        images.extend(pipe(prompt, guidance_scale=7.5).images)
        #images.extend(pipe(prompt, guidance_scale=7.5).images)
        #images.extend(pipe(prompt, guidance_scale=7.5).images)

    return images

def sendImage(imageList):
    img_name_list = []
    for image in imageList:
        with io.BytesIO() as output:
            image.save(output, format="PNG")
            img_byte = output.getvalue()
            img_encoded = base64.b64encode(img_byte)
            img_name = img_encoded.decode("utf-8")
            img_name_list.append(img_name)
    return img_name_list

@app.route("/", methods=["GET", "POST"])
def index():
    img_name_list = []
    translatedWord = ""

    if request.method == "POST":
        messageList = doGet()
        translatedWord = translate(messageList)
        images = generateImage(translatedWord)
        img_name_list = sendImage(images)

    return render_template("index.html", img_name_list=img_name_list, translatedWord=translatedWord)

if __name__ == "__main__":
    app.run()