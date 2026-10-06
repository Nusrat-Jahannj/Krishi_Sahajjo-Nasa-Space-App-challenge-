
import streamlit as st
import requests
import pandas as pd


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Krishi Sahajjo - NASA Space Apps",
    page_icon="🌾",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🌾 Krishi Sahajjo")
st.subheader("Climate-Smart Crop Rotation Advisor for Bangladesh")

st.caption(
    "Powered by NASA POWER — NASA Earth observation and meteorological data"
)

st.markdown(
    """
    **Krishi Sahajjo** helps farmers explore crop-rotation strategies
    using climate information, local farming conditions, crop characteristics,
    and farmer priorities.

    The tool is a **decision-support prototype**, not a replacement for
    agricultural experts or guaranteed yield predictions.
    """
)


# ============================================================
# BANGLADESH REGIONS
# ============================================================

DISTRICTS = {

    "Rajshahi — Barind Drought Zone": {
        "lat": 24.36,
        "lon": 88.60
    },

    "Rangpur — North-Western Agricultural Zone": {
        "lat": 25.74,
        "lon": 89.27
    },

    "Barishal — Southern Coastal Belt": {
        "lat": 22.70,
        "lon": 90.35
    },

    "Dhaka — Central Agricultural Zone": {
        "lat": 23.81,
        "lon": 90.41
    }
}


# ============================================================
# CROP CHARACTERISTICS
# Qualitative prototype values: 1 = low, 5 = high
# ============================================================

CROPS = {

    "Mung Bean (Moog Dal)": {
        "water_need": 2,
        "nitrogen_benefit": 5,
        "drought_tolerance": 4,
        "flood_tolerance": 2,
        "heat_tolerance": 4
    },

    "Aman Rice": {
        "water_need": 4,
        "nitrogen_benefit": 2,
        "drought_tolerance": 2,
        "flood_tolerance": 5,
        "heat_tolerance": 4
    },

    "Mustard": {
        "water_need": 2,
        "nitrogen_benefit": 2,
        "drought_tolerance": 4,
        "flood_tolerance": 1,
        "heat_tolerance": 3
    },

    "Maize": {
        "water_need": 4,
        "nitrogen_benefit": 2,
        "drought_tolerance": 3,
        "flood_tolerance": 2,
        "heat_tolerance": 4
    },

    "Lentil": {
        "water_need": 2,
        "nitrogen_benefit": 4,
        "drought_tolerance": 4,
        "flood_tolerance": 1,
        "heat_tolerance": 3
    },

    "Jute": {
        "water_need": 4,
        "nitrogen_benefit": 2,
        "drought_tolerance": 2,
        "flood_tolerance": 4,
        "heat_tolerance": 4
    }
}


# ============================================================
# ROTATION STRATEGIES
# ============================================================

ROTATIONS = {

    "Rotation A — Water-Saving": [
        "Mung Bean (Moog Dal)",
        "Aman Rice",
        "Mustard"
    ],

    "Rotation B — Balanced": [
        "Maize",
        "Aman Rice",
        "Lentil"
    ],

    "Rotation C — Traditional + Resilient": [
        "Jute",
        "Aman Rice",
        "Mustard"
    ]
}


# ============================================================
# NASA POWER DATA
# ============================================================

@st.cache_data
def fetch_nasa_data(lat, lon):

    url = (
        "https://power.larc.nasa.gov/api/temporal/climatology/point"
        "?parameters=PRECTOTCORR,GWETTOP,T2M"
        "&community=AG"
        f"&longitude={lon}"
        f"&latitude={lat}"
        "&format=JSON"
    )

    try:

        response = requests.get(url, timeout=15)
        response.raise_for_status()

        data = response.json()

        params = data["properties"]["parameter"]

        months = [
            "Jan", "Feb", "Mar", "Apr",
            "May", "Jun", "Jul", "Aug",
            "Sep", "Oct", "Nov", "Dec"
        ]

        keys = [
            "JAN", "FEB", "MAR", "APR",
            "MAY", "JUN", "JUL", "AUG",
            "SEP", "OCT", "NOV", "DEC"
        ]

        dataframe = pd.DataFrame({

            "Month": months,

            "Soil Wetness (0-1)": [
                params["GWETTOP"][k]
                for k in keys
            ],

            "Precipitation (mm/day)": [
                params["PRECTOTCORR"][k]
                for k in keys
            ],

            "Temperature (°C)": [
                params["T2M"][k]
                for k in keys
            ]
        })

        return dataframe, True

    except Exception:

        # Clearly labelled demonstration values.
        # These are NOT presented as live NASA data.

        dataframe = pd.DataFrame({

            "Month": [
                "Jan", "Feb", "Mar", "Apr",
                "May", "Jun", "Jul", "Aug",
                "Sep", "Oct", "Nov", "Dec"
            ],

            "Soil Wetness (0-1)": [
                0.51, 0.44, 0.34, 0.37,
                0.47, 0.61, 0.76, 0.80,
                0.83, 0.71, 0.60, 0.60
            ],

            "Precipitation (mm/day)": [
                0.25, 0.41, 0.85, 2.67,
                5.09, 7.46, 9.21, 7.45,
                7.37, 4.41, 0.30, 0.20
            ],

            "Temperature (°C)": [
                16.5, 21.1, 26.7, 30.9,
                31.5, 30.3, 28.9, 28.6,
                27.8, 25.8, 21.6, 17.5
            ]
        })

        return dataframe, False


