import os
from flask import Blueprint, render_template
from flask_mail import Message
from extensions import db, mail
from models import ServiceRequest
from forms import ServiceRequestForm

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def home():
    return render_template('public/index.html')

@public_bp.route('/about')
def about():
    return render_template('public/about.html')

@public_bp.route('/submit', methods=['GET', 'POST'])
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

                Your ticket number is {ticket_number}. Please keep this email and reference your ticket number when communicating with WhizTech.

                A support specialist is reviewing your request and will reach out shortly.

                Most sincerely,
                The WhizTech Team
                """
            
            msg_customer = Message(subject_customer, recipients=[form.customer_email.data])
            msg_customer.body = body_customer
            mail.send(msg_customer)
            print("DEBUG: Customer confirmation email sent")

            return render_template('public/submit_success.html', name_in_html=full_name, ticket_id=ticket_number, email_in_html=form.customer_email.data)

        except Exception as e:
            print(f"CRITICAL ERROR: {e}")
            db.session.rollback()
            return "Internal error.", 500

    return render_template('public/submit.html', form=form)