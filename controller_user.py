import os, json
import pandas as pd
from flask import Flask, flash, request, redirect, url_for, jsonify
import pypyodbc
import datetime

""" get all users """
def getAllUsers(conn):
    #returns pd dataframe
    sql_query = pd.read_sql_query('SELECT * from tbl_user', conn)
    """
    split : columns, data objects with each being array
    records : standard json format
    """
    return sql_query

def getUserByPhone(conn, json):
    #print(json)
    #returns pd dataframe
    queryString = """
    Select [id],[username],[userDescription],[gender],[sexuality],
        [age],[email],[phone_number],[location_city],[location_x],[location_y] ,[date_of_birth] 
        from tbl_user where phone_number = '{phone_number}' and password = '{password}'
    """.format(phone_number=json['phone_number'], password=json['password'])
    sql_query = pd.read_sql_query(queryString, conn)
    return sql_query

def getUserByUserId(conn, json):
    #print(json)
    #returns pd dataframe
    queryString = """
    Select [id],[username],[userDescription],[gender],[sexuality],
        [age],[email],[phone_number],[location_city],[location_x],[location_y] ,[date_of_birth] 
        from tbl_user where id='{id}'
    """.format( id=json['id'] )
    sql_query = pd.read_sql_query(queryString, conn)
    return sql_query

def getAllUsersBySearchTerm(conn, json):
    _searchTerm=json['id']
    #print(json)
    #returns pd dataframe
    queryString = """
    Select [id],[username],[userDescription],[gender],[sexuality],
        [age],[email],[phone_number],[location_city],[location_x],[location_y] ,[date_of_birth] 
        from tbl_user 
        where   phone_number like '%{searchTerm}%' 
        or      username like '%{searchTerm}%'
        or      userDescription like '%{searchTerm}%'
    """.format( searchTerm=_searchTerm )
    sql_query = pd.read_sql_query(queryString, conn)
    return sql_query

def checkUnique(conn, json):
    if( not 'userName' in json):
        _userName=""
    else:
        _userName=json['userName']

    queryString = """Select top 1 [id],[username],[userDescription],[gender],[sexuality] 
        ,[age],[email],[phone_number],[location_city],[location_x],[location_y] ,[date_of_birth] 
        from tbl_user where tbl_user.phone_number = '{phone_number}' or tbl_user.userName = '{userName}'
    """.format(phone_number=json['phone_number'], userName=_userName)
    sql_query = pd.read_sql_query(queryString, conn)
    return sql_query

#insertUser
def insertUser(cursor, conn, json):
    try:
        queryString = """insert into tbl_user(
            username, userDescription,gender,sexuality,age,email,phone_number,
            location_city,location_x,location_y, password) output INSERTED.ID
            values(
            '{username}', '{userDescription}', '{gender}', '{sexuality}', {age}, '{email}', '{phone_number}', 
            '{location_city}', {location_x}, {location_y}, '{password}')
        """.format(
            username=json['userName'],              userDescription=json['userDescription'], 
            gender=json['gender'],                  sexuality=json['sexuality'], 
            age=json['age'],                        email='__@__',     
            phone_number=json['phone_number'],      location_city='__@__', 
            location_x=json['location_x'],          location_y=json['location_y'], 
            #date_of_birth=json['date_of_birth'],   , '{date_of_birth}'  ,date_of_birth
            password=json['password']
        )
        cursor.execute(queryString)
        insertId = cursor.fetchone()[0]
        conn.commit()         
        return {'id':insertId, 'message':'success'}
    except pypyodbc.Error as e:
        print("An error has occured")
        return {'id':'NA', 'message':'FAIL', 'Query':queryString, 'error':str(e)}

#updateUser
def updateUserProfile(cursor, conn, json):
    
    queryString = """update tbl_user set 
        username = '{username}',
        age =       {age},
        phone_number= '{phone_number}',
        password=  '{password}'
        WHERE id=   '{id}'
    """.format(
        username=   json['username'],              
        age=        json['age'],
        phone_number=json['phone_number'],      
        password=   json['password'],
        id=         json['id']
    )
    try:
        print(queryString)
        cursor.execute(queryString)
        conn.commit() 
        return {'id':json['id'], 'message':'success'}
    except pypyodbc.ProgrammingError:
        print("An error has occured")
        return {"message":"False"}

