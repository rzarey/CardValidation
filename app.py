from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

def validate_email(email):
    pattern = r"^([a-zA-Z0-9_\.-]+)@([a-z0-9_\.-]+)\.([a-z\.]{2,6})$"
    return bool(re.match(pattern, email))

def validate_name(name):
    pattern = r"^([a-zA-Z\s]+)$"
    return bool(re.match(pattern, name))

def validate_credit_card_number(card_number):
    pattern = r"^([0-9]{16})$"
    return bool(re.match(pattern, card_number))

def validate_expiry_date(expiry_date):
    pattern = r"^([0-9]{2})[\/\-]([0-9]{2})$"
    if re.match(pattern, expiry_date):
        month, year = map(int, re.split(r"[\/\-]", expiry_date))
        return 1 <= month <= 12
    return False

def validate_cvv(cvv):
    pattern = r"^([0-9]{3,4})$"
    return bool(re.match(pattern, cvv))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        card_number = request.form.get("card_number")
        expiry_date = request.form.get("expiry_date")
        cvv = request.form.get("cvv")

        email_valid = validate_email(email)
        name_valid = validate_name(name)
        card_valid = validate_credit_card_number(card_number)
        expiry_valid = validate_expiry_date(expiry_date)
        cvv_valid = validate_cvv(cvv)

        return render_template(
            "index.html",
            email=email,
            name=name,
            card_number=card_number,
            expiry_date=expiry_date,
            cvv=cvv,
            email_valid=email_valid,
            name_valid=name_valid,
            card_valid=card_valid,
            expiry_valid=expiry_valid,
            cvv_valid=cvv_valid,
            submitted=True
        )
    return render_template("index.html", submitted=False)


@app.route("/validate", methods=["POST"])
def validate():
  field = request.form.get("field")
  value = request.form.get("value")
  
  if field == "email":
    is_valid = validate_email(value)
  elif field == "name":
    is_valid = validate_name(value)
  elif field == "card_number":
      is_valid = validate_credit_card_number(value)
  elif field == "expiry_date":
      is_valid = validate_expiry_date(value)
  elif field == "cvv":
      is_valid = validate_cvv(value)
  else:
      is_valid = False

  return jsonify({"is_valid": is_valid})


if __name__ == "__main__":
    app.run(debug=True)