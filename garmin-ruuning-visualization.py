import pandas as pd

from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.models import HoverTool
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.models.ranges import Range1d
from bokeh.models.axes import LinearAxis

from lxml import etree
from dateutil import parser


# Get data from .tcx
tree = etree.parse("activity_4019358445.tcx")
root = tree.getroot()

points = root.findall('.//Trackpoint', root.nsmap)

all_data = []

for pt in points:
    t = pt.find('./Time', root.nsmap)
    bmp = pt.find('./HeartRateBpm/Value', root.nsmap)
    cad = pt.find('./Extensions/ns3:TPX/ns3:RunCadence', root.nsmap)
    dis = pt.find('./DistanceMeters', root.nsmap)
    spd = pt.find('./Extensions/ns3:TPX/ns3:Speed', root.nsmap)
    
    all_data.append( { 'time' : parser.parse(t.text),
                       'bmp' : int(bmp.text),
                       'cad' : float(cad.text),
                       'dis' : float(dis.text),
                       'spd' : float(spd.text) 
                     } 
                   )


# Visualize
output_file("final.html")

df = pd.DataFrame(all_data)

hover = HoverTool(
    tooltips=[
        ( 'time', '@time{%R}'),
        ( 'bmp', '@bmp{000.}'),
        ( 'cad', '@cad'),
        ( 'spd', '@spd')
    ],

    formatters={
        'time' : 'datetime',
    },

    mode='vline'
)

p = figure(x_axis_type="datetime", plot_width=600, plot_height=300, tools=[hover], title="all-data_time_hover")

# range for each data field
p.y_range = Range1d(0, 220)  # bmp
p.extra_y_ranges = {"cad": Range1d(start=0, end=140),   # RunCadence
                    "spd": Range1d(start=0, end=10.0) }  # Speed

# add the extra range to the right of the plot
p.add_layout(LinearAxis(y_range_name="cad"), 'right')
p.add_layout(LinearAxis(y_range_name="spd"), 'right')

# set axis text color
p.yaxis[0].major_label_text_color = "red"  
p.yaxis[1].major_label_text_color = "blue"  
p.yaxis[2].major_label_text_color = "purple"  


## plot !
p.line(df['time'], df['bmp'], legend='bmp', line_color="red", muted_color='red', muted_alpha=0.2)

p.line(df['time'], df['cad'], legend='cad', line_color="blue", muted_color='blue', muted_alpha=0.2, y_range_name='cad')

p.line(df['time'], df['spd'], legend='spd', color="purple", muted_color='purple', muted_alpha=0.2, y_range_name='spd')


# setting for legend
p.legend.location = "top_right"
p.legend.click_policy="mute"



show(p)

