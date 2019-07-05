from .htmlcomponents import *
from .htmlcomponents import _tag_class_dict
from addict import Dict


quasar_directives = ['v-close-popup', 'v-close-menu', 'v-ripple', 'v-model', 'v-close-dialog']

class QuasarPage(WebPage):

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        self.template_file='quasar.html'


class QDiv(Div):


    def __init__(self,  **kwargs):

        super().__init__(**kwargs)
        self.vue_type = 'quasar_component'
        self.directives = quasar_directives
        self.attributes.append('key')   # For group transition


class QInput(Input):


    slots = ['before_slot', 'after_slot', 'error_slot', 'hint_slot', 'counter_slot', 'loading_slot']

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        self.vue_type = 'quasar_component'
        self.html_tag = 'q-input'
        self.directives = quasar_directives
        self.prop_list = ['mask', 'fill-mask', 'unmasked-value', 'error', 'error-message', 'rules', 'lazy-rules',
                          'label', 'stack-label', 'hint', 'hide-hint', 'prefix', 'suffix', 'color', 'bg-color', 'dark',
                          'filled', 'outlined', 'borderless', 'standout', 'bottom-slots', 'rounded', 'square', 'dense',
                          'items-aligned', 'disable', 'readonly', 'value', 'type', 'debounce', 'counter', 'maxlength',
                          'autogrow', 'autofocus', 'input-class', 'input-style', 'clearable', 'clear-icon']



    def __setattr__(self, key, value):
        if key in self.__class__.slots:
            self.add_scoped_slot(key, value)
        else:
            self.__dict__[key] = value


    def convert_object_to_dict(self):    # Every object needs to redefine this
        d = super().convert_object_to_dict()
        # d['input_type'] = 'text'     # Needed for vue component updated life hook and event handler
        # d['value'] = str(self.value)
        # d['attrs']['value'] = self.value
        #
        # self.events.extend(['input'])
        #
        # try:
        #     d['attrs']['form'] = self.form.id
        # except:
        #     pass
        return d

_tag_class_dict['q-input'] = QInput


