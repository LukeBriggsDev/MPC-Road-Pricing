from http.server import HTTPServer,BaseHTTPRequestHandler
import subprocess
import re
import json

host = "127.0.0.1"
port = 7687

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf8")
        self.end_headers()
        output = subprocess.getoutput("./run_mpc.sh")
        is_in_bounds = re.search(r"Not in radius", output, re.MULTILINE) is None
        print(is_in_bounds)
        try:
            price = re.search(r"(?<=^Price: )([\d.\w]*)", output, re.MULTILINE).group()
            distance = re.search(r"(?<=^Distance: )([\d.\w]*)", output, re.MULTILINE).group()
        except AttributeError:
            price = None
            distance = re.search(r"(?<=^Distance: )([\d.\w]*)", output, re.MULTILINE).group()
        if is_in_bounds:
            response = {"price": price, "is_in_bounds": True, "distance": distance}
        else:
            response = {"is_in_bounds": False, "distance": distance}
        json_response = bytes(json.dumps(response), "utf-8")
        self.wfile.write(json_response)


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    httpd = HTTPServer((host, port), Server)
    print(f"Server started http://{host}:{port}")
    httpd.serve_forever()
    
if __name__ == "__main__":
    run()