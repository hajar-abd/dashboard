###########################################################################################################################################
import dash_bootstrap_components as dbc
import dash
from dash import dash_table, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import zipfile
import os
###########################################################################################################################################
# Obtenez le chemin absolu du répertoire contenant le script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Chargez les fichiers en utilisant les chemins absolus
df_trials = pd.read_csv(os.path.join(BASE_DIR, "trials.csv"))
df_mesh = pd.read_csv(os.path.join(BASE_DIR, "mesh.csv"))
df_loc = pd.read_csv(os.path.join(BASE_DIR, "loc.csv"))
###########################################################################################################################################


def unzip_and_load(file_path, extract_to='.'):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        xml_file = zip_ref.namelist()[0]
        return os.path.join(extract_to, xml_file)

xml_file_path = unzip_and_load('desc2024.zip')


#creation de l'application dash avec le theme Cerulean 
app = dash.Dash(
    "oncoTrials",
    external_stylesheets=[dbc.themes.LUMEN, "/assets/style.css"],
    suppress_callback_exceptions=True
)
server = app.server
#aggregation des dataframes pour les graph


navbar = html.Div(
    className="navbar-custom",
    children=[
        html.Span("ONCOTRIAL TRACKER", className="navbar-title"),
        html.A(
            href="https://gitlab.com/hajar.abdaoui/oncotrial_tracker",
            target="_blank",
            children=html.Img(
                src="/assets/github-mark-white.png",
                className="gitlab-icon"
            )
        )
    ]
)



# tabs = html.Div(
#     [html.Br(),
#         dbc.Tabs(
#             [
#                 dbc.Tab(
#                     label="Dashboard", activeTabClassName="fw-bold"
#                 ),
#                 dbc.Tab(label="Table", activeLabelClassName="fw-bold"),
#             ]
#         ),
#     ], style={"margin-top": "-20px"}
# )

tabs = html.Div(
    className="sidebar",
    children=[
        dcc.Tabs(
            id="tabs",
            value="tab-dashboard",
            className="tabs-container",
            vertical=True,  # Rend les onglets verticaux
            children=[
                dcc.Tab(
                    label="Dashboard",
                    value="tab-dashboard",
                    className="tab",
                    selected_className="tab active"
                ),
                dcc.Tab(
                    label="Table",
                    value="tab-table",
                    className="tab",
                    selected_className="tab active"
                ),
                dcc.Tab(
                    label="About",
                    value="tab-about",
                    className="tab",
                    selected_className="tab active"
                ),
            ]
        )
    ]
)

######################################
######################################
study_counts = df_trials.groupby('startYear').size().reset_index(name='count')

fig_year_count = px.line(
    study_counts,
    x='startYear',
    y='count',
    labels={'startYear': 'Year', 'count': 'Studies'},
    title='Studies Started Each Year',
    markers=True,  # Ajoute des points sur la ligne
    color_discrete_sequence=['#007BA7']  # Couleur principale (bleu Bootstrap)
)

fig_year_count.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',   #fond transparent
    paper_bgcolor='rgba(0,0,0,0)',  #fond transparent
    font=dict(family="Arial", size=9, color="#333"),
    title_x=0.5,  #centrage du titre
    margin=dict(l=20, r=20, t=40, b=20),
    hovermode="x unified",   #survol des points

)


fig_year_count.update_xaxes(range=[1990, 2027])

######################################
completed = df_trials[df_trials["status"]=="Completed"]#.dropna(subset=["duration_year"])

fig_box_duration = px.box(
    completed,
    y="duration_year",
    title="Duration of completed studies",
    labels={"Years"},
    color_discrete_sequence=["#007BA7"]  # Couleur principale (bleu Bootstrap)
)

fig_box_duration.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',   # fond transparent rgba(255,255,255,1)
    paper_bgcolor='rgba(0,0,0,0)',  # fond transparent
    font=dict(family="Arial", size=9, color="#333"),
    title_x=0.5,  # centrage du titre
    height=300,  # Hauteur réduite
    width=400,   # Largeur standard
    margin=dict(l=50, r=50, t=30, b=50) 
)

fig_box_duration.update_yaxes(range=[0, 20], title="Duration in years")  # Plage et titre de l'axe Y
fig_box_duration.update_traces(marker=dict(color='#007BA7'))  # Garde la même couleur bleue que le graphique linéaire

######################################
drug_pourcentage = round(len(df_trials[df_trials.drug_FDA == True])*100/(len(df_trials[df_trials.drug_FDA == True]) + len(df_trials[df_trials.drug_FDA == False])),1)
device_pourcentage = round(len(df_trials[df_trials.device_FDA == True])*100/(len(df_trials[df_trials.device_FDA == True]) + len(df_trials[df_trials.device_FDA == False])),1)

