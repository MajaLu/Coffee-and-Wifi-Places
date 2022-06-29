from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location', validators=[DataRequired('Please enter a valid input for URL!'), URL()])
    opening_time = StringField('Opening Time e.g. 8AM', validators=[DataRequired('Please enter a valid input for the opening time of the cafe!')])
    closing_time = StringField('Closing Time e.g. 5:30PM', validators=[DataRequired('Please enter a valid input for the closing time of the cafe!')])
    coffee_rating = SelectField('Coffee Rating', validators=[DataRequired('Please select a valid rating!')], choices=[('☕☕☕☕☕', '☕☕☕☕☕'), ('☕☕☕☕', '☕☕☕☕'), ('☕☕☕', '☕☕☕'), ('☕☕', '☕☕'), ('☕', '☕')])
    wifi_rating = SelectField('Wifi Strength Rating', validators=[DataRequired('Please select a valid rating!')], choices=[('💪💪💪💪💪', '💪💪💪💪💪'), ('💪💪💪💪', '💪💪💪💪'), ('💪💪💪', '💪💪💪'), ('💪💪', '💪💪'),
                                       ('💪', '💪'), ('✘', '✘')])
    power_rating = SelectField('Power Socket Availability', validators=[DataRequired('Please select a valid rating!')], choices=[('🔌🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'), ('🔌🔌🔌🔌', '🔌🔌🔌🔌'), ('🔌🔌🔌', '🔌🔌🔌'), ('🔌🔌', '🔌🔌'),
                                               ('🔌', '🔌'), ('✘', '✘')])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', encoding='utf-8', mode='a') as csv_file:
            csv_file.write(f"\n{form.cafe.data},"
                           f"{form.location.data},"
                           f"{form.opening_time.data},"
                           f"{form.closing_time.data},"
                           f"{form.coffee_rating.data},"
                           f"{form.wifi_rating.data},"
                           f"{form.power_rating.data}")
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()



@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        list_of_rows_without_heading = [i for i in list_of_rows[1:]]
        print(list_of_rows_without_heading)
    return render_template('cafes.html', cafes=list_of_rows, cafes_x=list_of_rows_without_heading)



if __name__ == '__main__':
    app.run(debug=True)
