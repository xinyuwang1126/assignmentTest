#!/usr/bin/python
from Tkinter import *
import ttk
import tkMessageBox
import pymysql
import time

hostname = 'academic-mysql.cc.gatech.edu'
username = 'cs4400_Team_87'
database = 'cs4400_Team_87'
password = 'sQ0k8QOS'

yearList = ['Freshman', 'Sophomore', 'Junior', 'Senior']


class sysDB:
    def __init__(self):
        # connect to db
        self.db = pymysql.connect(host=hostname, user=username, db=database, passwd=password)
        self.cursor = self.db.cursor()
        self.Login()


    def Login(self):
        # Login Page
        login_page = Tk()
        login_page.geometry("%dx%d+%d+%d" % (450, 150, 300, 20))
        self.login_page = login_page
        self.current_page = self.login_page
        login_page.title('login')

        topFrame = Frame(login_page)
        topFrame.pack()
        bottomFrame = Frame(login_page)
        bottomFrame.pack()

        # username
        self.Username = StringVar()
        Label(topFrame, text='Username:').grid(row=1, sticky=E, padx=10, pady=5)
        Entry(topFrame, width=20, textvariable=self.Username).grid(row=1, column=2, sticky=W, pady=5)

        # password
        self.Password = StringVar()
        Label(topFrame, text='Password:').grid(row=2, sticky=E, padx=10, pady=5)
        Entry(topFrame, width=20, textvariable=self.Password, show="*").grid(row=2, column=2, sticky=W, pady=5)

        # create 'Login' & 'Register' Button
        Button(bottomFrame, text='Register', width=10, command=self.createNewUser).grid(row=1, column=1, sticky=E)
        Button(bottomFrame, text='Login', width=10, command=self.checkLogin).grid(row=1, column=2, sticky=W, padx=10,
                                                                                  pady=20)

    def checkLogin(self):
        # Check if user exists
        self.curUsername = self.Username.get()
        self.curPassword = self.Password.get()
        self.cursor.execute("SELECT COUNT(*) FROM USER WHERE Username=%s AND Password=%s",
                            (self.curUsername, self.curPassword))
        (Exist,) = self.cursor.fetchone()

        if Exist == 1:
            # tkMessageBox.showinfo("Login Successful","Login Successful!")
            self.cursor.execute("SELECT Email,Major,Year,UserType FROM USER WHERE Username=%s AND Password=%s",
                                (self.curUsername, self.curPassword))
            (self.GTEmail, self.Major, self.Year, self.UserType) = self.cursor.fetchone()
            if self.UserType == 'STUDENT':
                self.gotoMainPage()
            else:
                self.gotoAdminMainPage()
        else:
            self.Password.set("")
            tkMessageBox.showwarning("Login Failure", "The Username or Password is incorrect.")

    def createNewUser(self):
        # Create new User (username, password, email)
        self.current_page.withdraw()
        register_page = Toplevel()
        register_page.geometry("%dx%d+%d+%d" % (450, 250, 300, 20))
        register_page.title("New Student Registration")
        self.register_page = register_page
        self.current_page = self.register_page

        topFrame = Frame(register_page)
        topFrame.pack()
        bottomFrame = Frame(register_page)
        bottomFrame.pack()

        self.newUsername = StringVar()
        Label(topFrame, text='Username:').grid(row=1, column=1, sticky=E, padx=15, pady=5)
        Entry(topFrame, width=20, textvariable=self.newUsername).grid(row=1, column=2, sticky=W, pady=5)

        self.newGTEmail = StringVar()
        Label(topFrame, text='GT Email Address:').grid(row=2, column=1, sticky=E, padx=15, pady=5)
        Entry(topFrame, width=20, textvariable=self.newGTEmail).grid(row=2, column=2, sticky=W, pady=5)

        self.newPassword = StringVar()
        Label(topFrame, text='Password:').grid(row=3, column=1, sticky=E, padx=15, pady=5)
        Entry(topFrame, width=20, textvariable=self.newPassword).grid(row=3, column=2, sticky=W, pady=5)

        self.newPwdConfirm = StringVar()
        Label(topFrame, text='Confirm Password:').grid(row=4, column=1, sticky=E, padx=15, pady=5)
        Entry(topFrame, width=20, textvariable=self.newPwdConfirm).grid(row=4, column=2, sticky=W, pady=5)

        Button(bottomFrame, text='Create', width=10, command=self.checkNewUser).grid(row=1, column=1, padx=10, pady=20)
        Button(bottomFrame, text='Back', width=10, command=self.backToLogin).grid(row=1, column=2, padx=10, pady=20)

    def backToLogin(self):
        self.current_page.withdraw()
        self.current_page = self.login_page
        self.login_page.deiconify()

    def checkNewUser(self):
        # Check the user inputs
        if self.newUsername.get() == "":
            tkMessageBox.showwarning("Error", "The username cannot be empty!")
            return None
        if not self.newGTEmail.get().endswith('@gatech.edu'):
            tkMessageBox.showwarning("Error", "Please provide a valid GT Email address!")
            return None
        if self.newPassword.get() == "":
            tkMessageBox.showwarning("Error", "The password cannot be empty!")
            return None
        if self.newPassword.get() != self.newPwdConfirm.get():
            tkMessageBox.showwarning("Error", "The passwords are not the same!")
            return None

        # Check if user already exists
        self.cursor.execute("SELECT COUNT(*) FROM USER WHERE Username=%s", self.newUsername.get())
        (Exist,) = self.cursor.fetchone()
        if Exist > 0:
            tkMessageBox.showwarning("Error", "Username already exists!")
            return None

        # Check if email already exists
        self.cursor.execute("SELECT COUNT(*) FROM USER WHERE Email=%s", self.newGTEmail.get())
        (Exist,) = self.cursor.fetchone()
        if Exist > 0:
            tkMessageBox.showwarning("Error", "Email already exists!")
            return None

        self.cursor.execute("INSERT INTO USER VALUES (%s,%s,%s,NULL,NULL,'STUDENT')",
                            (self.newUsername.get(), self.newPassword.get(), self.newGTEmail.get()))
        self.db.commit()
        tkMessageBox.showinfo("Register Success", "Your account has been created! Please continue to login!")
        self.backToLogin()

    def gotoAdminMainPage(self):
        # Create Admin Main Page
        self.current_page.withdraw()
        admin_main_page = Toplevel()
        admin_main_page.geometry("%dx%d+%d+%d" % (300, 350, 0, 0))
        admin_main_page.title("Administer Main Page")
        self.admin_main_page = admin_main_page
        self.current_page = self.admin_main_page

        chooseFunc = Label(admin_main_page, text="Choose Functionality", font=("Helvetica", 22), fg="gold").grid(row=0,
                                                                                                                 column=5,
                                                                                                                 sticky=W,
                                                                                                                 padx=40,
                                                                                                                 pady=5)
        Button(admin_main_page, text='View Applications', width=10, relief=SUNKEN,
               command=self.viewStudentApplication).grid(row=1, column=5, ipadx=30, pady=10)
        Button(admin_main_page, text='View popular project report', width=10,
               command=self.viewPopularProjectReport).grid(row=2, column=5, ipadx=50, pady=10)
        Button(admin_main_page, text='View Application report', width=10, command=self.viewApplicationReport).grid(
            row=3, column=5, ipadx=40, pady=10)
        Button(admin_main_page, text='Add a Project', width=10, command=self.addProject).grid(row=4, column=5, pady=10)
        Button(admin_main_page, text='Add a Course', width=10, command=self.addCourse).grid(row=5, column=5, pady=10)
        Button(admin_main_page, text='Log out', width=5, command=self.Logout).grid(row=6, column=5, ipadx=10, pady=25)

    def gotoMainPage(self):
        # Create Main Page
        self.current_page.withdraw()
        main_page = Toplevel()
        main_page.geometry("%dx%d+%d+%d" % (11200, 750, 100, 0))
        main_page.title("Main Page")
        self.main_page = main_page
        self.current_page = self.main_page

        frame1 = Frame(main_page)
        frame1.pack()
        frame2 = Frame(main_page)
        frame2.pack()
        frame3 = Frame(main_page)
        frame3.pack()
        frame4 = Frame(main_page)
        frame4.pack()

        Button(frame1, text='Logout', width=5, command=self.Logout).grid(row=1, column=4, padx=10, pady=20)
        welcome = Label(frame1, text='Welcome to Gatech Course and Project Center!', fg='RoyalBlue4',
                        font="-weight bold")
        welcome.grid(row=1, column=3, padx=70)
        welcome.config(font=("Courier", 30), )

        # 'Me' icon
        me_image = PhotoImage(file="me.gif")  # .subsample(5, 5)
        self.me_img = me_image
        me = Button(frame1, command=self.viewMyInfo)
        me.config(image=me_image)
        me.grid(row=1, column=1, sticky=S)

        me_text = Label(frame1, text="Me", fg='Gold')
        me_text.grid(row=1, column=2, sticky="W" + "S")
        me_text.config(font=("Courier", 20), )

        # Add searching title
        self.searchTitle = StringVar()
        Label(frame2, text='Title:').grid(row=1, column=2, sticky=E, padx=15, pady=5)
        Title_search = Entry(frame2, width=20, textvariable=self.searchTitle)
        Title_search.grid(row=1, column=3, sticky=W, pady=5)
        Title_search.config(width=30)

        # Populate Options from database
        cat_OPTIONS = ['']
        dsg_OPTIONS = ['']
        mj_OPTIONS = ['']
        yr_OPTIONS = [''] + yearList

        self.cursor.execute("SELECT Name FROM CATEGORY")
        categories = self.cursor.fetchall()
        for category in categories:
            (curCategory,) = category
            cat_OPTIONS.append(curCategory)

        self.cursor.execute("SELECT Name FROM DESIGNATION")
        designations = self.cursor.fetchall()
        for designation in designations:
            (curDesignation,) = designation
            dsg_OPTIONS.append(curDesignation)

        self.cursor.execute("SELECT Name FROM MAJOR")
        majors = self.cursor.fetchall()
        for major in majors:
            (curMajor,) = major
            mj_OPTIONS.append(curMajor)

        # Choose Category
        self.mainCatFilter_count = 1
        cur_idx = self.mainCatFilter_count - 1
        Label(frame2, text='Category:').grid(row=1, column=4, sticky=E, padx=15, pady=5)
        cat1 = StringVar()
        cat2 = StringVar()
        cat3 = StringVar()
        cat4 = StringVar()
        self.cat_variable_list = [cat1, cat2, cat3, cat4]
        self.cat_variable_list[cur_idx].set(cat_OPTIONS[0])  # default value
        category_dropdown = apply(OptionMenu, (frame2, self.cat_variable_list[cur_idx]) + tuple(cat_OPTIONS))
        category_dropdown.config(width=30)
        category_dropdown.grid(row=1, column=5, sticky=W, pady=5)

        # add more category filters
        addCate = Button(frame2, text="add a Category", command=lambda: self.addCate_filter(cat_OPTIONS, frame2))
        addCate.grid(row=1, column=6, sticky=S, pady=5)

        # Choose Designation
        Label(frame2, text='Designation:').grid(row=2, column=2, sticky=E, padx=15, pady=5)
        self.dsg_variable = StringVar()
        self.dsg_variable.set(dsg_OPTIONS[0])  # default value
        dsg_dropdown = apply(OptionMenu, (frame2, self.dsg_variable) + tuple(dsg_OPTIONS))
        dsg_dropdown.config(width=30)
        dsg_dropdown.grid(row=2, column=3, sticky=W, pady=5)

        # Choose Major
        Label(frame2, text='Major:').grid(row=3, column=2, sticky=E, padx=15, pady=5)
        self.mj_variable = StringVar()
        self.mj_variable.set(mj_OPTIONS[0])  # default value
        mj_dropdown = apply(OptionMenu, (frame2, self.mj_variable) + tuple(mj_OPTIONS))
        mj_dropdown.config(width=30)
        mj_dropdown.grid(row=3, column=3, sticky=W, pady=5)

        # Choose Year
        Label(frame2, text='Year:').grid(row=4, column=2, sticky=E, padx=15, pady=5)
        self.yr_variable = StringVar()
        self.yr_variable.set(yr_OPTIONS[0])  # default value
        yr_dropdown = apply(OptionMenu, (frame2, self.yr_variable) + tuple(yr_OPTIONS))
        yr_dropdown.config(width=30)
        yr_dropdown.grid(row=4, column=3, sticky=W, pady=5)

        # Check if include courses
        self.isCourse = IntVar()
        Checkbutton(frame3, text="Course", variable=self.isCourse).grid(row=1, column=1, sticky=E, padx=20, pady=10)

        # Check if include projects
        self.isProject = IntVar()
        Checkbutton(frame3, text="Project", variable=self.isProject).grid(row=1, column=2, sticky=W, padx=20, pady=10)

        # Filter apply / reset button
        Button(frame3, text='Apply Filter', width=10, command=self.searchCourseProject).grid(row=2, column=1, padx=10,
                                                                                             pady=20)
        Button(frame3, text='Reset Filter', width=10, command=self.gotoMainPage).grid(row=2, column=2, padx=10, pady=20)

        # Filter Results
        self.filterResults = ttk.Treeview(frame4, height=16)
        self.filterResults['columns'] = ('Name', 'Type')
        self.filterResults.heading("#0", text='', anchor='w')
        self.filterResults.column("#0", stretch=NO, width=2, anchor="w")
        self.filterResults.heading('Name', text='Name')
        self.filterResults.column('Name', anchor='center', width=800)
        self.filterResults.heading('Type', text='Type')
        self.filterResults.column('Type', anchor='center', width=100)
        self.filterResults.bind('<ButtonRelease-1>', self.viewCourseProject)
        self.filterResults.grid(row=1, column=0, columnspan=20, padx=5, pady=5)
        ttk.Style().configure('Treeview', font=('', 14))

    def addCate_filter(self, cat_option_copy, mainCatFilterFrame):
        if self.mainCatFilter_count < 4:
            self.mainCatFilter_count += 1
            cur_idx = self.mainCatFilter_count - 1
            # Choose Category
            Label(mainCatFilterFrame, text='Category:').grid(row=self.mainCatFilter_count, column=4, sticky=E, padx=15,
                                                             pady=5)
            self.cat_variable_list[cur_idx].set(cat_option_copy[0])  # default value
            category_dropdown = apply(OptionMenu,
                                      (mainCatFilterFrame, self.cat_variable_list[cur_idx]) + tuple(cat_option_copy))
            category_dropdown.config(width=30)
            category_dropdown.grid(row=self.mainCatFilter_count, column=5, sticky=W, pady=5)

    def searchCourseProject(self):
        item = self.filterResults.get_children()
        self.filterResults.delete(*item)
        curResults = []

        # Preprocess of all selected categories
        cat_variable_list = []
        for s in self.cat_variable_list:
            cat_variable_list.append(s.get())
        cat_variable_list = filter(None, cat_variable_list)

        # Search Course (check title, designation, category)
        course_title_requirement = '%'
        course_cat_requirement = '%'
        course_dsg_requirement = '%'
        if self.searchTitle.get() != '':
            course_title_requirement = self.searchTitle.get()
        if self.dsg_variable.get() != '':
            course_dsg_requirement = self.dsg_variable.get()

        if self.isCourse.get() == 1:
            # if no category provided, it can be any category
            if len(cat_variable_list) == 0:
                self.cursor.execute(
                    "SELECT Name FROM COURSE WHERE Designation_name LIKE %s AND Name IN (SELECT DISTINCT Course_name FROM COURSE_IS_CATEGORY WHERE Course_name LIKE %s AND Category_name LIKE %s)",
                    (course_dsg_requirement, course_title_requirement, course_cat_requirement))
                for (course,) in self.cursor.fetchall():
                    curResults.append((course, 'Course'))

                    # if there are categories specified, we loop through them
            for i in range(0, len(cat_variable_list)):
                self.cat_variable = cat_variable_list[i]
                course_cat_requirement = self.cat_variable
                self.cursor.execute(
                    "SELECT Name FROM COURSE WHERE Designation_name LIKE %s AND Name IN (SELECT DISTINCT Course_name FROM COURSE_IS_CATEGORY WHERE Course_name LIKE %s AND Category_name LIKE %s)",
                    (course_dsg_requirement, course_title_requirement, course_cat_requirement))
                for (course,) in self.cursor.fetchall():
                    curResults.append((course, 'Course'))

        # Search Project
        project_title_requirement = '%'
        project_cat_requirement = '%'
        project_dsg_requirement = '%'
        if self.searchTitle.get() != '':
            project_title_requirement = self.searchTitle.get()
        if self.dsg_variable.get() != '':
            project_dsg_requirement = self.dsg_variable.get()

        if self.isProject.get() == 1:
            # PART I: check title, designation, category
            # if no category specified
            candidates = []
            if len(cat_variable_list) == 0:
                self.cursor.execute(
                    "SELECT Name FROM PROJECT WHERE Designation LIKE %s AND Name IN (SELECT Project_name FROM PROJECT_IS_CATEGORY WHERE Category_name LIKE %s AND Project_name LIKE %s)",
                    (project_dsg_requirement, project_cat_requirement, project_title_requirement))
                for (project,) in self.cursor.fetchall():
                    candidates.append(project)

                    # if there are categories specified
            for i in range(0, len(cat_variable_list)):
                self.cat_variable = self.cat_variable_list[i]
                project_cat_requirement = self.cat_variable.get()

                self.cursor.execute(
                    "SELECT Name FROM PROJECT WHERE Designation LIKE %s AND Name IN (SELECT Project_name FROM PROJECT_IS_CATEGORY WHERE Category_name LIKE %s AND Project_name LIKE %s)",
                    (project_dsg_requirement, project_cat_requirement, project_title_requirement))

                for (project,) in self.cursor.fetchall():
                    candidates.append(project)

                    # PART II: check year
            project_yr_requirement = ['Only Freshman students',
                                      'Only Sophomore students',
                                      'Only Junior students',
                                      'Only Senior students']

            yr_exceptions = []
            if self.yr_variable.get() != '':
                yr_constraint = 'Only ' + self.yr_variable.get() + ' students'
                project_yr_requirement.remove(yr_constraint)
                self.cursor.execute(
                    "SELECT Name FROM PROJECT_REQUIREMENT WHERE Requirement=%s OR Requirement=%s OR Requirement=%s",
                    (project_yr_requirement[0], project_yr_requirement[1], project_yr_requirement[2]))
                for (project,) in self.cursor.fetchall():
                    yr_exceptions.append(project)

                    # PART III: check year
            mj = 'all_major'
            dept = 'all_dept'
            if self.mj_variable.get() != '':
                mj = self.mj_variable.get()

            mj_exceptions = []
            if mj != 'all_major':
                self.cursor.execute("SELECT Dept_name FROM MAJOR WHERE Name=%s", mj)
                (dept,) = self.cursor.fetchone()
                mj = 'Only ' + mj + ' students'
                dept = 'Only' + dept + ' students'
                self.cursor.execute(
                    "SELECT Name FROM PROJECT_REQUIREMENT WHERE Requirement<>%s AND Requirement<>%s AND Requirement<>%s AND Requirement<>%s AND Requirement<>%s AND Requirement<>%s AND Requirement<>%s",
                    ('None', 'Only Freshman students', 'Only Sophomore students', 'Only Junior students',
                     'Only Senior students', mj, dept))

                for (project,) in self.cursor.fetchall():
                    mj_exceptions.append(project)

            candidates = list(set(candidates) - set(yr_exceptions) - set(mj_exceptions))

            for project in candidates:
                curResults.append((project, 'Project'))

        # Remove duplicates
        curResults = list(set(curResults))

        # Insert values
        for (i1, i2) in curResults:
            self.filterResults.insert('', 'end', values=(i1, i2))

        return None

    def viewCourseProject(self, event):
        item = self.filterResults.selection()[0]
        itemname = self.filterResults.item(item)['values'][0]
        itemtype = self.filterResults.item(item)['values'][1]
        if itemtype == 'Course':
            self.viewCourse(itemname)
        else:
            self.viewProject(itemname)

    def viewCourse(self, courseName):
        # Create course page
        self.current_page.withdraw()
        course_page = Toplevel()
        course_page.geometry("%dx%d+%d+%d" % (600, 350, 300, 20))
        course_page.title('Course Info')
        self.course_page = course_page
        self.current_page = self.course_page

        topFrame = Frame(course_page)
        topFrame.pack()
        middleFrame = Frame(course_page)
        middleFrame.pack()
        bottomFrame = Frame(course_page)
        bottomFrame.pack()

        self.cursor.execute("SELECT * FROM COURSE WHERE Name=%s", courseName)
        (courseName, courseNo, Instructor, EstSize, Dsg) = self.cursor.fetchone()
        self.cursor.execute("SELECT Category_name FROM COURSE_IS_CATEGORY WHERE Course_name=%s", courseName)
        Cats = []
        for (cat,) in self.cursor.fetchall():
            Cats.append(cat)
        Cats = '; '.join(Cats)

        courseNoLabel = Label(topFrame, text=courseNo, fg='Gold', pady=30)
        courseNoLabel.config(font=("Courier", 35))
        courseNoLabel.pack()

        Label(middleFrame, text="Course Name:  " + courseName).grid(row=1, sticky=W)
        Label(middleFrame, text="Instructor:  " + Instructor).grid(row=2, sticky=W)
        Label(middleFrame, text="Designation:  " + Dsg).grid(row=3, sticky=W)
        Label(middleFrame, text="Category:  " + Cats).grid(row=4, sticky=W)
        Label(middleFrame, text="Estimated number of students:  " + str(EstSize)).grid(row=5, sticky=W)
        # Create a 'Back' Button
        Button(bottomFrame, text='Back', width=10, command=self.backToMainPage).grid(row=1, column=2, sticky=W, padx=20,
                                                                                     pady=40)

    def viewProject(self, projectName):
        # Create project page
        self.current_page.withdraw()
        project_page = Toplevel()
        project_page.geometry("%dx%d+%d+%d" % (770, 480, 300, 20))
        project_page.title('Project Info')
        self.project_page = project_page
        self.current_page = self.project_page

        topFrame = Frame(project_page)
        topFrame.pack()
        middleFrame = Frame(project_page)
        middleFrame.pack()
        bottomFrame = Frame(project_page)
        bottomFrame.pack()

        self.cursor.execute("SELECT * FROM PROJECT WHERE Name=%s", projectName)
        (projectName, Description, AdvisorEmail, AdvisorName, EstSize, Dsg) = self.cursor.fetchone()
        self.cursor.execute("SELECT Category_name FROM PROJECT_IS_CATEGORY WHERE Project_name=%s", projectName)
        Cats = []
        for (cat,) in self.cursor.fetchall():
            Cats.append(cat)
        Cats = '; '.join(Cats)

        self.cursor.execute("SELECT Requirement FROM PROJECT_REQUIREMENT WHERE Name=%s", projectName)
        Reqs = []
        for (req,) in self.cursor.fetchall():
            Reqs.append(req)
        Reqs = '; '.join(Reqs)

        projectNameLabel = Label(topFrame, text=projectName, fg='Gold', pady=30)
        if len(projectName) <= 26:
            font_size = 35
        elif len(projectName) >= 66:
            font_size = 18
        else:
            font_size = -0.425 * len(projectName) + 46.05
        projectNameLabel.config(font=("Courier", int(round(font_size))))
        projectNameLabel.pack()

        Label(middleFrame, text="Advisor:  " + AdvisorName + '(' + AdvisorEmail + ')').grid(row=1, sticky=W)
        Label(middleFrame, text="Description:  ").grid(row=2, sticky=W)
        describe_text = Message(middleFrame, text=Description, width=550)
        describe_text.grid(row=3, sticky=W)
        Label(middleFrame, text="Designation:  " + Dsg).grid(row=4, sticky=W)
        Label(middleFrame, text="Category:  " + Cats).grid(row=5, sticky=W)
        Label(middleFrame, text="Requirements:  " + Reqs).grid(row=6, sticky=W)
        Label(middleFrame, text="Estimated number of students:  " + str(EstSize)).grid(row=7, sticky=W)

        # Create a 'Back' & 'Apply' Button
        Button(bottomFrame, text='Back', width=10, command=self.backToMainPage).grid(row=1, column=1, sticky=W, padx=20)
        Button(bottomFrame, text='Apply', width=10, command=lambda: self.applyProject(projectName)).grid(row=1,
                                                                                                         column=2,
                                                                                                         sticky=W,
                                                                                                         padx=20,
                                                                                                         pady=40)

    def viewMyInfo(self):
        # Create my Info homepage
        self.current_page.withdraw()
        me_page = Toplevel()
        me_page.geometry("%dx%d+%d+%d" % (300, 400, 300, 20))
        me_page.title("Me")
        self.me_page = me_page
        self.current_page = self.me_page

        topFrame = Frame(me_page)
        topFrame.pack()
        bottomFrame = Frame(me_page)
        bottomFrame.pack()

        me = Label(topFrame, text="Me", fg='Gold')
        me.grid(row=1, column=1, sticky=S)
        me.config(font=("Courier", 35))
        mini = Label(topFrame)
        mini.config(image=self.me_img)
        mini.grid(row=2, column=1, padx=30, sticky=N, pady=2)

        Button(bottomFrame, text='Edit Profile', width=10, command=self.editProfile).grid(row=2, padx=20, pady=20)
        Button(bottomFrame, text='My Applications', width=10, command=self.viewMyApplication).grid(row=3, padx=20)
        Button(bottomFrame, text='Back', width=10, command=self.backToMainPage).grid(row=4, padx=10, pady=40)

    def backToMainPage(self):
        self.current_page.withdraw()
        self.current_page = self.main_page
        self.main_page.deiconify()

    def editProfile(self):
        # Create Profile Page
        self.current_page.withdraw()
        profile_page = Toplevel()
        profile_page.geometry("%dx%d+%d+%d" % (600, 300, 300, 20))
        profile_page.title("Edit Profile")
        self.profile_page = profile_page
        self.current_page = self.profile_page

        topFrame = Frame(profile_page)
        topFrame.pack()
        bottomFrame = Frame(profile_page)
        bottomFrame.pack()

        mini = Label(topFrame)
        mini.config(image=self.me_img)
        mini.grid(row=1, column=1, padx=30, pady=2)
        me = Label(topFrame, text="Edit Profile", fg='Gold')
        me.grid(row=1, column=2, pady=25)
        me.config(font=("Courier", 35))

        # Populate the OPTIONS
        mj_OPTIONS = []
        yr_OPTIONS = yearList
        dept_OPTIONS = []

        self.cursor.execute("SELECT Name FROM MAJOR")
        majors = self.cursor.fetchall()
        for major in majors:
            (curMajor,) = major
            mj_OPTIONS.append(curMajor)

        self.cursor.execute("SELECT DISTINCT Dept_name FROM MAJOR")
        depts = self.cursor.fetchall()
        for dept in depts:
            (curDept,) = dept
            dept_OPTIONS.append(curDept)

        # Major
        Label(bottomFrame, text='Major').grid(row=1, column=1, sticky=E, padx=15, pady=5)
        self.newMajor = StringVar()
        self.newMajor.set(self.Major)
        mj_dropdown = apply(OptionMenu, (bottomFrame, self.newMajor) + tuple(mj_OPTIONS))
        mj_dropdown.config(width=25)
        mj_dropdown.grid(row=1, column=2, sticky=W, pady=5)

        # Year
        Label(bottomFrame, text='Year:').grid(row=2, column=1, sticky=E, padx=15, pady=5)
        self.newYear = StringVar()
        self.newYear.set(self.Year)
        yr_dropdown = apply(OptionMenu, (bottomFrame, self.newYear) + tuple(yr_OPTIONS))
        yr_dropdown.config(width=12)
        yr_dropdown.grid(row=2, column=2, sticky=W, pady=5)

        # Update department handler
        def change_dept():
            curMajor = self.newMajor.get()
            if curMajor:
                self.cursor.execute("SELECT Dept_name FROM MAJOR WHERE Name=%s", curMajor)
                (dept,) = self.cursor.fetchone()
                self.newDept.set(dept)

        # Department
        Label(bottomFrame, text='Department:').grid(row=3, column=1, sticky=E, padx=15, pady=5)
        self.newDept = StringVar()
        if self.newMajor.get() == 'None':
            self.newDept.set('None')  # default value
        else:
            change_dept()
        dept_dropdown = apply(OptionMenu, (bottomFrame, self.newDept) + tuple(dept_OPTIONS))
        dept_dropdown.config(width=25)
        dept_dropdown.grid(row=3, column=2, sticky=W, pady=5)

        # Trace the major selection
        self.newMajor.trace('w', lambda *args: change_dept())

        # create 'Update (Profile)' & 'Back' Button
        Button(bottomFrame, text='Update', width=10, command=self.updateProfile).grid(row=5, column=2, padx=10, pady=40,
                                                                                      sticky=E)
        Button(bottomFrame, text='Back', width=10, command=self.backToMePage).grid(row=5, column=1, padx=10, pady=40,
                                                                                   sticky=W)

    def backToMePage(self):
        self.current_page.withdraw()
        self.current_page = self.me_page
        self.me_page.deiconify()

    def updateProfile(self):
        # Check if inputs meet the requirements
        if self.newYear.get() == 'None' or self.newMajor.get() == 'None':
            tkMessageBox.showwarning("Update Failure", "Please fill in all the required fields!")
            return None

        self.cursor.execute("SELECT COUNT(*) FROM MAJOR WHERE Name=%s AND Dept_name=%s",
                            (self.newMajor.get(), self.newDept.get()))

        (Exist,) = self.cursor.fetchone()
        if Exist != 1:
            tkMessageBox.showwarning("Update Failure", "Your Major and Department do not match!")
            return None

        # Update the varibales
        self.Major = self.newMajor.get()
        self.Year = self.newYear.get()

        # Update the info in db
        self.cursor.execute("UPDATE USER SET Year=%s, Major=%s WHERE Username=%s",
                            (self.newYear.get(), self.newMajor.get(), self.curUsername))
        tkMessageBox.showinfo("Update Success", "You have successfully updated your profile!")
        self.db.commit()

    def viewMyApplication(self):
        # Create View My Application Page
        self.current_page.withdraw()
        application_page = Toplevel()
        application_page.title("My Application")
        application_page.geometry("%dx%d+%d+%d" % (900, 300, 300, 100))
        self.application_page = application_page
        self.current_page = self.application_page

        topFrame = Frame(application_page)
        topFrame.pack()
        bottomFrame = Frame(application_page)
        bottomFrame.pack()
        frame3 = Frame(application_page)
        frame3.pack()

        me = Label(topFrame, text="My Application", fg='Gold')
        me.config(font=("Courier", 35))
        me.pack()

        # Application Items
        self.cursor.execute("SELECT Date,Project_name,Status FROM APPLY WHERE Student_name=%s", self.curUsername)
        curResults = self.cursor.fetchall()

        # Filter Results
        self.student_application = ttk.Treeview(bottomFrame, height=8)
        self.student_application['columns'] = ('Date', 'Project Name', 'Status')
        self.student_application.heading("#0", text='', anchor='w')
        self.student_application.column("#0", stretch=NO, width=2, anchor="w")

        self.student_application.heading('Date', text='Date')
        self.student_application.column('Date', anchor='center', width=80)

        self.student_application.heading('Project Name', text='Project Name')
        self.student_application.column('Project Name', anchor='center', width=700)

        self.student_application.heading('Status', text='Status')
        self.student_application.column('Status', anchor='center', width=80)

        self.student_application.grid(row=1, column=0, columnspan=20, padx=5, pady=5)
        ttk.Style().configure('Treeview', font=('', 14))

        for (date, project, status) in curResults:
            self.student_application.insert('', 'end', values=(str(date), project, status))

        # Create 'Back' Button
        Button(frame3, text='Back', width=20, command=self.backToMePage).pack()

    def backToApplication(self):
        self.current_page.withdraw()
        self.current_page = self.application_page
        self.application_page.deiconify()

    def applyProject(self, project):
        self.cursor.execute("SELECT COUNT(*) FROM APPLY WHERE Project_name=%s AND Student_name=%s",
                            (project, self.curUsername))
        date = time.strftime("%Y-%m-%d")
        (Exist,) = self.cursor.fetchone()
        if Exist == 1:
            tkMessageBox.askokcancel("Apply Failure", "Error: You cannot apply twice!")
        else:
            self.cursor.execute("INSERT INTO APPLY VALUES (%s,%s,%s,'Pending')", (project, self.curUsername, date))
            self.db.commit()
            tkMessageBox.showinfo("Apply Success",
                                  "You have successfully applied this project, go to your application page to check!")

    def viewStudentApplication(self):
        # Create a Page that contains all students' applications
        self.current_page.withdraw()
        view_application_page = Toplevel()
        view_application_page.title('Current Applications')
        view_application_page.geometry("%dx%d+%d+%d" % (1100, 500, 0, 0))
        self.view_application_page = view_application_page
        self.current_page = self.view_application_page

        # Present the table
        ttk.Style().configure("Treeview", font=('Helvetica', 12), foreground="blue")
        ViewAppTable = ttk.Treeview(view_application_page, height=20)
        ViewAppTable['columns'] = ('Project', 'Applicant Major', 'Applicant Year', 'Status')

        ViewAppTable.heading("#0", text='', anchor='w')
        ViewAppTable.column("#0", stretch=NO, width=2, anchor="w")
        ViewAppTable.heading('Project', text='Project')
        ViewAppTable.column('Project', anchor='center', width=400)
        ViewAppTable.heading('Applicant Major', text='Applicant Major')
        ViewAppTable.column('Applicant Major', anchor='center', width=300)
        ViewAppTable.heading('Applicant Year', text='Applicant Year')
        ViewAppTable.column('Applicant Year', anchor='center', width=200)
        ViewAppTable.heading('Status', text='Status')
        ViewAppTable.column('Status', anchor='center', width=200)
        ViewAppTable.bind('<ButtonRelease-1>', self.selectProject)
        ViewAppTable.grid(row=1, column=0, columnspan=20, padx=5, pady=6)
        self.ViewAppTable = ViewAppTable

        # Access the data
        self.cursor.execute("SELECT Project_name, Student_name, Status FROM APPLY")
        applications = self.cursor.fetchall()
        applicationList = []
        for application in applications:
            self.cursor.execute("SELECT Major, Year FROM USER WHERE Username=%s;", (application[1]))
            data = self.cursor.fetchone()
            applicationList.append((application[0], data[0], data[1], application[2], application[1]))

        for (i1, i2, i3, i4, i5) in applicationList:
            self.ViewAppTable.insert("", "end", values=(i1, i2, i3, i4, i5))

        # Add 'Accept' & 'Reject' & 'Back' Buttons
        Button(view_application_page, text='Back', command=self.backToAdminMainPage).grid(row=20, column=2, sticky=W)
        Button(view_application_page, text='Accept', command=self.acceptApplication).grid(row=20, column=16, sticky=W)
        Button(view_application_page, text='Reject', command=self.rejectApplication).grid(row=20, column=17, sticky=W)

    def backToAdminMainPage(self):
        self.current_page.withdraw()
        self.current_page = self.admin_main_page
        self.admin_main_page.deiconify()

    def selectProject(self, event):
        self.item = self.ViewAppTable.selection()[0]
        self.currentProjectName = self.ViewAppTable.item(self.item)['values'][0]
        self.currentMajor = self.ViewAppTable.item(self.item)['values'][1]
        self.currentYear = self.ViewAppTable.item(self.item)['values'][2]
        self.currentProjectStudent = self.ViewAppTable.item(self.item)['values'][4]
        self.currentStatus = self.ViewAppTable.item(self.item)['values'][3]

    def acceptApplication(self):
        if self.currentStatus != 'Pending':
            tkMessageBox.showwarning("Error", "This project is already processed!")
            return None
        else:
            self.cursor.execute("UPDATE APPLY SET Status='Accepted' WHERE Project_name=%s AND Student_name=%s",
                                (self.currentProjectName, self.currentProjectStudent))
            self.db.commit()
            self.ViewAppTable.delete(self.item)
            self.ViewAppTable.insert("", int(self.item[1:], 16) - 1, values=(
            self.currentProjectName, self.currentMajor, self.currentYear, 'Accepted', self.currentProjectStudent))
            tkMessageBox.showinfo("Success", "The application successfully is accepted!")

    def rejectApplication(self):
        if self.currentStatus != 'Pending':
            tkMessageBox.showwarning("Error", "This project is already processed!")
            return None
        else:
            self.cursor.execute("UPDATE APPLY SET Status='Rejected' WHERE Project_name=%s AND Student_name=%s",
                                (self.currentProjectName, self.currentProjectStudent))
            self.db.commit()
            self.ViewAppTable.delete(self.item)
            self.ViewAppTable.insert("", int(self.item[1:], 16) - 1, values=(
            self.currentProjectName, self.currentMajor, self.currentYear, 'Rejected', self.currentProjectStudent))
            tkMessageBox.showinfo("Success", "The application is successfully rejected!")

    def viewPopularProjectReport(self):
        # Create popular project page
        self.current_page.withdraw()
        popular_project_page = Toplevel()
        popular_project_page.title('Popular Project')
        popular_project_page.geometry("%dx%d+%d+%d" % (800, 350, 0, 0))
        self.popular_project_page = popular_project_page
        self.current_page = self.popular_project_page

        frame1 = Frame(popular_project_page)
        frame1.pack()
        frame2 = Frame(popular_project_page)
        frame2.pack()

        # Title
        Label(frame1, text="Popular Project", font=("Helvetica", 22), fg="gold").grid(row=0, column=1, sticky=W,
                                                                                      padx=60, pady=5)

        # Present popular projects
        ttk.Style().configure("Treeview", font=('Helvetica', 14))
        ViewPopProject = ttk.Treeview(frame1, height=10)
        ViewPopProject['columns'] = ('Project', '#ofApplicants')

        ViewPopProject.heading("#0", text='', anchor='w')
        ViewPopProject.column("#0", stretch=NO, width=2, anchor="w")
        ViewPopProject.heading('Project', text='Project')
        ViewPopProject.column('Project', anchor='center', width=500)
        ViewPopProject.heading('#ofApplicants', text='#ofApplicants')
        ViewPopProject.column('#ofApplicants', anchor='center', width=100)
        ViewPopProject.grid(row=1, column=1, padx=5, pady=6)

        self.cursor.execute(
            "SELECT Project_name, COUNT(*) FROM APPLY GROUP BY Project_name ORDER BY COUNT(*) DESC LIMIT 10;")
        for (project, no) in self.cursor.fetchall():
            ViewPopProject.insert("", "end", values=(project, no))

        # Create 'Back' Button
        Button(frame2, text='Back', command=self.backToAdminMainPage).grid(row=1, column=0, sticky=E)

    def viewApplicationReport(self):
        # Create application report page
        self.current_page.withdraw()
        application_report_page = Toplevel()
        application_report_page.title('Application Report')
        application_report_page.geometry("%dx%d+%d+%d" % (1300, 500, 0, 0))
        self.application_report_page = application_report_page
        self.current_page = self.application_report_page

        frame1 = Frame(application_report_page)
        frame1.pack()
        frame2 = Frame(application_report_page)
        frame2.pack()

        Label(frame1, text="Application Report", font=("Helvetica", 22), fg="gold").grid(row=0, column=0, sticky=W,
                                                                                         padx=40, pady=5)

        reportList = []
        self.cursor.execute(
            "SELECT Project_name ,count(*) AS total, SUM(CASE WHEN Status='Accepted' THEN 1 ELSE 0 END)*100/count(*) AS rate FROM APPLY GROUP By Project_name ORDER BY rate DESC")
        results = self.cursor.fetchall()
        for result in results:
            self.cursor.execute(
                "SELECT Major,count(*) FROM projStudent WHERE Project_name=%s GROUP BY Major ORDER BY count(*) DESC LIMIT 3",
                (result[0]))
            majors = self.cursor.fetchall()
            majorlist = []
            for each in majors:
                if each[0] != None:
                    majorlist.append(each[0])

            majorlist = ', '.join(majorlist)
            reportList.append([result[0], result[1], result[2], majorlist])

        ViewAppReport = ttk.Treeview(frame1, height=20)
        ViewAppReport['columns'] = ('Project', '#of Applicants', 'accept rate', 'top 3 major')
        ViewAppReport.heading("#0", text='', anchor='w')
        ViewAppReport.column("#0", stretch=NO, width=2, anchor="w")
        ViewAppReport.heading('Project', text='Project')
        ViewAppReport.column('Project', anchor='center', width=400)
        ViewAppReport.heading('#of Applicants', text='#of Applicants')
        ViewAppReport.column('#of Applicants', anchor='center', width=100)
        ViewAppReport.heading('accept rate', text='accept rate')
        ViewAppReport.column('accept rate', anchor='center', width=100)
        ViewAppReport.heading('top 3 major', text='top 3 major')
        ViewAppReport.column('top 3 major', anchor='center', width=600)
        ViewAppReport.grid(row=1, column=0, columnspan=20, padx=5, pady=6)
        ttk.Style().configure("Treeview", font=('', 14))

        for (i1, i2, i3, i4) in reportList:
            i3 = str(round(i3, 2)) + '%'
            ViewAppReport.insert("", "end", values=(i1, i2, i3, i4))

        Button(frame2, text='Back', command=self.backToAdminMainPage).grid(row=0, column=0, sticky=E)

    def addProject(self):
        # Add project page
        self.current_page.withdraw()
        add_project_page = Toplevel()
        add_project_page.title('Add a Project')
        add_project_page.geometry("%dx%d+%d+%d" % (650, 480, 0, 0))
        self.add_project_page = add_project_page
        self.current_page = self.add_project_page

        frame1 = Frame(add_project_page)
        frame1.pack()
        frame2 = Frame(add_project_page)
        frame2.pack()
        frame3 = Frame(add_project_page)
        frame3.pack()
        frame4 = Frame(add_project_page)
        frame4.pack()
        frame5 = Frame(add_project_page)
        frame5.pack()

        Label(frame2, text="Project Name").grid(row=0, column=2, sticky=W, padx=25, pady=5)
        Label(frame2, text="Advisor").grid(row=1, column=2, sticky=W, padx=25, pady=5)
        Label(frame2, text="Advisor Email").grid(row=2, column=2, sticky=W, padx=25, pady=5)
        Label(frame2, text="Description").grid(row=3, column=2, sticky=W, padx=25, pady=5)
        Label(frame3, text="Category").grid(row=0, column=2, sticky=W, pady=5)
        Label(frame4, text="Designation").grid(row=0, column=2, sticky=W, pady=5)
        Label(frame4, text="Estimated # of students").grid(row=1, column=2, pady=5, sticky=W)
        Label(frame4, text="Major Requirement").grid(row=2, column=2, pady=5, sticky=W)
        Label(frame4, text="Year Requirement").grid(row=3, column=2, pady=5, sticky=W)
        Label(frame4, text="Department Requirement").grid(row=4, column=2, pady=5, sticky=W)

        # User inputs
        cat1 = StringVar()
        cat2 = StringVar()
        cat3 = StringVar()
        cat4 = StringVar()
        self.newProject = StringVar()
        self.advisorName = StringVar()
        self.advisorEmail = StringVar()
        self.description = StringVar()
        self.projectCategoryList = [cat1, cat2, cat3, cat4]
        self.projectDesignation = StringVar()
        self.estimatedStudents = StringVar()
        self.majorRequirement = StringVar()
        self.yearRequirement = StringVar()
        self.deptRequirement = StringVar()
        self.AddCategory = StringVar()

        # Populate Scroll Down Menu
        self.cursor.execute("SELECT * FROM CATEGORY")
        category = self.cursor.fetchall()
        categoryList = []
        for (cat,) in category:
            categoryList.append(cat)

        self.cursor.execute("SELECT * FROM DESIGNATION")
        designation = self.cursor.fetchall()
        designationList = []
        for (dsg,) in designation:
            designationList.append(dsg)

        self.cursor.execute("SELECT Name FROM MAJOR")
        major = self.cursor.fetchall()
        self.cursor.execute("SELECT Name FROM DEPARTMENT;")
        department = self.cursor.fetchall()
        majorList = []
        deptList = []
        for (mj,) in major:
            majorList.append("Only %s students" % mj)
        for (dept,) in department:
            deptList.append("Only %s students" % dept)

        yearList = ['Only Freshman students', 'Only Sophomore students', 'Only Junior students', 'Only Senior students']

        Entry(frame2, width=30, textvariable=self.newProject).grid(row=0, column=3, sticky=W, padx=15)
        Entry(frame2, width=30, textvariable=self.advisorName).grid(row=1, column=3, sticky=W, padx=15)
        Entry(frame2, width=30, textvariable=self.advisorEmail).grid(row=2, column=3, sticky=W, padx=15, pady=0)
        Entry(frame2, width=50, textvariable=self.description).grid(row=3, column=3, sticky=W, padx=15, pady=0)

        self.projectCatFilter_count = 1
        cur_idx = self.projectCatFilter_count - 1
        categoryOM = apply(OptionMenu, (frame3, self.projectCategoryList[cur_idx]) + tuple(categoryList))
        categoryOM.grid(row=cur_idx, column=3, sticky=W)
        categoryOM.config(width=20)
        # Add a category
        addCate = Button(frame3, text="Add a Category", command=lambda: self.addProjectCat(categoryList, frame3)).grid(
            row=0, column=4, sticky=W, pady=5)

        designationOM = apply(OptionMenu, (frame4, self.projectDesignation) + tuple(designationList))
        designationOM.grid(row=0, column=3, sticky=W)
        designationOM.config(width=20)

        Entry(frame4, width=10, textvariable=self.estimatedStudents).grid(row=1, column=3, sticky=W, padx=15)
        MajorRequirementOM = apply(OptionMenu, (frame4, self.majorRequirement) + tuple(majorList))
        MajorRequirementOM.grid(row=2, column=3, sticky=W)
        MajorRequirementOM.config(width=25)
        YearRequirementOM = apply(OptionMenu, (frame4, self.yearRequirement) + tuple(yearList))
        YearRequirementOM.grid(row=3, column=3, sticky=W)
        YearRequirementOM.config(width=25)
        DepartmentRequirementOM = apply(OptionMenu, (frame4, self.deptRequirement) + tuple(deptList))
        DepartmentRequirementOM.grid(row=4, column=3, sticky=W)
        DepartmentRequirementOM.config(width=25)

        Button(frame5, text='Back', width=10, command=self.backToAdminMainPage).grid(row=0, column=2, pady=25)
        Button(frame5, text='Submit', width=10, command=self.submitNewProject).grid(row=0, column=4, padx=40, pady=25)

    def addProjectCat(self, optionList, filterFrame):
        if self.projectCatFilter_count < 4:
            self.projectCatFilter_count += 1
            cur_idx = self.projectCatFilter_count - 1

            Label(filterFrame, text='Category:').grid(row=cur_idx, column=2, sticky=W, padx=25, pady=5)
            categoryOM = apply(OptionMenu, (filterFrame, self.projectCategoryList[cur_idx]) + tuple(optionList))
            categoryOM.grid(row=cur_idx, column=3, sticky=W)
            categoryOM.config(width=20)

    def submitNewProject(self):
        # Preprocess of all selected categories
        cat_variable_list = []
        for s in self.projectCategoryList:
            cat_variable_list.append(s.get())
        cat_variable_list = filter(None, cat_variable_list)

        # Update PROJECT
        if self.newProject.get() == '':
            tkMessageBox.showwarning("Error", "Project name cannot be empty!")
            return None
        elif self.advisorName.get() == '':
            tkMessageBox.showwarning("Error", "Advisor name cannot be empty!")
            return None
        elif self.advisorEmail.get() == '':
            tkMessageBox.showwarning("Error", "Advisor email cannot be empty!")
            return None
        elif self.description.get() == '':
            tkMessageBox.showwarning("Error", "Description cannot be empty!")
            return None
        elif len(cat_variable_list) == 0:
            tkMessageBox.showwarning("Error", "Category cannot be empty!")
            return None
        elif self.projectDesignation.get() == '':
            tkMessageBox.showwarning("Error", "Project designation cannot be empty!")
            return None
        else:
            # Check if already exists
            self.cursor.execute("SELECT COUNT(*) FROM PROJECT WHERE Name=%s", self.newProject.get())
            (Exist,) = self.cursor.fetchone()
            if Exist != 0:
                tkMessageBox.showwarning("Error", "This project name already exists!")
                return None

            if self.estimatedStudents.get() == '':
                self.cursor.execute("INSERT INTO PROJECT VALUES (%s,%s,%s,%s,NULL,%s)", (
                self.newProject.get(), self.description.get(), self.advisorEmail.get(), self.advisorName.get(),
                self.projectDesignation.get()))
            else:
                self.cursor.execute("INSERT INTO PROJECT VALUES (%s,%s,%s,%s,%s,%s)", (
                self.newProject.get(), self.description.get(), self.advisorEmail.get(), self.advisorName.get(),
                self.estimatedStudents.get(), self.projectDesignation.get()))

            self.db.commit()

        # Update PROJECT_REQUIREMENT
        if self.yearRequirement.get() != '':
            self.cursor.execute("INSERT INTO PROJECT_REQUIREMENT VALUES (%s,%s)",
                                (self.newProject.get(), self.yearRequirement.get()))
            self.db.commit()

        if self.majorRequirement.get() != '':
            self.cursor.execute("INSERT INTO PROJECT_REQUIREMENT VALUES (%s,%s)",
                                (self.newProject.get(), self.majorRequirement.get()))
            self.db.commit()

        if self.deptRequirement.get() != '':
            self.cursor.execute("INSERT INTO PROJECT_REQUIREMENT VALUES (%s,%s)",
                                (self.newProject.get(), self.deptRequirement.get()))
            self.db.commit()

        if self.yearRequirement.get() == '' and self.majorRequirement.get() == '' and self.deptRequirement.get() == '':
            self.cursor.execute("INSERT INTO PROJECT_REQUIREMENT VALUES (%s,%s)", (self.newProject.get(), 'None'))
            self.db.commit()

        # Update PROJECT_IS_CATEGORY
        for cat in cat_variable_list:
            self.cursor.execute("INSERT INTO PROJECT_IS_CATEGORY VALUES(%s,%s)", (self.newProject.get(), cat))
            self.db.commit()

        tkMessageBox.showinfo("Success", "New project is added!")

    def addCourse(self):
        # Add course page
        self.current_page.withdraw()
        add_course_page = Toplevel()
        add_course_page.title('Add a Course')
        add_course_page.geometry("%dx%d+%d+%d" % (650, 350, 0, 0))
        self.add_course_page = add_course_page
        self.current_page = self.add_course_page

        frame1 = Frame(add_course_page)
        frame1.pack()
        frame2 = Frame(add_course_page)
        frame2.pack()
        frame3 = Frame(add_course_page)
        frame3.pack()
        frame4 = Frame(add_course_page)
        frame4.pack()
        frame5 = Frame(add_course_page)
        frame5.pack()

        Label(frame2, text="Course Number:").grid(row=0, column=2, sticky=W, padx=25, pady=5)
        Label(frame2, text="Course Name:").grid(row=1, column=2, sticky=W, padx=25, pady=5)
        Label(frame2, text="Instructor:").grid(row=2, column=2, sticky=W, padx=25, pady=5)
        Label(frame2, text="Designation:").grid(row=3, column=2, sticky=W, padx=25, pady=5)
        Label(frame3, text="Category:").grid(row=0, column=2, sticky=W, padx=25, pady=5)
        Label(frame4, text="Estimated # of students:").grid(row=0, column=2, sticky=W, padx=25, pady=5)

        # User inputs
        cat1 = StringVar()
        cat2 = StringVar()
        cat3 = StringVar()
        cat4 = StringVar()
        self.courseNum = StringVar()
        self.courseName = StringVar()
        self.instructor = StringVar()
        self.courseDesignation = StringVar()
        self.courseCategoryList = [cat1, cat2, cat3, cat4]
        self.courseStudentNum = StringVar()

        self.cursor.execute("SELECT * FROM CATEGORY")
        category = self.cursor.fetchall()
        categoryList = []
        for (cat,) in category:
            categoryList.append(cat)

        self.cursor.execute("SELECT * FROM DESIGNATION")
        designation = self.cursor.fetchall()
        designationList = []
        for (dsg,) in designation:
            designationList.append(dsg)

        Entry(frame2, width=20, textvariable=self.courseNum).grid(row=0, column=3, sticky=W, padx=15)
        Entry(frame2, width=20, textvariable=self.courseName).grid(row=1, column=3, sticky=W, padx=15)
        Entry(frame2, width=20, textvariable=self.instructor).grid(row=2, column=3, sticky=W, padx=15)

        designationOM = apply(OptionMenu, (frame2, self.courseDesignation) + tuple(designationList))
        designationOM.grid(row=3, column=3, sticky=W)
        designationOM.config(width=20)

        self.courseCatFilter_count = 1
        cur_idx = self.courseCatFilter_count - 1
        categoryOM = apply(OptionMenu, (frame3, self.courseCategoryList[cur_idx]) + tuple(categoryList))
        categoryOM.grid(row=cur_idx, column=3, sticky=W)
        categoryOM.config(width=20)

        # Add a category
        addCate = Button(frame3, text="Add a Category", command=lambda: self.addCourseCat(categoryList, frame3)).grid(
            row=0, column=4, sticky=W, pady=5)

        Entry(frame4, width=10, textvariable=self.courseStudentNum).grid(row=0, column=3, sticky=W, padx=15)

        # Add 'Back' & 'Submit' Button
        Button(frame5, text='Back', width=10, command=self.backToAdminMainPage).grid(row=0, column=0, sticky=W)
        Button(frame5, text='Submit', width=10, command=self.submitNewCourse).grid(row=0, column=2, padx=40, pady=25)

    def addCourseCat(self, optionList, filterFrame):
        if self.courseCatFilter_count < 4:
            self.courseCatFilter_count += 1
            cur_idx = self.courseCatFilter_count - 1

            Label(filterFrame, text='Category:').grid(row=cur_idx, column=2, sticky=W, padx=25, pady=5)
            categoryOM = apply(OptionMenu, (filterFrame, self.courseCategoryList[cur_idx]) + tuple(optionList))
            categoryOM.grid(row=cur_idx, column=3, sticky=W)
            categoryOM.config(width=20)

    def submitNewCourse(self):
        if self.courseNum.get() == '':
            tkMessageBox.showwarning("Error", "Course number cannot be empty!")
            return None
        elif self.courseName.get() == '':
            tkMessageBox.showwarning("Error", "Course name cannot be empty!")
            return None
        elif self.instructor.get() == '':
            tkMessageBox.showwarning("Error", "instructor cannot be empty!")
            return None
        elif self.courseDesignation.get() == '':
            tkMessageBox.showwarning("Error", "Designation cannot be empty!")
            return None
        elif self.courseCategoryList[0].get() == '' and self.courseCategoryList[1].get() == '' and \
                        self.courseCategoryList[2].get() == '' and self.courseCategoryList[3].get() == '':
            tkMessageBox.showwarning("Error", "Please choose a category!")
            return None
        else:
            # Check if course already exists
            self.cursor.execute("SELECT COUNT(*) FROM COURSE WHERE Name=%s", self.courseName.get())
            (Exist,) = self.cursor.fetchone()
            if Exist != 0:
                tkMessageBox.showwarning("Error", "This Course Name already exists!")
                return None

            # Update COURSE
            if self.courseStudentNum.get() == '':
                self.cursor.execute("INSERT INTO COURSE VALUES (%s,%s,%s,NULL,%s)", (
                self.courseName.get(), self.courseNum.get(), self.instructor.get(), self.courseDesignation.get()))
            else:
                self.cursor.execute("INSERT INTO COURSE VALUES (%s,%s,%s,%s,%s)", (
                self.courseName.get(), self.courseNum.get(), self.instructor.get(), self.courseStudentNum.get(),
                self.courseDesignation.get()))

            self.db.commit()

            # Preprocess of all selected categories
            cat_variable_list = []
            for s in self.courseCategoryList:
                cat_variable_list.append(s.get())
            cat_variable_list = filter(None, cat_variable_list)

            # Update COURES_IS_CATEGORY
            for cat in cat_variable_list:
                self.cursor.execute("INSERT INTO COURSE_IS_CATEGORY VALUES (%s,%s)",
                                    (self.courseName.get(), cat))
                self.db.commit()

            tkMessageBox.showinfo("Success", "New course is added!")

    def Logout(self):
        tkMessageBox.showinfo("Success", "You successfully logout the system!")
        self.login_page.destroy()


## Create the GUI object
GUI = sysDB()
mainloop()
