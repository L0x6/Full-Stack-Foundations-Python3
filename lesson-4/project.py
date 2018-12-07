from flask import Flask, render_template, redirect, request , url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from database_setup import Restaurant, MenuItem, Base

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

############# # fixing same thread id problem

session = scoped_session(sessionmaker(bind=engine))

'''
DBSession = sessionmaker(bind=engine)
session = DBSession()
'''
##########

app=Flask(__name__)

# fixing same thread id problem 
@app.teardown_request
def remove_session(ex=None):
    session.remove()

#============#APIs functions here#============#
# API list all Restaurants (GET request)
@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants= session.query(Restaurant).all()
    
    return jsonify( restaurants_List=[r.serialize for r in restaurants] )


# API list all menu (GET request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    #restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id ).all()
    return jsonify( MenuItems=[i.serialize for i in items] )

# API menu (GET request)
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def MenuJSON(restaurant_id,menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id ).one()
    return jsonify( MenuItem=[item.serialize] )

#============#EO_APIs#============#
#
#
#
#============#Restaurants Functions here#============#

#route for restaurants List  function here
@app.route('/')
@app.route('/restaurants/')
def restaurants():
    restaurants = session.query(Restaurant).all()    
    return render_template('restaurants.html', restaurants= restaurants)

#route for New restaurant function here 
@app.route('/restaurants/new/', methods=['GET','POST'])
def newRestaurant():
    if request.method== 'POST' :
        if request.form['name']:
            newRestaurant= Restaurant (name= request.form['name'])
            session.add(newRestaurant)
            session.commit()
            flash("new Restaurant added! oh yeah!")
        return redirect(url_for('restaurants'))
    else:
        return render_template('newrestaurant.html')

#route for edit restaurant name function here 
@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET','POST'])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method== 'POST' :
        if request.form['name']:
            oldRestaurantName=restaurant.name        
            restaurant.name= request.form['name']        
            session.add(restaurant)
            session.commit()
            flash("restaurant %s changed to %s" %oldRestaurantName %restaurant.name )    
        return redirect(url_for('restaurants'))
    else:
        return render_template('editrestaurant.html', restaurant=restaurant, restaurant_id= restaurant_id)

#route for delete restaurant function here // TODO 
@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()    
    if request.method== 'POST' :
        items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
        for item in items:
            session.delete(item)
        session.delete(restaurant)
        session.commit()
        flash("restaurant %s deleted (along with its menu)" %restaurant.name )    
        return redirect(url_for('restaurants'))
    else:
        return render_template('deleterestaurant.html', restaurant= restaurant, restaurant_id= restaurant_id)

#============#EO_Restaurants Functions#============#
#
#
#
#============#Menus Functions here#============#
#route for restaurant Menu function here
@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id )

    return render_template('menu.html', restaurant= restaurant, items = items)

#route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method== 'POST' :
        if request.form['name']:
            newItem= MenuItem (name= request.form['name'], description= request.form['description'], price= request.form['price'], course= request.form['course'], restaurant_id=restaurant.id)
            session.add(newItem)
            session.commit()
            flash("new menu added! oh yeah!")
        return redirect(url_for('restaurantMenu',restaurant_id= restaurant.id))
    else:
        return render_template('newmenuitem.html',restaurant=restaurant, restaurant_id=restaurant.id)

#route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menu/edit/<int:menu_id>/', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    editItem= session.query(MenuItem).filter_by(id= menu_id).one()
    if request.method== 'POST' :
        if request.form['name']:        
            editItem.name= request.form['name']
        if request.form['description']:
            editItem.description= request.form['description']
        if request.form['course']:
            editItem.price= request.form['course']            
        if request.form['price']:
            editItem.price= request.form['price']            
        session.add(editItem)
        session.commit()
        flash("menu %s edited" % editItem.name)
        return redirect(url_for('restaurantMenu',restaurant_id= restaurant_id))
    else:
        return render_template('editmenuitem.html',restaurant=restaurant, editItem=editItem, restaurant_id=restaurant.id, menu_id=editItem.id)

        
#route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menu/delete/<int:menu_id>/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    deleteItem= session.query(MenuItem).filter_by(id= menu_id).one()
    if request.method == 'POST' :
        item_name = deleteItem.name
        session.delete(deleteItem)
        session.commit()
        flash("menu %s deleted" % item_name)
        return redirect(url_for('restaurantMenu',restaurant_id= restaurant.id))
    else:
        return render_template('deletemenuitem.html',restaurant=restaurant, deleteItem=deleteItem, restaurant_id=restaurant.id, menu_id=deleteItem.id)

#============#EO_Menus Functions#============#
    

if __name__ == '__main__':

    app.secret_key="suppppper nani"
    app.debug=True
    app.run(host = '0.0.0.0', port = 5000)

    
