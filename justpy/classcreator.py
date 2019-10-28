
html_global_attributes =['accesskey', 'class', 'contenteditable', 'dir', 'draggable', 'dropzone', 'hidden', 'id',
                             'lang', 'spellcheck', 'style', 'tabindex', 'title']

# https://developer.mozilla.org/en-US/docs/Web/HTML/Element
html_tags = {'main_root': ['html'],
             'document_metadata': ['base', 'head', 'link', 'meta', 'style', 'title'],
             'sectioning_root': ['body'],
             'content_sectioning': ['address', 'article', 'aside', 'div', 'footer', 'header', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                                     'main', 'nav', 'section'],
             'text_content': ['blockquote', 'dd', 'dl', 'dt', 'figcaption', 'figure', 'hr', 'li',
                              'ol', 'p', 'pre', 'ul'],
             'inline_text_semantics': ['a', 'abbr', 'b', 'bdi', 'bdo', 'br', 'cite', 'code', 'data', 'dfn', 'em',
                                       'i', 'kbd', 'mark', 'q', 'rb', 'rp', 'rt', 'rtc', 'ruby', 's', 'samp', 'small',
                                       'span', 'strong', 'sub', 'sup', 'time', 'tt', 'u', 'var', 'wbr'],
             'image_and_multimedia': ['area', 'audio', 'img', 'map', 'track', 'video'],
             'embedded_content': ['embed', 'iframe', 'object', 'param', 'picture', 'source'],
             'scripting': ['canvas', 'noscript', 'script'],
             'demarcating_edits': ['del', 'ins'],
             'table_content': ['caption', 'col', 'colgroup', 'table', 'tbody', 'td', 'tfoot', 'th', 'thead', 'tr'],
             'forms': ['button', 'input', 'datalist', 'fieldset', 'form', 'label', 'legend', 'meter', 'optgroup',
                       'option', 'output', 'progress', 'select', 'textarea'],
             'interactive_elements': ['details', 'dialog', 'summary'], # 'menu', 'menuitem'
             'misc': ['template']  # 'template'

             }

no_create_list = ['div', 'input', 'form', 'label', 'output', 'select', 'textarea', 'a']

# https://www.w3schools.com/tags/ref_byfunc.asp
_tag_create_list = ['address', 'article', 'aside', 'footer', 'header', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'main', 'nav', 'section',
                'blockquote', 'dd', 'dl', 'dt', 'figcaption', 'figure', 'hr', 'li', 'ol', 'p', 'pre', 'ul',
                'abbr', 'b', 'bdi', 'bdo', 'br', 'cite', 'code', 'data', 'dfn', 'em', 'i', 'kbd', 'mark', 'q', 'rb',
                'rp', 'rt', 'rtc', 'ruby', 's', 'samp', 'small', 'span', 'strong', 'sub', 'sup', 'time', 'tt', 'u', 'var', 'wbr',
                'area', 'audio', 'img', 'map', 'track', 'video',
                'embed', 'iframe', 'object', 'param', 'picture', 'source',
                'del', 'ins',
                'caption', 'col', 'colgroup', 'table', 'tbody', 'td', 'tfoot', 'th', 'thead', 'tr',
                'button', 'fieldset', 'legend', 'meter', 'optgroup', 'option', 'progress',  # datalist not supported
                'details', 'summary' # dialog not supported
               ]

