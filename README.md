# IBSubjectSelect
#### Video Demo:  <https://youtu.be/Lyc-izV7BZA>
#### Description:
The goal of my project is to make the lives of IB students-particularly upcoming diploma students-easier by giving them an all in platform to plan their subject choices for the next two years

DATABASE-users.db
users: it records all the signup information of the users such as their name, email and passwords. It's then used to authenticate the users when they log in.
SISstudents- A list of students from the school(SIS) given directly by the school. When users register from SIS, their names are crosschecked with the list to ensure they are students.
SISteachers- A list of teachers from the school(SIS) given directly by the school. It also includes the subjects they teach.

HTML PAGES-
login.html: it takes the username and password of users and verifies it in the database before letting them proceed. 
logint.html- this is the login page for teachers. It also takes the username and password of users and verifies it in the database before letting them proceed. 
register.html: it takes the name, email, school and password of the users and verifies it with a school database. It also ensures the password meets the security requirements before registering them in the users database.

index.html: this page showcases all the subjects that the school(as of now, only SIS) offers. When they are clicked on(such as with aasl), they are further divided into 3 sections-
-A page to talk to other students interested in the course and see what they plan to do with it. This page is linked with the messages database to create a chatroom for the students.
-A page to talk to teachers of the course and get a better insight about what it would entail. This page is linked with the messages2 database to create a chatroom between the students and teachers.
-A page with all the prerequisites and resources for the course to help you be better prepared for it. It has subject guides, textbooks, practice problems and past papers.

index2.html: it allows students to plan their actual subjects(following the requirements for a regular diploma with two compulsory languages and one compulsory maths. science and humanity). It even allows them to choose the level they want to take it at- higher or standard.
The potential subject choices are saved in the user_subjects database and displayed to them on the screen.They can later be deleted as per the user's wishes.

subjectrec.html-If the user isn't sure of their subject choices, the website has an option for them to just tell it about their interests, hobbies or future plans and get combinations personalised for them(using the openai library)

When a user logs in as a teacher, they are taken to the chat with student screen for the subject they teach(extracted from the teachers database given by the school)

Through these features, the website makes the otherwise stressful subject selection process fun and easy!




Sample users to test the application-
Username, Password, School, Role
abc, abc123, SIS, Student
shraavya, shravya123, SIS, Student
test, tisb1234, TISB, Student
Dr.xyz, teach123, SIS, Teacher(AASL)
