from flask import Flask, render_template, redirect, url_for, request, session
from flask_cors import CORS
from common import database
from werkzeug.utils import secure_filename
from modules.animal import Animal
import os
import uuid
import random

UPLOAD_FOLDER = './static/uploads'

app = Flask(__name__)
app.secret_key = 'ufvowevgouwveougvweoivg30808213tifg20v8g0'
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = database.Database()
db.initialize()
@app.route("/")
def main():
    results = db.search([None, None])
    results = random.sample(results, 2)
    if 'username' not in session:
        return render_template('home-multipage.html', results=results)
    else:
        print(isAdmin)
        return render_template('home-multipage.html', user=session['username'], isAdmin=session['isAdmin'], results=results)


@app.route('/signup',  methods=['GET', 'POST'])
def signup():
    #[fname, lname, email, pnumber, username, password]
    error = None
    if 'username' in session:
        results = db.search([None, None])
        results = random.sample(results, 2)
        return render_template('home-multipage.html', user=session['username'], results=results)
        
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        pnumber = request.form['pnumber']
        username = request.form['username']
        password = request.form['password']
        results = db.search([None, None])
        results = random.sample(results, 2)
        if db.create_user(username, password, fname, lname, pnumber,email):
           session['username'] = request.form['username']
           return render_template('home-multipage.html', user=session['username'], results=results)
        else:
            error = "Database Error occured" 
   # remove the username from the session if it is there
    return render_template('signup.html', error=error)

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if 'username' in session:
        results = db.search([None, None])
        results = random.sample(results, 2)
        if session['isAdmin']:
            return render_template('home-multipage.html', user=session['username'], isAdmin=session['isAdmin'], results=results)
        return render_template('home-multipage.html', user=session['username'], results=results)
    error = None
    if request.method == 'POST':
        print(request.form['username'])
        if db.is_user(request.form['username']):
            user = db.get_user(request.form['username'])
            print(user)
            if user['Password'] == request.form['password']:
                session['username'] = request.form['username']
                session['isAdmin'] = user['isAdmin']
                print(session['isAdmin'])
                session['fname'] = user['First_name']
                session['user_id'] = user['profile_id']
                results = db.search([None, None])
                results = random.sample(results, 2)
                if session['isAdmin']:
                    return render_template('home-multipage.html', user=session['username'], isAdmin=session['isAdmin'], results=results)
                return render_template('home-multipage.html', user=session['username'], isAdmin=session['isAdmin'], results=results)
            else:
                error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'username' in session and session['isAdmin']:
        donations = db.get_donation_sum()
        adoptions = db.get_total_adoptions()
        return render_template('admin/index.html', user=session['fname'], donations=donations, adoptions=adoptions)
    else:
        return render_template('home-multipage.html', user=session['username'])


@app.route('/admin/animals', methods=['GET', 'POST'])
def animals():
    if 'username' in session and session['isAdmin'] and request.method == 'GET':
        breeds = db.get_breeds()
        return render_template('admin/add_animal.html', options=breeds, user=session['fname'])
    elif request.method == 'GET':
        return render_template('home-multipage.html', user=session['username'])

    if request.method == 'POST' and session['isAdmin']:
        filename = None
        # Will save the pet image if we have one with a unique name
        if 'file' in request.files:
            file = request.files['file']
            _, file_extension = os.path.splitext(file.filename)
            filename = str(uuid.uuid4())+file_extension
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        name = request.form['name']
        age = request.form['age']
        animal_type = request.form['type']
        color = request.form['color']
        availability = request.form['availability']
        size = request.form['size']
        breed = request.form['breed']
        description = request.form['description']
        adoption_fee = request.form['adoption_fee']
        if db.new_animal(name, age, animal_type, color, availability, size, breed, description, filename, adoption_fee):
            breeds = db.get_breeds()
            return render_template('admin/add_animal.html', options=breeds, msg="Added successfully", user=session['fname'])
        else:
            breeds = db.get_breeds()
            return render_template('admin/add_animal.html', options=breeds, error="Something went wrong", user=session['fname'])

@app.route('/admin/animals/delete', methods=['GET', 'POST'])
def delete_animal():
    if 'username' in session and session['isAdmin'] and request.method == 'GET':
        animals = db.get_animals()
        return render_template('admin/delete_animal.html', options=animals, user=session['fname'])
    elif request.method == 'GET':
        return render_template('home-multipage.html', user=session['username'])

    if request.method == 'POST' and session['isAdmin']:
        animal = request.form['animal']
        animal_id = animal.split(",")
        if db.delete_animal(animal_id[0]):
            animals = db.get_animals()
            return render_template('admin/delete_animal.html', msg="Deleted successfully", options=animals)
        else:
            animals = db.get_animals()
            return render_template('admin/delete_animal.html', error="Something went wrong", options=animals)


