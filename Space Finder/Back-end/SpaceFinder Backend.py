from flask import Flask, request, jsonify, make_response
from pymongo import MongoClient
from bson import ObjectId
from flask_cors import CORS
import pandas as pd
import matplotlib
matplotlib.use('agg')
import bcrypt# 
import jwt #jwt
import datetime #jwt
from functools import wraps #jwt
import datetime as datetime
from dotenv.main import load_dotenv
import os
import base64
import logging
from datetime import datetime, timedelta

# Setting Log Message info Configuration (Time - Log Level - message)
logging.basicConfig(filename='Logs/SpaceFinder - '+ datetime.today().strftime('%d-%m-%y') +'.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_JWT_KEY']
CORS(app)

# MongoDB Configuration
client = MongoClient("mongodb://127.0.0.1:27017") #Host
db = client.roomBookerDB 
Rooms = db.Rooms # Rooms
roomBookings = db.roomBookings # Room Bookings
uniNews =db.uniNews
uniEvents=db.uniEvent
userFeedback=db.userFeedback
userBugReport=db.userFeedback
users = db.users

# (name) - (type) - (descriptions)
# @Parameter - (name) - (Real Name/Description) - e.g (Example)
# @Return - (Describtion of Return stuff)

# Catch All - Catch any unhandled exceptions and return an Internal Server Error
# @Parameter - Exception - Any unhandled Exceptions
# @Return Returns an error code 500
@app.errorhandler(Exception)
def catch_all_errors(error):
    logging.critical("Internal Server Error")
    return make_response(jsonify({}),500)


# Login - Generate a JWT token if login credentials are correct
# @Parameter - Header.auth
# @Return - Will return a 200, and JWT token if sucessful  
@app.route('/api/v1.0/login', methods=['GET']) 
def login():

    logging.info("Login Request Initiated")

    authCred = request.authorization
    
    if authCred:
        user = users.find_one( {'username':authCred.username } )
        if user is not None:
            if bcrypt.checkpw(bytes(authCred.password, 'UTF-8'), user["password"]):

                # Encoding Username, token expiry and secret key
                token = jwt.encode( {'user' : authCred.username,'exp' : datetime.utcnow() + timedelta(minutes=90)}, app.config['SECRET_KEY'])

                logging.info("Login Request ended")

                return({'token' : token.decode('UTF-8')},200)
            
        logging.warning("Could not verify account details")

        return make_response(jsonify({"Error" : "Could not verify account" }), 404)

# Auth Token - Generates user information based on JWT token
# @Parameter - access-token within Request Header
# @Return - Will return a 200, and user information if sucessful          
@app.route('/api/v1.0/authtoken', methods=['GET'])
def authtoken():
        
        logging.info("authtoken Request Initiated")

        authtokens = None

        if 'access-token' in request.headers:
            authtokens = request.headers['access-token']
        if not authtokens:
            logging.error("Authtoken is missing")
            return (jsonify({'message' : 'Authtoken not found'}), 404)
        try:
            # Decoding JWT token
            jwtInfo = jwt.decode(authtokens, app.config['SECRET_KEY'])

            # Finding specific User, and returning more information
            for user in users.find():
                if user['username'] == jwtInfo['user']:
                    logging.info("authtoken Request Ended")
                    return jsonify({'auth' : 'True','name': user['name'], 'access': user['Access'], 'id':str(user['_id'])})
        except:
            logging.error("Token is invalid")
            return (jsonify( {'error' : 'Token has been detected as invalid'}), 404)

# Create new User - POST - Creates new user based on input
# @Parameter - name, username, password, email, accessLevel, profilePicture
# @Return - Will return a 200 response, with added new account
@app.route("/api/v1.0/newaccount", \
 methods=["POST"])
def post_new_user():

    logging.info("Post new User Request Initiated")

    if "name" in request.form and "userName" in request.form and "password" in request.form and "email" in request.form and "accessLevel" in request.form:
        new_account = {
            "name" : (request.form["name"]),
            "username" : (request.form["userName"]),
            "password" : request.form["password"],
            "email" : request.form["email"],
            "accessLevel" : (request.form["accessLevel"]),
            "profilePicture":(request.form["profilePicture"])
            }
        new_account["password"] = bcrypt.hashpw(new_account["password"].encode('utf-8'), bcrypt.gensalt())

        users.insert_one(new_account)
    else:
        logging.error("Missing Form Data")
        return make_response(jsonify({"error" : "Missing Form Data" }), 404)
    
    logging.info("Post new User Request Ended")
    return make_response(jsonify({"Sucessful" : "Added new account" }), 200)       

