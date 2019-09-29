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

import math

import numpy as np

# import webbrowser
import lib
import pygal
from pygal.style import DarkSolarizedStyle
from flask_wtf import Form
from flask_bootstrap import Bootstrap

from dateutil.relativedelta import relativedelta
import datetime



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

@app.route('/forms/address_form', methods=['GET', 'POST'])
def user_form_renderer():

    address_form = form_address.AddressForm(request.form)

    if request.method == 'POST' and address_form.validate():

        all_days = lib.get_sunlight_data(
            lib.get_bounding_box(
                lib.get_coords(address_form.address.data)
            ),
            lib.get_coords(address_form.address.data),
            start_time='2018-09-29',
            end_time='2019-09-29'
        )

        total_sun_time = 0

        for data in range(0, len(all_days)):
            total_sun_time += float(all_days[data][5])

        usage = int(address_form.yearly_usage.data)
        usage /= 365
        usage_per_hour = usage/24

        area = usage_per_hour/250
        area *= 10000

        # create a bar chart
        bar_chart = pygal.Bar(width=960,
                              height=400,
                              explicit_size=True,
                              title="# of cloudy days per year",
                              style=DarkSolarizedStyle)

        bar_chart.x_labels = ["0%", "10%", "20%", "30%",
                              "40%", "50%", "60%", "70%", "80%", "90%", "100%"]

        now = datetime.datetime.now()

        bar_chart.add("Clouds", lib.get_avg_cloud_cover(
            lib.get_bounding_box(
                lib.get_coords(
                    address_form.address.data),
                address_form.size.data
            ),
            verbose=False,
            start_time=now-relativedelta(years=3),
            end_time=now))

        bar_chart.show_legend = False


        return render_template('result.html', 
                               heading_text="You would need: %s m2" % (area),
                               bar_chart=bar_chart,
                               bar_chart2=bar_chart)

    return render_template('/forms/address_form.html', form=address_form)


@app.route('/forms/advanced_form', methods=['GET', 'POST'])
def advanced_form_renderer():

    advanced_form = form_advanced.AdvancedForm(request.form)

    if request.method == 'POST' and advanced_form.validate():

        lib.print_address(lib.get_coords(advanced_form.address.data))

        # create a bar chart
        bar_chart = pygal.Bar(width=960,
                              height=400,
                              explicit_size=True,
                              title="# of cloudy days per year: %s" %(advanced_form.address.data),
                              style=DarkSolarizedStyle)

        # create a bar chart
        bar_chart2 = pygal.Bar(width=960,
                              height=400,
                              explicit_size=True,
                              title="# of cloudy days per year: Sahara",
                              style=DarkSolarizedStyle)

        all_days = lib.get_sunlight_data(
            lib.get_bounding_box(
                lib.get_coords(advanced_form.address.data)
            ),
            lib.get_coords(advanced_form.address.data),
            start_time=advanced_form.start_point.data,
            end_time=advanced_form.end_point.data
        )

        total_output = 0

        for data in range(0, len(all_days)):
            total_output += 1*int(advanced_form.roof_100.data)*int(all_days[data][7])
            total_output += 0.9*int(advanced_form.roof_90.data)*int(all_days[data][7])
            total_output += 0.75*int(advanced_form.roof_75.data)*int(all_days[data][7])

        total_output /= 1000

        print(total_output)

        bar_chart.x_labels = ["0%", "10%", "20%", "30%",
                              "40%", "50%", "60%", "70%", "80%", "90%", "100%"]
        bar_chart2.x_labels = ["0%", "10%", "20%", "30%",
                              "40%", "50%", "60%", "70%", "80%", "90%", "100%"]

        st = advanced_form.start_point.data
        et = advanced_form.end_point.data

        bar_chart.add("-3 years", lib.get_avg_cloud_cover(
            lib.get_bounding_box(
                lib.get_coords(
                    advanced_form.address.data
                ),
                advanced_form.size.data
            ),
            start_time=st-datetime.timedelta(days=3*365),
            end_time=et-datetime.timedelta(days=3*365),
            verbose=False
        ))

        bar_chart.add("-2 years", lib.get_avg_cloud_cover(
            lib.get_bounding_box(
                lib.get_coords(
                    advanced_form.address.data
                ),
                advanced_form.size.data
            ),
            start_time=st-datetime.timedelta(days=2*365),
            end_time=et-datetime.timedelta(days=2*365),
            verbose=False
        ))

        bar_chart.add("-1 year", lib.get_avg_cloud_cover(
            lib.get_bounding_box(
                lib.get_coords(
                    advanced_form.address.data
                ),
                advanced_form.size.data
            ),
            start_time=st-datetime.timedelta(days=365),
            end_time=et-datetime.timedelta(days=365),
            verbose=False
        ))

        bar_chart.add("this year", lib.get_avg_cloud_cover(
            lib.get_bounding_box(
                lib.get_coords(
                    advanced_form.address.data),
                advanced_form.size.data
            ),
            start_time=advanced_form.start_point.data,
            end_time=advanced_form.end_point.data,
            verbose=False))

        bar_chart2.add("2019", lib.get_avg_cloud_cover(
            lib.get_bounding_box([8.5, 24.1]),
            start_time=advanced_form.start_point.data,
            end_time=advanced_form.end_point.data,
            verbose=False))

        return render_template('result.html',
                               heading_text="Production capacity: %s kWh" % math.ceil(total_output),
                               title="TITLE",
                               bar_chart=bar_chart,
                               bar_chart2=bar_chart2)

    return render_template('/forms/advanced_form.html', form=advanced_form)


def calculate_savings():
    # TODO:
    pass


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, threaded=True, debug=True)
