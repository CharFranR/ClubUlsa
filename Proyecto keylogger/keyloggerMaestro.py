import socket

def servidor():
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind(('0.0.0.0', 9999))
    servidor_socket.listen(1)
    print("Esperando conexión...")

    conn, addr = servidor_socket.accept()
    print(f"Conectado desde {addr}")

    with open('recibido.txt', 'a', encoding='utf-8') as f:
        while True:
            datos = conn.recv(1024)
            if not datos:
                break
            texto = datos.decode('utf-8')
            print(texto, end='', flush=True)
            f.write(texto)

    conn.close()
    servidor_socket.close()

if __name__ == '__main__':
    servidor()