#Return all Rooms - GET - Return all room information
#@Return - Returns all data in a JSON Response, with code 200 if sucessful
@app.route("/api/v1.0/rooms", methods=["GET"])
def return_all_rooms():
    logging.info("Return all rooms Request Initiated")
    data = []
    for room in Rooms.find():
        room['_id'] = str(room['_id'])
        data.append(room)

    # If data List is empty, returns false triggering error 
    if data:
        logging.info("Return all rooms Request ended")
        return make_response(jsonify(data),200)
    else:
        logging.warning("No rooms registered in system")
        return make_response(jsonify({"error" : "No Rooms Registered in System"}), 404)

# Show one room - GET - Return one room based on ID
# @Parameter - id - The ID of a given room - e.g 6394f12f318a7dfd9b51d8d7
# @Return - Will return all data on a single room and a 200 code, else will return 404
@app.route("/api/v1.0/rooms/<string:id>", \
 methods=["GET"])
def return_one_room(id):
    logging.info("Return one room Request Initiated")
    roomDetails = Rooms.find_one({'_id':ObjectId(id)})

    if roomDetails is not None:
        roomDetails['_id'] = str(roomDetails['_id'])
        logging.info("Return one room Request ended")
        return make_response( jsonify( [roomDetails] ), 200 )
    else:
        logging.error("Return one room Request Initiated")
        return make_response( jsonify( \
            {"error" : "Room Not Found - Possible Invalid Room ID"} ), 404 )

#Return all bookings - GET - Return all booking information
#@Return - Returns all data in a JSON Response, with code 200 if sucessful
@app.route("/api/v1.0/bookings", methods=["GET"])
def return_all_bookings():
    logging.info("Return all bookings Request Initiated")
    data = []
    for bookings in roomBookings.find():
        bookings['_id'] = str(bookings['_id'])
        data.append(bookings)

    # If data List is empty, returns false triggering error 
    if data:
        logging.info("Return all bookings Request Initiated")
        return make_response(jsonify(data),200)
    else:
        logging.warning("No bookings registered in system")
        return make_response(jsonify({"error" : "No Bookings Registered in System"}), 404)

# Show bookings for one room - GET - Return all bookings for a Room based on ID
#@Parameter - id - The ID of a given room - e.g 6394f12f318a7dfd9b51d8d7
#@Return - Will return all data on a single room's bookings and a 200 code, else will return 404
@app.route("/api/v1.0/bookings/<string:id>", \
 methods=["GET"])
def show_one_room_bookings(id):
    logging.info("Show one room booking Request Initiated")
    data = []

    for bookings in roomBookings.find():
        if str(bookings['roomID']) == str(id):
            bookings["_id"] = str(bookings["_id"])
            data.append(bookings)

    # If data List is empty, returns false triggering error 
    if data:
        logging.info("Show one room booking Request ended")
        return make_response(jsonify(data),200)
    else:
        logging.warning("No bookings for this room")
        return make_response(jsonify({"error" : "No Bookings for this room {} ".format(id) }), 404)

# Show one booking  - GET - Return one booking based on ID
#@Parameter - id - The ID of a given booking - e.g 6394f12f318a7dfd9b51d8d7
#@Return - Will return all data on a single booking and a 200 code, else will return 404
@app.route("/api/v1.0/booking/<string:id>", \
 methods=["GET"])
def show_one_booking(id):
    logging.info("Show one booking Request Initiated")
    data = roomBookings.find_one({'_id':ObjectId(id)})

    if data is not None:
        data['_id'] = str(data['_id'])
        logging.info("Show one booking Request ended")
        return make_response (jsonify(data), 200)
    else:
        logging.warning("Booking not found")
        return make_response( jsonify( \
            {"error" : "Booking Not Found - Possible Invalid Booking ID"} ), 404 )

# Show bookings for one User - GET - Return all bookings for a User
#@Parameter - id - The ID of a given user - e.g 1
#@Return - Will return all data related to Bookings for a User, will return 200 if no errors
@app.route("/api/v1.0/bookings/user/<string:id>", \
 methods=["GET"])
def show_all_bookings_for_a_user(id):
    logging.info("Show all bookings for a user Request Initiated")
    data = []

    for bookings in roomBookings.find():
        if str(bookings['userID']) == str(id):
            bookings["_id"] = str(bookings["_id"])
            data.append(bookings)

    # If data List is empty, returns false triggering error 
    if data:
        logging.info("Show all bookings for a user Request ended")
        return make_response(jsonify(data),200)
    else: 
        logging.warning("No bookings for this user {}".format(id))
        return make_response(jsonify({"error" : "No Bookings for this user {} ".format(id) }), 404)

