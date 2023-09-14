#!/bin/bash

set -ea

# NOTE: could create a new env. but most things are ok 
#       when using anaconda-2021.11 ..

function CreateEnv()
{
	conda create --name yolov5
	conda env list
	conda activate yolov5
}

function Setup()
{
	(test ! -d yolov5 && git clone https://github.com/ultralytics/yolov5) || echo "Git-repository already cloned.."

	#cd yolov5
	#pip install -r requirements.txt 

	# NOTE: torch version in original requirements incompatible with GPU hardware, 
	#       use the following instead ..
	pip install torch==1.10.1+cu111 torchvision==0.11.2+cu111 torchaudio==0.10.1 -f https://download.pytorch.org/whl/torch_stable.html

	# NOTE: then install whatever is not in conda ..
	pip install -r yolov5_swmal_requirements.txt
}

function UninstallPips()
{
	pip uninstall opencv-python tensorboard tensorboard-data-server thop torch torchaudio torchvision
	pip list --user
}

#CreateEnv
#Setup
#UninstallPips

echo "NOTE: use default setup on GPU-Cluster instead:"
echo "      module 'anaconda 2022.05' contains all torch libs needed'"

echo "DONE"