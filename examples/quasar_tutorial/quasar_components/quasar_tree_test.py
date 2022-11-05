# Justpy Tutorial demo quasar_tree_test from docs/quasar_tutorial/quasar_components.md
import justpy as jp

async def expand_tree(self, msg):
    return await self.tree.run_method('expandAll()', msg.websocket)

async def collapse_tree(self, msg):
    return await self.tree.run_method('collapseAll()', msg.websocket)


def quasar_tree_test():
    wp = jp.QuasarPage()
    d = jp.Div(classes="q-pa-md q-gutter-sm", a=wp)
    node_string = """
    [
        {
          label: 'Satisfied customers (with avatar)',
          avatar: 'https://cdn.quasar.dev/img/boy-avatar.png',
          children: [
            {
              label: 'Good food (with icon)',
              icon: 'restaurant_menu',
              children: [
                { label: 'Quality ingredients', icon: 'favorite' },
                { label: 'Good recipe' }
              ]
            },
            {
              label: 'Good service (disabled node with icon)',
              icon: 'room_service',
              disabled: true,
              children: [
                { label: 'Prompt attention' },
                { label: 'Professional waiter' }
              ]
            },
            {
              label: 'Pleasant surroundings (with icon)',
              icon: 'photo',
              children: [
                {
                  label: 'Happy atmosphere (with image)',
                  img: 'https://cdn.quasar.dev/img/logo_calendar_128px.png'
                },
                { label: 'Good table presentation' },
                { label: 'Pleasing decor' }
              ]
            }
          ]
        }
      ]
    """

    b1 = jp.QBtn(label='Expand', a=d, click=expand_tree)
    b2 = jp.QBtn(label='Collapse', a=d, click=collapse_tree)

    tree = jp.QTree(a=d, node_key='label', nodes=node_string, tick_strategy="leaf", no_connectors=False, default_expand_all=True)
    d1 = jp.Div(text='', a=d)

    def my_updated(self, msg):
        print('in my updated')
        d1.text = str(msg.value)
    tree.on('update:ticked', my_updated)

    b1.tree = tree
    b2.tree = tree
    return wp

# initialize the demo
from examples.basedemo import Demo
Demo("quasar_tree_test", quasar_tree_test)
