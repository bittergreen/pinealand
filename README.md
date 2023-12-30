# pinealand

Trying to understand the brain by coding it.

A layman project, only for personal learning purposes.

## backgrounds

Pinealand这个名字取自笛卡尔对"Pineal Gland"松果体的错误理解，他认为松果体是连接灵魂与肉体的器官。

我曾经想实现这个器官(through coding)，但作为外行人，一直没有开启这个过于宏大的项目。

最近读认知心理学，发现其中的一些主题可以和代码结合来研究。比如对于视觉中的色彩认知，理解色调、明度和饱和度的最好方式大概就是写代码了。

再比如Attention这一章节中的视觉搜索部分(visual search)，为啥feature search中目标刺激检出的反应时间和干扰刺激数量无关呢？(pop-out)

也就是说这个算法复杂度是O(1)，我们可以结合对Faster-RCNN之类的目标检测网络来研究这个问题。

注：可能并不意味着O(1)，而是pop-out有bottom-up的机制，在视觉皮层的浅层就直接检测出，并且bottom-up地把信息报上来了

而一些复杂的检测需要用到高级视觉皮层的信息，所以就无法pop-out，而需要注视一段时间才能处理，并通过眼动改变注视点，造成O(n)的感觉。

在这个背景下，我觉得Pinealand项目可以开始做了。

完全是个外行的兴趣使然，个人学习用。

## project

项目暂时分为knowledge部分和code部分

knowledge部分(./knowledge)存放一些neuroscience/cognitive psychology/computing的知识， 后续也会把notion上的论文和书籍的读后感迁移过来。

code部分(./pinealand)设计为一个Python module，尝试写一些感兴趣的额话题，比如说视觉里的rods & cones之类的，自娱自乐。