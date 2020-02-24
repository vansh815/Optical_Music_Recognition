import numpy as np

def edge_map(music_bw, template1_bw, filter_type):

	"""
	:param music_bw: Distance matrix of the image
	:param template: Edge detected template image
	:param filter_type: One of template_1, template_2, template_3, template_4
	:return: Returns a tuple of recognized coordinates with filter type
	"""

	result = []
	#temp = []
	for i in range(music_bw.shape[0]):
		for j in range(music_bw.shape[1]):
			if i + template1_bw.shape[0] < music_bw.shape[0] and j + template1_bw.shape[1] < music_bw.shape[1]:
				slice_music = music_bw[i:i + template1_bw.shape[0], j:j + template1_bw.shape[1]]

                # Thresholds were not good for this task
				if filter_type == "template_1":
					if np.sum(np.multiply(slice_music, template1_bw)) >= 250:
						result.append((i,j,filter_type))

				if filter_type == "template_2":
					if np.sum(np.multiply(slice_music, template1_bw)) >= 300:
						result.append((i,j,filter_type))

				if filter_type == "template_3":
					if np.sum(np.multiply(slice_music, template1_bw)) >= 289:
						result.append((i,j,filter_type))

                if filter_type == "template_4":
                    if np.sum(np.multiply(slice_music, template1_bw)) >= 289:
                        result.append((i,j,filter_type))
	
	return result
               
                 
                