import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Initialize the app
app = dash.Dash(__name__)

# Load the data from your dataset (replace 'updatedata.csv' with the actual path to your CSV file)
df = pd.read_csv('updatedata.csv')

# Check the first few rows to understand the structure
print(df.head())

# Layout
app.layout = html.Div([
    html.H1("Education Analytics Dashboard"),

    # Dropdown for Nomination Year
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': year, 'value': year} for year in df['Nomination Year'].unique()],
        value=df['Nomination Year'].max(),  # Default year set to the latest
        style={'width': '40%'}
    ),
    
    # Toggle switch for chart type selection
    dcc.RadioItems(
        id='chart-type-switch',
        options=[
            {'label': 'Bar Chart (Rank by Country)', 'value': 'bar'},
            {'label': 'Scatter Plot (Rank vs Rating)', 'value': 'scatter'},
            {'label': 'Line Chart (Rating Trend by Year)', 'value': 'line'},
            {'label': 'Pie Chart (Rating Distribution by Country)', 'value': 'pie'},
            {'label': 'Histogram (Rating Frequency)', 'value': 'histogram'},
            {'label': 'Bar Chart (Rating Comparison by Country)', 'value': 'bar_rating'},
            {'label': 'Line Chart (Rank Trend)', 'value': 'line_rank'},
            {'label': 'Box Plot (Rating Distribution)', 'value': 'box'}
        ],
        value='bar',  # Default chart type
        labelStyle={'display': 'inline-block'}
    ),

    # Graph to display the selected chart
    dcc.Graph(id='chart')
])

# Callbacks
@app.callback(
    Output('chart', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('chart-type-switch', 'value')]
)
def update_graph(selected_year, chart_type):
    # Filter the data for the selected year
    filtered_df = df[df['Nomination Year'] == selected_year]

    # Bar Chart - Rank by Country
    if chart_type == 'bar':
        fig = px.bar(filtered_df, x='Country', y='Rank', color='Country', 
                     title=f"Rank by Country for {selected_year}")
    
    # Scatter Plot - Rank vs Rating
    elif chart_type == 'scatter':
        fig = px.scatter(filtered_df, x='Rank', y='Rating', color='Country',
                         title=f"Rank vs Rating for {selected_year}")
    
    # Line Chart - Rating Trend by Year
    elif chart_type == 'line':
        fig = px.line(filtered_df, x='Nomination Year', y='Rating', color='Country',
                      title=f"Rating Trend for {selected_year}")
    
    # Pie Chart - Rating Distribution by Country
    elif chart_type == 'pie':
        rating_category = ['Good' if x >= 90 else 'Average' if x >= 80 else 'Poor' for x in filtered_df['Rating']]
        filtered_df['Rating Category'] = rating_category
        fig = px.pie(filtered_df, names='Rating Category', title=f"Rating Distribution for {selected_year}")
    
    # Histogram - Rating Frequency
    elif chart_type == 'histogram':
        fig = px.histogram(filtered_df, x='Rating', nbins=10, title=f"Rating Frequency for {selected_year}")
    
    # Bar Chart - Rating Comparison by Country
    elif chart_type == 'bar_rating':
        fig = px.bar(filtered_df, x='Country', y='Rating', color='Country', title=f"Rating Comparison for {selected_year}")
    
    # Line Chart - Rank Trend
    elif chart_type == 'line_rank':
        fig = px.line(filtered_df, x='Nomination Year', y='Rank', color='Country', 
                      title=f"Rank Trend for {selected_year}")
    
    # Box Plot - Rating Distribution
    elif chart_type == 'box':
        fig = px.box(filtered_df, y='Rating', title=f"Rating Distribution for {selected_year}")

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
