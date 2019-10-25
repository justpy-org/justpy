import requests
import lxml.html as lh
# import pandas as pd
html_tags = {'main_root': ['html'],
                 'document_metadata': ['base', 'head', 'link', 'meta', 'style', 'title'],
                 'sectioning_root': ['body'],
                 'content_sectioning': ['address', 'article', 'aside', 'footer', 'header', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                                        'hgroup', 'main', 'nav', 'section'],
                 'text_content': ['blockquote', 'dd', 'div', 'dl', 'dt', 'figcaption', 'figure', 'hr', 'li',
                                  'ol', 'p', 'pre', 'ul'],
                 'inline_text_semantics': ['a', 'abbr', 'b', 'bdi', 'bdo', 'br', 'cite', 'code', 'data', 'dfn', 'em',
                                           'i', 'kbd', 'mark', 'q', 'rb', 'rp', 'rt', 'rtc', 'ruby', 's', 'samp', 'small',
                                           'span', 'strong', 'sub', 'sup', 'time', 'tt', 'u', 'var', 'wbr'],
                 'image_and_multimedia': ['area', 'audio', 'img', 'map', 'track', 'video'],
                 'embedded_content': ['embed', 'iframe', 'object', 'param', 'picture', 'source'],
                 'scripting': ['canvas', 'noscript', 'script'],
                 'demarcating_edits': ['del', 'ins'],
                 'table_content': ['caption', 'col', 'colgroup', 'table', 'tbody', 'td', 'tfoot', 'th', 'thead', 'tr'],
                 'forms': ['button', 'datalist', 'fieldset', 'form', 'input', 'label', 'legend', 'meter', 'optgroup',
                           'option', 'output', 'progress', 'select', 'textarea'],
                 'interactive_elements': ['details', 'dialog', 'menu', 'menuitem', 'summary'],
                 'misc': ['template']

                 }

