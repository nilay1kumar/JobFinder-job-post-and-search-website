import mysql.connector
from flask import session
from datetime import datetime


class user_operation:
    def connection(self):
        db = mysql.connector.connect(
            host="localhost", port="3306", user="root", password="root", database="findjob")
        return db

    def user_signup_insert(self, name, email, mobile, password):
        db = self.connection()
        mycursor = db.cursor()
        sq = "insert into user(name,email,mobile,password) values(%s,%s,%s,%s)"
        record = [name, email, mobile, password]
        mycursor.execute(sq, record)
        db.commit()
        mycursor.close()
        db.close()
        return

    def user_delete(self, email):
        db = self.connection()
        mycursor = db.cursor()
        sq = "delete from user where email=%s"
        record = [email]
        mycursor.execute(sq, record)
        db.commit()
        mycursor.close()
        db.close()
        return

    def user_login_verify(self, email, password):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select name,email from user where email=%s and password=%s"
        record = [email, password]
        mycursor.execute(sq, record)
        row = mycursor.fetchall()
        rc = mycursor.rowcount
        mycursor.close()
        db.close()

        if (rc == 0):
            return 0
        else:
            for r in row:
                session['name'] = r[0]
                session['email'] = r[1]
            return 1

    def user_profile(self):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select name,email,mobile from user where email=%s"
        record = [session['email']]
        mycursor.execute(sq, record)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row

    def user_profile_update(self, name, mobile):
        db = self.connection()
        mycursor = db.cursor()
        sq = "update user set name=%s,mobile=%s where email=%s"
        record = [name, mobile, session['email']]
        mycursor.execute(sq, record)
        db.commit()
        mycursor.close()
        db.close()
        return

    def user_password_change(self, oldpassword, newpassword):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select password from user where password=%s and email=%s"
        record = [oldpassword, session['email']]
        mycursor.execute(sq, record)
        row = mycursor.fetchall()
        rc = mycursor.rowcount
        if (rc == 0):
            return 0
        else:
            sq = "update user set password=%s where password=%s and email=%s"
            record = [newpassword, oldpassword, session['email']]
            mycursor.execute(sq, record)
            db.commit()
            mycursor.close()
            db.close()
            return 1

    def user_job_search_list(self, qual):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select job_id,job_name,no_of_post,qualification,exp,apply_date,photo,company_email from job where qualification=%s"
        record = [qual]
        mycursor.execute(sq, record)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row

    def user_job_apply(self, job_id, company_email):
        db = self.connection()
        mycursor = db.cursor()
        sq = "insert into apply_job(job_id,user_email,company_email,applied_date) values(%s,%s,%s,%s)"
        applied_date = datetime.now()
        record = [job_id, session['email'], company_email, applied_date]
        mycursor.execute(sq, record)
        db.commit()
        mycursor.close()
        db.close()
        return

    def user_applied_job_view(self):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select j.job_id,job_name,no_of_post,qualification,exp,applied_date,apply_date,descp from job j, apply_job a where j.job_id=a.job_id and user_email=%s"
        record = [session['email']]
        mycursor.execute(sq, record)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row
