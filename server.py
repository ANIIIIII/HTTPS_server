from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading
import logging
import time
import ssl

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

class Handler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print(threading.current_thread())
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        with open('./login.html', 'rb') as file: 
            self.wfile.write(file.read())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print(threading.current_thread())
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n", str(self.path), str(self.headers), post_data.decode('utf-8'))

        if('sign_up' in post_data.decode("utf-8")):
            tmp = post_data.decode('utf-8').split('&')
            username = tmp[0].split('=')[1]
            password = tmp[1].split('=')[1]
            htmlfile = './signupsuccess.html'
            with open('./accounts.txt', 'rb') as file:
                if (username == '') or (password == '') or (username + '$') in file.read().decode("utf-8"):
                    htmlfile = './signupfailed.html'
                    file.close()
                else:
                    file.close()
                    with open('./accounts.txt', 'a') as file:
                        file.write((username + '$' + password) + '\n')
                        file.close()
            self._set_response()
            with open(htmlfile, 'rb') as file:
                self.wfile.write(file.read())
                file.close()
        elif('sign_in' in post_data.decode("utf-8")):
            tmp = post_data.decode('utf-8').split('&')
            username = tmp[0].split('=')[1]
            password = tmp[1].split('=')[1]
            htmlfile = './signinfailed.html'
            with open('./accounts.txt', 'rb') as file:
                if username != '' and password != '' and (username + '$' + password) in file.read().decode("utf-8"):
                    htmlfile = './index.html'
                file.close()
            comment = ''
            with open('./comments.txt', 'r') as file:
                comment = file.read()
                file.close()
            self._set_response()
            with open(htmlfile, 'rb') as file:
                tmp = file.read().decode("utf-8").format(text=comment).encode()
                self.wfile.write(tmp)
                file.close()
        elif('comment' in post_data.decode("utf-8")):
            tmp = post_data.decode('utf-8').split('=')
            comment = tmp[1]
            with open('./comments.txt', 'a') as file:
                file.write(comment + '<br>\n')
                file.close()
            comment = ''
            with open('./comments.txt', 'r') as file:
                comment = file.read()
                file.close()

            self._set_response()
            with open('./index.html', 'rb') as file:
                self.wfile.write(file.read().decode("utf-8").format(text=comment).encode())
                file.close()
        else:
            self._set_response()
            with open('./error.html', 'rb') as file:
                self.wfile.write(file.read())
                file.close()

if __name__ == '__main__':
    with open('./accounts.txt', 'wb') as file:
        file.truncate()
        file.close()
    with open('./comments.txt', 'wb') as file:
        file.truncate()
        file.close()
    server = ThreadedHTTPServer(('', 8080), Handler)
    server.socket = ssl.wrap_socket(server.socket, certfile='./server.pem', server_side=True)
    print('start')
    server.serve_forever()