attr_dict1 = {'html': ['xmlns'], 'base': ['href', 'target'], 'head': ['profile'], 'link': ['charset', 'crossorigin', 'href', 'hreflang', 'media', 'rel', 'rev', 'sizes', 'target', 'type'], 'meta': ['charset', 'content', 'http-equiv', 'name', 'scheme'], 'style': ['media', 'type'], 'title': [], 'body': ['alink', 'background', 'bgcolor', 'link', 'text', 'vlink'], 'address': [], 'article': [], 'aside': [], 'footer': [], 'header': [], 'h1': [], 'h2': [], 'h3': [], 'h4': [], 'h5': [], 'h6': [], 'hgroup': [], 'main': [], 'nav': [], 'section': [], 'blockquote': ['cite'], 'dd': [], 'div': ['align'], 'dl': [], 'dt': [], 'figcaption': [], 'figure': [], 'hr': ['align', 'noshade', 'size', 'width'], 'li': ['type', 'value'], 'ol': ['compact', 'reversed', 'start', 'type'], 'p': ['align'], 'pre': ['width'], 'ul': ['compact', 'type'], 'a': ['charset', 'coords', 'download', 'href', 'hreflang', 'media', 'name', 'ping', 'rel', 'rev', 'shape', 'target', 'type'], 'abbr': [], 'b': [], 'bdi': [], 'bdo': ['dir'], 'br': [], 'cite': [], 'code': [], 'data': ['value'], 'dfn': [], 'em': [], 'i': [], 'kbd': [], 'mark': [], 'q': ['cite'], 'rb': [], 'rp': [], 'rt': [], 'rtc': [], 'ruby': [], 's': [], 'samp': [], 'small': [], 'span': [], 'strong': [], 'sub': [], 'sup': [], 'time': ['datetime'], 'tt': [], 'u': [], 'var': [], 'wbr': [], 'area': ['alt', 'coords', 'download', 'href', 'hreflang', 'media', 'nohref', 'rel', 'shape', 'target', 'type'], 'audio': ['autoplay', 'controls', 'loop', 'muted', 'preload', 'src'], 'img': ['align', 'alt', 'border', 'crossorigin', 'height', 'hspace', 'ismap', 'longdesc', 'sizes', 'src', 'srcset', 'usemap', 'vspace', 'width'], 'map': ['name'], 'track': ['default', 'kind', 'label', 'src', 'srclang'], 'video': ['autoplay', 'controls', 'height', 'loop', 'muted', 'poster', 'preload', 'src', 'width'], 'embed': ['height', 'src', 'type', 'width'], 'iframe': ['align', 'frameborder', 'height', 'longdesc', 'marginheight', 'marginwidth', 'name', 'sandbox', 'scrolling', 'src', 'srcdoc', 'width'], 'object': ['align', 'archive', 'border', 'classid', 'codebase', 'codetype', 'data', 'declare', 'form', 'height', 'hspace', 'name', 'standby', 'type', 'usemap', 'vspace', 'width'], 'param': ['name', 'type', 'value', 'valuetype'], 'picture': [], 'source': ['src', 'srcset', 'media', 'sizes', 'type'], 'canvas': ['height', 'width'], 'noscript': [], 'script': ['async', 'charset', 'defer', 'src', 'type', 'xml:space'], 'del': ['cite', 'datetime'], 'ins': ['cite', 'datetime'], 'caption': ['align'], 'col': ['align', 'char', 'charoff', 'span', 'valign', 'width'], 'colgroup': ['align', 'char', 'charoff', 'span', 'valign', 'width'], 'table': ['align', 'bgcolor', 'border', 'cellpadding', 'cellspacing', 'frame', 'rules', 'summary', 'width'], 'tbody': ['align', 'char', 'charoff', 'valign'], 'td': ['abbr', 'align', 'axis', 'bgcolor', 'char', 'charoff', 'colspan', 'headers', 'height', 'nowrap', 'rowspan', 'scope', 'valign', 'width'], 'tfoot': ['align', 'char', 'charoff', 'valign'], 'th': ['abbr', 'align', 'axis', 'bgcolor', 'char', 'charoff', 'colspan', 'headers', 'height', 'nowrap', 'rowspan', 'scope', 'sorted', 'valign', 'width'], 'thead': ['align', 'char', 'charoff', 'valign'], 'tr': ['align', 'bgcolor', 'char', 'charoff', 'valign'], 'button': ['autofocus', 'disabled', 'form', 'formaction', 'formenctype', 'formmethod', 'formnovalidate', 'formtarget', 'name', 'type', 'value'], 'datalist': [], 'fieldset': ['disabled', 'form', 'name'], 'form': ['accept', 'accept-charset', 'action', 'autocomplete', 'enctype', 'method', 'name', 'novalidate', 'target'], 'input': ['accept', 'align', 'alt', 'autocomplete', 'autofocus', 'checked', 'dirname', 'disabled', 'form', 'formaction', 'formenctype', 'formmethod', 'formnovalidate', 'formtarget', 'height', 'list', 'max', 'maxlength', 'min', 'multiple', 'name', 'pattern', 'placeholder', 'readonly', 'required', 'size', 'src', 'step', 'type', 'value', 'width'], 'label': ['for', 'form'], 'legend': ['align'], 'meter': ['form', 'high', 'low', 'max', 'min', 'optimum', 'value'], 'optgroup': ['disabled', 'label'], 'option': ['disabled', 'label', 'selected', 'value'], 'output': ['for', 'form', 'name'], 'progress': ['max', 'value'], 'select': ['autofocus', 'disabled', 'form', 'multiple', 'name', 'required', 'size'], 'textarea': ['autofocus', 'cols', 'dirname', 'disabled', 'form', 'maxlength', 'name', 'placeholder', 'readonly', 'required', 'rows', 'wrap'], 'details': ['open'], 'dialog': ['open'], 'menu': ['label', 'type'], 'menuitem': ['checked', 'command', 'default', 'disabled', 'icon', 'label', 'radiogroup', 'type'], 'summary': [], 'template': []}

