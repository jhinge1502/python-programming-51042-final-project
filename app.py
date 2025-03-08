import pandas as pd
import plotly.express as px
import flask
from flask import render_template, send_file

# Dictionary mapping full state names to their abbreviations
us_state_abbrev = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
    'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
    'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
    'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
    'Wisconsin': 'WI', 'Wyoming': 'WY'
}

# Load the data from the Excel file (using the "inflation" sheet)
df = pd.read_excel("Real_Estate_Trends_USA.xlsx", sheet_name="inflation_data")

# If the "State" column contains full state names, convert them to abbreviations
if df["State"].str.len().max() > 2:
    df["State"] = df["State"].map(us_state_abbrev)

# Create the Flask app
app = flask.Flask(__name__)

@app.route("/")
def index():
    # 1) Create the choropleth map using the corrected column names
    fig_map = px.choropleth(
        df,
        locations="State",
        locationmode="USA-states",
        color="Inflation 2024 %",
        hover_data=["Inflation 2024 %", "Cumulative Inflation 2020-2024 %"],
        title="USA Map: Inflation 2024 and Cumulative Inflation 2020-2024",
        color_continuous_scale="Blues",
        scope="usa"
    )
    fig_map.update_layout(
        width=900,
        height=600,
        margin=dict(l=0, r=0, t=50, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig_map.update_traces(
        hovertemplate="<b>%{location}</b><br>"
                      "Inflation 2024 %: %{customdata[0]}<br>"
                      "Cumulative Inflation 2020-2024 %: %{customdata[1]}<br>"
                      "<extra></extra>"
    )
    map_html = fig_map.to_html(full_html=False)
    
    # Build the table with calculated columns, sorted by Potential Monthly Payoff descending.
    table_columns = [
        "State",
        "Typical Home Value as of 01/31/2024",
        "Down Payment",
        "Average Interest Rate (30 Yr Mortgage)",
        "Monthly Payment",
        "Average Rent",
        "Potential Monthly Payoff",
        "Average Rent Yield"
    ]
    df_table = df[table_columns].copy()
    df_table["Potential Monthly Payoff Numeric"] = pd.to_numeric(
        df_table["Potential Monthly Payoff"].astype(str).str.replace('[$,]', '', regex=True),
        errors="coerce"
    )
    df_table = df_table.sort_values(by="Potential Monthly Payoff Numeric", ascending=False)
    df_table.drop(columns=["Potential Monthly Payoff Numeric"], inplace=True)
    table_html = df_table.to_html(classes="table", index=False, border=0)
    
    # Create the bar charts for Home Price inflation in 2024 and overall price inflation from 2020 to 2024
    fig_bar1 = px.bar(
        df,
        x="State",
        y="Inflation 2024 %",
        title="Home Price Inflation 2024 by State",
        labels={"Inflation 2024 %": "Inflation 2024 (%)", "State": "State"}
    )
    fig_bar1.update_layout(
        margin=dict(l=0, r=0, t=50, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    bar1_html = fig_bar1.to_html(full_html=False)
    
    fig_bar2 = px.bar(
        df,
        x="State",
        y="Cumulative Inflation 2020-2024 %",
        title="Cumulative Home Price Inflation (2020-2024) by State",
        labels={"Cumulative Inflation 2020-2024 %": "Cumulative Inflation 2020-2024 (%)", "State": "State"}
    )
    fig_bar2.update_layout(
        margin=dict(l=0, r=0, t=50, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    bar2_html = fig_bar2.to_html(full_html=False)
    
    return render_template("index.html",
                           map_html=map_html,
                           table_html=table_html,
                           bar1_html=bar1_html,
                           bar2_html=bar2_html)

@app.route("/download")
def download():
    return send_file("Real_Estate_Trends_USA.xlsx", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
