from flask import Flask, render_template, make_response, request, session, redirect, url_for
import pymysql
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user
import datetime
import string
import time
import xlrd
import xlwt
import sys
import os
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user

from wtforms import Form, StringField, PasswordField, DateField, validators

app = Flask(__name__)

db = pymysql.connect("127.0.0.1", "root", "", "project fruit")
cursor = db.cursor()

################################################################################################################################## 来自黎略呈的部分：

@app.route('/')
def index():
	return render_template('Login/Login.html')

@app.route('/logout')
def logout():
	return render_template('Login/Login.html')	
					
@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		identity = request.form['identity']		
		db = pymysql.connect("127.0.0.1", "root", "", "project fruit")
		with db.cursor() as cursor:

			if len(username.strip()) == 0 or len(password.strip()) == 0:
				message = "Information is not completed"
				return render_template('Login/Login.html',message=message)

			if identity == "teacher":
				account_password = int(password)
				sql="select Teacher_Name from teacher where Teacher_Name = '%s'" % username
				cursor.execute(sql)
				row = cursor.rowcount
				if row == 1:

					sql="select Password from teacher where Teacher_Name = '%s'" % username
					cursor.execute(sql)
					result = cursor.fetchone()	
					password_result = int(result[0])
					sql2="select Teacher_Name from teacher where Teacher_Name = '%s'" % username
					cursor.execute(sql2)
					teacherName = cursor.fetchall()

					sql = "SELECT CourseID,Course_Title from course WHERE Teacher_Name = '%s' " %username
					cursor.execute(sql)
					results = cursor.fetchone()
					CourseID = int(results[0])
					CourseName = str(results[1])

					if password_result==account_password:						
						return render_template('Teacher/Teacher.html',teacherName=str(teacherName[0][0]),CourseID=CourseID,CourseName=CourseName)
					else:
						message = "Your password is Wrong! Please try again."
						return render_template('Login/Login.html',message=message)
				else:
					message = "Your ID is not exist or choose the wrong identity!"
					return render_template('Login/Login.html',message=message)
			
			elif identity == "student":
				account_password = int(password)
				sql="select email from student where email = '%s'" % username
				cursor.execute(sql)
				row = cursor.rowcount
				pwd = cursor.fetchone()
				if row == 1:
					sql="select Password from student where email = '%s'" % username
					cursor.execute(sql)
					result = cursor.fetchone()	
					password_result = int(result[0])
					sql2="select Stu_Name from student where email = '%s'" % username
					cursor.execute(sql2)
					studentName = cursor.fetchone()
					

					sql = "SELECT Stu_ID,CourseID from student WHERE email = '%s' " %username
					cursor.execute(sql)
					results = cursor.fetchone()
					CourseID = int(results[1])
					Stu_ID = int(results[0])

					if password_result==account_password:						
						return render_template('Student/Student.html',StudentName=str(studentName[0]),CourseID=CourseID,Stu_ID=Stu_ID)
					else:
						message = "Your password is Wrong! Please try again."
						return render_template('Login/Login.html',message=message)
				else:
					message = "Your ID is not exist or choose the wrong identity!"
					return render_template('Login/Login.html',message=message)
			
@app.route('/upload')
def upload():
	return render_template('Import/Upload file.html')

@app.route('/editOneItem1',methods=['GET', 'POST'])
def editOneItem1():
	######################通用三项数据
	teacherName = request.form["teacherName"]
	CourseID = request.form["CourseID"]
	CourseID = int(CourseID)
	CourseName = request.form["CourseName"]
	##############################  ,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName

	db_op = DatabaseOperations()
	result = db_op.submission_order(CourseID)
	return render_template('Edit/Edit submission.html',events=result,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)

@app.route('/edit',methods=['GET', 'POST'])
def editSubmission():

	######################通用三项数据
	teacherName = request.form["teacherName"]
	CourseID = request.form["CourseID"]
	CourseID = int(CourseID)
	CourseName = request.form["CourseName"]
	##############################  ,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName

	db_op = DatabaseOperations()  ##fanhui edit zhuye
	result = db_op.submission_order(CourseID)
	return render_template('Edit/Edit submission.html',events=result,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)
	
@app.route('/editOneItem', methods=['GET', 'POST'])
def editOneItem():
	if request.method == 'POST':
		
		######################通用三项数据
		teacherName = request.form["teacherName"]
		CourseID = request.form["CourseID"]
		CourseID = int(CourseID)
		CourseName = request.form["CourseName"]
		##############################  ,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName

		itemTitle = request.form["editOneItem"]	

		return render_template('Edit/Edit one item.html', itemTitle=itemTitle,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)


@app.route('/editOneItemPage', methods=['GET', 'POST'])  
def editOneItemPage():
	if request.method == 'POST':

		######################通用三项数据
		teacherName = request.form["teacherName"]
		CourseID = request.form["CourseID"]
		CourseID = int(CourseID)
		CourseName = request.form["CourseName"]
		##############################  ,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName

		db = pymysql.connect("127.0.0.1", "root", "", "project fruit")
		itemTitle = request.form["editOneItem"]
		newTitle = request.form["newTitle"]
		newPercentage = request.form["newPercentage"]
		

		with db.cursor() as cursor:

			if len(newTitle.strip()) == 0 or len(newPercentage.strip()) == 0:
				Message = "Please complete your information ! "
				return render_template('Edit/Edit one item.html',itemTitle=itemTitle,message=Message,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)

			newPercentage_result = float(newPercentage)
			sql_temp = "select Percentage from submission_item where Title = '%s'" % itemTitle #获取当前title的percentage
			cursor.execute(sql_temp)
			temp_percentage = cursor.fetchone()
			temp = float(temp_percentage[0])
			
			sql_total = "select sum(Percentage) from submission_item WHERE CourseID = '%d' " %CourseID #获取数据库中percentage的总和
			cursor.execute(sql_total)
			total_percentage = cursor.fetchone()
			total = float(total_percentage[0])
			
			new_percentage = total - temp + newPercentage_result
			if new_percentage<=1.0001:
				sql2 = "UPDATE submission_item SET Percentage = '%f' WHERE Title = '%s' AND CourseID = '%d'" % (newPercentage_result, itemTitle,CourseID)
				sql = "UPDATE submission_item SET Title = '%s' WHERE Title = '%s' AND CourseID = '%d' " % (newTitle, itemTitle,CourseID)
				cursor.execute(sql2)
				db.commit()
				cursor.execute(sql)
				db.commit()			
				db_op = DatabaseOperations()  ##fanhui edit zhuye
				result = db_op.submission_order(CourseID)
				return render_template('Edit/Edit submission.html', events=result,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)
			else:
				message = "Error: The total percentage must be smaller than 1"
				return render_template('Edit/Edit one item.html',itemTitle=itemTitle,message=message,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)

@app.route('/deleteItem', methods=['GET', 'POST'])   
def deleteItem():
	if request.method == 'POST':

		######################通用三项数据
		teacherName = request.form["teacherName"]
		CourseID = request.form["CourseID"]
		CourseID = int(CourseID)
		CourseName = request.form["CourseName"]
		##############################  ,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName

		db = pymysql.connect("127.0.0.1", "root", "", "project fruit")
		itemTitle = request.form["editOneItem"]
		with db.cursor() as cursor:
			sql = "delete from submission_item where Title = '%s' AND CourseID = '%d' " %(itemTitle,CourseID)
			cursor.execute(sql)
			db.commit()

			db_op = DatabaseOperations()  ##fanhui edit zhuye
			result = db_op.submission_order(CourseID)
			return render_template('Edit/Edit submission.html', events=result,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)

@app.route('/add', methods=['GET', 'POST'])  
def add():
	######################通用三项数据
	teacherName = request.form["teacherName"]
	CourseID = request.form["CourseID"]
	CourseID = int(CourseID)
	CourseName = request.form["CourseName"]
	##############################  ,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName

	return render_template('Edit/Add new item.html',teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)

@app.route('/addNewItem', methods=['GET', 'POST'])  
def addNewItem():
	if request.method == 'POST':

		######################通用三项数据
		teacherName = request.form["teacherName"]
		CourseID = request.form["CourseID"]
		CourseID = int(CourseID)
		CourseName = request.form["CourseName"]
		##############################  ,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName

		db = pymysql.connect("127.0.0.1", "root", "", "project fruit")
		title = request.form['title']

		percentage_result = request.form['percentage']
		

		if len(title.strip()) == 0 or len(percentage_result.strip()) == 0:
			Message = "Please complete your information ! "
			return render_template('Edit/Add new item.html',message=Message,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)

		percentage = float(percentage_result)

		with db.cursor() as cursor:

			sql = "SELECT * FROM submission_item WHERE '%d' " %CourseID
			cursor.execute(sql)
			row = cursor.rowcount
			if row==0:
				total = 0
			else: 
				sql_total = "select sum(Percentage) from submission_item WHERE CourseID = '%d' " %CourseID #获取数据库中percentage的总和
				cursor.execute(sql_total)
				total_percentage = cursor.fetchone()

				sql = "select * from submission_item WHERE CourseID = '%d' " %CourseID 
				cursor.execute(sql)
				exist = cursor.rowcount

				if exist == 0:
					total = 0.00
				else:
					total = float(total_percentage[0])
				
			new_percentage = total + percentage
			if new_percentage<=1.00001:
				sql_insert="""insert into submission_item(Title, Percentage,CourseID) values('%s','%f','%d')"""
				cursor.execute(sql_insert % (title ,percentage,CourseID))
				db.commit()
				db_op = DatabaseOperations()
				result = db_op.submission_order(CourseID)
				return render_template('Edit/Edit submission.html',events=result,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)
			else:
				message = "The total percentage must be smaller than 1"
				return render_template('Edit/Add new item.html',message=message,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)

