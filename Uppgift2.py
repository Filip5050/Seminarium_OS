import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import os


file_path = os.path.join(os.path.dirname(__file__), "athlete_events.csv")

OS_df = pd.read_csv(file_path)

app = Dash(__name__) #initiserar Dash
server = app.server
app.layout = html.Div([
    html.Div([
    html.H1("Medalj fördelningen mellan länderna i Basket och Judo"), #Ger dash datan en titel
    html.Label("Välj sport"),
    dcc.Dropdown( #Skapar en dropdown som gör man kan välja vilka sporter vi ska använda
        id="sport-dropdown", #skapar en id som används till inputen i callback funktionen senare
        #De olika valen som går att intergrera med
        options=[
            {"label": "Basketball", "value": "Basketball"},{"label": "Judo", "value": "Judo"},{"label": "Football", "value": "Football"},
        ],
        value="Basketball" #sporten som visas när man startar dashen
    ),
    dcc.Graph(id="medal-graph")
    ]),
    html.Hr(),
    html.Div([
        html.H1("längd skillnaden mellan sporterna"),
        html.Label("Välj Sport"),
        dcc.Dropdown(
            id="längd-dropdown",
            options=[
                {"label": "Basketball", "value": "Basketball"},{"label": "Judo", "value": "Judo"},{"label": "Football", "value": "Football"},
            ],
            value="Basketball"
        ),
        dcc.Graph(id="längd-graph")
    ]),
    html.Hr(),
    html.Div([
        html.H1("Åldersfördelning i Basket, Judo och Fotboll"),  
        html.Label("Välj sport"),  
        dcc.Dropdown(
        id="age-dropdown",
        options=[
            {"label": "Basketball", "value": "Basketball"},
            {"label": "Judo", "value": "Judo"},
            {"label": "Football", "value": "Football"}
        ],  # Endast dessa sporter är valbara
        value="Basketball"  # Förvald sport
    ),
    dcc.Graph(id="age-distribution-graph")  # Diagram för åldersfördelning
    ]),
    html.Hr(),
    html.Div([
        html.H1("Hur många deltagare det är ifrån de olika kontinenterna i sporterna Basket, Judo och Fotboll"),
        html.Label("Välj sport"),
        dcc.Dropdown(
        id="player-dropdown",
        options=[
            {"label": "Basketball", "value": "Basketball"},
            {"label": "Judo", "value": "Judo"},
            {"label": "Football", "value": "Football"}
        ],  # Endast dessa sporter är valbara
        value="Basketball"  # Förvald sport
    ),  
    dcc.Graph(id="players-graph")      
    ])
])

#Funktionen som tillkallas när man väljer en av alternativen i dropdownen
@app.callback(
    Output("medal-graph", "figure"),
    [Input("sport-dropdown", "value")]
)
def sport_graph(selected_sport):
    filtered_data = OS_df[OS_df["Sport"] == selected_sport] #filtrerar datan så jag bara får ut data från året jag väljer
    medals = filtered_data.groupby(["NOC","Medal"]).size().reset_index(name="Medaljer") #
    fig = px.histogram(medals, x="NOC", y="Medaljer", barmode="stack",  color="Medal", color_discrete_map={
            "Gold": "yellow", 
            "Silver": "grey", 
            "Bronze": "brown",}, 
        labels=f" Medaljer sporterna har fått i {selected_sport}")
    return fig

@app.callback(
    Output("längd-graph", "figure"),
    [Input("längd-dropdown", "value")]
)
def height_graph(selected_sport):
    filtered_data = OS_df[OS_df["Sport"] == selected_sport]
    fig = px.histogram(filtered_data, x="Height",y="ID", title=f"längd i {selected_sport}")
    fig.update_layout(
        xaxis_title="Längd",
        yaxis_title="Antal Idrottare",
        bargap=0.1,  
        xaxis=dict(tickmode="linear")  
    )
    return fig

@app.callback(
    Output("age-distribution-graph", "figure"),
    [Input("age-dropdown", "value")]
)
def update_age_distribution(selected_sport):
    filtered_sports_df = OS_df[OS_df["Sport"].isin(["Basketball", "Judo", "Football"])]
    # Filtrera data för den valda sporten
    filtered_data = filtered_sports_df[filtered_sports_df["Sport"] == selected_sport]
    
    # Skapa ett histogram för åldersfördelning
    fig = px.histogram(
        filtered_data,
        x="Age",
        title=f"Åldersfördelning i {selected_sport}",
        labels={"Age": "Ålder", "count": "Antal Idrottare"},
        color_discrete_sequence=["#1f77b4"],
        category_orders={"Age": sorted(filtered_data["Age"].unique())}  # Säkerställer sortering av åldrar
    )
    
    # Säkerställa att åldrar inte grupperas
    fig.update_layout(
        xaxis_title="Ålder",
        yaxis_title="Antal Idrottare",
        bargap=0.1,  
        xaxis=dict(tickmode="linear")  
    )
    
    return fig
@app.callback(
    Output("players-graph", "figure"),
    [Input("player-dropdown", "value")]
)
def palyer_graph(selected_sport):
    filtered_data = OS_df[OS_df["Sport"] == selected_sport] #filtrerar datan så jag bara får ut data från året jag väljer
    medals = filtered_data.groupby(["NOC","ID"]).size().reset_index(name="Players") #
    fig = px.histogram(medals, x="NOC", y="Players", barmode="stack", labels=f" Hur många spelare i läderna i{selected_sport}")
    fig.update_layout(
        xaxis_title="Länder",
        yaxis_title="Hur många Idrottare",
        bargap=0.1,  
        xaxis=dict(tickmode="linear")  
    )
    return fig
if __name__ == "__main__":
    app.run_server(debug=True)