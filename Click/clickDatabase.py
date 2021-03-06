#CS304 Project
#Dana, Erica, and Gabby

import sys
import MySQLdb

'''our clickdb connection'''
def getConn(db):
    conn = MySQLdb.connect(host='localhost',
                           user='ubuntu',
                           passwd='',
                           db=db)
    conn.autocommit(True)
    return conn


#get all student's skills from database    

import threading
from connection import getConn
import re


'''Gets student's information (name, email) from database'''
def getStudent(conn, email):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''Select name, email, active from user where email = %s''', [email])
    return curs.fetchone()

'''Returns results of SQL query to get student's skills from the database'''   
def studentSkills(conn, email):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    #use inner join to get list of skills
    curs.execute('''select skill from skills inner join hasSkill using (sid)
    where hasSkill.email = %s''', [email])
    return curs.fetchall()
    
#removes skill from student  
def removeSkill(conn, email, skill):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''Select sid from skills where skill = %s''', [skill])
    skillNum = curs.fetchone().values()[0]
    nr = curs.execute('''delete from hasSkill where sid = %s and email = %s''', [skillNum, email])
    return nr

'''Adds skill to student'''    
def addSkill(conn, email, skill):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    curs.execute('''Select sid from skills where skill = %s''', [skill])
    skillQuery = curs.fetchone() #stores results from query to get skills
    #if skill not in skills table, add it
    if skillQuery == None:
        curs.execute('''insert into skills(skill) values (%s)''', [skill])
        curs.execute('''select last_insert_id()''')
        skillNum = curs.fetchone()['last_insert_id()']
    else:
        skillNum = skillQuery['sid'] #set skillNum to sid from skillQuery
    #continue with inserting email and skill into hasSkill table
    nr = curs.execute('''insert into hasSkill(email, sid) values (%s, %s)''', [email, skillNum])
    return nr


'''Update student's name, email, and/or active status'''
def updateStudentProfile(conn, oldEmail, newEmail, newName, newActive):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    nr = curs.execute('''update user
                    set email = %s, name = %s, active = %s where email = %s''',
                    [newEmail, newName, newActive, oldEmail])
    return nr
    
'''Get all jobs in the database'''
def getJobs(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select pid, name, minHours, pay, location from project''')
    return curs.fetchall()
    
def searchJobs(conn, search):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''select pid, name, minHours, pay, location from project
                    where name like %s''', ['%'+ search + '%'])
    return curs.fetchall()

#adds a new user
def addUser(conn,email,password):
    curs=conn.cursor()
    newrow=curs.execute('''insert into user(email,password) values (%s,%s)''',[email,password])
    return newrow
   
if __name__ == '__main__':
    conn = getConn('clickdb')
    #addSkill(conn, "student2@gmail.com", "public speaking")
    #print(removeSkill(conn, "student1@gmail.com", "math tutoring"))
    #print(studentSkills(conn, "student1@gmail.com"))



