from django.shortcuts import render
from django.db.models import Max, Min
from commodities.models import CommoditiesPrices

from bokeh.models import ColumnDataSource
from bokeh.embed import components 
from bokeh.plotting import figure
from bokeh.layouts import column

from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # Dados de exemplo
    x_values = [1, 2, 3, 4, 5]
    y_values = [6, 7, 2, 3, 6]

    data = {'x_values': x_values, 'y_values': y_values}

    # Criar ColumnDataSource
    source = ColumnDataSource(data=data)

    # Criar figura
    fig = figure(title="Exemplo de Linha", x_axis_label="x", y_axis_label="y", height=500, width=800)
    fig.line(x='x_values', y='y_values', legend_label="Temp.", color="blue", line_width=2, source=source)
        
    # Layout
    layout = column(fig)

    # Obter os componentes do layout
    script, div = components(layout)

    # Contexto para o template
    context = {
        'script': script,
        'div': div,
    }

    return render(request, 'commodities/dashboard.html', context)
