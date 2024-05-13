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
    # max_data = CommoditiesPrices.objects.all().aggregate(Max('data'))
    # max_preco = CommoditiesPrices.objects.all().aggregate(Max('preco_de_fechamento'))
    # min_preco = CommoditiesPrices.objects.all().aggregate(Min('preco_de_fechamento'))
    
    count = int(request.GET.get('count', 5))
    recorte = CommoditiesPrices.objects.all().order_by('data').reverse()[:count]
    ativo = [r.ativo for r in recorte]
    preco_ativo = [r.preco_de_fechamento for r in recorte]
    
    cds = ColumnDataSource(data=dict(ativo=ativo, preco_ativo=preco_ativo))
    
    fig = figure(x_range=ativo, height=500, title=f' Maiores {{count}} preços de fechamento por ativo',)
    
    fig.vbar(x='ativo', top='preco_ativo', width=0.8, source=cds)
    
    script, div = components(fig)

    context = {
        'script': script,
        'div': div
    }
    
    
    return render(request, 'commodities/dashboard.html', context)