# Only tags that have unique attributes that are supported by HTML 5 are in this dict
_attr_dict = {'a': ['download', 'href', 'hreflang', 'media', 'ping', 'rel', 'target', 'type'],
             'area': ['alt', 'coords', 'download', 'href', 'hreflang', 'media', 'rel', 'shape', 'target', 'type'],
             'audio': ['autoplay', 'controls', 'loop', 'muted', 'preload', 'src'], 'base': ['href', 'target'],
             'bdo': ['dir'], 'blockquote': ['cite'],
             'button': ['autofocus', 'disabled', 'form', 'formaction', 'formenctype', 'formmethod',
                        'formnovalidate', 'formtarget', 'name', 'type', 'value'], 'canvas': ['height', 'width'],
             'col': ['span'], 'colgroup': ['span'], 'data': ['value'], 'del': ['cite', 'datetime'],
             'details': ['open'], 'dialog': ['open'], 'embed': ['height', 'src', 'type', 'width'],
             'fieldset': ['disabled', 'form', 'name'],
             'form': ['accept-charset', 'action', 'autocomplete', 'enctype', 'method', 'name', 'novalidate',
                      'target'], 'html': ['xmlns'],
             'iframe': ['height', 'name', 'sandbox', 'src', 'srcdoc', 'width'],
             'img': ['alt', 'crossorigin', 'height', 'ismap', 'longdesc', 'sizes', 'src', 'srcset', 'usemap',
                     'width'],
             'input': ['accept', 'alt', 'autocomplete', 'autofocus', 'checked', 'dirname', 'disabled', 'form',
                       'formaction', 'formenctype', 'formmethod', 'formnovalidate', 'formtarget', 'height', 'list',
                       'max', 'maxlength', 'min', 'multiple', 'name', 'pattern', 'placeholder', 'readonly',
                       'required', 'size', 'src', 'step', 'type', 'value', 'width'], 'ins': ['cite', 'datetime'],
             'label': ['for', 'form'], 'li': ['value'],
             'link': ['crossorigin', 'href', 'hreflang', 'media', 'rel', 'sizes', 'type'], 'map': ['name'],
             'meta': ['charset', 'content', 'http-equiv', 'name'],
             'meter': ['form', 'high', 'low', 'max', 'min', 'optimum', 'value'],
             'object': ['data', 'form', 'height', 'name', 'type', 'usemap', 'width'],
             'ol': ['reversed', 'start', 'type'], 'optgroup': ['disabled', 'label'],
             'option': ['disabled', 'label', 'selected', 'value'], 'output': ['for', 'form', 'name'],
             'param': ['name', 'value'], 'progress': ['max', 'value'], 'q': ['cite'],
             'script': ['async', 'charset', 'defer', 'src', 'type'],
             'select': ['autofocus', 'disabled', 'form', 'multiple', 'name', 'required', 'size'],
             'source': ['src', 'srcset', 'media', 'sizes', 'type'], 'style': ['media', 'type'],
             'td': ['colspan', 'headers', 'rowspan'],
             'textarea': ['autofocus', 'cols', 'dirname', 'disabled', 'form', 'maxlength', 'name', 'placeholder',
                          'readonly', 'required', 'rows', 'wrap'],
             'th': ['abbr', 'colspan', 'headers', 'rowspan', 'scope', 'sorted'], 'time': ['datetime'],
             'track': ['default', 'kind', 'label', 'src', 'srclang'],
             'video': ['autoplay', 'controls', 'height', 'loop', 'muted', 'poster', 'preload', 'src', 'width']}




# window.addEventListener("afterprint", function(event){...});
# window.onafterprint = function(event){...};
windows_events = ['afterprint', 'beforeprint', 'beforeunload', 'error', 'hashchange', 'load',
                          'message', 'offline', 'online', 'pagehide', 'pageshow', 'popstate',
                          'resize', 'storage', 'unload']
form_events = ['blur', 'change', 'contextmenu', 'focus', 'input', 'invalid', 'reset', 'search', 'select', 'submit']
keyboard_events = ['keydown', 'keypress', 'keyup']
mouse_events = ['click', 'dblclick', 'mousedown', 'mousemove', 'mouseout', 'mouseover', 'mouseup', 'wheel',
                'mouseenter', 'mouseleave']


class_format = f'''\
class TextJP(Div):


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'span'


'''

def class_template(tag, tag_attributes):
    return f'''
class {tag.capitalize()}(Div):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = '{tag}'
        self.attributes = {tag_attributes}


_tag_class_dict['{tag}'] = {tag.capitalize()}

'''


def create_class_file():
    with open('class_file_table.py', 'w') as f:
       f.write('class DivJP: \n    pass\n\n\n')
       f.write('_tag_class_dict = {}\n\n\n')
       # tag_list = html_tags['content_sectioning'] + html_tags['text_content'] + html_tags['inline_text_semantics'] +html_tags['forms']
       tag_list = html_tags['table_content']
       for tag in tag_list:
           try:
               tag_attributes = _attr_dict[tag]
               print(tag, tag_attributes)
           except:
               tag_attributes = []
           f.write(class_template(tag, tag_attributes))

    print('finished class import')

# create_class_file()
s = ''
for tag in _tag_create_list:
    s += tag.capitalize() + '='
print(s)