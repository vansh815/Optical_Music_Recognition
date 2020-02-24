# -*- coding: utf-8 -*-

import numpy as np
import cv2

def hough(img_binary):
    # code block modified from https://alyssaq.github.io/2014/understanding-hough-transform/
    height, width = img_binary.shape

    #voting space for hough
    accumulator = np.zeros((height, height//8), dtype=np.uint64)
    
    #get the rows of pixels
    #in a limited width
    #1. because they are not perfect horizontal lines
    #2. because it's faster
    #3. not all lines start from the beginning of the sheet
    y_idxs = []
    for i in range(height):
      for j in range(width//6, width//2):
        if img_binary[i][j] == 0:
          y_idxs.append(i)

    # Vote
    for i in range(len(y_idxs)):
      y = y_idxs[i]

      for s_ind in range(2, height//8):
        for j in range(5):
          l_start = y - (j * s_ind)
          l_end = y + (4 - j) * s_ind
          if l_start >= 0 and l_end < height:
            accumulator[l_start, s_ind] += 1


    #temp array to modify
    temp_array = np.ndarray.copy(accumulator)
    temp_pre = 0
    x_list = []
    y_list = []

    #iterate finding argmax from accumulator
    #then remove the argmax value
    #and all the votes in the voting space
    #that can be regarded as the same line
    while True:
      temp_idx = np.argmax(temp_array)
      if temp_array[temp_idx//(height//8)][temp_idx%(height//8)] < width:
        break
      if temp_pre%(height//8) != temp_idx%(height//8) and temp_pre != 0:
        temp_array[temp_idx//(height//8)][temp_idx%(height//8)] = 0
        continue
      x_list.append(temp_idx//(height//8))
      y_list.append(temp_idx%(height//8))
      for i in range(temp_idx//(height//8) - (temp_idx%(height//8))*3 - 3, temp_idx//(height//8) + (temp_idx%(height//8))*4 + 4):
        temp_array[i][temp_idx%(height//8)] = 0
      temp_pre = temp_idx

    return x_list, y_list[0]


