
1.制作眼睛Eye

基于RGB通道来制作Cones(视锥)细胞

Cones有三种，分别对R, G, B通道敏感，并且分布在视网膜中央，只能检测强光

Rods用来干嘛？检测弱光条件下的轮廓？

Design: 目标是还原一张图片。使用Pillow库做图像输入输出和展示，eye可以眼动，每次focus on part of the picture.

Retina接受一个固定大小image，每个像素会通过一个rod或者cone通道处理(rod, cone定义为一个信息处理通道)

返回