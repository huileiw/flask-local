from flask import Flask, render_template
app = Flask(__name__)

import requests
import pandas as pd
from bokeh.plotting import figure,output_file,show
from bokeh.embed import components

url_path = 'https://www.quandl.com/api/v3/datasets/WIKI/%s' % "GOOG"
session = requests.Session()
r = requests.get(url_path)
new_data = r.json()

# Bokeh tools
TOOLS = "resize,pan,wheel_zoom,box_zoom,reset,previewsave"

column_names = new_data['dataset']['column_names']
inp_dataset=new_data['dataset']['data']
df = pd.DataFrame(inp_dataset,columns = column_names)

df['Date']=pd.to_datetime(df['Date'])


def make_figure():
    plot = figure(tools=TOOLS
                 , width = 750
                 , height = 450
                 , title = 'Google Stock Price'
                 , x_axis_label = 'date'
                 , x_axis_type = 'datetime')
    plot.line(df['Date'], df.get('Open'), color = 'Orange', legend = 'Open')
    
    return plot

@app.route('/')
def hello_world():
    plot = make_figure()
    script, div = components(plot)
    return render_template('graph.html',script=script, div=div)

if __name__ == '__main__':
    app.run(port=33507)