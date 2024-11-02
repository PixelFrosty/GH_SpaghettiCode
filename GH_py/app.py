from flask import Flask, render_template, redirect, url_for, flash

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import openai
import os
import json


openai.api_key = os.getenv("OPENAI_API_KEY")  # If using an environment variable



class InputForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

@app.route('/', methods=['GET', 'POST'])
def home():
    form = InputForm()
    inputCountry = ""
    if form.validate_on_submit():
        inputCountry = form.name.data
        flash(openAItest(inputCountry))
        statDict = openAIemojis(inputCountry)
        flash("Food: " + statDict["favorite_food"])
        flash("Rating: " + statDict["rating"])
        flash("Language: " + statDict["main_language"])
        flash("Activities: " + statDict["activities"])
        return render_template('index.html', form=form, food=statDict["favorite_food"],
                               rating=statDict["rating"],
                               lang=statDict["main_language"],
                               activites=statDict["activities"])

    return render_template('index.html', form=form,)

@app.route('/flights', methods=['GET', 'POST'])
def flights():
    flightForm = InputForm()
    if flightForm.validate_on_submit():
        flight = flightForm.name.data
        return redirect(f"https://www.google.com/search?q={"flights to " + flight}")
    return render_template('flights.html', form=flightForm)


def openAItest(data):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or another model
        messages=[{"role": "user", "content":
            "In 200 tokens or fewer, Why should I travel to" + data}], temperature=0,
        max_tokens=200
    )
    return response.choices[0].message['content']


def openAIJSON(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or another model
        messages=[{"role": "user", "content":
            prompt + "population statistics in the JSON format of city: population, and use single quotes only"}], temperature=0,
        max_tokens=200
    )
    return response.choices[0].message['content']

def openAIemojis(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or another model
        messages=[{"role": "user", "content":
            "Put the following in a JSON format. For the country/location of " + prompt + "respond with its \'favorite_food\' (followed by an emoji), "
                                            "its \'main_language\' (followed by a flag emoji), "
                                            "\'rating\'(followed by 1 to 5 star emojis,"
                                            "and \'activites\'(followed by emojis)"}], temperature=0,
        max_tokens=200
    )
    rsp = response.choices[0].message['content']

    # Convert JSON string to dictionary
    data = json.loads(rsp.lower())

    # Print the dictionary
    #print(rsp)
    #print(data["favorite_food"])
    #expected values: [favorite food], ["main_language"] ["rating"] ["activities"]
    return data


if __name__ == '__main__':
    app.run(debug=True)
