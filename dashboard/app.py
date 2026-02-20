import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import joblib
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from io import BytesIO

from src.config import PROCESSED_DATA_PATH, MODEL_DIR

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="PricingAI", layout="wide")
st.title("📊 Pricing Sensitivity & Revenue Optimization Analyzer")


# ---------------------------
# LOAD DATA
# ---------------------------
df = pd.read_csv(PROCESSED_DATA_PATH)
categories = df["product_category"].unique()

# ---------------------------
# SIDEBAR
# ---------------------------
category = st.sidebar.selectbox("Category", categories)
cost_ratio = st.sidebar.slider("Cost Ratio", 0.1, 0.9, 0.6)
scenario_price = st.sidebar.number_input("Scenario Price", min_value=0.0, value=0.0)

cat_df = df[df["product_category"] == category]
avg_price = cat_df["price_per_unit"].mean()

user_price = st.slider(
    "Adjust Price",
    float(avg_price * 0.5),
    float(avg_price * 2.0),
    float(avg_price)
)

# ---------------------------
# LOAD MODEL
# ---------------------------
model = joblib.load(os.path.join(MODEL_DIR, f"{category}_model.pkl"))
alpha = model.params["const"]
beta = model.params["log_price"]

conf_int = model.conf_int().loc["log_price"]
beta_lower = conf_int[0]
beta_upper = conf_int[1]

# ---------------------------
# SIMULATION
# ---------------------------
price_range = np.linspace(avg_price * 0.5, avg_price * 2.0, 150)

revenues = []
profits = []
profits_lower = []
profits_upper = []

for P in price_range:
    Q = np.exp(alpha) * (P ** beta)
    Q_lower = np.exp(alpha) * (P ** beta_lower)
    Q_upper = np.exp(alpha) * (P ** beta_upper)

    revenues.append(P * Q)
    profits.append((P - P * cost_ratio) * Q)
    profits_lower.append((P - P * cost_ratio) * Q_lower)
    profits_upper.append((P - P * cost_ratio) * Q_upper)

profits = np.round(profits, 2)
profits_lower = np.round(profits_lower, 2)
profits_upper = np.round(profits_upper, 2)
revenues = np.round(revenues, 2)

optimal_index = np.argmax(profits)
optimal_price = round(price_range[optimal_index], 2)
optimal_profit = profits[optimal_index]

# Current
current_index = min(range(len(price_range)), key=lambda i: abs(price_range[i] - user_price))
current_profit = profits[current_index]
current_revenue = revenues[current_index]

# Scenario
if scenario_price > 0:
    Q_scenario = np.exp(alpha) * (scenario_price ** beta)
    scenario_profit = round((scenario_price - scenario_price * cost_ratio) * Q_scenario, 2)
else:
    scenario_profit = None

# ---------------------------
# KPI SECTION
# ---------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Current Profit", f"${current_profit:,.2f}")
col2.metric("Optimal Profit", f"${optimal_profit:,.2f}")
col3.metric("Optimal Price", f"${optimal_price:,.2f}")


# ---------------------------
# PREMIUM SaaS PLOT
# ---------------------------

fig = go.Figure()

# --- Confidence Band ---
fig.add_trace(go.Scatter(
    x=price_range,
    y=profits_upper,
    line=dict(width=0),
    showlegend=False,
    hoverinfo="skip"
))

fig.add_trace(go.Scatter(
    x=price_range,
    y=profits_lower,
    fill="tonexty",
    fillcolor="rgba(46, 204, 113, 0.12)",  # soft green
    line=dict(width=0),
    name="Confidence Interval",
    hoverinfo="skip"
))

# --- Glow Effect (Layer 1 - thicker transparent line) ---
fig.add_trace(go.Scatter(
    x=price_range,
    y=profits,
    line=dict(width=10, color="rgba(0,191,255,0.15)"),
    hoverinfo="skip",
    showlegend=False
))

# --- Main Profit Curve ---
fig.add_trace(go.Scatter(
    x=price_range,
    y=profits,
    name="Profit",
    line=dict(width=3, color="#00BFFF"),
    hovertemplate=
        "Price: $%{x:.2f}<br>" +
        "Profit: $%{y:.2f}<extra></extra>"
))

# --- Optimal Zone Highlight ---
optimal_band_width = optimal_price * 0.08  # 8% zone around optimal