attr_dict = {'html': ['xmlns'], 'base': ['href', 'target'],
                 'link': ['crossorigin', 'href', 'hreflang', 'media', 'rel', 'sizes', 'type'],
                 'meta': ['charset', 'content', 'http-equiv', 'name'], 'style': ['media', 'type'],
                 'blockquote': ['cite'], 'li': ['value'], 'ol': ['reversed', 'start', 'type'],
                 'a': ['download', 'href', 'hreflang', 'media', 'ping', 'rel', 'target', 'type'], 'bdo': ['dir'],
                 'data': ['value'], 'q': ['cite'], 'time': ['datetime'],
                 'area': ['alt', 'coords', 'download', 'href', 'hreflang', 'media', 'rel', 'shape', 'target', 'type'],
                 'audio': ['autoplay', 'controls', 'loop', 'muted', 'preload', 'src'],
                 'img': ['alt', 'crossorigin', 'height', 'ismap', 'longdesc', 'sizes', 'src', 'srcset', 'usemap',
                         'width'], 'map': ['name'], 'track': ['default', 'kind', 'label', 'src', 'srclang'],
                 'video': ['autoplay', 'controls', 'height', 'loop', 'muted', 'poster', 'preload', 'src', 'width'],
                 'embed': ['height', 'src', 'type', 'width'],
                 'iframe': ['height', 'name', 'sandbox', 'src', 'srcdoc', 'width'],
                 'object': ['data', 'form', 'height', 'name', 'type', 'usemap', 'width'], 'param': ['name', 'value'],
                 'source': ['src', 'srcset', 'media', 'sizes', 'type'], 'canvas': ['height', 'width'],
                 'script': ['async', 'charset', 'defer', 'src', 'type'], 'del': ['cite', 'datetime'],
                 'ins': ['cite', 'datetime'], 'col': ['span'], 'colgroup': ['span'],
                 'td': ['colspan', 'headers', 'rowspan'],
                 'th': ['abbr', 'colspan', 'headers', 'rowspan', 'scope', 'sorted'],
                 'button': ['autofocus', 'disabled', 'form', 'formaction', 'formenctype', 'formmethod',
                            'formnovalidate', 'formtarget', 'name', 'type', 'value'],
                 'fieldset': ['disabled', 'form', 'name'],
                 'form': ['accept-charset', 'action', 'autocomplete', 'enctype', 'method', 'name', 'novalidate',
                          'target'],
                 'input': ['accept', 'alt', 'autocomplete', 'autofocus', 'checked', 'dirname', 'disabled', 'form',
                           'formaction', 'formenctype', 'formmethod', 'formnovalidate', 'formtarget', 'height', 'list',
                           'max', 'maxlength', 'min', 'multiple', 'name', 'pattern', 'placeholder', 'readonly',
                           'required', 'size', 'src', 'step', 'type', 'value', 'width'], 'label': ['for', 'form'],
                 'meter': ['form', 'high', 'low', 'max', 'min', 'optimum', 'value'], 'optgroup': ['disabled', 'label'],
                 'option': ['disabled', 'label', 'selected', 'value'], 'output': ['for', 'form', 'name'],
                 'progress': ['max', 'value'],
                 'select': ['autofocus', 'disabled', 'form', 'multiple', 'name', 'required', 'size'],
                 'textarea': ['autofocus', 'cols', 'dirname', 'disabled', 'form', 'maxlength', 'name', 'placeholder',
                              'readonly', 'required', 'rows', 'wrap'], 'details': ['open'], 'dialog': ['open'],
                 'menu': ['label', 'type'],
                 'menuitem': ['checked', 'command', 'default', 'disabled', 'icon', 'label', 'radiogroup', 'type']}


