import justpy as jp
jp.LOGGING_LEVEL = 0
input_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"

async def input_demo(request):
    wp = jp.WebPage()
    in1 = jp.Input(a=wp, classes=input_classes, placeholder='Please type here')
    return wp

jp.justpy(input_demo)
