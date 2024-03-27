import socket
import asyncio


async def parser(reader, writer):
    try:
        while True:
            data = await reader.read(1024)
            source_port = int.from_bytes(data[0:2], 'big')
            destination_port = int.from_bytes(data[2:4], 'big')
            verification_tag = int.from_bytes(data[4:8], 'big')
            checksum = int.from_bytes(data[8:12], 'big')
            chunk_type = int.from_bytes(data[13:14], 'big')
            chunk_flags = int.from_bytes(data[14:15], 'big')
            chunk_length = int.from_bytes(data[15:17], 'big')
            if chunk_length > 4:
                data_end = 17 + chunk_length - 4
                chunk_value = int.from_bytes(data[17:data_end], 'big')
            else:
                chunk_value = None
            print(f'source_port = {source_port}\n'
                  f'destination_port = {destination_port}\n'
                  f'verification_tag = {verification_tag}\n'
                  f'checksum = {checksum}\n'
                  f'chunk_type = {chunk_type}\n'
                  f'chunk_flags = {chunk_flags}\n'
                  f'chunk_length = {chunk_length}\n'
                  f'chunk_value = {chunk_value}')
    except asyncio.CancelledError:
        writer.close()
        await writer.wait_closed()


async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_SCTP)
    server_socket.bind(('localhost', 5500))
    server_socket.listen()
    server = await asyncio.start_server(parser, 'localhost', 5500, sock=server_socket)
    async with server:
        await server.serve_forever()




if __name__ == "__main__":
    asyncio.run(main())
