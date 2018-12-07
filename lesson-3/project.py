from flask import Flask, render_template, redirect, request , url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, MenuItem, Base

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app=Flask(__name__)

# API (GET request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    #restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id ).all()
    return jsonify( MenuItems=[i.serialize for i in items] )

# API (GET request)
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def MenuJSON(restaurant_id,menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id ).one()
    return jsonify( MenuItem=[item.serialize] )


@app.route('/')
@app.route('/restaurants/')
def restaurants():
    restaurants = session.query(Restaurant).all()    
    return render_template('restaurants.html', restaurants= restaurants)


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id )

    return render_template('menu.html', restaurant= restaurant, items = items)

# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET','POST'])
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

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/edit/<int:menu_id>/', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    editItem= session.query(MenuItem).filter_by(id= menu_id).one()
    if request.method== 'POST' :
        if request.form['name']:        
            editItem.name= request.form['name']
            edited=True
        if request.form['description']:
            editItem.description= request.form['description']
            edited=True
        if request.form['course']:
            editItem.price= request.form['course']
            edited=True
        if request.form['price']:
            editItem.price= request.form['price']
            edited=True
        
        session.add(editItem)
        session.commit()
        flash("menu %s edited" % editItem.name)
        return redirect(url_for('restaurantMenu',restaurant_id= restaurant_id))
    else:
        return render_template('editmenuitem.html',restaurant=restaurant, editItem=editItem, restaurant_id=restaurant.id, menu_id=editItem.id)

        
# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/delete/<int:menu_id>/', methods=['GET','POST'])
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
    


if __name__ == '__main__':
    app.secret_key="suppppper nani"
    app.debug=True
    app.run(host = '0.0.0.0', port = 5000)
    

