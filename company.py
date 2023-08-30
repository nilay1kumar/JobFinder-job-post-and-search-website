import mysql.connector
from flask import session


class company_operation:
    def connection(self):
        db = mysql.connector.connect(
            host="localhost", port="3306", user="root", password="root", database="findjob")
        return db

    def company_signup_insert(self, name, email, mobile, address, password):
        db = self.connection()
        mycursor = db.cursor()
        sq = "insert into company(name,email,mobile,address,password) values(%s,%s,%s,%s,%s)"
        record = [name, email, mobile, address, password]
        mycursor.execute(sq, record)
        db.commit()
        mycursor.close()
        db.close()
        return

    def company_delete(self, email):
        db = self.connection()
        mycursor = db.cursor()
        sq = "delete from company where email=%s"
        record = [email]
        mycursor.execute(sq, record)
        db.commit()
        mycursor.close()
        db.close()
        return

    def company_login_verify(self, email, password):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select name,email from company where email=%s and password=%s"
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
                session['company_email'] = r[1]
            return 1

    def company_profile(self):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select name,email,mobile,address from company where email=%s"
        record = [session['company_email']]
        mycursor.execute(sq, record)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row

    def company_profile_update(self, name, mobile, address):
        db = self.connection()
        mycursor = db.cursor()
        sq = "update company set name=%s,mobile=%s,address=%s where email=%s"
        record = [name, mobile, address, session['company_email']]
        mycursor.execute(sq, record)
        db.commit()
        mycursor.close()
        db.close()
        return

    def company_password_change(self, oldpassword, newpassword):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select password from company where password=%s and email=%s"
        record = [oldpassword, session['company_email']]
        mycursor.execute(sq, record)
        row = mycursor.fetchall()
        rc = mycursor.rowcount
        if (rc == 0):
            return 0
        else:
            sq = "update company set password=%s where password=%s and email=%s"
            record = [newpassword, oldpassword, session['company_email']]
            mycursor.execute(sq, record)
            db.commit()
            mycursor.close()
            db.close()
            return 1

    def company_job_post_insert(self, job_name, no_of_post, eligibility, qualification, exp, apply_date, descp, photo):
        db = self.connection()
        mycursor = db.cursor()
        sq = "insert into job(company_email, job_name, no_of_post, eligibility, qualification, exp, apply_date, descp, photo) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        record = [session['company_email'], job_name, no_of_post,
                  eligibility, qualification, exp, apply_date, descp, photo]
        mycursor.execute(sq, record)
        db.commit()
        mycursor.close()
        db.close()
        return

    def company_job_list(self):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select job_id,job_name,no_of_post,qualification,exp,apply_date,photo from job where company_email=%s"
        record = [session['company_email']]
        mycursor.execute(sq, record)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row

    def company_job_delete(self, job_id):
        db = self.connection()
        mycursor = db.cursor()
        sq = "delete from job where job_id=%s"
        record = [job_id]
        mycursor.execute(sq, record)
        db.commit()
        mycursor.close()
        db.close()
        return

    def company_job_applied_view(self, job_id):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select job_id,name,email,mobile,applied_date from apply_job a, user u where a.user_email =u.email and job_id=%s"
        record = [job_id]
        mycursor.execute(sq, record)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row
