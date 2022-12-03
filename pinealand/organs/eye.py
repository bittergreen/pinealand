from organ import *
from PIL import Image
import math
import numpy as np


# normally we have 2 functioning eyes
# each is able to capture the world by projecting it onto the retina
# meanwhile, it would constantly change the projection with rapid saccades
class Eye(SensoryOrgan):

    def __init__(self, central_size=(50, 50)):
        super(Eye, self).__init__()
        self.__image__ = None
        self.__central_size__ = central_size
        self.perception = None

    def input_image(self, input_im: Image):
        self.__image__ = input_im
        tmp_size = max(input_im.size[0], input_im.size[1])
        self.__central_size__ = (tmp_size // 10, tmp_size // 10)

    def fixation(self, fix_point):
        if self.__image__ is None:
            raise RuntimeError("This Eye hasn't received any image input, please pass PIL.Image with Eye.input_image()")
        max_x, max_y = self.__image__.size
        center_x, center_y = fix_point
        x, y = self.__central_size__
        # (left, upper, right, lower)
        fix_area = (max(center_x - math.floor(x / 2), 0),
                    max(center_y - math.floor(y / 2), 0),
                    min(center_x + math.ceil(x / 2), max_x),
                    min(center_y + math.ceil(y / 2), max_y))
        return fix_area

    # Todo: 增加saccade序列生成方式
    def saccade(self):
        fix_point_sequence = []
        fix_point_sequence.append((self.__image__.size[0] // 2, self.__image__.size[1] // 2))
        fix_point_sequence.append((500, 100))
        fix_point_sequence.append((900, 1000))
        return fix_point_sequence

    def fixed_perceive(self, fix_point):
        fix_area = self.fixation(fix_point)
        transformed_image_array = convolution(self.__image__, fix_area, kernel=(3, 3), stride=3)
        transformed_image = Image.fromarray(np.uint8(transformed_image_array))
        return transformed_image

    # Todo: 设计上应该叠加多次saccade并fixed_perceive到的图像，叠加方式需要优化，最好能保留每次fixed_perceive到的central图像。下次吧
    def perceive(self):
        fix_point_sequence = self.saccade()
        synthetic_image = Image.new("RGB", self.__image__.size, (0, 0, 0))
        # Do一些图像叠加
        for i, fix_point in enumerate(fix_point_sequence):
            tmp_image = self.fixed_perceive(fix_point)
            if i == 0:
                synthetic_image = tmp_image
            else:
                synthetic_image = Image.blend(tmp_image, synthetic_image, 0.5)
        self.perception = Image.fromarray(np.uint8(synthetic_image))
        return self.perception


def merge(im1, im2):
    w = im1.size[0] + im2.size[0]
    h = max(im1.size[1], im2.size[1])
    im = Image.new("RGBA", (w, h))
    im.paste(im1)
    im.paste(im2, (im1.size[0], 0))
    return im


# retina contains lots of cones in its middle area
# and lots of rods in the peripheral
# Here the retina is some form of matrix transformation mapping original Image -> perceived Image
# cones are good at detecting R/G/B value
# distributed mostly in the central area of the retina
# Todo: 修改cone和rod的处理方式
def cone(pixel: np.array):
    color_list = ['r', 'g', 'b']
    return pixel * 2


# rod is good at detecting strength of light
# distributed mostly in the peripheral area of the retina
def rod(pixel: np.array):
    return pixel / 5


def convolution(original_im: Image, fix_area, kernel=(3, 3), stride=3):
    img_array = np.array(original_im)
    shape = img_array.shape
    height = shape[0]
    width = shape[1]
    left, upper, right, lower = fix_area
    new_image_array = np.zeros((height, width, 3))
    for i in range(0, height - kernel[0] + stride, stride):
        for j in range(0, width - kernel[1] + stride, stride):
            tmp = img_array[i:i+kernel[0], j:j+kernel[1]]
            if left <= j <= right and upper <= i <= lower:
                new_image_array[i:i + kernel[0], j:j + kernel[1]] = cone(tmp)
            else:
                new_image_array[i:i + kernel[0], j:j + kernel[1]] = rod(tmp)
    return new_image_array


if __name__ == '__main__':
    image = Image.open("/home/wengqi/1.jpg")
    left_eye = Eye()
    left_eye.input_image(image)
    result = left_eye.perceive()
    result.show()