def scrape(url):
    page = requests.get(url)
    doc = lh.fromstring(page.content)
    tr_elements = doc.xpath('//tr')
    result_list = []
    print_flag = False
    for e in tr_elements:
        name = e[0].text_content()
        try:
            desc = e[2].text_content()
        except:
            desc = ''
        if print_flag:
            print(name)
            if not desc.startswith('Not supported in HTML5'):
                result_list.append(name)
        if name=='Attribute':
            print_flag = True
    return result_list


# r = scrape('https://www.w3schools.com/tags/tag_ul.asp')
# print(r)

def create_attribute_dict():
    attribute_dict = {}
    for key, value in html_tags.items():
        print(value)
        for tag in value:
            r = scrape(f'https://www.w3schools.com/tags/tag_{tag}.asp')
            if r:
                attribute_dict[tag] = r
    print(attribute_dict)

# create_attribute_dict()

def clean_dict(d):
    temp = {}
    for key, value in d.items():
        if value:
            temp[key] = value
    print(temp)

# clean_dict(attr_dict)
# a1 = {}
# for key,value in sorted(attr_dict.items()):
#     a1[key] = value
#
# print(a1)

def tailwind_scrape(url):
    page = requests.get(url)
    doc = lh.fromstring(page.content)
    tr_elements = doc.xpath('//li')
    l = []
    for e in tr_elements:
        for g in e:
            s = g.attrib
            print(s['href'][6:], s)
            l.append(s['href'][6:])
            s = g.text_content()
            # if s[0]=='.':
            #     l.append(s[1:])
            # print(g.text_content())
            # print(g.get('href'))
    return l

def tailwind_scrape_options(url):
    page = requests.get(url)
    doc = lh.fromstring(page.content)
    tr_elements = doc.xpath('//tr')
    l = []
    for e in tr_elements:
        for g in e:
            s = g.text_content()
            try:
                if s[0]=='.':
                    l.append(s[1:])
            except:
                pass
            # print(g.text_content())
            # print(g.get('href'))
    return l


#print(tailwind_scrape('https://tailwindcss.com/docs/padding'))
tw = [
    'container', 'display', 'float', 'object-fit', 'object-position', 'overflow', 'position', 'top-right-bottom-left',
    'visibility', 'z-index', 'font-family', 'font-size', 'font-smoothing', 'font-style', 'font-weight',
    'letter-spacing', 'line-height', 'list-style-type', 'list-style-position', 'text-align', 'text-color',
    'text-decoration', 'text-transform', 'vertical-align', 'whitespace', 'word-break', 'background-attachment',
    'background-color', 'background-position', 'background-repeat', 'background-size', 'border-color', 'border-style',
    'border-width', 'border-radius', 'flex-direction', 'flex-wrap', 'align-items', 'align-content', 'align-self',
    'justify-content', 'flex', 'flex-grow', 'flex-shrink', 'order', 'padding', 'margin', 'width', 'min-width',
    'max-width', 'height', 'min-height', 'max-height', 'border-collapse', 'table-layout', 'box-shadow', 'opacity',
    'appearance', 'cursor', 'outline', 'pointer-events', 'resize', 'user-select', 'fill', 'stroke']

# g = tailwind_scrape_options('https://tailwindcss.com/docs/padding')
# print(g)

def create_tailwind_file():
    with open('tailwind___new.py', 'w') as f:
        tw_dict = {}
        tw_reverse_dict = {}
        for t in tw:
            g = tailwind_scrape_options(f'https://tailwindcss.com/docs/{t}')
            t_new = t.replace('-', '_')
            print(t_new, g)
            tw_dict[t_new] = g
            for i in g:
                tw_reverse_dict[i] = t_new

        f.write(str(tw_dict))
        f.write('\n\n')
        f.write(str(tw_reverse_dict))
    print(str(tw_dict))



# create_tailwind_file()