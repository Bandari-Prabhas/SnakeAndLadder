import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
import os
from collections import Counter

st.set_page_config(page_title="Geographic Map", page_icon="🌍", layout="wide")

def load_logs():
    events = []
    if os.path.exists('logs/honeypot.log'):
        with open('logs/honeypot.log', 'r') as f:
            for line in f:
                try:
                    events.append(json.loads(line.strip()))
                except:
                    continue
    
    if events:
        df = pd.DataFrame(events)
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    return pd.DataFrame()

# Sample country mapping (in production, use a GeoIP database)
def get_country_from_ip(ip):
    """Mock function - in production use GeoIP2 or similar"""
    # Common country codes for demonstration
    ip_ranges = {
        '185': 'Russia',
        '192': 'United States',
        '203': 'China',
        '91': 'India',
        '45': 'Brazil',
        '103': 'Singapore',
        '80': 'Germany',
        '151': 'Australia',
        '41': 'Switzerland',
        '195': 'United Kingdom'
    }
    
    prefix = ip.split('.')[0]
    return ip_ranges.get(prefix, 'Unknown')

# Header
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <h1 style='color: #a78bfa; font-size: 2.5em;'>🌍 Geographic Attack Distribution</h1>
    <p style='color: #9ca3af;'>Visualize attack sources from around the world</p>
