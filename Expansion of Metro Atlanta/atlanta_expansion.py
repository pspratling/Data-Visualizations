import pandas as pd
from bokeh.plotting import figure, ColumnDataSource
from bokeh.io import curdoc
from bokeh.models import HoverTool, LinearColorMapper
from bokeh.models.widgets import Slider
from bokeh.layouts import column, widgetbox
from bokeh.sampledata.us_counties import data as counties
from bokeh.palettes import PuBuGn8


#reading in GA population density data 
df = pd.read_csv(".\data\GA County Population Density 1980-2017.csv")

#extracting ga county information
ga_counties = {key: info for key, info in counties.items() if info['state']=='ga'}
county_names = [county_info['name'] for county_info in ga_counties.values()]
county_lons = [county_info['lons'] for county_info in ga_counties.values()]
county_lats = [county_info['lats'] for county_info in ga_counties.values()]        

#initializing ColumnDataSource to 1980 densities
source = ColumnDataSource(data=dict(
    x = county_lons,
    y = county_lats,
    county = county_names,
    density = df['1980']
))

#initializing Slider object
slider = Slider(title='Year', value=1980, start=1980, end=2017)

#updating source data on slider change
def update_data(attr, old, new):
    year = str(slider.value)
    source.data['density'] = df[year]

slider.on_change('value', update_data) 


#displays county name and population density on hover
hover = HoverTool(tooltips=[
        ('County', '@county'),
        ('Population Density', '@density people/square mile')
        ])

#creating figure    
p = figure(
        title='Georgia Population Density by County',
        tools=[hover, 'reset', 'pan', 'wheel_zoom']
        )

#setting color palette, reversing, and getting rid of lighter colors
palette = PuBuGn8[-3::-1]
cmap = LinearColorMapper(palette=palette)

#plotting counties and setting to be colored by density value
p.patches('x', 'y', source=source,
          fill_color={'field': 'density', 'transform': cmap},
          fill_alpha=0.8, line_color="white", line_width=0.5
          )

#plotting Atlanta and getting rid of plot grid
p.circle(-84.388, 33.749, color='red', alpha=0.5)
p.grid.grid_line_color = None
 
    
#adding layouts    
layout = widgetbox(slider)
curdoc().add_root(column(slider, p))
curdoc().title = 'Expansion of Metro Atlanta'