# -*- coding: utf-8 -*-
# python ShuffleMakeIcons.py samples/WVW69ig4HC0o1_nAXC.jpg
# python ShuffleMakeIcons.py samples/WVW69ig4LfQzEn6wy-.jpg


from PIL import Image           # PIL module. Only if you use the PIL library.
from ShuffleClassifier import ShuffleClassifier
import sys

import config

filepath = sys.argv[1]

image = Image.open(filepath)

image = image.crop(config.varBox)

image.save('outputs/crop.png','PNG')

# Load Classifier
mac = ShuffleClassifier()

# Import Image to Classifer
mac.load_image2(image)

# Save Blocks
mac.save_blocks()


quit()
