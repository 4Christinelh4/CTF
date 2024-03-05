
class CrudUser:
    def __init__(self, conn) -> None:
        self.connection = conn

    def addUser(self, username, email, hashed_pw):
        cur = self.connection.cursor()
        cur.execute('''insert into person (name, password, email) values (%s, %s, %s)''', (username, hashed_pw, email))
        self.connection.commit()
        cur.close()

    def change_password(self, email, new_pw):
        cur = self.connection.cursor()
        cur.execute('''update person set password = %s where email = %s''', (new_pw, email))
        # Get the number of rows updated
        updated_rows = cur.rowcount

        self.connection.commit()
        cur.close()

        return updated_rows
    
    def getUserSize(self):
        cur = self.connection.cursor()
        cur.execute('''select count(*) from person''')
        sz = cur.fetchone()[0]
        cur.close()
        return sz

    def searchUser(self, username, password):
        # print(f"[DEBUG]: search user {username}, {password}")
        cur = self.connection.cursor()
    
        # sql injection~
        # SPOILER: 
        # select name, password from person where name = '' or 1=1 union select 'a', current_database();
        # ' or 1=1 union select 'a', current_database() ; --

        # this will show all tables
        # select * from information_schema.tables where table_catalog = 'comp6841db' and table_schema = 'public';
        # in this case, only show the top_secret table!!!!!

        # select name, password from person where name = '' union select '1',
        # table_name from information_schema.tables where table_catalog = 'comp6841db' and table_schema = 'public'; -- 
        # this is where the injection happens !
        query = "select name, password from person where name = '" + username + "' and password = '" + password + "';"
        # check if the query is select all tables, because 'public' is very particular in pgsql
        # ' union select something, table_name from information_schema.tables where table_catalog = '';

        cur.execute(query)
        rows = cur.fetchall()
        results = []

        for r in rows:
            n, p = r
            results.append((n, p))
        cur.close()

        def check_sql_top_secret(query_results):
            for each_pair in query_results:
                if each_pair[1] ==  'top_secret' or each_pair[0] == 'top_secret':
                    return (True, each_pair)
            return (False, ())

        checker = check_sql_top_secret(results)
        # ' union select '1', table_name from information_schema.tables where table_catalog = 'comp6841db' and table_schema = 'public'; -- 
        if checker[0]:
            print("don't show all tables!")
            return ([checker[1]], True)
        
        return (results, False)

    def getAllCourses(self):
        cur = self.connection.cursor()
        cur.execute('''select course_name, description from course''')
        rows = cur.fetchall()

        cur.close()
        res = []
        for c in rows:
            res.append({'name': c[0], 'description': c[1]})
        return res
    
    def searchAllPrerequisites (self, course_name):
        cur = self.connection.cursor()
        cur.execute('''select pre_id from prerequsite where course_id = (select id from \
                    course where course_name = %s )''', (course_name, ))
        
        rows = cur.fetchall()
        res = [tmp[0] for tmp in rows]
        cur.close()
        return res
    
    def searchAllCourseForUser(self, username):
        res = []
        cur = self.connection.cursor()
        cur.execute('''select c.course_name,  sc.status from course c right join student_course sc on c.id=sc.course_id where \
                    sc.student_id = (select id from person where name = %s )''', (username, ))

        rows = cur.fetchall()
        for r in rows:
            res.append({'name': r[0], 'status': r[1]})
        cur.close()

        for each in res:
            print(f'[DEBUG] {each}')
        return res

    def searchAllCoursePassed(self, username):
        cur = self.connection.cursor()
        cur.execute('''select course_id from student_course where status = 't' and student_id = (SELECT id from person \
                    where name= %s )''', (username, ))
        rows = cur.fetchall()
        res = [tmp[0] for tmp in rows]
        cur.close()
        return res
    
    def searchCourseByName(self, course_name):
        cur = self.connection.cursor()
        query_search = f'select id, course_name, description from course where course_name=\'{course_name}\''
        print(f"searchCourseByName: {query_search}")
        cur.execute(query_search)
        
        rows = cur.fetchall() # rows = [('COMP9311 DB management', 'a course on database management systems')]
        # print(f'search course by name - rows = {rows}')
        cur.close()
        return {'id': rows[0][0], 'name': rows[0][1], 'description': rows[0][1]}

    def addCourseToUser(self, course_name, username):
        print(f"ADD {course_name} to {username}")
        cur = self.connection.cursor()
        query_course= f"select id from course where course_name = '{course_name}' "
        cur.execute(query_course)
        course_id = int(cur.fetchall()[0][0]) 

        # find the student id
        query_student = f"select id from person where name = '{username}' "
        cur.execute(query_student)

        student_id = int(cur.fetchall()[0][0])
        # print(f"course_id = {course_id}, studend_id = {student_id}")
        query = f"insert into student_course values ({student_id}, {course_id}, 'f')"

        cur.execute(query)
        self.connection.commit()
        cur.close()

    def insertCommentOnCourse(self, course_id, single_comment):
        cur = self.connection.cursor()
        # query = f"insert into course_comment values ({course_id}, '{single_comment}')"
        cur.execute('''insert into course_comment values (%s, %s)''', (course_id, single_comment, ))
        # print("insert result = ", result)
        self.connection.commit()
        cur.close()

    # remove xss comment
    def remove_xss_comment(self, course_id, single_comment):
    #     print("remove xss comment")
        cur = self.connection.cursor()
        cur.execute('''delete from course_comment where course_id=%s and comment=%s''', (course_id, single_comment))
        self.connection.commit()
        cur.close()

    def selectAllCommentsByCourse(self, course_id):
        # return ["It's good", f"{course_name} is best one I've ever taken!!"]
        cur = self.connection.cursor()
        cur.execute('''select comment from course_comment where course_id = %s ''', (course_id, ))
        rows = cur.fetchall()
        cur.close()
        return [i[0] for i in rows]