import http.server
import socketserver

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    password = "my_password"

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'image/jpeg')
        self.end_headers()

    def do_GET(self):
        if self.headers.get('password') != self.password:
            self.send_response(401)
            self.end_headers()
        else:
            self.do_HEAD()
            with open('/srv/tftp/charley/uRamdisk.img', 'rb') as f:
                self.wfile.write(f.read())

PORT = 8000

Handler = RequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.serve_forever()


'''
On client side, the following command will be used:
wget  --tries=3 --limit-rate 60k --header="password: my_password" http://192.168.103.1:8000/srv/tftp/charley/uRamdisk.img
'''