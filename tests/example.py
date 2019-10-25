import justpy as jp


wp = jp.WebPage()
for i in range(100):
    p = jp.P(text=f'{i+1}) Hello World!', style=f'font-size: {i}px')
    wp.add(p)

@jp.SetRoute('/hello')
async def hello_world():
    return wp


jp.justpy()
print('after')