cards_info = [
    {"title": "Total Trials", "content": len(df_trials)},
    {"title": "Completed Trials", "content": len(completed)},
    {"title": "FDA Regulated Drug Product", "content": "{} %".format(drug_pourcentage)},
    {"title": "FDA Regulated Device Product", "content": "{} %".format(device_pourcentage)}
]

card_layout = html.Div(
    className="number-card-layout-container",  # Applique le style global du conteneur
    children=[
        html.Div(
            className="number-card",  # Style pour chaque carte
            children=[
                html.Div(card["content"], className="number-card-title"),  # Le chiffre principal
                html.Div(card["title"], className="number-card-text")  # Le texte descriptif
            ]
        ) for card in cards_info  # Génération dynamique des cartes
    ]
)



######################################

categories = df_mesh['neoplasm_category'].unique()
@app.callback(
    Output('top-neoplasms-graph', 'figure'),
    Input('category-dropdown', 'value')
)
def update_graph(selected_category):
    # Filtrer le DataFrame en fonction de la catégorie sélectionnée
    df_filtered = df_mesh[df_mesh['neoplasm_category'] == selected_category]

    # Compter le nombre d'études par néoplasme
    count_df = df_filtered['neoplasm'].value_counts().reset_index()
    count_df.columns = ['neoplasm', 'count']
    count_df = count_df.sort_values(by='count', ascending=False)

    # Sélectionner les 10 néoplasmes les plus fréquents
    top_10_df = count_df.head(10)

    # Création de la figure harmonisée
    fig = px.bar(
        top_10_df,
        x='neoplasm',
        y='count',
        labels={'neoplasm': 'Neoplasm class', 'count': "Number of studies"},
        title=f"The 10 most studied neoplasms ({selected_category})",
        color_discrete_sequence=["#027699"]  # Même bleu que le boxplot
    )

    # Mise en forme harmonisée
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',    # Fond transparent
        paper_bgcolor='rgba(0,0,0,0)',   # Fond transparent
        font=dict(family="Arial", size=9, color="#333"),  # Police uniforme
        title_x=0.5,                     # Titre centré
        margin=dict(l=40, r=40, t=60, b=30),
        height=450,
        hovermode="x unified"            # Effet de survol unifié
    )

    fig.update_xaxes(tickangle=-45)     # Inclinaison des étiquettes X
    fig.update_yaxes(showgrid=True, gridcolor='lightgrey')  # Grille légère

    return fig
######################################

df=df_trials[df_trials.results==True]
last_results = df[["nctid", "title", "organization", "description", "last_update"]].sort_values(by='last_update', ascending=False).head(5)

study_cards = [
    dbc.Card(
        dbc.CardBody([
            html.A(study["title"], href="https://clinicaltrials.gov/ct2/show/{}".format(study["nctid"]), target="_blank", style={"font-size": "0.85rem"}),
            html.H6(study['organization'], className="card-subtitle mb-2 text-muted", style={"font-size": "0.8rem"}),
            html.P(study["description"], className="card-text", style={"text-align": "justify", "font-size": "0.7rem"}),
            html.Footer(f"Last Update: {study['last_update']}", className="text-end text-secondary", style={"font-size": "0.6rem"})
        ]),
        className="mb-3 shadow-sm p-2 bg-light rounded"
    )
    for _, study in last_results.iterrows()
]
######################################


