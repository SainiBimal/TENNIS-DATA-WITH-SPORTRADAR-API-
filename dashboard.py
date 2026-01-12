import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# DATABASE
# =====================================================
from sqlalchemy import create_engine

@st.cache_resource
def get_engine():
    return create_engine("mysql+pymysql://root:root@localhost/game_analytics")


@st.cache_data(show_spinner=False) 
def load_data(query): 
    engine = get_engine() 
    return pd.read_sql(query, engine) 

@st.cache_data(show_spinner=False) 
def load_data_params(query, params): 
    engine = get_engine() 
    return pd.read_sql(query, engine, params=params)

# =====================================================
# STREAMLIT CONFIG
# =====================================================
st.set_page_config(page_title="Tennis Analytics Dashboard", layout="wide")
st.title("🎾 Tennis Analytics Dashboard")

# =====================================================
# SIDEBAR NAVIGATION
# =====================================================
st.sidebar.header("📊 Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["🏆 Competition Overview", "🌍 Venue & Complex Insights", "👤 Competitor Rankings"]
)

# Common helpers
def two_by_three_layout():
    rows = []
    rows.append(st.columns(3))
    rows.append(st.columns(3))
    return rows  # returns [ [col1,col2,col3], [col4,col5,col6] ]

def kpi_row(items):
    cols = st.columns(len(items))
    for i, (label, value) in enumerate(items):
        cols[i].metric(label, value)

