"""
Created on 2022-09-07

@author: wf
"""
from tests.basetest import Basetest
from jpcore.template import Context

class TestTemplate(Basetest):
    """
    Tests template handling
    """
    
    def setUp(self, debug=False, profile=True):
        Basetest.setUp(self, debug=debug, profile=profile)
        self.context_dict = {
            "html": "",
            "justpy_dict": '[{"attrs": {}, "id": null, "vue_type": "html_component", '
            '"show": true, "events": [], "event_modifiers": {}, "classes": '
            '"text-5xl m-2", "style": "", "set_focus": false, "html_tag": '
            '"p", "class_name": "P", "event_propagation": true, '
            '"inner_html": "", "animation": false, "debug": false, '
            '"transition": null, "directives": {}, "scoped_slots": {}, '
            '"object_props": [], "text": "Hello there!"}]',
            "options": {
                "aggrid": True,
                "aggrid_enterprise": False,
                "bokeh": False,
                "component_file_list": [],
                "deckgl": False,
                "highcharts": True,
                "katex": False,
                "no_internet": True,
                "plotly": False,
                "quasar": False,
                "quasar_version": None,
                "static_name": "static",
                "tailwind": True,
                "vega": False,
            },
            "page_id": 0,
            "page_options": {
                "body_classes": "",
                "body_html": "",
                "body_style": "",
                "css": "",
                "dark": False,
                "debug": False,
                "display_url": None,
                "events": [],
                "favicon": "",
                "head_html": "",
                "highcharts_theme": None,
                "redirect": None,
                "reload_interval": None,
                "title": "JustPy",
            },
            "request": None,
            "use_websockets": "true",
        }
        self.context_obj = Context(self.context_dict)

    def test_html(self):
        """
        test html generation
        """
        html=self.context_obj.as_html_lines()
        print(html)
        
    def test_javascript(self):
        """
        test javascript generation
        """
        js = self.context_obj.as_javascript_constructor()
        debug = True
        if debug:
            print(js)
        for param in [
            "window",
            "page_id",
            "title",
            "use_websockets",
            "redirect",
            "display_url",
            "page_ready",
            "result_ready",
            "reload_interval",
            "events",
            "static_resources_url",
            "debug",
        ]:
            self.assertIn(f"// {param}", js)
