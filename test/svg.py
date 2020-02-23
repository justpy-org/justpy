import csv
from collections import OrderedDict


# ['accumulate', 'animate', 'animateMotion', 'animateTransform']
no_list = ['id']
svg_tags_use = ['animate', 'animateMotion', 'animateTransform', 'circle', 'clipPath', 'defs',
            'desc', 'discard', 'ellipse', 'feBlend', 'feColorMatrix', 'feComponentTransfer', 'feComposite',
            'feConvolveMatrix', 'feDiffuseLighting', 'feDisplacementMap', 'feDistantLight', 'feDropShadow', 'feFlood',
            'feFuncA', 'feFuncB', 'feFuncG', 'feFuncR', 'feGaussianBlur', 'feImage', 'feMerge', 'feMergeNode',
            'feMorphology', 'feOffset', 'fePointLight', 'feSpecularLighting', 'feSpotLight', 'feTile', 'feTurbulence',
            'filter', 'foreignObject', 'g', 'image', 'line', 'linearGradient', 'marker', 'mask', 'metadata',
            'mpath', 'path', 'pattern', 'polygon', 'polyline', 'radialGradient', 'rect', 'set', 'stop',
            'svg', 'switch', 'symbol', 'text', 'textPath', 'tspan', 'use', 'view']
def read_svg():
    svg_dict = {}
    with open('svg1.txt') as csvfile:
        my_reader = csv.reader(csvfile)
        for row in my_reader:
            # print(row)
            print(row)
            print(row[1:])
            attr = row[0]
            for tag in list(row[1:]):
                print(tag)
                try:
                    svg_dict[tag] = svg_dict[tag] + [attr]
                except:
                    svg_dict[tag] = [attr]
            # print(row)
            # print(row[0])
            # print(row[1])
    new_dict = {}

    print(dict(OrderedDict(sorted(svg_dict.items()))))

def stam():
    s = f''
    for v in svg_tags_use:
        c = v[0].capitalize()
        s=f'{s} = {c + v[1:]}'
    print(s)

stam()
# read_svg()