@app.route('/admin/animals/edit', methods=['GET', 'POST'])
def edit_animal():
    if 'username' in session and session['isAdmin'] and request.method == 'GET':
        animals = db.get_animals()
        return render_template('admin/edit_animal.html', options=animals, view_form=False, init=True, user=session['fname'])
    elif request.method == 'GET':
        return render_template('home-multipage.html', user=session['username'])

    if request.method == 'POST' and session['isAdmin']:
        if 'tag' in request.form:
            animal = request.form['animal']
            animal_id = animal.split(",")
            animal_dict = db.get_one_animal(animal_id[0])
            animal_attr = animal_dict.split(",")
            print(animal_attr)
            adoption_fee = db.get_one_adoption_fee(animal_id[0])
            animal_attr.append(adoption_fee)
            anim = Animal(animal_attr)
            session['animalId'] = anim.id
            session['animalImage'] = anim.image
            session['date'] = anim.date
            breeds = db.get_breeds()
            return render_template('admin/edit_animal.html', options=breeds, view_form=True, animal=anim, init=False, user=session['fname'])
        else:
            name = request.form['name']
            age = request.form['age']
            animal_type = request.form['type']
            color = request.form['color']
            availability = request.form['availability']
            size = request.form['size']
            breed = request.form['breed']
            description = request.form['description']
            adoption_fee = request.form['adoption_fee']

            if db.edit_animal(session['animalId'], name, age, animal_type, color, availability, size, breed, description, session['animalImage'], session['date'], adoption_fee):
                return render_template('admin/edit_animal.html', msg="Updated successfully", view_form=False, init=False, user=session['fname'])
            else:
                return render_template('admin/edit_animal.html', msg="Something went wrong", view_form=False, init=False, user=session['fname'])

@app.route('/admin/donation/byuser', methods=['GET', 'POST'])
def donation_user():
    if 'username' in session and session['isAdmin'] and request.method == 'GET':
        users = db.get_all_user()
        print(users)
        all_usernames = []
        for user in users:
            all_usernames.append(user['Username'])
        return render_template('admin/donation_user.html', options=all_usernames, view_table=False, init=True, user1=session['fname'])
    elif request.method == 'GET':
        return render_template('home-multipage.html', user=session['username'])
    
    if request.method == 'POST' and session['isAdmin']:
        if 'tag' in request.form:
            username = request.form['user']
            print(username)
            info = db.get_donation_byuser(username)
            print(info)
            return render_template('admin/donation_user.html', info=info, user=username, view_table=True, init=False, user1=session['fname'])

@app.route('/admin/donation/bydate', methods=['GET', 'POST'])
def donation_date():
    if 'username' in session and session['isAdmin'] and request.method == 'GET':
        users = db.get_all_user()
        all_usernames = []
        for user in users:
            all_usernames.append(user['Username'])
        return render_template('admin/donation_date.html', options=all_usernames, view_table=False, init=True, user1=session['fname'])
    elif request.method == 'GET':
        return render_template('home-multipage.html', user=session['username'])


    if request.method == 'POST' and session['isAdmin']:
        if 'tag' in request.form:
            date = request.form['date']
            print(date)
            info = db.get_donation_bydate(date)
            return render_template('admin/donation_date.html', info=info, user=date, view_table=True, init=False, user1=session['fname'])

@app.route('/admin/adoptions', methods=['GET', 'POST'])
def adoptions():
    
    if 'username' in session and session['isAdmin'] and request.method == 'GET':
        users = db.get_all_user()
        all_usernames = []
        for user in users:
            all_usernames.append(user['Username'])
        return render_template('admin/adoption_user.html', options=all_usernames, view_table=False, init=True, user1=session['fname'])
    elif request.method == 'GET':
        return render_template('home-multipage.html', user=session['username'])
    
    if request.method == 'POST' and session['isAdmin']:
        if 'tag' in request.form:
            username = request.form['user']
            info = db.get_adoption_byuser(username)
            return render_template('admin/adoption_user.html', info=info, user=username, view_table=True, init=False, user1=session['fname'])
    return "Something went wrong"