@app.route('/ImportFile', methods = ['GET', 'POST'])  
def import_file():
	if request.method == 'POST':

		######################通用三项数据
		teacherName = request.form["teacherName"]
		CourseID = request.form["CourseID"]
		CourseID = int(CourseID)
		CourseName = request.form["CourseName"]
		##############################  ,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName
		
		db = pymysql.connect("127.0.0.1", "root", "", "project fruit")
		cursor = db.cursor(pymysql.cursors.DictCursor)
		cursor2 = db.cursor()
		book = xlrd.open_workbook("C:/Users/92356/Desktop/workshop/project 2020/templates/Import/Import Student Information.xlsx")

		initialPassword = request.form["password"]
		intinitialPassword = int(initialPassword)

		sheet = book.sheet_by_name("sheet1")
		for i in range(1, sheet.nrows):
			Stu_Name = sheet.cell(i, 0).value
			Stu_ID = sheet.cell(i, 1).value
			email = sheet.cell(i, 2).value
			GPA = sheet.cell(i, 3).value

			#check student ID
			checkID = "SELECT * from student where Stu_ID = '%d' AND CourseID = '%d'" %(Stu_ID,CourseID)
			if cursor2.execute(checkID):
				message = "Student ID " + str(int(Stu_ID)) +  " has already got an account. Please check the Excel file."
				return render_template('Import/Upload file.html', message = message)

			else:
				sql = "insert into student(Stu_Name, Stu_ID, email, GPA, Password, courseID) values('%s', %d, '%s', '%f', '%d', '%d')"
				cursor.execute(sql % (Stu_Name, Stu_ID, email, GPA, intinitialPassword, CourseID))
				db.commit()

		db = pymysql.connect("127.0.0.1", "root", "", "project fruit")
		with db.cursor() as cursor:
			sql = "SELECT * FROM student WHERE CourseID = '%d' AND Password = '%d'" %(CourseID,intinitialPassword)
			cursor.execute(sql)
			List = cursor.fetchall()
			return render_template('Import/DisplayImport.html',List=List,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)


@app.route('/Export', methods = ['GET', 'POST'])
def Export_file():
	if request.method == 'POST':
		######################通用三项数据
		teacherName = request.form["teacherName"]
		CourseID = request.form["CourseID"]
		CourseID = int(CourseID)
		CourseName = request.form["CourseName"]
		##############################  ,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName
		

		db = pymysql.connect("127.0.0.1", "root", "", "project fruit")
		with db.cursor() as cursor:

			sql = "select * from team where CourseID = %d " %CourseID
			cursor = db.cursor()
			cursor.execute(sql)
			exist = cursor.rowcount
			result = cursor.fetchall()

			if exist == 0:
				Message = "ERROR:There is no Team in this course yet!"
				return render_template('Export/Export contribution file.html',Message=Message,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)

			book = xlwt.Workbook(encoding='utf-8')
			ws = book.add_sheet(str(CourseID), cell_overwrite_ok = True)
			row = ['Student Name', 'Contribution', 'Bonus', 'Identify', 'CourseID', 'TeamNO']
			for i in range(0, len(row)):
				ws.write(0, i, row[i])
			k = 1
			for i in result:
				for j in range (6):
					if i[3] == "M" and j == 2:
						ws.write(k, j, 0)
					else:
						ws.write(k, j, i[j])
				k += 1
			book.save('C:/Users/92356/Desktop/workshop/project 2020/templates/Export/Contribution.xls')

			Message = "Download successcully. Please check the excel file in: C:/Users/92356/Desktop/workshop/project 2020/templates/Export"

			return render_template('Export/Export contribution file.html',Message=Message,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)

		
@app.route('/Import page',methods = ['GET', 'POST'])
def ImportPage():

	######################通用三项数据
	teacherName = request.form["teacherName"]
	CourseID = request.form["CourseID"]
	CourseID = int(CourseID)
	CourseName = request.form["CourseName"]
	##############################  ,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName

	return render_template('Import/Upload file.html',teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)

	
@app.route('/Export contribution file',methods = ['GET', 'POST'])
def ExportPage():
	######################通用三项数据
	teacherName = request.form["teacherName"]
	CourseID = request.form["CourseID"]
	CourseID = int(CourseID)
	CourseName = request.form["CourseName"]
	##############################  ,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName
	db = pymysql.connect("127.0.0.1", "root", "", "project fruit")
	with db.cursor() as cursor:

		sql = "select * from team where CourseID = %d " %CourseID
		cursor.execute(sql)
		exist = cursor.rowcount
		results = cursor.fetchall()
		if exist == 0:
				Message = "ERROR:There is no Team in this course yet!"
				return render_template('Export/Export contribution file.html',Message=Message,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)

		for i in range (0,exist):
			if str(results[i][3]) == "M":
				sql = "INSERT INTO export_file VALUES('%s','%f','%f','%s','%d','%d')" %(str(results[i][0]),float(results[i][1]),0.00,str(results[i][3]),int(results[i][4]),int(results[i][5]))
			else:
				sql = "INSERT INTO export_file VALUES('%s','%f','%f','%s','%d','%d')" %(str(results[i][0]),float(results[i][1]),float(results[i][2]),str(results[i][3]),int(results[i][4]),int(results[i][5]))
			cursor.execute(sql)
			db.commit()

		sql = "SELECT * from export_file WHERE CourseID = '%d' " %CourseID	
		cursor.execute(sql)
		results = cursor.fetchall()

		sql = "DELETE from export_file"
		cursor.execute(sql)
		db.commit()

		return render_template('Export/Export contribution file.html',results=results,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)


@app.route('/Generate',methods=['GET', 'POST'])  #000000000000000000000000000000000000000000000000000000000
def Generate():
	######################通用三项数据
	teacherName = request.form["teacherName"]
	CourseID = request.form["CourseID"]
	CourseID = int(CourseID)
	CourseName = request.form["CourseName"]
	##############################  ,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName

	return render_template('Generate/Generate account.html',teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)

@app.route('/GAccount',methods=['GET', 'POST'])
def GAccount():

	######################通用三项数据
	teacherName = request.form["teacherName"]
	CourseID = request.form["CourseID"]
	CourseID = int(CourseID)
	CourseName = request.form["CourseName"]
	##############################  ,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName

	if request.method == 'POST':
		name = request.form["Name"]
		id = request.form["ID"]
		email = request.form["Email"]
		inipassword = request.form["Initial password"]
		gpa = request.form["GPA"]

		if len(name.strip()) == 0 or len(id.strip()) == 0 or len(email.strip()) == 0 or len(inipassword.strip()) == 0 or len(gpa.strip()) == 0:
			message = "Information is not completed"
			return render_template('Generate/Generate account.html',message=message,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)
		else:
			Name = str(name)
			ID = int(id)
			Email = str(email)
			Inipassword = int(inipassword)
			if type(float(gpa)) != type(3.00):
				message = "Error: Please check your GPA input form again, it needs to be float."
				return render_template('Generate/Generate account.html',message=message,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)
			GPA = float(gpa)

			db = pymysql.connect("localhost", "root", "", "project fruit")
			with db.cursor() as cursor:
				sql = "SELECT Stu_ID from student WHERE Stu_ID = '%d' AND CourseID = '%d' " %(ID,CourseID)
				if cursor.execute(sql):
					message = "No account needs to be generated for this student ID again"
					return render_template('Generate/Generate account.html',message=message,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)
				else:
					sql = "INSERT INTO student VALUE ('%s','%d','%s', '%f','%d', null, '%d');" %(Name, ID, Email, GPA, Inipassword, CourseID)
					cursor.execute(sql)
					db.commit()
					sql = "SELECT Stu_Name, Stu_ID, Email, GPA, Password from student WHERE Stu_ID = '%d'" %(ID)
					cursor.execute(sql)
					ret1 = cursor.fetchone()
					Name = str(ret1[0])
					ID = str(ret1[1])
					Email = str(ret1[2])
					GPA = str(ret1[3])
					password = str(ret1[4])
					return render_template('Generate/Display account.html',Name=Name,ID=ID,Email=Email,GPA=GPA,password=password,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)

@app.route('/DAccount',methods=['GET', 'POST'])
def DAccount():

	######################通用三项数据
	teacherName = request.form["teacherName"]
	CourseID = request.form["CourseID"]
	CourseID = int(CourseID)
	CourseName = request.form["CourseName"]
	##############################  ,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName

	if request.method == 'POST':
		message = "Generate account successful!"
		return render_template('Generate/Generate account.html',message=message,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)

@app.route('/ChangePassword', methods=['GET', 'POST']) 
def ChangePassword():
	if request.method == 'POST':
		
		#####获取三项通用
		Stu_ID = request.form["Stu_ID"]
		Stu_ID = int(Stu_ID)
		StudentName = request.form["StudentName"]
		CourseID = request.form["CourseID"]
		CourseID = int(CourseID)
		#####以上 ,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID

		return render_template('Student/ChangePsw.html',StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)


@app.route('/Change',methods=['GET', 'POST'])
def Change():
	if request.method == 'POST':

		#####获取三项通用
		Stu_ID = request.form["Stu_ID"]
		Stu_ID = int(Stu_ID)
		StudentName = request.form["StudentName"]
		CourseID = request.form["CourseID"]
		CourseID = int(CourseID)
		#####以上 ,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID

		oldpassword = request.form["OldPassword"]
		newpassword = request.form["NewPasswordOne"]
		confirmPassword = request.form["NewPasswordTwo"]
		
		if len(oldpassword.strip()) == 0 or len(newpassword.strip()) == 0 or len(confirmPassword.strip()) == 0:
			message = "Error: Full input is required !"
			return render_template('Student/ChangePsw.html',message=message,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)
		else:
			Oldpassword = int(oldpassword)
			Newpassword = int(newpassword)
			ConfirmPassword = int(confirmPassword)
			db = pymysql.connect("localhost", "root", "", "project fruit")
			with db.cursor() as cursor:
				sql ="select Password from student where Stu_ID = '%d'" % Stu_ID
				cursor.execute(sql)
				result = cursor.fetchone()	
				password_result = int(result[0])
				if password_result==Oldpassword:
					Newpw = str(Newpassword)
					if(len(Newpw) < 0):
						message = "Error: The Password should not less than 0 characters"
						return render_template('Student/ChangePsw.html',message=message,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)
					else:
						if Newpassword==ConfirmPassword:
							sql = "UPDATE student SET Password = '%d' WHERE Stu_ID = '%d'" % (Newpassword, Stu_ID)
							cursor.execute(sql)
							db.commit()
							message = "Confirmed: Change password successfully!"
							return render_template('Student/ChangePsw.html', message=message,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)
						else:
							message = "Error: Two passwords are different! Please try again."
							return render_template('Student/ChangePsw.html', message=message,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)
				else:
					message = "Error: Old password is incorrect! Please try again."
					return render_template('Student/ChangePsw.html', message=message,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)

