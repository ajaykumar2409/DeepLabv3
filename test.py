# -*- coding: utf-8 -*-
"""Test.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AVT0_va0iVt3NNpQuUxROwrCzAfggety
"""

import torch
import torch.nn as nn
from utils import *
from models.deeplabv3 import DeepLabV3
import sys
import os
from tqdm import tqdm
import matplotlib.pyplot as plt

def test(FLAGS):
    # Check if the pretrained model is available
    if not FLAGS.model_path.endswith('.pth'):
        raise RuntimeError('Unknown file passed. Must end with .pth')
    if FLAGS.image_path is None or not os.path.exists(FLAGS.image_path):
        raise RuntimeError('An image file path must be passed')
    
    h = FLAGS.resize_height
    w = FLAGS.resize_width

    checkpoint = torch.load(FLAGS.model_path,  map_location='cpu')
    
    # Assuming the dataset is camvid
    deeplabv3 = DeepLabV3(12)
    deeplabv3.load_state_dict(checkpoint['state_dict'])

    tmg_ = plt.imread(FLAGS.image_path)
    tmg_ = cv2.resize(tmg_, (h, w), cv2.INTER_NEAREST)
    tmg = torch.tensor(tmg_).unsqueeze(0).float()
    tmg = tmg.transpose(2, 3).transpose(1, 2)

    with torch.no_grad():
        out1 = deeplabv3(tmg.float()).squeeze(0)
    
    #smg_ = Image.open('/content/training/semantic/' + fname)
    #smg_ = cv2.resize(np.array(smg_), (512, 512), cv2.INTER_NEAREST)

    b_ = out1.data.max(0)[1].cpu().numpy()

    decoded_segmap = decode_segmap(b_)

    images = {
        0 : ['Input Image', tmg_],
        1 : ['Predicted Segmentation', b_],
    }

    show_images(images)