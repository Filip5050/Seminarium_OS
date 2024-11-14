import pandas as pd
import plotly.express as px
import hashlib as hl
from dash import Dash, dcc, html, Input, Output

OS_df = pd.read_csv(r"C:\Code\Seminarium_OS\athlete_events.csv")
OS_fr_df = OS_df[OS_df['Team'] == 'France'].copy()
def hash_name(name):
    return hl.sha256(name.encode()).hexdigest()
OS_fr_df['Name'] = OS_fr_df['Name'].apply(hash_name)
OS_fr_df_years = sorted(OS_fr_df["Year"].unique()) #Here we take out so we don't get bunch of duplicates of the year when we select

app = Dash(__name__) 
app.layout = html.Div([
    html.H1(children="How much medals France has gotten each year in OS"), 
    html.Hr(),
    html.Label("Select Year"),
   
    dcc.Dropdown(
        id="year-dropdown", 
        options=[{"label": str(year), "value": year}for year in OS_fr_df_years], 
        value=OS_fr_df_years[0] 
    ),
    dcc.Graph(id="graph")
])
@app.callback(
    Output("graph", "figure"),
    [Input("year-dropdown", "value")] 
)

def update_graph(selected_year):
    filtered_df = OS_fr_df[OS_fr_df["Year"] == selected_year]

    fig = px.histogram(filtered_df, x="Medal", y="ID", title=f"Medals they got year {selected_year}")
    return fig

if __name__ == "__main__":
    app.run(debug=True)

