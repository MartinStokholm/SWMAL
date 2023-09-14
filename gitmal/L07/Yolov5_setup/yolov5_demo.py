#!/usr/bin/env python3

import torch
import sys

def TorchVersions():
    print("VERSIONS:")
    sysver = sys.version.replace("\n", "")
    print(f"  _sys.version                             = {sysver}")
    print(f"  torch.__version__                        = {torch.__version__}")
    print(f"  torch.cuda.is_available()                = {torch.cuda.is_available()}")
    print(f"  torch.backends.cudnn.enabled             = {torch.backends.cudnn.enabled}")
    try:
        device = torch.device("cuda")
        print(f"  torch.cuda.get_device_properties(device) = {torch.cuda.get_device_properties(device)}")
        print(f"  torch.tensor([1.0, 2.0]).cuda()          = {torch.tensor([1.0, 2.0]).cuda()}")
        return True
        
    except RuntimeError as ex:
        print(f"EXCEPTION({type(ex)}): {ex}", file=sys.stderr)
        print(f"WARNING: Sorry mate, it seems your PC is without a CUDA enabled GPU!", file=sys.stderr)
    except Exception as ex:
        print(f"EXCEPTION({type(ex)}): {ex}", file=sys.stderr)
    return False

def PredictDemo():
    # Model
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5l, yolov5x, custom

    # Images
    #img = 'https://ultralytics.com/images/zidane.jpg'  # or file, Path, PIL, OpenCV, numpy, list
    #img = 'Figs/zidane.jpg'
    img = 'Figs/demo.jpg'

    # Inference
    results = model(img)

    # Results
    results.print()  # or .show(), .save(), .crop(), .pandas(), etc.
    #results.show()
    results.save('temp.jpg')
    
TorchVersions()
PredictDemo()