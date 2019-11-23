"""
Parameters and utility functions to run ESRGAN on images within WorkingImageData's
"""

import os
from os import path
from shutil import copyfile

ESRGANPath = "TextureUpscaler/ESRGAN/"
ESRGANScript = path.join(ESRGANPath, "test.py")
ESRGANModel = "interp_09.pth"
ESRGANSrcPath = path.join(ESRGANPath, "LR")
ESRGANDstPath = path.join(ESRGANPath, "results")

def upscale_esrgan(workingImages, workingPath):
    for currImage in workingImages:
        src = currImage.lastPath
        dst = path.join(ESRGANSrcPath, currImage.workingFilename)
        copyfile(src, dst)

    ESRGANCommand = "python " + ESRGANScript + " " + ESRGANModel
    print(ESRGANCommand)
    os.system(ESRGANCommand)

    for currImage in workingImages:
        destFilename = str(currImage.ID) + "_rlt.png"
        src = path.join(ESRGANDstPath, destFilename)
        dst = path.join(workingPath, currImage.workingFilename)
        copyfile(src, dst)
        currImage.lastPath = dst
        