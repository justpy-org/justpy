import uvicorn
from starlette.applications import Starlette
from starlette.endpoints import WebSocketEndpoint, HTTPEndpoint
from starlette.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'])

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.route("/")
class Homepage(HTTPEndpoint):
    async def get(self, request):
        return HTMLResponse(html)


@app.websocket_route("/ws")
class Echo(WebSocketEndpoint):
    socket_id = 0
    sockets = []
    # encoding = "json"
    async def on_connect(self, websocket):
        await websocket.accept()
        print('connected')
        Echo.sockets.append(websocket)
        websocket.open = True
        websocket.state.id = Echo.socket_id
        Echo.socket_id += 1
        print(websocket)
        # print(dir(websocket))
        await websocket.send_text(f"You are connected")

    async def on_receive(self, websocket, data):
        print(data)
        print(websocket, websocket.state.id)
        # print(dir(websocket))
        await websocket.send_text(f"Message text was: {data}")
        for w in Echo.sockets:
            print('socket', w)
            if w.open:
                await w.send_text(f"From other socket: {data}")

    async def on_disconnect(self, websocket, close_code):
        websocket.open = False
        print(close_code,'close')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)