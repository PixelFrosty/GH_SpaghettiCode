from flask import Flask, render_template, redirect, url_for, flash

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import openai
import os


openai.api_key = os.getenv("OPENAI_API_KEY")  # If using an environment variable



class InputForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

@app.route('/', methods=['GET', 'POST'])
def home():
    form = InputForm()
    if form.validate_on_submit():
        inputCountry = form.name.data
        flash(openAItest(inputCountry))
        return redirect(url_for('home'))
    return render_template('base.html', form=form)

@app.route('/flights', methods=['GET', 'POST'])
def flights():
    flightForm = InputForm()
    if flightForm.validate_on_submit():
        flight = flightForm.name.data
        return redirect(f"https://www.google.com/search?q={"flights to " + flight}")
    return render_template('flights.html', form= flightForm)


def openAItest(data):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or another model
        messages=[{"role": "user", "content":
            "In 200 tokens or fewer, Why should I travel to" + data}], temperature=0,
        max_tokens=200
    )
    return response.choices[0].message['content']


if __name__ == '__main__':
    app.run(debug=True)
