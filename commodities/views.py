from django.shortcuts import render
import numpy as np
from commodities.models import CommoditiesPrices, MediasCommodities
from bokeh.models import ColumnDataSource, RangeTool, HoverTool, Range1d
from bokeh.embed import components 
from bokeh.plotting import figure
from bokeh.layouts import column
from django.contrib.auth.decorators import login_required, user_passes_test
from bokeh.palettes import Category20, Category10

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


ALL_SPECIES_DATA = {
    'cordyceps': { 'nome': 'Cordyceps', 'preco_medio': {'extrato': 2.0537, 'capsulas': 0.1768, 'desidratado': 1.9836}, 'desvio_padrao': {'extrato': 0.7016, 'capsulas': 0.0627, 'desidratado': 0.6946}, 'tabela': {'Extrato (R$/ml)': {'media': 2.0537, 'mais_1s': 2.7553, 'menos_1s': 1.3522},'Cápsula (R$/mg)': {'media': 0.1768, 'mais_1s': 0.2395, 'menos_1s': 0.1140},'Desidratado (R$/g)': {'media': 1.9836, 'mais_1s': 2.6782, 'menos_1s': 1.2889}}},
    'reishi': { 'nome': 'Reishi', 'preco_medio': {'extrato': 2.4408, 'capsulas': 0.1689, 'desidratado': 2.0971}, 'desvio_padrao': {'extrato': 0.4311, 'capsulas': 0.0678, 'desidratado': 0.6607}, 'tabela': {'Extrato (R$/ml)': {'media': 2.4408, 'mais_1s': 2.8719, 'menos_1s': 2.0097},'Cápsula (R$/mg)': {'media': 0.1689, 'mais_1s': 0.2367, 'menos_1s': 0.1012},'Desidratado (R$/g)': {'media': 2.0971, 'mais_1s': 2.7578, 'menos_1s': 1.4363}}},
    'agaricus': { 'nome': 'Agaricus', 'preco_medio': {'extrato': 1.8998, 'capsulas': 0.1134, 'desidratado': 1.3996}, 'desvio_padrao': {'extrato': 0.5102, 'capsulas': 0.0501, 'desidratado': 0.5177}, 'tabela': {'Extrato (R$/ml)': {'media': 1.8998, 'mais_1s': 2.4100, 'menos_1s': 1.3896},'Cápsula (R$/mg)': {'media': 0.1134, 'mais_1s': 0.1635, 'menos_1s': 0.0633},'Desidratado (R$/g)': {'media': 1.3996, 'mais_1s': 1.9173, 'menos_1s': 0.8819}}},
    'juba': { 'nome': 'Juba de Leão', 'preco_medio': {'extrato': 1.9501, 'capsulas': 0.1603, 'desidratado': 2.0509}, 'desvio_padrao': {'extrato': 0.6688, 'capsulas': 0.0544, 'desidratado': 0.5906}, 'tabela': {'Extrato (R$/ml)': {'media': 1.9501, 'mais_1s': 2.6189, 'menos_1s': 1.2813},'Cápsula (R$/mg)': {'media': 0.1603, 'mais_1s': 0.2147, 'menos_1s': 0.1060},'Desidratado (R$/g)': {'media': 2.0509, 'mais_1s': 2.6415, 'menos_1s': 1.4602}}}
}
SPECIES_LIST_FOR_SIDEBAR = [
    {'slug': 'all', 'nome': 'Todas as Espécies'}, {'slug': 'cordyceps', 'nome': 'Cordyceps'},
    {'slug': 'reishi', 'nome': 'Reishi'}, {'slug': 'agaricus', 'nome': 'Agaricus'},
    {'slug': 'juba', 'nome': 'Juba de Leão'},
]