content = dbc.Container(
    [
        # Section des cartes principales
        card_layout,

        # Section combinée : Encadré + Graphique linéaire + Boxplot
        dbc.Row([
            # Colonne principale (Encadré + Graphique linéaire)
            dbc.Col([
                # Encadré d'information
                dbc.Card(
                    dbc.CardBody([
                        html.H6("Study Trends Over the Years", className="fw-bold text-primary", style={"margin-top": "-5px", "font-size": "0.85rem"}),
                        html.P(
                            "This graph shows the annual distribution of studies, providing insights into research trends over time.",
                            style={"text-align": "justify", "font-size": "0.75rem"}
                        )
                    ]),
                    className="text-card"
                ),

                # Graphique linéaire
                dbc.Card(
                    dbc.CardBody(
                        dbc.Spinner(
                            dcc.Graph(id='study-year-graph', figure=fig_year_count,
                                      style={"width": "100%", "height": "150px", "margin": "-25px"}),
                            color="primary"
                        )
                    ),
                    className="shadow-sm p-3 mb-4 bg-white rounded",
                    style={"width": "100%"}
                )
            ], width=8),

            # Boxplot aligné à droite
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        dbc.Spinner(
                            dcc.Graph(id='study-duration-graph', figure=fig_box_duration,
                                      style={"width": "100%", "margin": "0", "margin-top": "30px", "margin-right": "-10px"}),
                            color="primary"
                        )
                    ),
                    className="shadow-sm p-3 mb-4 bg-white rounded",
                    style={"width": "100%", "height": "315px", "margin-top": "-75px", "justify-content": "center", "align-items": "center"}
                ),
                width=4
            )
        ],justify="between"),

        dbc.Row([
            # Dropdown + Graphique des néoplasmes
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        dcc.Dropdown(
                            id='category-dropdown',
                            options=[{'label': cat, 'value': cat} for cat in categories],
                            value='Neoplasms by Site',
                            clearable=False, 
                            style={
                                    "width": "100%",  # Réduit la largeur à 50% de son conteneur
                                    "height": "30px",  # Réduit la hauteur
                                    "font-size": "0.85rem",  # Réduit la taille de la police
                                    "padding": "0px"  # Réduit les marges internes
                                }
                        ),
                        dbc.Spinner(
                            dcc.Graph(id='top-neoplasms-graph'),
                            color="primary"
                        )
                    ]),
                    className="shadow-sm p-3 mb-4 bg-white rounded", 
                    style={"height": "525px", "margin-top": "-18px"}
                ),
                width=6
            ),

            # Deux encadrés de texte descriptif
            dbc.Col([
                # Premier encadré
                dbc.Card(
                    dbc.CardBody([
                        html.P(
                            '''MeSH (Medical Subject Headings) is a controlled vocabulary 
                            developed by the National Library of Medicine (NLM) to index, organize, and search biomedical information 
                            in databases like PubMed and ClinicalTrials.gov. It follows a hierarchical structure, allowing terms to be 
                            classified from broad categories to more specific subcategories. For example, Neoplasms is a primary category, 
                            which branches into subcategories like Neoplasms by Site, Neoplasms by Histologic Type, and Cysts. 
                            This structure helps standardize medical terminology, improve the accuracy of search queries, 
                            and link related research topics.''',
                            style={"text-align": "justify", "font-size" : "0.7rem", "margin-top": "-10px"}
                        )
                    ]),
                    className="text-card",
                    style={"height": "135px", "margin-top": "-20px"}  # Texte défilable
                ),

                # Deuxième encadré
                dbc.Card(
                    dbc.CardBody([
                        html.H6("Latest 5 Studies", className="text-center fw-bold text-primary"),
                        html.Div(study_cards, style={"height": "340px", "overflowY": "auto"})  # Scrollable
                    ]),
                    className="shadow-sm p-3 bg-white rounded",
                    style={"height": "388px", "overflowY": "hidden", "margin-top" : "2px"}  # Texte défilable
                )
            ], width=6)
        ])
    ],
    fluid=True,
    className="mt-4"
)

######################################

df_loc_grouped = df_loc.groupby("nctid").agg({
    "facility": lambda x: "\n".join(sorted(set(x.dropna()))),
    "city": lambda x: "\n".join(sorted(set(x.dropna()))),
    "country": "first"
}).reset_index()

# Fusion des DataFrames
df_combined = pd.merge(df_trials, df_loc_grouped, on="nctid", how="inner")[[
    "title", "organization", "condition", "study_type", "status", "city", "contact"
]]

# Renommer les colonnes pour plus de clarté
df_combined.rename(columns={
    "title": "Title",
    "organization": "Organization",
    "condition": "Condition",
    "study_type": "Type",
    "city": "Location",
    "status": "Status",
    "contact": "Contact"
}, inplace=True)
######################################

content2 = dbc.Container([
    html.H3("Tableau des Essais Cliniques", className="text-center my-4 fw-bold text-primary"),

    dbc.Card(
        dbc.CardBody([
            dash_table.DataTable(
                id='table',
                columns=[
                    {"name": col, "id": col, "deletable": False} 
                    for col in df_combined.columns
                ],
                data=df_combined.to_dict('records'),
                page_size=10,
                filter_action="native",  # Activation du filtrage natif
                sort_action="native",    # Activation du tri natif
                sort_mode="multi",       # Tri sur plusieurs colonnes
                column_selectable='single',  # Activation de la sélection de colonnes
                style_table={'overflowX': 'auto'},
                style_cell={
                    'whiteSpace': 'pre-line',  # Support du saut de ligne '\n'
                    'textAlign': 'left',
                    'padding': '10px',
                    'fontFamily': 'Arial'
                },
                style_header={
                    'backgroundColor': '#007BA7',
                    'color': 'white',
                    'fontWeight': 'bold',
                    'textAlign': 'center'
                },
                style_data={
                    'backgroundColor': 'white',
                    'color': 'black'
                },
                style_data_conditional=[
                    {  # Effet zébré pour les lignes impaires
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#F9F9F9'
                    }
                ]
            )
        ]),
        className="shadow-sm p-4 bg-white rounded"
    )
], fluid=True)


