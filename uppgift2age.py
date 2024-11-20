import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

OS_df = pd.read_csv(r"athlete_events.csv")

# Filtrera datasetet för att inkludera endast Basket, Judo och Fotboll
filtered_sports_df = OS_df[OS_df["Sport"].isin(["Basketball", "Judo", "Football"])]

app = Dash(__name__)

# Definiera layouten
app.layout = html.Div([
    html.H1("Åldersfördelning i Basket, Judo och Fotboll"),  
    html.Label("Välj sport"),  
    dcc.Dropdown(
        id="sport-dropdown",
        options=[
            {"label": "Basketball", "value": "Basketball"},
            {"label": "Judo", "value": "Judo"},
            {"label": "Football", "value": "Football"}
        ],  # Endast dessa sporter är valbara
        value="Basketball"  # Förvald sport
    ),
    dcc.Graph(id="age-distribution-graph")  # Diagram för åldersfördelning
])


@app.callback(
    Output("age-distribution-graph", "figure"),
    [Input("sport-dropdown", "value")]
)
def update_age_distribution(selected_sport):
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


if __name__ == "__main__":
    app.run_server(debug=True)