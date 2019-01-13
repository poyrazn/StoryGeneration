#
# main
# StoryGeneration
#
# Created by Nehir Poyraz on 16.12.2018
# Copyright 2018 Nehir Poyraz. All rights reserved.

import pandas as pd
import numpy as np
import random


def generate(data: pd.DataFrame, s: int):
	IDS = random.sample(list(np.unique(data['storyID'].values)), s)
	samples = []
	for ID in IDS:
		title = list(data['storytitle'][(ID - 1) * 5:(ID - 1) * 5 + 1])[0]
		text = list(data['text'][(ID - 1) * 5:ID * 5])
		line = list(data['keyword'][(ID - 1) * 5:ID * 5])
		samples.append({'title': title, 'text': text, 'line': line})
	return samples



def load(dataset: str):
	return pd.read_csv(dataset)



def vectorize():
	# TODO implement
	pass


