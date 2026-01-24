import os
from flask import Flask, render_template, request
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER_BR')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT_BR'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS_BR') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL_BR') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME_BR')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_SMTP_KEY_BR')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_SENDER_G')


mail = Mail(app)

@app.route('/')
def home():
    return render_template('submit.html')

@app.route('/submit', methods=['POST'])
def submit():
    customer_fname = request.form.get('customer_fname')
    customer_lname = request.form.get('customer_lname')
    customer_email = request.form.get('customer_email')
    service_type = request.form.get('service_type')
    details = request.form.get('details')

    full_name = customer_fname + " " + customer_lname

    subject = f"New Service Request from {full_name}"
    body = f"""
    You have receieved a new request!"

    Customer: {full_name}
    Email: {customer_email}
    Service Type: {service_type}

    Details:
    {details}
    """

    msg = Message(subject, recipients=[os.getenv("MAIL_SENDER_G")])
    msg.body = body

    try:
        mail.send(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

    return render_template('submit_success.html', name_in_html=full_name)

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False') == 'True'
    app.run(debug=debug_mode)