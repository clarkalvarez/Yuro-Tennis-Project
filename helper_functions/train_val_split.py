import os
import shutil
import numpy as np

TRAIN = "train"
TRAIN_BALLS = "train/balls"
TRAIN_EMPTY = "train/empty"

VAL_BALLS = "validation/balls"
VAL_EMPTY = "validation/empty"

SPLIT = [0.7, 0.3]

train_balls = os.listdir(TRAIN_BALLS)
train_empty = os.listdir(TRAIN_EMPTY)

TRAIN_BALLS_LEN = len(train_balls)
TRAIN_EMPTY_LEN = len(train_empty)

np_train_balls = np.array(train_balls)
np_train_empty = np.array(train_empty)

np.random.shuffle(np_train_balls)
np.random.shuffle(np_train_empty)

val_balls = np_train_balls[:int(SPLIT[1]*TRAIN_BALLS_LEN)]
val_empty = np_train_empty[:int(SPLIT[1]*TRAIN_EMPTY_LEN)]

val_balls_dir = [os.path.join(TRAIN_BALLS, x) for x in val_balls]
val_empty_dir = [os.path.join(TRAIN_EMPTY, x) for x in val_empty]

for i, j in zip(val_balls_dir, val_empty_dir):
	basename_balls = os.path.basename(i)
	basename_empty = os.path.basename(j)

	val_balls = os.path.join(VAL_BALLS, basename_balls)
	val_empty = os.path.join(VAL_EMPTY, basename_empty)

	shutil.move(i, val_balls)
	print(val_balls)
	shutil.move(j, val_empty)
	print(val_empty)