# =====================================================
# PAGE 1: COMPETITION OVERVIEW (6 charts)
# =====================================================
if page == "🏆 Competition Overview":
    st.sidebar.header("🔎 Competition Filters")
    categories = load_data("SELECT DISTINCT category_name FROM categories ORDER BY category_name")["category_name"].tolist()
    types = load_data("SELECT DISTINCT type FROM competitions WHERE type IS NOT NULL ORDER BY type")["type"].tolist()
    genders = load_data("SELECT DISTINCT gender FROM competitions WHERE gender IS NOT NULL ORDER BY gender")["gender"].tolist()
    levels = load_data("SELECT DISTINCT level FROM competitions WHERE level IS NOT NULL ORDER BY level")["level"].tolist()

    selected_category = st.sidebar.selectbox("Category", ["All"] + categories)
    selected_type = st.sidebar.selectbox("Competition Type", ["All"] + types)
    selected_gender = st.sidebar.selectbox("Gender", ["All"] + genders)
    selected_level = st.sidebar.selectbox("Level", ["All"] + levels)
    name_search = st.sidebar.text_input("Search competition name")

    where_clause = "WHERE 1=1"
    if selected_category != "All":
        where_clause += f" AND c.category_name = '{selected_category}'"
    if selected_type != "All":
        where_clause += f" AND comp.type = '{selected_type}'"
    if selected_gender != "All":
        where_clause += f" AND comp.gender = '{selected_gender}'"
    if selected_level != "All":
        where_clause += f" AND comp.level = '{selected_level}'"
    if name_search.strip():
        where_clause += f" AND comp.competition_name LIKE '%{name_search.strip()}%'"

    # KPIs
    total_categories = load_data("SELECT COUNT(*) cnt FROM categories")["cnt"][0]
    total_competitions = load_data(f"SELECT COUNT(*) cnt FROM competitions comp JOIN categories c ON comp.category_id=c.category_id {where_clause}")["cnt"][0]
    top_level_events = load_data("SELECT COUNT(*) cnt FROM competitions WHERE parent_id IS NULL")["cnt"][0]
    distinct_types = load_data("SELECT COUNT(DISTINCT type) cnt FROM competitions WHERE type IS NOT NULL")["cnt"][0]
    distinct_genders = load_data("SELECT COUNT(DISTINCT gender) cnt FROM competitions WHERE gender IS NOT NULL")["cnt"][0]
    distinct_levels = load_data("SELECT COUNT(DISTINCT level) cnt FROM competitions WHERE level IS NOT NULL")["cnt"][0]

    kpi_row([
        ("Total Categories", total_categories),
        ("Filtered Competitions", total_competitions),
        ("Top-Level Events", top_level_events),
        ("Types", distinct_types),
        ("Genders", distinct_genders),
        ("Levels", distinct_levels)
    ])
    st.divider()

    rows = two_by_three_layout()

    # Chart 1: Competitions by Category (bar)
    df_category = load_data(f"""
        SELECT c.category_name, COUNT(*) total
        FROM competitions comp
        JOIN categories c ON comp.category_id = c.category_id
        {where_clause}
        GROUP BY c.category_name
        ORDER BY total DESC
    """)
    rows[0][0].plotly_chart(
        px.bar(df_category, x="category_name", y="total", title="Competitions by category", text_auto=True),
        use_container_width="stretch"
    )

    # Chart 2: Competition type distribution (pie)
    df_type = load_data(f"""
        SELECT comp.type, COUNT(*) total
        FROM competitions comp
        JOIN categories c ON comp.category_id = c.category_id
        {where_clause}
        GROUP BY comp.type
        ORDER BY total DESC
    """)
    rows[0][1].plotly_chart(
        px.pie(df_type, names="type", values="total", title="Competition type distribution"),
        use_container_width="stretch"
    )

    # Chart 3: Gender distribution (bar)
    df_gender = load_data(f"""
        SELECT comp.gender, COUNT(*) total
        FROM competitions comp
        JOIN categories c ON comp.category_id = c.category_id
        {where_clause}
        GROUP BY comp.gender
        ORDER BY total DESC
    """)
    rows[0][2].plotly_chart(
        px.bar(df_gender, x="gender", y="total", title="Gender distribution", text_auto=True),
        use_container_width="stretch"
    )

    # Chart 4: Category vs Type (stacked bar)
    df_cat_type = load_data(f"""
        SELECT c.category_name, comp.type, COUNT(*) total
        FROM competitions comp
        JOIN categories c ON comp.category_id = c.category_id
        {where_clause}
        GROUP BY c.category_name, comp.type
    """)
    fig_ct = px.bar(df_cat_type, x="category_name", y="total", color="type", title="Category vs type")
    rows[1][0].plotly_chart(fig_ct, use_container_width="stretch")

    # Chart 5: Parent-child hierarchy (sunburst)
    df_hier = load_data("""
        SELECT parent.competition_name AS parent_event,
               child.competition_name AS sub_event,
               child.gender,
               child.type
        FROM competitions child
        JOIN competitions parent ON child.parent_id = parent.competition_id
    """)
    if not df_hier.empty:
        fig_sb = px.sunburst(df_hier, path=["parent_event", "sub_event"], title="Competition hierarchy (parent → sub-event)")
        rows[1][1].plotly_chart(fig_sb, use_container_width="stretch")
    else:
        rows[1][1].write("No hierarchy data available.")

    # Chart 6: Heatmap type vs gender
    df_heat = load_data(f"""
        SELECT comp.type, comp.gender, COUNT(*) total
        FROM competitions comp
        JOIN categories c ON comp.category_id = c.category_id
        {where_clause}
        GROUP BY comp.type, comp.gender
    """)
    fig_heat = px.density_heatmap(df_heat, x="type", y="gender", z="total", title="Type vs gender heatmap", text_auto=True)
    rows[1][2].plotly_chart(fig_heat, use_container_width="stretch")

    st.subheader("Competition details (filtered)")
    df_comp = load_data(f"""
        SELECT c.category_name, comp.competition_name, comp.type, comp.gender, comp.level, comp.parent_id
        FROM competitions comp
        JOIN categories c ON comp.category_id = c.category_id
        {where_clause}
        ORDER BY comp.competition_name
    """)
    st.dataframe(df_comp, use_container_width="stretch")
    st.download_button("Download competitions CSV", df_comp.to_csv(index=False), "competitions_filtered.csv")

