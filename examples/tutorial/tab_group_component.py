"""
Created on 2022-08-24

@author: em
"""
from justpy import Div, Ul, Li, A


class Tabs(Div):

    tab_label_classes = "overflow-hidden cursor-pointer bg-white inline-block py-2 px-4 text-blue-500 hover:text-blue-800 font-semibold"
    tab_label_classes_selected = "overflow-hidden cursor-pointer bg-white inline-block border-l border-t border-r rounded-t py-2 px-4 text-blue-700 font-semibold"
    item_classes = "flex-shrink mr-1"
    item_classes_selected = "flex-shrink -mb-px mr-1"
    wrapper_style = "display: flex; position: absolute; width: 100%; height: 100%;  align-items: center; justify-content: center; background-color: #fff;"

    def __init__(self, **kwargs):

        self.tabs = []  # list of {'id': id, 'label': label, 'content': content}
        self.value = (
            None  # The value of the tabs component is the id of the selected tab
        )
        self.content_height = 500
        self.last_rendered_value = None
        self.animation = False
        self.animation_next = "slideInRight"
        self.animation_prev = "slideOutLeft"
        self.animation_speed = "faster"  # '' | 'slow' | 'slower' | 'fast'  | 'faster'

        super().__init__(**kwargs)

        self.tab_list = Ul(classes="flex flex-wrap border-b", a=self)
        self.content_div = Div(a=self)
        self.delete_list = []

    def __setattr__(self, key, value):
        if key == "value":
            try:
                self.previous_value = self.value
            except:
                pass
        self.__dict__[key] = value

    def add_tab(self, id, label, content):
        self.tabs.append({"id": id, "label": label, "content": content})
        if not self.value:
            self.value = id

    def get_tab_by_id(self, id):
        for tab in self.tabs:
            if tab["id"] == id:
                return tab
        return None

    def set_content_div(self, tab):
        self.content_div.add(tab["content"])
        self.content_div.set_classes("relative overflow-hidden border")
        self.content_div.style = f"height: {self.content_height}px"

    def set_content_animate(self, tab):
        self.wrapper_div_classes = (
            self.animation_speed
        )  # Component in this will be centered

        if self.previous_value:
            self.wrapper_div = Div(
                classes=self.wrapper_div_classes,
                animation=self.animation_next,
                temp=True,
                style=f"{self.wrapper_style} z-index: 50;",
                a=self.content_div,
            )
            self.wrapper_div.add(tab["content"])
            self.wrapper_div = Div(
                classes=self.wrapper_div_classes,
                animation=self.animation_prev,
                temp=True,
                style=f"{self.wrapper_style} z-index: 0;",
                a=self.content_div,
            )
            self.wrapper_div.add(self.get_tab_by_id(self.previous_value)["content"])
        else:
            self.wrapper_div = Div(
                classes=self.wrapper_div_classes,
                temp=True,
                a=self.content_div,
                style=self.wrapper_style,
            )
            self.wrapper_div.add(tab["content"])

        self.content_div.set_classes("relative overflow-hidden border")
        self.content_div.style = f"height: {self.content_height}px"

    def model_update(self):
        val = self.model[0].data[self.model[1]]
        if self.get_tab_by_id(val):
            self.value = val

    def delete(self):
        for c in self.delete_list:
            c.delete_flag = True
            c.delete()
            c.needs_deletion = False

        if self.delete_flag:
            for tab in self.tabs:
                tab["content"].delete()
                tab["content"] = None
        super().delete()

    @staticmethod
    async def tab_click(self, msg):
        if self.tabs.value != self.tab_id:
            previous_tab = self.tabs.value
            self.tabs.value = self.tab_id
            if hasattr(self.tabs, "model"):
                self.tabs.model[0].data[self.tabs.model[1]] = self.tabs.value
            # Run change if it exists
            if self.tabs.has_event_function("change"):
                msg.previous_tab = previous_tab
                msg.new_tab = self.tabs.value
                msg.id = self.tabs.id
                msg.value = self.tabs.value
                msg.class_name = self.tabs.__class__.__name__
                return await self.tabs.run_event_function("change", msg)
        else:
            return True  # No need to update page

    def convert_object_to_dict(self):
        if hasattr(self, "model"):
            self.model_update()
        self.set_classes("flex flex-col")
        self.tab_list.delete_components()
        self.content_div.components = []
        for tab in self.tabs:
            if tab["id"] != self.value:
                tab_li = Li(a=self.tab_list, classes=self.item_classes)
                li_item = A(
                    text=tab["label"],
                    classes=self.tab_label_classes,
                    a=tab_li,
                    delete_flag=False,
                )
                self.delete_list.append(li_item)
            else:
                tab_li = Li(a=self.tab_list, classes=self.item_classes_selected)
                li_item = A(
                    text=tab["label"],
                    classes=self.tab_label_classes_selected,
                    a=tab_li,
                    delete_flag=False,
                )
                self.delete_list.append(li_item)
                if self.animation and (self.value != self.last_rendered_value):
                    self.set_content_animate(tab)
                else:
                    self.set_content_div(tab)
            li_item.tab_id = tab["id"]
            li_item.tabs = self
            li_item.on("click", self.tab_click)
        self.last_rendered_value = self.value
        d = super().convert_object_to_dict()

        return d


class TabsPills(Tabs):
    tab_label_classes = "cursor-pointer inline-block border border-white rounded hover:border-gray-200 text-blue-500 hover:bg-gray-200 py-1 px-3"
    tab_label_classes_selected = "cursor-pointer inline-block border border-blue-500 rounded py-1 px-3 bg-blue-500 text-white"
    item_classes = "flex-shrink mr-3"
    item_classes_selected = "flex-shrink -mb-px mr-3"