# Show bookings for one room for one User - GET - Return all bookings for a User for one room
#@Parameter - id - The ID of a given user - e.g 1 and the Room ID e.g. 1
#@Return - Will return all data related to Bookings for a User for a room, will return 200 if no errors
@app.route("/api/v1.0/bookings/user/<string:userid>/<string:roomid>", \
 methods=["GET"])
def show_all_bookings_for_a_user_for_a_room(userid, roomid):
    logging.info("Show all bookings for a user for a room Request Initiated")
    data = []

    for bookings in roomBookings.find():
        if str(bookings['userID']) == str(userid):
            if str(bookings['roomID']) == str(roomid):
                bookings["_id"] = str(bookings["_id"])
                data.append(bookings)

    # If data List is empty, returns false triggering error 
    if data:
        logging.info("Show all bookings for a user for a room Request ended")
        return make_response(jsonify(data),200)
    else: 
        logging.warning("No Bookings for this User")
        return make_response(jsonify({"error" : "No Bookings for this user {} ".format(id) }), 404)

# Add a Booking - POST - Add a Booking for a User
#@Parameter - UserID - endDateTime - startDateTime - roomID
#@Return - Will return all data related to Bookings for a User for a room, will return 200 if no errors
@app.route("/api/v1.0/bookingsname", \
 methods=["POST"])
def post_a_booking_by_Name():
    logging.info("Post a booking by Name Request Initiated")
    if "userid" in request.form and "roomname" in request.form and "startdatetime" in request.form and "enddatetime" in request.form:
      
        for room in Rooms.find():
            if room['roomName'] == (request.form["roomname"]):
                roomid = room['roomID']


        # Check if Booking Already Exists
        for bookings in roomBookings.find():
            if (bookings['roomID']) == (roomid):
                if bookings['startDateTime'] <= request.form["startdatetime"] <= bookings['endDateTime']:
                    if bookings['startDateTime'] <= request.form["enddatetime"] <= bookings['endDateTime']:
                        return make_response(jsonify({"error" : "Booking Time is in conflict with existing time" }), 202)
        
        new_booking = {
            "roomID" : (roomid),
            "roomName":request.form["roomname"],
            "startDateTime" : request.form["startdatetime"],
            "endDateTime" : request.form["enddatetime"],
            "userID" : (request.form["userid"]),
            }
        bookingID = roomBookings.insert_one(new_booking)
    else:
        logging.warning("Missing Form Data")
        return make_response(jsonify({"error" : "Missing Form Data" }), 404)
    logging.info("Post a booking by Name Request Ended")
    return make_response(jsonify({"Sucessful" : "Added Booking" }), 201)

# Add a Booking - POST - Add a Booking for a User
#@Parameter - UserID - endDateTime - startDateTime - roomID
#@Return - Will return all data related to Bookings for a User for a room, will return 200 if no errors
@app.route("/api/v1.0/bookingid", \
 methods=["POST"])
def post_a_booking_by_id():
    logging.info("Post a booking by id Request Initiated")
    if "userid" in request.form and "roomid" in request.form and "startdatetime" in request.form and "enddatetime" in request.form:
      
        for room in Rooms.find():
                if str(room['_id']) == (request.form['roomid']):
                    roomname = room['roomName']


        # Check if Booking Already Exists
        for bookings in roomBookings.find():
            if (bookings['roomID']) == (request.form["roomid"]):
                if bookings['startDateTime'] <= request.form["startdatetime"] <= bookings['endDateTime']:
                    if bookings['startDateTime'] <= request.form["enddatetime"] <= bookings['endDateTime']:
                        return make_response(jsonify({"error" : "Booking Time is in conflict with existing time" }), 202)
        
        new_booking = {
            "roomID" : request.form["roomid"],
            "roomName":(roomname),
            "startDateTime" : request.form["startdatetime"],
            "endDateTime" : request.form["enddatetime"],
            "userID" : (request.form["userid"]),
            }
        bookingID = roomBookings.insert_one(new_booking)
    else:
        logging.error("Missing Form Data")
        return make_response(jsonify({"error" : "Missing Form Data" }), 404)
    logging.info("Post a booking by id Request Ended")
    return make_response(jsonify({"Sucessful" : "Added Booking" }), 201)

# Add a Booking - POST - Add a Booking for a User
#@Parameter - firstName - lastName - email - header - message
#@Return -  Will return 200 if no errors
@app.route("/api/v1.0/feedback", \
 methods=["POST"])
