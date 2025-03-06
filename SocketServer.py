import socket
import http.server
import threading

DATA_FILE = "data.txt"

# Función para manejar el servidor de sockets
def socket_server():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(("0.0.0.0", 12345))
  s.listen(5)
  print("Servidor de sockets esperando conexiones en el puerto 12345...")

  while True:
    conn, addr = s.accept()
    data = conn.recv(1024).decode()
    print(f"Datos recibidos: {data}")
    with open(DATA_FILE, "w") as f:
      f.write(data)
    conn.close()

# Servidor HTTP simple
class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
  def do_GET(self):
    if self.path == "/data":
      try:
        with open(DATA_FILE, "r") as f:
          content = f.read()
      except FileNotFoundError:
        content = "Esperando datos..."
      self.send_response(200)
      self.send_header("Content-type", "text/plain")
      self.end_headers()
      self.wfile.write(content.encode())
    else:
      super().do_GET()

# Iniciar servidores en hilos diferentes
if __name__ == "__main__":
  threading.Thread(target=socket_server, daemon=True).start()
  
  httpd = http.server.ThreadingHTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler)
  print("Servidor web en http://localhost:8000")
  httpd.serve_forever()