#updateUserLocation
def updateUserLocation(cursor, conn, json):
    queryString = """update tbl_user set 
            tbl_user.location_x =    {locationX}, 
            tbl_user.location_y =    {locationy} 
            WHERE 
            tbl_user.id=            {id}
            """.format(
            locationX=   json['locationx'],              
            locationy=   json['locationy'],
            id=          json['id']
        )
    try:
        
        cursor.execute(queryString)
        conn.commit() 
        return {'id':json['id'], 'message':'success'}
    except:
        print("An error has occured")
        return {"message":"FAIL", 'query':queryString}
"""================================================
Conversation, chat history section
================================================"""
def getConversationList(cursor, conn, json):
    queryString = """ 
        select u.id, u.userName, conv.msgCount, conv.converserId
        from(
            select count(coreConvers.conv_id) as msgCount, coreConvers.converserId
            from(
                SELECT [conv_id]
                    ,(
                        case when [fromUserId] = {userId}
                            then [toUserId] 
                            else [fromUserId]
                            end
                    ) as converserId
                FROM [db_pop].[dbo].[tbl_chat_history]
                where [fromUserId] = {userId}
                    or [toUserId]={userId}
            ) coreConvers				
                group by coreConvers.converserId
        ) as conv
        left join tbl_user as u on u.id = conv.converserId 

        """.format(
            userId=    json['userId']
        )
    sql_query = pd.read_sql_query(queryString, conn)
    return sql_query

def getConversation(cursor, conn, json):
    queryString = """
        SELECT conv_id,
            fromUserId,
            toUserId,
            message,
            time_stamp,
            CONVERT(VARCHAR(8), time_stamp, 108) as 'senttime'
        FROM [db_pop].[dbo].[tbl_chat_history]
        where [fromUserId] = {userId} and [toUserId]={fromUserId}
    	or	[fromUserId] = {fromUserId} and [toUserId]= {userId}
        """.format(
            fromUserId=    json['fromUserId'],
            userId=    json['userId'],
        )
    sql_query = pd.read_sql_query(queryString, conn)
    return sql_query

def getConversationLatest(cursor, conn, json):
    conversationid=''
    if('conv_id' in json ):
        conversationid = json['conv_id']
    else:
        conversationid=0
    queryString = """
        SELECT conv_id,
            fromUserId,
            toUserId,
            message,
            time_stamp,
            CONVERT(VARCHAR(8), time_stamp, 108) as 'senttime'
        FROM [db_pop].[dbo].[tbl_chat_history]
        where ([fromUserId] = {userId} and [toUserId]={fromUserId}
    	or	[fromUserId] = {fromUserId} and [toUserId]= {userId})
        AND conv_id>{conv_Id}
        """.format(
            fromUserId=    json['fromUserId'],
            userId=    json['userId'],
            conv_Id =   conversationid 
        )
    sql_query = pd.read_sql_query(queryString, conn)
    return sql_query

def insertConversation(cursor, conn, json):
    queryString = """
        insert into [db_pop].[dbo].[tbl_chat_history]
            ([toUserId],[fromUserId],[message])
        output INSERTED.conv_id
        values ({toUserId},{fromUserId},'{message}')
    """.format(
            fromUserId=  json['fromUserId'],              
            toUserId=    json['toUserId'],
            message=     json['message']
        )
    try:        
        cursor.execute(queryString)
        insertId = cursor.fetchone()[0]
        print('INSERTID', insertId)
        conn.commit() 
        return {'id':insertId, 'message':'success'}
        #return getConversation(cursor, conn, {'fromUserId': json['fromUserId'], 'userId' : json['toUserId']})
    except:
        print("An error has occured")
        return {"message":"FAIL", 'query':queryString}
