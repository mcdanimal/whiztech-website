from flask import Flask, render_template, request

app = Flask(__name__)

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

    #*************JUST FOR DEV TEST - SEND TO DB AND EMAIL LATER***************
    print("--------NEW SERVICE REQUEST--------")
    print(f"NAME: {full_name}")
    print(f"EMAIL: {customer_email}")
    print(f"SERVICE: {service_type}")
    print(f"DETAILS: {details}")
    print("----------------END----------------")

    return render_template('submit_success.html', name_in_html=full_name)

if __name__ == '__main__':
    app.run(debug=True)