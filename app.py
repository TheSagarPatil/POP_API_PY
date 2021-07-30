import controller_user, controller_file_upload, controller_match
import os, json
from flask import Flask, flash, request, redirect, url_for, jsonify, render_template
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import pypyodbc      
from datetime import datetime 
import controller_token as tokenController


UPLOAD_FOLDER = 'C:/Users/abc/repo/smash_or_pass/pop_hy_py_fl/POP_HY_PY/uploadedFiles'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask (__name__ , template_folder='templates')
cors = CORS(app)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 64 * 4096 * 4096
app.config['CORS_HEADERS'] = 'Content-Type'

def isAuthenticated(token='true'):
	if(token=='true'):
		return true
	else:
		return false

def parseQueryData(query_data_frame):
	result = query_data_frame.to_json(orient="records")
	parsed = json.loads(result)
	return parsed

def getConnection():
  connection = pypyodbc.connect('DRIVER={SQL Server};'
																'Server=ABC-PC\SQLEXPRESS;'
																'Database=db_pop;'
																'Trusted_Connection=yes;')
  #print(connection)
  cursor = connection.cursor()  
  return cursor, connection
""" 
formResponse get Response 
"""
def formResponse(data, statusCode=200):
	return app.response_class(
        response=json.dumps(data),
        status=statusCode,
        mimetype='application/json'
    )
	
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
  return render_template('index.html')
"""
#######################
#USERS SECTION
#######################
"""
#Get all Users
@app.route('/api/getUsers', methods=['GET', 'POST'])
@cross_origin()
def getUsers():
	cursor, conn = getConnection()
	query_data_frame = controller_user.getAllUsers(conn)
	parsed = parseQueryData(query_data_frame)
	return formResponse(parsed)

#Get a user by Id
@app.route('/api/Token/GetToken', methods=['POST'])
@app.route('/api/getUserByPhone', methods=['POST'])
@cross_origin()
def getUsersByPhonePassword():
	if(request.method =='POST'):
		json = request.json
		cursor, conn = getConnection()
		query_data_frame = controller_user.getUserByPhone(conn, json)
		if(len(query_data_frame.index)>0):
			parsed = parseQueryData(query_data_frame)
			jwt = tokenController.encode_auth_token(parsed[0]['username'])
			parsed[0]["data"]=jwt
			return formResponse(parsed[0])
		else:
			return formResponse({'message':'no user found'}, 401)
	else:
		return formResponse({'message':'bad request (input format)'}, 401)

#checkUnique
@app.route('/api/Token/checkUnique', methods=['POST'])
@app.route('/api/checkUnique', methods=['POST'])
@cross_origin()
def checkUnique():
	if(request.method =='POST'):
		json = request.json
		cursor, conn = getConnection()
		query_data_frame = controller_user.checkUnique(conn, json)
		parsed = {}
		if( len(query_data_frame.index)>0 ):
			parsed = { "isUnnique": "false",  "isUnique" : "false", "message" : "false"}
		else:
			parsed = { "isUnnique" : "true",  "isUnique" : "true",  "message" : "true"}
		return formResponse(parsed)
	else:
		return formResponse({'message':'bad request (input format)'}, 401)

#getUserByUserId
@app.route('/api/getUserByUserId', methods=['POST'])
@app.route('/api/UserProfile/GetUserById', methods=['POST'])
@cross_origin()
def getUserByUserId():
	if(request.method =='POST'):
		json = request.json
		cursor, conn = getConnection()
		query_data_frame = controller_user.getUserByUserId(conn, json)
		parsed = parseQueryData(query_data_frame)
		return formResponse(parsed)
	else:
		return formResponse({'message':'bad request (input format)'}, 401)

#InsertUser
@app.route('/api/UserProfile/insertUser', methods=['POST'])
@app.route('/api/userProfile/insertUser', methods=['POST'])
@app.route('/api/insertUser', methods=['POST'])
@cross_origin()
def insertUser():
	if(request.method =='POST'):
		json = request.json
		cursor, conn = getConnection()
		query_data_frame = controller_user.insertUser(cursor, conn, json)
		code=200
		if(query_data_frame['id']=="NA"):
			code=400
		#parsed = parseQueryData(query_data_frame)
		return formResponse(query_data_frame, code)
	else:
		return formResponse({'message':'bad request (input format)'}, 401)

#UpdateUser
@app.route('/api/updateUserProfile', methods=['POST'])
@app.route('/api/UserProfile/updateuser', methods=['POST'])
@cross_origin()
def updateUserProfile():
	if(request.method =='POST'):
		json = request.json
		cursor, conn = getConnection()
		query_data_frame = controller_user.updateUserProfile(cursor, conn, json)
		#parsed = parseQueryData(query_data_frame)
		return formResponse(query_data_frame)
	else:
		return formResponse({'message':'bad request (input format)'}, 401)


#UpdateUser
@app.route('/api/updateUserLocation', methods=['POST'])
@app.route('/api/UserProfile/updateUserLocation', methods=['POST'])
@cross_origin()
def updateUserLocation():
	if(request.method =='POST'):
		json = request.json
		cursor, conn = getConnection()
		query_data_frame = controller_user.updateUserLocation(cursor, conn, json)
		#parsed = parseQueryData(query_data_frame)
		return formResponse(query_data_frame)
	else:
		return formResponse({'message':'bad request (input format)'}, 401)

