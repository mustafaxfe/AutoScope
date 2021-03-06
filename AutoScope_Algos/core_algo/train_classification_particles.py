# Import basic libraries
import os
import numpy as np
import glob

#Import keras libraries
from tensorflow.python.keras.optimizers import SGD, RMSprop
from tensorflow.python.keras.metrics import categorical_accuracy
from tensorflow.python.keras.utils import plot_model

# import from local libraries
from ClassifyParticlesData import ClassifyParticlesData
import CNN_functions
from classification_models import base_model_with_pos as createModel
from ClassifyParticles_config import ClassifyParticles_Config



# Instantiates configuration for training/validation
config = ClassifyParticles_Config()

# Configuration sanity check
CNN_functions.validate_classification_config(config)

# Instantiate training/validation data
data = ClassifyParticlesData(config)

# Create necessary data generators
train_generator = data.create_custom_labeled_generator(target_directory=config.train_images_dir, augment_data=True)
val_generator = data.create_custom_labeled_generator(target_directory=config.val_images_dir, augment_data=False)

# Print configuration
CNN_functions.print_configurations(config) # Print config summary to log file
data.print_data_summary() # Print data summary to log file


# Builds model
model = createModel(input_shape = config.image_shape, base_weights = config.imagenet_weights_file, classes=config.nclasses)
# plot_model(model, to_file='model.png')


# Load weights (if the load file exists)
CNN_functions.load_model(model, config.weight_file_input, config)

# Train
data.train_entire_model(
	model = model, 
	train_generator = train_generator, 
	val_generator = val_generator)

