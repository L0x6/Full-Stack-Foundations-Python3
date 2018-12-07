from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
#import cgitb
#cgitb.enable()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, MenuItem, Base

########### initiating the database: create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling 
# session.rollback()
session = DBSession()


    
class  webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()

                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                
                output= ""
                output += "<html><body>"
                output += "<h1>All the Restaurants in the world (^_^)</h1>"
                output += "<h1><a href='/restaurants/new'>Click here</a> to add new restaurant</h1>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href=/restaurants/%s/edit>EDIT</a>"% restaurant.id 
                    output += "</br>"
                    output += "<a href=/restaurants/%s/delete >DELETE</a>" % restaurant.id
                    output += "</br>=======</br>"
                output += "</body></html>"

                self.wfile.write(bytes(output,'utf-8'))
                print (output)
                return

            elif self.path.endswith("/restaurants/new"):
                restaurants = session.query(Restaurant).all()

                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                
                output= ""
                output += "<html><body>"
                output += "<h1> New Restaurant (*_*)</h1>"
                output += " <form method='POST' enctype='multipart/form-data' action='/restaurants/new'> <h2> Make a new restaurant </h2> <input name='newRestaurantName' type='text'> <input type='submit' value='Create'> </form>"

                output += "</body></html>"
                self.wfile.write(bytes(output,'utf-8'))
                print (output)
                return

            elif self.path.endswith("/edit"):
                print(self.path)
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery= session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                
                if myRestaurantQuery != [] :
                    self.send_response(200)
                    self.send_header('Content-type','text/html')
                    self.end_headers()
                
                    output= ""
                    output += "<html><body>"
                    output += "<h1> EDIT %s </h1>"% myRestaurantQuery.name
                    output += " <form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurantIDPath
                    output += " <input name='newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
                    output += "<input type='submit' value='Rename'> "
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(bytes(output,'utf-8'))
                    #print (output)
                
            elif self.path.endswith("/delete"):
                print(self.path)
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery= session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                
                if myRestaurantQuery != [] :
                    self.send_response(200)
                    self.send_header('Content-type','text/html')
                    self.end_headers()
                
                    output= ""
                    output += "<html><body>"
                    output += "<h1> Deleting %s </h1>"% myRestaurantQuery.name
                    output += " <form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurantIDPath
                    output += "<input type='submit' value='Delete'> "
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(bytes(output,'utf-8'))
                    #print (output)


                  

            else : 
                self.send_error(404, "File Not Found %s" % self.path)
                return
        except IOError:
                self.send_error(404, "File Not Found %s" % self.path)
    
    def do_POST(self):
        try:

            if self.path.endswith("/edit"):
                
            # HEADERS are in dict/json style container
                ctype, pdict = cgi.parse_header(self.headers['Content-type'])
                       
            # boundary data needs to be encoded in a binary format
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if myRestaurantQuery != []:
                    myRestaurantQuery.name = messagecontent[0].decode()
                    session.add(myRestaurantQuery)
                    session.commit()
                    self.send_response(301) 
                self.send_header('Content-type','text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()

            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()            
                if myRestaurantQuery != []:                    
                    session.delete(myRestaurantQuery)
                    session.commit()
                    self.send_response(301) 
                self.send_header('Content-type','text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()



            if self.path.endswith("/restaurants/new"):
                self.send_response(301)
            
            # HEADERS are in dict/json style container
                ctype, pdict = cgi.parse_header(self.headers['Content-type'])
                       
            # boundary data needs to be encoded in a binary format
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    #print ("\n user wrote : ", messagecontent[0])
            
                newRestaurantName=messagecontent[0].decode()
                restaurant_new = Restaurant(name=newRestaurantName)
                session.add(restaurant_new)
                session.commit()

                self.send_header('Content-type','text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()

            

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
