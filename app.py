import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="PondGuard | Aquaculture Early Warning",
    page_icon="🐟",
    layout="wide",
)

st.title("🐟 PondGuard")
st.subheader("Explainable Early-Warning System for Aquaculture Ponds")
st.caption(
    "A prototype that flags potentially concerning water-quality readings and explains each alert. "
    "It is not a validated disease or mortality prediction model."
)

with st.sidebar:
    st.header("Pond details")
    pond_name = st.text_input("Pond name / ID", "Pond A")
    species = st.selectbox(
        "Farmed species", ["Tilapia", "Carp", "Catfish", "Shrimp", "Other"]
    )
    st.markdown("---")
    st.caption(
        "Enter readings from a test kit, sensor, or sample dataset. "
        "Thresholds are illustrative and should be validated for the species and farm."
    )

st.markdown("### Water-quality readings")
st.write("Enter the latest measurements and, if available, an earlier reading to compare trends.")

current_col, previous_col = st.columns(2)

with current_col:
    st.markdown("#### Current reading")
    c1, c2, c3 = st.columns(3)
    with c1:
        oxygen = st.number_input(
            "Dissolved oxygen (mg/L)", min_value=0.0, max_value=20.0,
            value=5.0, step=0.1, key="oxygen"
        )
    with c2:
        temp = st.number_input(
            "Water temperature (°C)", min_value=0.0, max_value=50.0,
            value=28.0, step=0.5, key="temp"
        )
    with c3:
        ph = st.number_input(
            "pH", min_value=0.0, max_value=14.0,
            value=7.5, step=0.1, key="ph"
        )

with previous_col:
    st.markdown("#### Previous reading")
    p1, p2, p3 = st.columns(3)
    with p1:
        prev_oxygen = st.number_input(
            "Previous dissolved oxygen (mg/L)", min_value=0.0, max_value=20.0,
            value=6.0, step=0.1, key="prev_oxygen"
        )
    with p2:
        prev_temp = st.number_input(
            "Previous temperature (°C)", min_value=0.0, max_value=50.0,
            value=28.0, step=0.5, key="prev_temp"
        )
    with p3:
        prev_ph = st.number_input(
            "Previous pH", min_value=0.0, max_value=14.0,
            value=7.5, step=0.1, key="prev_ph"
        )

hours = st.slider(
    "Hours between current and previous readings",
    min_value=1, max_value=48, value=6
)

# Transparent illustrative scoring. This is a rule-based baseline, not ML.
score = 0
reasons = []

if oxygen < 3:
    score += 45
    reasons.append((
        "Critically low dissolved oxygen",
        f"Current dissolved oxygen is {oxygen:.1f} mg/L, below the prototype's illustrative 3 mg/L threshold."
    ))
elif oxygen < 5:
    score += 25
    reasons.append((
        "Low dissolved oxygen",
        f"Current dissolved oxygen is {oxygen:.1f} mg/L, below the prototype's illustrative 5 mg/L caution threshold."
    ))

if temp > 32:
    score += 20
    reasons.append((
        "High water temperature",
        f"Temperature is {temp:.1f}°C, above the prototype's illustrative 32°C threshold."
    ))
elif temp < 20:
    score += 10
    reasons.append((
        "Low water temperature",
        f"Temperature is {temp:.1f}°C, below the prototype's illustrative 20°C threshold."
    ))

if ph < 6.5 or ph > 8.5:
    score += 20
    reasons.append((
        "pH outside the reference range",
        f"Measured pH is {ph:.1f}; this prototype uses an illustrative reference range of 6.5–8.5."
    ))

do_drop = prev_oxygen - oxygen
if do_drop >= 1.0:
    score += 20
    reasons.append((
        "Dissolved oxygen is falling",
        f"Dissolved oxygen fell by {do_drop:.1f} mg/L over {hours} hour(s). Consider promptly rechecking the measurement."
    ))
elif do_drop >= 0.5:
    score += 10
    reasons.append((
        "Dissolved oxygen trend needs attention",
        f"Dissolved oxygen fell by {do_drop:.1f} mg/L over {hours} hour(s)."
    ))

temp_change = abs(temp - prev_temp)
if temp_change >= 3:
    score += 10
    reasons.append((
        "Notable temperature change",
        f"Temperature changed by {temp_change:.1f}°C between the two readings."
    ))

score = min(score, 100)

if score >= 60:
    risk, indicator = "HIGH", "🔴"
elif score >= 30:
    risk, indicator = "MODERATE", "🟠"
else:
    risk, indicator = "LOW", "🟢"

st.markdown("---")
st.markdown(f"### Risk assessment — {pond_name or 'Unnamed pond'}")
st.caption(f"Species selected: {species}")

metric1, metric2, metric3 = st.columns(3)
metric1.metric("Illustrative risk score", f"{score}/100")
metric2.metric("Risk category", f"{indicator} {risk}")
metric3.metric("Dissolved oxygen change", f"{do_drop:+.1f} mg/L")

if risk == "HIGH":
    st.error(
        "High-priority alert: recheck the measurements promptly and follow your farm's established response procedures. "
        "Do not rely on this prototype alone."
    )
elif risk == "MODERATE":
    st.warning(
        "Attention advised: recheck water quality and inspect pond conditions. Review the contributing factors below."
    )
else:
    st.success(
        "The current illustrative rules did not detect a major alert. Continue routine monitoring; "
        "a low score does not guarantee that the pond is safe."
    )

st.markdown("### Why was this alert generated?")
if reasons:
    for title, detail in reasons:
        st.markdown(f"- **{title}:** {detail}")
else:
    st.write("No alert conditions were triggered by the current illustrative rules.")

st.markdown("### Suggested response")
if any("oxygen" in title.lower() for title, _ in reasons):
    st.write(
        "- Recheck dissolved oxygen with a reliable test or calibrated instrument.\n"
        "- Inspect fish behaviour and pond conditions, and follow your farm's established low-oxygen procedure if needed."
    )
elif risk == "MODERATE":
    st.write(
        "- Recheck the readings and inspect pond conditions.\n"
        "- Compare the measurements with guidance appropriate for your species and farm."
    )
else:
    st.write(
        "- Continue routine water-quality monitoring.\n"
        "- Use locally appropriate aquaculture guidance to interpret the readings."
    )

st.markdown("### Reading comparison")
history = pd.DataFrame({
    "Reading": ["Previous", "Current"],
    "Dissolved oxygen (mg/L)": [prev_oxygen, oxygen],
    "Temperature (°C)": [prev_temp, temp],
    "pH": [prev_ph, ph],
})
st.dataframe(history, width="stretch", hide_index=True)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    fig, ax = plt.subplots()
    ax.plot(history["Reading"], history["Dissolved oxygen (mg/L)"], marker="o")
    ax.set_ylabel("Dissolved oxygen (mg/L)")
    ax.set_title("Dissolved oxygen comparison")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)

with chart_col2:
    fig, ax = plt.subplots()
    ax.plot(history["Reading"], history["Temperature (°C)"], marker="o")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Temperature comparison")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)

with st.expander("About this prototype"):
    st.write(
        "PondGuard currently uses transparent, illustrative rules to calculate a risk score from the entered "
        "readings and their changes. It does not use a trained machine-learning model, diagnose fish disease, "
        "or predict mortality. Thresholds and suggested responses must be checked against reliable, "
        "species- and farm-specific guidance before real-world use."
    )
