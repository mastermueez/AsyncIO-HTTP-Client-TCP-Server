import asyncio

async def handle_echo(reader, writer): # reader = request, writer = response
    # data sent by client 
    data = await reader.read(100) # byte object

    #print("Raw data type: ",type(data))
    message = data.decode() # str object
    #print("After decoding, data type: ",type(message))

    addr = writer.get_extra_info('peername')
    print("\nReceived %r from %r" % (message, addr))

    # data to be sent back to client
    writer.write(("ACK message: "+message).encode()) # data written must be byte object
    await writer.drain()

    print("Close the client socket")
    writer.close()

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', 8888, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()