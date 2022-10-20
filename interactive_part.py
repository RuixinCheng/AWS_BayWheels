import sys
sys.path.append("/home/ec2-user/.local/lib/python3.7/site-packages")

import pandas as pd
from pandas.core.dtypes.inference import is_number
import difflib

#read dataset
station_data = pd.read_csv("Station_info_cleaned.csv")
# prepare station name list 
station_list = list(station_data['short_name']) + list(station_data['name'])
# input x should be string and the station name (either short name or name),
# the return value will be the capacity of this station. 
def st_info(x):
    output = 0
    for i in range(len(station_data)):
        if x in station_list:
            output = station_data['capacity'][i]
            break
    return output

# start flask
from flask import Flask, request, render_template
app = Flask("APAN5450App")
@app.route('/interactive',methods = ['POST','GET'])

def find_capacity():
    # connect with iabw.html file
    if request.method == 'POST':
        finding_name = str(request.form.get('finding_name'))
        capacity = st_info(finding_name)
        return render_template("iabw.html", output = capacity)
    else:
        capacity = 'Unfind'
        return render_template("iabw.html", output = capacity)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