############################################################################################################################################

@app.route('/teacher',methods=['GET', 'POST'])
def teacher():

	######################通用三项数据
	teacherName = request.form["teacherName"]
	CourseID = request.form["CourseID"]
	CourseID = int(CourseID)
	CourseName = request.form["CourseName"]
	##############################  ,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName

	return render_template('Teacher/Teacher.html',teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)

@app.route('/Form team',methods=['GET', 'POST'])
def form():

	######################通用三项数据
	teacherName = request.form["teacherName"]
	CourseID = request.form["CourseID"]
	CourseID = int(CourseID)
	CourseName = request.form["CourseName"]
	##############################  ,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName

	return render_template('Form/Form team.html',teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)

@app.route('/MoreMember',methods=['GET', 'POST'])
def MoreMember():
	if request.method == 'POST':

		######################通用三项数据
		teacherName = request.form["teacherName"]
		CourseID = request.form["CourseID"]
		CourseID = int(CourseID)
		CourseName = request.form["CourseName"]
		##############################  ,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName

		consider = request.form["consider"]

		db = pymysql.connect("127.0.0.1", "root", "", "project fruit")
		with db.cursor() as cursor:

			sql = "SELECT"
			#################################################### 123 随机分 人多
			sql = "select random,Total_Amount,Member_Num from team_method where CourseID = '%d' order by rand() " %CourseID
			cursor.execute(sql)
			result = cursor.fetchone()

			sql = "UPDATE team_method SET Multiple = 'M' WHERE CourseID = '%d' " %CourseID
			cursor.execute(sql)
			db.commit()

			if result[0] == 1:
				sql = "select * from student where CourseID = '%d' order by rand() " %CourseID
				cursor.execute(sql)
				NameList = cursor.fetchall()
				i = 0
				for teamAmount in range(1,int(result[1]/result[2])+1):
					for a in range(1,int(result[2])+1):

						sql = "INSERT INTO team_all VALUES('%d','%s','%d',null)" %(CourseID,NameList[i][0],teamAmount)
						cursor.execute(sql)
						db.commit()

						sql = "INSERT INTO team VALUES('%s',1.0,0,'M','%d','%d')" %(NameList[i][0],CourseID,teamAmount)
						cursor.execute(sql)
						db.commit()
						i = i + 1

				for extraMember in range(1,int(result[1])-i+1):

					sql = "INSERT INTO team_all VALUES('%d','%s','%d',null)" %(CourseID,NameList[i][0],int(result[1]/result[2]))
					cursor.execute(sql)
					db.commit()

					sql = "INSERT INTO team VALUES('%s',1.0,0,'M','%d','%d')" %(NameList[i][0],CourseID,int(result[1]/result[2]))
					cursor.execute(sql)
					db.commit()
					i = i + 1

				db_op = DatabaseOperations()
				result = db_op.display(CourseID)

				if consider == "GPA":
					TotalGPA = 0.00
					sql = "select * from student where CourseID = '%d' order by rand() " %CourseID
					cursor.execute(sql)
					result = cursor.fetchall()
					row = cursor.rowcount

					for i in range(0,row):
							TotalGPA = TotalGPA + result[i][3]
					
					return render_template('Form/GPA.html',AverageGPA=float(TotalGPA/row),courseID=str(CourseID),teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)

				return render_template('Form/Display.html',display=result,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)
			#################################################### 123 随机分

			else:

				if consider == "GPA":
					TotalGPA = 0.00
					sql = "select * from student where CourseID = '%d' order by rand() " %CourseID
					cursor.execute(sql)
					result = cursor.fetchall()
					row = cursor.rowcount

					for i in range(0,row):
							TotalGPA = TotalGPA + result[i][3]
					
					return render_template('Form/GPA.html',AverageGPA=float(TotalGPA/row),courseID=str(CourseID),teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)
				
				return render_template('Teacher/Teacher.html',teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)


@app.route('/LessMember',methods=['GET', 'POST'])
def LessMember():
	if request.method == 'POST':

		######################通用三项数据
		teacherName = request.form["teacherName"]
		CourseID = request.form["CourseID"]
		CourseID = int(CourseID)
		CourseName = request.form["CourseName"]
		##############################  ,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName
		
		consider = request.form["consider"]

		db = pymysql.connect("127.0.0.1", "root", "", "project fruit")
		with db.cursor() as cursor:

			#################################################### 123 随机分 人少
			sql = "select random,Total_Amount,Member_Num from team_method where CourseID = '%d' order by rand() " %CourseID
			cursor.execute(sql)
			result = cursor.fetchone()

			sql = "UPDATE team_method set Multiple = 'L' where CourseID = '%d' " %CourseID
			cursor.execute(sql)
			db.commit()

			if result[0] == 1:
				sql = "select * from student where CourseID = '%d' order by rand() " %CourseID
				cursor.execute(sql)
				NameList = cursor.fetchall()
				i = 0
				for teamAmount in range(1,int(result[1]/result[2])+1):

					for a in range(1,int(result[2])+1):
						sql = "INSERT INTO team_all VALUES('%d','%s','%d',null)" %(CourseID,NameList[i][0],teamAmount)
						cursor.execute(sql)
						db.commit()

						sql = "INSERT INTO team VALUES('%s',1.0,0,'M','%d','%d')" %(NameList[i][0],CourseID,teamAmount)
						cursor.execute(sql)
						db.commit()

						sql = "UPDATE student SET TeamNO = '%d' WHERE Stu_Name = '%s' " %(teamAmount,NameList[i][0])
						cursor.execute(sql)
						db.commit()

						i = i + 1

				for extraMember in range(1,int(result[1])-i+1):

					sql = "INSERT INTO team_all VALUES('%d','%s','%d',null)" %(CourseID,NameList[i][0],int(result[1]/result[2])+1)
					cursor.execute(sql)
					db.commit()

					sql = "INSERT INTO team VALUES('%s',1.0,0,'M','%d','%d')" %(NameList[i][0],CourseID,int(result[1]/result[2])+1)
					cursor.execute(sql)
					db.commit()

					sql = "UPDATE student SET TeamNO = '%d' WHERE Stu_Name = '%s' " %(int(result[1]/result[2])+1,NameList[i][0])
					cursor.execute(sql)
					db.commit()

					i = i + 1

				db_op = DatabaseOperations()
				result = db_op.display(CourseID)

				if consider == "GPA":

					sql = "select * from student where CourseID = '%d' order by rand() " %CourseID
					cursor.execute(sql)
					result = cursor.fetchall()
					row = cursor.rowcount
					TotalGPA = 0
					for i in range(0,row):
							TotalGPA = TotalGPA + result[i][3]
					
					return render_template('Form/GPA.html',AverageGPA=float(TotalGPA/row),courseID=str(CourseID),teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)

				return render_template('Form/Display.html',display=result,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)
			#################################################### 123 随机分 人少

			else:

				if consider == "GPA":

					sql = "select * from student where CourseID = '%d' order by rand() " %CourseID
					cursor.execute(sql)
					result = cursor.fetchall()
					row = cursor.rowcount

					for i in range(0,row):
							TotalGPA = TotalGPA + result[i][3]
					
					return render_template('Form/GPA.html',AverageGPA=float(TotalGPA/row),courseID=str(CourseID),teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)
				
				return render_template('Teacher/Teacher.html',teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)


@app.route('/ConfirmDisplay',methods=['GET', 'POST'])
def ConfirmDisplay():
	if request.method == 'POST':

		######################通用三项数据
		teacherName = request.form["teacherName"]
		CourseID = request.form["CourseID"]
		CourseID = int(CourseID)
		CourseName = request.form["CourseName"]
		##############################  ,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName

		return render_template('Teacher/Teacher.html',teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)

@app.route('/CancelDisplay',methods=['GET', 'POST'])
def CancelDisplay():
	if request.method == 'POST':

		######################通用三项数据
		teacherName = request.form["teacherName"]
		CourseID = request.form["CourseID"]
		CourseID = int(CourseID)
		CourseName = request.form["CourseName"]
		##############################  ,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName

		ID = int(request.form["cancel"])
		db = pymysql.connect("127.0.0.1", "root", "", "project fruit")
		with db.cursor() as cursor:
			sql = "DELETE from team_all WHERE CourseID = '%d'" %ID
			cursor.execute(sql)
			db.commit()

			sql = "DELETE from team WHERE CourseID = '%d'" %ID
			cursor.execute(sql)
			db.commit()

			sql = "DELETE from team_method WHERE CourseID = '%d'" %ID
			cursor.execute(sql)
			db.commit()

			return render_template('Teacher/Teacher.html',teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)


@app.route('/CancelGPA',methods=['GET', 'POST'])
def CancelGPA():
	if request.method == 'POST':

		######################通用三项数据
		teacherName = request.form["teacherName"]
		CourseID = request.form["CourseID"]
		CourseID = int(CourseID)
		CourseName = request.form["CourseName"]
		##############################  ,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName

		db = pymysql.connect("127.0.0.1", "root", "", "project fruit")
		with db.cursor() as cursor:
			sql = "SELECT random FROM team_method WHERE CourseID = '%d' " %CourseID
			cursor.execute(sql)
			M = cursor.fetchone()

			if int(M[0]) == 1:

				db_op = DatabaseOperations()
				result = db_op.display(CourseID)
				return render_template('Form/Display.html',display=result,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)

			return render_template('Teacher/Teacher.html',teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)


