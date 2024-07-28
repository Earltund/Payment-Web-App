#from flask import Flask, render_template, request, redirect, url_for, flash
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pandas as pd
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key in production

def paid_amount():
    detail= pd.read_csv("transaction_details.csv")
    value_loc=0

    for i in range(1, len(detail)):
        if (i == len(detail)-1):
            value_loc = detail.loc[i, "Amount Paid"]
            return value_loc

def increment_cnt():
    detail = pd.read_csv("transaction_details.csv")
    cnt=0
    for i in range(1, len(detail)+1):
        if (i == len(detail) - 1):
            status = detail.loc[i, "Status"]
            if(status=="success"):
                cnt+=1
            elif(status=='failure'):
                cnt=cnt
            else:
                cnt=cnt
            return cnt

class StudentPaymentSystem:
    def __init__(self):
        self.student_id = None
        self.student_email = None
        self.school_fees = 890000.00
        self.payment_confirmed = False
        self.email_received=False
        self.outstanding_amount=self.school_fees
        self.cnt= 0


    def select_payment_amount(self, amount):
        self.cnt=increment_cnt()
        if (self.cnt >= 1):
            self.email_received = True

        #self.selected_amount = 890000
        if(self.email_received==True):
            self.payment_confirmed= True
            #self.outstanding_amount = self.school_fees - paid_amount()
        else:
            self.payment_confirmed= False


        if(self.payment_confirmed == False):
            self.paid_amount=0
        else:
            self.paid_amount = paid_amount()


        if (self.paid_amount!=0):
            self.outstanding_amount= self.outstanding_amount - self.paid_amount




    def check_fee_breakdown(self):
        # Simulated fee breakdown
        fee_breakdown = {
            'Academic fees': self.school_fees * 0.35,
            'Accomodation and Convenience': self.school_fees * 0.2,
            'Bench Fees': self.school_fees * 0.15,
            'Other Fees': self.school_fees * 0.08,
            'Computer and Information Technology Acquisition Skills': self.school_fees * 0.12,
            'Graduation Fee': self.school_fees * 0.1,
            'Total Fee': self.school_fees,
            'Outstanding Fee': self.outstanding_amount
        }
        return fee_breakdown

    def process_payment(self):
        # Simulated payment processing
        # In a real-world scenario, integrate with a payment gateway
        # and handle payment status accordingly.
        payment_status = 'success'  # Change this based on your integration
        # Alert the payment status using JavaScript
        alert_script = f'<script>alert("Payment {payment_status.capitalize()}");</script>'
        return payment_status + alert_script



student_payment_system = StudentPaymentSystem()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/select_payment_amount', methods=['POST'])
def select_payment_amount():
    #amount = float(request.form['amount'])
    amount = 890000
    student_payment_system.select_payment_amount(amount)
    return redirect(url_for('fee_breakdown'))

@app.route('/fee_breakdown')
def fee_breakdown():
    fee_breakdown = student_payment_system.check_fee_breakdown()
    return render_template('fee_breakdown.html', fee_breakdown=fee_breakdown)

@app.route('/make_payment')
def make_payment():
    return render_template('make_payment.html')

@app.route('/process_payment', methods=['POST'])
def process_payment():
    payment_status = student_payment_system.process_payment()

    if payment_status == 'success':
        student_payment_system.payment_confirmed = True
        flash('Payment successful. Receipt sent to your email.', 'success')
    else:
        flash('Payment failed. Please try again.', 'danger')

    return redirect(url_for('index'))

#comment



#comment

if __name__ == '__main__':
    app.run(debug=True)


# comment
