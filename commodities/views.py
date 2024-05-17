from django.shortcuts import render
from django.db.models import Max, Min
from commodities.models import CommoditiesPrices

from bokeh.models import ColumnDataSource
from bokeh.embed import components 
from bokeh.plotting import figure


from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def dashboard(request):

    data = {'x_values': [1, 2, 3, 4, 5],
            'y_values': [6, 7, 2, 3, 6]}

    # create a ColumnDataSource by passing the dict
    source = ColumnDataSource(data=data)
    
    fig = figure(title="Multiple line example", x_axis_label="x", y_axis_label="y", height=500,)
    
    # fig.vbar(x='País', top='Numero', width=0.8, source=cds)
    fig.line(x='x_values', y='y_values', legend_label="Temp.", color="blue", line_width=2, source=source)

    
    div, script = components(fig)

    context = {
        'script': script,
        'div': div,
    }
    
    
    return render(request, 'commodities/dashboard.html', context)