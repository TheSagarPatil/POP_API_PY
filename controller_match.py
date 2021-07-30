import os, json
import pandas as pd
from flask import Flask, flash, request, redirect, url_for, jsonify
import datetime

""" get all users """
def getMatchForUser(cursor, conn, json):
    #print(json)
    #returns pd dataframe
    queryString = """select
            count(concat(ue1.userId, '-', ue2.userId)) as score,
            ue2.userId, u.userName, u.userDescription, 
            (select top 1 tbl_userImages.imageId from tbl_userImages where tbl_userImages.userId = ue2.userId) as imageId
        from db_pop.dbo.tbl_user_userExpectations as ue1 
            inner join db_pop.dbo.tbl_user_userExpectations as ue2 
            on ue1.exptId = ue2.exptId"
            inner join db_pop.dbo.tbl_user as u 
            on ue2.userId = u.Id 
        where ue1.userId < ue2.userId 
            and ue1.userId = {userId} and 
            u.location_x < (select(location_x + {querydist} ) from db_pop.dbo.tbl_user where Id = {userId} ) and 
            u.location_x > (select(location_x - {querydist} ) from db_pop.dbo.tbl_user where Id = {userId} ) and 
            u.location_y < (select(location_y + {querydist} ) from db_pop.dbo.tbl_user where Id = {userId} ) and 
            u.location_y > (select(location_y - {querydist} ) from db_pop.dbo.tbl_user where Id = {userId} ) 
        group by ue2.userId, u.userName, u.userDescription 
        order by score desc
    """.format(querydist=json['distance'], userId=json['userId'])
    sql_query = pd.read_sql_query(queryString, conn)
    return sql_query

""" get users in Area """
def getMatchForUserInGivenArea(conn, json):
    #print(json)
    #returns pd dataframe
    queryString = """Select * from tbl_user as u where 
        u.location_x < (select(location_x + {querydist} ) from db_pop.dbo.tbl_user where Id = {userId} ) and 
        u.location_x > (select(location_x - {querydist} ) from db_pop.dbo.tbl_user where Id = {userId} ) and 
        u.location_y < (select(location_y + {querydist} ) from db_pop.dbo.tbl_user where Id = {userId} ) and 
        u.location_y > (select(location_y - {querydist} ) from db_pop.dbo.tbl_user where Id = {userId} ) 
    """.format(querydist=json['distance'], userId=json['userId'])
    sql_query = pd.read_sql_query(queryString, conn)
    return sql_query

#getMatchList
def getMatchList(conn, json):
    #print(json)
    #returns pd dataframe
    queryString = """
        SELECT us1.[userSwipERId] as swiper
            us1.[userSwipEDId] as swiped ,us1.[swipe] ,us1.[_timestamp],
            (Select top 1 imageId from tbl_userImages where userId = us1.[userSwipEDId]) as imageId
        FROM[db_pop].[dbo].[tbl_user_swipe] as us1
            INNER JOIN [db_pop].[dbo].[tbl_user_swipe] as us2
            on us1.userSwipEDId = us2.userSwipERId
        WHERE us1.[userSwipERId] = {userId} AND us1.[swipe] = 1 
            AND us2.[userSwipEdId] = {userId} AND us2.[swipe] = 1
    """.format(userId=json['userId'])
    sql_query = pd.read_sql_query(queryString, conn)
    return sql_query


"""getAttributesListByUser"""
def getAttributesListByUser(conn, json):
    #print(json)
    #returns pd dataframe
    queryString = """
        SELECT TOP 1000 UE.[exptId],UE.[exptName] FROM [db_pop].[dbo].[tbl_userExpectations] as  UE
            inner join[tbl_user_userExpectations] as UUE
            on UUE.exptId = UE.exptId
            WHERE UUE.userId =  {userId}
    """.format(userId=json['userId'])
    sql_query = pd.read_sql_query(queryString, conn)
    return sql_query

def insertMatchByUser(cursor, conn, json):
    try:
        _swipe = True
        if (json['swipe'] == "false" or json['swipe'] == False):
            _swipe = False
        else:
            _swipe = True
        queryString ="""
            insert into tbl_user_swipe values ({swiper}, {swiped}, '{swipe}', CURRENT_TIMESTAMP)
        """.format( swiper = json['swiper'], 
                    swiped = json['swiped'],
                    swipe  = _swipe
                )
        #cursor.execute(queryString)
        #userId, notification to 
        #relateduserId who triggered the application
        #type : type of notification (SWIPE, MESSAGE)
        if(_swipe == True):
            queryString +="""
                ;insert into tbl_userNotifications 
                        (userId,    relatedUserId,  type,       _timestamp) 
                values  ({swiped},  {swiper},       'SWIPE',    CURRENT_TIMESTAMP);
            """.format( swiper = json['swiper'], 
                        swiped = json['swiped']
                    )
        cursor.execute(queryString)
        conn.commit() 
        return {'message':'success'}
    except:
        print("An error has occured")
        return {'message':'FAIL', 'Query':queryString}

"""getMatchNotification"""
def getNotificationsListByUser(conn, json):
    #print(json)
    #returns pd dataframe
    queryString = """
        /****** Script for SelectTopNRows command from SSMS  ******/
        SELECT TOP 1000 n.[id]
            ,[userId]
            ,[type]
            ,[metadatajson]
            ,[relatedUserId]
            ,[_timestamp]
            ,[readByUser]
            ,u.username as [relatedusername]
        
        FROM [db_pop].[dbo].[tbl_userNotifications] as n
        left join [db_pop].[dbo].[tbl_user]  u on u.id = n.relateduserId
        WHERE userId =  {userId}
    """.format(userId=json['userId'])
    sql_query = pd.read_sql_query(queryString, conn)
    return sql_query
