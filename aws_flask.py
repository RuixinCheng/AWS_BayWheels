import sys
sys.path.append("/home/ec2-user/.local/lib/python3.7/site-packages")

import pandas as pd
import numpy as np

import io
from io import BytesIO
import base64
from matplotlib import pyplot as plt
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main():
    ### First Plot
    # load data
    all_trips_data = pd.read_csv("start_2020_all_trip_cleaned.csv")
    top10_popular = all_trips_data[["start_station_name", "start_station_id"]]
    top10_popular = top10_popular.groupby(['start_station_name']).size().reset_index(name='count')
    top10_popular = top10_popular.sort_values('count',ascending = False).head(10)

    # set the figure size
    plt.rcParams["figure.figsize"] = [8.5, 5.5]
    plt.rcParams["figure.autolayout"] = True

    fig = Figure()
    ax = fig.subplots()
    # plot
    ax.barh(top10_popular['start_station_name'], top10_popular['count'], color='#c9bbe5')
    # Despine
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    # change the tick label font size
    ax.tick_params(axis='both', which='major', labelsize=8)
    # set x/ y label & title
    ax.set_title("Top 10 Popular Station", weight='bold', size=12)
    ax.set_xlabel("Count of User", labelpad=10, weight='bold', size=10)
    ax.set_ylabel("Station Name", labelpad=10, weight='bold', size=10)
    # invert value of y-axis
    ax.invert_yaxis()
    # display the value of each barh
    for i, v in enumerate(top10_popular['count']):
        ax.text(v + 4, i + .2, str(v), fontsize = 8)
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)

    ## Second Plot
    top10_unpopular = all_trips_data[["start_station_name", "start_station_id"]]
    top10_unpopular = top10_unpopular.groupby(['start_station_name']).size().reset_index(name='count')
    top10_unpopular = top10_unpopular.sort_values('count',ascending = False).tail(10)

    # set the figure size
    plt.rcParams["figure.figsize"] = [8.5, 5.5]
    plt.rcParams["figure.autolayout"] = True

    fig = Figure()
    ax = fig.subplots()
    # plot
    ax.barh(top10_unpopular['start_station_name'], top10_unpopular['count'], color='#d7e5bb')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    # change the tick label font size
    ax.tick_params(axis='both', which='major', labelsize=8)
    # set x/ y label & title
    ax.set_title("Top 10 Unpopular Station", weight='bold', size=12)
    ax.set_xlabel("Count of User", labelpad=10, weight='bold', size=10)
    ax.set_ylabel("Station Name", labelpad=10, weight='bold', size=10)
    # invert value of y-axis
    ax.invert_yaxis()
    # display the value of each barh
    for i, v in enumerate(top10_unpopular['count']):
        ax.text(v + .5, i + .1, str(v), fontsize = 8)
    # Save it to a temporary buffer.
    buf1 = BytesIO()
    fig.savefig(buf1, format="png")
    buf1.seek(0)
    # Embed the result in the html output.
    image1 = base64.b64encode(buf.getbuffer()).decode("ascii")
    image2 = base64.b64encode(buf1.getbuffer()).decode("ascii")
    return render_template('baywheel.html', image1 = image1, image2 = image2)



if __name__ == "__main__":
   # app.run(debug=True)
    app.run(host='0.0.0.0', port=80)
