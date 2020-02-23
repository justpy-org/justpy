import justpy as jp

html_string = """
<div>
    <button class="bg-pink-500 text-white active:bg-pink-600 font-bold uppercase text-sm px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 mb-1" type="button" style="transition: all .15s ease" name="button">
      Open regular modal
    </button>
    <div  class="overflow-x-hidden overflow-y-auto fixed inset-0 z-50 outline-none focus:outline-none justify-center items-center flex" name="modal">
      <div class="relative w-auto my-6 mx-auto max-w-3xl">
        <!--content-->
        <div class="border-0 rounded-lg shadow-lg relative flex flex-col w-full bg-white outline-none focus:outline-none">
          <!--header-->
          <div class="flex items-start justify-between p-5 border-b border-solid border-gray-300 rounded-t">
            <h3 class="text-3xl font-semibold">
              Modal Title
            </h3>
            <button class="p-1 ml-auto bg-transparent border-0 text-black opacity-5 float-right text-3xl leading-none font-semibold outline-none focus:outline-none" name="close_icon">
              <span class="bg-transparent text-black opacity-5 h-6 w-6 text-2xl block outline-none focus:outline-none">
                ×
              </span>
            </button>
          </div>
          <!--body-->
          <div class="relative p-6 flex-auto">
            <p class="my-4 text-gray-600 text-lg leading-relaxed">
              I always felt like I could do anything. That’s the main
              thing people are controlled by! Thoughts- their perception
              of themselves! They're slowed down by their perception of
              themselves. If you're taught you can’t do anything, you
              won’t do anything. I was taught I could do everything.
            </p>
          </div>
          <!--footer-->
          <div class="flex items-center justify-end p-6 border-t border-solid border-gray-300 rounded-b">
            <button class="text-red-500 bg-transparent border border-solid border-red-500 hover:bg-red-500 hover:text-white active:bg-red-600 font-bold uppercase text-sm px-6 py-3 rounded outline-none focus:outline-none mr-1 mb-1" type="button" style="transition: all .15s ease">
              Close
            </button>
            <button class="text-red-500 background-transparent font-bold uppercase px-6 py-2 text-sm outline-none focus:outline-none mr-1 mb-1" type="button" style="transition: all .15s ease" >
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>
    <div  class="opacity-25 fixed inset-0 z-40 bg-black" name="modal_background"></div>
  </div>
"""

def show_modal(self, msg):
    self.modal.show =True
    self.modal.modal_background.show = True

def close_modal(self, msg):
    self.modal.show = False
    self.modal.modal_background.show = False

def test_tailwind():
    wp = jp.WebPage()
    d = jp.Div(a=wp, classes='m-2 w-1/3')
    c = jp.parse_html(html_string, a=d)
    modal = c.name_dict['modal']
    modal.modal_background = c.name_dict['modal_background']
    modal.show = False
    modal.modal_background.show = False
    modal_button = c.name_dict['button']
    modal_button.modal = modal
    modal_button.on('click', show_modal)
    close_icon = c.name_dict['close_icon']
    close_icon.modal = modal
    close_icon.on('click', close_modal)


    return wp

jp.justpy(test_tailwind)