@app.route('/admin/inquiries', methods=['GET', 'POST'])
def inquiries():
    if 'username' in session and session['isAdmin'] and request.method == 'GET':
        animals = db.get_animals()
        return render_template('admin/inquiries_animal.html', options=animals, view_table=False, init=True, user=session['fname'])
    elif request.method == 'GET':
        return render_template('home-multipage.html', user=session['username'])
    
    if request.method == 'POST' and session['isAdmin']:
        if 'tag' in request.form:
            animal = request.form['animal']
            animal_info = animal.split(',')
            animal_id = animal_info[0]
            print(animal_id)
            info = db.get_inquiries_byanimal(animal_id)
            return render_template('admin/inquiries_animal.html', info=info, animal=animal_info[1], view_table=True, init=False, user=session['fname'])


@app.route('/admin/inquiries/<string:id>', methods=['GET', 'POST'])
def inquiries_by_id(id):
    print("in here")
    print(id)
    if 'username' in session and session['isAdmin'] and request.method == 'GET':
        return render_template('admin/inquiries_animal_reply.html', id=id, user=session['fname'])
    elif request.method == 'GET':
        return render_template('home-multipage.html', user=session['username'])
    
    if request.method == 'POST' and session['isAdmin']:
        message = request.form['reply']
        if db.reply_inquiry(id, message):
            return render_template('admin/inquiries_animal_reply.html', msg="Replied successfully", user=session['fname'])
        return render_template('admin/inquiries_animal_reply.html', error="Error while Replying", user=session['fname'])

@app.route('/pet_info/<string:id>')
def pet_info(id):
    animal = db.get_one_animal(id)
    animal_info = animal.split(",")
    breed = db.get_one_breed(animal_info[9])
    adoption_fee = db.get_one_adoption_fee(animal_info[0])
    animal_dict = {
        'animal_id': animal_info[0],
        'name': animal_info[1],
        'age': animal_info[2],
        'type': animal_info[3],
        'color': animal_info[4],
        'ava':animal_info[5],
        'size':animal_info[6],
        'desc':animal_info[7],
        'date':animal_info[8],
        'breed':breed,
        'image':animal_info[10],
        'adoption_fee': adoption_fee
    }
    print(animal_dict)
    if 'username' in session and request.method == 'GET':
        if session['isAdmin']:
            print("in pet info admin")
            return render_template('temp.html', info=animal_dict, user=session['username'], isAdmin=session['isAdmin'], isAva=animal_dict['ava'])
        else:
            return render_template('temp.html', info=animal_dict, user=session['username'], isAva=animal_dict['ava'])
    else:
        return render_template('temp.html', info=animal_dict, isAva=animal_dict['ava'])

@app.route('/pet_info/donate', methods=['GET','POST'])
def pet_donate():
    if 'username' in session and request.method == 'POST':
        amount = request.form['donation_amaount']
        animal_id = request.form['animal_id']
        user_id = session['user_id']
        animal = db.get_one_animal(animal_id)
        animal_info = animal.split(",")
        breed = db.get_one_breed(animal_info[9])
        adoption_fee = db.get_one_adoption_fee(animal_info[0])
        animal_dict = {
            'animal_id': animal_info[0],
            'name': animal_info[1],
            'age': animal_info[2],
            'type': animal_info[3],
            'color': animal_info[4],
            'ava':animal_info[5],
            'size':animal_info[6],
            'desc':animal_info[7],
            'date':animal_info[8],
            'breed':breed,
            'image':animal_info[10],
            'adoption_fee': adoption_fee
        }
        if db.make_donation(animal_id, user_id, amount):
            if session['isAdmin']:
                return render_template('temp.html', info=animal_dict, user=session['username'], isAdmin=session['isAdmin'], msg="Thank your for your donation", isAva=animal_dict['ava'])
            else:
                return render_template('temp.html', info=animal_dict, user=session['username'], msg="Thank your for your donation", isAva=animal_dict['ava'])
        else:
            if session['isAdmin']:
                return render_template('temp.html', info=animal_dict, user=session['username'], isAdmin=session['isAdmin'], msg="Something went wrong", isAva=animal_dict['ava'])
            else:
                return render_template('temp.html', info=animal_dict, user=session['username'], msg="Something went wrong", isAva=animal_dict['ava'])
    else:
        return "You need to be Signed In as a user to make a donation"



