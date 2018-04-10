from flask import Flask, request, redirect
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    template = jinja_env.get_template('index.html')
    return template.render()

@app.route("/", methods=['POST'])
def verify():
    template_success = jinja_env.get_template('welcome.html')
    template_fail = jinja_env.get_template('index.html')
    username = request.form['username']
    password1 = request.form['password1']
    password2 = request.form['password2']
    email = request.form['email']

    user_message = ''
    password1_message = ''
    password2_message = ''
    email_message = ''

##input validation section

    ##checking item 1
    if username == '':
        user_message = "Please enter a username"
    if password1 == '':
        password1_message = "Please enter a password here"
    if password2 == '':
        password2_message = "Please re-enter the password here"

    ##checking item 2 - username
    if (len(username) > 20) or (len(username) < 3):
        user_message = "Please enter a username more than 3 characters long and less than 20, not containing a space"
    else:
        for i in username:
            if i == ' ':
                user_message = "Please no spaces in usernames"

    ##checking item 2 - password
    if (len(password1) > 20) or (len(password1) < 3):
        password1_message = "Please enter a valid password, between 3 and 20 characters long and no spaces."
    else:
        for i in password1:
            if i == ' ':
                password1_message = "Please enter a valid password, between 3 and 20 characters long and no spaces."


    ##checking item 3
    if password1 != password2:
        password2_message = "Passwords do not match! Please enter matching passwords!"
    
    ##checking item 4
    if email != '':
        if (len(email) > 20) or (len(email) < 3):
            email_message = "Email must be between 3 and 20 characters long"
        else:
            at_counter = 0
            space_counter = 0
            period_counter = 0

            for i in email:
                if i == '@':
                    at_counter = at_counter + 1
            
            for i in email:
                if i == ' ':
                    space_counter = space_counter + 1

            for i in email:
                if i == '.':
                    period_counter = period_counter + 1
            
            if (at_counter != 1):
                email_message = "Email address must have ONE and only ONE @ symbol"
            elif (space_counter != 0):
                email_message = "Email address cannot have any spaces"
            elif (period_counter != 1 ):
                email_message = "Email address must have one period"

    ##check what form to send
    if (user_message == '') and (password1_message == '') and (password2_message == '') and (email_message == ''):
        return template_success.render(user = username)
    else:
        return template_fail.render(username=username, username_error = user_message, password1_error = password1_message, password2_error = password2_message, email = email, email_error = email_message )

app.run()