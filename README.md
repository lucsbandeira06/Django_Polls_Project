# Polls/Accounts Django Project #
## Lucas Bandeira ##
### Student ID: 23884 ####

### CA1 - Back End development ###

On this project, the main objective was to create a polls web application using python where users can click on a question and choose an option to vote. This data will then be sent to a mysql database connected to a local host. To facilitate the process, it was used Django framework to install all dependencies and views in this project. The main idea is to create a polls application where football players can vote for best player of the match annonimously.

First step was to create a project in PyCharm CE. Once that was done, it was time to create a mini app within that project. As I use a MacOS, I had to install django and mysql extensions manually on my project. To create a mini app using Django, the command line 'python manage.py startapp 'appname' ' was entered on the terminal. By doing that, a virtual environment was created where this app will be run. By default, when you create an app using django framework, it installs some applications on your project, such as:     
    
    'django.contrib.admin'
    'django.contrib.auth'
    'django.contrib.contenttypes'
    'django.contrib.sessions'
    'django.contrib.messages'
    'django.contrib.staticfiles'

As the objective of this project was to create a polls application, another mini app was initiated within the root directory. By entering 'python manage.py startapp polls', a second mini app was created within the main project. It is important that you add this app to the settings.py on the main application, otherwise you would not be able to access it. Once I had done the installation of the polls app, in order to visualize the questions and choices on this poll app, it was neccesary to create views for this application in the file view.py. 

As we know index.html is always the first file that is rendered in an application by default. All html files were stored inside a directory called 'templates'. To make sure the application knows where to find this files, I did a small modification on the 'template' class in the setting files of the main application. By adding 'DIRS': [BASE_DIR / 'templates'] to this class, the application will search for a folder called templates to fetch those files when they are required.

After creating the home view, next step was to create a view for the details of each question and then another view for their results. It is important to mention that whenever there is a view which is linked to a html file, you must connect them through a file called urls.py. If you do not connect them using this file, the application will not be able to find any views and it will probably show the error message 404. The same goes to the main Django application. You must include the paths to the polls application on the urls.py file in the main application, otherwise you will not be able to access those pages when your server is running.

Another important step you must follow in your application is connecting it to a database. In this project, I used a MySQL database in my localhost to store questions as well as the users' choices for each question. To connect your application to a MySQL database you need to connect to an existent schema. You must then specify which engine you are using, the name of the database, the user, the password, host, and port that will be connected. As this project is not a production level application, it is fine to use a database in the localhost and to leave its password visible. However, if this application was to be built in the future,for security purposes, I would have to connect it to a hosted database and make sure no one can see the password.

Once the credential were added to the settings.py in the main application, the command lines 'python manage.py makemigrations' and 'python manage.py migrate' were entered to connect to the database to the main application. One important point that was not mentioned previously is: How are the questions and choices created? The answer is quite straightforward. By creating two new models (Questions & Models) in the models.py file within the polls application. This models can be seen by accessing 127.0.0.1/admin, where you can create or delete questions and choices for normal users. If you delete any questions on this page, it will also disappear from the database. 

After doing another 'py manage.py migrate', you would be able to see these two tables in the database, "Questions" and "Choices". These are the main steps taken to create a polls application using Django framework. As you can see in the files structure of this project, I was trying to deploy this app in production level by using Vercel platform, but I have now to connect this application to a hosted database. I hope to achieve it in the next couple weeks.

### CA2 - Accounts Application ###

For CA2, I used the same project as CA1 as base for this assignment. The objetive was to create another application which would run simultaneously with other applications within the same Django project.

By using the command line 'python manage.py startapp 'accounts'', a new application was created within django project. Once that was done, it was time to create the views for this app. In this case, we need to create a template folder and then create another folder called registration inside it. There I created HTML files for every single step of signing up a new user to the login screen.
This user would then be returned to the index.html. It is important to mention that the users credentials are not being transferred to the database as it is confidential data.

Another thing that we must ensure to add to the main application is the app path 'accounts'. Bellow you can see how the settings.py file looks like after creating the accounts app.

INSTALLED_APPS = [
    'polls.apps.PollsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts', // App installed.
]

Make sure to have these two url paths included in your main project urls.py file:

  path("accounts/", include("accounts.urls")),
  path("accounts/", include("django.contrib.auth.urls")),
  
After this step, whenever a new user is created, his data is stored in the local host. You would be able to switch from one account to another account with no problems. What is interesting about this app is that now I can implement a condition on the polls application created for CA1. By limiting the number of votes per user in each question, the application would be able to count votes more accurately.