# ============================================================
# CLIMATE ANALYSIS
# ============================================================

def analyze_climate(dataframe):

    pre_monsoon = dataframe[
        dataframe["Month"].isin(["Mar", "Apr", "May"])
    ]

    monsoon = dataframe[
        dataframe["Month"].isin(["Jun", "Jul", "Aug", "Sep"])
    ]

    winter = dataframe[
        dataframe["Month"].isin(["Nov", "Dec", "Jan", "Feb"])
    ]

    pre_monsoon_moisture = pre_monsoon[
        "Soil Wetness (0-1)"
    ].mean()

    monsoon_rainfall = monsoon[
        "Precipitation (mm/day)"
    ].mean()

    winter_rainfall = winter[
        "Precipitation (mm/day)"
    ].mean()

    annual_temperature = dataframe[
        "Temperature (°C)"
    ].mean()

    if pre_monsoon_moisture < 0.40:
        water_stress = "High"

    elif pre_monsoon_moisture < 0.55:
        water_stress = "Moderate"

    else:
        water_stress = "Low"

    if monsoon_rainfall >= 6:
        rainfall_signal = "High"

    elif monsoon_rainfall >= 3:
        rainfall_signal = "Moderate"

    else:
        rainfall_signal = "Low"

    return {

        "pre_monsoon_moisture": pre_monsoon_moisture,

        "monsoon_rainfall": monsoon_rainfall,

        "winter_rainfall": winter_rainfall,

        "annual_temperature": annual_temperature,

        "water_stress": water_stress,

        "rainfall_signal": rainfall_signal
    }


# ============================================================
# CROP SCORING
# ============================================================

def score_crop(crop, priority):

    characteristics = CROPS[crop]

    water_score = 6 - characteristics["water_need"]

    drought_score = characteristics["drought_tolerance"]

    flood_score = characteristics["flood_tolerance"]

    nitrogen_score = characteristics["nitrogen_benefit"]

    if priority == "Conserve Groundwater":

        score = (
            water_score * 0.45
            + drought_score * 0.20
            + flood_score * 0.15
            + nitrogen_score * 0.20
        )

    elif priority == "Restore Soil Nitrogen":

        score = (
            water_score * 0.20
            + drought_score * 0.15
            + flood_score * 0.15
            + nitrogen_score * 0.50
        )

    else:

        score = (
            water_score * 0.25
            + drought_score * 0.30
            + flood_score * 0.30
            + nitrogen_score * 0.15
        )

    return score


# ============================================================
# ROTATION SCORING
# ============================================================

