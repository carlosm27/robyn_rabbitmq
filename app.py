from robyn import Robyn, status_codes

from robyn.robyn import Response
import asyncio
import aio_pika

import ast
app = Robyn(__file__)


@app.get("/")
async def hello():
    return Response(status_code=status_codes.HTTP_200_OK, headers={}, body="Hello, World!")


async def startup():
    loop = asyncio.get_event_loop()
    connection = await aio_pika.connect("amqp://guest:guest@localhost/", loop = loop)
    channel =  await connection.channel()
    queue = await channel.declare_queue("hello")
    

    def callback(message: aio_pika.IncomingMessage):
        tracker = message.body.decode("utf-8")

        print(tracker)
    await queue.consume(callback)    

app.startup_handler(startup)

app.start(port=8000, url="0.0.0.0")
