from flask import Flask, render_template, redirect, url_for, flash

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import openai
import os
import json


openai.api_key = "nuh uh"



class InputForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

@app.route('/')
def home():
    return render_template('index.html',)

@app.route('/explore', methods=['GET', 'POST'])
def explore():
    form = InputForm()
    inputCountry = ""
    if form.validate_on_submit():
        inputCountry = form.name.data
        flash(openAItest(inputCountry))
        try:
            statDict = openAIemojis(inputCountry)
        except:
            statDict = {"favorite_food": "None",
                    "rating": "None",
                    "main_language": "None",
                    "activities": "None"
                    }
            #flash("Error genreating fun facts.")
        try:
            flash("Food: " + statDict["favorite_food"])
        except KeyError:
            flash("Error generating favorite food.")
        try:
            flash("Rating: " + statDict["rating"])
        except KeyError:
            flash("Error generating rating.")
        try:
            flash("Language: " + statDict["main_language"])
        except KeyError:
            flash("Error generating language statistic.")
        try:
            flash("Activities: " + statDict["activities"])
        except KeyError:
            flash("Error generating activities.")

        return render_template('explore.html', form=form, )

    return render_template('explore.html', form=form,)
@app.route('/about')
def about():
    return render_template('about.html')

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
    data = json.loads(rsp.lower())
    return data


if __name__ == '__main__':
    app.run(debug=True)
