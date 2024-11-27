import pandas as pd
import plotly.express as px
import hashlib as hl
from dash import Dash, dcc, html, Input, Output
import os


file_path = os.path.join(os.path.dirname(__file__), "athlete_events.csv")
OS_df = pd.read_csv(file_path)
OS_fr_df = OS_df[OS_df['NOC'] == 'FRA'].copy() #Skapar en variabel som visar all statistik för laget frankrike

def hash_name(name):
    return hl.sha256(name.encode()).hexdigest()
OS_fr_df['Name'] = OS_fr_df['Name'].apply(hash_name) #Här anonymiserar alla spelare i frankrike lager

#Förberedande för första dashboarden
OS_fr_df_years = sorted(OS_fr_df["Year"].unique()) #Sorterar åren i ordning och tar bort alla kopior så jag inte kan välja samma årtal flera gånger i dashboarden

#Förberedande för andra dashboarden
medals_data = OS_fr_df[OS_fr_df['Medal'].notna()]
medals_data = medals_data.drop_duplicates(subset=["Event", "Games", "Medal"])
medals_by_sport = medals_data.groupby(["Sport"]).size().reset_index(name="medals") # Gruppera medaljerna efter sport och räkna antalet medaljer för varje sport
sorted_sports = medals_by_sport.sort_values("medals", ascending=False)

#Förberendade för tredje dashboarde 
medals_per_OS = medals_data.groupby("Games").size().reset_index(name="Medals") #tar samma dataframe från förra dashboarden men grupperar istället "Games" istället


#Förberedande för fjärde dashboarden
ages_sort_OS = OS_fr_df["Age"].dropna().sort_values()

#Förberedande för femte dashboarden
cities = OS_fr_df["City"].dropna().unique()
cities_sorted = sorted(cities)

#Förberedande för sjätte dashboarden
gender_counts = OS_fr_df.drop_duplicates(subset=["ID"]).groupby("Sex").size().reset_index(name="players")

#Förberedande för sjunde dashboarden
sport = OS_fr_df["Sport"].dropna().unique()
sport_sorted = sorted(sport)




#initierar dashboarden
app = Dash(__name__)
server = app.server 
#Skapar en layout som får en titel
app.layout = html.Div([

    html.H1(children="Statistik för Frankrike i OS"),
    html.Hr(),
    
    #Första dashboarfen
    html.Div([
        html.H2(children="Medaljen för åren"), #Text som kommer visas över dashboarden
        html.Label("Välj år"),
        dcc.Dropdown( #Här används dropdown som gör att man kan intergrera med dashboarden
            id="year-dropdown", #Id är något jag kommer komma tillbaka till senare när jag kodar min callback funktion
            options=[{"label": str(year), "value": year} for year in OS_fr_df_years], #Här är de olika valen man kan intergrera med och vilket är de olika åren som finns is csv filen
            value=OS_fr_df_years[0] #Här sätts första året som default värdet när man går in i dashboarden 
        ),
        dcc.Graph(id="graph") #dcc.graph är det som bygger själva grafen som visas men här lägger jag bara in ett id vilket gör så att jag kan koda den senare 
    ]),
    html.Hr(),
    
    #Andra dashboarden
    html.Div([
        html.H2(children="Medaljer i sporten"),
        #Här skapar jag en barplot som har Sport som x värde och medals som y värde.
        dcc.Graph(
            figure=px.bar(sorted_sports, x="Sport", y="medals", color="Sport")
        )
    ]),
    html.Hr(),

    #Tredje dashboarden
    html.Div([
        html.H2(children="Hur många medaljer för åren"),
    dcc.Graph(
        figure=px.bar(medals_per_OS,x="Games", y="Medals", color="Games")
    )
    ]),
    html.Hr(),
    #Fjärde dashboarden
    html.Div([
        html.H2(children="Histogram över åldrarna"),
        dcc.Graph(
            figure=px.histogram(ages_sort_OS, x="Age", color="Age")
        )
    ]),
    html.Hr(),
    #femte dashboarden
    html.Div([
        html.H2(children="Hur mycket medaljer frankrike fick i de olika städerna"),
        html.Label("Välj stad"),
        dcc.Dropdown(
            id="city-dropdown",
            options=[{"label":str(city),"value": city} for city in cities_sorted],
            value=cities_sorted[0]
        ),
        dcc.Graph(id="city-graph")
    ]),
    html.Hr(),
    #sjätte dashboarden
    html.Div([
        html.H2(children="Hur många kvinnor och män var med och tävlade för frankrike i OS"),
        dcc.Graph(
            figure=px.histogram(gender_counts, x="Sex", y="players", color="Sex")
        )
    ]),
    html.Hr(),
    #sjunde dashboarden
    html.Div([
        html.H2(children="Spelarnas längd inom en sport"),
        html.Label("Välj sport"),
        dcc.Dropdown(
            id="7th-dropdown",
            options=[{"label":str(sport),"value": sport} for sport in sport],
            value=sport[0]
        ),
        dcc.Graph(id="sport-graph")
        ])
])

