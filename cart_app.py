from flask import Flask, render_template, request
import random
import string
import boto3
import pymysql

# Connect to the database
conn = pymysql.connect(
    host='database-hostname',
    user='database-username',
    password='database-password',
    database='database-name'
)

# Create a Flask app
app = Flask(__name__)

# Create an SNS client
sns = boto3.client('sns')

# Define the home page route
@app.route('/')
def home():
    return render_template('home.html')

# Define the route for registering the user and generating and sending the random string
@app.route('/register', methods=['POST'])
def register():
    # Get the user's full name, email, and phone number from the form
    full_name = request.form['full_name']
    email = request.form['email']
    phone_number = request.form['phone_number']

    # Register the user in the database
    with conn.cursor() as cur:
        cur.execute('INSERT INTO users (full_name, email, phone_number) VALUES (%s, %s, %s)', (full_name, email, phone_number))
        conn.commit()

    # Generate a random string
    length = 10
    include_numbers = True
    include_symbols = True
    letters = string.ascii_letters
    if include_numbers:
        letters += string.digits
    if include_symbols:
        letters += string.punctuation
    random_string = ''.join(random.choice(letters) for i in range(length))

    # Register the random string in the database
    with conn.cursor() as cur:
        cur.execute('INSERT INTO random_strings (string) VALUES (%s)', (random_string,))
        conn.commit()

    # Send the random string to the user's phone number using SNS
    sns.publish(
        PhoneNumber=phone_number,
        Message=f'Your random string is: {random_string}'
    )

    return render_template('verify.html')

# Define the route for verifying the random string
@app.route('/verify', methods=['POST'])
def verify():
    # Get the user's random string and phone number from the form
    random_string = request.form['random_string']
    phone_number = request.form['phone_number']

    # Check if the random string matches the one in the database
    with conn.cursor() as cur:
        cur.execute('SELECT string FROM random_strings ORDER BY id DESC LIMIT 1')
        result = cur.fetchone()
        if result is None:
            return render_template('fail.html')
        elif result[0] == random_string:
            return render_template('success.html')
        else:
            return render_template('fail.html')

# Start the app
if __name__ == '__main__':
    app.run()