def create_bokeh_bar_chart(x_labels, y_values, y_axis_label, y_tooltip_format="0,0.0000", bar_color=Category10[3][0]):
    p = figure(
        x_range=x_labels, height=250, toolbar_location=None, tools="hover",
        tooltips=[("Espécie", "@x"), (y_axis_label, f"@top{{{y_tooltip_format}}}")],
        sizing_mode="stretch_width", background_fill_alpha=0, border_fill_alpha=0, 
        outline_line_color=None, min_border_left=40, min_border_bottom=50
    )
    p.vbar(x=x_labels, top=y_values, width=0.7 if len(x_labels) > 1 else 0.3, 
           fill_color=bar_color, line_color=bar_color)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.xaxis.major_label_orientation = 0.8 if len(x_labels) > 2 else 0
    axis_color, grid_color = ("#6b7280", "#d1d5db")
    p.xaxis.major_label_text_color = axis_color
    p.yaxis.major_label_text_color = axis_color
    p.yaxis.axis_label = y_axis_label
    p.yaxis.axis_label_text_font_style = "normal"
    p.yaxis.axis_label_text_color = axis_color
    p.yaxis.axis_label_text_font_size = "0.85rem"
    p.xaxis.axis_line_color = grid_color 
    p.yaxis.axis_line_color = grid_color
    p.ygrid.grid_line_color = grid_color
    p.legend.visible = False # O UserWarning sobre isso é normal se não houver legendas definidas
    return components(p)

@login_required
@user_passes_test(is_admin)
def db_cogumelos_view(request):
    selected_species_slug = request.GET.get('especie', 'all')
    
    context = {
        'species_list_sidebar': SPECIES_LIST_FOR_SIDEBAR,
        'selected_species_slug': selected_species_slug,
        'all_species_data_for_tables': ALL_SPECIES_DATA,
        'charts': {}, 
        'view_mode': selected_species_slug,
        'current_species_data': None
    }

    all_species_names_for_chart = [data['nome'] for data in ALL_SPECIES_DATA.values()]
    
    chart_types_map = {'preco_medio': 'Preço Médio', 'desvio_padrao': 'Desvio Padrão'}
    presentations_map = {'extrato': 'Extrato (R$/ml)', 'capsulas': 'Cápsulas (R$/mg)', 'desidratado': 'Desidratado (R$/g)'}
    presentations_units = {'extrato': 'R$/ml', 'capsulas': 'R$/mg', 'desidratado': 'R$/g'}

    if selected_species_slug == 'all':
        context['view_mode'] = 'all'
        # Charts para "Todas as Espécies"
        for chart_data_key in chart_types_map.keys():
            for pres_key, pres_unit in presentations_units.items():
                data_values = [data[chart_data_key][pres_key] for data in ALL_SPECIES_DATA.values()]
                chart_context_key_base = f"all_{chart_data_key}_{pres_key}"
                script, div = create_bokeh_bar_chart(all_species_names_for_chart, data_values, pres_unit)
                context['charts'][f'{chart_context_key_base}_script'] = script
                context['charts'][f'{chart_context_key_base}_div'] = div
    
    elif selected_species_slug in ALL_SPECIES_DATA:
        context['view_mode'] = 'single'
        species_data = ALL_SPECIES_DATA[selected_species_slug]
        context['current_species_data'] = species_data
        
        # Charts para a espécie individual
        # Inicializa um sub-dicionário para a espécie selecionada em charts
        context['charts'][selected_species_slug] = {}

        for chart_data_key in chart_types_map.keys():
            for pres_key, pres_unit in presentations_units.items():
                data_value = [species_data[chart_data_key][pres_key]]
                # As chaves do sub-dicionário serão mais simples agora
                sub_chart_key_base = f"{chart_data_key}_{pres_key}" # ex: preco_medio_extrato
                
                script, div = create_bokeh_bar_chart([species_data['nome']], data_value, pres_unit)
                context['charts'][selected_species_slug][f'{sub_chart_key_base}_script'] = script
                context['charts'][selected_species_slug][f'{sub_chart_key_base}_div'] = div
                
    template_to_render = 'commodities/db_cogumelos.html'
    if 'HX-Request' in request.headers:
        template_to_render = 'commodities/partials/cogumelos_graficos_tabelas_partial.html'
        
    return render(request, template_to_render, context)