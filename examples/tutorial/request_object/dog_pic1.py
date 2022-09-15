# Justpy Tutorial demo dog_pic1 from docs/tutorial/request_object.md
import justpy as jp

async def dog_pic1(request):
    wp = jp.WebPage()
    breed = request.query_params.get('breed', 'papillon' )
    r = await jp.get(f'https://dog.ceo/api/breed/{breed}/images/random')
    img_url = r['message']
    jp.Img(src=img_url, a=wp, classes='m-2 p-2')
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("dog_pic1",dog_pic1)
