# -*- coding: utf-8 -*-

import numpy as np

from PIL import Image, ImageDraw

def pitch(tmp1_idx, tmp4_idx, line_idx_list, space, height):
  #determine which pitch sequence each line should use
  flag_list=[]
  for x in line_idx_list:
    rl_idx = np.argmin([abs(x - tmp4_idx[i][0]) for i in range(len(tmp4_idx))])
    if abs(x - tmp4_idx[rl_idx][0]) < space * 5:
      flag_list.append("right")
    else:
      flag_list.append("left")
 

  #for each note
  #get the corresponding line
  #and get the corresponding pitch
  right_list = ['G', 'F', 'E', 'D', 'C', 'B', 'A']
  left_list = ['B', 'A', 'G', 'F', 'E', 'D', 'C']
  ret_list = []
  for idx in tmp1_idx:
    line_idx = np.argmin([abs(line_idx_list[i] - idx[0]) for i in range(len(line_idx_list))])
    line_row = line_idx_list[line_idx]
    flag = flag_list[line_idx]
    loc_diff = line_row - idx[0]
    row_list = []
    for i in np.arange(-4.5, 8.5, 0.5):
      row = int(line_row + (i*space))
      if row >= 0 and row < height:
        row_list.append((abs(row - idx[0])))
      else:
        row_list.append(np.inf)
    if flag_list[line_idx] == "right":
      correct_pitch = right_list[np.argmin(row_list) % 7]
    else:
      correct_pitch = left_list[np.argmin(row_list) % 7]
    ret_list.append(correct_pitch)


  return ret_list