# =====================================================
# PAGE 2: VENUE & COMPLEX INSIGHTS (6 charts)
# =====================================================
elif page == "🌍 Venue & Complex Insights":
    st.sidebar.header("🔎 Venue Filters")

    venue_countries = load_data(
        "SELECT DISTINCT country_name FROM venues ORDER BY country_name"
    )["country_name"].tolist()

    complexes = load_data(
        "SELECT DISTINCT complex_name FROM complexes ORDER BY complex_name"
    )["complex_name"].tolist()

    timezones = load_data(
        "SELECT DISTINCT timezone FROM venues WHERE timezone IS NOT NULL ORDER BY timezone"
    )["timezone"].tolist()

    selected_country = st.sidebar.selectbox("Country", ["All"] + venue_countries)
    selected_complex = st.sidebar.selectbox("Complex", ["All"] + complexes)
    selected_timezone = st.sidebar.selectbox("Timezone", ["All"] + timezones)
    venue_name_search = st.sidebar.text_input("Search venue name")

    # -------------------------------------------------
    # Common WHERE clause (uses v + c aliases)
    # -------------------------------------------------
    venue_where = "WHERE 1=1"
    if selected_country != "All":
        venue_where += f" AND v.country_name = '{selected_country}'"
    if selected_complex != "All":
        venue_where += f" AND c.complex_name = '{selected_complex}'"
    if selected_timezone != "All":
        venue_where += f" AND v.timezone = '{selected_timezone}'"
    if venue_name_search.strip():
        venue_where += f" AND v.venue_name LIKE '%{venue_name_search.strip()}%'"

    # -------------------------------------------------
    # KPIs (FIXED: complexes JOIN added everywhere)
    # -------------------------------------------------
    total_complexes = load_data(
        "SELECT COUNT(*) cnt FROM complexes"
    )["cnt"][0]

    total_venues_filtered = load_data(f"""
        SELECT COUNT(*) cnt
        FROM venues v
        JOIN complexes c ON v.complex_id = c.complex_id
        {venue_where}
    """)["cnt"][0]

    countries_covered = load_data(f"""
        SELECT COUNT(DISTINCT v.country_name) cnt
        FROM venues v
        JOIN complexes c ON v.complex_id = c.complex_id
        {venue_where}
    """)["cnt"][0]

    distinct_timezones = load_data(f"""
        SELECT COUNT(DISTINCT v.timezone) cnt
        FROM venues v
        JOIN complexes c ON v.complex_id = c.complex_id
        {venue_where}
    """)["cnt"][0]

    complexes_with_multi_venues = load_data("""
        SELECT COUNT(*) cnt FROM (
            SELECT c.complex_id, COUNT(v.venue_id) AS total
            FROM complexes c
            JOIN venues v ON c.complex_id = v.complex_id
            GROUP BY c.complex_id
            HAVING COUNT(v.venue_id) > 1
        ) t
    """)["cnt"][0]

    distinct_complexes_filtered = load_data(f"""
        SELECT COUNT(DISTINCT c.complex_name) cnt
        FROM complexes c
        JOIN venues v ON c.complex_id = v.complex_id
        {venue_where}
    """)["cnt"][0]

    kpi_row([
        ("Total Complexes", total_complexes),
        ("Filtered Venues", total_venues_filtered),
        ("Countries (filtered)", countries_covered),
        ("Timezones (filtered)", distinct_timezones),
        ("Complexes with >1 venue", complexes_with_multi_venues),
        ("Distinct Complexes (filtered)", distinct_complexes_filtered),
    ])

    st.divider()

    rows = two_by_three_layout()


    # Chart 1: Venues by country (bar)
    df_country = load_data(f"""
        SELECT v.country_name, COUNT(*) total
        FROM venues v
        JOIN complexes c ON v.complex_id = c.complex_id
        {venue_where}
        GROUP BY v.country_name
        ORDER BY total DESC
    """)
    rows[0][0].plotly_chart(
        px.bar(df_country, x="country_name", y="total", title="Venues by country", text_auto=True),
        use_container_width="stretch"
    )

    # Chart 2: Venues per complex (bar)
    df_complex = load_data(f"""
        SELECT c.complex_name, COUNT(v.venue_id) total
        FROM complexes c
        JOIN venues v ON c.complex_id = v.complex_id
        {venue_where}
        GROUP BY c.complex_name
        ORDER BY total DESC
    """)
    rows[0][1].plotly_chart(
        px.bar(df_complex, x="complex_name", y="total", title="Venues per complex", text_auto=True),
        use_container_width="stretch"
    )

    # Chart 3: Timezone distribution (pie)
    df_tz = load_data(f"""
        SELECT v.timezone, COUNT(*) total
        FROM venues v
        JOIN complexes c ON v.complex_id = c.complex_id
        {venue_where}
        GROUP BY v.timezone
        ORDER BY total DESC
    """)
    rows[0][2].plotly_chart(
        px.pie(df_tz, names="timezone", values="total", title="Venue timezone distribution"),
        use_container_width="stretch"
    )

    # Chart 4: Country vs complex heatmap
    df_country_complex = load_data(f"""
        SELECT v.country_name, c.complex_name, COUNT(v.venue_id) total
        FROM venues v
        JOIN complexes c ON v.complex_id = c.complex_id
        {venue_where}
        GROUP BY v.country_name, c.complex_name
    """)
    fig_cc = px.density_heatmap(df_country_complex, x="country_name", y="complex_name", z="total", title="Country vs complex heatmap", text_auto=True)
    rows[1][0].plotly_chart(fig_cc, use_container_width="stretch")

    # Chart 5: Treemap country → complex
    df_country_complex = load_data(f"""
        SELECT
        TRIM(UPPER(v.country_name)) AS country_name,
        c.complex_name,
        COUNT(v.venue_id) AS total
        FROM venues v
        JOIN complexes c ON v.complex_id = c.complex_id
        {venue_where}
        AND v.country_name IS NOT NULL
        GROUP BY TRIM(UPPER(v.country_name)), c.complex_name
    """)

    if not df_country_complex.empty:
        fig_treemap = px.treemap(
          df_country_complex,
          path=["country_name", "complex_name"],
          values="total",
          title="Venue treemap: Country → Complex",
          branchvalues="total"
        )

        fig_treemap.update_layout(
          margin=dict(t=50, l=10, r=10, b=10)
        )

        rows[1][1].plotly_chart(fig_treemap, use_container_width=True)
    else:
        rows[1][1].write("No venue data available for treemap.")

    



    # Chart 6: Choropleth by country (if names align)
    try:
        fig_choro = px.choropleth(df_country, locations="country_name", locationmode="country names", color="total", title="Venues by country (choropleth)")
        rows[1][2].plotly_chart(fig_choro, use_container_width="stretch")
    except Exception:
        rows[1][2].write("Choropleth could not render due to country naming.")

    st.subheader("Venue details (filtered)")
    df_venue = load_data(f"""
        SELECT v.venue_name, v.country_name, v.timezone, c.complex_name
        FROM venues v
        JOIN complexes c ON v.complex_id = c.complex_id
        {venue_where}
        ORDER BY v.country_name, c.complex_name, v.venue_name
    """)
    st.dataframe(df_venue, use_container_width=True)
    st.download_button("Download venues CSV", df_venue.to_csv(index=False), "venues_filtered.csv")

