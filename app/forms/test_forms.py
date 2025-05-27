from flask import Flask, render_template_string
from template_temp.app.forms.login_form import LoginForm, RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'testsecret'

login_template = """
<form method="POST">
  {{ form.hidden_tag() }}
  {{ form.email.label }}<br>
  {{ form.email(size=32) }}<br>
  {% for error in form.email.errors %}
    <span style="color:red;">{{ error }}</span><br>
  {% endfor %}

  {{ form.password.label }}<br>
  {{ form.password(size=32) }}<br>
  {% for error in form.password.errors %}
    <span style="color:red;">{{ error }}</span><br>
  {% endfor %}

  {{ form.remember_me() }} {{ form.remember_me.label }}<br>
  {{ form.submit() }}
</form>
"""

registration_template = """
<form method="POST">
  {{ form.hidden_tag() }}
  {{ form.email.label }}<br>
  {{ form.email(size=32) }}<br>
  {% for error in form.email.errors %}
    <span style="color:red;">{{ error }}</span><br>
  {% endfor %}

  {{ form.password.label }}<br>
  {{ form.password(size=32) }}<br>
  {% for error in form.password.errors %}
    <span style="color:red;">{{ error }}</span><br>
  {% endfor %}

  {{ form.confirm_password.label }}<br>
  {{ form.confirm_password(size=32) }}<br>
  {% for error in form.confirm_password.errors %}
    <span style="color:red;">{{ error }}</span><br>
  {% endfor %}

  {{ form.terms_accepted() }} {{ form.terms_accepted.label }}<br>
  {% for error in form.terms_accepted.errors %}
    <span style="color:red;">{{ error }}</span><br>
  {% endfor %}

  {{ form.submit() }}
</form>
"""

@app.route('/test-login', methods=['GET', 'POST'])
def test_login():
    form = LoginForm()
    if form.validate_on_submit():
        return f"Login successful! Email: {form.email.data}"
    return render_template_string(login_template, form=form)

@app.route('/test-register', methods=['GET', 'POST'])
def test_register():
    form = RegistrationForm()
    if form.validate_on_submit():
        return f"Registration successful! Email: {form.email.data}"
    return render_template_string(registration_template, form=form)

if __name__ == "__main__":
    app.run(debug=True)
