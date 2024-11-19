import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

OS_df = pd.read_csv(r"C:\Code\Seminarium_OS\athlete_events.csv")
Filtered_os_df = OS_df[["Sport", "NOC", "Medal"]]  #filtrerar datan så jag bara får ut de nödvändiga kolumnerna som behövs i uppgift 2
app = Dash(__name__) #initiserar Dash
app.layout = html.Div([
    html.H1("Medalj fördelningen mellan länderna i Basket och Judo"), #Ger dash datan en titel
    html.Label("Välj sport"),
    dcc.Dropdown( #Skapar en dropdown som gör man kan välja vilka sporter vi ska använda
        id="sport-dropdown", #skapar en id som används till inputen i callback funktionen senare
        #De olika valen som går att intergrera med
        options=[
            {"label": "Basketball", "value": "Basketball"},
            {"label": "Judo", "value": "Judo"},
            {"label": "Football", "value": "Football"},
        ],
        value="Basketball" #sporten som visas när man startar dashen
    ),
    dcc.Graph(id="medal-graph")
])
#Funktionen som tillkallas när man väljer en av alternativen i dropdownen
@app.callback(
    Output("medal-graph", "figure"),
    [Input("sport-dropdown", "value")]
)
def sport_graph(selected_sport):
    filtered_data = Filtered_os_df[Filtered_os_df["Sport"] == selected_sport] #filtrerar datan så jag bara får ut data från året jag väljer
    medals = filtered_data.groupby(["NOC","Medal"]).size().reset_index(name="Medaljer") #
    fig = px.histogram(medals, x="NOC", y="Medaljer", barmode="stack",  color="Medal", color_discrete_map={
            "Gold": "yellow", 
            "Silver": "grey", 
            "Bronze": "brown",}, 
        labels=f" Medaljer sporterna har fått i {selected_sport}")
    return fig
if __name__ == "__main__":
    app.run_server(debug=True)