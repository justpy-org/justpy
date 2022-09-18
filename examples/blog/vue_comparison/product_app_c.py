# Justpy Tutorial demo product_app_c from docs/blog/vue_comparison.md
import justpy as jp

products = [
            {'id': 1, 'quantity': 1, 'name': 'Compass'},
            {'id': 2, 'quantity': 0, 'name': 'Jacket'},
            {'id': 3, 'quantity': 5, 'name': 'Hiking Socks'},
            {'id': 4, 'quantity': 2, 'name': 'Suntan Lotion'},
            ]


class Products(jp.Div):

    def __init__(self, **kwargs):
        self.products = products
        super().__init__(**kwargs)
        self.ul = jp.Ul(a=self)
        self.total_inventory = jp.H2(text='Totals', a=self)

    def total_products(self):
        total = 0
        for product in self.products:
            total += product["quantity"]
        return total

    def react2(self, data):
        self.ul.delete_components()
        for product in self.products:
            item = jp.Li(a=self.ul)
            jp.Input(type='number', product=product, a=item, value=product["quantity"], input='self.product["quantity"] = self.value')
            jp.Span(text=f'{product["quantity"]} {product["name"]}', a=item, style='margin-left: 10px')
            if product["quantity"] == 0:
                jp.Span(text=' - OUT OF STOCK', a=item)
            jp.Button(text='Add', a=item, product=product, click='self.product["quantity"] += 1', style='margin-left: 10px')
        self.total_inventory.text = f'Total Inventory: {self.total_products()}'


def product_app_c():
    wp = jp.WebPage(tailwind=False)
    Products(a=wp)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("product_app_c",product_app_c)
