# Justpy Tutorial demo alert_test2 from docs/tutorial/custom_components.md
import justpy as jp

class MyAlert(jp.Div):

    def __init__(self, **kwargs):
        self.title_text = 'This is the title'
        self.body_text = 'This is the body'
        super().__init__(**kwargs)
        root = self
        c1 = jp.Div(classes='bg-teal-100 border-t-4 border-teal-500 rounded-b text-teal-900 px-4 py-3 shadow-md',
                    role='alert', a=root)
        c2 = jp.Div(classes='flex', a=c1)
        c3 = jp.Div(classes='py-1', a=c2)
        c4 = jp.Svg(classes='fill-current h-6 w-6 text-teal-500 mr-4', xmlns='http://www.w3.org/2000/svg',
                    viewBox='0 0 20 20', a=c3)
        c5 = jp.Path(
            d='M2.93 17.07A10 10 0 1 1 17.07 2.93 10 10 0 0 1 2.93 17.07zm12.73-1.41A8 8 0 1 0 4.34 4.34a8 8 0 0 0 11.32 11.32zM9 11V9h2v6H9v-4zm0-6h2v2H9V5z',
            a=c4)
        c6 = jp.Div(a=c2)
        c7 = jp.P(classes='font-bold text-lg', a=c6, text=self.title_text)
        c8 = jp.P(classes='text-sm', a=c6, text=self.body_text)
        self.title_p = c7
        self.body_p = c8

    def react(self, data):
        self.title_p.text = self.title_text
        self.body_p.text = self.body_text
        self.text = ''


greetings = ['Bonjour', 'Hola', 'Zdravstvuyte', 'Nǐn hǎo', 'Salve', 'Konnichiwa', 'Guten Tag', 'Olá', 'Anyoung haseyo',
             'Asalaam alaikum', 'Goddag', 'Shikamoo', 'Goedendag', 'Yassas', 'Dzień dobry', 'Selamat siang', 'Namaste',
             'Merhaba', 'Shalom', ' God dag']


def translate(self, msg):
    self.title_text = 'Hello'

def alert_test2():
    wp = jp.WebPage()
    for greeting in greetings:
        d = MyAlert(a=wp, classes='m-2 w-1/4', title_text='hello', body_text='How is everybody?')
        d.on('click', translate)
        d.title_text = greeting
    return wp


# initialize the demo
from  examples.basedemo import Demo
Demo ("alert_test2",alert_test2)
