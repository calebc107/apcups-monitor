import base64
from http.server import HTTPServer,BaseHTTPRequestHandler
import apcaccess
import ssl

class APCStatusServerHandler(BaseHTTPRequestHandler):
    def do_HEAD(self,content_type="text/html"):
        self.send_response(200)
        self.send_header('Content-type',content_type)
        self.end_headers()
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate','Basic realm="APCStatusPage"')
        self.send_header("Content-type","application/json")
        self.end_headers()
        self.wfile.write("401 UNAUTHORIZED".encode("utf-8"))
    def do_GET(self):
        key = self.server.get_key()
        auth_header = self.headers.get('Authorization')
        if auth_header is None:
            self.do_AUTHHEAD()
        elif auth_header == "Basic "+str(key):
            path=self.path
            if path=="/":
                path="/index.html"
            if path=="/logout?":
                self.send_response(401)
                self.end_headers()
                return
            with open("http"+path,"r") as f:
                document = f.read()
            if "<maintable>" in document:
                maintable = ''
                status_dict = {"STATUS":"ONBATT"}#apcaccess.poll()
                maintable+="<table>"
                for key in status_dict:
                    maintable+="<tr><td>{}</td><td>{}</td></tr>".format(key,status_dict[key])
                maintable+=("</table>")
                document = document.replace("<maintable>",maintable)
            print("debug here")
            self.do_HEAD()
            self.wfile.write(document.encode('utf-8'))
        else:
            self.do_AUTHHEAD()

class APCStatusServer(HTTPServer):
    key=''
    def set_auth(self,username,password):
        self.key = str(base64.b64encode(bytes("{}:{}".format(username,password),"utf-8")),"ascii")
    def get_key(self):
        return self.key
if __name__ == "__main__":
    server = APCStatusServer(('',8080),APCStatusServerHandler)
    server.set_auth("user","password")
    server.socket = ssl.wrap_socket(server.socket,"key.pem","cert.pem",server_side=True)
    server.serve_forever()