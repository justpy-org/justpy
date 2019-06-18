AJAX Page Reload
================

By setting the ``reload_interval`` attribute of a WebPage, the page will
be set to reload every number of seconds as set by the number

Example:

.. code:: python

   async def ajax_clock_counter():
       clock_div.text = time.strftime("%a, %d %b %Y, %H:%M:%S", time.localtime())
       await asyncio.sleep(1)
       jp.JustPy.loop.create_task(ajax_clock_counter())


   async def ajax_clock_test(request):
       wp.reload_interval = 1
       return wp


   async def ajax_clock_init():
       jp.JustPy.loop.create_task(ajax_clock_counter())

   jp.justpy(ajax_clock_test, startup=ajax_clock_init)

This can be useful for dashboard and updating pages without using
websockets. Easier to host and run serverless.