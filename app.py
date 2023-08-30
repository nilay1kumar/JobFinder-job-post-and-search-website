from flask import Flask, render_template, request, flash, redirect, url_for, session
from user import user_operation
import hashlib
from company import company_operation
from captcha.image import ImageCaptcha
import random
from flask_mail import *
from validate import myvalidate

app = Flask(__name__)
app.secret_key = "hfsf6734hsdg6t43y"

# -------------------mail configuration---------------------------
app.config["MAIL_SERVER"] = 'smtp.office365.com'
app.config["MAIL_PORT"] = '587'
app.config["MAIL_USERNAME"] = 'your production eamil that will send email for verification goes here ' # put email and password
app.config["MAIL_PASSWORD"] = 'Your email password goes here'
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
mail = Mail(app)
# ----------------------------------------------------------


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logo')
def logo():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/user_signup')
def user_signup():
    num = random.randrange(100000, 999999)
    # Create an image instance of the given size
    img = ImageCaptcha(width=280, height=90)

    # Image captcha text
    global captcha_text
    captcha_text = str(num)  # convert integer into string

    # write the image on the given file and save it
    img.write(captcha_text, 'static/captcha/user_captcha.png')
    return render_template('user_signup.html')


@app.route("/user_signup_insert", methods=['POST', 'GET'])
def user_signup_insert():
    if request.method == 'POST':
        name = request.form['name']
        email=request.form['email']
        mobile=request.form['mobile']
        password=request.form['password']
        # validation required
        frm=[name,email,mobile,password]
        valid = myvalidate() 
        v=valid.required(frm)
        if(v==False):
            flash("field must be filled!!")
            return redirect(url_for("user_signup"))
        
        #validate name
        frm=[name]
        v=valid.mustalpha(frm)
        if(v==False):
            flash("name must be a alphabate!!")
            return redirect(url_for("user_signup"))
        
        #validate mobile
        v=valid.mustdigit(mobile)
        if(v==False):
            flash("mobile number must be of 10 digits!!")
            return redirect(url_for("user_signup"))
        #captcha verification
        if (captcha_text != request.form['captcha']):
            flash("Invalid captcha!!")
            return redirect(url_for("user_signup"))

    
        # --- password encryption----------------
        pas = hashlib.md5(password.encode())
        password = pas.hexdigest()

        op = user_operation()  # object created of class from user module
        op.user_signup_insert(name, email, mobile, password)

        # ------- email verification--------------------------------
        global otp
        otp = random.randint(100000, 999999)

        msg = Message('JobFinder Email verification',
                      sender='forproductionof@outlook.com', recipients=[email])

        msg.body = "Hi " + name + "\nYour email OTP is: " + str(otp)

        mail.send(msg)
        return render_template('user_email_verify.html', email=email)


@app.route('/user_email_otp_verify', methods=['GET', 'POST'])
def user_email_otp_verify():
    user_otp = request.form['otp']
    if otp == int(user_otp):
        flash("Your Email is Verified.. You can Login Now!!!")
        return redirect(url_for('user_login'))

    email = request.form['email']
    op = user_operation()  # object create
    op.user_delete(email)
    flash("Your Email verification is failed... Register with Valid Email!!!")
    return redirect(url_for('user_signup'))


@app.route('/user_login')
def user_login():
    return render_template('user_login.html')


@app.route("/user_dashboard")
def user_dashboard():
    if 'email' in session:
        return render_template("user_dashboard.html")
    else:
        flash("kindly login to access this page!!")
        return redirect(url_for('user_login'))


@app.route("/user_profile")
def user_profile():
    if 'email' in session:
        op = user_operation()  # object create
        r = op.user_profile()
        return render_template("user_profile.html", record=r)
    else:
        flash("kindly login to access this page!!")
        return redirect(url_for('user_login'))


@app.route("/user_profile_update", methods=['POST', 'GET'])
def user_profile_update():
    if 'email' in session:
        if request.method == 'POST':
            name = request.form['name']
            mobile = request.form['mobile']
            op = user_operation()  # object create
            op.user_profile_update(name, mobile)
            flash("Your profile is updated successfully!!")
            return redirect(url_for('user_profile'))
    else:
        flash("kindly login to access this page!!")
        return redirect(url_for('user_login'))


@app.route("/user_logout")
def user_logout():
    session.clear()
    return redirect(url_for('user_login'))


