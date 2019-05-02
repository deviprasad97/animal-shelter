import mysql.connector
import json
import time
import datetime
import uuid

class Database(object):
  mycursor = None
  mydb = mysql.connector.connect(
    host="localhost",
    port="8889",
    user="root",
    passwd="06811@mummy",
    database="animalshelter"
  )

  @staticmethod
  def initialize():
    Database.mycursor = Database.mydb.cursor(buffered=True)
    myresult = Database.mycursor.execute("SELECT User_id, username FROM User WHERE username='deviprasad'")
    print(myresult)
    myresult = Database.mycursor.fetchall()
    for x in myresult:
      print(x)


  @staticmethod
  def insert(table, data):
    pass
  
  @staticmethod
  def find(table, query):
    pass

  @staticmethod
  def find_one(table, query, key):
    Database.mycursor.execute("SELECT * FROM "+table+" WHERE "+key+"="+"'"+query+"'")
    myresult = Database.mycursor.fetchone()
    print(myresult)

  @staticmethod
  def get_user(username):
    user = {}
    Database.mycursor.execute("SELECT * FROM Profile WHERE Username=%s", (username,))
    row_headers=[x[0] for x in Database.mycursor.description] #this will extract row headers
    rv = Database.mycursor.fetchall()
    for index, header in enumerate(row_headers):
      print(rv[0][index])
      user[header] = rv[0][index]
    # Will check if user is admin or not
    Database.mycursor.execute("SELECT * FROM Admin WHERE Username=%s", (username,))
    msg = Database.mycursor.fetchone()
    if not msg:
      user['isAdmin'] = False
    else:
      user['isAdmin'] = True
    print(user)
    return user


  @staticmethod
  def get_user_by_id(id):
    user = {}
    Database.mycursor.execute("SELECT * FROM Profile WHERE profile_id=%s", (id,))
    row_headers=[x[0] for x in Database.mycursor.description] #this will extract row headers
    rv = Database.mycursor.fetchall()
    print(rv)
    for index, header in enumerate(row_headers):
      print(rv[0][index])
      user[header] = rv[0][index]
    return user


  @staticmethod
  def get_all_user():
    user = []
    Database.mycursor.execute("SELECT * FROM Profile")
    row_headers=[x[0] for x in Database.mycursor.description] #this will extract row headers
    rv = Database.mycursor.fetchall()
    row_count = Database.mycursor.rowcount
    for i in range(row_count):
      temp = {}
      for index, header in enumerate(row_headers):
        temp[header] = rv[i][index]
      user.append(temp)
    return user

  @staticmethod
  def is_user(username):
    Database.mycursor.execute(
        "SELECT Username FROM Profile WHERE Username = %s",(username,)
    )
    # gets the number of rows affected by the command executed
    row_count = Database.mycursor.rowcount
    print ("number of affected rows: {}".format(row_count))
    if row_count == 0:
        print ("It Does Not Exist")
        return False
    else:
      return True
  
  @staticmethod
  def create_user(username, password, fname, lname, pnumber, email):
    temp = time.strftime('%Y, %m, %d')
    date_split = temp.split(',')
    a = uuid.uuid4()
    profile_id = str(a)
    profile_id = profile_id[0:6]
    date = datetime.datetime(int(date_split[0]), int(date_split[1]), int(date_split[2]))
    date = str(date)
    date = date[0:10]
    isActive = '1'
    try:
      print(profile_id, fname, lname,username, email, password, pnumber, date)
      query = "INSERT INTO Profile (profile_id, First_name, Last_name, Username, Email, Password, Mobile_number, DateCreated, IsActive) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(profile_id, fname, lname,username, email, password, pnumber, date,isActive)
      query1 = "INSERT INTO User (User_id, Username) VALUES ('{}','{}')".format(profile_id, username)
      print(query)
      Database.mycursor.execute(query)
      Database.mycursor.execute(query1)
      Database.mydb.commit()
      print ("Record inserted successfully into python_users table")
      return True
    except mysql.connector.Error as error :
      Database.mydb.rollback() #rollback if any exception occured
      print("Failed inserting record into python_users table {}".format(error))
      return False

  @staticmethod
  def new_animal(name, age, animal_type, color, availability, size, breed, description, filename, adoption_fee):
    # will fetch the breed id for the breed that we got.
    Database.mycursor.execute("SELECT Breed_id FROM BREED where Breed=%s", (breed,))
    msg = Database.mycursor.fetchone()
    breed_id = msg[0]

    # Will create a unique animal id
    animal_id = str(uuid.uuid4())
    animal_id = animal_id[0:6]

    temp = time.strftime('%Y, %m, %d')
    date_split = temp.split(',')
    date = datetime.datetime(int(date_split[0]), int(date_split[1]), int(date_split[2]))
    date = str(date)
    date = date[0:10]

    query = "INSERT INTO ANIMAL (Animal_id, Name, Age, Type, Color, Availability, Size, Description, Ported_date, Breed_id, image) VALUES \
    ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')\
      ".format(animal_id, name, age, animal_type, color, availability, size, description, date, breed_id, filename)
    query1 = "INSERT INTO Adoption_fee (Animal_id, Adoption_fee) VALUES ('{}', '{}')".format(animal_id, adoption_fee)
    try:
      Database.mycursor.execute(query)
      Database.mydb.commit()
      print ("Record inserted successfully into ANIMAL table")
      Database.mycursor.execute(query1)
      Database.mydb.commit()
      print ("Record inserted successfully into Adoption_fee table")

    except mysql.connector.Error as error :
      Database.mydb.rollback() #rollback if any exception occured
      print("Failed inserting record into ANIMAL or Adoption_fee  table {}".format(error))
      return False
    return True
  
  @staticmethod
  def delete_animal(animal_id):
    query = "DELETE FROM ANIMAL WHERE Animal_id='{}'".format(animal_id)
    try:
      Database.mycursor.execute(query)
      Database.mydb.commit()
      print ("Record deleted successfully from ANIMAL table")
  
    except mysql.connector.Error as error :
      Database.mydb.rollback() #rollback if any exception occured
      print("Failed deleting record from ANIMAL table {}".format(error))
      return False
    return True

  @staticmethod
  def edit_animal(animal_id, name, age, animal_type, color, availability, size, breed, description, filename, date, adoption_fee):
    # will fetch the breed id for the breed that we got.
    Database.mycursor.execute("SELECT Breed_id FROM BREED where Breed=%s", (breed,))
    msg = Database.mycursor.fetchone()
    breed_id = msg[0]
    #sql = "UPDATE customers SET address = 'Canyon 123' WHERE address = 'Valley 345'"
    query = "UPDATE ANIMAL SET Name='{}', Age='{}', Type='{}', Color='{}', Availability='{}', Size='{}', Description='{}', Breed_id='{}', image='{}' WHERE \
    Animal_id='{}'".format(name, age, animal_type, color, availability, size, description, breed_id, filename, animal_id)
    query1 = "UPDATE Adoption_fee SET Adoption_fee='{}' where Animal_id='{}'".format(adoption_fee, animal_id)
    try:
      Database.mycursor.execute(query)
      Database.mydb.commit()
      print ("Record updated successfully into ANIMAL table")
      Database.mycursor.execute(query1)
      Database.mydb.commit()

    except mysql.connector.Error as error :
      Database.mydb.rollback() #rollback if any exception occured
      print("Failed updating record into ANIMAL or Adoption_fee table {}".format(error))
      return False
    return True
  
  @staticmethod
  def reply_inquiry(id, message):
    query = "UPDATE INQUIRIES SET Response='{}' WHERE Inquire_id='{}'".format(message, id)
    try:
      Database.mycursor.execute(query)
      Database.mydb.commit()
      print ("Record updated successfully into INQUIRIES table")

    except mysql.connector.Error as error :
      Database.mydb.rollback() #rollback if any exception occured
      print("Failed updating record into INQUIRIES table {}".format(error))
      return False
    return True
  @staticmethod
  def get_breeds():
    all_breeds = []
    Database.mycursor.execute("SELECT Breed FROM BREED")
    result_set = Database.mycursor.fetchall()
    for breed in result_set:
      all_breeds.append(breed[0])
    print(all_breeds)
    return all_breeds

  @staticmethod
  def get_one_adoption_fee(animal_id):
    query = "SELECT Adoption_fee FROM Adoption_fee where Animal_id='{}'".format(animal_id)
    Database.mycursor.execute(query)
    result_set = Database.mycursor.fetchone()
    return str(result_set[0])

  @staticmethod
  def get_one_breed(id):
    all_breeds = []
    print("Tag: Breed")
    print(id)
    query = "SELECT Breed FROM BREED where Breed_id='{}'".format(id)
    Database.mycursor.execute(query)
    result_set = Database.mycursor.fetchone()
    return str(result_set[0])

  @staticmethod
  def get_one_breed_id(breed):
    query = "SELECT Breed_id FROM BREED where Breed='{}'".format(breed)
    Database.mycursor.execute(query)
    result_set = Database.mycursor.fetchone()
    return str(result_set[0])


  @staticmethod
  def get_animals():
    all_animals = []
    Database.mycursor.execute("SELECT Animal_id, Name FROM ANIMAL")
    result_set = Database.mycursor.fetchall()
    for animal in result_set:
      temp = str(animal[0]) + "," + str(animal[1])
      all_animals.append(temp)
    return all_animals

  @staticmethod
  def get_one_animal(id):
    temp = None
    query = "SELECT * FROM ANIMAL where Animal_id='{}'".format(id)
    Database.mycursor.execute(query)
    result_set = Database.mycursor.fetchall()
    print(result_set)
    for animal in result_set:
      desc = animal[9]
      desc.replace("," , "")
      temp = str(animal[0]) + "," + str(animal[1]) + "," + str(animal[2]) + "," + str(animal[3]) + "," + str(animal[4])+ "," + str(animal[5])+ "," + str(animal[6])+ "," + str(animal[7])+ "," + str(animal[8])+ "," + str(animal[9])+ "," + str(animal[10])
    return temp

  @staticmethod
  def get_donation_byuser(username):
    info = []
    user = Database.get_user(username)
    user_id = user['profile_id']
    print("Tag: Database")
    print(user_id)
    query = "SELECT * FROM DONATIONS where User_id='{}'".format(user_id)
    Database.mycursor.execute(query)
    result_set = Database.mycursor.fetchall()
    for donation in result_set:
      animal_id = donation[1]
      donation_amount = donation[3]
      donation_date = donation[4]
      animal_info = Database.get_one_animal(animal_id)
      animal_name = None
      animal_age = None
      animal_type = None
      animal_size = None
      animal_info = animal_info.split(",")
      animal_name = animal_info[1]
      animal_age = animal_info[2]
      animal_type = animal_info[3]
      animal_size = animal_info[6]
      temp = {
        'name':animal_name,
        'age':animal_age,
        'type':animal_type,
        'size':animal_size,
        'amount':donation_amount,
        'donation_date':donation_date
      }
      info.append(temp)
    print(info)
    return info


  @staticmethod
  def get_donation_bydate(date):
    info = []
    query = "SELECT * FROM DONATIONS where donation_date='{}'".format(date)
    print("get_donation_bydate")
    print(query)
    Database.mycursor.execute(query)
    result_set = Database.mycursor.fetchall()
    print(result_set)
    for donation in result_set:
      animal_id = donation[1]
      donation_amount = donation[3]
      donation_date = donation[4]
      animal_info = Database.get_one_animal(animal_id)
      animal_info = animal_info.split(",")
      animal_name = animal_info[1]
      animal_age = animal_info[2]
      animal_type = animal_info[3]
      animal_size = animal_info[6]
      user_id = donation[0]
      user = Database.get_user_by_id(user_id)
      print(user)
      temp = {
        'name':animal_name,
        'age':animal_age,
        'type':animal_type,
        'size':animal_size,
        'amount':donation_amount,
        'donation_date':donation_date,
        'userfname': user['First_name'],
        'userlname': user['Last_name'],
        'email': user['Email'],
        'Mobile_number':user['Mobile_number']
      }
      info.append(temp)
    print(info)
    return info
  @staticmethod
  def get_adoption_byuser(username):
    info = []
    user = Database.get_user(username)
    user_id = user['profile_id']
    query = "SELECT * FROM ADOPTION where User_id='{}'".format(user_id)
    Database.mycursor.execute(query)
    result_set = Database.mycursor.fetchall()
    for donation in result_set:
      animal_id = donation[4]
      adoption_amount = donation[1]
      donation_date = donation[5]
      animal_info = Database.get_one_animal(animal_id)
      animal_name = None
      animal_age = None
      animal_type = None
      animal_size = None
      animal_info = animal_info.split(",")
      animal_name = animal_info[1]
      animal_age = animal_info[2]
      animal_type = animal_info[3]
      animal_size = animal_info[6]
      temp = {
        'animal_id': animal_id,
        'name':animal_name,
        'age':animal_age,
        'type':animal_type,
        'size':animal_size,
        'amount':adoption_amount,
        'adoption_date':donation_date
      }
      info.append(temp)
    print(info)
    return info


  @staticmethod
  def get_inquiries_byanimal(animalID):
    info = []
    animal = Database.get_one_animal(animalID)
    animal_info = animal.split(',')
    animal_id = animal_info[0]
    print(animal_id)
    query = "SELECT * FROM INQUIRIES where Animal_id='{}'".format(animal_id)
    Database.mycursor.execute(query)
    result_set = Database.mycursor.fetchall()
    for inquiry in result_set:
      user_id = inquiry[0]
      inquiry_id = inquiry[3]
      user = Database.get_user_by_id(user_id)
      message = inquiry[4]
      date = inquiry[6]

      temp = {
        'inquiry_id':inquiry_id,
        'userfname': user['First_name'],
        'userlname': user['Last_name'],
        'email': user['Email'],
        'Mobile_number':user['Mobile_number'],
        'animal_id':animalID,
        'animal_name':animal_info[1],
        'message':message,
        'adoption_date':date,
      }
      info.append(temp)
    print(info)
    return info

  @staticmethod
  def make_donation(animal_id, user_id, donation_amount):
    temp = time.strftime('%Y, %m, %d')
    date_split = temp.split(',')
    a = uuid.uuid4()
    donationID = str(a)
    donationID = donationID[0:6]
    date = datetime.datetime(int(date_split[0]), int(date_split[1]), int(date_split[2]))
    date = str(date)
    date = date[0:10]

    query = "INSERT INTO DONATIONS (User_id, Animal_id, DonationID, Amaount, donation_date) VALUES ('{}','{}','{}','{}','{}')".format(user_id, animal_id, donationID, donation_amount, date)
    try:
      Database.mycursor.execute(query)
      Database.mydb.commit()
      print ("Record inserted successfully into DONATION table")
      return True
    except mysql.connector.Error as error :
      Database.mydb.rollback() #rollback if any exception occured
      print("Failed inserting record into DONATION table {}".format(error))
      return False

  @staticmethod
  def make_inqury(animal_id, user_id, message):
    temp = time.strftime('%Y, %m, %d')
    date_split = temp.split(',')
    a = uuid.uuid4()
    Inquire_id = str(a)
    Inquire_id = Inquire_id[0:6]
    date = datetime.datetime(int(date_split[0]), int(date_split[1]), int(date_split[2]))
    date = str(date)
    date = date[0:10]
    admin = "1"
    response = " "
    query = "INSERT INTO INQUIRIES (User_id, Animal_id, Response, Inquire_id, Message, Assign_Admin_ID, date) VALUES ('{}','{}','{}','{}','{}','{}','{}')".format(user_id, animal_id, response, Inquire_id, message, admin, date)
    try:
      Database.mycursor.execute(query)
      Database.mydb.commit()
      print ("Record inserted successfully into INQUIRIES table")
      return True
    except mysql.connector.Error as error :
      Database.mydb.rollback() #rollback if any exception occured
      print("Failed inserting record into INQUIRIES table {}".format(error))
      return False

  @staticmethod
  def adopt(animal_id, user_id, adoption_fee):
    temp = time.strftime('%Y, %m, %d')
    date_split = temp.split(',')
    a = uuid.uuid4()
    Adoption_id = str(a)
    Adoption_id = Adoption_id[0:6]
    date = datetime.datetime(int(date_split[0]), int(date_split[1]), int(date_split[2]))
    date = str(date)
    date = date[0:10]
    Payment_method = "VISA"
    query = "INSERT INTO ADOPTION (Adoption_id, Adoption_fee, Payment_method, User_id, Animal_id, adoption_date) VALUES ('{}','{}','{}','{}','{}','{}')".format(Adoption_id, adoption_fee,Payment_method, user_id, animal_id, date)
    query1 = "UPDATE ANIMAL SET Availability='{}' where Animal_id='{}'".format('NO', animal_id)
    try:
      Database.mycursor.execute(query)
      Database.mydb.commit()
      print ("Record inserted successfully into INQUIRIES table")
      Database.mycursor.execute(query1)
      Database.mydb.commit()
      return True
    except mysql.connector.Error as error :
      Database.mydb.rollback() #rollback if any exception occured
      print("Failed inserting record into INQUIRIES or ANIMAL table {}".format(error))
      return False

  @staticmethod
  def search(filters):
    result = []
    breed = None
    animal_type = None
    if filters[0] is not None:
      breed = Database.get_one_breed_id(filters[0])
    if filters[1] is not None:
      animal_type = filters[1]

    matched_ids = []
    if breed is not None and animal_type is not None:
      query = "SELECT Animal_id FROM ANIMAL where Breed_id='{}' AND Type='{}'".format(breed, animal_type)
      Database.mycursor.execute(query)
      result_set = Database.mycursor.fetchall()
      for animal in result_set:
        temp = str(animal[0])
        matched_ids.append(temp)
      for id in matched_ids:
        animal_info = {}
        animal = Database.get_one_animal(id)
        animal_info = animal.split(",")
        breed = Database.get_one_breed(animal_info[9])
        adoption_fee = Database.get_one_adoption_fee(animal_info[0])
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
        result.append(animal_dict)
    
    elif breed and not animal_type:
      query = "SELECT Animal_id FROM ANIMAL where Breed_id='{}'".format(breed)
      Database.mycursor.execute(query)
      result_set = Database.mycursor.fetchall()
      for animal in result_set:
        temp = str(animal[0])
        matched_ids.append(temp)
      for id in matched_ids:
        animal_info = {}
        animal = Database.get_one_animal(id)
        animal_info = animal.split(",")
        breed = Database.get_one_breed(animal_info[9])
        adoption_fee = Database.get_one_adoption_fee(animal_info[0])
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
        result.append(animal_dict)


    elif animal_type and not breed:
      query = "SELECT Animal_id FROM ANIMAL where Type='{}'".format(animal_type)
      Database.mycursor.execute(query)
      result_set = Database.mycursor.fetchall()
      for animal in result_set:
        temp = str(animal[0])
        matched_ids.append(temp)
      for id in matched_ids:
        animal_info = {}
        animal = Database.get_one_animal(id)
        animal_info = animal.split(",")
        breed = Database.get_one_breed(animal_info[9])
        adoption_fee = Database.get_one_adoption_fee(animal_info[0])
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
        result.append(animal_dict)
    else:
      query = "SELECT Animal_id FROM ANIMAL"
      Database.mycursor.execute(query)
      result_set = Database.mycursor.fetchall()
      for animal in result_set:
        temp = str(animal[0])
        matched_ids.append(temp)
      for id in matched_ids:
        animal_info = {}
        animal = Database.get_one_animal(id)
        animal_info = animal.split(",")
        breed = Database.get_one_breed(animal_info[9])
        adoption_fee = Database.get_one_adoption_fee(animal_info[0])
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
        result.append(animal_dict)
    return result

  @staticmethod
  def get_donation_sum():
    total_donation = 0
    query = "SELECT Amaount FROM DONATIONS"
    Database.mycursor.execute(query)
    result_set = Database.mycursor.fetchall()
    for donation in result_set:
      temp = str(donation[0])
      total_donation = total_donation + int(temp)
    return total_donation
