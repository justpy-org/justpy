from .htmlcomponents import *
from .htmlcomponents import _tag_class_dict


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


class QInput(Input):


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
        # self.events = ['input']

    def convert_object_to_dict(self):    # Every object needs to redefine this
        d = super().convert_object_to_dict()
        d['input_type'] = 'text'     # Needed for vue component updated life hook and event handler
        d['value'] = str(self.value)
        d['attrs']['value'] = self.value
        # d['checked'] = self.checked
        # self.events.extend(['input', 'blur', 'focus'])
        self.events.extend(['input'])
        # if self.checked:
        #     d['attrs']['checked'] = True
        # else:
        #     d['attrs']['checked'] = False
        try:
            d['attrs']['form'] = self.form.id
        except:
            pass
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


class QTabs(Input):

    def __init__(self, **kwargs):
        self.value = 'Movies'
        super().__init__(**kwargs)
        self.vue_type = 'quasar_component'
        self.html_tag = 'q-tabs'
        self.directives = quasar_directives
        self.prop_list = ['breakpoint', 'vertical', 'align', 'left-icon', 'right-icon', 'shrink', 'switch-indicator',
                          'narrow-indicator', 'inline-label', 'no-caps', 'value', 'active-color', 'active-bg-color',
                          'indicator-color', 'dense']


    def convert_object_to_dict(self):  # Every object needs to redefine this
        d = super().convert_object_to_dict()
        d['input_type'] = 'text'  # Needed for vue component updated life hook and event handler
        d['value'] = str(self.value)
        d['attrs']['value'] = self.value
        # d['checked'] = self.checked
        # self.events.extend(['input', 'blur', 'focus'])
        self.events.extend(['input'])
        # if self.checked:
        #     d['attrs']['checked'] = True
        # else:
        #     d['attrs']['checked'] = False
        # try:
        #     d['attrs']['form'] = self.form.id
        # except:
        #     pass
        return d

_tag_class_dict['q-tabs'] = QTabs


class QTab(QDiv):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'q-tab'
        self.prop_list = ['icon', 'label', 'alert', 'no-caps', 'name', 'tabindex', 'disable', 'ripple']

_tag_class_dict['q-tab'] = QTab


class QTabPanels(Input):

    def __init__(self, **kwargs):
        self.value = ''
        super().__init__(**kwargs)
        self.html_tag = 'q-tab-panels'
        self.vue_type = 'quasar_component'
        self.directives = quasar_directives
        self.prop_list = ['keep-alive', 'animated', 'infinite', 'swipeable', 'transition-prev', 'transition-next', 'value']

    def convert_object_to_dict(self):  # Every object needs to redefine this
        d = super().convert_object_to_dict()
        d['input_type'] = 'text'  # Needed for vue component updated life hook and event handler
        d['value'] = str(self.value)
        d['attrs']['value'] = self.value
        # d['checked'] = self.checked
        # self.events.extend(['input', 'blur', 'focus'])
        self.events.extend(['input'])
        # if self.checked:
        #     d['attrs']['checked'] = True
        # else:
        #     d['attrs']['checked'] = False
        # try:
        #     d['attrs']['form'] = self.form.id
        # except:
        #     pass
        return d

_tag_class_dict['q-tab-panels'] = QTabPanels


class QTabPanel(QDiv):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'q-tab-panel'
        self.prop_list = ['name', 'disable']

_tag_class_dict['q-tab-panel'] = QTabPanel



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