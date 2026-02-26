import streamlit as st
import matplotlib.pyplot as plt
from model import train_model, predict_delay
from optimizer import optimize_schedule
from utils import calculate_costs, risk_level
import numpy as np

st.set_page_config(page_title="AI Construction Optimizer", layout="wide")

st.title("🏗 Dynamic Digital Twin – Construction Optimizer")

# ------------------------
# Project Parameters
# ------------------------
planned_days = 70
planned_cost = 100  # Cr

st.sidebar.header("Live Site Conditions")

rain = st.sidebar.slider("Rain Intensity", 0.0, 10.0, 3.0)
labor = st.sidebar.slider("Available Labor", 50.0, 120.0, 80.0)
material_delay = st.sidebar.slider("Material Delay (days)", 0.0, 7.0, 2.0)
productivity = st.sidebar.slider("Productivity Factor", 0.7, 1.2, 1.0)

scenario = st.sidebar.radio("Scenario Mode",
                            ["Normal Conditions", "Extreme Weather"])

if scenario == "Extreme Weather":
    rain += 3

model = train_model()

predicted_delay = predict_delay(model, rain, labor, material_delay, productivity)
predicted_completion = planned_days + predicted_delay

st.info(f"Under the assumed conditions (Rain={rain}, Labor={labor}, Material Delay={material_delay} days), the AI predicts a total project completion of {round(predicted_completion,2)} days.")

optimized_delay, new_labor, new_prod = optimize_schedule(
    model, rain, labor, material_delay, productivity
)

optimized_completion = planned_days + optimized_delay

delay_days, cost_overrun = calculate_costs(planned_days, predicted_completion)

# ------------------------
# Display Metrics
# ------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Predicted Completion (Days)", round(predicted_completion,2))
col2.metric("Optimized Completion (Days)", round(optimized_completion,2))
col3.metric("Cost Overrun (Cr)", round(cost_overrun,2))

st.markdown("## 📊 Performance KPIs")

delay_reduction = predicted_completion - optimized_completion
percent_reduction = (delay_reduction / predicted_completion) * 100

k1, k2, k3 = st.columns(3)

k1.metric("Days Saved", round(delay_reduction,2))
k2.metric("Delay Reduction (%)", round(percent_reduction,2))
k3.metric("Optimized Labor Allocation", round(new_labor,2))


risk = risk_level(predicted_delay)

if risk == "Low Risk":
    st.success("🟢 Low Risk – Schedule Stable")
elif risk == "Medium Risk":
    st.warning("🟡 Medium Risk – Monitor Closely")
else:
    st.error("🔴 High Risk – Immediate Optimization Required")

# ------------------------
# Visualization
# ------------------------
fig, ax = plt.subplots(figsize=(5,3))
ax.bar(
    ["Planned", "Predicted", "Optimized"],
    [planned_days, predicted_completion, optimized_completion],
)
ax.set_ylabel("Project Duration (Days)")
st.pyplot(fig, use_container_width=False)



st.markdown("## 🏢 Floor-wise Delay Simulation")

floors = 10
floor_delays = []

for i in range(floors):
    floor_delay = predicted_delay / floors + np.random.uniform(-0.5,0.5)
    floor_delays.append(max(floor_delay,0))

fig2, ax2 = plt.subplots(figsize=(5,3))
ax2.bar(range(1, floors+1), floor_delays)
ax2.set_xlabel("Floor Number")
ax2.set_ylabel("Delay (Days)")
st.pyplot(fig2, use_container_width=False)

# ------------------------
# Executive Summary
# ------------------------
st.success(
    f"Optimization saved approximately {round(predicted_completion - optimized_completion,2)} days "
    f"and reduced cost impact significantly."
)