</div>
""", unsafe_allow_html=True)

df = load_logs()

if df.empty:
    st.warning("⚠️ No data available. Start the honeypot services first.")
    st.stop()

# Add country information
if 'source_ip' in df.columns:
    df['country'] = df['source_ip'].apply(get_country_from_ip)
else:
    st.error("No source IP data available")
    st.stop()

# Country statistics
country_stats = df['country'].value_counts()

# Metrics
st.markdown("### 🌐 Global Statistics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Countries Detected", len(country_stats))

with col2:
    st.metric("Total Attacks", len(df))

with col3:
    most_active = country_stats.index[0] if not country_stats.empty else "N/A"
    st.metric("Most Active Country", most_active)

with col4:
    top_percentage = (country_stats.iloc[0] / len(df) * 100) if not country_stats.empty else 0
    st.metric("Top Country %", f"{top_percentage:.1f}%")

st.markdown("---")

# World map (simplified choropleth)
st.markdown("### 🗺️ Attack Heatmap by Country")

# Country coordinates (sample data)
country_coords = {
    'United States': {'lat': 37.0902, 'lon': -95.7129, 'code': 'USA'},
    'China': {'lat': 35.8617, 'lon': 104.1954, 'code': 'CHN'},
    'Russia': {'lat': 61.5240, 'lon': 105.3188, 'code': 'RUS'},
    'India': {'lat': 20.5937, 'lon': 78.9629, 'code': 'IND'},
    'Brazil': {'lat': -14.2350, 'lon': -51.9253, 'code': 'BRA'},
    'Germany': {'lat': 51.1657, 'lon': 10.4515, 'code': 'DEU'},
    'United Kingdom': {'lat': 55.3781, 'lon': -3.4360, 'code': 'GBR'},
    'Singapore': {'lat': 1.3521, 'lon': 103.8198, 'code': 'SGP'},
    'Australia': {'lat': -25.2744, 'lon': 133.7751, 'code': 'AUS'},
    'Switzerland': {'lat': 46.8182, 'lon': 8.2275, 'code': 'CHE'}
}

# Prepare map data
map_data = []
for country, count in country_stats.items():
    if country in country_coords:
        map_data.append({
            'country': country,
            'lat': country_coords[country]['lat'],
            'lon': country_coords[country]['lon'],
            'attacks': count,
            'code': country_coords[country]['code']
        })
    else:
        # Fallback: place "Unknown" attacks at (0,0)
        if country == "Unknown":
            map_data.append({
                'country': "Unknown",
                'lat': 0,
                'lon': 0,
                'attacks': count,
                'code': "UNK"
            })

map_df = pd.DataFrame(map_data)


if not map_df.empty:
    # Create scatter map
    fig = go.Figure()
    
    # Add markers for each country
    fig.add_trace(go.Scattergeo(
        lon=map_df['lon'],
        lat=map_df['lat'],
        text=map_df['country'] + '<br>Attacks: ' + map_df['attacks'].astype(str),
        mode='markers+text',
        marker=dict(
            size=map_df['attacks'] / map_df['attacks'].max() * 50 + 10,
            color=map_df['attacks'],
            colorscale='Reds',
            showscale=True,
            colorbar=dict(title="Attacks"),
            line=dict(width=1, color='white')
        ),
        textposition='top center',
        textfont=dict(size=10, color='white'),
        hoverinfo='text'
    ))
    
    fig.update_layout(
        geo=dict(
            projection_type='natural earth',
            showland=True,
            landcolor='rgb(30, 30, 30)',
            coastlinecolor='rgb(100, 100, 100)',
            showocean=True,
            oceancolor='rgb(10, 10, 30)',
            showcountries=True,
            countrycolor='rgb(60, 60, 60)'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e5e7eb'),
        height=600,
        title='Global Attack Distribution'
    )
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No geographic data available for mapping")

st.markdown("---")

# Country breakdown
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Top 15 Attacking Countries")
    
    top_countries = country_stats.head(15)
    
    fig = go.Figure(go.Bar(
        y=top_countries.index,
        x=top_countries.values,
        orientation='h',
        marker=dict(
            color=top_countries.values,
            colorscale='Reds',
            showscale=False
        ),
        text=top_countries.values,
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Attacks: %{x}<extra></extra>'
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e5e7eb'),
        xaxis=dict(showgrid=True, gridcolor='rgba(75, 85, 99, 0.3)'),
        yaxis=dict(autorange="reversed"),
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 🥧 Attack Distribution Pie Chart")
    
    # Group smaller countries into "Others"
    top_10 = country_stats.head(10)
    others = country_stats[10:].sum()
    
    if others > 0:
        plot_data = pd.concat([top_10, pd.Series({'Others': others})])
    else:
        plot_data = top_10
    
    colors = ['#ef4444', '#f59e0b', '#eab308', '#84cc16', '#22c55e',
              '#14b8a6', '#06b6d4', '#3b82f6', '#6366f1', '#8b5cf6', '#d946ef']
    
    fig = go.Figure(data=[go.Pie(
        labels=plot_data.index,
        values=plot_data.values,
        hole=0.4,
        marker=dict(colors=colors),
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>Attacks: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e5e7eb'),
        height=500,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Detailed country table
st.markdown("### 📋 Detailed Country Statistics")

country_details = pd.DataFrame({
    'Rank': range(1, len(country_stats) + 1),
    'Country': country_stats.index,
    'Total Attacks': country_stats.values,
    'Percentage': (country_stats.values / len(df) * 100).round(2),
    'Unique IPs': [df[df['country'] == country]['source_ip'].nunique() for country in country_stats.index]
})

st.dataframe(
    country_details,
    use_container_width=True,
    height=400
)

# Regional analysis
st.markdown("---")
st.markdown("### 🌏 Regional Analysis")

# Define regions (simplified)
regions = {
    'Asia': ['China', 'India', 'Singapore'],
    'Europe': ['Russia', 'Germany', 'United Kingdom', 'Switzerland'],
    'Americas': ['United States', 'Brazil'],
    'Oceania': ['Australia']
}

region_counts = {}
for region, countries in regions.items():
    count = sum(country_stats.get(country, 0) for country in countries)
    region_counts[region] = count

if region_counts:
    col1, col2 = st.columns(2)
    
    with col1:
        # Regional bar chart
        region_df = pd.DataFrame({
            'Region': region_counts.keys(),
            'Attacks': region_counts.values()
        }).sort_values('Attacks', ascending=False)
        
        fig = go.Figure(go.Bar(
            x=region_df['Region'],
            y=region_df['Attacks'],
            marker=dict(
                color=region_df['Attacks'],
                colorscale='Viridis',
                showscale=True
            ),
            text=region_df['Attacks'],
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Attacks by Region",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e5e7eb'),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Regional metrics
        for region, count in sorted(region_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(df) * 100) if len(df) > 0 else 0
            st.metric(f"{region}", f"{count:,} attacks", f"{percentage:.1f}%")

# Export options
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📥 Export Country Data", use_container_width=True):
        csv = country_details.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"country_stats_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

with col2:
    if st.button("🗺️ Export Map Data", use_container_width=True):
        if not map_df.empty:
            csv = map_df.to_csv(index=False)
            st.download_button(
                label="Download Map Data",
                data=csv,
                file_name=f"map_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

with col3:
    if st.button("🔄 Refresh Map", use_container_width=True):
        st.rerun()