#Denna callbacken kopplas med min dropdown jag gjorde innan i dashboard 1
#när year-dropwdown uppdateras och värdet ändras så kommer min figure att uppdateras 
@app.callback(
    Output("graph", "figure"),
    [Input("year-dropdown", "value")] 
)
#Funktionen som skapar grafen som kommer synas i dashboard 1.
def update_graph(selected_year):
    filtered_df = OS_fr_df[OS_fr_df["Year"] == selected_year] #filtrerar datan så jag bara får ut data från året jag väljer
    medals = filtered_df.groupby("Medal").size().reset_index(name="number of medals") #Grupperar de olika medaljen för de olika typerna vilket behövs föra att skapa histogramen och ändrar indexet namn till number of medals
    fig = px.histogram(medals, x="Medal", y="number of medals", color= "Medal", color_discrete_map={
            "Gold": "yellow", 
            "Silver": "grey", 
            "Bronze": "brown",}, 
        title=f"Medals they got year {selected_year}")
    #fixar layouten och ändrar namnen på x linjen och y linjen
    fig.update_layout(
        xaxis_title="Typ av medalj",
        yaxis_title="Antal medaljer",
        bargap=0.1,  
        xaxis=dict(tickmode="linear")  
    )
    return fig

#callback för femte dashboarden
@app.callback(
    Output("city-graph", "figure"),
    [Input("city-dropdown", "value")]
)


def update_city(selected_city):
    filtered_city = OS_fr_df[OS_fr_df["City"] == selected_city]
    medals = filtered_city.groupby("Medal").size().reset_index(name="number of medals") #Grupperar de olika medaljen för de olika typerna vilket behövs föra att skapa histogramen och ändrar indexet namn till number of medals
    fig = px.bar(medals, x="Medal", y="number of medals",  color="Medal", color_discrete_map={ # Ger olika medaljerna passande färg
            "Gold": "yellow", 
            "Silver": "grey", 
            "Bronze": "brown",},
        title=f"Medaljer i {selected_city}")
    fig.update_layout(
        xaxis_title="typ av medalj",
        yaxis_title="antal medaljer",
        bargap=0.1,  
        xaxis=dict(tickmode="linear")  
    )
    return fig

#callback och funktion för sjunde dashboarden
@app.callback(
    Output("sport-graph", "figure"),
    [Input("7th-dropdown", "value")]
)
#Funktion för sjunde dashboarden
def update_height(selected_sport): 
    #filtrera datan för valda sporten
    filtered_sport = OS_fr_df[OS_fr_df["Sport"] == selected_sport]
    #Förberedande för sjunde dashboarden
    fig = px.histogram(filtered_sport, x="Height", color="Height",  barmode="group", nbins=10, title=f"Höjden på spelarna i {selected_sport}")
    fig.update_layout(
        xaxis_title="Längd",
        yaxis_title="Antal Idrottare",
        bargap=0.1,  
        xaxis=dict(tickmode="linear")  
    )                   
    
    
    return fig

if __name__ == "__main__":
    app.run(debug=True)

