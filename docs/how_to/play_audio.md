# How to Play Audio

```python
import justpy as jp

audio_file_url = 'https://file-examples-com.github.io/uploads/2017/11/file_example_MP3_700KB.mp3'


async def play_audio(self, msg):
    await msg.page.run_javascript(f"""
    new Audio('{audio_file_url}').play();
    """)


def audio_test():
    wp = jp.WebPage()
    jp.Button(text='Play Audio', classes='m-2 '+jp.Styles.button_simple, click=play_audio, a=wp)
    return wp


jp.justpy(audio_test)
```