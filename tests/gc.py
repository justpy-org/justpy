import justpy as jp
import gc

class MyPage(jp.WebPage):

    async def on_disconnect(self, websocket):
        self.remove_page()
        for c in self.components:
            c.delete()
        # self.components = None
        # del self.components
        del self
        print('len', len(jp.JustpyBaseComponent.instances))
        print('collected', gc.collect())


def gc_test():
    wp = MyPage()
    print(jp.WebPage.instances)
    for i in range(1000):
        d = jp.Div(text=f'{i}', temp=False, a=wp)
    return wp

jp.justpy(gc_test)