# =====================================================
# PAGE 3: COMPETITOR RANKINGS (6 charts)
# =====================================================
elif page == "👤 Competitor Rankings":
    st.sidebar.header("🔎 Ranking Filters")

    countries = load_data("SELECT DISTINCT country FROM competitors ORDER BY country")["country"].tolist()
    selected_country = st.sidebar.selectbox("Country", ["All"] + countries)

    rank_min, rank_max = st.sidebar.slider("Rank range", min_value=1, max_value=500, value=(1, 100))
    movement_filter = st.sidebar.selectbox("Movement filter", ["All", "Stable (0)", "Positive (>0)", "Negative (<0)"])
    name_search = st.sidebar.text_input("Search competitor name")

    rank_where = "WHERE 1=1"
    rank_where += f" AND r.ranking BETWEEN {rank_min} AND {rank_max}"
    if selected_country != "All":
        rank_where += f" AND c.country = '{selected_country}'"
    if movement_filter == "Stable (0)":
        rank_where += " AND r.movement = 0"
    elif movement_filter == "Positive (>0)":
        rank_where += " AND r.movement > 0"
    elif movement_filter == "Negative (<0)":
        rank_where += " AND r.movement < 0"
    if name_search.strip():
        rank_where += f" AND c.name LIKE '%{name_search.strip()}%'"

    # KPIs
    players_filtered = load_data(f"SELECT COUNT(*) cnt FROM competitors c JOIN competitor_rankings r ON c.competitor_id=r.competitor_id {rank_where}")["cnt"][0]
    countries_total = load_data("SELECT COUNT(DISTINCT country) cnt FROM competitors")["cnt"][0]
    max_points_filtered = load_data(f"SELECT MAX(points) maxp FROM competitor_rankings r JOIN competitors c ON r.competitor_id=c.competitor_id {rank_where}")["maxp"][0]
    stable_ranks = load_data(f"SELECT COUNT(*) cnt FROM competitor_rankings r JOIN competitors c ON r.competitor_id=c.competitor_id {rank_where} AND r.movement=0")["cnt"][0]
    avg_points_filtered = load_data(f"SELECT AVG(points) avgp FROM competitor_rankings r JOIN competitors c ON r.competitor_id=c.competitor_id {rank_where}")["avgp"][0]

    kpi_row([
        ("Players (filtered)", players_filtered),
        ("Countries (total)", countries_total),
        ("Max points (filtered)", max_points_filtered if pd.notnull(max_points_filtered) else 0),
        ("Stable ranks (filtered)", stable_ranks),
        ("Avg points (filtered)", round(avg_points_filtered, 2) if pd.notnull(avg_points_filtered) else 0),
        ("Rank range", f"{rank_min}-{rank_max}")
    ])
    st.divider()

    rows = two_by_three_layout()

    # Base ranking DF
    df_rank = load_data(f"""
        SELECT c.name, c.country, r.ranking, r.points, r.movement
        FROM competitors c
        JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
        {rank_where}
        ORDER BY r.ranking
    """)

    # Chart 1: Top players by points (bar)
    rows[0][0].plotly_chart(
        px.bar(df_rank.head(10), x="name", y="points", title="Top players by points", text_auto=True),
        use_container_width=True
    )

    # Chart 2: Scatter ranking vs points (colored by country)
    rows[0][1].plotly_chart(
        px.scatter(df_rank, x="ranking", y="points", color="country", hover_name="name", title="Ranking vs points (by country)"),
        use_container_width="stretch"
    )

    # Chart 3: Player distribution by country (pie)
    df_country_share = load_data(f"""
        SELECT c.country, COUNT(*) total
        FROM competitors c
        JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
        {rank_where}
        GROUP BY c.country
        ORDER BY total DESC
        LIMIT 10
    """)
    rows[0][2].plotly_chart(
        px.pie(df_country_share, names="country", values="total", title="Player distribution by country (Top 10)"),
        use_container_width="stretch"
    )

    # Chart 4: Movement distribution (bar)
    df_move = df_rank.groupby("movement", as_index=False)["name"].count().rename(columns={"name": "count"})
    rows[1][0].plotly_chart(
        px.bar(df_move, x="movement", y="count", title="Rank movement distribution", text_auto=True),
        use_container_width="stretch"
    )

    # Chart 5: Max points by country (horizontal bar)
    df_max_country = load_data(f"""
        SELECT c.country, MAX(r.points) AS max_points
        FROM competitors c
        JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
        {rank_where}
        GROUP BY c.country
        ORDER BY max_points DESC
    """)
    rows[1][1].plotly_chart(
        px.bar(df_max_country, x="max_points", y="country", orientation="h", title="Max points by country", text_auto=True),
        use_container_width="stretch"
    )

    # Chart 6: Points distribution (histogram)
    rows[1][2].plotly_chart(
        px.histogram(df_rank, x="points", nbins=30, title="Points distribution"),
        use_container_width="stretch"
    )

    st.subheader("Rankings (filtered)")
    st.dataframe(df_rank, use_container_width=True)
    st.download_button("Download rankings CSV", df_rank.to_csv(index=False), "rankings_filtered.csv")

# =====================================================
# FOOTER
# =====================================================
st.caption("📊 Streamlit • MySQL • Plotly | SportRadar Tennis Analytics Project")
