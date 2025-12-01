from http.server import BaseHTTPRequestHandler, HTTPServer

class HoneypotHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # The fake content
        html = """
        <html>
        <head><title>Admin Panel v2.0</title></head>
        <body style="background-color:black; color:red; font-family:monospace;">
            <h1>⚠️ RESTRICTED ACCESS ⚠️</h1>
            <p>Enter Master Password to proceed.</p>
            <form><input type="password"><button>Login</button></form>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))
        print(f"🍯 HONEYPOT TRAPPED A VICTIM: {self.client_address[0]}")

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), HoneypotHandler)
    print("Honeypot Active on port 8000...")
    server.serve_forever()