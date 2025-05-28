import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

# Load the dataset
df = pd.read_csv("cleaned_sales_data.csv")

# Create your figures

fig1 = px.line(df.groupby("Year")["Energy Sale (GWh)"].sum().reset_index(),
               x="Year", y="Energy Sale (GWh)",
               title="Total Energy Sales in India Over Time",
               markers=True)
fig1.update_traces(line=dict(width=3), marker=dict(size=8))

fig2 = px.treemap(df, path=['State'], values='Energy Sale (GWh)'),
fig2 = px.treemap(df, path=['State'], values='Energy Sale (GWh)',
                  title="Energy Sales Distribution by State")

fig3 = px.sunburst(df, path=['State', 'Consumer Category'], values='Energy Sale (GWh)',
                   title="Sunburst of Energy Sales by State and Consumer Category")

category_data = df.groupby("Consumer Category")["Energy Sale (GWh)"].sum().reset_index()
fig4 = px.pie(category_data, names='Consumer Category', values='Energy Sale (GWh)',
              title='Share of Energy Sales by Consumer Category',
              hole=0.4)

top_states = df.groupby("State")["Energy Sale (GWh)"].sum().nlargest(10).reset_index()
fig5 = px.bar(top_states, x='State', y='Energy Sale (GWh)',
              title='Top 10 States by Total Energy Sales',
              text_auto=True)

fig6 = px.bar(df, x='State', y='Energy Sale (GWh)', color='Consumer Category',
              animation_frame='Year', animation_group='State',
              title='Animated Energy Sales by State and Consumer Category Over Years',
              range_y=[0, df["Energy Sale (GWh)"].max()])

# Function to generate category trend plot (for first category just to show example)
def plot_category_trend(category):
    filtered = df[df["Consumer Category"] == category]
    grouped = filtered.groupby("Year")["Energy Sale (GWh)"].sum().reset_index()
    return px.line(grouped, x="Year", y="Energy Sale (GWh)",
                   title=f"Energy Sale Trend Over Time for {category}", markers=True)

fig7 = plot_category_trend(df['Consumer Category'].unique()[0])


# Now save all figures into one HTML file with tabs

from plotly.subplots import make_subplots
import plotly.offline as offline

html_str = """
<html>
<head>
<title>Energy Sales Dashboard</title>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<style>
  body { font-family: Arial, sans-serif; margin: 20px;}
  h1 { text-align: center; }
  .plot-container { margin-bottom: 60px; }
</style>
</head>
<body>
<h1>Energy Sales Dashboard</h1>
"""

figures = [fig1, fig2, fig3, fig4, fig5, fig6, fig7]
titles = [
    "Total Energy Sales in India Over Time",
    "Energy Sales Distribution by State",
    "Sunburst of Energy Sales by State and Consumer Category",
    "Share of Energy Sales by Consumer Category",
    "Top 10 States by Total Energy Sales",
    "Animated Energy Sales by State and Consumer Category Over Years",
    f"Energy Sale Trend Over Time for {df['Consumer Category'].unique()[0]}"
]

for i, fig in enumerate(figures):
    div_id = f"plot{i}"
    inner_html = fig.to_html(include_plotlyjs=False, full_html=False, div_id=div_id)
    html_str += f'<div class="plot-container"><h2>{titles[i]}</h2>{inner_html}</div>'

html_str += """
</body>
</html>
"""

# Save to file
with open("energy_sales_dashboard.html", "w") as f:
    f.write(html_str)

print("Dashboard saved to energy_sales_dashboard.html")
