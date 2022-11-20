from organ import *
from PIL import Image
import math


# normally we have 2 functioning eyes
# each is able to capture the world by projecting it onto the retina
# meanwhile, it would constantly change the projection with rapid saccades
class Eye(Organ):

    def __init__(self, reception_size=(50, 50)):
        self.__name__ = "Eye"
        self.__image__ = None
        self.reception_size = reception_size
        self.retina = Retina(reception_size)

    def input_image(self, input_im: Image):
        self.__image__ = input_im

    # box.size should be same with the size of the retina
    def saccade(self, fix_point):
        if self.__image__ is None:
            raise RuntimeError("This Eye hasn't received any image input, please pass PIL.Image with Eye.input_image()")
        center_x, center_y = fix_point
        x, y = self.reception_size
        # (left, upper, right, lower)
        box = (center_x - math.floor(x / 2),
               center_y - math.floor(y / 2),
               center_x + math.ceil(x / 2),
               center_y + math.ceil(y / 2))
        return box

    def perceive(self, image: Image):
        return self.retina.perceive(image)

    # Todo: 设计上应该叠加多次saccade并perceive到的图像，我懒得写了，下次吧
    def do_work(self):
        # Perform some designed saccades on the original image
        fix_point = (self.__image__.size[0] // 2, self.__image__.size[1] // 2)
        box = self.saccade(fix_point)
        tmp_image = self.__image__.crop(box)  # crop the original image with saccade
        tmp_result = self.perceive(tmp_image)
        # Do一些图像叠加
        # self.image = 叠加后的图像
        self.image = tmp_image
        return self.image


class Retina(Organ):
    # retina contains lots of cones in its middle area
    # and lots of rods in the peripheral
    # Here the retina is some form of matrix transformation mapping original Image -> perceived Image
    def __init__(self, size):
        self.__name__ = "Retina"
        self.size = size
        self.paving()

    # Todo: paving the retina with cones & rods, form a transformation matrix for the input images of fixed size
    def paving(self):
        (w, h) = self.size

    # Todo: shit, so many to-dos
    def perceive(self, input_image: Image):
        if input_image.size != self.size:
            raise RuntimeError("Size mismatch! The Retina can't perceive!")
        original_image = input_image
        transformed_image = original_image
        return transformed_image


# cones are good at detecting R/G/B value
# distributed mostly in the central area of the retina
def cone(pixel, color='r'):
    color_list = ['r', 'g', 'b']
    return pixel


# rod is good at detecting strength of light
# distributed mostly in the peripheral area of the retina
def rod(pixel):
    return pixel


if __name__ == '__main__':
    image = Image.open("/home/wengqi/1.jpg")
    left_eye = Eye()
    left_eye.input_image(image)
    result = left_eye.do_work()
    result.show()
