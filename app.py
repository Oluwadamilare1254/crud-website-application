from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from db_config import db_config

app = Flask(__name__)
app.config.update(db_config)

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM items")
    items = cur.fetchall()
    cur.close()
    return render_template('index.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO items (name, quantity, price) VALUES (%s, %s, %s)", (name, quantity, price))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    return render_template('add_items.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        cur.execute("UPDATE items SET name=%s, quantity=%s, price=%s WHERE id=%s", (name, quantity, price, id))
        mysql.connection.commit()
        return redirect(url_for('index'))

    cur.execute("SELECT * FROM items WHERE id=%s", [id])
    item = cur.fetchone()   
    return render_template('edit.html', item=item)

@app.route('/delete/<int:id>')
def delete_item(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM items WHERE id=%s", [id])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)