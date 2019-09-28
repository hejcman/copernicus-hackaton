#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Main Part of app.

Contains the renderes, and calls functions in /senders and /forms.
Currently contains the module SSLify, which automatically redirects traffic to
an SSL encrypted version of the side (works only when app.debug=False)
"""

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request

from forms import form_address
from forms import form_advanced

from senders import sender_email

from flask_sslify import SSLify

from flask_googlemaps import *

import datetime

# import webbrowser
import lib
import pygal
from pygal.style import DarkSolarizedStyle
from flask_wtf import Form
from flask_bootstrap import Bootstrap

from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map


app = Flask(__name__)
Bootstrap(app)
GoogleMaps(app, key="8JZ7i18MjFuM35dJHq70n3Hx4")
sslify = SSLify(app)
app.secret_key = '3zIGue1wpJtrFKs0m5Yn'
# webbrowser.open_new_tab("http://127.0.0.1:5000")


@app.route('/')
def index():
    """Render of the main home page."""
    return render_template('home.html')


@app.route('/about')
def about():
    """Render of the about page."""
    return render_template('about.html')

# @app.route('/forms/address_form', methods=['GET', 'POST'])
# def user_form_renderer():
#     address_form = form_address.AddressForm(request.form)
#     if request.method == 'POST' and address_form.validate():
#         print(address_form.address)
#         values = lib.get_avg_cloud_cover(lib.get_bounding_box(), verbose=False)
#         print(values)
#         labels = ["0%", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]
#         return render_template('result.html', values=values, labels=labels)
#     return render_template('/forms/address_form.html', form=address_form)


@app.route('/forms/address_form', methods=['GET', 'POST'])
def user_form_renderer():

    address_form = form_address.AddressForm(request.form)

    if request.method == 'POST' and address_form.validate():

        print(address_form.size.data)
        print(address_form.yearly_usage.data)
        print(address_form.yearly_spending.data)

        # create a bar chart
        bar_chart = pygal.Bar(width=960,
                              height=400,
                              explicit_size=True,
                              title="# of cloudy days per year",
                              style=DarkSolarizedStyle)

        bar_chart.x_labels = ["0%", "10%", "20%", "30%",
                              "40%", "50%", "60%", "70%", "80%", "90%", "100%"]

        bar_chart.add("Clouds", lib.get_avg_cloud_cover(
            lib.get_bounding_box(
                lib.get_coords(
                    address_form.address.data),
                address_form.size.data
            ),
            verbose=False))

        bar_chart.show_legend = False

        mymap = Map(
            identifier="view-side",
            lat=37.4419,
            lng=-122.1419,
            markers=[(37.4419, -122.1419)]
        )

        return render_template('result.html', title="TITLE", bar_chart=bar_chart, mymap=mymap)

    return render_template('/forms/address_form.html', form=address_form)



@app.route('/forms/advanced_form', methods=['GET', 'POST'])
def advanced_form_renderer():

    advanced_form = form_advanced.AdvancedForm(request.form)

    if request.method == 'POST' and advanced_form.validate():

        print(advanced_form.size.data)
        print(advanced_form.yearly_usage.data)
        print(advanced_form.yearly_spending.data)
        print(advanced_form.roof_50.data)
        print(advanced_form.roof_65.data)
        print(advanced_form.roof_70.data)
        print(advanced_form.roof_75.data)
        print(advanced_form.roof_90.data)
        print(advanced_form.roof_95.data)
        print(advanced_form.roof_100.data)

        lib.print_address(lib.get_coords(advanced_form.address.data))

        # create a bar chart
        bar_chart = pygal.Bar(width=960,
                              height=400,
                              explicit_size=True,
                              title="# of cloudy days per year",
                              style=DarkSolarizedStyle)

        bar_chart.x_labels = ["0%", "10%", "20%", "30%",
                              "40%", "50%", "60%", "70%", "80%", "90%", "100%"]

        bar_chart.add("Clouds", lib.get_avg_cloud_cover(
            lib.get_bounding_box(
                lib.get_coords(
                    advanced_form.address.data),
                advanced_form.size.data
            ),
            verbose=False))

        bar_chart.show_legend = False

        mymap = Map(
            identifier="view-side",
            lat=37.4419,
            lng=-122.1419,
            markers=[(37.4419, -122.1419)]
        )

        return render_template('result.html', title="TITLE", sun_days=lib.get_sun_time(datetime.datetime('2018-09-28')) , bar_chart=bar_chart, mymap=mymap)

    return render_template('/forms/advanced_form.html', form=advanced_form)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, threaded=True, debug=True)
