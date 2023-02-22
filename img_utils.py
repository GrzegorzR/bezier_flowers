import copy


class Element(object):
    def __new__(cls, *args, **kwargs):
        instance = super(Element, cls).__new__(cls)
        instance.id = hash(instance)
        return instance

    def __init__(self, svg_elem):
        self.svg_elem = svg_elem
        self.rotation = (0, 0, 0)
        self.translation = (0, 0)
        self.transform = ''
        self.id = str(hash(self))

    def draw(self, surface):
        self.svg_elem.args['transform'] = self.transform
        self.svg_elem.id = self.id
        surface.append(self.svg_elem)

    def apply_transform(self, transform_str):
        self.transform = transform_str + self.transform


class ElementContainer:
    def __init__(self, elements):
        self.elements = elements

    def apply_transform(self, transform_str):
        for e in self.elements:
            e.apply_transform(transform_str)

    def draw(self, surface):
        for e in self.elements:
            e.draw(surface)


class Transformation:
    def __init__(self, trans_str):
        self.trans_str = trans_str

    def __call__(self, *args, **kwargs):
        elem = args[0]
        res = copy.deepcopy(elem)
        res.apply_transform(self.trans_str)
        return res


class Rotation(Transformation):
    def __init__(self, r, x, y):
        self.r, self.x, self.y = r, x, y
        trans_str = 'rotate({}, {}, {}) '.format(str(self.r), str(self.x), str(self.y))
        super().__init__(trans_str)


class Translation(Transformation):
    def __init__(self, x, y):
        self.x, self.y = x, y
        trans_str = 'translate({}, {}) '.format(str(self.x), str(self.y))
        super().__init__(trans_str)

class Scale(Transformation):
    def __init__(self, scale_parameter):
        trans_str = 'scale({}) '.format(scale_parameter)
        super().__init__(trans_str)

class RoseTrans():
    def __init__(self, order_num, x_p=0, y_p=0):
        self.order_num = order_num
        self.x_p = x_p
        self.y_p = y_p

    def __call__(self, *args, **kwargs):
        elem = args[0]
        elem_copy = copy.deepcopy(elem)
        result = []
        for n in range(self.order_num):
             result.append(Rotation((n / self.order_num) * 360., self.x_p, self.y_p)(elem_copy))

        return ElementContainer(result)