class QAvatar(QDiv):

    def __init__(self,  **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'q-avatar'
        self.prop_list = ['icon', 'size', 'font-size', 'color', 'text-color', 'square', 'rounded']


_tag_class_dict['q-avatar'] = QAvatar


class QBadge(QDiv):

    def __init__(self,  **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'q-badge'
        self.prop_list = ['color', 'text-color', 'floating', 'transparent', 'multi-line', 'label', 'align']


_tag_class_dict['q-badge'] = QBadge


class QBanner(QDiv):

    def __init__(self,  **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'q-banner'
        self.prop_list = ['inline-actions', 'dense', 'rounded']
        # Slots: avatar, action


_tag_class_dict['q-banner'] = QBanner


class QBar(QDiv):

    def __init__(self,  **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'q-bar'
        self.prop_list = ['dense', 'dark']
        # Slots: avatar, action


_tag_class_dict['q-bar'] = QBar


class QBreadcrumbs(QDiv):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'q-breadcrumbs'
        self.prop_list = ['separator', 'active-color', 'gutter', 'separator-color', 'align']

_tag_class_dict['q-breadcrumbs'] = QBreadcrumbs


class QBreadcrumbsEl(QDiv):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'q-breadcrumbs-el'
        self.prop_list = ['to', 'exact', 'append', 'replace', 'active-class', 'exact-active-class', 'label', 'icon']

_tag_class_dict['q-breadcrumbs-el'] = QBreadcrumbsEl


class QButton(QDiv):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'q-btn'
        self.prop_list = ['ripple', 'type', 'to', 'replace', 'label', 'icon', 'icon-right', 'round', 'outline', 'flat',
                          'unelevated', 'rounded', 'push', 'glossy', 'size', 'fab', 'fab-mini', 'color', 'text-color',
                          'no-caps', 'no-wrap', 'dense', 'tabindex', 'align', 'stack', 'stretch', 'loading', 'disable',
                          'percentage', 'dark-percentage']
        # Slots: loading


_tag_class_dict['q-btn'] = QButton


class QBtnGroup(QDiv):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'q-btn-group'
        self.prop_list = ['spread', 'stretch', 'outline', 'flat', 'unelevated', 'rounded', 'push', 'glossy']

_tag_class_dict['q-btn-group'] = QBtnGroup


class QBtnDropdown(QDiv):
#TODO: Finish this, need items to check
    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'q-btn-dropdown'
        self.prop_list = ['spread', 'stretch', 'outline', 'flat', 'unelevated', 'rounded', 'push', 'glossy']
        self.prop_list = ['ripple', 'type', 'to', 'replace', 'label', 'icon', 'icon-right', 'round', 'outline', 'flat',
                          'unelevated', 'rounded', 'push', 'glossy', 'size', 'fab', 'fab-mini', 'color', 'text-color',
                          'no-caps', 'no-wrap', 'dense', 'tabindex', 'align', 'stack', 'stretch', 'loading', 'disable',
                          'percentage', 'dark-percentage']

_tag_class_dict['q-btn-dropdown'] = QBtnDropdown


class QCard(QDiv):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'q-card'
        self.prop_list = ['dark', 'square', 'flat', 'bordered']

_tag_class_dict['q-card'] = QCard


class QCardSection(QDiv):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'q-card-section'
        self.prop_list = []

_tag_class_dict['q-card-section'] = QCardSection


class QCardActions(QDiv):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'q-card-actions'
        self.prop_list = ['align', 'vertical']

_tag_class_dict['q-card-actions'] = QCardActions


class QTabs(QInput):

    slots = []

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.value = kwargs.get('value','')
        # self.vue_type = 'quasar_component'
        self.html_tag = 'q-tabs'
        # self.directives = quasar_directives
        self.prop_list = ['breakpoint', 'vertical', 'align', 'left-icon', 'right-icon', 'shrink', 'switch-indicator',
                          'narrow-indicator', 'inline-label', 'no-caps', 'value', 'active-color', 'active-bg-color',
                          'indicator-color', 'dense']



_tag_class_dict['q-tabs'] = QTabs


class QTab(QDiv):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'q-tab'
        self.prop_list = ['icon', 'label', 'alert', 'no-caps', 'name', 'tabindex', 'disable', 'ripple']

_tag_class_dict['q-tab'] = QTab


class QSplitter(QInput):


    slots = ['before', 'after']

    def __init__(self, **kwargs):

        # self.limits =[10, 90]
        super().__init__(**kwargs)
        self.value = kwargs.get('value', 50.0)
        self.type = 'float'
        # self.vue_type = 'quasar_component'
        self.html_tag = 'q-splitter'
        # self.directives = quasar_directives
        self.prop_list = ['horizontal', 'limits', 'value', 'disable', 'before-class', 'after-class', 'separator-class',
                          'separator-style', 'dark']


_tag_class_dict['q-splitter'] = QSplitter


class QChatMessage(QDiv):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'q-chat-message'
        self.prop_list = ['label-sanitize', 'name-sanitize', 'text-sanitize', 'stamp-sanitize', 'sent', 'label',
                          'name', 'avatar', 'text', 'stamp', 'bg-color', 'text-color', 'size']
        # slot: avatar
        # Note that name is an attribute here, may cause problems

    def convert_object_to_dict(self):  # Every object needs to redefine this

        d = super().convert_object_to_dict()
        try:
            d.pop('text')
        except:
            pass
        return d


_tag_class_dict['q-chat-message'] = QChatMessage


class QChip(QDiv):

    def __init__(self, **kwargs):
        self.selected = False
        self.clickable = False
        self.removable = False
        super().__init__(**kwargs)
        self.html_tag = 'q-chip'
        self.prop_list = ['icon', 'icon-right', 'label', 'tabindex', 'value', 'selected', 'clickable', 'removable',
                          'disable', 'ripple', 'dense', 'color', 'text-color', 'square', 'outline']

        # self.events = ['remove']
        self.add_event('remove')
        def chip_remove(self, message):
            self.show = False
        self.on('input', chip_remove)
        self.on('remove', chip_remove)


    @staticmethod
    def chip_select(self, message):
        self.selected = not self.selected

    def convert_object_to_dict(self):  # Every object needs to redefine this

        d = super().convert_object_to_dict()
        if self.clickable:
            self.on('click', self.chip_select)
        else:
            if 'click' in self.events:
                self.events.remove('click')
            d['attrs'].pop('clickable')
        if not self.selected:
            d['attrs'].pop('selected')
        # Used by the Vue component
        d['selected'] = self.selected
        d['clickable'] = self.clickable
        d['removable'] = self.removable
        return d

_tag_class_dict['q-chip'] = QChip


class QCircularProgress(QDiv):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'q-circular-progress'
        self.prop_list = ['indeterminate', 'show-value', 'reverse', 'angle', 'value', 'min', 'max', 'color', 'center-color' ,
                          'track-color', 'size', 'font-size', 'thickness']


_tag_class_dict['q-circular-progress'] = QCircularProgress


class QColor(QInput):

    slots = []


    def __init__(self, **kwargs):
        self.value = ''
        self.format_model = 'hex'
        super().__init__(**kwargs)
        # self.vue_type = 'quasar_component'
        self.html_tag = 'q-color'
        # self.directives = quasar_directives
        self.prop_list = ['default-view', 'no-header', 'no-footer', 'value', 'default-value', 'format-model',
                          'disable', 'readonly', 'dark']



    def convert_object_to_dict(self):  # Every object needs to redefine this
        d = super().convert_object_to_dict()
        # d['input_type'] = 'text'  # Needed for vue component updated life hook and event handler
        # d['value'] = str(self.value)
        # d['attrs']['value'] = self.value
        # self.events.extend(['input'])
        return d


_tag_class_dict['q-color'] = QColor


class QPopupProxy(QDiv):
    # TODO: Need to add QMenu and QDialog props as they are passed through
    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'q-popup-proxy'
        self.prop_list = ['target', 'context-menu', 'breakpoint']

_tag_class_dict['q-popup-proxy'] = QPopupProxy


class QDialog(QInput):

    slots = []

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.type = 'boolean'
        if self.value:
            self.value = True
        else:
            self.value = False
        # self.vue_type = 'quasar_component'
        # self.directives = quasar_directives
        self.html_tag = 'q-dialog'
        self.prop_list = ['persistent', 'no-esc-dsimiss', 'no-backdrop-dismiss', 'no-route-dismiss', 'auto-close',
                          'transition-show', 'transition-hide', 'no-refocus', 'no-focus', 'seamless', 'maximized',
                          'full-width', 'full-height', 'position', 'value', 'content-class', 'content-style', 'square']



_tag_class_dict['q-dialog'] = QDialog


class QEditor(QInput):

    slots = []

    icon_set = Dict({'align': "format_align_left",
                'bold': "format_bold",
                'center': "format_align_center",
                'code': "code",
                'font': "font_download",
                'fontSize': "format_size",
                'formatting': "text_format",
                'header': "format_size",
                'hr': "remove",
                'hyperlink': "link",
                'indent': "format_indent_increase",
                'italic': "format_italic",
                'justify': "format_align_justify",
                'left': "format_align_left",
                'orderedList': "format_list_numbered",
                'outdent': "format_indent_decrease",
                'print': "print",
                'quote': "format_quote",
                'redo': "redo",
                'removeFormat': "format_clear",
                'right': "format_align_right",
                'size': "format_size",
                'strikethrough': "strikethrough_s",
                'subscript': "vertical_align_bottom",
                'superscript': "vertical_align_top",
                'toggleFullscreen': "fullscreen",
                'underline': "format_underlined",
                'undo': "undo",
                'unorderedList': "format_list_bulleted"})

    lang = Dict({"url": "URL", "bold": "Bold", "italic": "Italic", "strikethrough": "Strikethrough",
            "underline": "Underline", "unorderedList": "Unordered List", "orderedList": "Ordered List",
            "subscript": "Subscript", "superscript": "Superscript", "hyperlink": "Hyperlink",
            "toggleFullscreen": "Toggle Fullscreen", "quote": "Quote", "left": "Left align", "center": "Center align",
            "right": "Right align", "justify": "Justify align", "print": "Print", "outdent": "Decrease indentation",
            "indent": "Increase indentation", "removeFormat": "Remove formatting", "formatting": "Formatting",
            "fontSize": "Font Size", "align": "Align", "hr": "Insert Horizontal Rule", "undo": "Undo", "redo": "Redo",
            "header1": "Header 1", "header2": "Header 2", "header3": "Header 3", "header4": "Header 4",
            "header5": "Header 5", "header6": "Header 6", "paragraph": "Paragraph", "code": "Code",
            "size1": "Very small", "size2": "A bit small", "size3": "Normal", "size4": "Medium-large", "size5": "Big",
            "size6": "Very big", "size7": "Maximum", "defaultFont": "Default Font"})

    simple_options = [['left', 'center', 'right', 'justify'],
        ['bold', 'italic', 'strike', 'underline', 'subscript', 'superscript'],
        ['hr', 'link'], ['undo', 'redo'], ['print', 'fullscreen']]

    fonts = {"arial": "Arial", "arial_black": "Arial Black", "comic_sans": "Comic Sans MS",
             "courier_new": "Courier New", "impact": "Impact", "lucida_grande": "Lucida Grande",
             "times_new_roman": "Times New Roman", "verdana": "Verdana"}

    kitchen_sink = [
        [
            {
                'label': lang.align,
                'icon': icon_set.align,
                'fixedLabel': True,
                'list': 'only-icons',
                'options': ['left', 'center', 'right', 'justify']
            },
            {
                'label': lang.align,
                'icon': icon_set.align,
                'fixedLabel': True,
                'options': ['left', 'center', 'right', 'justify']
            }
        ],
        ['bold', 'italic', 'strike', 'underline', 'subscript', 'superscript'],
        ['token', 'hr', 'link', 'custom_btn'],
        ['print', 'fullscreen'],
        [
            {
                'label': lang.formatting,
                'icon': icon_set.formatting,
                'list': 'no-icons',
                'options': [
                    'p',
                    'h1',
                    'h2',
                    'h3',
                    'h4',
                    'h5',
                    'h6',
                    'code'
                ]
            },
            {
                'label': lang.fontSize,
                'icon': icon_set.fontSize,
                'fixedLabel': True,
                'fixedIcon': True,
                'list': 'no-icons',
                'options': [
                    'size-1',
                    'size-2',
                    'size-3',
                    'size-4',
                    'size-5',
                    'size-6',
                    'size-7'
                ]
            },
            {
                'label': lang.defaultFont,
                'icon': icon_set.font,
                'fixedIcon': True,
                'list': 'no-icons',
                'options': [
                    'default_font',
                    'arial',
                    'arial_black',
                    'comic_sans',
                    'courier_new',
                    'impact',
                    'lucida_grande',
                    'times_new_roman',
                    'verdana'
                ]
            },
            'removeFormat'
        ],
        ['quote', 'unordered', 'ordered'],

        ['undo', 'redo']
    ]

    def __init__(self, **kwargs):
        # https://quasar.dev/vue-components/editor
        self.kitchen_sink = False
        self.toolbar = QEditor.simple_options
        super().__init__(**kwargs)

        # self.vue_type = 'quasar_component'
        # self.directives = quasar_directives
        self.html_tag = 'q-editor'
        self.prop_list = ['fullscreen', 'value', 'readonly', 'disable', 'square', 'flat', 'dense', 'min-height', 'max-height',
                          'height', 'toolbar-outline', 'toolbar-push', 'toolbar-rounded', 'content-style', 'content-class',
                          'definitions', 'fonts', 'toolbar', 'toolbar-color', 'toolbar-text-color', 'toolbar-toggle-color',
                          'toolbar-bg', 'toolbar-outline', 'toolbar-push', 'toolbar-rounded']


    def convert_object_to_dict(self):  # Every object needs to redefine this
        if self.kitchen_sink:
            self.toolbar = QEditor.kitchen_sink
            self.fonts = QEditor.fonts
        d = super().convert_object_to_dict()
        return d

_tag_class_dict['q-editor'] = QEditor


class QExpansionItem(QInput):

    slots = ['default_slot', 'header_slot']

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.type = 'boolean'
        if self.value:
            self.value = True
        else:
            self.value = False
        # self.vue_type = 'quasar_component'
        # self.directives = quasar_directives
        self.html_tag = 'q-expansion-item'
        self.prop_list = ['to', 'exact', 'append', 'replace', 'active-class', 'exact-active-class', 'duration', 'default-opened',
                          'expand-icon-toggle', 'group', 'popup', 'icon', 'expand-icon', 'label', 'label-lines', 'caption',
                          'caption-lines', 'header-inset-level', 'content-inset-level', 'expand-separator', 'switch-toggle-side',
                          'value', 'disable', 'expand-icon-class', 'dark', 'dense', 'dense-toggle', 'header-style', 'header-class']

    def convert_object_to_dict(self):  # Every object needs to redefine this
        d = super().convert_object_to_dict()
        try:
            if d['attrs']['default-opened']:
                d['value'] = True
                d['attrs']['value'] = True
        except:
            pass
        return d

_tag_class_dict['q-expansion-item'] = QExpansionItem


class QImg(QDiv):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'q-img'
        self.prop_list = ['transition', 'alt', 'basic', 'contain', 'position', 'ratio', 'src', 'srcset', 'sizes',
                          'placeholder-src', 'spinner-color', 'spinner-size']
        # Scoped slots: loading, error
        # Events: loading, error

_tag_class_dict['q-img'] = QImg

#TODO Inifinte Scroll

class QInnerLoading(QDiv):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'q-inner-loading'
        self.prop_list = ['transition-show', 'transition-hide', 'showing', 'color', 'size', 'dark']


_tag_class_dict['q-inner-loading'] = QInnerLoading


class Transition(QDiv):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'transition'
        self.prop_list = ['appear', 'appear-class', 'appear-to-class', 'appear-active-class',
                          'enter-class', 'enter-active-class', 'enter-to-class', 'leave-class',
                          'leave-active-class', 'leave-to-class', 'duration', 'mode']


_tag_class_dict['transition'] = Transition


class TransitionGroup(QDiv):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'transition-group'
        self.prop_list = ['appear', 'appear-class', 'appear-to-class', 'appear-active-class',
                          'enter-class', 'enter-active-class', 'enter-to-class', 'leave-class',
                          'leave-active-class', 'leave-to-class', 'duration', 'mode', 'tag', 'key']


_tag_class_dict['transition-group'] = TransitionGroup



class QIcon(QDiv):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'q-icon'
        self.prop_list = ['name', 'color', 'size', 'left', 'right']

_tag_class_dict['q-icon'] = QIcon


class QSpinner(QDiv):

    spinner_types = ['audio', 'ball', 'bars', 'comment', 'cube', 'dots', 'facebook', 'gears', 'grid', 'hearts', 'hourglass',
                     'infinity', 'ios', 'oval', 'pie', 'puff', 'radio', 'rings', 'tail']
    def __init__(self, **kwargs):

        self.size = '1em'
        self.color = 'primary'
        self.spinner_type = ''
        super().__init__(**kwargs)
        self.html_tag = 'q-spinner'
        self.prop_list = ['size', 'color', 'thickness']


    def convert_object_to_dict(self):  # Every object needs to redefine this
        if self.spinner_type in QSpinner.spinner_types:
            self.html_tag = 'q-spinner-' + self.spinner_type
        else:
            self.html_tag = 'q-spinner'
        d = super().convert_object_to_dict()
        return d

#TODO: Take care of all spinner types
_tag_class_dict['q-spinner'] = QSpinner


# List and list items

class QList(QDiv):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'q-list'
        self.prop_list = ['separator', 'padding', 'bordered', 'dense', 'dark']

_tag_class_dict['q-list'] = QList


class QItem(QDiv):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'q-item'
        self.prop_list = ['to', 'exact', 'append', 'replace', 'active-class', 'exact-active-class',
                          'inset-level', 'tag', 'tabindex', 'disable', 'active', 'clickable', 'manual-focus',
                          'focused', 'dark', 'dense']

_tag_class_dict['q-item'] = QItem


class QItemSection(QDiv):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'q-item-section'
        self.prop_list = ['avatar', 'thumbnail', 'side', 'top', 'no-wrap']

_tag_class_dict['q-item-section'] = QItemSection


class QItemLabel(QDiv):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'q-item-label'
        self.prop_list = ['lines', 'overline', 'caption', 'header', 'lines']

_tag_class_dict['q-item-label'] = QItemLabel


class QSeparator(QDiv):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'q-separator'
        self.prop_list = ['spaced', 'inset', 'vertical', 'dark', 'color']

_tag_class_dict['q-separator'] = QSeparator


class QSpace(QDiv):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'q-space'
        self.prop_list = []

_tag_class_dict['q-space'] = QSpace