@app.route('/pet_info/inquiry', methods=['GET','POST'])
def pet_inquiry():
    if 'username' in session and request.method == 'POST':
        message = request.form['message']
        print("message")
        animal_id = request.form['animal_id']
        print("animal_id")
        user_id = session['user_id']
        animal = db.get_one_animal(animal_id)
        animal_info = animal.split(",")
        breed = db.get_one_breed(animal_info[9])
        adoption_fee = db.get_one_adoption_fee(animal_info[0])
        animal_dict = {
            'animal_id': animal_info[0],
            'name': animal_info[1],
            'age': animal_info[2],
            'type': animal_info[3],
            'color': animal_info[4],
            'ava':animal_info[5],
            'size':animal_info[6],
            'desc':animal_info[7],
            'date':animal_info[8],
            'breed':breed,
            'image':animal_info[10],
            'adoption_fee': adoption_fee
        }
        print(animal_dict)
        if db.make_inqury(animal_id, user_id, message):
            if session['isAdmin']:
                return render_template('temp.html', info=animal_dict, user=session['username'], isAdmin=session['isAdmin'], msg="Thank your message has been sent", isAva=animal_dict['ava'])
            else:
                return render_template('temp.html', info=animal_dict, user=session['username'], msg="Thank your message has been sent", isAva=animal_dict['ava'])
        else:
            if session['isAdmin']:
                return render_template('temp.html', info=animal_dict, user=session['username'], isAdmin=session['isAdmin'], msg="Something went wrong", isAva=animal_dict['ava'])
            else:
                return render_template('temp.html', info=animal_dict, user=session['username'], msg="Something went wrong", isAva=animal_dict['ava'])
    else:
        return "You need to be Signed In as a user to make a inquiry"

@app.route('/pet_info/adopt', methods=['GET','POST'])
def pet_adopt():
    if 'username' in session and request.method == 'POST':
        adoption_fee = request.form['adoption_fee']
        animal_id = request.form['animal_id']
        user_id = session['user_id']
        print("In here at per adopt")
        if db.adopt(animal_id, user_id, adoption_fee):
            animal = db.get_one_animal(animal_id)
            animal_info = animal.split(",")
            breed = db.get_one_breed(animal_info[9])
            animal_dict = {
                'animal_id': animal_info[0],
                'name': animal_info[1],
                'age': animal_info[2],
                'type': animal_info[3],
                'color': animal_info[4],
                'ava':animal_info[5],
                'size':animal_info[6],
                'desc':animal_info[7],
                'date':animal_info[8],
                'breed':breed,
                'image':animal_info[10],
                'adoption_fee': adoption_fee
            }
            if session['isAdmin']:
                return render_template('temp.html', info=animal_dict, user=session['username'], isAdmin=session['isAdmin'], msg="Thank your message has been sent", isAva=animal_dict['ava'])
            else:
                return render_template('temp.html', info=animal_dict, user=session['username'], msg="Thank your message has been sent", isAva=animal_dict['ava'])
        else:
            animal = db.get_one_animal(animal_id)
            animal_info = animal.split(",")
            breed = db.get_one_breed(animal_info[9])
            animal_dict = {
                'animal_id': animal_info[0],
                'name': animal_info[1],
                'age': animal_info[2],
                'type': animal_info[3],
                'color': animal_info[4],
                'ava':animal_info[5],
                'size':animal_info[6],
                'desc':animal_info[7],
                'date':animal_info[8],
                'breed':breed,
                'image':animal_info[10],
                'adoption_fee': adoption_fee
            }
            if session['isAdmin']:
                return render_template('temp.html', info=animal_dict, user=session['username'], isAdmin=session['isAdmin'], msg="Thank your message has been sent", isAva=animal_dict['ava'])
            else:
                return render_template('temp.html', info=animal_dict, user=session['username'], msg="Thank your message has been sent", isAva=animal_dict['ava'])
    else:
        return "You need to be Signed In as a user to make a adoption"

@app.route('/browse/', methods=['GET','POST'])
def search():
    breeds = db.get_breeds()
    if request.method == 'POST':
        filters = []
        breed = request.form['breed']
        animal_type = request.form['type']
        if breed != 'Any':
            filters.append(breed)
        else:
            filters.append(None)
        if animal_type != 'Any':
            filters.append(animal_type)
        else:
            filters.append(None)
        results = db.search(filters)
        print("Search, POST")
        print(results)
        print(len(results))
        return render_template('browse.html', breeds=breeds, results=results, num=len(results))
    else:
         results = db.search([None, None])
         print("Search, GET")
         print(results)
         print(len(results))
         return render_template('browse.html', breeds=breeds, results=results, num=len(results))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect("/")
if __name__ == "__main__":
    app.run()