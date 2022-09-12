import hjson

from .htmlcomponents import *
from .htmlcomponents import _tag_class_dict, parse_dict
from addict import Dict

quasar_directives = [
    "v-close-popup",
    "v-close-menu",
    "v-ripple",
    "v-model",
    "v-close-dialog",
]


class QuasarPage(WebPage):
    """
    a Quasar based WebPage
    """

    def __init__(self, **kwargs):
        """
        constructor
        """
        super().__init__(**kwargs)
        self.tailwind = kwargs.get("tailwind", False)
        self.template_file = "quasar.html"
        self.quasar = True

    async def set_dark_mode(self, flag):
        try:
            websocket_dict = WebPage.sockets[self.page_id]
        except:
            return self
        for websocket in list(websocket_dict.values()):
            try:
                WebPage.loop.create_task(
                    websocket.send_json({"type": "page_mode_update", "dark": flag})
                )
            except:
                print("Problem with websocket in page update, ignoring")
        return self

    async def toggle_full_screen(self):
        await self.run_javascript("Quasar.AppFullscreen.toggle()")
        return True

class QDiv(Div):
    slots = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vue_type = "quasar_component"
        self.directives = quasar_directives

    def __setattr__(self, key, value):
        if key in self.slots:
            q_slot = key[: key.index("_slot")].replace("_", "-")
            self.add_scoped_slot(q_slot, value)
        else:
            super().__setattr__(key, value)


class _QInputBase(Input):
    """
    Base Class for Quasar Input
    """

    slots = []

    def __init__(self, **kwargs):
        """
        constructor
        """
        self.disable_input_event = False
        super().__init__(**kwargs)
        self.vue_type = "quasar_component"
        self.directives = quasar_directives
        self.disable_events = False
        self.prop_list = []
        self.attributes = []
        self.evaluate_prop = []

    def __setattr__(self, key, value):
        if key == "options":
            if isinstance(value, str):
                self.load_json(value)
            else:
                self.__dict__[key] = value
        elif key in self.slots:
            q_slot = key[: key.index("_slot")].replace("_", "-")
            self.add_scoped_slot(q_slot, value)
        else:
            self.__dict__[key] = value

    def model_update(self):
        update_value = self.model[0].data[self.model[1]]
        self.value = update_value

    def load_json(self, options_string):
        self.options = hjson.loads(options_string.encode("ascii", "ignore"))
        return self.options

    def load_json_from_file(self, file_name):
        with open(file_name, "r") as f:
            self.options = hjson.loads(f.read().encode("ascii", "ignore"))
        return self.options

    def convert_object_to_dict(self):

        d = super().convert_object_to_dict()
        if self.disable_events:
            d["events"] = []
        d["evaluate_prop"] = self.evaluate_prop
        d["disable_input_event"] = self.disable_input_event
        return d


QInputBase = _QInputBase


