import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import math

def convolve(music, filter):
	shape = music.shape
	conv_result = []
	music = np.pad(music, ((filter.shape[0]//2, filter.shape[0]//2), (filter.shape[1]//2, filter.shape[1]//2)), mode='constant', constant_values=255)

	filter = np.flip(np.flip(filter, axis = 0), axis = 1)
	for i in range(music.shape[0]):
		for j in range(music.shape[1]):
			if i+filter.shape[0] <= music.shape[0] and j+filter.shape[1] <= music.shape[1]: 
				slice_music = music[i:i+filter.shape[0], j:j+filter.shape[1]]
				conv_result.append(np.sum(np.multiply(slice_music,filter)))
	return np.array(conv_result).reshape(shape)

def hamming(music, template1_convolve, filter_type, conf_interval_denom):

	result = []
	conf_interval = []
	for i in range(music.shape[0]):
		for j in range(music.shape[1]):
			if i+template1_convolve.shape[0] < music.shape[0] and j+template1_convolve.shape[1] < music.shape[1]: 
				slice_music = music[i:i+template1_convolve.shape[0], j:j+template1_convolve.shape[1]]


				first = np.multiply(slice_music, template1_convolve)
				second = np.multiply(np.ones((slice_music.shape[0], slice_music.shape[1]))-slice_music,np.ones((template1_convolve.shape[0], template1_convolve.shape[1])) - template1_convolve)

				if filter_type == "template_1":
					if int(np.sum(first + second)) >= 154:
						result.append((i,j))
						conf_interval.append(round(int(np.sum(first + second))/conf_interval_denom,2))
				if filter_type == "template_2":
					if int(np.sum(first + second)) > 450:
						result.append((i,j))
						conf_interval.append(round(int(np.sum(first + second))/conf_interval_denom,2))
				if filter_type == "template_3":
					if int(np.sum(first + second)) >= 340:
						result.append((i,j))
						conf_interval.append(round(int(np.sum(first + second))/conf_interval_denom,2))
				if filter_type == "template_4":
					if int(np.sum(first + second)) >= 1750:
						result.append((i,j))
						conf_interval.append(round(int(np.sum(first + second))/conf_interval_denom,2))

	temp = []
	temp1 = []
	for i in range(len(result)):
		for j in range(i+1, len(result)):
			if int(np.sqrt((result[i][0] - result[j][0])**2 + (result[i][1] - result[j][1])**2)) < 5:
				temp.append(result[j])
				temp1.append(j)


	result = list(set(result) - set(temp))
	conf_interval = np.delete(np.array(conf_interval), temp1)
	template_shape = template1_convolve.shape
	
	return result, conf_interval, template_shape


def sobel(music):

	# Horizontal edge detection
	music_sobel = convolve(music, np.array([[1,0,-1]]).T)
	music_sobel = convolve(music_sobel, np.array([[1,2,1]]))
    
	# Vertical edge detection
	music_sobel = convolve(music_sobel, np.array([[1,2,1]]).T)
	music_sobel = convolve(music_sobel, np.array([[1,0,-1]]))

	music_sobel = abs(music_sobel)
   
   	# # Normalizing
	music_sobel = 255*(music_sobel - np.min(music_sobel))/(np.max(music_sobel) - np.min(music_sobel))
	music_sobel = np.where(music_sobel >= 20, 1, 0)
	
	return music_sobel

def detection(img_binary, draw, template_type):

	

	if template_type == "template_1" or template_type == "template_2":

		if template_type == "template_1":
			template1 = Image.open("template1.png").convert('L')
		else:
			template1 = Image.open("template2.png").convert('L')
		template1 = np.array(template1)
		template1_bw = np.where(template1 >= 128, 1, 0)

		first = np.multiply(template1_bw, template1_bw)
		second = np.multiply(np.ones((template1_bw.shape[0], template1_bw.shape[1]))-template1_bw,np.ones((template1_bw.shape[0], template1_bw.shape[1])) - template1_bw)
		conf_interval_denom = int(np.sum(first + second))

		if template_type == "template_1":
			result, conf_interval, template_shape = hamming(img_binary, template1_bw, "template_1", conf_interval_denom)
		else:
			result, conf_interval, template_shape = hamming(img_binary, template1_bw, "template_2", conf_interval_denom)



	if template_type == "template_3" or template_type == "template_4":

		if template_type == "template_3":
			template1 = Image.open("template3.png").convert('L')
		else:
			template1 = Image.open("template4.png").convert('L')
		template1 = np.array(template1)
		template1_bw = np.where(template1 >= 128, 1, 0)

		music_sobel = sobel(img_binary)
		template_sobel = sobel(template1)

		first = np.multiply(template_sobel, template_sobel)
		second = np.multiply(np.ones((template_sobel.shape[0], template_sobel.shape[1]))-template_sobel,np.ones((template_sobel.shape[0], template_sobel.shape[1])) - template_sobel)
		conf_interval_denom = int(np.sum(first + second))

		if template_type == "template_3":
			result, conf_interval, template_shape = hamming(np.array(music_sobel), np.array(template_sobel), "template_3", conf_interval_denom)
		else:
			result, conf_interval, template_shape = hamming(np.array(music_sobel), np.array(template_sobel), "template_4", conf_interval_denom)

	return result, conf_interval, template_shape