def score_rotation(
    rotation,
    current_crop,
    priority,
    soil_type,
    irrigation
):

    crops = ROTATIONS[rotation]

    crop_scores = [
        score_crop(crop, priority)
        for crop in crops
    ]

    base_score = sum(crop_scores) / len(crop_scores)

    adjustment = 0

    # --------------------------------------------------------
    # Previous crop adjustment
    # --------------------------------------------------------

    if current_crop == "Boro Rice (High Water)":

        if "Mung Bean (Moog Dal)" in crops:
            adjustment += 0.4

    elif current_crop == "Maize":

        if "Lentil" in crops:
            adjustment += 0.3

    elif current_crop == "Jute":

        if "Mustard" in crops:
            adjustment += 0.2

    # --------------------------------------------------------
    # Irrigation adjustment
    # --------------------------------------------------------

    if irrigation == "Low":

        average_water_need = sum(
            CROPS[crop]["water_need"]
            for crop in crops
        ) / len(crops)

        if average_water_need <= 2.5:
            adjustment += 0.5

        elif average_water_need >= 3.5:
            adjustment -= 0.4

    elif irrigation == "High":

        adjustment += 0.1

    # --------------------------------------------------------
    # Soil adjustment
    # --------------------------------------------------------

    if soil_type == "Sandy Loam":

        if "Mung Bean (Moog Dal)" in crops:
            adjustment += 0.2

        if "Lentil" in crops:
            adjustment += 0.2

    elif soil_type == "Clay":

        if "Aman Rice" in crops:
            adjustment += 0.3

    elif soil_type == "Clay Loam":

        adjustment += 0.2

    final_score = base_score + adjustment

    # Convert to an easy-to-read 0–100 style score

    adaptation_score = min(
        100,
        max(
            0,
            round(final_score / 5 * 100)
        )
    )

    return adaptation_score


# ============================================================
# USER INPUTS
# ============================================================

st.divider()

st.header("🌱 Tell Us About Your Farm")

col1, col2, col3 = st.columns(3)

with col1:

    selected_district = st.selectbox(
        "📍 Target Region",
        list(DISTRICTS.keys())
    )

    current_crop = st.selectbox(
        "🌾 Current / Last Harvested Crop",
        [
            "Boro Rice (High Water)",
            "Maize",
            "Jute"
        ]
    )


with col2:

    priority = st.selectbox(
        "🎯 Primary Farmer Goal",
        [
            "Conserve Groundwater",
            "Restore Soil Nitrogen",
            "Max Climate Resilience"
        ]
    )

    soil_type = st.selectbox(
        "🪨 Soil Type",
        [
            "Loam",
            "Sandy Loam",
            "Clay",
            "Clay Loam"
        ]
    )


with col3:

    irrigation = st.selectbox(
        "💧 Irrigation Availability",
        [
            "Low",
            "Moderate",
            "High"
        ]
    )


# ============================================================
# FETCH NASA DATA
# ============================================================

coordinates = DISTRICTS[selected_district]

df, live_nasa = fetch_nasa_data(
    coordinates["lat"],
    coordinates["lon"]
)

climate = analyze_climate(df)


if live_nasa:

    st.success(
        "🛰️ Live NASA POWER climate data loaded successfully."
    )

else:

    st.warning(
        "⚠️ NASA POWER could not be reached right now. "
        "The app is showing clearly labelled demonstration data "
        "so the prototype can still be explored."
    )


# ============================================================
# CLIMATE SNAPSHOT
# ============================================================

st.divider()

st.header("🛰️ NASA Climate Snapshot")

m1, m2, m3, m4 = st.columns(4)

with m1:

    st.metric(
        "Pre-Monsoon Soil Wetness",
        f"{climate['pre_monsoon_moisture']:.2f}"
    )

with m2:

    st.metric(
        "Monsoon Rainfall",
        f"{climate['monsoon_rainfall']:.1f} mm/day"
    )

with m3:

    st.metric(
        "Annual Mean Temperature",
        f"{climate['annual_temperature']:.1f} °C"
    )

with m4:

    st.metric(
        "Water Stress",
        climate["water_stress"]
    )


# ============================================================
# RECOMMEND ROTATION
# ============================================================

rotation_scores = {}

for rotation in ROTATIONS:

    rotation_scores[rotation] = score_rotation(
        rotation,
        current_crop,
        priority,
        soil_type,
        irrigation
    )


best_rotation = max(
    rotation_scores,
    key=rotation_scores.get
)

best_score = rotation_scores[best_rotation]

best_crops = ROTATIONS[best_rotation]


# ============================================================
# RECOMMENDATION
# ============================================================

st.divider()

st.header("🚜 Recommended Climate-Resilient Rotation")

st.success(
    f"### ⭐ Recommended Strategy: {best_rotation}"
)

st.metric(
    "Prototype Adaptation Score",
    f"{best_score}/100"
)

st.write(
    "This score is a comparative decision-support indicator "
    "based on the selected farmer priorities, crop characteristics, "
    "local conditions and NASA climate indicators. "
    "It is not a guaranteed yield prediction."
)


# ============================================================
# THREE-SEASON PLAN
# ============================================================

r1, r2, r3 = st.columns(3)

