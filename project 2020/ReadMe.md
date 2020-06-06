Database: 
	Xampp->admin
    	1. please execute the project.sql on xampp
		2. Then, please execute this two sql for the default username and password for teacher.
		INSERT INTO `course` (`CourseID`, `Course_Title`, `Teacher_Name`) VALUES ('1001', 'Math', 'Wang'), ('1002', 'Chinese', 'Wang_Chn'), ('1003', 'java', 'Jack_java');
		INSERT INTO `teacher` (`Teacher_Name`, `Password`) VALUES ('Wang', '123'), ('Wang_Chn', '123'), ('Jack_java', '123')

    
## library

```py
pip install Flask，xlrd, xlwt, os, sys
```

Run:
	1. Run Xampp with xampp-control.exe 
	2. Start Apache and MySQL, open the file of localhost database by click the Admin of MySQL.
	3. import the project.sql file in database.
	4. Run Windows PoweShell, cd to the directory of project2020.py
	5. input $env:FLASK_APP = "project2020.py" (make sure the import part has already done before this input)
	6. If run it on windows CMD, input 'set FLASK_APP=project2020.py' instead of step 5.
	7. input 'flask run'
	8. Open 'http://localhost:5000/' via a mainstream broswer.

Note:
	1. After login to teacher main page, please import the student excel file.
	2. The student excel file is on the /templates/import. At here, please change the path on line 303 in project2020.py to direct to your own computer path.
	3. As well as to export the file, please also change the path on line 371 in project2020.py