@parse_dict
class QInput(_QInputBase):
    """
    https://quasar.dev/vue-components/input
    """

    html_tag = "q-input"
    slots = [
        "default_slot",
        "before_slot",
        "after_slot",
        "error_slot",
        "hint_slot",
        "counter_slot",
        "loading_slot",
        "prepend_slot",
        "append_slot",
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = [
            "mask",
            "fill-mask",
            "unmasked-value",
            "error",
            "error-message",
            "rules",
            "lazy-rules",
            "label",
            "stack-label",
            "hint",
            "hide-hint",
            "prefix",
            "suffix",
            "color",
            "bg-color",
            "dark",
            "filled",
            "outlined",
            "borderless",
            "standout",
            "bottom-slots",
            "rounded",
            "square",
            "dense",
            "items-aligned",
            "disable",
            "readonly",
            "value",
            "type",
            "debounce",
            "counter",
            "maxlength",
            "autogrow",
            "autofocus",
            "input-class",
            "input-style",
            "clearable",
            "clear-icon",
            "placeholder",
            "min",
            "max",
            "loading",
        ]

        self.allowed_events = [
            "keypress",
            "input",
            "focus",
            "blur",
            "change",
        ]  # Not different from focus and blur in documentation
        self.set_keyword_events(**kwargs)
        self.evaluate_prop = ["rules"]


class QInputBlur(QInput):
    def before_event_handler(self, msg):
        logging.debug(
            "%s %s %s %s %s", "before ", self.type, msg.event_type, msg.input_type, msg
        )
        if hasattr(self, "model"):
            self.model[0].data[self.model[1]] = msg.value
        self.value = msg.value

    def convert_object_to_dict(self):
        d = super().convert_object_to_dict()
        d["disable_input_event"] = True
        if "blur" not in self.events:
            self.events.append("blur")
        return d


class QInputChange(QInput):
    def before_event_handler(self, msg):
        logging.debug(
            "%s %s %s %s %s", "before ", self.type, msg.event_type, msg.input_type, msg
        )
        if hasattr(self, "model"):
            self.model[0].data[self.model[1]] = msg.value
        self.value = msg.value

    def convert_object_to_dict(self):
        d = super().convert_object_to_dict()
        d["disable_input_event"] = True
        try:
            d["events"].remove("input")
        except:
            pass
        if "change" not in self.events:
            self.events.append("change")
        return d


@parse_dict
class QField(QDiv):
    html_tag = "q-field"
    slots = [
        "default_slot",
        "before_slot",
        "prepend_slot",
        "append_slot",
        "after_slot",
        "label_slot",
        "error_slot",
        "hint_slot",
        "counter_slot",
        "loading_slot",
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = [
            "error",
            "rules",
            "reactive-rules",
            "lazy-rules",
            "autofocus",
            "name",
            "error-message",
            "no-error-icon",
            "label",
            "stack-label",
            "hint",
            "hide-hint",
            "prefix",
            "suffix",
            "loading",
            "clearable",
            "clear-icon",
            "label-slot",
            "bottom-slots",
            "counter",
            "maxlength",
            "disable",
            "readonly",
            "label-color",
            "color",
            "bg-color",
            "dark",
            "filled",
            "outlined",
            "borderless",
            "standout",
            "hide-bottom-space",
            "rounded",
            "square",
            "dense",
            "item-aligned",
            "value",
        ]

        self.allowed_events = ["clear", "input", "focus", "blur"]


@parse_dict
class QSelect(_QInputBase):
    html_tag = "q-select"
    slots = [
        "default_slot",
        "before_slot",
        "after_slot",
        "error_slot",
        "hint_slot",
        "counter_slot",
        "loading_slot",
        "selected_slot",
        "nooption_slot",
        "selecteditem_slot",
        "option_slot",
        "prepend_slot",
        "append_slot",
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "object"
        self.value = kwargs.get("value", None)
        self.prop_list = [
            "color",
            "bg-color",
            "dark",
            "filled",
            "outlined",
            "borderless",
            "standout",
            "hide-bottom-space",
            "rounded",
            "square",
            "dense",
            "popup-content-class",
            "popup-content-style",
            "error",
            "rules",
            "lazy-rules",
            "loading",
            "clearable",
            "autofocus",
            "hide-dropdown-icon",
            "fill-input",
            "new-value-mode",
            "transition-show",
            "transition-hide",
            "error-message",
            "no-error-icon",
            "label",
            "stack-label",
            "hint",
            "hide-hint",
            "prefix",
            "suffix",
            "clear-icon",
            "bottom-slots",
            "counter",
            "items-aligned",
            "dropdown-icon",
            "use-input",
            "input-debounce",
            "value",
            "multiple",
            "emit-value",
            "options",
            "options-value",
            "option-label",
            "option-disable",
            "options-dense",
            "options-dark",
            "options-selected-class",
            "options-cover",
            "options-sanitize",
            "map-options",
            "display-value",
            "display-value-sanitize",
            "hide-selected",
            "max-values",
            "use-chips",
            "disable",
            "readonly",
            "behavior",
            "input-class",
            "input-style",
            "virtual-scroll-slice-size",
            "virtual-scroll-item-size",
            "virtual-scroll-sticky-size-start",
            "virtual-scroll-sticky-size-end",
        ]

        self.allowed_events = [
            "input",
            "remove",
            "add",
            "new-value",
            "filter",
            "filter-abort",
            "focus",
            "blur",
            "clear",
        ]
        # self.set_keyword_events(**kwargs)


@parse_dict
class QOptionGroup(_QInputBase):
    html_tag = "q-option-group"
    slots = []

    def __init__(self, **kwargs):
        self.options = []
        super().__init__(**kwargs)
        # Type: radio | checkbox | toggle https://quasar.dev/vue-components/option-group
        if self.type == "checkbox" or self.type == "toggle":
            self.value = kwargs.get("value", [])
        else:
            self.type = "radio"
            self.value = kwargs.get("value", "")
        self.prop_list = [
            "keep-color",
            "type",
            "left-label",
            "inline",
            "value",
            "options",
            "disable",
            "size",
            "color",
            "dark",
            "dense",
        ]
        self.allowed_events = ["input"]
        # self.set_keyword_events(**kwargs)

    def before_event_handler(self, msg):
        logging.debug(
            "%s %s %s %s %s", "before ", self.type, msg.event_type, msg.input_type, msg
        )
        if hasattr(self, "model"):
            self.model[0].data[self.model[1]] = msg.value
        self.value = msg.value

    def convert_object_to_dict(self):

        d = super().convert_object_to_dict()
        d["events"] = ["before", "input"]
        return d


@parse_dict
class QBtnToggle(_QInputBase):
    html_tag = "q-btn-toggle"
    slots = []

    def __init__(self, **kwargs):
        self.options = []
        super().__init__(**kwargs)
        self.type = "object"
        self.value = kwargs.get("value", None)
        self.prop_list = [
            "spread",
            "no-caps",
            "no-wrap",
            "stack",
            "stretch",
            "value",
            "options",
            "readonly",
            "disable",
            "ripple",
            "color",
            "text-color",
            "toggle-color",
            "toggle-text-color",
            "outline",
            "flat",
            "unelevated",
            "rounded",
            "push",
            "glossy",
            "size",
            "dense",
            "clearable",
        ]
        self.allowed_events = ["input"]
        # self.set_keyword_events(**kwargs)


@parse_dict
class QSlider(_QInputBase):
    # TODO: Deal with label-value prop, for now use suffix
    html_tag = "q-slider"
    slots = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "float"
        self.value = kwargs.get("value", 0)
        # The label suffix is a stop gap till full label-value prop implemented
        self.label_suffix = kwargs.get("label_suffix", "")
        self.prop_list = [
            "label-always",
            "snap",
            "label",
            "label-value",
            "label-always",
            "markers",
            "tabindex",
            "vertical",
            "value",
            "min",
            "max",
            "step",
            "disable",
            "readonly",
            "color",
            "label-color",
            "dark",
            "dense",
        ]
        self.allowed_events = ["input", "change"]
        # self.set_keyword_events(**kwargs)

    def convert_object_to_dict(self):
        d = super().convert_object_to_dict()
        if self.label_suffix:
            d["attrs"]["label-value"] = str(self.value) + self.label_suffix
        return d


@parse_dict
class QRange(_QInputBase):
    # TODO: Deal with left-label-value  and right-label-value props, for now use suffix for both right and left

    slots = []
    html_tag = "q-range"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "object"
        self.value = kwargs.get("value", {"min": 0, "max": 100})
        # The label suffix is a stop gap till full label-value prop implemented
        self.label_suffix = kwargs.get("label_suffix", "")
        self.prop_list = [
            "drag-range",
            "drag-range-only",
            "left-label-color",
            "right-label-color",
            "left-label-value",
            "right-label-value",
            "label-always",
            "snap",
            "label",
            "label-always",
            "markers",
            "tabindex",
            "value",
            "min",
            "max",
            "step",
            "disable",
            "readonly",
            "color",
            "dark",
            "dense",
        ]
        self.allowed_events = ["input", "change"]

        # self.set_keyword_events(**kwargs)

    def convert_object_to_dict(self):
        d = super().convert_object_to_dict()
        if self.label_suffix:
            d["attrs"]["label-value"] = str(self.value) + self.label_suffix
        return d


@parse_dict
class QRating(_QInputBase):
    slots = []
    html_tag = "q-rating"

    def __init__(self, **kwargs):
        self.no_reset = False
        super().__init__(**kwargs)
        self.debounce = 30
        self.prop_list = [
            "icon",
            "max",
            "value",
            "no-reset",
            "readonly",
            "disable",
            "color",
            "size",
            "icon-selected",
            "icon-half",
            "no-dimming",
            "color-selected",
            "color-half",
        ]
        self.allowed_events = ["input"]
        # self.set_keyword_events(**kwargs)

    def before_event_handler(self, msg):
        if msg.event_type not in ["input"]:
            return

        if hasattr(self, "model"):
            self.model[0].data[self.model[1]] = msg.value

        if not self.no_reset and (self.value == msg.value):
            self.value = 0
        else:
            self.value = msg.value


@parse_dict
class QTime(_QInputBase):
    slots = []
    html_tag = "q-time"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Options prop not supported and left out from list. It is a function
        self.prop_list = [
            "landscape",
            "format24h",
            "options",
            "hour-options",
            "minute-options",
            "second-options",
            "with-seconds",
            "now-btn",
            "value",
            "mask",
            "locale",
            "calendar",
            "readonly",
            "disable",
            "color",
            "text-color",
            "dark",
            "square",
            "flat",
            "bordered",
        ]
        self.allowed_events = ["input"]
        # self.set_keyword_events(**kwargs)


@parse_dict
class QDate(_QInputBase):
    slots = []
    html_tag = "q-date"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Options prop not supported and left out from list. It is a function
        self.prop_list = [
            "landscape",
            "title",
            "subtitle",
            "today-btn",
            "minimal",
            "readonly",
            "disable",
            "color",
            "text-color",
            "dark",
            "event-color",
            "value",
            "mask",
            "locale",
            "calendar",
            "emit-immediately",
            "default-year-month",
            "default-view",
            "events-date",
            "options-date",
            "first-day-of-week",
            "square",
            "flat",
            "bordered",
        ]
        self.allowed_events = ["input"]
        self.evaluate_prop = []
        # self.set_keyword_events(**kwargs)

    def convert_object_to_dict(self):
        d = super().convert_object_to_dict()
        try:
            d["attrs"]["events"] = self.events_date
        except:
            pass
        try:
            d["attrs"]["options"] = self.options_date
        except:
            pass
        return d


@parse_dict
class QCheckbox(_QInputBase):
    slots = ["default_slot"]
    html_tag = "q-checkbox"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "object"
        self.value = kwargs.get("value", False)
        self.prop_list = [
            "keep-color",
            "indeterminate-value",
            "toggle-indeterminate",
            "tabindex",
            "label",
            "left-label",
            "name",
            "toggle-order",
            "value",
            "val",
            "true-value",
            "false-value",
            "disable",
            "color",
            "dark",
            "dense",
            "size",
        ]
        self.allowed_events = ["input"]
        # self.set_keyword_events(**kwargs)

    def convert_object_to_dict(self):
        d = super().convert_object_to_dict()
        return d


@parse_dict
class QToggle(_QInputBase):
    slots = ["default_slot"]
    html_tag = "q-toggle"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.debounce = 50
        self.type = "object"
        self.value = kwargs.get("value", False)
        self.prop_list = [
            "keep-color",
            "icon",
            "checked-icon",
            "unchecked-icon",
            "tabindex",
            "label",
            "left-label",
            "value",
            "val",
            "true-value",
            "false-value",
            "disable",
            "color",
            "dark",
            "dense",
            "size",
        ]
        self.allowed_events = ["input"]
        # self.set_keyword_events(**kwargs)

    def convert_object_to_dict(self):
        d = super().convert_object_to_dict()
        return d


@parse_dict
class QForm(QDiv):
    slots = ["default_slot"]
    html_tag = "q-form"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = ["autofocus", "no-error-focus", "no-reset-focus", "greedy"]
        self.allowed_events = ["submit", "before"]

        def default_submit(self, msg):
            print("Default form submit", msg.form_data)
            return True

        if not self.has_event_function("submit"):
            # If an event handler is not  assigned, the front end cannot stop the default page request that happens when a form is submitted
            self.on("submit", default_submit)


@parse_dict
class QAvatar(QDiv):
    slots = ["default_slot"]
    html_tag = "q-avatar"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = [
            "icon",
            "size",
            "font-size",
            "color",
            "text-color",
            "square",
            "rounded",
        ]


@parse_dict
class QAjaxBar(QDiv):
    slots = []
    html_tag = "q-ajax-bar"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = ["skip-hijack", "reverse", "position", "size", "color"]
        self.allowed_events = ["start", "stop"]
        self.set_keyword_events(**kwargs)


@parse_dict
class QBadge(QDiv):
    slots = ["default_slot"]
    html_tag = "q-badge"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = [
            "color",
            "text-color",
            "floating",
            "transparent",
            "multi-line",
            "label",
            "align",
            "outline",
        ]


@parse_dict
class QBanner(QDiv):
    slots = ["default_slot", "avatar_slot", "action_slot"]
    html_tag = "q-banner"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = ["inline-actions", "dense", "rounded"]


@parse_dict
class QBar(QDiv):
    slots = ["default_slot"]
    html_tag = "q-bar"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = ["dense", "dark"]


@parse_dict
class QToolbar(QDiv):
    slots = ["default_slot"]
    html_tag = "q-toolbar"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = ["inset"]


@parse_dict
class QToolbarTitle(QDiv):
    slots = ["default_slot"]
    html_tag = "q-toolbar-title"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = ["shrink"]


@parse_dict
class QBreadcrumbs(QDiv):
    # DOES NOT WORK
    html_tag = "q-breadcrumbs"

    def __init__(self, **kwargs):
        self.separator = "/"
        super().__init__(**kwargs)
        self.prop_list = [
            "separator",
            "active-color",
            "gutter",
            "separator-color",
            "align",
        ]
        self.separator = "h"
        self.separator_color = "primary"


@parse_dict
class QBreadcrumbsEl(QDiv):
    slots = []
    html_tag = "q-breadcrumbs-el"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = [
            "to",
            "exact",
            "append",
            "replace",
            "active-class",
            "exact-active-class",
            "label",
            "icon",
        ]


@parse_dict
class QBtn(QDiv):
    slots = ["default_slot", "loading_slot"]
    html_tag = "q-btn"

    def __init__(self, **kwargs):
        self.loading = False
        super().__init__(**kwargs)
        self.prop_list = [
            "ripple",
            "type",
            "to",
            "replace",
            "label",
            "icon",
            "icon-right",
            "round",
            "outline",
            "flat",
            "unelevated",
            "rounded",
            "push",
            "glossy",
            "size",
            "fab",
            "fab-mini",
            "color",
            "text-color",
            "no-caps",
            "no-wrap",
            "dense",
            "tabindex",
            "align",
            "stack",
            "stretch",
            "loading",
            "disable",
            "percentage",
            "dark-percentage",
            "href",
            "target",
            "download",
        ]


QButton = QBtn


@parse_dict
class QBtnGroup(QDiv):
    slots = ["default_slot"]
    html_tag = "q-btn-group"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = [
            "spread",
            "stretch",
            "outline",
            "flat",
            "unelevated",
            "rounded",
            "push",
            "glossy",
        ]


@parse_dict
class QBtnDropdown(_QInputBase):
    slots = ["default_slot", "label_slot"]
    html_tag = "q-btn-dropdown"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "boolean"
        self.value = bool(self.value)
        self.prop_list = [
            "loading",
            "split",
            "disable-main-btn",
            "disable-dropdown",
            "persistent",
            "auto-close",
            "label",
            "icon",
            "icon-right",
            "no-caps",
            "no-wrap",
            "align",
            "stack",
            "stretch",
            "dropdown-icon",
            "type",
            "tabindex",
            "value",
            "cover",
            "menu-anchor",
            "menu-self",
            "to",
            "replace",
            "disable",
            "ripple",
            "round",
            "outline",
            "flat",
            "unelevated",
            "rounded",
            "push",
            "size",
            "fab",
            "fab-mini",
            "color",
            "text-color",
            "dense",
            "content-style",
            "content-class",
        ]
        self.allowed_events = [
            "input",
            "show",
            "before_show",
            "hide",
            "before_hide",
            "click",
        ]
        self.set_keyword_events(**kwargs)


@parse_dict
class QMenu(_QInputBase):
    slots = ["default_slot"]
    html_tag = "q-menu"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "boolean"
        self.value = bool(self.value)
        self.prop_list = [
            "target",
            "context-menu",
            "fit",
            "no-parent-event",
            "touch-position",
            "persistent",
            "auto-close",
            "no-focus",
            "transition-show",
            "transition-hide",
            "value",
            "cover",
            "anchor",
            "self",
            "offset",
            "content-class",
            "content-style",
            "square",
            "max-height",
            "max-width",
        ]
        self.allowed_events = [
            "input",
            "show",
            "before_show",
            "hide",
            "before_hide",
            "escape_key",
        ]
        self.set_keyword_events(**kwargs)


@parse_dict
class QCard(QDiv):
    slots = ["default_slot"]
    html_tag = "q-card"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = ["dark", "square", "flat", "bordered"]


@parse_dict
class QCardSection(QDiv):
    slots = ["default_slot"]
    html_tag = "q-card-section"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = ["horizontal"]


@parse_dict
class QCardActions(QDiv):
    slots = ["default_slot"]
    html_tag = "q-card-actions"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = ["align", "vertical"]


@parse_dict
class QTabs(_QInputBase):
    slots = ["default_slot"]
    html_tag = "q-tabs"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = kwargs.get("value", "")
        self.prop_list = [
            "breakpoint",
            "vertical",
            "align",
            "left-icon",
            "right-icon",
            "shrink",
            "switch-indicator",
            "narrow-indicator",
            "inline-label",
            "no-caps",
            "value",
            "active-color",
            "active-bg-color",
            "indicator-color",
            "dense",
        ]
        self.allowed_events = ["input"]
        # self.set_keyword_events(**kwargs)


@parse_dict
class QTab(QDiv):
    slots = ["default_slot"]
    html_tag = "q-tab"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = [
            "icon",
            "label",
            "alert",
            "no-caps",
            "name",
            "tabindex",
            "disable",
            "ripple",
        ]


@parse_dict
class QTabPanels(_QInputBase):
    # Does not work
    slots = ["default_slot"]
    html_tag = "q-tab-panels"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = kwargs.get("value", "")
        self.prop_list = [
            "keep-alive",
            "animated",
            "infinite",
            "swipeable",
            "transition-prev",
            "transition-next",
            "value",
        ]
        self.allowed_events = ["input"]
        # self.set_keyword_events(**kwargs)


@parse_dict
class QTabPanel(QDiv):
    slots = ["default_slot"]
    html_tag = "q-tab-panel"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = ["name", "disable"]


@parse_dict
class QSplitter(_QInputBase):
    slots = ["before_slot", "after_slot", "separator_slot"]
    html_tag = "q-splitter"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = kwargs.get("value", 50.0)
        self.limits = kwargs.get("limits", [0, 100])
        self.type = "float"
        self.prop_list = [
            "horizontal",
            "limits",
            "value",
            "disable",
            "before-class",
            "after-class",
            "separator-class",
            "separator-style",
            "dark",
        ]
        self.allowed_events = ["input"]
        # self.set_keyword_events(**kwargs)


@parse_dict
class QKnob(_QInputBase):
    slots = ["default_slot"]
    html_tag = "q-knob"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = kwargs.get("value", 0)
        self.type = "float"
        self.prop_list = [
            "show-value",
            "angle",
            "tabindex",
            "value",
            "min",
            "max",
            "step",
            "disable",
            "readonly",
            "color",
            "center-color",
            "track-color",
            "size",
            "font-size",
            "thickness",
        ]
        self.allowed_events = ["input", "change", "drag_value"]
        self.set_keyword_events(**kwargs)


@parse_dict
class QPagination(_QInputBase):
    slots = []
    html_tag = "q-pagination"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = kwargs.get("value", 1)
        self.type = "float"
        self.prop_list = [
            "input",
            "boundary-links",
            "direction-links",
            "boundary-numbers",
            "ellipses",
            "value",
            "min",
            "max",
            "max-pages",
            "disable",
            "color",
            "text-color",
            "input-style",
            "input-class",
            "size",
            "icon-prev",
            "icon-next",
            "icon-first",
            "icon-last",
            "ripple",
        ]
        self.allowed_events = ["input"]
        # self.set_keyword_events(**kwargs)


@parse_dict
class QChatMessage(QDiv):
    slots = ["default_slot", "avatar_slot"]
    html_tag = "q-chat-message"

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.prop_list = [
            "label-sanitize",
            "name-sanitize",
            "text-sanitize",
            "stamp-sanitize",
            "sent",
            "label",
            "name",
            "avatar",
            "text",
            "stamp",
            "bg-color",
            "text-color",
            "size",
        ]

    def convert_object_to_dict(self):

        d = super().convert_object_to_dict()
        try:
            d.pop("text")
        except:
            pass
        return d


@parse_dict
class QChip(QDiv):
    slots = ["default_slot"]
    html_tag = "q-chip"

    def __init__(self, **kwargs):
        self.selected = None
        super().__init__(**kwargs)
        self.prop_list = [
            "icon",
            "icon-right",
            "label",
            "tabindex",
            "value",
            "selected",
            "clickable",
            "removable",
            "disable",
            "ripple",
            "dense",
            "color",
            "text-color",
            "square",
            "outline",
        ]
        self.allowed_events = ["update:selected", "click", "remove"]
        self.set_keyword_events(**kwargs)

        def chip_remove(self, message):
            self.show = False
            self.value = False

        self.on("remove", chip_remove)

    @staticmethod
    def chip_select(self, message):
        self.selected = not self.selected

    def convert_object_to_dict(self):

        d = super().convert_object_to_dict()
        if self.selected is not None:
            self.on("update:selected", self.chip_select)
        else:
            self.remove_event("update:selected")
        return d


@parse_dict
class QCircularProgress(QDiv):
    slots = ["default_slot"]
    html_tag = "q-circular-progress"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = [
            "indeterminate",
            "show-value",
            "reverse",
            "angle",
            "value",
            "min",
            "max",
            "color",
            "center-color",
            "track-color",
            "size",
            "font-size",
            "thickness",
        ]


@parse_dict
class QLinearProgress(QDiv):
    slots = ["default_slot"]
    html_tag = "q-linear-progress"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = [
            "buffer",
            "reverse",
            "indeterminate",
            "query",
            "stripe",
            "value",
            "color",
            "track-color",
            "dark",
            "rounded",
        ]


@parse_dict
class QColor(_QInputBase):
    slots = []
    html_tag = "q-color"

    def __init__(self, **kwargs):
        self.value = ""
        self.format_model = "hex"
        super().__init__(**kwargs)
        self.prop_list = [
            "default-view",
            "no-header",
            "no-footer",
            "value",
            "default-value",
            "format-model",
            "disable",
            "readonly",
            "dark",
        ]
        self.allowed_events = ["input", "change"]
        # self.set_keyword_events(**kwargs)


@parse_dict
class QPopupProxy(_QInputBase):
    html_tag = "q-popup-proxy"
    slots = ["default_slot"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = kwargs.get("value", False)
        # self.prop_list = ['target', 'context-menu', 'breakpoint', 'value']
        # self.qdialog_prop_list = ['persistent', 'no-esc-dsimiss', 'no-backdrop-dismiss', 'no-route-dismiss',
        #                           'auto-close',
        #                           'transition-show', 'transition-hide', 'no-refocus', 'no-focus', 'seamless',
        #                           'maximized',
        #                           'full-width', 'full-height', 'position', 'value', 'content-class', 'content-style',
        #                           'square']
        # self.qmenu_prop_list = ['target', 'context-menu', 'fit', 'no-parent-event', 'touch-position', 'persistent',
        #                         'auto-close', 'no-focus', 'transition-show', 'transition-hide', 'value', 'cover',
        #                         'anchor', 'self',
        #                         'offset', 'content-class', 'content-style', 'square', 'max-height', 'max-width']
        # Union of all three. QDialog and QMenu props are passed through
        self.prop_list = [
            "touch-position",
            "context-menu",
            "max-width",
            "no-route-dismiss",
            "content-style",
            "full-width",
            "max-height",
            "no-esc-dsimiss",
            "cover",
            "no-parent-event",
            "square",
            "no-backdrop-dismiss",
            "value",
            "transition-hide",
            "breakpoint",
            "content-class",
            "seamless",
            "transition-show",
            "fit",
            "no-focus",
            "auto-close",
            "position",
            "full-height",
            "self",
            "maximized",
            "offset",
            "anchor",
            "no-refocus",
            "target",
            "persistent",
        ]
        self.allowed_events = [
            "input",
            "show",
            "before_show",
            "hide",
            "before_hide",
            "escape_key",
        ]
        self.set_keyword_events(**kwargs)


@parse_dict
class QDialog(_QInputBase):
    slots = []
    html_tag = "q-dialog"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.type = "boolean"
        self.value = bool(self.value)
        self.prop_list = [
            "persistent",
            "no-esc-dsimiss",
            "no-backdrop-dismiss",
            "no-route-dismiss",
            "auto-close",
            "transition-show",
            "transition-hide",
            "no-refocus",
            "no-focus",
            "seamless",
            "maximized",
            "full-width",
            "full-height",
            "position",
            "value",
            "content-class",
            "content-style",
            "square",
        ]
        self.allowed_events = [
            "input",
            "show",
            "before_show",
            "hide",
            "before_hide",
            "escape_key",
        ]
        self.set_keyword_events(**kwargs)


@parse_dict
class QTooltip(_QInputBase):
    slots = ["default_slot"]
    html_tag = "q-tooltip"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.disable_events = True  # For tooltips, events are disabled by default otherwise input event occurs every time tooltip shows.
        self.type = "boolean"
        self.value = bool(self.value)
        self.prop_list = [
            "transition-show",
            "transition-hide",
            "target",
            "delay",
            "max-height",
            "max-width",
            "value",
            "anchor",
            "self",
            "offset",
            "content-class",
            "content-style",
            "hide-delay",
        ]
        self.allowed_events = [
            "input",
            "show",
            "before_show",
            "hide",
            "before_hide",
            "before",
        ]
        self.set_keyword_events(**kwargs)


@parse_dict
class QStepper(_QInputBase):
    # Not working
    html_tag = "q-stepper"

    slots = ["default_slot", "navigation_slot", "message_slot"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = [
            "keep-alive",
            "animated",
            "infinite",
            "swipeable",
            "transition-prev",
            "transition-next",
            "vertical",
            "header-nav",
            "value",
            "dark",
            "flat",
            "bordered",
            "alternative-labels",
            "contracted",
            "inactive-icon",
            "inactive-color",
            "done-icon",
            "done-color",
            "active-icon",
            "active-color",
            "error-icon",
            "error-color",
        ]
        self.allowed_events = ["input", "before-transition", "transition"]
        self.set_keyword_events(**kwargs)


@parse_dict
class QStep(QDiv):
    slots = ["default_slot"]
    html_tag = "q-step"

    def __init__(self, **kwargs):
        self.done = False
        super().__init__(**kwargs)
        self.prop_list = [
            "header-nav",
            "name",
            "disable",
            "done",
            "error",
            "color",
            "icon",
            "title",
            "caption",
            "prefix",
            "done-icon",
            "done-color",
            "active-icon",
            "active-color",
            "error-icon",
            "error-color",
        ]


@parse_dict
class QStepperNavigation(QDiv):
    slots = ["default_slot"]
    html_tag = "q-stepper-navigation"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = []


@parse_dict
class QSlideTransition(QDiv):
    slots = ["default_slot"]
    html_tag = "q-slide-transition"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = ["appear", "duration"]


@parse_dict
class QTimeline(QDiv):
    slots = ["default_slot"]
    html_tag = "q-timeline"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = ["side", "layout", "color", "dark"]


@parse_dict
class QTimelineEntry(QDiv):
    slots = ["default_slot", "title_slot", "subtitle_slot"]
    html_tag = "q-timeline-entry"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = [
            "color",
            "heading",
            "tag",
            "icon",
            "avatar",
            "title",
            "subtitle",
            "body",
            "side",
        ]


@parse_dict
class QEditor(QInput):
    slots = []
    html_tag = "q-editor"

    icon_set = Dict(
        {
            "align": "format_align_left",
            "bold": "format_bold",
            "center": "format_align_center",
            "code": "code",
            "font": "font_download",
            "fontSize": "format_size",
            "formatting": "text_format",
            "header": "format_size",
            "hr": "remove",
            "hyperlink": "link",
            "indent": "format_indent_increase",
            "italic": "format_italic",
            "justify": "format_align_justify",
            "left": "format_align_left",
            "orderedList": "format_list_numbered",
            "outdent": "format_indent_decrease",
            "print": "print",
            "quote": "format_quote",
            "redo": "redo",
            "removeFormat": "format_clear",
            "right": "format_align_right",
            "size": "format_size",
            "strikethrough": "strikethrough_s",
            "subscript": "vertical_align_bottom",
            "superscript": "vertical_align_top",
            "toggleFullscreen": "fullscreen",
            "underline": "format_underlined",
            "undo": "undo",
            "unorderedList": "format_list_bulleted",
        }
    )

    lang = Dict(
        {
            "url": "URL",
            "bold": "Bold",
            "italic": "Italic",
            "strikethrough": "Strikethrough",
            "underline": "Underline",
            "unorderedList": "Unordered List",
            "orderedList": "Ordered List",
            "subscript": "Subscript",
            "superscript": "Superscript",
            "hyperlink": "Hyperlink",
            "toggleFullscreen": "Toggle Fullscreen",
            "quote": "Quote",
            "left": "Left align",
            "center": "Center align",
            "right": "Right align",
            "justify": "Justify align",
            "print": "Print",
            "outdent": "Decrease indentation",
            "indent": "Increase indentation",
            "removeFormat": "Remove formatting",
            "formatting": "Formatting",
            "fontSize": "Font Size",
            "align": "Align",
            "hr": "Insert Horizontal Rule",
            "undo": "Undo",
            "redo": "Redo",
            "header1": "Header 1",
            "header2": "Header 2",
            "header3": "Header 3",
            "header4": "Header 4",
            "header5": "Header 5",
            "header6": "Header 6",
            "paragraph": "Paragraph",
            "code": "Code",
            "size1": "Very small",
            "size2": "A bit small",
            "size3": "Normal",
            "size4": "Medium-large",
            "size5": "Big",
            "size6": "Very big",
            "size7": "Maximum",
            "defaultFont": "Default Font",
        }
    )

    simple_options = [
        ["left", "center", "right", "justify"],
        ["bold", "italic", "strike", "underline", "subscript", "superscript"],
        ["hr", "link"],
        ["undo", "redo"],
        ["print", "fullscreen"],
    ]

    fonts = {
        "arial": "Arial",
        "arial_black": "Arial Black",
        "comic_sans": "Comic Sans MS",
        "courier_new": "Courier New",
        "impact": "Impact",
        "lucida_grande": "Lucida Grande",
        "times_new_roman": "Times New Roman",
        "verdana": "Verdana",
    }

    kitchen_sink = [
        [
            {
                "label": lang.align,
                "icon": icon_set.align,
                "fixedLabel": True,
                "list": "only-icons",
                "options": ["left", "center", "right", "justify"],
            },
            {
                "label": lang.align,
                "icon": icon_set.align,
                "fixedLabel": True,
                "options": ["left", "center", "right", "justify"],
            },
        ],
        ["bold", "italic", "strike", "underline", "subscript", "superscript"],
        ["token", "hr", "link", "custom_btn"],
        ["print", "fullscreen"],
        [
            {
                "label": lang.formatting,
                "icon": icon_set.formatting,
                "list": "no-icons",
                "options": ["p", "h1", "h2", "h3", "h4", "h5", "h6", "code"],
            },
            {
                "label": lang.fontSize,
                "icon": icon_set.fontSize,
                "fixedLabel": True,
                "fixedIcon": True,
                "list": "no-icons",
                "options": [
                    "size-1",
                    "size-2",
                    "size-3",
                    "size-4",
                    "size-5",
                    "size-6",
                    "size-7",
                ],
            },
            {
                "label": lang.defaultFont,
                "icon": icon_set.font,
                "fixedIcon": True,
                "list": "no-icons",
                "options": [
                    "default_font",
                    "arial",
                    "arial_black",
                    "comic_sans",
                    "courier_new",
                    "impact",
                    "lucida_grande",
                    "times_new_roman",
                    "verdana",
                ],
            },
            "removeFormat",
        ],
        ["quote", "unordered", "ordered"],
        ["undo", "redo"],
    ]

    def __init__(self, **kwargs):
        self.kitchen_sink = False
        self.toolbar = QEditor.simple_options
        super().__init__(**kwargs)
        self.prop_list = [
            "fullscreen",
            "value",
            "readonly",
            "disable",
            "square",
            "flat",
            "dense",
            "min-height",
            "max-height",
            "height",
            "toolbar-outline",
            "toolbar-push",
            "toolbar-rounded",
            "content-style",
            "content-class",
            "definitions",
            "fonts",
            "toolbar",
            "toolbar-color",
            "toolbar-text-color",
            "toolbar-toggle-color",
            "toolbar-bg",
            "toolbar-outline",
            "toolbar-push",
            "toolbar-rounded",
        ]
        self.allowed_events = ["input"]
        # self.set_keyword_events(**kwargs)

    def convert_object_to_dict(self):
        self.debounce = 0  # Component has its own debounce mechanism
        if self.kitchen_sink:
            self.toolbar = QEditor.kitchen_sink
            self.fonts = QEditor.fonts
        d = super().convert_object_to_dict()
        return d


@parse_dict
class QExpansionItem(_QInputBase):
    slots = ["default_slot", "header_slot"]
    html_tag = "q-expansion-item"

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.type = "boolean"
        self.value = bool(self.value)
        self.prop_list = [
            "to",
            "exact",
            "append",
            "replace",
            "active-class",
            "exact-active-class",
            "duration",
            # 'default-opened',  Do not use, just set value to True: self.value = True
            "expand-icon-toggle",
            "group",
            "popup",
            "icon",
            "expand-icon",
            "label",
            "label-lines",
            "caption",
            "caption-lines",
            "header-inset-level",
            "content-inset-level",
            "expand-separator",
            "switch-toggle-side",
            "value",
            "disable",
            "expand-icon-class",
            "dark",
            "dense",
            "dense-toggle",
            "header-style",
            "header-class",
        ]
        self.allowed_events = [
            "input",
            "show",
            "before_show",
            "hide",
            "before_hide",
            "escape_key",
        ]
        self.set_keyword_events(**kwargs)

    def convert_object_to_dict(self):
        d = super().convert_object_to_dict()
        try:
            if d["attrs"]["default-opened"]:
                d["value"] = True
                d["attrs"]["value"] = True
        except:
            pass
        return d


@parse_dict
class QImg(QDiv):
    slots = ["defualt_slot", "loading_slot", "error_slot"]
    html_tag = "q-img"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = [
            "transition",
            "alt",
            "basic",
            "contain",
            "position",
            "ratio",
            "src",
            "srcset",
            "sizes",
            "placeholder-src",
            "spinner-color",
            "spinner-size",
        ]
        # Events: load, error


@parse_dict
class QInnerLoading(QDiv):
    slots = ["default_slot"]
    html_tag = "q-inner-loading"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = [
            "transition-show",
            "transition-hide",
            "showing",
            "color",
            "size",
            "dark",
        ]


@parse_dict
class QParallax(QDiv):
    slots = ["default_slot", "media_slot", "content_slot"]
    html_tag = "q-parallax"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = ["speed", "src", "height"]


@parse_dict
class Transition(QDiv):
    html_tag = "transition"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = [
            "appear",
            "appear-class",
            "appear-to-class",
            "appear-active-class",
            "enter-class",
            "enter-active-class",
            "enter-to-class",
            "leave-class",
            "leave-active-class",
            "leave-to-class",
            "duration",
            "mode",
        ]


@parse_dict
class TransitionGroup(QDiv):
    html_tag = "transition-group"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = [
            "appear",
            "appear-class",
            "appear-to-class",
            "appear-active-class",
            "enter-class",
            "enter-active-class",
            "enter-to-class",
            "leave-class",
            "leave-active-class",
            "leave-to-class",
            "duration",
            "mode",
            "tag",
            "key",
        ]


@parse_dict
class QIcon(QDiv):
    slots = ["default_slot"]
    html_tag = "q-icon"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = ["name", "color", "size", "left", "right", "tag"]


@parse_dict
class QSpinner(QDiv):
    # TODO: Take care of all spinner types in parser

    spinner_types = [
        "audio",
        "ball",
        "bars",
        "comment",
        "cube",
        "dots",
        "facebook",
        "gears",
        "grid",
        "hearts",
        "hourglass",
        "infinity",
        "ios",
        "oval",
        "pie",
        "puff",
        "radio",
        "rings",
        "tail",
    ]
    html_tag = "q-spinner"

    def __init__(self, **kwargs):

        self.size = "1em"
        self.color = "primary"
        self.spinner_type = ""
        super().__init__(**kwargs)
        self.prop_list = ["size", "color", "thickness"]

    def convert_object_to_dict(self):
        if self.spinner_type in QSpinner.spinner_types:
            self.html_tag = "q-spinner-" + self.spinner_type
        else:
            self.html_tag = "q-spinner"
        d = super().convert_object_to_dict()
        return d


@parse_dict
class QList(QDiv):
    slots = ["default_slot"]
    html_tag = "q-list"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = ["separator", "padding", "bordered", "dense", "dark"]


@parse_dict
class QItem(QDiv):
    slots = ["default_slot"]
    html_tag = "q-item"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = [
            "to",
            "exact",
            "append",
            "replace",
            "active-class",
            "exact-active-class",
            "inset-level",
            "tag",
            "tabindex",
            "disable",
            "active",
            "clickable",
            "manual-focus",
            "focused",
            "dark",
            "dense",
        ]


@parse_dict
class QItemSection(QDiv):
    slots = ["default_slot"]
    html_tag = "q-item-section"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = ["avatar", "thumbnail", "side", "top", "no-wrap"]


@parse_dict
class QItemLabel(QDiv):
    slots = ["default_slot"]
    html_tag = "q-item-label"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = ["lines", "overline", "caption", "header"]


@parse_dict
class QSlideItem(QDiv):
    slots = ["default_slot", "left_slot", "right_slot"]
    html_tag = "q-slide-item"

    def __init__(self, **kwargs):
        self.reset = False
        super().__init__(**kwargs)
        self.prop_list = ["left-color", "right-color"]
        self.allowed_events = ["left", "right", "action", "bottom", "top"]
        self.set_keyword_events(**kwargs)

    def convert_object_to_dict(self):
        d = super().convert_object_to_dict()
        d["reset"] = self.reset
        return d


@parse_dict
class QInfiniteScroll(QDiv):
    # https://quasar.dev/vue-components/infinite-scroll

    # To work MUST add 'scroll' to classes of container that holds this component. Otherwise endless load events generated
    # Also styling must be through style not color or size props because they disappear after first event

    slots = ["default_slot", "loading_slot"]
    html_tag = "q-infinite-scroll"

    def __init__(self, **kwargs):
        self.done = False
        self.initial = True
        super().__init__(**kwargs)
        self.prop_list = ["offset", "scrollTarget", "reverse", "disable"]
        self.allowed_events = ["load"]
        self.set_keyword_events(**kwargs)

    def convert_object_to_dict(self):
        d = super().convert_object_to_dict()
        d["done"] = self.done
        return d


@parse_dict
class QScrollArea(QDiv):
    slots = ["default_slot"]
    html_tag = "q-scroll-area"

    def __init__(self, **kwargs):
        self.offset = None
        self.duration = None
        super().__init__(**kwargs)
        # Offset and duration are added props to activate the setScrollPosition function
        self.prop_list = [
            "delay",
            "horizontal",
            "thumb-style",
            "content-style",
            "content-active-style",
            "offset",
            "duration",
        ]

    def convert_object_to_dict(self):
        d = super().convert_object_to_dict()
        d["offset"] = self.offset
        d["duration"] = self.duration
        return d


@parse_dict
class QScrollObserver(QDiv):
    html_tag = "q-scroll-observer"

    def __init__(self, **kwargs):
        self.debounce = 300
        super().__init__(**kwargs)
        self.prop_list = ["debounce", "horizontal"]
        self.allowed_events = ["scroll"]
        self.set_keyword_events(**kwargs)


@parse_dict
class QMarkupTable(QDiv):
    slots = ["default_slot"]
    html_tag = "q-markup-table"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = [
            "separator",
            "wrap-cells",
            "dense",
            "dark",
            "flat",
            "bordered",
            "square",
        ]


@parse_dict
class QSeparator(QDiv):
    html_tag = "q-separator"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = ["spaced", "inset", "vertical", "dark", "color"]


@parse_dict
class QSpace(QDiv):
    html_tag = "q-space"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = []


@parse_dict
class QVideo(QDiv):
    html_tag = "q-video"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = ["src", "ratio"]


@parse_dict
class QTree(QDiv):
    slots = []
    html_tag = "q-tree"

    def __init__(self, **kwargs):

        self.ticked = []
        self.expanded = []
        self.selected = []
        self.tick_strategy = "none"  # none | strict | leaf | leaf-filtered
        self.default_expand_all = False
        super().__init__(**kwargs)
        self.attributes = [
            "tick-strategy",
            "default-expand-all",
            "accordion",
            "nodes",
            "node-key",
            "label-key",
            "icon",
            "no-nodes-label",
            "no-results-label",
            "filter",
            "filter-method",
            "ticked",
            "expanded",
            "selected",
            "color",
            "control-color",
            "text-color",
            "selected-color",
            "dark",
            "duration",
            "no-connectors",
        ]
        self.allowed_events = [
            "before",
            "after",
            "update:expanded",
            "lazy-load",
            "update:ticked",
            "update:selected",
        ]
        self.set_keyword_events(**kwargs)
        self.events = ["update:expanded", "update:ticked", "update:selected"]

        def default_input(self, msg):
            return self.before_event_handler(msg)

        self.on("before", default_input)

    def before_event_handler(self, msg):
        if msg.event_type == "update:expanded":
            self.expanded = msg.value
        elif msg.event_type == "update:selected":
            self.selected = msg.value
        elif msg.event_type == "update:ticked":
            self.ticked = msg.value

    def model_update(self):
        pass

    def __setattr__(self, key, value):
        if key == "nodes":
            if isinstance(value, str):
                self.load_json(value)
            else:
                self.__dict__[key] = value
        elif key in self.slots:
            self.add_scoped_slot(key[: key.index("_")], value)
        else:
            self.__dict__[key] = value

    def load_json(self, options_string):
        self.nodes = hjson.loads(options_string.encode("ascii", "ignore"))
        return self.nodes

    def load_json_from_file(self, file_name):
        with open(file_name, "r") as f:
            self.nodes = hjson.loads(f.read().encode("ascii", "ignore"))
        return self.nodes

    def convert_object_to_dict(self):
        d = super().convert_object_to_dict()
        d["default_expand_all"] = self.default_expand_all
        return d


@parse_dict
class QNotify(QDiv):
    # TODO: Add handler for action that sends message back to server. Currently does not support actions

    html_tag = "q-notify"

    # This is a special component that does not wrap a quasar component but activates a quasar utility
    # https://quasar.dev/quasar-plugins/notify
    # Add 'after' event to button that activates that sets 'notify' prop back to false. Otherwise, will appear every update
    # Or, await page update in event and then set notify to false

    def __init__(self, **kwargs):
        self.notify = False
        # Possible position: top-left | top-right | bottom-left | bottom-right | top | bottom | left | right | center
        self.position = "bottom-right"
        super().__init__(**kwargs)
        self.prop_list = [
            "notify",
            "color",
            "textColor",
            "message",
            "html",
            "icon",
            "avatar",
            "position",
            "closeBtn",
            "timeout",
            "actions",
            "multiLine",
            "caption",
            "reply",
        ]

    def convert_object_to_dict(self):
        d = super().convert_object_to_dict()
        d["notify"] = self.notify
        return d


@parse_dict
class QTable(QDiv):
    # Has also specific slots for column names body-cell-{name}
    slots = [
        "item_slot",
        "body_slot",
        "body-cell_slot",
        "top-row_slot",
        "bottom-row_slot",
        "bottom_slot",
        "pagination_slot",
        "header_slot",
        "header-cell_slot",
        "top-left_slot",
        "top-right_slot",
        "top-selection_slot",
        "top_slot",
        "bottom_slot",
        "loading_slot",
    ]
    html_tag = "q-table"

    def __init__(self, **kwargs):

        self.pagination = False
        self.selected = []
        super().__init__(**kwargs)
        self.attributes = [
            "fullscreen",
            "loading",
            "columns",
            "visible-columns",
            "title",
            "hide-header",
            "hide-bottom",
            "separator",
            "wrap-cells",
            "no-data-label",
            "no-results-label",
            "loading-label",
            "filter",
            "filter-method",
            "data",
            "row-key",
            "rows-per-page-label",
            "pagination-label",
            "pagination",
            "rows-per-page-options",
            "selected-rows-label",
            "selection",
            "selected",
            "binary-state-sort",
            "sort-method",
            "color",
            "grid",
            "dense",
            "dark",
            "flat",
            "bordered",
            "square",
            "table-style",
            "table-class",
            "table-header-style",
            "table-header-class",
            "card-style",
            "card-class",
            "icon-first-page",
            "con-prev-page",
            "icon-next-page",
            "icon-last-page",
        ]
        # Need to load: columns, data
        # separator one of  horizontal | vertical | cell | none
        self.allowed_events = [
            "before",
            "after",
            "request",
            "selection",
            "update:pagination",
            "update:selected",
        ]
        self.set_keyword_events(**kwargs)
        self.events = ["update:pagination", "update:selected"]

        def default_input(self, msg):
            return self.before_event_handler(msg)

        self.on("before", default_input)

    def before_event_handler(self, msg):
        if msg.event_type == "update:selected":
            self.selected = msg.value
        elif msg.event_type == "update:pagination":
            self.pagination = msg.value

    def model_update(self):
        pass

    def __setattr__(self, key, value):
        if key in ["data", "columns"]:
            if isinstance(value, str):
                self.__dict__[key] = self.load_json(value)
            else:
                self.__dict__[key] = value
        elif key in self.slots:
            self.add_scoped_slot(key[: key.index("_")], value)
        else:
            self.__dict__[key] = value

    def load_json(self, options_string):
        self.nodes = hjson.loads(options_string.encode("ascii", "ignore"))
        return self.nodes

    def load_json_from_file(self, file_name):
        with open(file_name, "r") as f:
            self.nodes = hjson.loads(f.read().encode("ascii", "ignore"))
        return self.nodes

    def load_pandas_frame(self, df):
        self.columns = [
            Dict(
                {
                    "name": col,
                    "align": "center",
                    "label": col,
                    "field": col,
                    "sortable": True,
                }
            )
            for col in df.columns
        ]
        self.data = df.to_dict("records")


@parse_dict
class QTh(QDiv):
    slots = ["default_slot"]
    html_tag = "q-th"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # position one of top-right | top-left | bottom-right | bottom-left | top | right | bottom | left
        self.prop_list = ["props", "auto-width"]
        self.allowed_events = []
        self.set_keyword_events(**kwargs)


@parse_dict
class QTr(QDiv):
    slots = ["default_slot"]
    html_tag = "q-tr"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # position one of top-right | top-left | bottom-right | bottom-left | top | right | bottom | left
        self.prop_list = ["props", "no-hover"]
        self.allowed_events = []
        self.set_keyword_events(**kwargs)


@parse_dict
class QTd(QDiv):
    slots = ["default_slot"]
    html_tag = "q-td"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # position one of top-right | top-left | bottom-right | bottom-left | top | right | bottom | left
        self.prop_list = ["auto-width", "props", "no-hover"]
        self.allowed_events = []
        self.set_keyword_events(**kwargs)


# Layout components  https://quasar.dev/layout/layout


@parse_dict
class QLayout(QDiv):
    # To understand the 'view' prop read https://quasar.dev/layout-builder

    slots = ["default_slot"]
    html_tag = "q-layout"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # position one of top-right | top-left | bottom-right | bottom-left | top | right | bottom | left
        self.prop_list = ["view", "container"]
        self.allowed_events = ["resize", "scroll", "scroll-height"]
        self.set_keyword_events(**kwargs)


@parse_dict
class QHeader(QDiv):
    slots = ["default_slot"]
    html_tag = "q-header"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # position one of top-right | top-left | bottom-right | bottom-left | top | right | bottom | left
        self.prop_list = ["reveal", "reveal-offset", "value", "bordered", "elevated"]
        self.allowed_events = ["reveal"]
        self.set_keyword_events(**kwargs)


@parse_dict
class QFooter(QDiv):
    slots = ["default_slot"]
    html_tag = "q-footer"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = ["reveal", "reveal-offset", "value", "bordered", "elevated"]
        self.allowed_events = ["reveal"]
        self.set_keyword_events(**kwargs)


@parse_dict
class QDrawer(QDiv):
    slots = ["default_slot", "mini_slot"]
    html_tag = "q-drawer"

    def __init__(self, **kwargs):
        self.value = True  # Default is to show drawer
        self.mini = False
        super().__init__(**kwargs)
        self.prop_list = [
            "side",
            "overlay",
            "mini",
            "mini-to-overlay",
            "breakpoint",
            "behavior",
            "persistent",
            "show-if-above",
            "no-swipe-open",
            "no-swipe-close",
            "value",
            "width",
            "mini-width",
            "bordered",
            "elevated",
            "content-class",
            "content-style",
        ]
        self.allowed_events = [
            "before",
            "input",
            "show",
            "before-show",
            "hide",
            "before-hide",
            "on-layout",
            "click",
            "mouseover",
            "mouseout",
        ]
        self.set_keyword_events(**kwargs)
        self.on("input", self.default_input)
        self.on("before", self.default_before)

    def default_before(self, msg):
        if hasattr(self, "model"):
            self.set_model(msg.value)
        self.value = msg.value

    def default_input(self, msg):
        pass

    async def toggle(self, msg):
        await self.run_method("toggle()", msg.websocket)

    def model_update(self):
        update_value = self.model[0].data[self.model[1]]
        self.value = update_value


@parse_dict
class QPageContainer(QDiv):
    slots = ["default_slot"]
    html_tag = "q-page-container"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = []


@parse_dict
class QPage(QDiv):
    slots = ["default_slot"]
    html_tag = "q-page"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = ["padding", "style-fn"]


@parse_dict
class QPageSticky(QDiv):
    slots = ["default_slot"]
    html_tag = "q-page-sticky"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # position one of top-right | top-left | bottom-right | bottom-left | top | right | bottom | left
        self.prop_list = ["expand", "position", "offset"]


@parse_dict
class QPageScroller(QDiv):
    slots = ["default_slot"]
    html_tag = "q-page-scroller"

    def __init__(self, **kwargs):
        self.duration = 300
        super().__init__(**kwargs)
        # position one of top-right | top-left | bottom-right | bottom-left | top | right | bottom | left
        self.prop_list = ["expand", "position", "offset", "scroll-offset", "duration"]
        # Required in order not have the vue update during the scroll
        self.on("click", self.default_click)

    @staticmethod
    async def default_click(self, msg):
        await asyncio.sleep(1 + self.duration / 1000)


@parse_dict
class QFab(QDiv):
    slots = ["default_slot", "tooltip_slot"]
    html_tag = "q-fab"

    def __init__(self, **kwargs):
        self.value = False  # Default is to show drawer
        super().__init__(**kwargs)
        # direction on of  up | right | down | left   , type one of  a | submit | button | reset
        self.prop_list = [
            "direction",
            "persistent",
            "icon",
            "active-icon",
            "type",
            "value",
            "disable",
            "outline",
            "push",
            "flat",
            "color",
            "text-color",
            "glossy",
            "label",
            "external-label",
            "label-position",
        ]
        self.allowed_events = [
            "input",
            "show",
            "before-show",
            "hide",
            "before-hide",
            "click",
            "mouseover",
            "mouseout",
        ]
        self.set_keyword_events(**kwargs)

    def model_update(self):
        update_value = self.model[0].data[self.model[1]]
        self.value = update_value


@parse_dict
class QFabAction(QDiv):
    slots = ["default_slot"]
    html_tag = "q-fab-action"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # position one of top-right | top-left | bottom-right | bottom-left | top | right | bottom | left
        self.prop_list = [
            "icon",
            "type",
            "to",
            "replace",
            "disable",
            "outline",
            "push",
            "flat",
            "color",
            "text-color",
            "glossy",
            "label",
            "external-label",
            "label-position",
        ]


@parse_dict
class QSkeleton(QDiv):
    slots = ["default_slot"]
    html_tag = "q-skeleton"

    def __init__(self, **kwargs):
        self.type = "rect"
        self.tag = "div"
        super().__init__(**kwargs)
        if not self.animation:
            self.animation = "wave"
        self.prop_list = [
            "tag",
            "type",
            "dark",
            "animation",
            "square",
            "bordered",
            "size",
            "width",
            "height",
        ]


@parse_dict
class QPopupEdit(_QInputBase):
    # Work in progress
    # 'cancel' and 'save' events not working
    html_tag = "q-popup-edit"
    slots = ["default_slot", "title_slot"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list = [
            "touch-position",
            "persistent",
            "separate-close-popup",
            "title",
            "buttons",
            "label-set",
            "label-cancel",
            "value",
            "validate",
            "fit",
            "cover",
            "anchor",
            "self",
            "disable",
            "content-class",
            "content-style",
            "color",
            "offset",
            "square",
            "max-height",
            "max-width",
        ]

        self.allowed_events = ["input", "cancel", "save"]
        self.set_keyword_events(**kwargs)

        def default_event_handler(self, msg):
            print(msg)

        self.on("save", default_event_handler)
        self.on("cancel", default_event_handler)


class ToggleDarkModeBtn(QBtn):
    def __init__(self, **kwargs):
        self.label = "Toggle Dark Mode"
        super().__init__(**kwargs)
        self.on("click", self.toggle_dark_mode)

    @staticmethod
    async def toggle_dark_mode(self, msg):
        msg.page.dark = not msg.page.dark
        await msg.page.set_dark_mode(msg.page.dark)


class QInputDateTime(QInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mask = "####-##-## ##:##"
        self.fill_mask = True
        self.proxy = {}

        date_slot = QIcon(name="event", classes="cursor-pointer")
        c2 = QPopupProxy(transition_show="scale", transition_hide="scale", a=date_slot)
        self.date = QDate(mask="YYYY-MM-DD HH:mm", name="date", a=c2)
        self.proxy["QDate"] = c2

        time_slot = QIcon(name="access_time", classes="cursor-pointer")
        c2 = QPopupProxy(transition_show="scale", transition_hide="scale", a=time_slot)
        self.time = QTime(mask="YYYY-MM-DD HH:mm", format24h=True, name="time", a=c2)
        self.proxy["QTime"] = c2

        self.date.parent = self
        self.time.parent = self
        self.date.value = self.value
        self.time.value = self.value
        self.date.model = self.model
        self.time.model = self.model
        self.prepend_slot = date_slot
        self.append_slot = time_slot
        self.date.on("input", self.date_time_change)
        self.time.on("input", self.date_time_change)
        self.on("input", self.input_change)

    @staticmethod
    async def date_time_change(self, msg):
        self.parent.value = self.value
        self.parent.date.value = self.value
        self.parent.time.value = self.value
        await self.parent.proxy[msg.class_name].run_method("hide()", msg.websocket)

    @staticmethod
    def input_change(self, msg):
        self.date.value = self.value
        self.time.value = self.value


class QInputDate(QInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        date_slot = QIcon(name="event", classes="cursor-pointer")
        c2 = QPopupProxy(transition_show="scale", transition_hide="scale", a=date_slot)
        self.date = QDate(mask="YYYY-MM-DD", name="date", a=c2)

        self.date.parent = self
        self.date.value = self.value
        self.append_slot = date_slot
        self.date.on("input", self.date_time_change)
        self.on("input", self.input_change)
        self.proxy = c2

    @staticmethod
    async def date_time_change(self, msg):
        self.parent.value = self.value
        self.parent.date.value = self.value
        await self.parent.proxy.run_method("hide()", msg.websocket)

    @staticmethod
    def input_change(self, msg):
        self.date.value = self.value


@parse_dict
class QResizeObserver(QDiv):
    html_tag = "q-resize-observer"

    def __init__(self, **kwargs):
        self.debounce = 300
        super().__init__(**kwargs)
        self.prop_list = ["debounce"]
        self.allowed_events = ["resize"]
        self.set_keyword_events(**kwargs)