@app.route("/user_login_verify", methods=['POST', 'GET'])
def user_login_verify():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # --- password encryption----------------
        pas = hashlib.md5(password.encode())
        password = pas.hexdigest()

        op = user_operation()  # object create
        r = op.user_login_verify(email, password)
        if (r == 0):
            flash("invalid email and password")
            return redirect(url_for('user_login'))
        else:
            flash("successfully logged in")
            return redirect(url_for('user_dashboard'))


@app.route("/user_password_form")
def user_password_form():
    if 'email' in session:
        return render_template("user_password_form.html")
    else:
        flash("kindly login to access this page!!")
        return redirect(url_for('user_login'))


@app.route("/user_password_change", methods=['POST', 'GET'])
def user_password_change():
    if 'email' in session:
        if request.method == 'POST':
            oldpassword = request.form['oldpassword']
            newpassword = request.form['newpassword']

            # --- password encryption----------------
            pas = hashlib.md5(oldpassword.encode())
            oldpassword = pas.hexdigest()

            pas = hashlib.md5(newpassword.encode())
            newpassword = pas.hexdigest()

            op = user_operation()  # object create
            r = op.user_password_change(oldpassword, newpassword)
            if (r == 0):
                flash("Your old password is invalid!!")
                return redirect(url_for('user_password_form'))
            else:
                session.clear()
                flash("Your password is updated successfully..login now!!")
                return redirect(url_for('user_login'))
    else:
        flash("kindly login to access this page!!")
        return redirect(url_for('user_login'))


@app.route("/user_job_search")
def user_job_search():
    if 'email' in session:
        return render_template("user_job_search.html")
    else:
        flash("kindly login to access this page!!")
        return redirect(url_for('user_login'))


@app.route("/user_job_search_list", methods=['POST', 'GET'])
def user_job_search_list():
    if 'email' in session:
        if request.method == 'POST':
            qual = request.form['qualification']
            op = user_operation()  # object create
            r = op.user_job_search_list(qual)
            return render_template("user_job_search.html", record=r)
    else:
        flash("kindly login to access this page!!")
        return redirect(url_for('user_login'))


@app.route("/user_job_apply", methods=['POST', 'GET'])
def user_job_apply():
    if 'email' in session:
        if request.method == 'GET':
            job_id = request.args.get('job_id')
            company_email = request.args.get('company_email')
            op = user_operation()  # object create
            op.user_job_apply(job_id, company_email)
            flash("job applied successfully")
            return redirect(url_for('user_job_search'))
    else:
        flash("kindly login to access this page!!")
        return redirect(url_for('user_login'))


@app.route("/user_applied_job_view")
def user_applied_job_view():
    if 'email' in session:
        op = user_operation()  # object create
        r = op.user_applied_job_view()
        return render_template("user_applied_job_view.html", record=r)
    else:
        flash("kindly login to access this page!!")
        return redirect(url_for('user_login'))

# ---------------------------Company Module ----------------------------------------------------------


@app.route('/company')
def company():
    return render_template('company.html')


@app.route("/company_signup")
def company_signup():
    num = random.randrange(100000, 999999)
    # Create an image instance of the given size
    img = ImageCaptcha(width=280, height=90)

    # Image captcha text
    global captcha_text1
    captcha_text1 = str(num)  # convert integer into string

    # write the image on the given file and save it
    img.write(captcha_text1, 'static/captcha/company_captcha.png')
    return render_template("company_signup.html")


@app.route("/company_signup_insert", methods=['POST', 'GET'])
def company_signup_insert():
    if request.method == 'POST':
        name=request.form['name']
        email=request.form['email']
        mobile=request.form['mobile']
        address=request.form['address']
        password=request.form['password']
        # validation
        frm=[name,email,mobile,address,password]
        valid = myvalidate() 
        v=valid.required(frm)
        if(v==False):
            flash("field must be filled!!")
            return redirect(url_for("company_signup"))
        
        #captcha varification
        if (captcha_text1!=request.form['captcha']):
            flash("Invalid captcha!!")
            return redirect(url_for("company_signup"))
        
        # --- password encryption----------------
        pas = hashlib.md5(password.encode())
        password = pas.hexdigest()

        op = company_operation()  # object created of class from company module
        op.company_signup_insert(name, email, mobile, address, password)

        flash("Successfully Registered.. You can Login Now!!!")
        return redirect(url_for('company_login'))


@app.route("/company_login")
def company_login():
    return render_template("company_login.html")


@app.route("/company_login_verify", methods=['POST', 'GET'])
def company_login_verify():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # --- password encryption----------------
        pas = hashlib.md5(password.encode())
        password = pas.hexdigest()

        op = company_operation()  # object create
        r = op.company_login_verify(email, password)
        if (r == 0):
            flash("Invalid email and password!!")
            return redirect(url_for('company_login'))
        else:
            return redirect(url_for('company_dashboard'))