with r1:

    st.info("### 🌱 Phase 1 — Kharif-1")

    st.write(
        f"**{best_crops[0]}**"
    )

    st.write(
        "Selected as the first stage of the proposed rotation "
        "based on the farmer's priority and crop characteristics."
    )


with r2:

    st.success("### 🌧️ Phase 2 — Monsoon")

    st.write(
        f"**{best_crops[1]}**"
    )

    st.write(
        "The monsoon phase considers rainfall and water availability "
        "when evaluating crop suitability."
    )


with r3:

    st.warning("### 🌾 Phase 3 — Rabi")

    st.write(
        f"**{best_crops[2]}**"
    )

    st.write(
        "The final phase considers water demand, soil benefits "
        "and climate resilience."
    )


# ============================================================
# WHY THIS ROTATION?
# ============================================================

st.divider()

st.header("💡 Why Was This Rotation Selected?")

st.write(
    f"""
    **Farmer priority:** {priority}

    **Current / previous crop:** {current_crop}

    **Soil type:** {soil_type}

    **Irrigation availability:** {irrigation}

    **Pre-monsoon soil wetness:** 
    {climate['pre_monsoon_moisture']:.2f}

    **Average monsoon rainfall:** 
    {climate['monsoon_rainfall']:.1f} mm/day

    These factors are combined with qualitative crop characteristics
    to compare the three rotation strategies.
    """
)


# ============================================================
# ROTATION COMPARISON
# ============================================================

st.divider()

st.header("📊 Compare Rotation Strategies")

comparison_data = []

for rotation, score in rotation_scores.items():

    comparison_data.append({

        "Rotation": rotation,

        "Season 1": ROTATIONS[rotation][0],

        "Season 2": ROTATIONS[rotation][1],

        "Season 3": ROTATIONS[rotation][2],

        "Adaptation Score": score
    })


comparison_df = pd.DataFrame(comparison_data)

st.dataframe(
    comparison_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# NASA TRENDS
# ============================================================

st.divider()

st.header("📈 NASA Climate Trends")

st.write(
    "Monthly precipitation and top-layer soil wetness indicators "
    "help visualize the climate conditions considered by the prototype."
)

chart_df = df.set_index("Month")[
    [
        "Precipitation (mm/day)",
        "Soil Wetness (0-1)"
    ]
]

st.line_chart(chart_df)


# ============================================================
# METHODOLOGY
# ============================================================

st.divider()

with st.expander("🔬 How Krishi Sahajjo Works"):

    st.markdown(
        """
        **Step 1 — Local context**

        The farmer selects a Bangladesh region, current crop,
        soil type, irrigation availability and farming priority.

        **Step 2 — NASA climate information**

        Krishi Sahajjo retrieves climate indicators from NASA POWER,
        including precipitation, temperature and top-layer soil wetness.

        **Step 3 — Crop characteristics**

        Crops are represented using qualitative prototype characteristics
        such as water demand, drought tolerance, flood tolerance and
        potential nitrogen benefit.

        **Step 4 — Transparent scoring**

        The system compares different crop rotations using explicit
        weighting rules rather than a black-box prediction.

        **Step 5 — Recommendation**

        The highest-scoring rotation is presented together with the
        factors that influenced the recommendation.
        """
    )


# ============================================================
# DATA & LIMITATIONS
# ============================================================

with st.expander("📚 Data Sources & Limitations"):

    st.markdown(
        """
        ### NASA Data

        NASA POWER provides agroclimatology and meteorological
        data used in this prototype.

        Parameters used:

        - Precipitation
        - Top-layer soil wetness
        - Temperature

        ### Important limitations

        This is a prototype decision-support system.

        The current version does **not** provide:

        - Guaranteed crop yield predictions
        - Guaranteed economic returns
        - Individual farm-level soil laboratory analysis
        - Real-time field sensor measurements
        - Agricultural prescriptions
        - Disease diagnosis

        Crop characteristics used in the scoring model are
        qualitative prototype assumptions and should be replaced
        or validated with authoritative agricultural datasets
        before real-world deployment.
        """
    )


# ============================================================
# SAFETY / RESPONSIBLE USE
# ============================================================

st.divider()

st.info(
    """
    🌱 **Responsible Use**

    Krishi Sahajjo is designed to help farmers explore climate-smart
    crop-rotation options. It should support — not replace —
    local agricultural experts, extension officers and field-level
    knowledge before making real farming decisions.
    """
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Krishi Sahajjo | NASA Space Apps Challenge 2026 | "
    "Bangladesh-focused climate-smart agriculture prototype"
)