def post_feedback():
    logging.info("Post feedback Request Initiated")
    if "firstName" in request.form and "lastName" in request.form and "type" in request.form and "email" in request.form and "header" in request.form and "time" in request.form and "message" in request.form:
        
        new_feedback = {
            "type" : (request.form["type"]),
            "firstName" : (request.form["firstName"]),
            "lastName" : request.form["lastName"],
            "email" : request.form["email"],
            "header" : (request.form["header"]),
            "phone" : (request.form["phone"]),
            "message" : (request.form["message"]),
            "time": (request.form["time"])
            }
        userFeedback.insert_one(new_feedback)
    else:
        logging.error("Missing Form Data")
        return make_response(jsonify({"error" : "Missing Form Data" }), 404)
    logging.info("Post feedback Request Ended")
    return make_response(jsonify({"Sucessful" : "Added user feedback" }), 201)

# Delete booking - delete - Will delete any booking gaven
# @Parameter - ID - The booking ID of a given booking - e.g 6394f12f318a7dfd9b51d8d7
# @Return - Will return an empty JSON with a 404 status code if not found, otherwise will return an empty set with a 204
@app.route("/api/v1.0/bookings/<string:id>", \
 methods=["delete"])
def delete_booking(id):
     
     logging.info("Delete Booking Request Initiated")

     result = roomBookings.delete_one( { "_id" : ObjectId(id) } )

     if result.deleted_count == 1:
        logging.info("Delete Booking Request Ended")
        return make_response( jsonify( {} ), 204)
     else:
         logging.warning("Could not find Booking ID")
         return make_response( jsonify( { "error" : "Could not find Booking ID" } ), 404)

# Update booking - update - Will update any booking gaven
# @Parameter - ID - The booking ID of a given booking - e.g 6394f12f318a7dfd9b51d8d7
# @Return - Will return an 201, or a 404 status code if not found
@app.route("/api/v1.0/bookings/<string:id>", \
 methods=["PUT"])
def update_booking(id):

    logging.info("Update Booking Request Initiated")

    if "userid" in request.form and "roomname" and "startdatetime" in request.form and "enddatetime" in request.form:
        
        for room in Rooms.find():
                if room['roomName'] == (request.form['roomname']):
                    roomid= room['roomID']
        
        
        result = roomBookings.update_one( { "_id" : ObjectId(id) }, {
                "$set" : { 
                                
                                "roomID" : roomid,
                                "roomName":request.form["roomname"],
                                "startDateTime" : request.form["startdatetime"],
                                "endDateTime" : request.form["enddatetime"],
                                "userID" : request.form["userid"],
                }})
    else:
         logging.error("Missing Form Data")
         return make_response(jsonify({"error" : "Missing Form Data" }), 404)

    if result.matched_count == 1:
        logging.info("Update Booking Request Ended")
        return make_response(jsonify({"Sucessful" : "Updated Booking" }), 200)
    else:
        logging.warning("No booking matches this ID found")
        return make_response(jsonify({"error" : "No booking matching this ID found" }), 404)
    
#Show all university news - GET - Return all news
#@Return - Will return all data related to university news, will return 200 if no errors
@app.route("/api/v1.0/uniNews", \
 methods=["GET"])
def show_all_university_news():

    logging.info("Show all university news Request Initiated")

    data = []
    for news in uniNews.find():
        news['_id'] = str(news['_id'])
        data.append(news)

    # If data List is empty, returns false triggering error 
    if data:
        logging.info("Show all university news Request Ended")
        return make_response(jsonify(data),200)
    else: 
        logging.warning("No news registered in system")
        return make_response(jsonify({"error" : "No News Registered in System"}), 404)
    
#@Parameter - firstName - lastName - email - header - message
#@Return -  Will return 200 if no errors
@app.route("/api/v1.0/bugReport", \
 methods=["POST"])
def post_bugReport():
    logging.info("Post Bug Report Request Initiated")
    if "firstName" in request.form and "lastName" in request.form and "category" in request.form and "type" in request.form and "email" in request.form and "header" in request.form and "time" in request.form and "message" in request.form:
        
        new_bugreport = {
            "type" : (request.form["type"]),
            "firstName" : (request.form["firstName"]),
            "lastName" : (request.form["lastName"]),
            "category" :(request.form["category"]),
            "email" : (request.form["email"]),
            "header" : (request.form["header"]),
            "phone" : (request.form["phone"]),
            "message" : (request.form["message"]),
            "time": (request.form["time"])
            }
        userBugReport.insert_one(new_bugreport)
    else:
        logging.error("Missing Form Data")
        return make_response(jsonify({"error" : "Missing Form Data" }), 404)
    logging.info("Post Bug Report Request Ended")
    return make_response(jsonify({"Sucessful" : "Added bug report" }), 201)
    
