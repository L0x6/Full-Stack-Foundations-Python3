from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

import cgitb
cgitb.enable()


class  webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                
                output= ""
                output += "<html><body>"
                output += "Hello First Server"
                output += " <form method='POST' enctype='multipart/form-data' action='/hello'> <h2> what would you want me to say? </h2> <input name='message' type='text'> <input type='submit' value='Submit'> </form>"
                output += "</body></html>"
                #self.wfile.write(output) #python 2 code
                self.wfile.write(bytes(output,'utf-8')) #python3 treats it as bytes
                print (output)
                return

            elif self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                
                output = ""
                output += "<html><body>" 
                output += "Hello admin hola <a href='/hello'>back</a>"
                output += " <form method='POST' enctype='multipart/form-data' action='/hello'> <h2> what would you want me to say? </h2> <input name='message' type='text'> <input type='submit' value='Submit'> </form>"

                output += "</body></html>"
                
                self.wfile.write(bytes(output,'utf-8')) 
                print (output)
                return

            else : 
                self.send_error(404, "File Not Found %s" % self.path)
                return
        except IOError:
                self.send_error(404, "File Not Found %s" % self.path)
    
    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type','text/html')
            self.end_headers()
            
            # HEADERS are in dict/json style container
            ctype, pdict = cgi.parse_header(self.headers['Content-type'])
                       
            # boundary data needs to be encoded in a binary format
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
                #print ("\n user wrote : ", messagecontent[0])
            
            output= ""
            output += "<html><body>"
            output += " <h2> okay, how about this: </h2>"            
            output += " <h1> {} </h1>".format(messagecontent[0].decode())

            output += " <form method='POST' enctype='multipart/form-data' action='/hello'> <h2> what would you want me to say? </h2> <input name='message' type='text'> <input type='submit' value='Submit'> </form>"

            output += "</body></html>"
            
            self.wfile.write(bytes(output,'utf-8'))
            print (output)


        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webserverHandler)
        print ("Web server runiing on port {}".format(port))
        server.serve_forever()
        
    except KeyboardInterrupt:
        print ("\n^C entered, stopping web server...")
        server.socket.close()

if __name__== '__main__':
    main()