@app.route("/company_logout")
def company_logout():
    session.clear()
    return redirect(url_for('company_login'))


@app.route("/company_dashboard")
def company_dashboard():
    if 'company_email' in session:
        return render_template("company_dashboard.html")
    else:
        flash("kindly login to access this page!!")
        return redirect(url_for('company_login'))


@app.route("/company_profile")
def company_profile():
    if 'company_email' in session:
        op = company_operation()  # object create
        r = op.company_profile()
        return render_template("company_profile.html", record=r)
    else:
        flash("kindly login to access this page!!")
        return redirect(url_for('company_login'))


@app.route("/company_profile_update", methods=['POST', 'GET'])
def company_profile_update():
    if 'company_email' in session:
        if request.method == 'POST':
            name = request.form['name']
            mobile = request.form['mobile']
            address = request.form['address']
            op = company_operation()  # object create
            op.company_profile_update(name, mobile, address)
            flash("Your profile is updated successfully!!")
            return redirect(url_for('company_profile'))
    else:
        flash("kindly login to access this page!!")
        return redirect(url_for('company_login'))


@app.route("/company_password_form")
def company_password_form():
    if 'company_email' in session:
        return render_template("company_password_form.html")
    else:
        flash("kindly login to access this page!!")
        return redirect(url_for('company_login'))


@app.route("/company_password_change", methods=['POST', 'GET'])
def company_password_change():
    if 'company_email' in session:
        if request.method == 'POST':
            oldpassword = request.form['oldpassword']
            newpassword = request.form['newpassword']

            # --- password encryption----------------
            pas = hashlib.md5(oldpassword.encode())
            oldpassword = pas.hexdigest()

            pas = hashlib.md5(newpassword.encode())
            newpassword = pas.hexdigest()

            op = company_operation()  # object create
            r = op.company_password_change(oldpassword, newpassword)
            if (r == 0):
                flash("Your old password is invalid!!")
                return redirect(url_for('company_password_form'))
            else:
                session.clear()
                flash("Your password is updated successfully..login now!!")
                return redirect(url_for('company_login'))
    else:
        flash("kindly login to access this page!!")
        return redirect(url_for('company_login'))


@app.route("/company_job_post")
def company_job_post():
    if 'company_email' in session:
        return render_template("company_job_post.html")
    else:
        flash("kindly login to acces this page!!")
        return redirect(url_for('company_login'))


@app.route("/company_job_post_insert", methods=['POST', 'GET'])
def company_job_post_insert():
    if 'company_email' in session:
        if request.method == 'POST':
            job_name = request.form['job_name']
            no_of_post = request.form['no_of_post']
            eligibility = request.form['eligibility']
            qualification = request.form['qualification']
            exp = request.form['exp']
            apply_date = request.form['apply_date']
            descp = request.form['descp']
            photo_obj = request.files['photo']
            photo = photo_obj.filename
            photo_obj.save("static/job/" + photo)
            op = company_operation()
            op.company_job_post_insert(
                job_name, no_of_post, eligibility, qualification, exp, apply_date, descp, photo)
            flash("your job is posted successfully !")
            return redirect(url_for('company_job_post'))
    else:
        flash("kindly login to acces this page!!")
        return redirect(url_for('company_login'))


@app.route("/company_job_list")
def company_job_list():
    if 'company_email' in session:
        op = company_operation()
        r = op.company_job_list()
        return render_template("company_job_list.html", record=r)
    else:
        flash("kindly login to acces this page!!")
        return redirect(url_for('company_login'))


@app.route("/company_job_delete", methods=['POST', 'GET'])
def company_job_delete():
    if 'company_email' in session:
        job_id = request.args.get('job_id')
        op = company_operation()
        op.company_job_delete(job_id)
        flash("job deleted successfully !")
        return render_template("company_job_list.html")
    else:
        flash("kindly login to acces this page!!")
        return redirect(url_for('company_login'))


@app.route("/company_job_applied_view", methods=['POST', 'GET'])
def company_job_applied_view():
    if 'company_email' in session:
        job_id = request.args.get('job_id')
        op = company_operation()  # object create
        r = op.company_job_applied_view(job_id)
        return render_template("company_job_applied_view.html", record=r)
    else:
        flash("kindly login to access this page!!")
        return redirect(url_for('company_login'))


if __name__ == "__main__":
    app.run(debug=True)
