import selectors
import socket
import types


def accept_wrapper(sock):
    conexion, direccion = sock.accept()
    print("Conexion proveniente de", direccion)
    conexion.setblocking(False)
    data = types.SimpleNamespace(addr=direccion, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conexion, events, data=data)


def service_connection(cliente, accionRW):
    sock = cliente.fileobj
    data = cliente.data
    if accionRW & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
        else:
            print("Conexion cerrada para", data.addr)
            sel.unregister(sock)
            sock.close()
    if accionRW & selectors.EVENT_WRITE:
        if data.outb:
            print("Replicando", repr(data.outb), "para", data.addr)
            data_enviar = sock.send(data.outb)
            data.outb = data.outb[data_enviar:]


sel = selectors.DefaultSelector()
HOST = "127.0.0.1"  # Mi localhost
PORT = 2000  # > 1023
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((HOST, PORT))
lsock.listen()
print("Escuchando en", (HOST, PORT))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)
while True:
    events = sel.select(timeout=None)
    for cliente, accionRW in events:
        if cliente.data is None:
            accept_wrapper(cliente.fileobj)
        else:
            service_connection(cliente, accionRW)
