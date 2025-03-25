from flask import Flask, request, jsonify, render_template
import random
import smtplib
from email.message import EmailMessage
from flask import redirect, url_for
import mysql.connector



app = Flask(__name__)

# Global variable to store OTPs
otp_storage = {}



@app.route('/')
def index():
    return render_template('index.html')  # This serves index.html

@app.route('/login')
def login():
    return render_template('login.html') 

    

@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({"success": False, "message": "Email is required."})

    # Generate a 6-digit OTP
    otp = "".join([str(random.randint(0, 9)) for _ in range(6)])

    try:
        # Send OTP via email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        from_mail = 'mithraa1906@gmail.com'
        app_password = 'tikp eqax pxmo arcw'  # Use an app-specific password
        server.login(from_mail, app_password)

        msg = EmailMessage()
        msg['Subject'] = "OTP Verification"
        msg['From'] = from_mail
        msg['To'] = email
        msg.set_content(f"Your OTP is: {otp}")

        server.send_message(msg)
        server.quit()

        # Store OTP in memory (for demo purposes only, not recommended for production)
        otp_storage[email] = otp

        return jsonify({"success": True, "message": "OTP sent successfully."})
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to send OTP: {str(e)}"})

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get('email')
    input_otp = data.get('otp')

    if not email or not input_otp:
        return jsonify({"success": False, "message": "Email and OTP are required."})

    # Verify OTP
    if email in otp_storage and otp_storage[email] == input_otp:
        del otp_storage[email]  # Remove OTP after successful verification
        return jsonify({"success": True, "message": "OTP verified successfully."})
    else:
        return jsonify({"success": False, "message": "Invalid OTP."})

@app.route('/main')
def main():
    return render_template('main.html')
@app.route('/view')
def view_details():
    return render_template('view.html')
@app.route('/review')
def review():
    restaurant_name = request.args.get('name')  # Get the 'name' query parameter
    return render_template('review.html', name=restaurant_name)
@app.route('/add')
def add():
    return render_template('add.html')
@app.route('/custreview/<restaurant>', methods=['GET', 'POST'])
def submit_review(restaurant):
    if request.method == 'POST':
        reviewer = request.form['reviewer']
        email = request.form['email']
        date = request.form['date']
        rating = request.form['rating']
        review = request.form['review']
        
        # Placeholder database connection function
        # Replace this with your actual database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reviews (restaurant, reviewer, email, date, rating, review) VALUES (%s, %s, %s, %s, %s, %s)",
            (restaurant, reviewer, email, date, rating, review)
        )
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('thank_you'))  # Redirect to thank you page

    return render_template('custreview.html', restaurant=restaurant)

@app.route('/thank-you')
def thank_you():
    return "Thank you for submitting your review!"

@app.template_filter('replace_and_capitalize')
def replace_and_capitalize(value):
    return value.replace('-', ' ').capitalize()
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='mithraa@2325',
        database='restaurant_reviews'
    )


# Placeholder for database connection function

# Endpoint to fetch reviews for a specific restaurant
@app.route('/get_reviews', methods=['GET'])
def get_reviews():
    restaurant_name = request.args.get('name')

    if not restaurant_name:
        return jsonify({"error": "Restaurant name is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM reviews WHERE restaurant_name = %s', (restaurant_name,))
    reviews = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(reviews)
if __name__ == '__main__':
    app.run(debug=True)
