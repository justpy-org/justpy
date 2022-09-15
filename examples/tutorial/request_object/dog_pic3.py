# Justpy Tutorial demo dog_pic3 from docs/tutorial/request_object.md
import justpy as jp

async def get_image2(self, msg):
    r = await jp.get(f'https://dog.ceo/api/breed/{msg.page.breed}/images/random')
    self.src = r['message']

@jp.SetRoute('/breed/{breed}')
async def dog_pic3(request):
    wp = jp.WebPage()
    breed = request.path_params.get('breed', 'papillon')
    wp.breed = breed
    r = await jp.get(f'https://dog.ceo/api/breed/{breed}/images/random')
    img_url = r['message']
    jp.Img(src=img_url, a=wp, classes='m-2 p-2 cursor-pointer', click=get_image2)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("dog_pic3",dog_pic3)