@app.route('/display',methods=['GET', 'POST'])
def display():
	if request.method == 'POST':

		######################通用三项数据
		teacherName = request.form["teacherName"]
		CourseID = request.form["CourseID"]
		CourseID = int(CourseID)
		CourseName = request.form["CourseName"]
		##############################  ,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName

		MemberAmount = request.form["MemberAmount"]
		formMethod = request.form["form-team-method"]
		


		consider = request.form["GPA"]
	
		if len(MemberAmount.strip()) == 0:
			message = "Error: You need to input an integer for team member amount !"
			return render_template('Form/Form team.html',message = message,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)

		MemberAmount = int(MemberAmount)

		db = pymysql.connect("127.0.0.1", "root", "", "project fruit")
		with db.cursor() as cursor:

			sql = "select * from student where CourseID = '%d' order by rand() " %CourseID
			cursor.execute(sql)
			result = cursor.fetchall()
			row = cursor.rowcount
			sql = "select * from team_method where CourseID = '%d' " %CourseID
			cursor.execute(sql)
			exist = cursor.rowcount
			existResult = cursor.fetchone()

			if row == 0:
				message = "Error: No student in your course yet, please check it again!"
				return render_template('Form/Form team.html',message = message,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)

			if row < MemberAmount:
				message = "Error: Member amount is over the total amount( "+ str(row) +" ) of students!" 
				return render_template('Form/Form team.html',message = message,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)

			if exist>0:

				if int(existResult[3]) == 1:
					message = "Notice: There is already a Free form method with " + str(existResult[2]) + " members each team for forming team of this course!"
				if int(existResult[4]) == 1:
					message = "Notice: There is already a Partner form method with " + str(existResult[2]) + " members each team for forming team of this course!"
				if int(existResult[5]) == 1:
					message = "Notice: There is already a random form method with " + str(existResult[2]) + " members each team for forming team of this course! Please check team display."

				return render_template('Form/Form team.html',message = message,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)

			if int(row % MemberAmount) != 0:  ######确认人数方法
				Message = ""
				if formMethod == "random":
					sql = "INSERT INTO team_method VALUES('%d','%d','%d',0,0,1,0,null)" %(CourseID,row,MemberAmount)
					cursor.execute(sql)
					db.commit()
				elif formMethod == "free":
					sql = "INSERT INTO team_method VALUES('%d','%d','%d',1,0,0,0,null)" %(CourseID,row,MemberAmount)
					cursor.execute(sql)
					db.commit()
				else:
					sql = "INSERT INTO team_method VALUES('%d','%d','%d',0,1,0,0,null)" %(CourseID,row,MemberAmount)
					cursor.execute(sql)
					db.commit()

				if consider == "GPA":
					sql = "UPDATE team_method SET GPA_Consider = 1 "
					cursor.execute(sql)
					db.commit()

				if int(row % MemberAmount) == 1:   ####只剩一个人
					Message = "Notice: The rest student is one! Please only consider for A TEAM WITH MORE MEMBER to avoid some troubles causing by only one member in a team !"
				return render_template('Form/Notice.html',consider=consider,Message=Message,amount=row,MemberAmount=MemberAmount,mode=int(row % MemberAmount),display=str(CourseID),teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)
			
			else:

				time = int(row/MemberAmount)
				i = 0
				if formMethod == "random":     ####随机分方法
					if consider == "NOGPA":
						sql = "INSERT INTO team_method VALUES('%d','%d','%d',0,0,1,0,null)" %(CourseID,row,MemberAmount)
						cursor.execute(sql)
						db.commit()
						for teamAmount in range(1,time+1):
							for a in range(1,MemberAmount+1):
								sql = "INSERT INTO team_all VALUES('%d','%s','%d',null)" %(CourseID,str(result[i][0]),teamAmount)
								cursor.execute(sql)
								db.commit()

								sql = "INSERT INTO team VALUES('%s',1.0,0,'M','%d','%d')" %(str(result[i][0]),CourseID,teamAmount)
								cursor.execute(sql)
								db.commit()

								sql = "UPDATE student SET TeamNO = '%d' WHERE Stu_Name = '%s' " %(teamAmount,str(result[i][0]))
								cursor.execute(sql)
								db.commit()

								i = i + 1
						
						db_op = DatabaseOperations()
						results = db_op.display(CourseID)
						return render_template('Form/Display.html',display=results,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)
					else:

						sql = "INSERT INTO team_method VALUES('%d','%d','%d',0,1,0,1,null)" %(CourseID,row,MemberAmount)
						cursor.execute(sql)
						db.commit()
						TotalGPA = 0.00
						for i in range(0,row):
							TotalGPA = TotalGPA + result[i][3]
						return render_template('Form/GPA.html',AverageGPA=float(TotalGPA/row),courseID=str(CourseID),teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)
				elif formMethod == "free":

					sql = "INSERT INTO team_method VALUES('%d','%d','%d',1,0,0,0,null)" %(CourseID,row,MemberAmount)
					cursor.execute(sql)
					db.commit()
					return render_template('Teacher/Teacher.html',teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)
				else:
					if consider == "NOGPA":

						sql = "INSERT INTO team_method VALUES('%d','%d','%d',0,1,0,0,null)" %(CourseID,row,MemberAmount)
						cursor.execute(sql)
						db.commit()
						return render_template('Teacher/Teacher.html',teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)

					else:

						sql = "INSERT INTO team_method VALUES('%d','%d','%d',0,1,0,1,null)" %(CourseID,row,MemberAmount)
						cursor.execute(sql)
						db.commit()
						TotalGPA = 0.00
						for i in range(0,row):
							TotalGPA = TotalGPA + result[i][3]
						return render_template('Form/GPA.html',AverageGPA=float(TotalGPA/row),courseID=str(CourseID),teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)

##################   老师的显示分组方法
@app.route('/TeDisplayTeam',methods=['GET', 'POST'])
def TeDisplayTeam():
	######################通用三项数据
	teacherName = request.form["teacherName"]
	CourseID = request.form["CourseID"]
	CourseID = int(CourseID)
	CourseName = request.form["CourseName"]
	##############################  ,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName

	db = pymysql.connect("127.0.0.1", "root", "", "project fruit")
	with db.cursor() as cursor:

		sql = "SELECT TeamNO,Stu_Name,Identify from team WHERE CourseID = '%d' " %int(CourseID)
		cursor.execute(sql)
		Results = cursor.fetchall()

		return render_template('Form/DisplayTeam.html',Results=Results,teacherName=teacherName,CourseID=CourseID,CourseName=CourseName)


@app.route('/student',methods=['GET', 'POST'])
def student():

	#####获取三项通用
	Stu_ID = request.form["Stu_ID"]
	Stu_ID = int(Stu_ID)
	StudentName = request.form["StudentName"]
	CourseID = request.form["CourseID"]
	CourseID = int(CourseID)
	#####以上 ,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID

	return render_template('Student/Student.html',StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)

@app.route('/ChooseMember',methods=['GET', 'POST'])
def ChooseMember():

	#####获取三项通用
	Stu_ID = request.form["Stu_ID"]
	Stu_ID = int(Stu_ID)
	StudentName = request.form["StudentName"]
	CourseID = request.form["CourseID"]
	CourseID = int(CourseID)
	#####以上 ,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID

	db = pymysql.connect("127.0.0.1", "root", "", "project fruit")
	with db.cursor() as cursor:

		sql = "select CourseID,Stu_name,Stu_ID from student WHERE CourseID = (select CourseID from student WHERE Stu_ID = '%d' ) AND Stu_ID <> '%d'" %(Stu_ID,Stu_ID)
		cursor.execute(sql)
		results = cursor.fetchall()

		sql = "select Course_Title from course WHERE CourseID = '%d'" %(CourseID)
		cursor.execute(sql)
		resultName = cursor.fetchone()

		sql = "select Stu_Name from student WHERE Stu_ID = '%d'" %Stu_ID
		cursor.execute(sql)
		invitator = cursor.fetchone()

		################## 随机分组时
		sql = "SELECT random FROM team_method WHERE CourseID = '%d' " %(CourseID)
		cursor.execute(sql)
		method = cursor.fetchone()
		method = int(method[0])

		sql = "SELECT * FROM team WHERE Stu_Name = '%s'" %StudentName
		cursor.execute(sql)
		exist = cursor.rowcount
		
		if method == 1 or exist > 0:

			db_op = DatabaseOperations()
			results = db_op.displayTeam(StudentName)

			sql = "SELECT Course_Title from course WHERE CourseID = '%d'" %(CourseID)
			cursor.execute(sql)
			CourseName = cursor.fetchone()
			CourseName = str(CourseName[0])

			sql = "SELECT TeamName from team_all WHERE CourseID = '%d' AND TeamNO = '%d'" %(CourseID,int(results[0][2]))
			cursor.execute(sql)
			TeamName = cursor.fetchone()
			TeamName = str(TeamName[0])

			Message = "Notice: Form team has already done."

			return render_template('Student/DisplayTeam.html',TeamName=TeamName,results=results,CourseName=CourseName,Stu_name=StudentName,Message=Message,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)
			################

		sql = "SELECT * FROM tablesum WHERE CourseID = '%d' " %CourseID
		cursor.execute(sql)
		TableExist = cursor.rowcount

		if TableExist == 0:
			sql = "INSERT INTO tablesum VALUES('%d',0)" %CourseID
			cursor.execute(sql)
			db.commit()

		return render_template('Student/ChooseMember.html',invitator=str(invitator[0]),results=results,resultName=str(resultName[0]),CourseID=int(results[0][0]),StudentName=StudentName,Stu_ID=Stu_ID)

@app.route('/check',methods=['GET','POST'])
def check():
	if request.method == 'POST':

		#####获取三项通用
		Stu_ID = request.form["Stu_ID"]
		Stu_ID = int(Stu_ID)
		StudentName = request.form["StudentName"]
		CourseID = request.form["CourseID"]
		CourseID = int(CourseID)
		#####以上 ,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID

		name = request.form["invitator"]
		db_op = DatabaseOperations()
		results = db_op.CheckOP1(name)
		Invitation_Result = db_op.CheckOP2(name)

		##########
		sql = "select Free,Multiple from team_method WHERE CourseID = '%d'" %CourseID
		cursor.execute(sql)
		# method = cursor.fetchone()

		return render_template('Student/CheckTeamState.html',results=results,Invitation_Result=Invitation_Result,Myself=name,CourseID=CourseID, StudentName=StudentName,Stu_ID=Stu_ID)

@app.route('/CheckTeamState',methods=['GET', 'POST'])
def CheckTeamState():        
	if request.method == 'POST':

		#####获取三项通用
		Stu_ID = request.form["Stu_ID"]
		Stu_ID = int(Stu_ID)
		StudentName = request.form["StudentName"]
		CourseID = request.form["CourseID"]
		CourseID = int(CourseID)
		#####以上 ,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID

		name = request.form["invitator"]
		friendName = request.form["invite"]
		
		db = pymysql.connect("127.0.0.1", "root", "", "project fruit")
		with db.cursor() as cursor:

			sql = "INSERT INTO friend VALUES('%s','%s','No response',null)" %(name,friendName)
			cursor.execute(sql)
			db.commit()

			sql = "INSERT INTO friend VALUES('%s',null,'No response','%s')" %(friendName,name)
			cursor.execute(sql)
			db.commit()

			db_op = DatabaseOperations()
			results = db_op.CheckOP1(name)
			Invitation_Result = db_op.CheckOP2(name)

			return render_template('Student/CheckTeamState.html',results=results,Invitation_Result=Invitation_Result,Myself=name,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)