""" 
#############################
USER MATCH SECTION
#############################
"""
#getMatchForUser
@app.route('/api/getMatchForUser', methods=['POST'])
@app.route('/api/match/findMatch', methods=['POST'])
@cross_origin()
def getMatchForUser():
	if(request.method =='POST'):
		json = request.json
		cursor, conn = getConnection()
		#query_data_frame = controller_match.getMatchForUser(conn, json)
		query_data_frame = controller_match.getMatchForUserInGivenArea(conn, json)		
		parsed = parseQueryData(query_data_frame)
		return formResponse(parsed)
	else:
		return formResponse({'message':'bad request (input format)'}, 401)
#getMatchList
@app.route('/api/getMatchList', methods=['POST'])
@app.route('/api/match/getMatchList', methods=['POST'])
@cross_origin()
def getMatchList():
	if(request.method =='POST'):
		json = request.json
		cursor, conn = getConnection()
		query_data_frame = controller_match.getMatchList(conn, json)
		parsed = parseQueryData(query_data_frame)
		return formResponse(parsed)
	else:
		return formResponse({'message':'bad request (input format)'}, 401)


@app.route('/api/getMatchList', methods=['POST'])
@app.route('/api/match/getAttributesListByUser', methods=['POST'])
@cross_origin()
def getAttributesListByUser():
	if(request.method =='POST'):
		json = request.json
		cursor, conn = getConnection()
		query_data_frame = controller_match.getAttributesListByUser(conn, json)
		parsed = parseQueryData(query_data_frame)
		return formResponse(parsed)
	else:
		return formResponse({'message':'bad request (input format)'}, 401)

@app.route('/api/match/insertMatchByUser', methods=['POST'])
@cross_origin()
def insertMatchByUser():
	if(request.method =='POST'):
		json = request.json
		cursor, conn = getConnection()
		query_data_frame = controller_match.insertMatchByUser(cursor, conn, json)
		print(query_data_frame)
		#parsed = parseQueryData(query_data_frame)
		return formResponse({'message':query_data_frame, 'json':json})
	else:
		return formResponse({'message':'bad request (input format)'}, 401)
@app.route('/api/getNotificationsListByUser', methods=['POST'])
@app.route('/api/match/getNotificationsListByUser', methods=['POST'])
@cross_origin()
def getNotificationsListByUser():
	if(request.method =='POST'):
		json = request.json
		cursor, conn = getConnection()
		query_data_frame = controller_match.getNotificationsListByUser(conn, json)
		parsed = parseQueryData(query_data_frame)
		return formResponse(parsed)
	else:
		return formResponse({'message':'bad request (input format)'}, 401)


"""
#############################
CHAT / CONVERSATION SECTION
#############################
"""
@app.route('/api/UserProfile/getConversationList', methods=['POST'])
@cross_origin()
def getConversationList():
	if(request.method =='POST'):
		json = request.json
		cursor, conn = getConnection()
		query_data_frame = controller_user.getConversationList(cursor, conn, json)
		print(query_data_frame)
		parsed = parseQueryData(query_data_frame)
		#return formResponse({'message':'success', 'json':json})
		return formResponse(parsed)
	else:
		return formResponse({'message':'bad request (input format)'}, 401)

@app.route('/api/comm/getConversation', methods=['POST'])
@app.route('/api/UserProfile/getConversation', methods=['POST'])
@cross_origin()
def getConversation():
	if(request.method =='POST'):
		json = request.json
		cursor, conn = getConnection()
		query_data_frame = controller_user.getConversation(cursor, conn, json)
		print(query_data_frame)
		parsed = parseQueryData(query_data_frame)
		#return formResponse({'message':'success', 'json':json})
		return formResponse(parsed)
	else:
		return formResponse({'message':'bad request (input format)'}, 401)

@app.route('/api/comm/getConversationLatest', methods=['POST'])
@app.route('/api/UserProfile/getConversationLatest', methods=['POST'])
@cross_origin()
def getConversationLatest():
	if(request.method =='POST'):
		json = request.json
		cursor, conn = getConnection()
		query_data_frame = controller_user.getConversationLatest(cursor, conn, json)
		print(query_data_frame)
		parsed = parseQueryData(query_data_frame)
		#return formResponse({'message':'success', 'json':json})
		return formResponse(parsed)
	else:
		return formResponse({'message':'bad request (input format)'}, 401)

@app.route('/api/comm/insertConversation', methods=['POST'])
@app.route('/api/UserProfile/insertConversation', methods=['POST'])
@cross_origin()
def insertConversation():
	if(request.method =='POST'):
		json = request.json
		cursor, conn = getConnection()
		query_data_frame = controller_user.insertConversation(cursor, conn, json)
		print(query_data_frame)
		code=200
		#if(query_data_frame['id']=="NA"):
		#	code=400
		#parsed = parseQueryData(query_data_frame)
		return formResponse(query_data_frame, code)
	else:
		return formResponse({'message':'bad request (input format)'}, 401)


""" 
#############################
FILE UPLOAD SECTION
#############################
UPLOAD FILE
"""
@app.route('/upload-file', methods=['GET', 'POST'])
@cross_origin()
def upload_file():
	# check if the post request has the file part
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		resp = jsonify({'message' : 'File successfully uploaded'})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
		resp.status_code = 400
		return resp

if(__name__ == '__main__'):
  app.run(debug=True)