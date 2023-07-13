from flask import Flask, request, render_template, redirect
from datetime import datetime as dt
import sqlite3 as sql

class Library:
	def __init__(self):
		self.fine_amount = 5
		self.login_name = sql.connect('login.db')

app = Flask(__name__)
lib = Library()

def current_date():
	day = dt.now().strftime('%d')
	month = dt.now().strftime('%m')
	year = dt.now().strftime('%Y')
	string = year + '-' + month + '-' + day
	return string

def duration_count(last_date):
	start = dt.now()
	end = last_date.split('-')
	end = [int(i) for i in end]
	end = dt(end[0], end[1], end[2])
	days = str(end - start)
	if ',' not in days: days = 0
	else: days = int(days.split(',')[0].split(' ')[0])
	return days + 1

@app.route('/', methods = ['GET','POST'])
def bookstore(admin_name = ''):
	db = sql.connect('library.db')
	booklist = list(db.execute(f"SELECT * FROM BOOKS;"))
	if request.method == 'POST':
		attribute = request.form['search-by']
		value = request.form['search-value']
		if value == '': return render_template('library_store.html', totalList = booklist)
		booklist = list(db.execute(f"SELECT * FROM BOOKS WHERE {attribute} = '{value}';"))
	return render_template('library_store.html', totalList = booklist)

@app.route('/addbook', methods = ['GET','POST'])
def addbook():
	db = sql.connect('library.db')
	if request.method == 'POST':
		bookid = request.form['add-bookid']
		bookname = request.form['add-bookname']
		subject = request.form['add-subject']
		author = request.form['add-author']
		quantity = request.form['add-quantity']
		if '' in [bookid, bookname, subject, author, quantity]: return render_template('library_bookadd.html')
		quantity = int(quantity)
		inserted_id = list(db.execute("SELECT Book_ID from BOOKS;"))
		if (bookid,) not in inserted_id:
			db.execute(f"INSERT INTO BOOKS VALUES('{bookid}','{bookname}','{subject}','{author}',{quantity});")
			db.commit()
	return render_template('library_bookadd.html')

@app.route('/deletebook/<book_id>')
def deletebook(book_id):
	db = sql.connect('library.db')
	borrowers = list(db.execute(f"SELECT * FROM BORROWERS WHERE Book_ID = '{book_id}'"))
	if len(borrowers) != 0: 
		booklist = list(db.execute(f"SELECT * FROM BOOKS;"))
		return render_template('library_store.html', message = 'CANNOT DELETE BORROWED BOOK', totalList = booklist)
	db.execute(f"DELETE FROM BOOKS WHERE Book_ID = '{book_id}';")
	db.commit()
	return redirect('/')

@app.route('/updatebook/<book_id>', methods = ['GET','POST'])
def updatebook(book_id):
	db = sql.connect('library.db')
	data = list(db.execute(f"SELECT * FROM BOOKS WHERE Book_ID = '{book_id}';"))
	if request.method == 'POST':
		bookname = request.form['upd-bookname']
		subject = request.form['upd-subject']
		author = request.form['upd-author']
		quantity = request.form['upd-quantity']
		db.execute(f"""UPDATE BOOKS SET Book_Name = '{bookname}', Subject = '{subject}',
		Author = '{author}', Quantity = {quantity} WHERE Book_ID = '{book_id}';""")
		db.commit()
		return redirect('/')
	return render_template('library_bookupdate.html', data = data[0])

@app.route('/borrowers', methods = ['GET','POST'])
def borrowers():
	db = sql.connect('library.db')
	leftover = {}
	borrowerlist = list(db.execute(f"SELECT * FROM BORROWERS;"))
	for i in borrowerlist: leftover[i[4]] = duration_count(i[4])
	if request.method == 'POST':
		attribute = request.form['search-by']
		value = request.form['search-value']
		if value == '': return render_template('library_borrowers.html', totalList = borrowerlist, leftover = leftover)
		borrowerlist = list(db.execute(f"SELECT * FROM BORROWERS WHERE {attribute} = '{value}';"))
		return render_template('library_borrowers.html', totalList = borrowerlist, leftover = leftover)
	return render_template('library_borrowers.html', totalList = borrowerlist, leftover = leftover)

@app.route('/lendbook', methods = ['GET','POST'])
def lendbook():
	db = sql.connect('library.db')
	if request.method == 'POST':
		borrowerid = request.form['add-borrowerid']
		totalids = list(db.execute(f"SELECT Member_ID FROM MEMBERS;"))
		if (borrowerid,) not in totalids:
			return render_template('library_booklend.html', message = 'BORROWER ID IS NOT IN DATABASE')
		borrowertype = list(db.execute(f"SELECT Member_Type FROM MEMBERS WHERE Member_ID = '{borrowerid}';"))[0][0]
		bookid = request.form['add-bookid']
		bookids = list(db.execute(f"SELECT Book_ID FROM BOOKS;"))
		if (bookid,) not in bookids:
			return render_template('library_booklend.html', message = 'BOOK ID IS NOT IN DATABASE')
		issuedate = current_date()
		returndate = request.form['add-returndate']
		daysleft = duration_count(returndate)
		if daysleft >= 0: fine = 0
		else: fine = (-1 * daysleft * app.fine_amount)
		available_quantity = list(db.execute(f"SELECT Quantity FROM BOOKS WHERE Book_ID = '{bookid}';"))[0][0]
		db.execute(f"""INSERT INTO BORROWERS VALUES('{borrowerid}','{borrowertype}','{bookid}','{issuedate}','{returndate}',{fine});""")
		db.commit()
		db.execute(f"UPDATE BOOKS SET Quantity = {available_quantity - 1} WHERE Book_ID = '{bookid}'")
		db.commit()
		return render_template('library_booklend.html', message = 'ISSUE SUCCESSFUL')
	return render_template('library_booklend.html')

@app.route('/returned/<borrower_id> - <book_id>')
def returnbook(borrower_id, book_id):
	db = sql.connect('library.db')
	available_quantity = list(db.execute(f"SELECT Quantity FROM BOOKS WHERE Book_ID = '{book_id}';"))[0][0]
	db.execute(f"DELETE FROM BORROWERS WHERE Book_ID = '{book_id}' AND Borrower_ID = '{borrower_id}';")
	db.commit()
	db.execute(f"UPDATE BOOKS SET Quantity = {available_quantity + 1} WHERE Book_ID = '{book_id}'")
	db.commit()
	return redirect('/borrowers')

if __name__ == '__main__': app.run(debug = True)
