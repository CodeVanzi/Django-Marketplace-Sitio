from django.shortcuts import render
from django.db.models import Max, Min
from commodities.models import CommoditiesPrices
from django.db.models import Q

from bokeh.models import ColumnDataSource
from bokeh.embed import components 
from bokeh.plotting import figure
from bokeh.layouts import column

from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # Dados de exemplo
    ativos = CommoditiesPrices.objects.values_list('ativo', flat=True).distinct()
    seen = set()
    ativos = [x for x in ativos if not (x in seen or seen.add(x))]
    active_category = request.GET.get('ativo', '')
    query = request.GET.get('query','')
    
    #se tiver query, busca na lista ativos se existe correspondencia parcial, e define active_category com a correspondencia mais proxima
    if query:
        busca = [x for x in ativos if query.lower() in x.lower()]
        if busca:
            active_category = busca[0]
        else:
            active_category = ''
    



    
    x_values = [1, 2, 3, 4, 5]
    y_values = [6, 7, 2, 3, 6]

    data = {'x_values': x_values, 'y_values': y_values}

    # Criar ColumnDataSource
    source = ColumnDataSource(data=data)

    # Criar figura
    fig = figure(title="Exemplo de Linha", x_axis_label="x", y_axis_label="y", height=500, width=800)
    fig.line(x='x_values', y='y_values', legend_label="Temp.", color="blue", line_width=2, source=source)
    fig.title.align = 'center'
    fig.title.text_font_size = '1.5em'
        
    # Layout
    layout = column(fig)

    # Obter os componentes do layout
    script, div = components(layout)

    # Contexto para o template
    context = {
        'script': script,
        'div': div,
        'ativos': ativos,
        'active_category': active_category,
    }
    if request.htmx:
        return render(request, 'commodities/partials/graf_partials.html', context)
    return render(request, 'commodities/dashboard.html', context)