fig.add_vrect(
    x0=optimal_price - optimal_band_width,
    x1=optimal_price + optimal_band_width,
    fillcolor="rgba(255, 215, 0, 0.08)",  # subtle gold
    layer="below",
    line_width=0,
    annotation_text="Optimal Zone",
    annotation_position="top left"
)

# --- Optimal Line ---
fig.add_vline(
    x=optimal_price,
    line_dash="dash",
    line_color="#2ECC71",
    annotation_text="Optimal Price"
)

# --- Current Marker ---
fig.add_scatter(
    x=[round(user_price, 2)],
    y=[current_profit],
    mode="markers",
    marker=dict(size=10, color="#FFD700"),
    name="Current",
    hovertemplate=
        "Price: $%{x:.2f}<br>" +
        "Profit: $%{y:.2f}<extra></extra>"
)

# --- Scenario Marker ---
if scenario_profit:
    fig.add_scatter(
        x=[round(scenario_price, 2)],
        y=[scenario_profit],
        mode="markers",
        marker=dict(size=10, color="#00FFFF"),
        name="Scenario",
        hovertemplate=
            "Price: $%{x:.2f}<br>" +
            "Profit: $%{y:.2f}<extra></extra>"
    )

fig.update_layout(
    template="plotly_dark",
    height=600,
    title="Profit Optimization with Confidence Interval",
    hovermode="x unified",
    legend=dict(
        orientation="h",
        y=1.05,
        x=1,
        xanchor="right"
    )
)

st.plotly_chart(fig, use_container_width=True)



# ---------------------------
# CATEGORY PROFIT RANKING
# ---------------------------
ranking = []

for cat in categories:
    model_cat = joblib.load(os.path.join(MODEL_DIR, f"{cat}_model.pkl"))
    a = model_cat.params["const"]
    b = model_cat.params["log_price"]

    price_local = np.linspace(avg_price * 0.5, avg_price * 2.0, 100)
    profits_local = [
        (P - P * cost_ratio) * (np.exp(a) * (P ** b))
        for P in price_local
    ]

    ranking.append({
        "Category": cat,
        "Max Profit": round(max(profits_local), 2)
    })

ranking_df = pd.DataFrame(ranking).sort_values(by="Max Profit", ascending=False)

st.subheader("📊 Category Profit Ranking")

fig_rank = px.bar(
    ranking_df,
    x="Category",
    y="Max Profit",
    text=ranking_df["Max Profit"].apply(lambda x: f"${x:,.2f}"),
    color="Max Profit",
    template="plotly_dark"
)

fig_rank.update_traces(
    hovertemplate="<b>%{x}</b><br>Max Profit: $%{y:.2f}<extra></extra>"
)

st.plotly_chart(fig_rank, use_container_width=True)

# ---------------------------
# EXECUTIVE PDF
# ---------------------------
st.subheader("📄 Download Executive Summary")

if st.button("Generate Executive PDF"):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph(
        "Pricing Sensitivity & Revenue Optimization Executive Report",
        styles["Title"]
    ))

    elements.append(Spacer(1, 0.5 * inch))

    summary_points = [
        f"Category: {category}",
        f"Elasticity: {beta:.3f}",
        f"Current Profit: ${current_profit:,.2f}",
        f"Optimal Price: ${optimal_price:,.2f}",
        f"Optimal Profit: ${optimal_profit:,.2f}"
    ]

    elements.append(ListFlowable(
        [ListItem(Paragraph(point, styles["Normal"])) for point in summary_points]
    ))

    doc.build(elements)

    st.download_button(
        label="Download PDF",
        data=buffer.getvalue(),
        file_name="pricing_executive_report.pdf",
        mime="application/pdf"
    )

# ---------------------------
# AI SUMMARY
# ---------------------------
st.subheader("🤖 AI Executive Summary")

if beta < -1:
    elasticity_type = "Highly Elastic"
elif -1 <= beta < 0:
    elasticity_type = "Inelastic"
else:
    elasticity_type = "Abnormal"

st.success(f"""
Elasticity Classification: {elasticity_type}

Profit-maximizing price is ${optimal_price:,.2f}.

Confidence interval analysis applied.

Current pricing impact evaluated with precision control.
""")