############################################################################################

content3 = dbc.Container(
    [
        html.H5("About", className="text-center my-4 fw-bold text-primary"),

        # Une seule carte pour contenir tout le contenu
        dbc.Card(
            dbc.CardBody(
                [
                    # Section Contexte
                    html.H6("Context", className="fw-bold text-secondary"),
                    html.P(
                        '''The OncoTrials Tracker application presented here was developed as part of the web scraping course, 
                        with the aim of facilitating the analysis and exploration of clinical trials listed in the 
                        ClinicalTrials.gov database. The trials concern cancers listed in France.''',
                        style={"text-align": "justify", "font-size": "0.8rem"}
                    ),
                    html.Hr(),  # Ligne séparatrice

                    # Section Objectifs du projet
                    html.H6("Project objectives", className="fw-bold text-secondary"),
                    html.Ul(
                        [
                            html.Li("Centralize and visualize data on clinical trials in France."),
                            html.Li("Provide an interactive tool for exploring studies by organ, type of intervention or trial status."),
                            html.Li("Provide graphical analyses to improve understanding of clinical trials."),
                            html.Li("Help healthcare professionals and researchers identify opportunities and keep abreast of the latest trends and advances in the field.")
                        ],
                        style={"font-size": "0.8rem", "text-align": "justify"}
                    ),
                    html.Hr(),

                    # Section Sources des données
                    html.H6("Data sources", className="fw-bold text-secondary"),
                    html.P(
                        '''The data used in this project comes from the ClinicalTrials.gov public API. 
                        Using web scraping scripts, the data was collected, cleaned and integrated into a database. 
                        The application then presents this information intuitively and interactively through an interface built with Dash (or other).''',
                        style={"text-align": "justify", "font-size": "0.8rem"}
                    ),
                    html.Hr(),

                    # Section Comment ça fonctionne ?
                    html.H6("How it works ?", className="fw-bold text-secondary"),
                    html.P(
                        '''Clinical trials are extracted and organized into several categories. This data is processed to provide a clear 
                        visualization, with sorting and search options.''',
                        style={"text-align": "justify", "font-size": "0.8rem"}
                    ),
                    html.P(
                        '''The project uses data manipulation techniques and interactive visualization tools to meet the needs of end-users.''',
                        style={"text-align": "justify", "font-size": "0.8rem"}
                    ),
                    html.Hr(),

                    # Section À qui s'adresse ce projet ?
                    html.H6("Who is this project for?", className="fw-bold text-secondary"),
                    html.Ul(
                        [
                            html.Li("Healthcare professionals seeking an overview of clinical trials in France."),
                            html.Li("Researchers working on the development of new therapies."),
                            html.Li("Institutions involved in monitoring clinical trials.")
                        ],
                        style={"font-size": "0.8rem", "text-align": "justify"}
                    ),
                    html.Hr(),

                    # Section Équipe et développement
                    html.H6("Team and development", className="fw-bold text-secondary"),
                    html.P(
                        '''This project was created by ..., as part of the Master Data Science en Santé program at the University of Lille (ILIS). 
                        It is based on data extracted via the ClinicalTrials.gov API, and was presented during the web scraping course taught by Mr. Djamel ZITOUNI.''',
                        style={"text-align": "justify", "font-size": "0.8rem"}
                    ),
                    html.P(
                        '''The application is an information tool, and the data it synthesizes should not be used for medical or legal decisions.''',
                        style={"text-align": "justify", "font-size": "0.8rem"}
                    )
                ]
            ),
            className="shadow-sm p-4 mb-4 bg-white rounded"  # Style de la carte
        )
    ],
    fluid=True
)



######################################
# app.layout = html.Div([
#     dcc.Location(id="url"),
#     navbar, tabs, content, footer
# ])
@app.callback(
    Output('tab-content', 'children'),
    [Input('tabs', 'value')]
)
def render_content(tab):
    if tab == 'tab-dashboard':
        return content
    elif tab == 'tab-table':
        return content2
    elif tab == 'tab-about':  # Condition pour "À propos"
        return content3
    return content  # Par défaut

app.layout = html.Div(
    className="main-container",
    children=[
        navbar,
        html.Div(
            className="layout-container",
            children=[
                tabs,  # Navigation latérale
                html.Div(
                    id="tab-content",
                    className="content-container"  # Conteneur pour afficher le contenu
                )
            ]
        )
    ]
)

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=5000, debug=True)


