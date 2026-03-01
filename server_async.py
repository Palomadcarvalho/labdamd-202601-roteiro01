import asyncio

HOST = '127.0.0.1'
PORT = 65432

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    """
    Corrotina chamada pelo Event Loop para cada nova conexão.
    Substitui a função que antes rodava em uma Thread separada.
    """
    addr = writer.get_extra_info('peername')
    print(f"[NOVA CONEXÃO] {addr}")

    # 1. Leia os dados enviados pelo cliente (use 'await reader.read(1024)')
    data = await reader.read(1024)
    msg = data.decode('utf-8')
    
    if msg:
        print(f"[{addr}] Processando: {msg}")

        # 2. Simule um processamento pesado SEM bloquear a thread principal.
        #    Use 'await asyncio.sleep(5)' — NÃO use 'time.sleep(5)'.
        #    Entenda a diferença: time.sleep bloqueia a Thread; asyncio.sleep
        #    apenas suspende a corrotina e devolve o controle ao Event Loop.
        await asyncio.sleep(5)

        # 3. Envie a resposta ao cliente (use 'writer.write(...)' e 'await writer.drain()')
        resposta = f"Processado: {msg}".encode('utf-8')
        writer.write(resposta)
        await writer.drain()

    # 4. Feche a conexão (use 'writer.close()' e 'await writer.wait_closed()')
    writer.close()
    await writer.wait_closed()

    print(f"[DESCONECTADO] {addr}")


async def main():
    """
    Ponto de entrada assíncrono: cria e inicia o servidor.
    """
    # Use asyncio.start_server() passando handle_client, HOST e PORT
    server = await asyncio.start_server(handle_client, HOST, PORT)

    print(f"[ASSÍNCRONO] Servidor rodando em {HOST}:{PORT} — Event Loop ativo.")

    # Mantenha o servidor rodando indefinidamente
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())