@app.route('/AcceptInvitation',methods=['GET', 'POST'])
def AcceptInvitation():        
	if request.method == 'POST':

		#####获取三项通用
		Stu_ID = request.form["Stu_ID"]
		Stu_ID = int(Stu_ID)
		StudentName = request.form["StudentName"]
		CourseID = request.form["CourseID"]
		CourseID = int(CourseID)
		#####以上 ,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID

		myself = request.form["self"]
		Object = request.form["Object"]
		
		db = pymysql.connect("127.0.0.1", "root", "", "project fruit")
		with db.cursor() as cursor:
			
			sql = "SELECT Total_Amount from team_method WHERE CourseID = '%d' " %CourseID
			cursor.execute(sql)
			TotalAmount = cursor.fetchone()
			TotalAmount = int(TotalAmount[0])

			sql = "select Free,Multiple from team_method WHERE CourseID = '%d'" %CourseID
			cursor.execute(sql)
			method = cursor.fetchone()

			if int(method[0]) == 1: #方法是Free (weiwanncheng)

				###更新friend数据库状态 在选择按钮之后###
				sql = "DELETE from friend WHERE Stu_name = '%s' AND Invitation_Name = '%s'" %(myself,Object)
				cursor.execute(sql)
				db.commit()

				sql = "UPDATE friend SET Invitation_State = 'Accepted' WHERE Stu_Name = '%s' AND Friend_Name = '%s'" %(Object,myself)
				cursor.execute(sql)
				db.commit()
				### 请注意，上面这条更新的测试结果查看需要更换用户名，也就是以你这次邀请的人的身份登录才能生效，测试需要自行添加数据库条目 或检查数据库状态###
				
				sql = "select DISTINCT CourseID,TeamNO from team_all WHERE CourseID = '%d' " %CourseID
				cursor.execute(sql)
				TeamExisitNum = cursor.rowcount

				sql = "select Total_Amount,Member_Num from team_method WHERE CourseID = '%d' " %CourseID
				cursor.execute(sql)
				CalTeamNO = cursor.fetchone()
				
				Full = int(CalTeamNO[1])  #######存疑 注意是否报错

				db_op = DatabaseOperations()
				Sum = db_op.GetSum(CourseID)

				flag = True

				for TableNum in range(0,TotalAmount):

					if Sum == 0:	 
						sql_create = "CREATE TABLE `%s` ( `Stu_Name` VARCHAR(10) NOT NULL,`Full` INT(2) NOT NULL) ENGINE = InnoDB;" %str(TableNum)
						cursor.execute(sql_create)
						db.commit()

						sql = "UPDATE tablesum SET NUM = NUM + 1"
						cursor.execute(sql)
						db.commit()
						db_op = DatabaseOperations()
						Sum = db_op.GetSum(CourseID)

						sql = "INSERT INTO `%d` (`Stu_Name`, `Full`) VALUES('%s','%d')" %(TableNum,Object,Full)
						cursor.execute(sql)
						db.commit()
						
					sql = "SELECT * FROM `%d` WHERE Stu_Name='%s' " %(TableNum,Object)
					cursor.execute(sql)
					CheckExist = cursor.rowcount

					if CheckExist > 0:
						sql = "INSERT INTO `%d` (`Stu_Name`, `Full`) VALUES ('%s', '%d')" %(TableNum,myself,Full)
						cursor.execute(sql)
						db.commit()

						##########加进team
						sql = "SELECT * FROM `%d`" %TableNum
						cursor.execute(sql)
						CurrentNum = cursor.rowcount

						sql = "SELECT * FROM team WHERE CourseID = '%d' " %CourseID
						cursor.execute(sql)
						CurrentTeamMember = cursor.rowcount

						RestNum = TotalAmount - CurrentTeamMember

						if CurrentNum == Full:

							TeamNO = TeamExisitNum + 1
							sql = "SELECT Stu_name from `%d`" %TableNum
							cursor.execute(sql)
							Info = cursor.fetchall()

							for a in range(0,Full):

								sql = "INSERT INTO team_all VALUES('%d','%s','%d',null)" %(CourseID,str(Info[a][0]),TeamNO)
								cursor.execute(sql)
								db.commit()

								sql = "INSERT INTO team VALUES('%s',1.0,0,'M','%d','%d')" %(str(Info[a][0]),CourseID,TeamNO)
								cursor.execute(sql)
								db.commit()

								sql = "UPDATE student set TeamNO = '%d' WHERE Stu_Name = '%s' " %(TeamNO,str(Info[a][0]))
								cursor.execute(sql)
								db.commit()

						sql = "SELECT * FROM team WHERE CourseID = '%d' " %CourseID
						cursor.execute(sql)
						CurrentTeamMember = cursor.rowcount

						RestNum = TotalAmount - CurrentTeamMember

						sql = "select DISTINCT CourseID,TeamNO from team_all WHERE CourseID = '%d' " %CourseID
						cursor.execute(sql)
						TeamExisitNum = cursor.rowcount

						if RestNum < Full:

							Mode = int(CalTeamNO[0]) % int(CalTeamNO[1]) #friend 也可以用这里的方法
							
							if str(method[1]) == "L": 	
								TeamNO = TeamExisitNum + 1
							elif str(method[1]) == "M":
								TeamNO = TeamExisitNum

							if RestNum == Mode:
								sql = "SELECT Stu_Name from student WHERE TeamNO IS NULL AND CourseID = '%d' " %CourseID
								cursor.execute(sql)
								Info = cursor.fetchall()

								for a in range(0,Mode):

									sql = "INSERT INTO team_all VALUES('%d','%s','%d',null)" %(CourseID,str(Info[a][0]),TeamNO)
									cursor.execute(sql)
									db.commit()

									sql = "INSERT INTO team VALUES('%s',1.0,0,'M','%d','%d')" %(str(Info[a][0]),CourseID,TeamNO)
									cursor.execute(sql)
									db.commit()

									sql = "UPDATE student set TeamNO = '%d' WHERE Stu_Name = '%s' " %(TeamNO,str(Info[a][0]))
									cursor.execute(sql)
									db.commit()

								###############################

						break

					else:
						for i in range(0,Sum):

							sql = "SELECT * from `%d` WHERE Stu_Name = '%s' " %(i,Object)
							cursor.execute(sql)
							CheckExist = cursor.rowcount

							if CheckExist > 0:
								sql = "INSERT INTO `%d` (`Stu_Name`, `Full`) VALUES('%s','%d')" %(i,myself,Full)
								cursor.execute(sql)
								db.commit()

								##########加进team
								sql = "SELECT * FROM `%d`" %i
								cursor.execute(sql)
								CurrentNum = cursor.rowcount

								sql = "SELECT * FROM team WHERE CourseID = '%d' " %CourseID
								cursor.execute(sql)
								CurrentTeamMember = cursor.rowcount

								RestNum = TotalAmount - CurrentTeamMember

								if CurrentNum == Full:

									TeamNO = TeamExisitNum + 1
									sql = "SELECT Stu_name from `%d`" %i
									cursor.execute(sql)
									Info = cursor.fetchall()

									for a in range(0,Full):

										sql = "INSERT INTO team_all VALUES('%d','%s','%d',null)" %(CourseID,str(Info[a][0]),TeamNO)
										cursor.execute(sql)
										db.commit()

										sql = "INSERT INTO team VALUES('%s',1.0,0,'M','%d','%d')" %(str(Info[a][0]),CourseID,TeamNO)
										cursor.execute(sql)
										db.commit()

										sql = "UPDATE student set TeamNO = '%d' WHERE Stu_Name = '%s' " %(TeamNO,str(Info[a][0]))
										cursor.execute(sql)
										db.commit()
								
								sql = "SELECT * FROM team WHERE CourseID = '%d' " %CourseID
								cursor.execute(sql)
								CurrentTeamMember = cursor.rowcount

								RestNum = TotalAmount - CurrentTeamMember

								sql = "select DISTINCT CourseID,TeamNO from student WHERE CourseID = '%d' AND TeamNO IS NOT NULL" %CourseID
								cursor.execute(sql)
								TeamExisitNum = cursor.rowcount

								if RestNum < Full:

									Mode = int(CalTeamNO[0]) % int(CalTeamNO[1]) #friend 也可以用这里的方法
									
									if str(method[1]) == "L": 	
										TeamNO = TeamExisitNum + 1
									else:
										TeamNO = TeamExisitNum

									if RestNum == Mode:
										sql = "SELECT Stu_Name from student WHERE TeamNO IS NULL"
										cursor.execute(sql)
										Info = cursor.fetchall()
										checkV = cursor.rowcount
										
										# if checkV != 0:
										for a in range(0,Mode):

											sql = "INSERT INTO team_all VALUES('%d','%s','%d',null)" %(CourseID,str(Info[a][0]),TeamNO)
											cursor.execute(sql)
											db.commit()

											sql = "INSERT INTO team VALUES('%s',1.0,0,'M','%d','%d')" %(str(Info[a][0]),CourseID,TeamNO)
											cursor.execute(sql)
											db.commit()

											sql = "UPDATE student set TeamNO = '%d' WHERE Stu_Name = '%s' " %(TeamNO,str(Info[a][0]))
											cursor.execute(sql)
											db.commit()
								###########

								flag = False
								break

						if flag == False:
							break

						sql_create = "CREATE TABLE `%s` ( `Stu_Name` VARCHAR(10) NOT NULL,`Full` INT(2) NOT NULL) ENGINE = InnoDB;" %str(Sum)
						cursor.execute(sql_create)
						db.commit()

						sql = "INSERT INTO `%d` (`Stu_Name`, `Full`) VALUES('%s','%d')" %(Sum,Object,Full)
						cursor.execute(sql)
						db.commit()
						
						sql = "UPDATE tablesum SET NUM = NUM + 1"
						cursor.execute(sql)
						db.commit()
						db_op = DatabaseOperations()
						Sum = db_op.GetSum(CourseID)

				########################################### end of for

				db_op = DatabaseOperations()
				results = db_op.CheckOP1(myself)
				Invitation_Result = db_op.CheckOP2(myself)
			
			else: ####搭档方法                        888888888888888888888888888888888888888888888888888888888888888
				
				sql = "select DISTINCT CourseID,TeamNO from team_all WHERE CourseID = '%d' " %CourseID
				cursor.execute(sql)
				TeamExisitNum = cursor.rowcount

				sql = "select Total_Amount,Member_Num from team_method WHERE CourseID = '%d' " %CourseID
				cursor.execute(sql)
				CalTeamNO = cursor.fetchone()
				
				Full = int(CalTeamNO[1])

				###更新friend数据库状态 在选择按钮之后###
				if Full == 2:
					sql = "DELETE from friend WHERE Invitation_Name = '%s'" %Object
					cursor.execute(sql)
					db.commit()
				
				sql = "DELETE from friend WHERE Stu_name = '%s' AND Invitation_Name = '%s'" %(myself,Object)
				cursor.execute(sql)
				db.commit()

				sql = "UPDATE friend SET Invitation_State = 'Accepted' WHERE Stu_Name = '%s' AND Friend_Name = '%s'" %(Object,myself)
				cursor.execute(sql)
				db.commit()
				### 请注意，上面这条更新的测试结果查看需要更换用户名，也就是以你这次邀请的人的身份登录才能生效，测试需要自行添加数据库条目 或检查数据库状态###
				####设定为预备组员

				sql = "UPDATE student SET TeamNO = 0 WHERE Stu_Name = '%s' " %Object
				cursor.execute(sql)
				db.commit()

				sql = "UPDATE student SET TeamNO = 0 WHERE Stu_Name = '%s' " %myself
				cursor.execute(sql)
				db.commit()

				sql = "SELECT Stu_Name from student WHERE TeamNO = 0"
				cursor.execute(sql)
				CurrentPreMember = cursor.rowcount
				NameList = cursor.fetchall()

				sql = "SELECT DISTINCT TeamNO from student WHERE TeamNO IS NOT NULL AND TeamNO != 0 "
				cursor.execute(sql)
				CurrentTeamNum = cursor.rowcount

				if CurrentPreMember == Full:
					CurrentTeamNum = CurrentTeamNum + 1
					for i in range(0,Full):

						sql = "INSERT INTO team_all VALUES('%d','%s','%d',null)" %(CourseID,str(NameList[i][0]),CurrentTeamNum)
						cursor.execute(sql)
						db.commit()

						sql = "INSERT INTO team VALUES('%s',1.0,0,'M','%d','%d')" %(str(NameList[i][0]),CourseID,CurrentTeamNum)
						cursor.execute(sql)
						db.commit()

						sql = "UPDATE student set TeamNO = '%d' WHERE Stu_Name = '%s' " %(CurrentTeamNum,str(NameList[i][0]))
						cursor.execute(sql)
						db.commit()

				if str(method[1]) == "L": 	
					TeamMax = int(int(CalTeamNO[0])/int(CalTeamNO[1])) + 1
					if CurrentTeamNum == TeamMax-1:

						CurrentTeamNum = CurrentTeamNum + 1
						sql = "SELECT Stu_Name from student WHERE TeamNO IS NULL OR TeamNO = 0 "
						cursor.execute(sql)
						NameList2 = cursor.fetchall()
						Full = cursor.rowcount

						for i in range(0,Full):

							sql = "INSERT INTO team_all VALUES('%d','%s','%d',null)" %(CourseID,str(NameList2[i][0]),CurrentTeamNum)
							cursor.execute(sql)
							db.commit()

							sql = "INSERT INTO team VALUES('%s',1.0,0,'M','%d','%d')" %(str(NameList2[i][0]),CourseID,CurrentTeamNum)
							cursor.execute(sql)
							db.commit()

							sql = "UPDATE student set TeamNO = '%d' WHERE Stu_Name = '%s' " %(CurrentTeamNum,str(NameList2[i][0]))
							cursor.execute(sql)
							db.commit()

				if str(method[1]) == "M":
					TeamMax = int(int(CalTeamNO[0])/int(CalTeamNO[1]))
					if CurrentTeamNum == TeamMax:
						
						CurrentTeamNum = CurrentTeamNum + 1

						sql = "SELECT Stu_Name from student WHERE TeamNO IS NULL OR TeamNO = 0 "
						cursor.execute(sql)
						NameList2 = cursor.fetchall()
						Full = cursor.rowcount

						for i in range(0,Full):

							sql = "INSERT INTO team_all VALUES('%d','%s','%d',null)" %(CourseID,str(NameList2[i][0]),CurrentTeamNum)
							cursor.execute(sql)
							db.commit()

							sql = "INSERT INTO team VALUES('%s',1.0,0,'M','%d','%d')" %(str(NameList2[i][0]),CourseID,CurrentTeamNum)
							cursor.execute(sql)
							db.commit()

							sql = "UPDATE student set TeamNO = '%d' WHERE Stu_Name = '%s' " %(CurrentTeamNum,str(NameList2[i][0]))
							cursor.execute(sql)
							db.commit()

				db_op = DatabaseOperations()
				results = db_op.CheckOP1(myself)
				Invitation_Result = db_op.CheckOP2(myself)

			return render_template('Student/CheckTeamState.html',a=int(CalTeamNO[0]) / int(CalTeamNO[1]),results=results,Invitation_Result=Invitation_Result,Myself=myself,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)


