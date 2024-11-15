import pandas as pd
import plotly.express as px
import hashlib as hl
from dash import Dash, dcc, html, Input, Output

OS_df = pd.read_csv(r"C:\Code\Seminarium_OS\athlete_events.csv")
OS_fr_df = OS_df[OS_df['Team'] == 'France'].copy() #Skapar en variabel som visar all statistik för laget frankrike
def hash_name(name):
    return hl.sha256(name.encode()).hexdigest()
OS_fr_df['Name'] = OS_fr_df['Name'].apply(hash_name) #Här anonymiserar alla spelare i frankrike lager

#Förberedande för första dashboarden
OS_fr_df_years = sorted(OS_fr_df["Year"].unique()) #Sorterar åren i ordning och tar bort alla kopior så jag inte kan välja samma årtal flera gånger i dashboarden

#Förberedande för andra dashboarden
medals_by_sport = OS_fr_df.groupby(["Sport"]).size().reset_index(name="medals") # Gruppera medaljerna efter sport och räkna antalet medaljer för varje sport
sorted_sports = medals_by_sport.sort_values("medals", ascending=False)

#Förberendade för tredje dashboarde 
medals_per_OS = OS_fr_df.groupby("Games").size().reset_index(name="Medals")
medals_per_OS.head()

#Förberedande för fjärde dashboarden
ages_sort_OS = OS_fr_df["Age"].dropna().sort_values()




#initierar dashboarden
app = Dash(__name__)
#Skapar en layout som får en titel
app.layout = html.Div([
    html.H1(children="Statistik för Frankrike i OS"),
    html.Hr(),
    
    #Första dashboarfen
    html.Div([
        html.H2(children="Medals by Year"), #Text som kommer visas över dashboarden
        html.Label("Select Year"),
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
            figure=px.bar(sorted_sports, x="Sport", y="medals")
        )
    ]),
    html.Hr(),

    #Tredje dashboarden
    html.Div([
        html.H2(children="Hur många medaljer för åren"),
    dcc.Graph(
        figure=px.bar(medals_per_OS,x="Games", y="Medals")
    )
    ]),
    html.Hr(),
    html.Div([
        html.H2(children="Histogram över åldrarna"),
        dcc.Graph(
            figure=px.histogram(ages_sort_OS)
        )
    ])
])

#Denna callbacken kopplas med min dropdown jag gjorde innan i dashboard 1
#när year-dropwdown uppdateras och värdet ändras så kommer min figure att uppdateras där graph id finns
@app.callback(
    Output("graph", "figure"),
    [Input("year-dropdown", "value")] 
)
#Funktionen som skapar grafen som kommer synas i dashboard 1.
def update_graph(selected_year):
    filtered_df = OS_fr_df[OS_fr_df["Year"] == selected_year]

    fig = px.histogram(filtered_df, x="Medal", y="ID", title=f"Medals they got year {selected_year}")
    return fig

if __name__ == "__main__":
    app.run(debug=True)

