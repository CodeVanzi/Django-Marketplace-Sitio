from django.shortcuts import render
import numpy as np
from commodities.models import CommoditiesPrices, MediasCommodities
from bokeh.models import ColumnDataSource, RangeTool, HoverTool, Range1d
from bokeh.embed import components 
from bokeh.plotting import figure
from bokeh.layouts import column
from django.contrib.auth.decorators import login_required, user_passes_test
from bokeh.palettes import Category20

# Função de verificação para checar se o usuário é um administrador
def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def dashboard(request):
    ativos = CommoditiesPrices.objects.values_list('ativo', flat=True).distinct()
    seen = set()
    ativos = [x for x in ativos if not (x in seen or seen.add(x))]
    active_category = request.GET.get('ativo', '')
    query = request.GET.get('query', '')
    dados_tabela = MediasCommodities.objects.all()

    # Se tiver query, busca na lista ativos se existe correspondência parcial, e define active_category com a correspondência mais próxima
    if query:
        busca = [x for x in ativos if query.lower() in x.lower()]
        if busca:
            active_category = busca[0]
        else:
            active_category = ''

    # Filtra por ativo, se um ativo específico foi selecionado
    if active_category:
        df = CommoditiesPrices.objects.filter(ativo=active_category)
        dados_tabela = MediasCommodities.objects.filter(ativo=active_category)
    else:
        df = CommoditiesPrices.objects.all()
        dados_tabela = MediasCommodities.objects.all()

    # Definindo a paleta de cores para os ativos
    colors = Category20[len(ativos)] if len(ativos) <= 20 else Category20[20]

    p = figure(title=f'Preços do(s) ativo(s) { active_category }', height=500, width=800, tools="xpan", toolbar_location=None,
               x_axis_type="datetime", x_axis_location="above",
               background_fill_color="#efefef")

    # Adiciona o HoverTool
    hover = HoverTool(
        tooltips=[
            ("Ativo", "@ativo"),
            ("Data", "@date{%F}"),
            ("Preço", "@close{$0,0.00}")
        ],
        formatters={
            "@date": "datetime",
        },
        mode='vline'
    )
    p.add_tools(hover)

    select = figure(title="Arraste o meio e as bordas da caixa abaixo, para alterar o intervalo de visualização acima",
                    height=130, width=800, x_axis_type="datetime", y_axis_type=None,
                    tools="", toolbar_location=None, background_fill_color="#efefef")


    date_start = np.datetime64('2023-05-14')
    date_end = np.datetime64('2024-05-14')

    for i, ativo in enumerate(ativos):
        # Filtra os dados para o ativo atual
        df_ativo = df.filter(ativo=ativo)
        dates = np.array(df_ativo.values_list('data', flat=True).distinct(), dtype=np.datetime64)
        prices = np.array(df_ativo.values_list('preco_de_fechamento', flat=True), dtype=float)
        
        # Atualiza o intervalo de datas
        if len(dates) > 0:
            date_start = min(date_start, dates.min())
            date_end = max(date_end, dates.max())

        source = ColumnDataSource(data=dict(date=dates, close=prices, ativo=[ativo] * len(dates)))

        # Adiciona a linha ao gráfico principal
        p.line('date', 'close', source=source, color=colors[i % len(colors)], legend_label=ativo)
        
        # Adiciona a linha ao gráfico de seleção
        select.line('date', 'close', source=source, color=colors[i % len(colors)])
    
    p.yaxis.axis_label = 'Preço de fechamento ($USD/tonelada)'
    p.title.align = 'center'
    p.title.text_font_size = '1.5em'
    p.x_range = Range1d(start=date_start, end=date_end)
    p.legend.title = 'Commodities'
    p.legend.location = "top_left"

    select.ygrid.grid_line_color = None
    range_tool = RangeTool(x_range=p.x_range)
    range_tool.overlay.fill_color = "navy"
    range_tool.overlay.fill_alpha = 0.2
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
        'dados_tabela': dados_tabela,
    }
    
    if 'HX-Request' in request.headers:
        return render(request, 'commodities/partials/graf_partials.html', context)
    return render(request, 'commodities/dashboard.html', context)
