import os
from flask import Flask, render_template, request
from flask_mail import Mail, Message
from dotenv import load_dotenv

from extensions import db
from models import ServiceRequest
from forms import ServiceRequestForm

load_dotenv()

app = Flask(__name__)

#--DB CONFIG
db_url = os.getemv('DATABASE_URL', 'sqlite:///whiztech.db')

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#--MAIL CONFIG
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER_BR')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT_BR'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS_BR') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL_BR') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME_BR')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_SMTP_KEY_BR')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_SENDER_G')
app.config['SECRET_KEY'] = os.getenv('P_KEY')

#--PLUGINS
mail = Mail(app)
db.init_app(app)

@app.route('/')
def home():
    form = ServiceRequestForm()
    return render_template('submit.html', form=form)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = ServiceRequestForm()

    if form.validate_on_submit():

        full_name = form.customer_fname.data + " "  + form.customer_lname.data

        new_ticket = ServiceRequest(
            customer_lname=form.customer_lname.data,
            customer_fname=form.customer_fname.data,
            customer_email=form.customer_email.data,
            service_type=form.service_type.data,
            details=form.details.data
        )

        try:
            db.session.add(new_ticket)
            db.session.commit()

            ticket_number = new_ticket.id
            print(f"DEBUG: Saved Ticket #{ticket_number}")

            #---ADMIN EMAIL
            subject_admin = f"New Service Request From {full_name} [{ticket_number}]"
            body_admin = f"""
                ----------NEW SERVICE REQEST----------
                TICKET: {ticket_number}
                CUSTOMER: {full_name}
                EMAIL: {form.customer_email.data}
                SERVICE: {form.service_type.data}
                DETAILS: {form.details.data}
                --------------------------------------
                """
            
            msg_admin = Message(subject_admin, recipients=[os.getenv('MAIL_USERNAME_G')])
            msg_admin.reply_to = form.customer_email.data
            msg_admin.body = body_admin
            mail.send(msg_admin)
            print("DEBUG: Admin notification email sent")

            #---CUSTOMER EMAIL
            subject_customer = f"We have recieved your Service Request [Ticket #{ticket_number}]"
            body_customer = f"""
                Hi {form.customer_fname.data},

                Thank you for choosing WhizTech! We have received your service request.

                Your ticket number is {ticket_number}. Please keept this email and reference your ticket number when contacting WhizTech.

                A support specialist is reviewing your request and will reach out shortly.

                Most sincerely,
                The WhizTech Team
                """
            
            msg_customer = Message(subject_customer, recipients=[form.customer_email.data])
            msg_customer.body = body_customer
            mail.send(msg_customer)
            print("DEBUG: Customer confirmation email sent")

            return render_template('submit_success.html', name_in_html=full_name, ticket_id=ticket_number, email_in_html=form.customer_email.data)

        except Exception as e:
            print(f"CRITICAL ERROR: {e}")
            db.session.rollback()
            return "Internal error.", 500
    
    if form.errors:
        return f"Form Errors: {form.errors}", 400
    
    return "Please submit the form from correct page.", 200
    
if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False') == 'True'
    app.run(debug=debug_mode)