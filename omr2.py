#!/usr/local//bin/python3
from hough import hough
from pitch import pitch
from detection import detection
import cv2
import sys
from PIL import Image, ImageDraw
import numpy as np
import operator
import time


tic = time.time()
image_path = sys.argv[1]

img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
img_binary = cv2.threshold(img, 250, 255, cv2.THRESH_BINARY)[1]

height, width = img.shape
line_idx_list, scale = hough(img_binary)

#scaling image for detection
img_scale = 11.5/scale

scaled_img = Image.open(sys.argv[1]).convert('L')
scaled_img = scaled_img.resize((int(scaled_img.width*img_scale), int(scaled_img.height*img_scale)))
scaled_img = np.array(scaled_img)
scaled_img_bw = np.where(scaled_img >= 128, 1, 0)

#image output
result_image = Image.open(sys.argv[1])

if result_image.mode == 'L':
    	music2 = Image.new("RGBA", result_image.size)
    	music2.paste(result_image)
    	result_image = music2
    	
draw = ImageDraw.Draw(result_image)



#info of each templates
#detection should return
#
#the (row,col) list in tmp_idx
#
#confidence values
#which can be calculated using the denominator
#by comparing each template to each other
#
#template size
#which is the size of template after scaling
#
#Also, the functions will draw the corresponding boxes

tmp1_idx, tmp1_conf, tmp1_size = detection(scaled_img_bw, draw, "template_1")
#print("tmp1 finished!\n")
tmp2_idx, tmp2_conf, tmp2_size = detection(scaled_img_bw, draw, "template_2")
#print("tmp2 finished!\n")
tmp3_idx, tmp3_conf, tmp3_size = detection(scaled_img, draw, "template_3")
#print("tmp3 finished!\n")
tmp4_idx, tmp4_conf, tmp4_size = detection(scaled_img, draw, "template_4")
#print("tmp4 finished!\n")

#rescaling the coordinates
#and size of the templates
tmp1_idx = [(int(tmp1_idx[i][0] / img_scale), int(tmp1_idx[i][1] / img_scale)) for i in range(len(tmp1_idx))]
tmp1_size = (int(tmp1_size[0]/img_scale), int(tmp1_size[1]/img_scale))
tmp2_idx = [(int(tmp2_idx[i][0] / img_scale), int(tmp2_idx[i][1] / img_scale)) for i in range(len(tmp2_idx))]
tmp2_size = (int(tmp2_size[0]/img_scale), int(tmp2_size[1]/img_scale))
tmp3_idx = [(int(tmp3_idx[i][0] / img_scale), int(tmp3_idx[i][1] / img_scale)) for i in range(len(tmp3_idx))]
tmp3_size = (int(tmp3_size[0]/img_scale), int(tmp3_size[1]/img_scale))
tmp4_idx = [(int(tmp4_idx[i][0] / img_scale), int(tmp4_idx[i][1] / img_scale)) for i in range(len(tmp4_idx))]
tmp4_size = (int(tmp4_size[0]/img_scale), int(tmp4_size[1]/img_scale))
#print("resized!\n")

#find the pitch
#the function will draw the pitches next to the notes
pitch_list = pitch(tmp1_idx, tmp4_idx, line_idx_list, scale, height)
#print("found pitch!\n")

#output the info about resulting templates
#and draw the template on image
#row, col height, width, symbol_type, <pitch>, confidence

output_file = open("detected.txt", "w")
for idx in range(len(tmp1_idx)):
    output_file.write(str(tmp1_idx[idx][0]) + " " + str(tmp1_idx[idx][1]) + " " + str(tmp1_size[0]) + " " + str(tmp1_size[1]) + " " + "filled_note" + " " + pitch_list[idx] + " " + str(tmp1_conf[idx]) + "\n")
    draw.rectangle(((tmp1_idx[idx][1], tmp1_idx[idx][0]), (tmp1_idx[idx][1] + tmp1_size[1], tmp1_idx[idx][0] + tmp1_size[0])), outline="red", width = 2)
    draw.text((tmp1_idx[idx][1]-6, tmp1_idx[idx][0]), pitch_list[idx], fill="red")

for idx in range(len(tmp2_idx)):
    output_file.write(str(tmp2_idx[idx][0]) + " " + str(tmp2_idx[idx][1]) + " " + str(tmp2_size[0]) + " " + str(tmp2_size[1]) + " " + "quarter_rest" + " " + str(tmp2_conf[idx]) + "\n")
    draw.rectangle(((tmp2_idx[idx][1], tmp2_idx[idx][0]), (tmp2_idx[idx][1] + tmp2_size[1], tmp2_idx[idx][0] + tmp2_size[0])), outline="green", width = 2)

for idx in range(len(tmp3_idx)):
    output_file.write(str(tmp3_idx[idx][0]) + " " + str(tmp3_idx[idx][1]) + " " + str(tmp3_size[0]) + " " + str(tmp3_size[1]) + " " + "eighth_rest" + " " + str(tmp3_conf[idx]) + "\n")
    draw.rectangle(((tmp3_idx[idx][1], tmp3_idx[idx][0]), (tmp3_idx[idx][1] + tmp3_size[1], tmp3_idx[idx][0] + tmp3_size[0])), outline="blue", width = 2)

for idx in range(len(tmp4_idx)):
    output_file.write(str(tmp4_idx[idx][0]) + " " + str(tmp4_idx[idx][1]) + " " + str(tmp4_size[0]) + " " + str(tmp4_size[1]) + " " + "treble_clef" + " " + str(tmp4_conf[idx]) + "\n")
    draw.rectangle(((tmp4_idx[idx][1], tmp4_idx[idx][0]), (tmp4_idx[idx][1] + tmp4_size[1], tmp4_idx[idx][0] + tmp4_size[0])), outline="yellow", width = 2)

output_file.close()
result_image.save("detected.png", "PNG")

#print(time.time() - tic)