@app.route('/RejectInvitation',methods=['GET', 'POST'])
def RejectInvitation():        
	if request.method == 'POST':

		#####获取三项通用
		Stu_ID = request.form["Stu_ID"]
		Stu_ID = int(Stu_ID)
		StudentName = request.form["StudentName"]
		CourseID = request.form["CourseID"]
		CourseID = int(CourseID)
		#####以上 ,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID

		myself = request.form["self"]
		Object = request.form["Object"]

		db = pymysql.connect("127.0.0.1", "root", "", "project fruit")
		with db.cursor() as cursor:

			###更新friend数据库状态 在选择按钮之后###
			sql = "DELETE from friend WHERE Stu_name = '%s' AND Invitation_Name = '%s'" %(myself,Object)
			cursor.execute(sql)
			db.commit()

			sql = "UPDATE friend SET Invitation_State = 'Refused' WHERE Stu_Name = '%s' AND Friend_Name = '%s'" %(Object,myself)
			cursor.execute(sql)
			db.commit()
			### 请注意，上面这条更新的测试结果查看需要更换用户名，也就是以你这次邀请的人的身份登录才能生效，测试需要自行添加数据库条目 或检查数据库状态###
				
			db_op = DatabaseOperations()
			results = db_op.CheckOP1(myself)
			Invitation_Result = db_op.CheckOP2(myself)
			return render_template('Student/CheckTeamState.html',results=results,Invitation_Result=Invitation_Result,Myself=myself,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)


@app.route('/DisplayTeam',methods=['GET', 'POST'])
def DisplayTeam():

	#####获取三项通用
	Stu_ID = request.form["Stu_ID"]
	Stu_ID = int(Stu_ID)
	StudentName = request.form["StudentName"]
	CourseID = request.form["CourseID"]
	CourseID = int(CourseID)
	#####以上 ,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID

	db_op = DatabaseOperations()
	results = db_op.displayTeam(StudentName)

	if len(results) == 0:
		Message = "Error: You don't have a Team yet.."
		return render_template('Student/EvaluateFail.html',Message=Message,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)

	db = pymysql.connect("127.0.0.1", "root", "", "project fruit")
	with db.cursor() as cursor:

		sql = "SELECT Course_Title from course WHERE CourseID = '%d'" %CourseID
		cursor.execute(sql)
		CourseName = cursor.fetchone()
		CourseName = str(CourseName[0])

		sql = "SELECT TeamName from team_all WHERE CourseID = '%d' AND TeamNO = '%d'" %(CourseID,int(results[0][2]))
		cursor.execute(sql)
		TeamName = cursor.fetchone()
		TeamName = str(TeamName[0])

		################### 随机分组时
		sql = "SELECT random FROM team_method WHERE CourseID = '%d' " %(results[0][0])
		cursor.execute(sql)
		method = cursor.fetchone()
		method = int(method[0])
		
		if method == 1:

			db_op = DatabaseOperations()
			results = db_op.displayTeam(StudentName)

			sql = "SELECT Course_Title from course WHERE CourseID = '%d'" %(int(results[0][0]))
			cursor.execute(sql)
			CourseName = cursor.fetchone()
			CourseName = str(CourseName[0])

			sql = "SELECT TeamName from team_all WHERE CourseID = '%d' AND TeamNO = '%d'" %(int(results[0][0]),int(results[0][2]))
			cursor.execute(sql)
			TeamName = cursor.fetchone()
			TeamName = str(TeamName[0])

			Message = "Notice: Form team has already done."

			return render_template('Student/DisplayTeam.html',TeamName=TeamName,results=results,CourseName=CourseName,Stu_name=StudentName,Message=Message,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)
			#################

		return render_template('Student/DisplayTeam.html',TeamName=TeamName,results=results,CourseName=CourseName,Stu_name=StudentName,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)

@app.route('/SetTeamName',methods=['GET', 'POST'])             #````````````````````````````````````done```````````````````````````````
def SetTeamName():
	if request.method == 'POST':

		#####获取三项通用
		Stu_ID = request.form["Stu_ID"]
		Stu_ID = int(Stu_ID)
		StudentName = request.form["StudentName"]
		CourseID = request.form["CourseID"]
		CourseID = int(CourseID)
		#####以上 ,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID

		StudentName = request.form["self"]
		TeamName = request.form["TeamName"]
		TeamNO = int(request.form["TeamNO"])
		db_op = DatabaseOperations()
		results = db_op.displayTeam(StudentName)
		db = pymysql.connect("127.0.0.1", "root", "", "project fruit")
		with db.cursor() as cursor:

			sql = "UPDATE team_all SET TeamName = '%s' WHERE TeamNO = '%d'" %(TeamName,TeamNO)
			cursor.execute(sql)
			db.commit()

			sql = "SELECT Course_Title from course WHERE CourseID = '%d'" %(int(results[0][0]))
			cursor.execute(sql)
			CourseName = cursor.fetchone()
			CourseName = str(CourseName[0])

			sql = "SELECT TeamName from team_all WHERE CourseID = '%d' AND TeamNO = '%d'" %(int(results[0][0]),int(results[0][2]))
			cursor.execute(sql)
			TeamName = cursor.fetchone()
			TeamName = str(TeamName[0])
			return render_template('Student/DisplayTeam.html',TeamName=TeamName,results=results,CourseName=CourseName,Stu_name=StudentName,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)