#Show all university events - GET - Return all events
#@Return - Will return all data related to university events, will return 200 if no errors
@app.route("/api/v1.0/uniEvents", \
 methods=["GET"])
def show_all_university_events():
    logging.info("show all unversity events Request Initiated")

    data = []
    for event in uniEvents.find():
        event['_id'] = str(event['_id'])
        data.append(event)

    # If data List is empty, returns false triggering error 
    if data:
        logging.info("show all unversity events Request Ended")
        return make_response(jsonify(data),200)
    else:
        logging.warning("No Events Registered in System")
        return make_response(jsonify({"error" : "No Events Registered in System"}), 404)



#Return all Rooms with closest name match - GET - Return all relevant room information
#@Parameter - searchParameter - The name of a given room e.g. Belfast
#@Return - Returns all data in a JSON Response, with code 200 if sucessful
@app.route("/api/v1.0/rooms/close/<string:searchParameter>", methods=["GET"])
def return_all_rooms_closest_match(searchParameter):
    logging.info("All rooms closest matches Request Initiated")
    rgx = ("^"+searchParameter); 
    data = []
    for room in Rooms.find({"name" : rgx}):
        room['_id'] = str(room['_id'])
        data.append(room)

    # If data List is empty, returns false triggering error 
    if data:
        logging.info("All rooms closest matches Request ended")
        return make_response(jsonify(data),200)
    else:
        logging.warning("No rooms registered in System")
        return make_response(jsonify({"error" : "No Rooms Registered in System"}), 404)

# Generates a Pie Chart and returns it within the response as a Byte Array
#@Return - Return piechart with today's room utalisation
@app.route("/api/v1.0/rooms/piegraph/<string:currentDate>", methods=["GET"])
def generate_PieChart_totalRoom_Usage(currentDate):
    logging.info("Generate Pie Chart Usage Request Initiated")
    num_of_Rooms = 0 
    data = []
    difference = timedelta(0)


    for room in Rooms.find():
        num_of_Rooms = num_of_Rooms + 1
    for booking in roomBookings.find():
        if(booking['startDateTime'] <= currentDate <= booking['endDateTime']):
            difference = difference + (datetime.strptime(booking['endDateTime'],'%Y-%m-%d %H:%M' ) - datetime.strptime(booking['startDateTime'], '%Y-%m-%d %H:%M'))
            print("Hi ;)")

    totalUsedRooms = difference.seconds / 60
    totalRoomMinutes = num_of_Rooms * 60

    df = pd.DataFrame({'Usage': ['Rooms Occupied', 'Rooms Free'],
                   'Values': [totalUsedRooms, totalRoomMinutes]})

    pieChartImg = df.groupby(['Usage']).sum().plot(kind='pie', y='Values', autopct='%1.0f%%', labeldistance=None).get_figure()
    pieChartImg.savefig("output.jpeg")

    with open("output.jpeg", "rb") as image:
     encoded_string = base64.b64encode(image.read())
     edit = str(encoded_string)
     edit = edit.replace("b'", "")
     edit = edit.replace("'","")

     logging.info("Generate Pie Chart Usage Request Ended")
     return make_response(jsonify({"image" : str(edit)}),200)
    
@app.route("/api/v1.0/rooms/profileimg/<string:userID>", methods=['GET'])
def return_ProfilePicture(userID):

    logging.info("ProfilePicture Request Initiated")

    profilePic = "userProfileImg/DefaultProfilePictures.png"

    for user in users.find():
        if str(user['_id']) == str(userID):
            profilePic = user['profilePicture']


    with open(profilePic, "rb") as image:
        encodedImg = base64.b64encode(image.read())
        img = str(encodedImg)
        img = img.replace("b'", "")
        img = img.replace("'","")
    logging.info("ProfilePicture Request Ended")
    return make_response(jsonify({"image" : str(img)}),200)

@app.route("/api/v1.0/rooms/roommapimg/<string:roomID>", methods=['GET'])
def return_RoomMappingPicture(roomID):
    logging.info("Room Mapping Picture Request Initiated")
    roomMappingPic = "buildingMaps/Floor_1.png"

    for room in Rooms.find():
        if str(room['_id']) == str(roomID):
            roomMappingPic = room['Maplink']


    with open(roomMappingPic, "rb") as image:
        encodedImg = base64.b64encode(image.read())
        img = str(encodedImg)
        img = img.replace("b'", "")
        img = img.replace("'","")

    logging.info("Room Mapping Picture Request Ended")
    return make_response(jsonify({"image" : str(img)}),200)


    

__name__ == "__main__"
app.run(debug=True)

































