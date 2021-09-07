# https://css-tricks.com/alpine-js-the-javascript-framework-thats-used-like-jquery-written-like-vue-and-inspired-by-tailwindcss/  good examples
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# https://codewithhugo.com/alpinejs-component-communication-event-bus/
from .htmlcomponents import *
import re
import tokenize
import io

try:
    from bs4 import BeautifulSoup
    _has_bs4 = True
except:
    _has_bs4 = False


svg_attr_translate_dict = {}
for k,v in svg_attr_dict.items():
    for i in v:
        svg_attr_translate_dict[i.lower()] = i



# class DefaultSimpleDict(Meadows):
class DefaultSimpleDict:

    def __init__(self, wp, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        setattr(self, 'refs', wp.meadows_data['refs'])
        self.wp = wp

    async def dispatch(self, event, event_param=None):
        c = self.wp.meadows_data['events'][event]['el']
        return await c.run_event_function(event, event_param)


if _has_bs4:

    class NewParser():

        allowed_transition_phases = ['enter', 'enter-start', 'enter-end', 'leave', 'leave-start', 'leave-end', 'load', 'load-start', 'load-end']
        default_transition = {'enter': "transition ease-in duration-150", 'enter_start': "transform opacity-0 scale-95",
                              'enter_end': "transform opacity-100 scale-100", 'leave': "transition ease-in duration-75",
                              'leave_start': "transform opacity-100 scale-100", 'leave_end': "transform opacity-0 scale-95",
                              'load': '', 'load_start': '', 'load_end': ''}



        def __init__(self, wp, context, **kwargs):
            super().__init__()
            self.context = context
            self.wp = wp
            self.soup = None
            initial_x_data = kwargs.get('x_data')
            if initial_x_data:
                self.data_components = [Div(data=initial_x_data)]
            else:
                eval_value = DefaultSimpleDict(wp)
                # 'refs': wp.meadows_data['refs']
                setattr(eval_value, 'this', eval_value)
                self.data_components = [Div(data=eval_value.__dict__)]
            self.base_component = None
            self.eval_flag = True
            self.current_tag = None
            self.show_flag = kwargs.get('show_flag', True)

            # Change for_var into a dict like locals() or globals() : {'i': <value of i}
            # self.for_var = kwargs.get('for_var', {})
            #
            self.for_var = kwargs.get('for_var', [])
            self.for_var_name = kwargs.get('for_var_name', [])


        def evaluate(self, expr):
            # evaluate an expression
            if self.eval_flag:
                result = eval(expr, self.context.f_globals, self.current_tag.c.data)
            else:
                result = expr
            return result

        def evaluate_attr(self, tag, attr):
            if self.eval_flag:
                result = eval(tag.attrs[attr], self.context.f_globals, tag.c.data)
            else:
                result = tag.attrs[attr]
            return result

        async def async_evaluate_attr_old(self, tag, attr):
            if self.eval_flag:
                result = (eval(tag.attrs[attr], self.context.f_globals, tag.c.data))
                if inspect.iscoroutine(result):
                    result = await result
            else:
                result = tag.attrs[attr]
            return result

        async def async_evaluate_attr(self, tag, attr, attr_dict):
            if self.eval_flag:
                result = (eval(attr_dict[attr]['value'], self.context.f_globals, tag.c.data))
                if inspect.iscoroutine(result):
                    result = await result
            else:
                result = attr_dict[attr]['value']
            return result

        @staticmethod
        def fix_attr(attr):
            if attr in svg_attr_translate_dict:
                attr = svg_attr_translate_dict[attr]
            return attr.replace('-', '_')


        @staticmethod
        def get_for_vars(s):
            g = tokenize.tokenize(io.BytesIO(s.encode('utf-8')).readline)  # tokenize the string
            t_list = []
            for i in g:
                if i[1] == 'in':
                    break
                if i[0] in [1]:  # NAME is type 1 and OP is type 53
                    t_list.append(i[1])
            return t_list[1:]

        async def feed(self, html_string):
            wp = self.wp
            # html_clean = lxml.html.clean.clean_html(html_string)
            # html_clean = "".join(line.strip() for line in html_clean.split("\n"))
            self.soup = BeautifulSoup(html_string.strip(), 'html.parser')
            assert len(self.soup.contents) > 0, 'Page is empty'
            tag = self.soup.contents[0]
            if tag.name == 'body':
                tag.name = 'div'

            while True:
                # tag = tag.next_element
                if not tag:
                    break
                self.current_tag = tag
                if 'Comment' == type(tag).__name__:
                    tag = tag.next_element
                    continue

                if 'NavigableString' == type(tag).__name__:
                    sv = tag.string.strip()
                    if sv and ('x-text' not in tag.parent.attrs):
                        tag.parent.c.text = tag.string
                    tag = tag.next_element
                    continue
                else:
                    pass
                try:
                    if tag.name == 'input_change':
                        c = tag.c = InputChangeOnly()
                    elif tag.name == 'template':
                        tag.name = 'div'
                        c = tag.c = Div()
                    else:
                        c = tag.c = component_by_tag(tag.name)
                except:
                    print(f'Unknown tag {tag.name}')
                    c = component_by_tag('div')

                attr_dict = {}  # {main: {'modifiers': [], 'value'}}
                for attr, attr_value in tag.attrs.items():
                    # attr_value = tag.attrs[attr]
                    for i, sub_attr in enumerate(attr.split('.')):
                        if i == 0:
                            if sub_attr[:7].lower() == 'x-bind:':
                                main_key = f':{sub_attr[7:]}'
                            elif sub_attr[:5].lower() == 'x-on:':
                                main_key = f'@{sub_attr[5:]}'
                            else:
                                main_key = sub_attr
                            attr_dict[main_key] = {'modifiers': [], 'value': attr_value}
                        else:
                            attr_dict[main_key]['modifiers'].append(sub_attr)

                # if tag.name == 'svg':
                #     print('svg tag', attr_dict)

                if 'x-data' in attr_dict:

                    for_dict = {}
                    if self.for_var_name:
                        for_dict[self.for_var_name] = self.for_var
                    result = (eval(tag.attrs['x-data'], self.context.f_globals, for_dict))
                    if inspect.iscoroutine(result):
                        result = await result
                    eval_value = result


                    if type(eval_value) == dict:
                        # Create class instance from dict
                        eval_value = DefaultSimpleDict(self.wp, **eval_value)
                    # Set 'this' attribute to be the class instance
                    setattr(eval_value, 'this', eval_value)
                    setattr(eval_value, 'refs', wp.meadows_data['refs'])
                    setattr(eval_value, 'wp', wp)
                    # Add methods and class variables to instance dict
                    method_and_var_dict = {}
                    for k, v in eval_value.__class__.__dict__.items():
                        if (not k.startswith('__')) and (k not in eval_value.__dict__):
                            if inspect.isfunction(v):
                                # Differentiate between class methods and instance methods
                                if hasattr(v, '__self__'):
                                    method_and_var_dict[k] = MethodType(v, eval_value.__class__)
                                else:
                                    method_and_var_dict[k] = MethodType(v, eval_value)
                            else:
                                method_and_var_dict[k] = v

                    eval_value.__dict__.update(method_and_var_dict)
                    c.data = eval_value.__dict__
                    eval_value.c = c
                    self.data_components.append(c)
                else:
                    if self.data_components:
                        c.data = self.data_components[-1].data
                    else:
                        c.data = {}

                if 'x-init' in attr_dict:
                    # No await allowed in x-init.
                    exec(tag.attrs['x-init'], self.context.f_globals, c.data)

                if 'x-ref' in attr_dict:
                    wp.meadows_data['refs'][attr_dict['x-ref']['value']] = c

                if ':x-ref' in attr_dict:
                    eval_value = await self.async_evaluate_attr(tag, ':x-ref', attr_dict)
                    wp.meadows_data['refs'][eval_value] = c

                if 'x-if' in attr_dict:
                    if self.show_flag:
                        wp.meadows_data['if'].append((c, attr_dict['x-if']['value'], self.context.f_globals))
                    if await self.async_evaluate_attr(tag, 'x-if', attr_dict):
                        c.show = True
                    else:
                        c.show = False


                try:
                    if 'x-slot' not in attr_dict:
                        tag.parent.c.add(c)
                    else:
                        tag.parent.c.add_scoped_slot(attr_dict['x-slot']['value'], c)
                except:
                    self.base_component = c

                if 'class' in attr_dict:

                    # c.classes = ' '.join(tag.attrs['class'])
                    c.classes = ' '.join(attr_dict['class']['value'])
                    # Class evaluation may change original classes so need to restore them on update
                    if ':class' in attr_dict:
                        # JustPy.class_list.append((c, ' '.join(tag.attrs['class'])))
                        wp.meadows_data['class'].append((c, ' '.join(attr_dict['class']['value'])))

                if ':class' in attr_dict:
                    wp.meadows_data['class_evaluate'].append((c, tag.attrs[':class'], self.context.f_globals))
                    class_dict = self.evaluate(attr_dict[':class']['value'])
                    if isinstance(class_dict, dict):
                        for k, v in class_dict.items():
                            if v:
                                c.set_classes(k)
                    else:
                        c.classes = class_dict

                if 'x-for' in attr_dict:
                    # Creates a function to run using the x-for attribute value as the loop initiator statement
                    # x-for block must be in ONE tag enclosed. So has only one child. If not, first child will be used.
                    # The parent container of the x-for must also have just one child also, the x-for block (siblings will be lost on update)
                    # attr_value = tag.attrs['x-for']
                    attr_value = attr_dict['x-for']['value']
                    if not attr_value:
                        continue
                    for_parent = tag.parent
                    # Next tag to start processing from
                    for_next_tag = tag.next_sibling
                    if not for_next_tag:
                        for_next_tag = tag.parent
                    wp.meadows_data['event_handler_count'] += 1
                    event_handler_count = wp.meadows_data['event_handler_count']
                    func_name = f"for_func{event_handler_count}_{wp.page_id}"
                    attr_value = re.sub(' +', ' ', attr_value)  # Remove multiple spaces
                    for_var = self.get_for_vars(attr_value)
                    for_assignments = ''
                    value_list='['
                    for var in for_var:
                        for_assignments = f'''{for_assignments}c1.data["{var}"] = {var};'''
                        value_list = f'{value_list}{var},'
                    value_list = f'{value_list[:-1]}]'
                    print('for assignments', for_assignments)
                    init_string = ''
                    for k in ['this']:
                        init_string = f'{init_string}{k}=c1.data["{k}"];'
                    for var_name, var_value in zip(self.for_var_name, self.for_var):
                        init_string = f'{init_string}{var_name}={var_value.__repr__()};'
                    for_html_str = ""
                    for child in tag.contents:
                        for_html_str = f'{for_html_str}{str(child)}\n'
                    for_html_str = f'<span>{for_html_str}</span>'

                    func = f'async def {func_name}(wp, c1, pos=None):\n {init_string}\n {attr_value}'
                    func = func + '\n  s = """\n' + for_html_str + '\n"""'


                    func = f'''{func}
      {for_assignments}
      t = await jp.new_parse_meadows_html(wp, s, eval_flag=True, x_data=c1.data, show_flag=False, for_var={value_list}, for_var_name={for_var})
      t._for_creation_{event_handler_count} = True
      for child in t.components:
       child._for_creation_{event_handler_count} = True
       c1.add_component(child, pos)
       pos = pos + 1 if pos==0 or pos else pos
     c1.name = "Liat"
     return c1            
    '''

                    print(func)
                    t = tag.extract()
                    for_parent.c.components.pop()
                    try:
                        exec(func, self.context.f_globals, c.data)
                    except:
                        sys.exit()
                    func_to_run = c.data[func_name]
                    result = await func_to_run(wp, for_parent.c)
                    if not self.for_var and not 'once' in tag.attrs:
                        wp.meadows_data['for'].append((for_parent.c, func_to_run, self.context.f_globals, event_handler_count))

                    tag = for_next_tag.next_element
                    continue


                for attr in attr_dict:

                # for attr in main_attr_list:
                #     attr_split = attr_dict[attr]['modifiers']
                    if attr in ['x-data', 'x-if', 'x-init', 'class', ':class']:  # Add pop above
                        continue
                    attr_value = attr_dict[attr]['value']
                    # old_attr = attr
                    # if attr[:5].lower() == 'x-on:':
                    #     attr = f'@{attr[5:]}'
                    # elif attr[:7].lower() == 'x-bind:':
                    #     attr = f':{attr[7:]}'


                    if attr == 'x-text':
                        c.text = await self.async_evaluate_attr(tag, attr, attr_dict)
                        # JustPy.attrs_list.append((c, 'text', attr_value, self.context.f_globals))
                        if 'once' not in attr_dict[attr]['modifiers']:
                            wp.meadows_data['attrs'].append((c, 'text', attr_value, self.context.f_globals))
                    elif attr == 'x-html':
                        c.inner_html = await self.async_evaluate_attr(tag, attr, attr_dict)
                        wp.meadows_data['attrs'].append((c, 'inner_html', attr_value, self.context.f_globals))
                    elif attr == 'x-model':
                        c.model = [c, attr_value]
                        # exec(f'c.model = [c, {attr_value}]', self.context.f_globals, tag.c.data)
                    elif attr[:13].lower() == 'x-transition:':  # x-transition
                        transition_phase = attr.split(':')[1]
                        assert transition_phase in self.allowed_transition_phases, f'Unrecognized transition phase: {transition_phase}'
                        if not c.transition:
                            c.transition = create_transition()
                        c.transition[transition_phase.replace('-','_')] = attr_value

                    # elif attr == 'x-for':
                    #     # Runs the function given as vale of x_for
                    #     JustPy.for_list.append((c, attr_value, self.context.f_globals))
                    #     func = self.context.f_globals[attr_value]
                    #     # Do you need another parameter for func which is self.context.f_globals? probably not
                    #     if inspect.iscoroutinefunction(func):
                    #         await func(c)
                    #     else:
                    #         func(c)


                    elif attr[0] == '@':
                        if attr_value in self.context.f_locals:
                            c.on(attr[1:], self.context.f_locals[attr_value], meadows=True)
                        elif attr_value in self.context.f_globals:
                            c.on(attr[1:], self.context.f_globals[attr_value],meadows=True)
                        else:
                            # JustPy.event_handler_count += 1
                            wp.meadows_data['event_handler_count'] += 1
                            func_name = f"_implied_func{wp.meadows_data['event_handler_count']}_{wp.page_id}"
                            init_string = ""
                            end_string = """
     for k,v in locals().items():
      if k in self.data:
       self.data[k] = v
                              """

                            # for k,v in c.data.items():
                            #     init_string= f'{init_string}{k}=self.data["{k}"];'
                            for k in ['this']:
                                init_string = f'{init_string}{k}=self.data["{k}"];'

                            # if self.for_var_name:
                            #     setattr(c, f'___{self.for_var_name}', self.for_var)
                            #     init_string = f'{init_string}{self.for_var_name}=self.___{self.for_var_name};'

                            if self.for_var_name:
                                for i, f in enumerate(self.for_var_name):
                                    setattr(c, f'___{f}', self.for_var[i])
                                    init_string = f'{init_string}{f}=self.___{f};'



                            fn_string = f'async def {func_name}(self, msg):\n {init_string}{attr_value}'  # remove first and last characters which are quotes
                            if 'noupdate' in attr_dict[attr]['modifiers']:
                                fn_string = f'{fn_string}; return True'
                            # print('*****\n',fn_string,'\n******')
                            exec(fn_string)
                            if 'window' in attr_dict[attr]['modifiers']:
                                wp.on(attr[1:], locals()[func_name], meadows=True)
                                wp.data = c.data
                            else:
                                c.on(attr[1:], locals()[func_name], meadows=True)
                                wp.meadows_data['events'][attr[1:]] = {'el': c}
                            if 'stop' in attr_dict[attr]['modifiers']:
                                c.event_propagation = False
                    elif attr[0] == ':':
                        fixed_attr = self.fix_attr(attr[1:])
                        setattr(c, fixed_attr, await self.async_evaluate_attr(tag, attr, attr_dict))
                        if 'once' not in attr_dict[attr]['modifiers']:
                            wp.meadows_data['attrs'].append((c, fixed_attr, attr_value, self.context.f_globals))
                    else:
                        # Take care of svg camelcase attributes
                        # if attr == 'viewbox':
                        #     print(svg_tags_use_dict)
                            # attr = 'viewBox'
                        setattr(c, self.fix_attr(attr), attr_value)

                # Done last in case classes has been changed
                # for attr in tag.attrs:
                #     attr_split = attr.split('.')
                #     if 'x-show' == attr_split[0]:
                #         attr_value = tag.attrs[attr]
                #         if self.show_flag:
                #             wp.meadows_data['show'].append((c, attr_value, self.context.f_globals))
                #         # if self.evaluate_attr(tag, 'x-show'):
                #         if await self.async_evaluate_attr(tag, attr):
                #             c.remove_class('hidden')
                #         else:
                #             c.set_class('hidden')
                #         if 'transition' in attr_split:
                #             c.transition = self.default_transition

                if 'x-show' in attr_dict:
                    if self.show_flag:
                        wp.meadows_data['show'].append((c, attr_dict['x-show']['value'], self.context.f_globals))
                    # if self.evaluate_attr(tag, 'x-show'):
                    if await self.async_evaluate_attr(tag, 'x-show', attr_dict):
                        c.remove_class('hidden')
                    else:
                        c.set_class('hidden')
                    if 'transition' in attr_dict['x-show']['modifiers']:
                        c.transition = self.default_transition


                tag = tag.next_element





            # print('-----------------')
            # print(self.base_component.to_html(2,2))






async def new_parse_meadows_html(wp, html_string, **kwargs):
    context = inspect.stack()[1][0]
    parser = NewParser(wp, context, **kwargs)
    await parser.feed(html_string)
    return parser.base_component


async def new_parse_meadows_html_file(wp, html_file, **kwargs):
    with open(html_file, encoding="utf-8") as f:
        context = inspect.stack()[1][0]
        parser = NewParser(wp, context, **kwargs)
        await parser.feed(f.read())
        return parser.base_component





async def update_lists(wp):
    meadows_data = {'if': [], 'show': [], 'attrs': [], 'for': [], 'class': [], 'class_evaluate': [],
                         'refs': Dict({}), 'event_handler_count': 0}
    # JustPy.show_list.append((c, attr[0], attr[1]))
    # print('attrs update')
    # for p in JustPy.class_list:
    for p in wp.meadows_data['class']:
        setattr(p[0], 'classes', p[1])
    for p in wp.meadows_data['class_evaluate']:
        # class_dict = eval(p[1], p[2], p[0].data)
        class_dict = await update_eval(p[1], p[2], p[0].data)
        assert isinstance(class_dict, dict), "Class evaluation did not result in dict in update"
        for k, v in class_dict.items():
            if v:
                p[0].set_classes(k)
    for p in wp.meadows_data['attrs']:
        # setattr(p[0], p[1], eval(p[2], p[3], p[0].data))
        setattr(p[0], p[1], await update_eval(p[2], p[3], p[0].data))
    for p in wp.meadows_data['for']:
        c = p[0]
        for_id = p[3]
        insert_position = None
        for i, comp in enumerate(c.components):
            if hasattr(comp, f'_for_creation_{for_id}'):
                comp.delete_components()
                if insert_position is None:
                    insert_position = i
        c.components[:] = [comp for comp in c.components if not hasattr(comp, f'_for_creation_{for_id}')]
        func = p[1]
        if inspect.iscoroutinefunction(func):
            # await func(c, insert_position)
            await func(wp, c, insert_position)
        else:
            # func(c, insert_position)
            func(wp, c, insert_position)
    for p in wp.meadows_data['show']:
        c = p[0]
        r = await update_eval(p[1], p[2], c.data)
        print(r)
        if not r:
            c.set_class('hidden')
        else:
            c.remove_class('hidden')
    for p in wp.meadows_data['if']:
        c = p[0]
        # r = eval(p[1], p[2], c.data)
        r = await update_eval(p[1], p[2], c.data)
        if r:
            c.show = True
        else:
            c.show = False


async def update_eval(attr_value, global_context, local_context):
    result = eval(attr_value, global_context, local_context)
    if inspect.iscoroutine(result):
        result = await result
    return result


