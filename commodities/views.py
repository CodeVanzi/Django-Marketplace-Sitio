from django.shortcuts import render
import numpy as np
from commodities.models import CommoditiesPrices
from bokeh.models import ColumnDataSource, RangeTool
from bokeh.embed import components 
from bokeh.plotting import figure
from bokeh.layouts import column
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    ativos = CommoditiesPrices.objects.values_list('ativo', flat=True).distinct()
    seen = set()
    ativos = [x for x in ativos if not (x in seen or seen.add(x))]
    active_category = request.GET.get('ativo', '')
    query = request.GET.get('query', '')
    
    # Se tiver query, busca na lista ativos se existe correspondência parcial, e define active_category com a correspondência mais próxima
    if query:
        busca = [x for x in ativos if query.lower() in x.lower()]
        if busca:
            active_category = busca[0]
        else:
            active_category = ''
    
    if active_category != '':
        df = CommoditiesPrices.objects.filter(ativo=active_category)
    else:
        df = CommoditiesPrices.objects.all()
    
    # Converter valores do QuerySet para listas
    dates = list(df.values_list('data', flat=True).distinct())
    prices = list(df.values_list('preco_de_fechamento', flat=True))

    # Garantir que as listas sejam arrays numpy para o Bokeh
    dates = np.array(dates, dtype=np.datetime64)
    prices = np.array(prices, dtype=float)

    source = ColumnDataSource(data=dict(date=dates, close=prices))

    if len(dates) > 0:
        date_start = dates.min()
        date_end = dates.max()
    else:
        date_start = np.datetime64('2023-05-14')
        date_end = np.datetime64('2024-05-14')

    p = figure(title=f'{active_category}', height=500, width=830, tools="xpan", toolbar_location=None,
               x_axis_type="datetime", x_axis_location="above",
               background_fill_color="#efefef", x_range=(date_start, date_end))

    p.line('date', 'close', source=source)
    p.yaxis.axis_label = 'Price'
    p.title.align = 'center'
    p.title.text_font_size = '1.5em'

    select = figure(title="Arraste a caixa para alterar o intervalo de datas",
                    height=130, width=830, y_range=p.y_range,
                    x_axis_type="datetime", y_axis_type=None,
                    tools="", toolbar_location=None, background_fill_color="#efefef")

    range_tool = RangeTool(x_range=p.x_range)
    range_tool.overlay.fill_color = "navy"
    range_tool.overlay.fill_alpha = 0.2

    select.line('date', 'close', source=source)
    select.ygrid.grid_line_color = None
    select.add_tools(range_tool)

    # Layout
    layout = column(p, select)
    
    # Componentes do layout
    script, div = components(layout)

    # Contexto para o template
    context = {
        'script': script,
        'div': div,
        'ativos': ativos,
        'active_category': active_category,
    }
    
    if 'HX-Request' in request.headers:
        return render(request, 'commodities/partials/graf_partials.html', context)
    return render(request, 'commodities/dashboard.html', context)