@app.route('/vote',methods=['GET', 'POST'])                    #````````````````````````````````````done```````````````````````````````
def vote():
	#####获取三项通用
	Stu_ID = request.form["Stu_ID"]
	Stu_ID = int(Stu_ID)
	StudentName = request.form["StudentName"]
	CourseID = request.form["CourseID"]
	CourseID = int(CourseID)
	#####以上 ,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID   CourseID,Stu_Name,TeamNO
	
	db = pymysql.connect("127.0.0.1", "root", "", "project fruit")
	with db.cursor() as cursor:

		sql = "SELECT * from team WHERE Stu_Name = '%s' " %StudentName
		cursor.execute(sql)
		CheckExist = cursor.rowcount
		
		if CheckExist == 0:
			Message = "Error: You don't have a Team yet.."
			return render_template('Student/EvaluateFail.html',Message=Message,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)

		sql = "SELECT TeamNO from student WHERE Stu_ID = '%d' " %Stu_ID
		cursor.execute(sql)
		TeamNO = cursor.fetchone()
		TeamNO = int(TeamNO[0])

		sql = "SELECT * FROM vote WHERE TeamNO = '%d' AND Stu_Name = '%s' " %(TeamNO,StudentName)
		cursor.execute(sql)
		exist = cursor.rowcount

		sql = "SELECT TeamName,Stu_Name FROM team_all WHERE TeamNO = '%d' AND CourseID = '%d' " %(TeamNO,CourseID)
		cursor.execute(sql)
		List = cursor.fetchall()
		TeamName = str(List[0][0])
		Num = cursor.rowcount

		if exist == 0:
			for i in range(0,Num):
				sql = "INSERT INTO vote VALUES('%d','%s','%s',0,0)"  %(TeamNO,TeamName,List[i][1])
				cursor.execute(sql)
				db.commit()

		sql = "SELECT * FROM vote WHERE TeamNO = '%d' " %TeamNO
		cursor.execute(sql)
		VoteResult = cursor.fetchall()
		All = cursor.rowcount
		
		sql = "SELECT CheckVote from vote WHERE Stu_Name = '%s' " %StudentName
		cursor.execute(sql)
		AlreadyVote = cursor.fetchone()
		AlreadyVote = int(AlreadyVote[0])
		
		if AlreadyVote == 0:
			return render_template('Student/vote.html',TeamNO=TeamNO,TeamName=TeamName,VoteResult=VoteResult,CourseID=CourseID,StudentName=StudentName,Stu_ID=Stu_ID)
		elif AlreadyVote == 1:
			
			sql = "SELECT * FROM vote WHERE CheckVote = '1' AND TeamNO = '%d' " %TeamNO
			cursor.execute(sql)
			CheckAll = cursor.rowcount

			if CheckAll == All:
				sql = "SELECT Stu_Name FROM vote ORDER BY Votes desc"
				cursor.execute(sql)
				Leader = cursor.fetchone()
				Leader = str(Leader[0])

				sql = "UPDATE team SET Identify = 'L' WHERE TeamNO = '%d' AND  Stu_Name = '%s' " %(int(VoteResult[0][0]),Leader)
				cursor.execute(sql)
				db.commit()
				
				###########
				sql = "SELECT Title from submission_item WHERE CourseID = '%d' " %CourseID
				cursor.execute(sql)
				Title_list = cursor.fetchall()
				Title_num = cursor.rowcount

				sql = "SELECT Stu_name FROM team WHERE TeamNO = '%d' AND Identify = 'M' " %int(VoteResult[0][0])
				cursor.execute(sql)
				Stu_list = cursor.fetchall()

				sql = "select * FROM Temp_ctr where Stu_Name = '%s' " %str(Stu_list[0][0])
				cursor.execute(sql)
				exist = cursor.rowcount

				if exist == 0:
					for StuNum in range(0,All-1):
						for TitleNum in range(0,Title_num):
							sql = "INSERT INTO Temp_ctr VALUES('%d','%s','%s',0) " %(CourseID,str(Stu_list[StuNum][0]),str(Title_list[TitleNum][0]))
							cursor.execute(sql)
							db.commit()
				##############

				Message = "Leader is: " + Leader
				return render_template('Student/voteResult.html',TeamName=TeamName,VoteResult=VoteResult,Message=Message,CourseID=CourseID,StudentName=StudentName,Stu_ID=Stu_ID)

			return render_template('Student/voteResult.html',TeamName=TeamName,VoteResult=VoteResult,CourseID=CourseID,StudentName=StudentName,Stu_ID=Stu_ID)

@app.route('/VoteLeader',methods=['GET', 'POST'])              #````````````````````````````````````done```````````````````````````````
def VoteLeader():
	if request.method == 'POST':

		#####获取三项通用
		Stu_ID = request.form["Stu_ID"]
		Stu_ID = int(Stu_ID)
		StudentName = request.form["StudentName"]
		CourseID = request.form["CourseID"]
		CourseID = int(CourseID)
		#####以上 ,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID

		Voter = StudentName
		VoteFor = request.form["Vote"]
		TeamName = request.form["TeamName"]
		TeamNO = request.form["TeamNO"]
		TeamNO = int(TeamNO)

		db = pymysql.connect("127.0.0.1", "root", "", "project fruit")
		with db.cursor() as cursor:
			sql = "SELECT Votes FROM vote WHERE Stu_name = '%s'" %VoteFor
			cursor.execute(sql)
			PreVotes = cursor.fetchone()
			PreVotes = int(PreVotes[0]) + 1

			sql = "UPDATE vote SET Votes = '%d' WHERE Stu_name = '%s'" %(PreVotes,VoteFor)
			cursor.execute(sql)
			db.commit()

			sql = "UPDATE vote SET CheckVote = '1' WHERE Stu_Name = '%s' " %Voter
			cursor.execute(sql)
			db.commit()

			sql = "SELECT * FROM vote WHERE TeamNO = '%d' " %TeamNO
			cursor.execute(sql)
			VoteResult = cursor.fetchall()
			All = cursor.rowcount

			sql = "SELECT * FROM vote WHERE CheckVote = '1' AND TeamNO = '%d' " %TeamNO
			cursor.execute(sql)
			CheckAll = cursor.rowcount

			if CheckAll == All:
				sql = "SELECT Stu_Name FROM vote WHERE TeamNO = '%d' ORDER BY Votes desc " %TeamNO
				cursor.execute(sql)
				Leader = cursor.fetchone()
				Leader = str(Leader[0])

				sql = "UPDATE team SET Identify = 'L' WHERE TeamNO = '%d' AND  Stu_Name = '%s' " %(TeamNO,Leader)
				cursor.execute(sql)
				db.commit()

				###########
				sql = "SELECT Title from submission_item WHERE CourseID = '%d' " %CourseID
				cursor.execute(sql)
				Title_list = cursor.fetchall()
				Title_num = cursor.rowcount

				sql = "SELECT Stu_name FROM team WHERE TeamNO = '%d' AND Identify = 'M' " %TeamNO
				cursor.execute(sql)
				Stu_list = cursor.fetchall()

				sql = "select * FROM Temp_ctr where Stu_Name = '%s' " %str(Stu_list[0][0])
				cursor.execute(sql)
				exist = cursor.rowcount

				if exist == 0:
					for StuNum in range(0,All-1):
						for TitleNum in range(0,Title_num):
							sql = "INSERT INTO Temp_ctr VALUES('%d','%s','%s',0) " %(CourseID,str(Stu_list[StuNum][0]),str(Title_list[TitleNum][0]))
							cursor.execute(sql)
							db.commit()
				##############

				Message = "Leader is: " + Leader
				return render_template('Student/voteResult.html',TeamName=TeamName,VoteResult=VoteResult,Message=Message,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)

			return render_template('Student/voteResult.html',TeamName=TeamName,VoteResult=VoteResult,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)

@app.route('/Evaluate',methods=['GET', 'POST'])                #````````````````````````````````````done```````````````````````````````
def Evaluate():

	#####获取三项通用
	Stu_ID = request.form["Stu_ID"]
	Stu_ID = int(Stu_ID)
	StudentName = request.form["StudentName"]
	CourseID = request.form["CourseID"]
	CourseID = int(CourseID)
	#####以上

	db = pymysql.connect("127.0.0.1", "root", "", "project fruit")
	with db.cursor() as cursor:

		sql = "SELECT TeamName from team_all WHERE Stu_Name = (select Stu_Name from student WHERE Stu_ID = '%d')" %Stu_ID
		cursor.execute(sql)
		TeamName = cursor.fetchone()
		exist = cursor.rowcount

		if exist == 0:
			Message = "Error: You don't have a Team yet.."
			return render_template('Student/EvaluateFail.html',Message=Message,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)

		TeamName = str(TeamName[0])

		db_op = DatabaseOperations()
		results = db_op.displayTeam(StudentName)

		TeamNO = int(results[0][2])

		sql = "SELECT Stu_Name from team WHERE Identify = 'L' AND TeamNO = '%d' AND CourseID = '%d' " %(TeamNO,CourseID)
		cursor.execute(sql)
		Leader = cursor.fetchone()
		exist = cursor.rowcount

		if exist == 0:
			Message = "Error: You don't have a Team Leader.."
			return render_template('Student/EvaluateFail.html',Message=Message,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)
		
		Leader = str(Leader[0])

		if StudentName == Leader:
			Message = "Notice: You are leader, you cannot evaluate yourself!"
			return render_template('Student/EvaluateFail.html',Message=Message,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)
		
		return render_template('Student/Evaluate.html',TeamName=TeamName,Leader=Leader,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)


