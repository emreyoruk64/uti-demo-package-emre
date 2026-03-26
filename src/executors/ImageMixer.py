import os
import cv2
import sys
import numpy as np
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.DemoPackageEmre.src.utils.response import build_response_mix
from components.DemoPackageEmre.src.models.PackageModel import PackageModel

class ImageMixer(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.image = self.request.get_param("inputImage")
        self.image_two = self.request.get_param("inputImageTwo")
        self.mixing_mode = self.request.get_param("MixingMode")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def mix(self, inputimage, inputimagetwo):
        if inputimage.shape != inputimagetwo.shape:
            height, width = inputimage.shape[:2]
            inputimagetwo = cv2.resize(inputimagetwo, (width, height))

        mode_name = self.mixing_mode.get("name")

        if mode_name == "ManuelAlpha":
            alpha_value = float(self.mixing_mode.get("alpha",0.5))

        elif mode_name == "UsePreset":
            strength_level = self.mixing_mode.get("strength_level")

            if strength_level == "Low":
                alpha_value = 0.8

            elif strength_level == "High":
                alpha_value = 0.5

            else:
                alpha_value = 0.5

        else:
            alpha_value = 0.5

        beta = 1 - alpha_value

        mixed_image = cv2.addWeighted(inputimage, alpha_value, inputimagetwo, beta, 0.0)

        diff_image = cv2.absdiff(inputimage, inputimagetwo)

        difference_map = cv2.cvtColor(diff_image, cv2.COLOR_BGR2GRAY)

        return mixed_image, difference_map


    def run(self):
        img1 = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.image_two, redis_db=self.redis_db)
        self.mix = self.mix(img1.value, img2.value)
        if isinstance(self.mix, dict): self.mix = [self.mix]
        img1.value, img2.value = self.mix(img1.value, img2.value)
        self.image = Image.set_frame(img=img1, package_uID=self.uID, redis_db=self.redis_db)
        self.image_two = Image.set_frame(img=img2, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_response_mix(context=self)
        return packageModel



if "__main__" == __name__:
    Executor(sys.argv[1]).run()