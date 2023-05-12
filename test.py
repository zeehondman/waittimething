import pytz
from flask import Flask, render_template
import requests
from datetime import datetime

app = Flask(__name__)

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
    # Convert the datetime string to a datetime object
    dt = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')

    # Set the timezone to Amsterdam
    amsterdam_tz = pytz.timezone('Europe/Amsterdam')
    dt_amsterdam = pytz.utc.localize(dt).astimezone(amsterdam_tz)

    # Format the datetime object in the specified format
    return dt_amsterdam.strftime(format)

@app.route('/')
def index():
    url = "https://queue-times.com/parks/305/queue_times.json"
    response = requests.get(url)
    
    if response.ok:
        data = response.json()
        return render_template('index.html', rides=data['rides'])
    else:
        return "Error retrieving data:", response.status_code

if __name__ == '__main__':
    app.run(debug=True)