@app.route('/EvaluateLeader',methods=['GET', 'POST'])          #````````````````````````````````````done```````````````````````````````
def EvaluateLeader():
	if request.method == 'POST':

		#####获取三项通用
		Stu_ID = request.form["Stu_ID"]
		Stu_ID = int(Stu_ID)
		StudentName = request.form["StudentName"]
		CourseID = request.form["CourseID"]
		CourseID = int(CourseID)
		#####以上 ,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID

		Bonus = request.form["EvaluateButton"]
		TeamName = request.form["TeamName"]
		Leader = request.form["Leader"]
		Bonus = int(Bonus)
		db = pymysql.connect("127.0.0.1", "root", "", "project fruit")
		with db.cursor() as cursor:
			sql = "UPDATE team SET Bonus = '%f' WHERE Stu_Name = '%s' " %(float(Bonus),StudentName)
			cursor.execute(sql)
			db.commit()


			sql = "select TeamNO from team WHERE Stu_Name = '%s' " %StudentName
			cursor.execute(sql)
			TeamNO = cursor.fetchone()
			TeamNO = int(TeamNO[0])

			sql = "SELECT Bonus FROM team WHERE Identify = 'M' AND TeamNO = '%d'"  %TeamNO
			cursor.execute(sql)
			BonusList = cursor.fetchall()
			Num = cursor.rowcount
			Amount = float(Num)
			CurrentBonus = 0

			for i in range(0,Num):
				CurrentBonus = CurrentBonus + float(BonusList[i][0])
			
			AverageBonus = CurrentBonus/Amount

			sql = "UPDATE team SET Bonus = '%f' WHERE Identify = 'L' " %AverageBonus
			cursor.execute(sql)
			db.commit()
			Message = "Notice: You have selected " + str(Bonus)
			return render_template('Student/Evaluate.html',Message=Message,TeamName=TeamName,Leader=Leader,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)

@app.route('/SetCtr',methods=['GET', 'POST'])                  #````````````````````````````````````done```````````````````````````````
def SetCtr():

	#####获取三项通用
	Stu_ID = request.form["Stu_ID"]
	Stu_ID = int(Stu_ID)
	StudentName = request.form["StudentName"]
	CourseID = request.form["CourseID"]
	CourseID = int(CourseID)
	#####以上 ,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID
	
	db = pymysql.connect("127.0.0.1", "root", "", "project fruit")
	with db.cursor() as cursor:
		sql = "SELECT Course_Title from course WHERE CourseID = (SELECT CourseID from student WHERE Stu_ID = '%d' ) " %Stu_ID
		cursor.execute(sql)
		CourseName = cursor.fetchone()
		CourseName = str(CourseName[0])

		sql = "SELECT Stu_Name from student WHERE Stu_ID = '%d' " %Stu_ID
		cursor.execute(sql)
		Stu_Name = cursor.fetchone()
		Stu_Name = str(Stu_Name[0])

		db_op = DatabaseOperations()
		results = db_op.displayTeam(Stu_Name)

		if len(results) == 0:
			Message = "Error: You don't have a Team yet.."
			return render_template('Student/EvaluateFail.html',Message=Message,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)
		
		TeamNO = int(results[0][2])

		sql = "SELECT Stu_name FROM team WHERE TeamNO = '%d' AND Identify = 'M' " %TeamNO
		cursor.execute(sql)
		Stu_list = cursor.fetchall()

		sql = "SELECT Title from submission_item WHERE CourseID = '%d' " %int(results[0][0])
		cursor.execute(sql)
		Title_list = cursor.fetchall()

		sql = "SELECT Stu_Name from team WHERE Identify = 'L' AND TeamNO = '%d' AND CourseID = '%d' " %(TeamNO,int(results[0][0]))
		cursor.execute(sql)
		Leader = cursor.fetchone()
		exist = cursor.rowcount

		if exist == 0:
			Message = "Error: You don't have a Team Leader.."
			return render_template('Student/EvaluateFail.html',Message=Message,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)
		
		Leader = str(Leader[0])

		sql = "SELECT * FROM temp_ctr"
		cursor.execute(sql)
		exist = cursor.rowcount

		if Stu_Name != Leader:
			Message = "Notice: You are a team member, you are not able to set contribution!"
			return render_template('Student/SetCtrFail.html',Message=Message,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)
		elif exist == 0:
			Message = "Notice: You need to have a team leader before set contribution!"
			return render_template('Student/SetCtrFail.html',Message=Message,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)

		return render_template('Student/SetCtr.html',CourseName=CourseName,Stu_list=Stu_list,Title_list=Title_list,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID)

@app.route('/SetContribution',methods=['GET', 'POST'])         #````````````````````````````````````done```````````````````````````````
def SetContribution():
	if request.method == 'POST':

		#####获取三项通用
		Stu_ID = request.form["Stu_ID"]
		Stu_ID = int(Stu_ID)
		StudentName = request.form["StudentName"]
		CourseID = request.form["CourseID"]
		CourseID = int(CourseID)
		#####以上 ,StudentName=StudentName,CourseID=CourseID,Stu_ID=Stu_ID

		SelectStu = request.form["SelectStu"]
		SelectTitle = request.form["SelectTitle"]
		SelectCtr = request.form["SelectCtr"]
		db = pymysql.connect("127.0.0.1", "root", "", "project fruit")
		with db.cursor() as cursor:

			sql = "SELECT Course_Title from course WHERE CourseID = (SELECT CourseID from student WHERE Stu_ID = '%d' ) " %int(Stu_ID)
			cursor.execute(sql)
			CourseName = cursor.fetchone()
			CourseName = str(CourseName[0])

			sql = "SELECT Stu_Name from student WHERE Stu_ID = '%d' " %int(Stu_ID)
			cursor.execute(sql)
			Stu_Name = cursor.fetchone()
			Stu_Name = str(Stu_Name[0])

			db_op = DatabaseOperations()
			results = db_op.displayTeam(Stu_Name)
			TeamNO = int(results[0][2])

			sql = "SELECT Stu_name FROM team WHERE TeamNO = '%d' AND Identify = 'M' " %TeamNO
			cursor.execute(sql)
			Stu_list = cursor.fetchall()

			sql = "SELECT Title from submission_item WHERE CourseID = '%d' " %int(results[0][0])
			cursor.execute(sql)
			Title_list = cursor.fetchall()

			sql = "SELECT Percentage FROM submission_item WHERE Title = '%s' " %SelectTitle
			cursor.execute(sql)
			Percentage = cursor.fetchone()
			Percentage = float(Percentage[0])

			sql = "SELECT CheckSelect from temp_ctr WHERE Stu_Name = '%s' AND Submission_Title = '%s' " %(SelectStu,SelectTitle)
			cursor.execute(sql)
			CheckNum = cursor.fetchone()
			CheckNum = int(CheckNum[0])

			if CheckNum == 1:
				Message = "Error: You already set contribution for " + SelectStu + " on Title: " + SelectTitle
				return render_template('Student/SetCtr.html',CourseName=CourseName,Stu_list=Stu_list,Title_list=Title_list,Stu_ID=Stu_ID,Message=Message,StudentName=StudentName,CourseID=CourseID)

			sql = "UPDATE temp_ctr SET CheckSelect = 1 WHERE Stu_Name = '%s' AND Submission_Title = '%s' " %(SelectStu,SelectTitle)
			cursor.execute(sql)
			db.commit()

			sql = "SELECT Contribution from team WHERE Stu_Name = '%s' " %SelectStu
			cursor.execute(sql)
			CurrentCtr = cursor.fetchone()
			CurrentCtr = float(CurrentCtr[0])

			sql = "UPDATE team SET Contribution = '%f' WHERE Stu_Name = '%s' " %((CurrentCtr - (Percentage * float(SelectCtr))),SelectStu)
			cursor.execute(sql)
			db.commit()
			Message = "Operation confirmed: set contribution for " + SelectStu + " on Title: " + SelectTitle + " with contribution of " + str(1.00-float(SelectCtr))
			return render_template('Student/SetCtr.html',CourseName=CourseName,Stu_list=Stu_list,Title_list=Title_list,Stu_ID=Stu_ID,Message=Message,StudentName=StudentName,CourseID=CourseID)




class DatabaseOperations():
	__db_url = '127.0.0.1'
	__db_username = 'root' 
	__db_password = ''
	__db_name = 'project fruit'
	__db = ''

	def __init__(self):
		self.__db = self.db_connect()

	def __del__(self):
		self.__db.close()

	def db_connect(self):
		self.__db = pymysql.connect(
			self.__db_url, self.__db_username, self.__db_password, self.__db_name)
		return self.__db

	def display(self,CourseID):
		cursor = self.__db.cursor()
		try:
			sql = "SELECT CourseID,Stu_Name, TeamNO FROM team_all WHERE CourseID = '%d' order by TeamNO" %CourseID
			cursor.execute(sql)
			results = cursor.fetchall()
			return results
		except Exception as e:
			return None
	
	def displayTeam(self,Stu_name):
		cursor = self.__db.cursor()
		try:
			sql = "SELECT CourseID,Stu_Name,TeamNO,Identify FROM team WHERE TeamNO = (SELECT TeamNO from team WHERE Stu_Name = '%s')" %Stu_name
			cursor.execute(sql)
			results = cursor.fetchall()
			return results
		except Exception as e:
			return None
	
	def CheckOP1(self,name):
		cursor = self.__db.cursor()
		try:
			sql = "SELECT Friend_Name,Invitation_State from friend WHERE Stu_Name = '%s' AND Friend_Name is not null " %name
			cursor.execute(sql)
			results = cursor.fetchall()
			return results
		except Exception as e:
			return None
			
	def CheckOP2(self,name):
		cursor = self.__db.cursor()
		try:
			sql = "SELECT Invitation_Name from friend WHERE Stu_Name = '%s' AND Friend_Name is null" %name
			cursor.execute(sql)
			Invitation_Result = cursor.fetchall()
			return Invitation_Result
		except Exception as e:
			return None

	def GetSum(self,CourseID):
		cursor = self.__db.cursor()
		try:
			sql = "SELECT Num from tablesum WHERE CourseID = '%d' " %CourseID
			cursor.execute(sql)
			Sum = cursor.fetchone()
			Sum = int(Sum[0])
			return Sum
		except Exception as e:
			return None

###########part：
	def submission_order(self,CourseID):
		cursor = self.__db.cursor()
		try:
			sql = "SELECT * FROM submission_item WHERE CourseID = '%d' " %CourseID
			cursor.execute(sql)
			results = cursor.fetchall()
			return results
		except Exception as e:
			return None   
################## 
