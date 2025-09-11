import streamlit as st
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.set_page_config(page_title="PowerPedal Interactive Pitch Deck", layout="wide")
st.title("🚴 PowerPedal – The Future of Smart Urban Mobility")
st.caption("Switch Mobility | Interactive Investor Deck")

st.markdown(
    """
    <details>
      <summary style="font-size:16px; font-weight:bold; cursor:pointer;">
        👋 Welcome! Read this for a detailed guide on navigating the deck.
      </summary>
      <div style="margin-top:10px;">
        <p>
        This interactive deck is designed for deep exploration. Here’s a detailed guide to each section to help you get the most out of our presentation.
        </p>
        <h4>A Tab-by-Tab Guide</h4>
        <ul>
          <li><b>🌍 Vision & Mission:</b> Start here to understand our core purpose and long-term goal.</li>
          <li><b>⚠️ Problem:</b> Learn about the critical challenges in the current e-bike market.</li>
          <li><b>🌏 Market Opportunity:</b> See our analysis of the market size and target.</li>
          <li><b>⚙️ PowerPedal – The Product:</b> Discover our hardware + software solution.</li>
          <li><b>💼 Business Model:</b> Understand our revenue streams.</li>
          <li><b>🚀 Go-to-Market Strategy:</b> Explore our actionable plan.</li>
          <li><b>📊 Financial Projections:</b> Review key financial forecasts.</li>
          <li><b>📍 Milestones & Traction:</b> See the tangible progress we’ve already made.</li>
          <li><b>🧑‍🤝‍🧑 Team & Advisors:</b> Meet the experienced team driving PowerPedal.</li>
          <li><b>💰 Funding Ask & Use:</b> Find the details of our funding round.</li>
          <li><b>🔮 Future Tech & Expansion:</b> Look ahead at our roadmap and R&D.</li>
          <li><b>🎙️ Audio Pitch:</b> Listen to our narrated pitch for a quick summary.</li>
        </ul>
      </div>
    </details>
    """,
    unsafe_allow_html=True
)

# Initialize session state globally
if 'selected_market' not in st.session_state:
    st.session_state.selected_market = "PAM"  # Default to PAM
if 'selected_challenge' not in st.session_state:
    st.session_state.selected_challenge = None  # For challenge sub-tab selection

# ---- Global CSS (Moved here to avoid conflicts) ----
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        /* Import Figtree font */
        @import url('https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800&display=swap');

        /* Apply Figtree globally to all elements */
        * {
            font-family: 'Figtree', sans-serif !important;
        }

        /* Main tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            width: 100%;
            justify-content: center;
        }
        .stTabs [data-baseweb="tab"] {
            flex: 0 0 18%;
            padding: 16px 24px;
            font-size: 24px;
            font-weight: 600;
            text-align: center;
            border-radius: 6px;
            background-color: #1e1e1e;
            color: #e0e0e0;
            transition: background-color 0.3s, color 0.3s;
        }
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color: #A8F1FF;
            color: #000000;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #91C8E4;
        }
        .stTabs [data-baseweb="tab"][aria-selected="true"]::after {
            content: '';
            display: block;
            width: 100%;
            height: 3px;
            background-color: #A8F1FF;
            position: absolute;
            bottom: 0;
            left: 0;
        }
        /* Separate CSS for Problem tab sub-tabs */
        .problem-tab .stTabs [data-baseweb="tab-list"] .stTabs [data-baseweb="tab"] {
            flex: 0 0 40% !important;
            padding: 56px 80px !important;
            font-size: 120px !important;
            font-weight: 800 !important;
            background-color: #1B3C53;
            color: #e0e0e0 !important;
            border-radius: 20px !important;
            margin: 10px 0 !important;
        }
        .problem-tab .stTabs [data-baseweb="tab-list"] .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color: #2e2e2e !important;
            color: #4caf50 !important;
        }
        .problem-tab .stTabs [data-baseweb="tab-list"] .stTabs [data-baseweb="tab"]:hover {
            background-color: #262626 !important;
        }
        .challenge-container {
            border: 1px solid #1B3C53;
            border-radius: 10px;
            padding: 20px;
            background-color: #1B3C53;
            min-height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            transition: background-color 0.3s, transform 0.2s, border-color 0.3s, opacity 0.3s;
            margin: 10px;
        }
        .challenge-container.active {
            background-color: #1B3C53;
            border: 2px solid #78C841;
            transform: scale(1.1);
            min-height: 200px;
            opacity: 1;
        }
        .challenge-container h4 {
            color: #78C841 !important;
            margin: 10px 0 5px 0;
        }
        .challenge-container p {
            font-size: 14px !important;
            line-height: 1.4 !important;
            margin: 10px 0 0 0 !important;
            color: #FFF5F2 !important;
        }
        .challenge-container.active p {
            font-size: 18px !important;
            line-height: 1.4 !important;
            margin: 10px 0 0 0 !important;
            color: #FFF5F2 !important;
        }
        .challenge-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            justify-content: center;
            margin: 20px 0;
        }
        .problem-image-container {
            transition: opacity 0.3s;
        }
        .problem-image-container.faded {
            opacity: 0.5;
        }
        .problem-text {
            transition: opacity 0.3s;
        }
        .problem-text.faded {
            opacity: 0.5;
        }
        /* Table styling for Ebike tables */
        .ebike-table {
            width: 100%;
            max-width: 700px;
            border-collapse: collapse;
            background-color: #1B3C53;
            color: #FFF5F2;
            margin-top: 20px;
            margin-bottom: 20px;
        }
        .ebike-table th {
            background-color: #1B3C53;
            color: #78C841;
            font-size: 16px;
            font-weight: 600;
            padding: 12px;
            border: 1px solid #78C841;
            text-align: center;
        }
        .ebike-table td {
            font-size: 14px;
            padding: 12px;
            border: 1px solid #78C841;
            text-align: center;
        }
        .ebike-table-title {
            color: #78C841;
            font-size: 20px;
            font-weight: 600;
            margin-top: 30px;
            margin-bottom: 10px;
            text-align: left;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- Function to Create HTML Table from DataFrame ----
def create_html_table(df, title):
    table_html = f"""
    <h3 class="ebike-table-title">{title}</h3>
    <table class="ebike-table">
        <tr>
    """
    for col in df.columns:
        table_html += f"<th>{col}</th>"
    table_html += "</tr>"
    for _, row in df.iterrows():
        table_html += "<tr>"
        for value in row:
            table_html += f"<td>{value}</td>"
        table_html += "</tr>"
    table_html += "</table>"
    return table_html

# ---- Function to Load and Transpose Excel Data ----
def load_excel_data(file_name, expected_columns, fallback_data, transpose=False):
    try:
        df = pd.read_excel(file_name)
        if all(col.lower() in [c.lower() for c in df.columns] for col in expected_columns):
            if transpose:
                df = df.set_index(df.columns[0]).T.reset_index()
                attr_count = len(df.columns) - 1
                if attr_count > 0:
                    attr_names = ['Cost', 'Performance', 'Efficiency', 'Features', 'Average Price'][:attr_count]
                    df.columns = ['Drive System'] + attr_names
                else:
                    df.columns = ['Drive System']
            return df, None
        else:
            st.error(f"Error: {file_name} does not contain all required columns: {expected_columns}")
            return pd.DataFrame(fallback_data, columns=expected_columns), f"Missing columns in {file_name}"
    except FileNotFoundError:
        st.error(f"Error: {file_name} not found in the current directory")
        return pd.DataFrame(fallback_data, columns=expected_columns), f"{file_name} not found"
    except Exception as e:
        st.error(f"Error loading {file_name}: {str(e)}")
        return pd.DataFrame(fallback_data, columns=expected_columns), f"Error loading {file_name}"

# ---- TABS ----
tabs = st.tabs([
    "🌍 Vision & Mission",
    "⚠️ Problem",
    "🌏 Market Opportunity",
    "⚙️ PowerPedal – The Product",
    "💼 Business Model",
    "🚀 Go-to-Market Strategy",
    "📊 Financial Projections",
    "📍 Milestones & Traction",
    "🧑‍🤝‍🧑 Team & Advisors",
    "💰 Funding Ask & Use",
    "🔮 Future Tech & Expansion",
    "🎙️Audio Pitch"
    
])

import requests
from io import BytesIO

# ---- TAB 1: Vision & Mission ---
with tabs[0]:
    st.header("🌍 Vision & Mission")
    
    # Display single vision.png image
    image_path = "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/vision.png"
    st.markdown('<div class="vision-images">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            # Fetch the image from the URL
            response = requests.get(image_path)
            if response.status_code == 200:
                img = BytesIO(response.content)
                st.image(img, use_container_width=False, width=1500, output_format="auto", channels="RGB")
            else:
                st.error(f"Failed to load image from {image_path}. Status code: {response.status_code}")
                st.markdown(
                    """
                    <div style="text-align: center; border: 1px solid #e6e6e6; border-radius: 10px; padding: 20px; background-color: #f0f0f0;">
                        <p style="color: #555;">Placeholder: No image</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        except Exception as e:
            st.error(f"Failed to display image at {image_path}. Error: {str(e)}")
            st.markdown(
                """
                <div style="text-align: center; border: 1px solid #e6e6e6; border-radius: 10px; padding: 20px; background-color: #f0f0f0;">
                    <p style="color: #555;">Placeholder: No image</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style='border: 1px solid #1B3C53; border-radius: 10px; padding: 20px; background-color: #1B3C53; margin-top: 10px; margin-bottom: 10px;'>
            <h3 style='color: #78C841; margin-top: 0;'>🌍 Our Vision</h3>
            <p style='font-size: 20px; font-style: italic; color: #FFF5F2; margin-bottom: 0;'>
                Creating sustainable, efficient, and affordable urban mobility technology for a smarter future. </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <div style='border: 1px solid #1B3C53; border-radius: 10px; padding: 20px; background-color: #1B3C53; margin-top: 10px;'>
            <h3 style='color: #78C841; margin-top: 0;'>🎯 Our Mission</h3>
            <p style='font-size: 20px; font-style: italic; color: #FFF5F2; margin-bottom: 0;'>
                We enable widespread use of optimized light electric vehicles through innovation, smart engineering, and strategic collaborations, making advanced mobility accessible to all.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

import streamlit as st
import requests
from io import BytesIO

# ---- TAB 2: Problem ----
with tabs[1]:
    st.header("⚠️ Problem")
    
    # Add problem-tab class to wrap sub-tabs
    st.markdown('<div class="problem-tab">', unsafe_allow_html=True)

    # Challenges Infographic
    st.markdown(
        """
        <p class='problem-text' style='font-size: 18px; color: #e0e0e0; text-align: center; margin: 20px 0;'>
            Current e-bike drive systems face significant hurdles that limit performance, affordability, and scalability.
        </p>
        """,
        unsafe_allow_html=True
    )

    # Display problem.png (centered)
    problem_image_path = "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/problem.png"
    image_class = "problem-image-container faded" if st.session_state.get('selected_challenge') else "problem-image-container"
    st.markdown(f'<div class="{image_class}">', unsafe_allow_html=True)
    try:
        # Fetch the image from the URL
        response = requests.get(problem_image_path)
        if response.status_code == 200:
            img = BytesIO(response.content)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(img, use_container_width=False, width=1500, output_format="auto", channels="RGB")
        else:
            st.error(f"Failed to load image from {problem_image_path}. Status code: {response.status_code}")
            st.markdown(
                """
                <div style="text-align: center; border: 1px solid #e6e6e6; border-radius: 10px; padding: 20px; background-color: #f0f0f0;">
                    <p style="color: #555;">Placeholder: No image available for problem.png</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    except Exception as e:
        st.error(f"Failed to display image at {problem_image_path}. Error: {str(e)}")
        st.markdown(
            """
            <div style="text-align: center; border: 1px solid #e6e6e6; border-radius: 10px; padding: 20px; background-color: #f0f0f0;">
                <p style="color: #555;">Placeholder: No image available for problem.png</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)
    # Challenge data
    challenges = [
        {
            "icon": "🚲",
            "title": "Inefficient Ride",
            "detailed_desc": """
                Poor cadence sensors, expensive torque sensors<br>
                In many low-cost Chinese drive systems, cadence-based pedal assist dominates. Cadence sensors only detect if the pedals are turning — they don’t measure how hard the rider is pedaling.<br>
                • This results in delayed motor activation, abrupt surges, and assistance that feels disconnected from rider effort.<br>
                • While torque sensors provide a much smoother and more natural ride by measuring actual pedaling force, they are significantly more expensive, which pushes up system cost.<br>
                • In practice, OEMs often opt for cadence sensors to keep prices low, sacrificing efficiency and ride quality.
            """
        },
        {
            "icon": "💰",
            "title": "High Costs",
            "detailed_desc": """
                Japanese and European systems are too expensive<br>
                Japanese and European drive systems deliver top-tier refinement, reliability, and performance — but at a price that’s out of reach for many OEMs in emerging markets.<br>
                • The drive unit cost alone can make up 30–50% of an eBike’s retail price.<br>
                • This pricing model locks out small to mid-size manufacturers and limits the spread of high-performance eBikes in cost-sensitive regions.
            """
        },
        {
            "icon": "⚙️⚙️",
            "title": "Integration Issues",
            "detailed_desc": """
                Lack of interoperability, difficult to integrate, no diagnostics, causing downtime<br>
                • Many existing systems are closed ecosystems, making them hard to integrate with third-party components.<br>
                • Limited compatibility with different displays, batteries, and controllers forces OEMs into vendor lock-in.<br>
                • Integration can require custom wiring harnesses, firmware changes, and long trial-and-error cycles.<br>
                • The absence of built-in self-diagnostics means even small issues require manual troubleshooting, increasing downtime and service costs.
            """
        },
        {
            "icon": "📉",
            "title": "Limited Features",
            "detailed_desc": """
                Lack of affordable remote diagnostics and smart analytics<br>
                While premium systems offer connected apps, cloud analytics, and remote troubleshooting, affordable drive systems rarely include these features.<br>
                • Without remote diagnostics, problems are identified only after a manual inspection, delaying repairs.<br>
                • The absence of usage analytics means there’s no visibility into rider behavior, battery health trends, or early signs of failure.<br>
                • This results in reactive maintenance, higher operational costs, and missed opportunities to improve performance over time.
            """
        }
    ]

    # Sub-tabs for challenges (including Overview)
    sub_tab_titles = ["Overview"] + [f"{challenge['icon']} {challenge['title']}" for challenge in challenges]
    sub_tabs = st.tabs(sub_tab_titles)

    # Overview tab: show all challenge icons and titles in a grid
    with sub_tabs[0]:
        st.session_state.selected_challenge = None
        st.markdown(
            """
            <div class='challenge-grid'>
            """,
            unsafe_allow_html=True
        )
        for challenge in challenges:
            st.markdown(
                f"""
                <div class='challenge-container' style='position: relative;'>
                    <div style='font-size: 40px;'>{challenge['icon']}</div>
                    <h4 style='color: #78C841; margin: 10px 0 5px 0;'>{challenge['title']}</h4>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown(
            """
            </div>
            """,
            unsafe_allow_html=True
        )

    # Individual challenge tabs
    for i, challenge in enumerate(challenges):
        with sub_tabs[i + 1]:
            st.session_state.selected_challenge = challenge["title"]
            st.markdown(
                f"""
                <div class='challenge-container active' style='position: relative;'>
                    <div style='font-size: 40px;'>{challenge['icon']}</div>
                    <h4 style='color: #78C841; margin: 10px 0 5px 0;'>{challenge['title']}</h4>
                    <p>{challenge['detailed_desc']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Close problem-tab div
    st.markdown('</div>', unsafe_allow_html=True)

# Helper function to load Excel data with proper URL handling
def load_excel_data(url, expected_columns, fallback_data, transpose=True):
    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_excel(BytesIO(response.content))
        if not all(col in df.columns for col in expected_columns):
            st.warning(f"Expected columns {expected_columns} not found in {url}. Using fallback data.")
            if transpose and isinstance(fallback_data, pd.DataFrame):
                return fallback_data, f"Column mismatch in {url}"
            elif not transpose and isinstance(fallback_data, pd.DataFrame):
                return fallback_data, f"Column mismatch in {url}"
            else:
                return pd.DataFrame(fallback_data), f"Column mismatch in {url}"
        return df, None
    except Exception as e:
        st.warning(f"Error loading {url}: {str(e)}. Using fallback data.")
        if transpose and isinstance(fallback_data, pd.DataFrame):
            return fallback_data, str(e)
        elif not transpose and isinstance(fallback_data, pd.DataFrame):
            return fallback_data, str(e)
        else:
            return pd.DataFrame(fallback_data), str(e)

# ---- TAB 3: Market Opportunity ----
with tabs[2]:
    st.header("🌏 Market Opportunity")
    st.caption("PAM / TAM / SAM / SOM for PowerPedal")

    # Market data for circles and containers
    market_data = [
        {
            "id": "pam",
            "title": "PAM",
            "value": "$50.8B",
            "full_desc": "Potential Addressable Market: $50.8 Billion USD - Global e-bike market growing.",
            "bg_color": "#3E3F29"
        },
        {
            "id": "tam",
            "title": "TAM",
            "value": "$7.16B",
            "full_desc": "Total Addressable Market: $7.16 Billion USD - Global e-bike drivetrain market.",
            "bg_color": "#819067"
        },
        {
            "id": "sam",
            "title": "SAM",
            "value": "$2.7B",
            "full_desc": "Serviceable Addressable Market: $2.7 Billion USD - Non-Chinese (50%) drivetrain market focusing on Hub drives (60% of total drive market) and Entry level Mid-drives.",
            "bg_color": "#A08963"
        },
        {
            "id": "som",
            "title": "SOM",
            "value": "$0.25B",
            "full_desc": "Serviceable Obtainable Market: $0.25 Billion USD - PowerPedal is targeting a 9% share of the 11 million-unit non-Chinese top 100 hub-drive eBike market by 2025-30, focusing on India, Europe, the US, and Asia (excluding China), with 1 million units sold through OEM and licensing, leveraging the 60% hub-drive segment of the 48.9 million-unit global eBike market.",
            "bg_color": "#2E2E2E"
        }
    ]

    # Define expected columns and fallback data
    expected_columns_seg = ["Drive System", "Global Market Share", "Indian Market Share", "Key Insights"]
    fallback_data_seg = [
        {"Drive System": "Hub Drive", "Global Market Share": "~60%", "Indian Market Share": "Dominant", "Key Insights": "Low cost, widely adopted"},
        {"Drive System": "Mid-Drive", "Global Market Share": "~40%", "Indian Market Share": "Emerging segment", "Key Insights": "Premium pricing, high efficiency"}
    ]
    expected_columns_pos = ["Hub driven e-bike", "Mid driven e-bike", "PowerPedal driven e-bike"]
    fallback_data_pos = {
        "Cost": ["Low cost", "Expensive", "Slight premium over hub e-bikes(€150-200)"],
        "Performance": ["Poor performance", "Amazing performance", "Amazing performance"],
        "Efficiency": ["Low efficiency", "High efficiency", "High efficiency"],
        "Features": ["No Features", "Usually feature rich", "Feature rich"],
        "Average Price": ["Average price ~ €1,200-1,500", "Average price ~ €3,000-3,500", "Average price ~ €1,400-2,000"]
    }
    df_pos_fallback = pd.DataFrame(fallback_data_pos).T
    df_pos_fallback.index.name = "Attribute"
    expected_columns_market = ["Feature", "Advantage"]
    fallback_data_market = [
        {"Feature": "Bridging the Gap", "Advantage": "Positioned between hub drive (affordable) and mid-drive (high performance)"},
        {"Feature": "Cost-Effective", "Advantage": "2-3x lower price than premium mid-drive systems (Bosch, Bafang)"},
        {"Feature": "High Efficiency", "Advantage": "Achieves mid-drive performance at a slightly higher cost than hub drives"},
        {"Feature": "Retrofittable", "Advantage": "Can be installed on existing hub-driven ebikes without the need to modify frames"}
    ]

    # Load data for each table
    df_seg, error_seg = load_excel_data(
        "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/data/Ebike_Drive_Segmentation_and_Comparison.xlsx",
        expected_columns_seg,
        fallback_data_seg
    )
    df_pos, error_pos = load_excel_data(
        "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/data/E-Bike_Drivetrain_Positioning.xlsx",
        expected_columns_pos,
        df_pos_fallback,
        transpose=False
    )
    if df_pos.shape != (5, 3):
        st.warning(f"Data mismatch in E-Bike Drivetrain Positioning. Expected 5x3 structure, got {df_pos.shape}. Using Excel data with adjustments or fallback.")
        if df_pos.shape == (6, 3):
            df_pos = df_pos.iloc[1:6]
            df_pos.columns = expected_columns_pos
            df_pos.index = df_pos_fallback.index
        else:
            df_pos = df_pos_fallback
    else:
        df_pos.columns = expected_columns_pos
        df_pos.index = df_pos_fallback.index
    df_market, error_market = load_excel_data(
        "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/data/PowerPedal_Market_Positioning.xlsx",
        expected_columns_market,
        fallback_data_market
    )

    # Layout: Centered image at top using columns
    with st.container():
        st.markdown(
            """
            <style>
            .market-opportunity-tab .centered-image {
                display: flex;
                justify-content: center;
                align-items: center;
                width: 100%;
                margin: 0 auto;
                padding: 0;
            }
            .market-opportunity-tab .centered-image img {
                max-width: 1500px;
                width: 100%;
                height: auto;
            }
            /* Scope Streamlit overrides to Market Opportunity tab */
            .market-opportunity-tab .stElementContainer, 
            .market-opportunity-tab .st-emotion-cache-uf99v8, 
            .market-opportunity-tab .st-emotion-cache-1wivap2, 
            .market-opportunity-tab .st-emotion-cache-1r4s1g0 {
                padding: 0 !important;
                margin: 0 !important;
            }
            /* Scope div override to Market Opportunity tab */
            .market-opportunity-tab div {
                margin: 0 !important;
                padding: 0 !important;
            }
            /* Scope caption styling */
            .market-opportunity-tab .stCaption p {
                margin: 0 !important;
                padding: 0 !important;
            }
            .market-opportunity-tab .custom-caption {
                font-size: 12px;
                color: #999999;
                margin: 0 !important;
                padding: 0 !important;
            }
            .market-opportunity-tab .table-viz-container {
                display: flex;
                align-items: flex-start; /* Changed to flex-start for top alignment */
                justify-content: space-between;
                margin: 0 0 -25px 0;
                padding: 0;
                gap: 2px;
                width: 100%;
                min-height: 10px;
                box-sizing: border-box;
            }
            .market-opportunity-tab .table-container {
                flex: 2;
                padding: 0;
                margin: 0;
                display: flex;
                flex-direction: column;
                justify-content: flex-start;
                align-items: flex-start;
                min-height: 10px;
            }
            .market-opportunity-tab .viz-container {
                flex: 1;
                padding: 0;
                margin: 0;
                display: flex;
                flex-direction: column;
                justify-content: flex-start; /* Changed to flex-start for top alignment */
                align-items: center;
                min-height: 10px;
                box-sizing: border-box;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            st.markdown('<div class="centered-image">', unsafe_allow_html=True)
            try:
                st.image(
                    "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/market.png",
                    use_container_width=False,
                    width=1500
                )
            except FileNotFoundError:
                st.error("Image not found at: https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/market.png")
                st.markdown(
                    """
                    <div style="text-align: center; border: 1px solid #e6e6e6; border-radius: 10px; padding: 5px; background-color: #f0f0f0; margin: 0;">
                        <p style="color: #555; margin: 0;">Placeholder: No image available for market.png</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            st.markdown('</div>', unsafe_allow_html=True)

    # Content below image in a single container
    with st.container():
        st.markdown("<div style='margin: 0; padding: 0; margin-bottom: -25px;'>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown(
                """
                <div style="display: flex; justify-content: flex-start; margin: 0; padding: 0;">
                    <div class="svg-container" style="position: relative; width: 900px; height: 600px;">
                        <svg width="900" height="600" viewBox="-450 -300 1000 600">
                            <circle id="pam" cx="0" cy="0" r="300" fill="#3E3F29" opacity="0.7"></circle>
                            <circle id="tam" cx="0" cy="0" r="220" fill="#819067" opacity="0.7"></circle>
                            <circle id="sam" cx="0" cy="0" r="140" fill="#A08963" opacity="0.7"></circle>
                            <circle id="som" cx="0" cy="0" r="60" fill="#2E2E2E" opacity="0.7"></circle>
                            <text x="0" y="-250" text-anchor="middle" font-size="34" fill="#e0e0e0" font-weight="bold">PAM</text>
                            <text x="0" y="-160" text-anchor="middle" font-size="30" fill="#e0e0e0">TAM</text>
                            <text x="0" y="-85" text-anchor="middle" font-size="26" fill="#e0e0e0">SAM</text>
                            <text x="0" y="-20" text-anchor="middle" font-size="24" fill="#e0e0e0">SOM</text>
                            <text x="0" y="270" text-anchor="middle" font-size="30" fill="#000000" font-weight="bold">$50.8B</text>
                            <text x="0" y="190" text-anchor="middle" font-size="26" fill="#000000" font-weight="bold">$7.16B</text>
                            <text x="0" y="105" text-anchor="middle" font-size="22" fill="#000000" font-weight="bold">$2.7B</text>
                            <text x="0" y="20" text-anchor="middle" font-size="20" fill="#000000" font-weight="bold">$0.25B</text>
                        </svg>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            selected_market = st.selectbox("Select Market Segment", [data["title"] for data in market_data])
            if selected_market != st.session_state.get("selected_market"):
                st.session_state.selected_market = selected_market

            st.markdown(
                """
                <div style='padding: 0; margin: 0;'>
                    <p style='color: #e0e0e0; font-size: 16px; margin: 0 0 2px 0;'>Market Overview:</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            for market in market_data:
                container_class = "market-container active" if st.session_state.get("selected_market") == market["title"] else "market-container"
                if st.session_state.get("selected_market") == market["title"]:
                    st.markdown(
                        f"""
                        <div class='{container_class}' style='background-color: {market["bg_color"]}; border-radius: 10px; text-align: center; padding: 10px; margin: 0 0 2px 0;'>
                            <h4 style='color: #e0e0e0; margin: 0 0 2px 0;'>{market["title"]}</h4>
                            <p style='color: #000000; font-size: 18px; font-weight: bold; margin: 0 0 2px 0;'>{market["value"]}</p>
                            <p style='color: #e0e0e0; font-size: 14px; margin: 0 0 2px 0;'>{market["title"]} Description</p>
                            <p style='color: #e0e0e0; font-size: 14px; margin: 0;'>{market["full_desc"]}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    if market["title"] == "SOM":
                        st.subheader("PowerPedal's 2025–30 Market Target")
                        st.markdown(
                            """
                            <p style='color: #4caf50; font-size: 18px; font-weight: bold; text-align: center; margin: 0 0 2px 0;'>
                                PowerPedal’s 2025–30 Goal: 1M Units, 9% of Non-China Hub-Drive Market
                            </p>
                            """,
                            unsafe_allow_html=True
                        )
                        fig, (ax_bar, ax_pie) = plt.subplots(1, 2, figsize=(6, 3), gridspec_kw={'width_ratios': [3, 2.3]})
                        fig.patch.set_facecolor('none')
                        ax_bar.set_facecolor('none')
                        ax_pie.set_facecolor('none')

                        labels = ['Global eBike', 'Hub-Drive', 'Non-China', 'PowerPedal']
                        values = [48.9, 29.34, 11, 1]
                        colors = ['#1B263B', '#2A4066', '#415A77', "#156d17"]
                        y_pos = np.arange(len(labels))

                        for i, (label, value, color) in enumerate(zip(labels, values, colors)):
                            bar = ax_bar.barh(y_pos[i], value, color=color, edgecolor='#1e1e1e', linewidth=1.5, zorder=2)
                            ax_bar.barh(y_pos[i], value, color='#000000', alpha=0.2, left=0.2, zorder=1)
                            if value > 5:
                                ax_bar.text(value * 0.4, y_pos[i], f'{label}\n{value}M',
                                            ha='center', va='center', color='#e0e0e0', fontsize=7, fontweight='bold')
                            else:
                                ax_bar.text(value + 0.5, y_pos[i], f'{label}\n{value}M',
                                            ha='left', va='center', color='#e0e0e0', fontsize=7, fontweight='bold')

                        ax_bar.set_xlim(0, 55)
                        ax_bar.set_yticks([])
                        ax_bar.invert_yaxis()
                        ax_bar.axis('off')

                        sizes = [9, 91]
                        labels_pie = ['PowerPedal (9%)', 'Rest (91%)']
                        colors_pie = ['#156d17', "#E3FF9D"]
                        explode = (0.2, 0)
                        ax_pie.pie(sizes, explode=explode, labels=labels_pie, colors=colors_pie, startangle=90,
                                   autopct='%1.0f%%', textprops={'color': '#e0e0e0', 'fontsize': 6},
                                   wedgeprops={'edgecolor': '#1e1e1e', 'linewidth': 1})
                        ax_pie.axis('equal')
                        ax_pie.legend(labels_pie, loc="best", fontsize=6, frameon=False, labelcolor='#e0e0e0')

                        plt.tight_layout(pad=0.2)
                        st.pyplot(fig)

                        st.markdown(
                            """
                            <p style='color: #e0e0e0; font-size: 14px; text-align: right; margin: 0;'>
                                9% Target = 1M Units of 11M Non-China Hub-Drive Market<br>
                                Leveraging 60% hub-drive share of 48.9M-unit global eBike market
                            </p>
                            """,
                            unsafe_allow_html=True
                        )

        # Add CSS for table-visual alignment, scoped to Market Opportunity tab
        st.markdown(
            """
            <style>
            .market-opportunity-tab .table-viz-container {
                display: flex;
                align-items: flex-start; /* Changed to flex-start for top alignment */
                justify-content: space-between;
                margin: 0 0 -25px 0;
                padding: 0;
                gap: 2px;
                width: 100%;
                min-height: 10px;
                box-sizing: border-box;
            }
            .market-opportunity-tab .table-container {
                flex: 2;
                padding: 0;
                margin: 0;
                display: flex;
                flex-direction: column;
                justify-content: flex-start;
                align-items: flex-start;
                min-height: 10px;
            }
            .market-opportunity-tab .viz-container {
                flex: 1;
                padding: 0;
                margin: 0;
                display: flex;
                flex-direction: column;
                justify-content: flex-start; /* Changed to flex-start for top alignment */
                align-items: center;
                min-height: 10px;
                box-sizing: border-box;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Helper function to clean market share values
        def clean_share(s):
            if isinstance(s, str):
                cleaned = s.replace('~', '').replace('%', '').replace(' ', '').strip()
                try:
                    return float(cleaned)
                except ValueError:
                    if "Dominant" in s:
                        return 99.0
                    elif "Emerging" in s:
                        return 1.0
                    return 0.0
            return float(s) if isinstance(s, (int, float)) else 0.0

        # Tables and Visualizations Section
        # Table 1: Ebike Drive Segmentation and Comparison
        st.markdown('<div class="table-viz-container">', unsafe_allow_html=True)
        col_table1, col_viz1 = st.columns([2, 1])
        with col_table1:
            st.markdown('<div class="table-container">', unsafe_allow_html=True)
            st.markdown(create_html_table(df_seg, "Ebike Drive Segmentation and Comparison"), unsafe_allow_html=True)
            if error_seg:
                st.warning(error_seg)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_viz1:
            st.markdown('<div class="viz-container">', unsafe_allow_html=True)
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(4, 2.5))
            fig.patch.set_facecolor('none')
            ax1.set_facecolor('none')
            ax2.set_facecolor('none')

            labels = df_seg['Drive System']
            global_share = [clean_share(s) for s in df_seg['Global Market Share']]
            indian_share = [clean_share(s) for s in df_seg['Indian Market Share']]

            ax1.pie(global_share, labels=labels, colors=['#415A77', '#A08963'], autopct='%1.0f%%',
                    textprops={'color': '#e0e0e0', 'fontsize': 6}, wedgeprops={'edgecolor': '#1e1e1e', 'linewidth': 1})
            ax1.set_title('Global Market', fontsize=8, color='#e0e0e0')
            ax2.pie(indian_share, labels=labels, colors=['#78C841', '#E3FF9D'], autopct='%1.0f%%',
                    textprops={'color': '#e0e0e0', 'fontsize': 6}, wedgeprops={'edgecolor': '#1e1e1e', 'linewidth': 1})
            ax2.set_title('Indian Market', fontsize=8, color='#e0e0e0')

            plt.tight_layout(pad=0.2)
            st.pyplot(fig)
            st.markdown(
                """
                <p style='color: #78C841; font-size: 15px; text-align: center; margin: 0;'>
                    Global and Indian market shares for Hub Drive and Mid-Drive e-bikes.
                </p>
                """,
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Table 2: E-Bike Drivetrain Positioning
        st.markdown('<div class="table-viz-container">', unsafe_allow_html=True)
        col_table2, col_viz2 = st.columns([2, 1])
        with col_table2:
            st.markdown('<div class="table-container">', unsafe_allow_html=True)
            if not all(col in df_pos.columns for col in expected_columns_pos):
                st.warning(f"Missing columns in E-Bike Drivetrain Positioning: {expected_columns_pos}. Using adjusted data.")
                df_pos = df_pos.reindex(columns=expected_columns_pos, fill_value="")
            st.markdown(create_html_table(df_pos, "E-Bike Drivetrain Positioning"), unsafe_allow_html=True)
            if error_pos:
                st.warning(error_pos)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_viz2:
            st.markdown('<div class="viz-container">', unsafe_allow_html=True)
            # Grouped bar chart for E-Bike Drivetrain Positioning, excluding Average Price
            labels = [label for label in df_pos.index.tolist() if label != "Average Price"]
            categories = df_pos.columns.tolist()

            value_map = {
                'Low cost': 1, 'Slight premium over hub e-bikes(€150-200)': 2, 'Expensive': 3,
                'Poor performance': 1, 'Amazing performance': 3,
                'Low efficiency': 1, 'High efficiency': 3,
                'No Features': 1, 'Feature rich': 3, 'Usually feature rich': 3,
            }

            data = []
            for cat in categories:
                values = [value_map.get(str(df_pos.loc[attr, cat]), 1) for attr in labels]
                data.append(values)

            fig, ax = plt.subplots(figsize=(6, 3.5))  # Adjusted size for better layout
            fig.patch.set_facecolor('none')
            ax.set_facecolor('none')

            bar_width = 0.25
            x = np.arange(len(labels))
            colors = ['#415A77', '#78C841', '#156d17']

            for i, (cat_data, category, color) in enumerate(zip(data, categories, colors)):
                ax.bar(x + i * bar_width, cat_data, bar_width, color=color, edgecolor='#1e1e1e')

            ax.set_xticks(x + bar_width)
            ax.set_xticklabels(labels, fontsize=10, color='#e0e0e0', rotation=45, ha='right')
            ax.set_yticks([1, 2, 3])
            ax.set_yticklabels(['Low', 'Medium', 'High'], fontsize=10, color='#e0e0e0')
            ax.set_title('Drivetrain Comparison', fontsize=12, color='#e0e0e0')
            # Removed ax.legend() to avoid overlap
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#e0e0e0')
            ax.spines['bottom'].set_color('#e0e0e0')
            plt.tight_layout(pad=0.5)

            # Add custom legend above the graph
            st.markdown(
                """
                <div style='display: flex; justify-content: center; gap: 20px; margin-bottom: 10px;'>
                    <div style='display: flex; align-items: center;'>
                        <div style='width: 12px; height: 12px; background-color: #415A77; margin-right: 5px;'></div>
                        <span style='color: #e0e0e0; font-size: 12px;'>Hub driven e-bike</span>
                    </div>
                    <div style='display: flex; align-items: center;'>
                        <div style='width: 12px; height: 12px; background-color: #78C841; margin-right: 5px;'></div>
                        <span style='color: #e0e0e0; font-size: 12px;'>Mid driven e-bike</span>
                    </div>
                    <div style='display: flex; align-items: center;'>
                        <div style='width: 12px; height: 12px; background-color: #156d17; margin-right: 5px;'></div>
                        <span style='color: #e0e0e0; font-size: 12px;'>PowerPedal driven e-bike</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.pyplot(fig)
            st.markdown(
                """
                <p style='color: #78C841; font-size: 15px; text-align: center; margin: 0;'>
                    Comparison of drivetrain attributes across Hub, Mid, and PowerPedal systems.
                </p>
                """,
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Table 3: PowerPedal’s Market Positioning
        st.markdown('<div class="table-viz-container">', unsafe_allow_html=True)
        col_table3, col_viz3 = st.columns([2, 1])
        with col_table3:
            st.markdown('<div class="table-container">', unsafe_allow_html=True)
            st.markdown(create_html_table(df_market, "PowerPedal’s Market Positioning"), unsafe_allow_html=True)
            if error_market:
                st.warning(error_market)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_viz3:
            st.markdown('<div class="viz-container">', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(4, 2.5))
            fig.patch.set_facecolor('none')
            ax.set_facecolor('none')

            features = df_market['Feature']
            scores = [5, 4, 3, 3]
            max_score = 5
            y_pos = np.arange(len(features))
            colors = ['#78C841', '#156d17', '#A08963', '#415A77']

            bars = ax.barh(y_pos, scores, color=colors, edgecolor='#1e1e1e', height=0.4)
            ax.barh(y_pos, max_score, color='#e0e0e0', alpha=0.2, height=0.4, zorder=-1)

            for bar, score in zip(bars, scores):
                ax.text(score + 0.1, bar.get_y() + bar.get_height() / 2, f'{score}',
                        va='center', ha='left', color='#e0e0e0', fontsize=8)

            ax.set_yticks(y_pos)
            ax.set_yticklabels(features, fontsize=8, color='#e0e0e0')
            ax.set_xticks([0, 1, 3, 5])
            ax.set_xticklabels(['', 'Low', 'Medium', 'High'], fontsize=8, color='#e0e0e0')
            ax.set_xlim(0, max_score + 0.5)
            ax.set_title('PowerPedal Feature Strengths', fontsize=10, color='#e0e0e0')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#e0e0e0')
            ax.spines['bottom'].set_color('#e0e0e0')
            plt.tight_layout(pad=0.2)
            st.pyplot(fig)
            st.markdown(
                """
                <p style='color: #78C841; font-size: 15px; text-align: center; margin: 0;'>
                    PowerPedal’s feature strengths compared to an ideal score of 5.
                </p>
                """,
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Final caption with CSS styling
    st.markdown(
        """
        <style>
        .market-opportunity-tab .custom-caption {
            font-size: 12px;
            color: #999999;
            margin: 0 !important;
            padding: 0 !important;
        }
        </style>
        <p class="custom-caption">Data based on market research and internal projections as of 2025.</p>
        """,
        unsafe_allow_html=True
    )

# ---- TAB 4: PowerPedal – The Product ----
with tabs[3]:
    # Header aligned to the left
    st.header("Meet PowerPedal")
    st.caption("The Smart, Affordable, and High-Performance eBike Drive System")

    # CSS for Product Tab
    st.markdown(
        """
        <style>
        .product-tab .banner-container {
            text-align: center;
            margin-bottom: 20px;
        }
        .product-tab .banner-image {
            max-width: 800px;
            width: 100%;
            height: auto;
            border-radius: 12px;
            transition: transform 0.3s ease;
        }
        .product-tab .banner-image:hover {
            transform: scale(1.02);
        }
        .product-tab .banner-tagline {
            color: #FFF5F2;
            font-size: 22px;
            font-weight: 600;
            text-align: center;
            margin-top: 10px;
            background: linear-gradient(45deg, #1B3C53, #78C841);
            padding: 10px 20px;
            border-radius: 8px;
            display: inline-block;
        }
        .product-tab .overview {
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background: linear-gradient(135deg, #1B3C53, #2e2e2e);
            border: 2px solid #78C841;
            border-radius: 12px;
            color: #FFF5F2;
            text-align: center;
        }
        .product-tab .tab-container {
            margin-top: 20px;
        }
        .tab-content {
            padding: 20px;
        }
        .tab-content .component-container {
            background: linear-gradient(135deg, #1B3C53, #2e2e2e);
            border: 2px solid #78C841;
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
            display: flex;
            flex-direction: row;
            align-items: flex-start;
            justify-content: flex-start;
            gap: 20px;
            min-height: 150px;
        }
        .tab-content h3 {
            font-size: 24px;
            color: #78C841;
            margin: 0 0 10px 0;
        }
        .tab-content p {
            font-size: 16px;
            line-height: 1.6;
            margin: 0;
            color: #A8F1FF;
            text-align: left;
        }
        .tab-content .image-container {
            flex: 0 0 150px;
            margin-right: 20px;
            display: flex;
            align-items: flex-start;
            justify-content: center;
        }
        .tab-content .image-container img {
            max-width: 150px;
            width: 150px;
            height: auto;
            border-radius: 8px;
        }
        .tab-content .text-container {
            flex: 1;
            min-width: 200px;
        }
        .test-lab {
            margin: 20px auto;
            padding: 20px;
            background: linear-gradient(135deg, #1B3C53, #2e2e2e);
            border: 2px solid #78C841;
            border-radius: 12px;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            max-width: 500px;
            width: 100%;
        }
        .test-lab h3 {
            color: #78C841;
            font-size: 24px;
            margin-bottom: 15px;
        }
        .test-lab-link {
            display: inline-block;
            padding: 10px 20px;
            background: linear-gradient(45deg, #78C841, #A8F1FF);
            color: #000000 !important;
            text-decoration: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: 600;
            transition: transform 0.3s ease, background 0.3s ease;
        }
        .test-lab-link:hover {
            transform: scale(1.05);
            background: linear-gradient(45deg, #A8F1FF, #78C841);
            color: #000000 !important;
        }
        .video-section {
            margin-top: 20px;
        }
        .video-section .video-header {
            text-align: center;
            margin-bottom: 20px;
        }
        .video-section .video-header h3 {
            color: #78C841;
            font-size: 24px;
            margin: 0;
        }
        .video-section .video-item {
            margin-bottom: 20px;
            padding: 10px;
            background: #2e2e2e;
            border-radius: 8px;
            border: 1px solid #78C841;
        }
        .video-section .video-item h4 {
            color: #78C841;
            font-size: 20px;
            margin-bottom: 5px;
        }
        .video-section .video-item p {
            color: #A8F1FF;
            font-size: 14px;
            margin: 0;
        }
        .app-section {
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
            flex-wrap: wrap;
            gap: 20px;
        }
        .app-section .expander-container {
            flex: 1;
            margin: 0 10px;
            min-width: 300px;
            max-width: 400px;
        }
        .app-section .highlight-expander {
            flex: 1;
            margin: 0 10px;
            min-width: 300px;
            max-width: 800px; /* Wider when expanded */
            background: linear-gradient(135deg, #2e2e2e, #1B3C53);
            border: 3px solid #A8F1FF !important;
            border-radius: 12px;
            box-shadow: 0 0 10px rgba(120, 200, 65, 0.5);
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 10px rgba(120, 200, 65, 0.5); }
            50% { box-shadow: 0 0 20px rgba(120, 200, 65, 0.8); }
            100% { box-shadow: 0 0 10px rgba(120, 200, 65, 0.5); }
        }
        .app-section .component-container {
            display: flex;
            flex-direction: row;
            align-items: flex-start;
            gap: 20px;
            padding: 15px;
            background: linear-gradient(135deg, #1B3C53, #2e2e2e);
            border: 2px solid #78C841;
            border-radius: 12px;
        }
        .app-section .image-container {
            flex: 0 0 150px;
            display: flex;
            align-items: flex-start;
            justify-content: center;
        }
        .app-section .image-container img {
            max-width: 150px;
            width: 150px;
            height: auto;
            border-radius: 8px;
        }
        .app-section .text-container {
            flex: 1;
            min-width: 150px;
            padding-right: 10px;
        }
        .app-section h3 {
            font-size: 20px;
            color: #78C841;
            margin: 0 0 10px 0;
        }
        .app-section p {
            font-size: 14px;
            line-height: 1.5;
            color: #A8F1FF;
            margin: 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Banner with Main Picture
    st.markdown('<div class="product-tab">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown('<div class="banner-container">', unsafe_allow_html=True)
        product_image_path = os.path.abspath("https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/product.png")
        if os.path.exists(product_image_path):
            st.image(product_image_path, use_container_width=True)
            st.markdown(
                '<div class="banner-tagline">Mid-drive experience. Rear hub affordability.</div>',
                unsafe_allow_html=True
            )
        else:
            st.warning(f"Image not found: {product_image_path}")
            st.markdown(
                """
                <div style="text-align: center; border: 1px solid #e6e6e6; border-radius: 10px; padding: 20px; background-color: #f0f0f0;">
                    <p style="color: #555;">Placeholder: No image available for product.png</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # Overview
    st.markdown('<div class="overview">', unsafe_allow_html=True)
    st.markdown(
        """
        PowerPedal is a revolutionary eBike drive system that combines mid-drive performance with rear hub affordability. 
        Designed for efficiency and compatibility, it offers a seamless riding experience with advanced torque-sensing technology.
        """
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Tab Container with 4 Sections
    st.markdown('<div class="tab-container">', unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["Power Sensor", "Controller", "HMI Control Unit", "Mobile App"])

    with tab1:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
        with col_img2:
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            image_path = os.path.abspath("https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/powersense.png")
            if os.path.exists(image_path):
                st.image(image_path, caption="Power Sensor")
            else:
                st.warning(f"Image not found: {image_path}")
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="component-container">', unsafe_allow_html=True)
        st.markdown('<h3>Power Sensor – The “muscle detector” of the rider’s eBike</h3>', unsafe_allow_html=True)
        st.markdown(
            '<p>Picture a clever little device tucked inside the rider’s pedal system—the PowerPedal Power Sensor—measuring every bit of force applied with stunning ±2% accuracy. In less than 10 milliseconds, it whisks this data to the controller, painting a vivid picture of the rider’s journey. Unlike basic cadence-based systems that merely tally pedal spins, this sensor knows whether the rider is gliding effortlessly or conquering a steep hill, ensuring the motor responds instantly with just the right boost. Say goodbye to jerky starts or wasted battery—every ride becomes a smooth, natural dance with the road!</p>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
        with col_img2:
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            image_path = os.path.abspath("https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/powerdrive.png")
            if os.path.exists(image_path):
                st.image(image_path, caption="Controller")
            else:
                st.warning(f"Image not found: {image_path}")
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="component-container">', unsafe_allow_html=True)
        st.markdown('<h3>Controller – The brain that makes split-second decisions</h3>', unsafe_allow_html=True)
        st.markdown(
            '<p>Step into the mind of the rider’s eBike with the Controller—a brilliant brain processing live data from the power sensor, battery, and motor hundreds of times per second. It calculates torque, speed, and efficiency, delivering a power-packed 250W to 350W of assistance with a 1:1 to 3:1 ratio—meaning it can amplify the rider’s effort up to three times! Hills and headwinds melt away, doubling the rider’s range on a single charge. This versatile genius works with nearly any eBike motor, hub or mid-drive, and its remote diagnostics let the support team troubleshoot or fix issues online.</p>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
        with col_img2:
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            image_path = os.path.abspath("https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/powershift.png")
            if os.path.exists(image_path):
                st.image(image_path, caption="HMI Control Unit")
            else:
                st.warning(f"Image not found: {image_path}")
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="component-container">', unsafe_allow_html=True)
        st.markdown('<h3>HMI (Human–Machine Interface) – The rider’s handlebar command center</h3>', unsafe_allow_html=True)
        st.markdown(
            '<p>Meet the HMI, the rider’s sleek handlebar command center that puts control in their hands. Twist the throttle for 0–100% variable control—though OEM-set speed limits keep it safe—and flip the assist level selector from eco cruising to a full-power boost. A battery State of Charge indicator, accurate to ±1%, reveals the rider’s range at a glance, while the horn switch delivers quick safety alerts in traffic. Plus, the built-in USB port powers the rider’s lights or charges their phone mid-ride—it’s a multitasking marvel!</p>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        # Mobile App Section with Dropdowns
        st.markdown('<div class="app-section">', unsafe_allow_html=True)

        # First row of expanders
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            with st.expander("Ride Dashboard 📊", expanded=st.session_state.get('ride_dashboard_expanded', False)):
                st.markdown('<div class="component-container">', unsafe_allow_html=True)
                st.markdown('<h3>Ride Dashboard – The rider’s live stats hub</h3>', unsafe_allow_html=True)
                col_img, col_text = st.columns([2, 3])
                with col_img:
                    st.markdown('<div class="image-container">', unsafe_allow_html=True)
                    image_path = os.path.abspath("https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/app_live.jpg")
                    if os.path.exists(image_path):
                        st.image(image_path, caption="Ride Dashboard", width=150, output_format="PNG", channels="RGB")
                    else:
                        st.warning(f"Image not found: {image_path}")
                    st.markdown('</div>', unsafe_allow_html=True)
                with col_text:
                    st.markdown('<div class="text-container">', unsafe_allow_html=True)
                    st.markdown(
                        '<p>Step into the rider’s cockpit with the Ride Dashboard—a dynamic hub that brings the journey to life. Watch current speed, assist level, battery percentage (accurate to ±1%), pedal force, and estimated range refresh in under a second, mirroring every twist and turn in real time. No need to glance down at the hardware HMI—this keeps the rider’s effort and battery perfectly in sync, letting them focus on the road ahead!</p>',
                        unsafe_allow_html=True
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            with st.expander("Ride History 📜", expanded=st.session_state.get('ride_history_expanded', False)):
                st.markdown('<div class="component-container">', unsafe_allow_html=True)
                st.markdown('<h3>Ride History – The rider’s cycling time machine</h3>', unsafe_allow_html=True)
                col_img, col_text = st.columns([2, 3])
                with col_img:
                    st.markdown('<div class="image-container">', unsafe_allow_html=True)
                    image_path = os.path.abspath("https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/app_ride_history.jpg")
                    if os.path.exists(image_path):
                        st.image(image_path, caption="Ride History", width=150, output_format="PNG", channels="RGB")
                    else:
                        st.warning(f"Image not found: {image_path}")
                    st.markdown('</div>', unsafe_allow_html=True)
                with col_text:
                    st.markdown('<div class="text-container">', unsafe_allow_html=True)
                    st.markdown(
                        '<p>Unlock the rider’s past with the Ride History—a magical scroll of every adventure. Dive into details like distance, duration, average speed, calories burned, and total elevation gain, all neatly organized by date. With week or month filters at the rider’s fingertips, they can trace progress or relive the best rides, turning every pedal stroke into a story worth telling!</p>',
                        unsafe_allow_html=True
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        with col3:
            with st.expander("Performance Analytics 📈", expanded=st.session_state.get('performance_analytics_expanded', False)):
                st.markdown('<div class="component-container">', unsafe_allow_html=True)
                st.markdown('<h3>Performance Analytics – For the data-driven rider</h3>', unsafe_allow_html=True)
                col_img, col_text = st.columns([2, 3])
                with col_img:
                    st.markdown('<div class="image-container">', unsafe_allow_html=True)
                    image_path = os.path.abspath("https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/app_analytics.jpg")
                    if os.path.exists(image_path):
                        st.image(image_path, caption="Performance Analytics", width=150, output_format="PNG", channels="RGB")
                    else:
                        st.warning(f"Image not found: {image_path}")
                    st.markdown('</div>', unsafe_allow_html=True)
                with col_text:
                    st.markdown('<div class="text-container">', unsafe_allow_html=True)
                    st.markdown(
                        '<p>Embark on a data adventure for the rider with Performance Analytics—where graphs and charts unravel the secrets of their ride. Explore power output patterns, battery efficiency over time, and assistance usage across terrains, with the app spotlighting the rider’s most efficient rides. It’s like having a coach in the rider’s pocket, guiding them to ride smarter with every journey!</p>',
                        unsafe_allow_html=True
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        # Second row of expanders
        st.markdown('<div class="app-section">', unsafe_allow_html=True)
        col4, col5, col6 = st.columns([1, 1, 1])

        with col4:
            with st.expander("Settings & Profiles ⚙️", expanded=st.session_state.get('settings_profiles_expanded', False)):
                st.markdown('<div class="component-container">', unsafe_allow_html=True)
                st.markdown('<h3>Settings & Profiles – The rider’s bike, their rules</h3>', unsafe_allow_html=True)
                col_img, col_text = st.columns([2, 3])
                with col_img:
                    st.markdown('<div class="image-container">', unsafe_allow_html=True)
                    st.markdown('<p>No image available</p>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                with col_text:
                    st.markdown('<div class="text-container">', unsafe_allow_html=True)
                    st.markdown(
                        '<p>Take the reins for the rider with Settings & Profiles—their personal command center. Tweak assist levels, sculpt power delivery curves, set speed limits (within OEM-defined max), and activate battery-saving modes. For riders with multiple eBikes, store profiles for each and switch between them in an instant—it’s like tailoring the ride to the rider’s every whim!</p>',
                        unsafe_allow_html=True
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        with col5:
            with st.expander("Remote Diagnostics 🛠" + "\u00A0" * 20 + "Key Feature ⭐", expanded=st.session_state.get('remote_diagnostics_expanded', False)):
                st.markdown('<div class="component-container highlight-expander">', unsafe_allow_html=True)
                st.markdown(
                    '<h3>Remote Diagnostics (AI-Powered & Monetizable) – The rider’s bike’s personal mechanic in their pocket</h3>',
                    unsafe_allow_html=True
                )
                col_img, col_text = st.columns([2, 3])
                with col_img:
                    st.markdown('<div class="image-container">', unsafe_allow_html=True)
                    image_path = os.path.abspath("https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/app_diagnostic.jpg")
                    if os.path.exists(image_path):
                        st.image(image_path, caption="Remote Diagnostics", width=150, output_format="PNG", channels="RGB")
                    else:
                        st.warning(f"Image not found: {image_path}")
                    st.markdown('</div>', unsafe_allow_html=True)
                with col_text:
                    st.markdown('<div class="text-container">', unsafe_allow_html=True)
                    st.markdown(
                        '<p>Meet the rider’s bike’s guardian angel—the Remote Diagnostics system, a pocket-sized mechanic powered by AI. It doesn’t just spot faults; it learns from ride data, sensor readings, and trends across thousands of eBikes, catching early warnings like torque sensor drift or motor temperature spikes before the rider notices. When an issue arises, it notifies the rider with a clear explanation and actions, sends technical reports to technicians for remote fixes, and suggests preventive maintenance based on the rider’s actual usage—not guesses.</p>',
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        '<p>We’re training certified technicians to use this remotely or in the field, making repairs faster and smarter. This platform is a standalone product—OEMs, fleets, and service centers can subscribe to our diagnostics API and dashboard to manage hundreds or thousands of bikes. Monetization shines with free basics for riders, premium AI alerts by subscription, OEM licensing fees, and fleet monitoring per bike.</p>',
                        unsafe_allow_html=True
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        with col6:
            with st.expander("Updates & Notifications 🔔", expanded=st.session_state.get('updates_notifications_expanded', False)):
                st.markdown('<div class="component-container">', unsafe_allow_html=True)
                st.markdown('<h3>Updates & Notifications – Keeping the rider’s bike future-ready</h3>', unsafe_allow_html=True)
                col_img, col_text = st.columns([2, 3])
                with col_img:
                    st.markdown('<div class="image-container">', unsafe_allow_html=True)
                    st.markdown('<p>No image available</p>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                with col_text:
                    st.markdown('<div class="text-container">', unsafe_allow_html=True)
                    st.markdown(
                        '<p>Step into the future for the rider with Updates & Notifications—their gateway to a smarter bike. Firmware updates flow through the app, unlocking new features and optimizations without ever touching the hardware. Stay ahead with maintenance reminders, battery care tips, and celebratory milestones, all delivered right to the rider’s screen—it’s like having a personal bike concierge!</p>',
                        unsafe_allow_html=True
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Test Lab Section
    st.container()
    st.markdown(
        """
        <div class="test-lab">
            <h3>Test Lab</h3>
            <a href="https://powerpedaltestdashboard-4tmrensx9crg9j7ezjytog.streamlit.app/" 
               target="_blank" class="test-lab-link">Visit PowerPedal Test Dashboard</a>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Test Videos Section
    st.markdown(
        """
        <div class="video-section">
            <div class="video-header">
                <h3>Test Videos</h3>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Video Section with Side-by-Side Layout
    st.markdown('<div class="video-section">', unsafe_allow_html=True)
    video_dir = os.path.dirname(__file__)  # Use relative directory

    col1, col2 = st.columns(2)  # Two columns for side-by-side videos

    with col1:
        video_path1 = os.path.join(video_dir, "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/videos/powerpedal_efficiency_testing.mp4")
        if os.path.exists(video_path1):
            st.markdown('<div class="video-item">', unsafe_allow_html=True)
            st.markdown('<h4>Efficiency Testing</h4>', unsafe_allow_html=True)
            st.markdown(
                '<p>Explore how PowerPedal optimizes energy use across various riding conditions, showcasing its superior efficiency and range extension.</p>',
                unsafe_allow_html=True
            )
            st.video(video_path1, start_time=0, width=300)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning(f"Video not found: {video_path1}")

    with col2:
        video_path2 = os.path.join(video_dir, "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/videos/powerpedal_terrain_testing.mp4")
        if os.path.exists(video_path2):
            st.markdown('<div class="video-item">', unsafe_allow_html=True)
            st.markdown('<h4>Terrain Testing</h4>', unsafe_allow_html=True)
            st.markdown(
                '<p>Witness PowerPedal’s performance across diverse terrains, from steep hills to rough trails, proving its versatility and durability.</p>',
                unsafe_allow_html=True
            )
            st.video(video_path2, start_time=0, width=300)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning(f"Video not found: {video_path2}")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

import os
import streamlit as st

# Define helper at the top
@st.cache_resource
def load_image(image_path):
    if os.path.exists(image_path):
        return image_path
    return None

# ---- TAB 5: Business Model ----
with tabs[4]:
    # Top Section: Title & Tagline
    st.markdown(
        """
        <div class="business-model-header">
            <h2>Business Model</h2>
            <p class="tagline">From hardware to recurring revenue — designed for scale.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # CSS for styling expanders
    st.markdown(
        """
        <style>
        .business-model-header {
            text-align: center;
            margin: 20px auto;
            max-width: 800px;
        }
        .business-model-header h2 {
            color: #78C841;
            font-size: 32px;
            font-weight: 600;
            margin: 0 0 10px 0;
        }
        .business-model-header .tagline {
            color: #A8F1FF;
            font-size: 18px;
            font-weight: 400;
            margin: 0;
        }
        .business-model-section {
            display: flex;
            justify-content: space-around;
            margin: 20px 0;
            flex-wrap: wrap;
            gap: 20px;
        }
        .business-model-section .expander-container {
            flex: 1;
            margin: 0 10px;
            min-width: 300px;
            max-width: 400px;
        }
        .business-model-section .component-container {
            padding: 15px;
            background: linear-gradient(135deg, #1B3C53, #2e2e2e);
            border: 2px solid #78C841;
            border-radius: 12px;
        }
        .business-model-section h3 {
            font-size: 20px;
            color: #78C841;
            margin: 10px 0;
        }
        .business-model-section p {
            font-size: 14px;
            line-height: 1.5;
            color: #A8F1FF;
            margin: 5px 0;
        }
        .impact-statement {
            text-align: center;
            margin: 20px auto;
            max-width: 800px;
        }
        .impact-statement p {
            color: #A8F1FF;
            font-size: 18px;
            font-weight: 400;
            margin: 0;
        }
        /* Hide Streamlit's keyboard navigation hints */
        [data-testid="stTooltip"] {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Middle Section: 2 Expanders (Training removed)
    st.markdown('<div class="business-model-section">', unsafe_allow_html=True)

    with st.expander("Hardware Sales 💰", expanded=False):
        st.markdown('<div class="component-container">', unsafe_allow_html=True)
        st.markdown("<h3>Hardware Sales</h3>", unsafe_allow_html=True)
        st.markdown("<p>🛠 Sold in bulk to OEMs as the core revenue driver.</p>", unsafe_allow_html=True)
        st.markdown("<p>📦 Each PowerPedal system is a premium, one-time purchase.</p>", unsafe_allow_html=True)
        st.markdown(
            """
            <p>
            At the heart of PowerPedal’s business model is hardware sales to eBike OEMs. 
            Our PowerPedal system — including the sensor, controller, and HMI — is supplied directly 
            to manufacturers for seamless integration into their eBike models. 
            This OEM-first approach ensures predictable, scalable revenue, 
            while positioning our technology as part of the bike’s DNA rather than an add-on.
            </p>
            """,
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("AI Diagnostics Subscription 📈", expanded=False):
        st.markdown('<div class="component-container">', unsafe_allow_html=True)
        st.markdown("<h3>AI Diagnostics Subscription</h3>", unsafe_allow_html=True)
        st.markdown("<p>🤖 Remote monitoring, predictive maintenance, and troubleshooting.</p>", unsafe_allow_html=True)
        st.markdown("<p>💳 Monthly per-bike fee — keeps bikes running and customers happy.</p>", unsafe_allow_html=True)
        st.markdown(
            """
            <p>
            Once our hardware is in the field, we expand the value chain through AI-powered Remote Diagnostics. 
            OEMs, dealers, and fleet operators can subscribe to our service for real-time health monitoring, 
            predictive maintenance alerts, and data-driven performance optimization. 
            These subscriptions create a steady, recurring revenue stream 
            while lowering service costs and improving rider satisfaction.
            </p>
            """,
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Bottom Section: Impact Statement
    st.markdown(
        """
        <div class="impact-statement">
            <p>Every hardware sale creates a long-term recurring revenue stream — making each customer part of our ecosystem for years.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---- TAB 5: Go-to-Market Strategy ----
with tabs[5]:
    # Minimal CSS for Go-to-Market Tab
    st.markdown(
        """
        <style>
        .gtm-tab .hero-container {
            text-align: center;
            margin-bottom: 15px;
        }
        .gtm-tab .hero-title {
            color: #78C841;
            font-size: 26px;
            font-weight: 600;
            margin: 8px 0 4px;
        }
        .gtm-tab .hero-tagline {
            color: #A8F1FF;
            font-size: 14px;
            margin: 0 0 15px;
        }
        .gtm-tab .year-selector {
            max-width: 400px;
            margin: 15px auto;
            text-align: center;
        }
        .gtm-tab .year-section {
            display: flex;
            align-items: center;
            margin: 15px auto;
            max-width: 800px;
            min-height: 120px;
        }
        .gtm-tab .year-image-container {
            flex: 1;
            text-align: center;
            padding: 10px;
        }
        .gtm-tab .year-image {
            max-width: 200px;
            width: 100%;
            height: auto;
            border-radius: 6px;
            border: 1px solid #78C841;
        }
        .gtm-tab .year-text-container {
            flex: 2;
            padding: 10px;
            background: #1B3C53;
            border: 1px solid #78C841;
            border-radius: 6px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .gtm-tab .year-title {
            color: #78C841;
            font-size: 20px;
            font-weight: 600;
            margin: 0 0 6px;
        }
        .gtm-tab .year-text {
            color: #A8F1FF;
            font-size: 14px;
            line-height: 1.4;
            margin: 0;
        }
        .gtm-tab .year-text b {
            color: #FFF5F2;
            font-weight: 700;
        }
        .gtm-tab .milestone-counters {
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 10px;
        }
        .gtm-tab .milestone-counter {
            background: #1B3C53;
            border: 1px solid #78C841;
            border-radius: 6px;
            padding: 8px;
            min-width: 100px;
            text-align: center;
        }
        .gtm-tab .milestone-counter h4 {
            color: #78C841;
            font-size: 14px;
            margin: 0 0 4px;
        }
        .gtm-tab .milestone-counter p {
            color: #FFF5F2;
            font-size: 12px;
            font-weight: 700;
            margin: 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Hero Section (Image Removed)
    st.markdown('<div class="gtm-tab">', unsafe_allow_html=True)
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="hero-title">Go-to-Market Story (2025–2030)</h2>', unsafe_allow_html=True)
    st.markdown('<p class="hero-tagline">From pilot programs in India → to global category leadership.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Year Data
    years = [
        {
            "year": "2025",
            "theme": "The Beginning",
            "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/2025.png",
            "text": (
                "We officially launch PowerPedal in India, our first testing ground. With pilot programs alongside <b>Hero, Pedalze, and Cypro</b>, "
                "the product is put through real-world validation. To support this, we establish our first <b>30,000-unit production plant</b> in India. "
                "By the end of the year, we target <b>10,000 units sold</b>, generating around <b>₹1.2 Cr</b> in revenue. This year is about proving that "
                "PowerPedal works, scales, and delivers value."
            )
        },
        {
            "year": "2026",
            "theme": "Proving & Certifying",
            "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/2026.png",
            "text": (
                "With the pilots completed successfully, we turn them into long-term <b>OEM contracts</b> in India, capturing a larger share of the hub-drive market. "
                "Having validated our product locally, the focus now shifts to preparing for international standards. We adapt PowerPedal to meet <b>European regulations (EN15194)</b> "
                "and begin the certification process. At the same time, sales in India grow steadily, taking cumulative units to around <b>100,000</b> and revenues to <b>₹8.5 Cr</b>. "
                "This year transforms PowerPedal from a local product into a globally certifiable technology."
            )
        },
        {
            "year": "2027",
            "theme": "Stepping Into Global Markets",
            "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/2027.png",
            "text": (
                "Armed with <b>EU certification</b>, PowerPedal enters <b>Europe</b>, the world’s most mature eBike market, while also breaking into the <b>US</b> through OEM partnerships. "
                "To support demand, we expand India’s production capacity to <b>100,000 units per year</b>. By the end of this stage, cumulative units double to <b>200,000</b>, "
                "with revenues crossing <b>₹124 Cr</b>. The groundwork laid in India now becomes a global launchpad."
            )
        },
        {
            "year": "2028",
            "theme": "Spreading Through Licensing & Dealers",
            "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/2028.png",
            "text": (
                "Once established in Europe and the US, our strategy shifts toward scaling through <b>licensing deals</b> with OEMs, creating new recurring revenue streams. "
                "Alongside OEM sales, we expand aggressively into <b>dealer networks</b>, enabling both retrofitting and aftermarket adoption of PowerPedal. With a balanced model of "
                "licensing + OEM + dealers, sales rise sharply, taking cumulative units to <b>500,000</b> and revenues to <b>₹237 Cr</b>. This is the year PowerPedal begins to feel "
                "like a standard in the industry, not just a product."
            )
        },
        {
            "year": "2029",
            "theme": "Scaling Globally",
            "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/2029.png",
            "text": (
                "With momentum building, we expand our dealer base to over <b>850 globally</b>. To ensure supply resilience and faster delivery, we add manufacturing partnerships in "
                "<b>Poland and Mexico</b>, complementing the India base. This reduces costs, shortens lead times, and diversifies risk. By the end of 2029, cumulative sales approach "
                "<b>1 million units</b>, with revenues leaping to <b>₹654 Cr</b>. PowerPedal becomes a globally available technology backed by a strong manufacturing ecosystem."
            )
        },
        {
            "year": "2030",
            "theme": "Market Leadership",
            "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/2030.png",
            "text": (
                "By <b>2030</b>, PowerPedal reaches the milestone of <b>1 million units sold</b> worldwide and scales its dealer network to more than <b>1,650</b>. "
                "With this, we capture <b>1.94%</b> of the global eBike market and <b>8.64%</b> of the top non-Chinese hub-drive segment. "
                "Revenues climb past <b>₹1,467 Cr</b>. At this stage, PowerPedal isn’t just a product—it’s a <b>global category leader</b> in eBike drive technology, "
                "built on patents, scalable manufacturing, and multi-channel growth."
            )
        }
    ]

    # Year Selector
    selected_year = st.selectbox("Select Year", [year_data["year"] for year_data in years], key="year_selector")

    # Display Selected Year's Content
    year_data = next(year_data for year_data in years if year_data["year"] == selected_year)
    col1, col2 = st.columns([1, 2])
    with col1:
        image_path = load_image(os.path.abspath(year_data["image"]))
        if image_path:
            st.image(image_path, use_container_width=True, output_format="PNG")
        else:
            st.warning(f"Image not found: {year_data['image']}")
            st.markdown(
                '<div style="text-align: center; border: 1px solid #e6e6e6; border-radius: 6px; padding: 10px; background-color: #f0f0f0;">'
                '<p style="color: #555;">Placeholder: No image available</p></div>',
                unsafe_allow_html=True
            )
    with col2:
        st.markdown(f'<h3 class="year-title">{year_data["year"]} – {year_data["theme"]}</h3>', unsafe_allow_html=True)
        st.markdown(f'<p class="year-text">{year_data["text"]}</p>', unsafe_allow_html=True)
        if selected_year == "2030":
            milestones = [
                {"title": "Units Sold", "value": "1M"},
                {"title": "Dealers", "value": "1,650+"},
                {"title": "Global Market Share", "value": "1.94%"},
                {"title": "Non-China Hub-Drive Share", "value": "8.64%"},
                {"title": "Revenue", "value": "₹1,467 Cr"}
            ]
            st.markdown('<div class="milestone-counters">', unsafe_allow_html=True)
            for milestone in milestones:
                st.markdown(
                    f'<div class="milestone-counter"><h4>{milestone["title"]}</h4><p>{milestone["value"]}</p></div>',
                    unsafe_allow_html=True
                )
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[6]:
    st.header("📈 Financial Projections")
    st.caption("From 1,000 units in 2025 → 1 Million units by 2030")
    st.markdown("**Revenue grows from ₹0.85 Cr in 2025 to ₹1,467.5 Cr in 2030, driven by PowerPedal adoption in India and Europe.**")

    # Initialize Session State
    if 'financials' not in st.session_state:
        st.session_state.financials = {
            'scenario': 'Base Case',
            'asp_powerpedal': 10000,  # Default ₹10,000
            'cogs_powerpedal': 6000,  # Default ₹6,000
            'opex_percent': 0.15,     # Default 0.15
            'fixed_costs': 2.4e7      # ₹2.4 Cr
        }

    # Simplified CSS for Key Elements
    st.markdown(
        """
        <style>
        .financial-tab {
            font-family: Arial, sans-serif;
        }
        .variables-section {
            background: #D6DAC8 !important;
            border: 2px solid #9CAFAA !important;
            border-radius: 10px !important;
            padding: 20px;
            margin: 10px 0;
            text-align: center;
        }
        .variables-section h3 {
            color: #FFFFFF !important;
            font-size: 20px;
            margin-bottom: 10px;
            text-align: center;
        }
        .variables-section .stSlider > div {
            padding: 0 8px;
        }
        .variables-section .stSlider label {
            color: #000000 !important;
            font-weight: 600;
            text-align: center;
        }
        .data-table-container {
            background: #D6DAC8 !important;
            border: 2px solid #9CAFAA !important;
            border-radius: 10px !important;
            padding: 20px;
            margin: 10px 0;
        }
        .data-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            border-radius: 10px !important;
            overflow: hidden;
        }
        .data-table th {
            background: #EE791F !important;
            color: #000000 !important;
            font-weight: 600;
            padding: 10px;
            text-align: center;
            border-bottom: 1px solid #9CAFAA !important;
            border-right: 1px solid #9CAFAA !important;
        }
        .data-table td {
            color: #000000 !important;
            padding: 10px;
            text-align: center;
            border-bottom: 1px solid #9CAFAA !important;
            border-right: 1px solid #9CAFAA !important;
        }
        .data-table tr:nth-child(even) {
            background: #F5F5F5 !important;
        }
        .data-table tr:nth-child(odd) {
            background: #FFFFFF !important;
        }
        .data-table tr:hover {
            background: #FFD6BA !important;
        }
        .data-table td.highlight {
            background: #FFF9BD !important;
            font-weight: 600;
        }
        .data-table-caption {
            color: #FFFFFF !important;
            font-size: 14px;
            text-align: left;
            margin-top: 10px;
        }
        .data-table-caption h3 {
            color: #FFFFFF !important;
            font-size: 16px;
            margin-bottom: 0px;
        }
        .data-table-caption ul {
            margin-top: 0px;
            padding-left: 20px;
        }
        .data-table-caption li {
            color: #FFFFFF !important;
            font-size: 14px;
        }
        .scenario-highlight {
            background: #9CAFAA !important;
            border: 2px solid #9CAFAA !important;
            border-radius: 10px !important;
            padding: 10px;
            margin-bottom: 20px;
            text-align: center;
            font-weight: 600;
            color: #000000 !important;
        }
        .headline-container {
            background: #FFF9BD !important;
            border: 2px solid #9CAFAA !important;
            border-radius: 10px !important;
            padding: 20px;
            text-align: center;
            min-height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .headline-container h4 {
            color: #000000 !important;
            font-size: 14px;
            margin: 0 0 8px;
        }
        .headline-container p {
            color: #000000 !important;
            font-size: 18px;
            font-weight: 600;
            margin: 0;
        }
        .highlights-section {
            background: #D6DAC8 !important;
            border: 2px solid #9CAFAA !important;
            border-radius: 10px !important;
            padding: 20px;
            margin: 10px 0;
            text-align: center;
        }
        .highlights-section p {
            color: #000000 !important;
            font-size: 16px;
            font-weight: 600;
            margin: 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="financial-tab">', unsafe_allow_html=True)

    # Image in Centered Column
    _, col_img, _ = st.columns([1, 4, 1])
    with col_img:
        image_path = os.path.abspath("https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/financial.png")
        if os.path.exists(image_path):
            st.image(image_path, caption="PowerPedal Growth Vision", use_container_width=True)
        else:
            st.warning("Image file not found at: https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/financial.png")
            st.markdown(
                """
                <div style="text-align: center; border: 1px solid #e6e6e6; border-radius: 10px; padding: 20px; background-color: #f0f0f0;">
                    <p style="color: #555;">Placeholder: No image available for financial.png</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Define Global Variables
    unit_sales_base = [1000, 10000, 100000, 200000, 500000, 1000000]
    revenue_base = [0.85e7, 8.5e7, 124e7, 237.45e7, 654e7, 1467.5e7]
    years = [2025, 2026, 2027, 2028, 2029, 2030]
    fixed_cogs_2025 = 8500  # Fixed COGS for 2025

    # Financial Calculations
    def calculate_financials(scenario, asp_powerpedal, cogs_powerpedal, opex_percent, fixed_costs):
        unit_sales = unit_sales_base
        if scenario == 'Conservative':
            unit_sales = [int(u * 0.8) for u in unit_sales_base]
        elif scenario == 'Aggressive':
            unit_sales = [int(u * 1.2) for u in unit_sales_base]

        cogs_decline_rate = 0.02
        base_tax_rate = 0.25
        tax_exemption_years = [2025, 2026, 2027]
        cogs_powerpedal_list = [fixed_cogs_2025] + [cogs_powerpedal * (1 - cogs_decline_rate) ** i for i in range(0, len(years) - 1)]
        revenue = [u * asp_powerpedal for u in unit_sales]
        gross_profit = [u * (asp_powerpedal - c) for u, c in zip(unit_sales, cogs_powerpedal_list)]
        opex = [
            0.35e7 if year == 2025 else
            2.3e7 if year == 2026 else
            15e7 if year == 2027 else
            r * opex_percent + fixed_costs
            for year, r in zip(years, revenue)
        ]
        ebitda = [gp - o for gp, o in zip(gross_profit, opex)]
        tax_rate = [0 if year in tax_exemption_years else base_tax_rate for year in years]
        net_income = [e * (1 - tr) for e, tr in zip(ebitda, tax_rate)]
        return unit_sales, revenue, cogs_powerpedal_list, gross_profit, opex, ebitda, net_income

    # Calculate Financials
    try:
        unit_sales, revenue, cogs_powerpedal_list, gross_profit, opex, ebitda, net_income = calculate_financials(
            st.session_state.financials['scenario'],
            st.session_state.financials['asp_powerpedal'],
            st.session_state.financials['cogs_powerpedal'],
            st.session_state.financials['opex_percent'],
            st.session_state.financials['fixed_costs']
        )
    except Exception as e:
        st.error(f"Error in financial calculations: {e}")
        st.stop()

    # Headline Metrics
    with st.container():
        st.markdown(
            f'<div class="scenario-highlight">'
            f'Active Scenario: <strong>{st.session_state.financials["scenario"]}</strong>'
            f'</div>',
            unsafe_allow_html=True
        )
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            try:
                revenue_value = sum(revenue) / 1e7
                st.markdown(
                    f'<div class="headline-container" style="background: #FFF9BD;">'
                    f'<h4 style="color: #000000; margin: 0 0 8px;">Total Revenue (2025–2030)</h4>'
                    f'<p style="color: #000000; font-size: 18px; font-weight: 600; margin: 0;">₹{revenue_value:.2f} Cr</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"Total Revenue: {e}")
        with col2:
            try:
                gross_profit_value = sum(gross_profit) / 1e7
                st.markdown(
                    f'<div class="headline-container" style="background: #FFD6BA;">'
                    f'<h4 style="color: #000000; margin: 0 0 8px;">Total Gross Profit (2025–2030)</h4>'
                    f'<p style="color: #000000; font-size: 18px; font-weight: 600; margin: 0;">₹{gross_profit_value:.2f} Cr</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"Total Gross Profit: {e}")
        with col3:
            try:
                net_profit_value = sum(net_income) / 1e7
                st.markdown(
                    f'<div class="headline-container" style="background: #D6DAC8;">'
                    f'<h4 style="color: #000000; margin: 0 0 8px;">Total Net Profit (2025–2030)</h4>'
                    f'<p style="color: #000000; font-size: 18px; font-weight: 600; margin: 0;">₹{net_profit_value:.2f} Cr</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"Total Net Profit: {e}")
        with col4:
            try:
                st.markdown(
                    f'<div class="headline-container" style="background: #9CAFAA;">'
                    f'<h4 style="color: #000000; margin: 0 0 8px;">Break-even Year</h4>'
                    f'<p style="color: #000000; font-size: 18px; font-weight: 600; margin: 0;">2026</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"Break-even Year: {e}")

    # Sliders and Table
    col_vars, col_table = st.columns([1, 3])

    with col_vars:
        st.markdown('<div class="variables-section">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #FFFFFF;">Key Variables</h3>', unsafe_allow_html=True)
        st.session_state.financials['asp_powerpedal'] = st.slider(
            "Selling Price of PowerPedal (₹)", 6000, 20000,
            st.session_state.financials['asp_powerpedal'], 100,
            key="asp_powerpedal_financial",
            help="Average Selling Price for PowerPedal"
        )
        st.session_state.financials['cogs_powerpedal'] = st.slider(
            "PowerPedal COGS (₹, 2026)", 4000, 8000,
            st.session_state.financials['cogs_powerpedal'], 100,
            key="cogs_powerpedal_financial",
            help="Cost of Goods Sold per unit for 2026 (2025 fixed at ₹8,500)"
        )
        st.session_state.financials['opex_percent'] = st.slider(
            "Operating Expenses (% of Revenue)", 0.10, 0.25,
            st.session_state.financials['opex_percent'], 0.01,
            key="opex_percent_financial",
            help="Operating Expenses as a percentage of revenue for 2028–2030"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Table
    with col_table:
        st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
        try:
            df = pd.DataFrame({
                'Year': years,
                'Units Sold': [f'{u:,}' for u in unit_sales],
                'Revenue (₹ Cr)': [round(r / 1e7, 2) for r in revenue],
                'COGS (₹ Cr)': [round((u * c) / 1e7, 2) for u, c in zip(unit_sales, cogs_powerpedal_list)],
                'Gross Profit (₹ Cr)': [round(gp / 1e7, 2) for gp in gross_profit],
                'Opex (₹ Cr)': [round(o / 1e7, 2) for o in opex],
                'EBITDA (₹ Cr)': [round(e / 1e7, 2) for e in ebitda],
                'Net Income (₹ Cr)': [f'<span class="highlight">{round(ni / 1e7, 2)}</span>' for ni in net_income],
                'EBITDA Margin (%)': [f'<span class="highlight">{round((e / r) * 100, 1)}</span>' if r > 0 else '0.0'
                                      for e, r in zip(ebitda, revenue)]
            })
            headers = df.columns.tolist()
            html = '<table class="data-table">'
            html += '<tr>' + ''.join(f'<th>{h}</th>' for h in headers) + '</tr>'
            for idx, row in df.iterrows():
                html += '<tr>'
                for col in headers:
                    html += f'<td>{row[col]}</td>'
                html += '</tr>'
            html += '</table>'
            st.markdown(html, unsafe_allow_html=True)
            st.markdown(
                '<div class="data-table-caption">'
                '<h3>Note</h3>'
                '<ul>'
                '<li>We have considered Section 80-IAC tax exemptions for 2025–2027.</li>'
                '<li>Opex will remain low in 2025–2026 due to lean operations, minimal hiring, and outsourced manufacturing (with only assembly done in-house).</li>'
                '</ul>'
                '</div>',
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"Error rendering table: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Scenario Comparison
    col_sc1, col_sc2, col_sc3 = st.columns(3)
    scenarios = ['Conservative', 'Base Case', 'Aggressive']
    scenario_units = {
        'Conservative': [int(u * 0.8) for u in unit_sales_base],
        'Base Case': unit_sales_base,
        'Aggressive': [int(u * 1.2) for u in unit_sales_base]
    }
    scenario_revenue = {
        'Conservative': [u * st.session_state.financials['asp_powerpedal'] for u in scenario_units['Conservative']],
        'Base Case': revenue_base,
        'Aggressive': [u * st.session_state.financials['asp_powerpedal'] for u in scenario_units['Aggressive']]
    }
    with col_sc1:
        try:
            st.markdown(
                f'<div style="background: #FFF9BD; border: 2px solid #9CAFAA; border-radius: 10px; padding: 20px; text-align: center;">'
                f'<h4 style="color: #000000;">Conservative (2030)</h4>'
                f'<p style="color: #000000;">{scenario_units["Conservative"][-1]:,} units, ₹{scenario_revenue["Conservative"][-1] / 1e7:.2f} Cr</p>'
                f'</div>',
                unsafe_allow_html=True
            )
            if st.button("Conservative", key="conservative_financial", use_container_width=True):
                st.session_state.financials['scenario'] = 'Conservative'
                st.rerun()
        except Exception as e:
            st.error(f"Conservative scenario: {e}")
    with col_sc2:
        try:
            st.markdown(
                f'<div style="background: #FFD6BA; border: 2px solid #9CAFAA; border-radius: 10px; padding: 20px; text-align: center;">'
                f'<h4 style="color: #000000;">Base Case (2030)</h4>'
                f'<p style="color: #000000;">{scenario_units["Base Case"][-1]:,} units, ₹{scenario_revenue["Base Case"][-1] / 1e7:.2f} Cr</p>'
                f'</div>',
                unsafe_allow_html=True
            )
            if st.button("Base Case", key="base_case_financial", use_container_width=True):
                st.session_state.financials['scenario'] = 'Base Case'
                st.rerun()
        except Exception as e:
            st.error(f"Base Case scenario: {e}")
    with col_sc3:
        try:
            st.markdown(
                f'<div style="background: #D6DAC8; border: 2px solid #9CAFAA; border-radius: 10px; padding: 20px; text-align: center;">'
                f'<h4 style="color: #000000;">Aggressive (2030)</h4>'
                f'<p style="color: #000000;">{scenario_units["Aggressive"][-1]:,} units, ₹{scenario_revenue["Aggressive"][-1] / 1e7:.2f} Cr</p>'
                f'</div>',
                unsafe_allow_html=True
            )
            if st.button("Aggressive", key="aggressive_financial", use_container_width=True):
                st.session_state.financials['scenario'] = 'Aggressive'
                st.rerun()
        except Exception as e:
            st.error(f"Aggressive scenario: {e}")

    # Charts
    st.markdown('<div class="charts-section">', unsafe_allow_html=True)
    col_chart1, col_chart2, col_chart3 = st.columns(3)

    with col_chart1:
        try:
            fig1, ax1 = plt.subplots(figsize=(4, 2.5))
            fig1.patch.set_facecolor('none')
            ax1.set_facecolor('none')
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            ax1.spines['left'].set_color('#FFFFFF')
            ax1.spines['bottom'].set_color('#FFFFFF')
            ax1.tick_params(colors='#FFFFFF', labelsize=8)
            ax1.plot(years, [r / 1e7 for r in revenue], label='Revenue', color='#EE791F', linewidth=2)
            ax1.set_xlabel('Year', color='#FFFFFF', fontsize=8)
            ax1.set_ylim(0, max([r / 1e7 for r in revenue]) * 1.2)
            ax1.set_title('Revenue (₹ Cr)', color='#FFFFFF', fontsize=10)
            ax1.legend(fontsize=7, frameon=False, labelcolor='#FFFFFF')
            ax1.set_ylabel('Revenue (₹ Cr)', color='#FFFFFF', fontsize=8)
            plt.tight_layout(pad=1.0)
            st.pyplot(fig1)
        except Exception as e:
            st.error(f"Revenue chart: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_chart2:
        try:
            fig2, ax2 = plt.subplots(figsize=(4, 2.5))
            fig2.patch.set_facecolor('none')
            ax2.set_facecolor('none')
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            ax2.spines['left'].set_color('#FFFFFF')
            ax2.spines['bottom'].set_color('#FFFFFF')
            ax2.tick_params(colors='#FFFFFF', labelsize=8)
            ax2.bar(years, unit_sales, color='#FFF9BD', label='Units Sold')
            ax2.set_ylim(0, max(unit_sales) * 1.2)
            ax2.set_ylabel('Units Sold', color='#FFFFFF', fontsize=8)
            ax2.set_title('Units Sold', color='#FFFFFF', fontsize=10)
            ax2.legend(loc='upper left', fontsize=7, frameon=False, labelcolor='#FFFFFF')
            plt.tight_layout(pad=1.0)
            st.pyplot(fig2)
        except Exception as e:
            st.error(f"Units Sold chart: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_chart3:
        try:
            fig3, ax3 = plt.subplots(figsize=(4, 2.5))
            fig3.patch.set_facecolor('none')
            ax3.set_facecolor('none')
            ax3.spines['top'].set_visible(False)
            ax3.spines['right'].set_visible(False)
            ax3.spines['left'].set_color('#FFFFFF')
            ax3.spines['bottom'].set_color('#FFFFFF')
            ax3.tick_params(colors='#FFFFFF', labelsize=8)
            ax3.bar(years, [gp / 1e7 for gp in gross_profit], color='#FFD6BA', label='Gross Profit')
            ax3.bar(years, [o / 1e7 for o in opex], bottom=[gp / 1e7 for gp in gross_profit],
                    color='#EE791F', label='Opex')
            ax3.plot(years, [e / 1e7 for e in ebitda], color='#FFF9BD', linewidth=2, label='EBITDA')
            ax3.plot(years, [ni / 1e7 for ni in net_income], color='#9CAFAA', linewidth=2, label='Net Income')
            ax3.set_xlabel('Year', color='#FFFFFF', fontsize=8)
            ax3.set_ylim(min([min([e / 1e7 for e in ebitda]), 0]) * 1.2, max([max([(gp + o) / 1e7 for gp, o in zip(gross_profit, opex)]), 10]) * 1.2)
            ax3.set_title('Profitability (₹ Cr)', color='#FFFFFF', fontsize=10)
            ax3.legend(fontsize=7, frameon=False, labelcolor='#FFFFFF')
            ax3.set_ylabel('₹ Cr', color='#FFFFFF', fontsize=8)
            plt.tight_layout(pad=1.0)
            st.pyplot(fig3)
        except Exception as e:
            st.error(f"Profitability chart: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Key Investor Highlights
    st.markdown('<div class="highlights-section">', unsafe_allow_html=True)
    with st.container():
        st.markdown(
            f'<div style="background: #D6DAC8; border: 2px solid #9CAFAA; border-radius: 10px; padding: 20px; text-align: center;">'
            f'<p style="color: #000000; font-size: 16px; font-weight: 600;">💡 Foundation built on grant money with minimal dilution – R&D, patents, pilots achieved capital-efficiently.</p>'
            f'</div>',
            unsafe_allow_html=True
        )
    with st.container():
        st.markdown(
            f'<div style="background: #D6DAC8; border: 2px solid #9CAFAA; border-radius: 10px; padding: 20px; text-align: center;">'
            f'<p style="color: #000000; font-size: 16px; font-weight: 600;">🤝 Equity given only to strategic partner – securing early distribution & GTM strength.</p>'
            f'</div>',
            unsafe_allow_html=True
        )
    with st.container():
        st.markdown(
            f'<div style="background: #D6DAC8; border: 2px solid #9CAFAA; border-radius: 10px; padding: 20px; text-align: center;">'
            f'<p style="color: #000000; font-size: 16px; font-weight: 600;">📈 Profitability achieved at 10K units (2026) – EBITDA positive far earlier than typical hardware.</p>'
            f'</div>',
            unsafe_allow_html=True
        )
    with st.container():
        st.markdown(
            f'<div style="background: #D6DAC8; border: 2px solid #9CAFAA; border-radius: 10px; padding: 20px; text-align: center;">'
            f'<p style="color: #000000; font-size: 16px; font-weight: 600;">🚀 10x growth in 2027 – driven by European expansion & OEM adoption.</p>'
            f'</div>',
            unsafe_allow_html=True
        )
    with st.container():
        st.markdown(
            f'<div style="background: #D6DAC8; border: 2px solid #9CAFAA; border-radius: 10px; padding: 20px; text-align: center;">'
            f'<p style="color: #000000; font-size: 16px; font-weight: 600;">🏭 Capital-light scaling model – contract manufacturing keeps costs lean while margins expand towards ~30% by 2030.</p>'
            f'</div>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
import streamlit as st
import os

with tabs[7]:
    # --- Styles specific to this storytelling timeline ---
    st.markdown("""
    <style>
        /* Reset Streamlit default margins and padding */
        .st-emotion-cache-1wmy9hl, .st-emotion-cache-0, .st-emotion-cache-1r4s1nx, .st-emotion-cache-12fmjuu {
            margin: 0 !important;
            padding: 0 !important;
        }

        /* Main container for the timeline */
        .timeline-container {
            margin: 0 !important;
            padding: 0 !important;
            width: 100% !important;
        }

        /* Container for each timeline entry */
        .timeline-entry {
            display: flex;
            justify-content: space-between;
            align-items: stretch;
            margin: 0 !important; /* Reduced from 0px */
            min-height: 30px; /* Reduced from 40px */
        }

        .timeline-content-left {
            text-align: right;
            padding: 0 !important; /* Set to 0px */
            margin-right: -5px; /* Negative margin to pull closer */
        }

        .timeline-content-right {
            text-align: left;
            padding: 0 !important; /* Set to 0px */
            margin-left: -5px; /* Negative margin to pull closer */
        }

        /* Styling for Product expanders */
        .expander-product div[data-testid="stExpander"] {
            background: #1A3636 !important;
            border: none !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
            border-radius: 10px !important;
            margin: 0 !important;
            height: 100% !important;
        }

        /* Styling for Funding expanders */
        .expander-funding div[data-testid="stExpander"] {
            background: #40534C !important;
            border: none !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
            border-radius: 10px !important;
            margin: 0 !important;
            height: 100% !important;
        }

        div[data-testid="stExpander"] .st-emotion-cache-p5msec {
            font-size: 1.2em !important;
            font-weight: 600 !important;
            color: #A8F1FF !important;
            padding: 8px !important;
        }
        
        div[data-testid="stExpander"] p {
            font-size: 1em !important;
            color: #FFF5F2 !important;
            margin: 0 !important;
            padding: 8px !important;
        }

        /* Media styling for images */
        .timeline-media img {
            max-width: 100% !important;
            border-radius: 8px !important;
            margin-top: 5px !important;
            border: 1px solid #78C841 !important;
        }

        /* Video styling */
        .timeline-media video {
            max-width: 100% !important;
            border-radius: 8px !important;
            margin-top: 5px !important;
            border: 1px solid #78C841 !important;
        }

        /* Story section styling */
        .story-section {
            background: linear-gradient(135deg, #1B3C53, #2e2e2e) !important;
            border: 2px solid #78C841 !important;
            border-radius: 12px !important;
            padding: 20px !important;
            margin: 20px 0 !important;
            text-align: center !important;
            max-width: 800px !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }
        .story-section h3 {
            color: #78C841 !important;
            font-size: 24px !important;
            margin-bottom: 10px !important;
        }
        .story-section p {
            color: #A8F1FF !important;
            font-size: 16px !important;
            line-height: 1.6 !important;
            margin: 0 0 10px 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- JavaScript to ensure background colors ---
    st.components.v1.html("""
    <script>
        function applyExpanderColors() {
            const productExpanders = document.querySelectorAll('.expander-product div[data-testid="stExpander"]');
            const fundingExpanders = document.querySelectorAll('.expander-funding div[data-testid="stExpander"]');
            
            productExpanders.forEach(expander => {
                expander.style.background = '#1A3636';
                expander.style.border = 'none';
                expander.style.borderRadius = '10px';
                expander.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
                expander.style.margin = '0';
            });
            
            fundingExpanders.forEach(expander => {
                expander.style.background = '#40534C';
                expander.style.border = 'none';
                expander.style.borderRadius = '10px';
                expander.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
                expander.style.margin = '0';
            });
        }

        // Run on page load
        window.addEventListener('load', applyExpanderColors);

        // Run periodically for dynamic rendering
        setInterval(applyExpanderColors, 100);
    </script>
    """, height=0)

    # --- Tab Content ---
    st.header("📍 Our Journey of Traction & Milestones")
    st.markdown("---")

    # --- High-level Visual Summary ---
    col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
    with col_img2:
        timeline_image_path = r"https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images\timeline.png"
        if os.path.exists(timeline_image_path):
            st.image(timeline_image_path, caption="A visual summary of our progress.", use_container_width=True)
        else:
            st.error(f"Image not found at {timeline_image_path}. Please verify the file exists.")

    # --- Enhanced Story Section ---
    st.markdown('<div class="story-section">', unsafe_allow_html=True)
    st.markdown('<h3>The Spark That Started It All</h3>', unsafe_allow_html=True)
    st.markdown("""
    <p>Our journey began in a college lab, where we built an award-winning electric skateboard, igniting our passion for redefining mobility. Driven by curiosity, we explored urban transportation—bicycles emerged as the perfect fusion of efficiency, practicality, and sustainability.</p>
    <p>We fearlessly experimented, creating a powered wheelchair attachment for accessibility, a Hybrid Energy Storage System (HESS), road presence lighting, and custom drivetrains. Each project honed our skills, but our focus crystallized on advanced drive technology. Today, Switch Mobility is a B2B leader, delivering responsive, efficient, and cost-effective eBike drive systems to OEMs worldwide, transforming urban mobility.</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("Our Journey, Step by Step")
    st.markdown(
        "From a bold idea to a production-ready eBike drive system, our path combines cutting-edge innovation with strategic funding. Explore our milestones below, with product breakthroughs on the left (dark teal expanders) and funding achievements on the right (dark gray-green expanders).",
        help="Product milestones are highlighted with dark teal expanders (#1A3636), while funding milestones have dark gray-green expanders (#40534C) for clear differentiation."
    )

    # --- Data for Milestones (with media only for Product milestones) ---
    milestones_data = [
        {
            "name": "Concept Validation",
            "type": "Product",
            "value": "N/A",
            "icon": "💡",
            "details": "Validated the core concept for an innovative e-bike drive system, leveraging urban mobility insights to prioritize efficiency, responsiveness, and rider comfort.",
            "media": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/concept_validation.png"
        },
        {
            "name": "Bootstrap & Family",
            "type": "Funding",
            "value": "₹2.5 Lakh",
            "icon": "💰",
            "details": "Secured initial seed funding from founders and family, enabling early research, component procurement, and the creation of our first proof-of-concept models.",
            "media": None
        },
        {
            "name": "Mentor Funding",
            "type": "Funding",
            "value": "₹5 Lakh",
            "icon": "🤝",
            "details": "Obtained funding and mentorship from a private investor, refining our technical vision and business strategy to accelerate development.",
            "media": None
        },
        {
            "name": "Prototype Development",
            "type": "Product",
            "value": "N/A",
            "icon": "🛠️",
            "details": "Built our first functional prototype with custom electronics and motor control algorithms, achieving a seamless, natural ride experience, supported by the Indian Institute of Science's Design Clinic Scheme.",
            "media": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/videos/prototype_development.mp4"
        },
        {
            "name": "Meity-EIR (PSG)",
            "type": "Funding",
            "value": "₹4 Lakh",
            "icon": "🏛️",
            "details": "Received support from the Ministry of Electronics and Information Technology’s Entrepreneur-in-Residence program at PSG College, fueling further innovation and prototype refinement.",
            "media": None
        },
        {
            "name": "Nidhi-Prayas",
            "type": "Funding",
            "value": "₹10 Lakh",
            "icon": "🏆",
            "details": "Awarded a grant from the Deshpande Foundation’s NIDHI-PRAYAS scheme, empowering us to transform innovative concepts into robust, market-ready prototypes.",
            "media": None
        },
        {
            "name": "Functional PowerPedal V1",
            "type": "Product",
            "value": "N/A",
            "icon": "✅",
            "details": "Developed and rigorously tested PowerPedal V1, our first complete eBike drive system, meeting stringent performance, efficiency, and cost benchmarks.",
            "media": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/videos/design_clinic.mp4"
        },
        {
            "name": "Elevate Karnataka",
            "type": "Funding",
            "value": "₹23 Lakh",
            "icon": "🚀",
            "details": "Earned a prestigious grant from Startup Karnataka, recognizing PowerPedal as a top innovator, and providing critical funds to scale toward production.",
            "media": None
        },
        {
            "name": "Production-Ready Product",
            "type": "Product",
            "value": "N/A",
            "icon": "🏁",
            "details": "Refined PowerPedal into a production-ready eBike drive system, now undergoing pilot programs with select OEMs for seamless integration and market entry.",
            "media": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/Production-Ready.png"
        }
    ]

    # --- Building the Vertical Timeline ---
    try:
        st.markdown('<div class="timeline-container">', unsafe_allow_html=True)
        
        for index, milestone in enumerate(milestones_data):
            st.markdown('<div class="timeline-entry">', unsafe_allow_html=True)
            col_left, col_center, col_right = st.columns([5, 0.01, 5])  # Minimized center column width
            
            # Format the expander title
            title = f"{milestone['icon']} **{milestone['name']}**"
            if milestone['value'] != 'N/A':
                title += f" — *{milestone['value']}*"
            
            # Assign unique class based on milestone type
            class_name = "expander-product" if milestone["type"] == "Product" else "expander-funding"
            
            if milestone["type"] == "Product":
                with col_left:
                    st.markdown('<div class="timeline-content-left">', unsafe_allow_html=True)
                    with st.container():
                        with st.expander(title, expanded=False):
                            st.markdown(f'<div class="{class_name}">', unsafe_allow_html=True)
                            st.write(milestone['details'])
                            if milestone['media']:
                                media_path = r"C:\Users\ranji\OneDrive - Switch\Switch\Dashboards\Pitch Dashboard\{}".format(milestone['media'])
                                if os.path.exists(media_path):
                                    st.markdown('<div class="timeline-media">', unsafe_allow_html=True)
                                    if milestone['media'].endswith(('.png', '.jpg', '.jpeg')):
                                        st.image(media_path, caption=milestone['name'], use_container_width=True)
                                    elif milestone['media'].endswith('.mp4'):
                                        st.video(media_path)
                                    st.markdown('</div>', unsafe_allow_html=True)
                                else:
                                    st.error(f"Media not found at {media_path}. Please verify the file exists.")
                            st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:  # Funding milestones
                with col_right:
                    st.markdown('<div class="timeline-content-right">', unsafe_allow_html=True)
                    with st.container():
                        with st.expander(title, expanded=False):
                            st.markdown(f'<div class="{class_name}">', unsafe_allow_html=True)
                            st.write(milestone['details'])
                            st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"An error occurred while rendering the timeline: {str(e)}")


import streamlit as st
import os
from pathlib import Path
import base64
import time

# Disable all Streamlit caching
st.set_page_config(page_title="PowerPedal Pitch Deck", layout="wide")
st.cache_data.clear()
st.cache_resource.clear()
try:
    st.experimental_memo.clear()
    st.experimental_singleton.clear()
except AttributeError:
    pass  # Handle older Streamlit versions

import streamlit as st
import time
import base64
from pathlib import Path
import os
import requests
from io import BytesIO

# ---- TAB 8: Team & Advisors ----
with tabs[8]:
    st.header("🧑‍🤝‍🧑 Team & Advisors", anchor=False)
    st.caption("Meet the Visionaries Powering Our Mission")

    # --- CSS (Updated for profile-image fit) ---
    st.markdown(
        f"""
        <style>
        .team-advisors-tab {{
            font-family: 'Figtree', sans-serif;
        }}
        .team-advisors-tab .profile-container {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #2e2e2e, #1B3C53);
            border: 3px solid #00FF7F;
            border-radius: 8px;
            padding: 15px !important;
            margin: 15px;
            max-width: 250px !important;
            width: 100%;
            box-sizing: border-box;
            transition: transform 0.4s ease, box-shadow 0.4s ease;
            text-align: center;
            text-decoration: none; /* Ensure no underline on link */
        }}
        .team-advisors-tab .profile-container:hover {{
            transform: scale(1.07);
            box-shadow: 0 0 15px rgba(0, 255, 127, 0.7);
        }}
        .team-advisors-tab .profile-image {{
            width: 120px !important;
            height: 120px !important;
            border-radius: 50%;
            object-fit: cover; /* Changed to cover for consistent fill */
            border: 2px solid #A8F1FF;
            padding: 2px;
            background: #FFFFFF;
            display: block;
            margin: 0 auto;
        }}
        .team-advisors-tab .profile-name {{
            color: #00FF7F;
            font-size: 18px;
            font-weight: 600;
            margin: 10px 0 5px 0;
            text-align: center;
            width: 100%;
        }}
        .team-advisors-tab .profile-role {{
            color: #A8F1FF;
            font-size: 14px;
            margin: 0;
            text-align: center;
            width: 100%;
        }}
        .team-advisors-tab .profile-details {{
            color: #FFF5F2;
            font-size: 12px;
        }}
        .team-advisors-tab .collage-grid {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            align-items: center;
            gap: 10px;
            padding: 10px;
            background: linear-gradient(135deg, #1B3C53, #00FF7F);
            border: 3px solid #00FF7F;
            border-radius: 8px;
            margin: 50px auto;
            max-width: 800px;
        }}
        .team-advisors-tab .collage-image {{
            width: 200px;
            height: 200px;
            object-fit: cover;
            border-radius: 8px;
            border: 2px solid #A8F1FF;
        }}
        .team-advisors-tab .supported-by-section {{
            background: #FFFFFF;
            border: 3px solid #00FF7F;
            border-radius: 8px;
            padding: 20px;
            margin: 50px 0;
            text-align: center;
        }}
        .team-advisors-tab .supported-by-section .section-title {{
            color: #1B3C53;
        }}
        .team-advisors-tab .institutions-grid {{
            display: flex;
            justify-content: center;
            align-items: center;
            flex-wrap: wrap;
            gap: 40px;
            margin-top: 20px;
        }}
        .team-advisors-tab .institution-logo-img {{
            height: 60px;
            max-width: 150px;
            object-fit: contain;
        }}
        .team-advisors-tab .summary-text {{
            color: #A8F1FF;
            text-align: center;
            max-width: 500px;
            margin: 20px auto;
        }}
        .team-advisors-tab .supported-by-section .summary-text {{
            color: #555555;
        }}
        .team-advisors-tab .section-divider {{
            border: 3px solid #00FF7F;
            margin: 50px 0;
        }}
        .team-advisors-tab .media-container {{
            background: #1B3C53;
            border: 3px solid #00FF7F;
            border-radius: 8px;
            padding: 15px;
            margin: 50px 0;
            text-align: center;
            box-sizing: border-box;
        }}
        .team-advisors-tab .media-section .section-title {{
            color: #FFFFFF;
        }}
        .team-advisors-tab .article-item {{
            margin: 15px 0;
            text-align: left;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
            padding: 10px;
            border-radius: 5px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .team-advisors-tab .article-item:hover {{
            transform: scale(1.02);
            box-shadow: 0 0 10px rgba(0, 255, 127, 0.7);
        }}
        .team-advisors-tab .article-title {{
            color: #00FF7F;
            font-size: 16px;
            font-weight: 600;
            text-decoration: none;
            display: block;
        }}
        .team-advisors-tab .article-title:hover {{
            color: #A8F1FF;
        }}
        .team-advisors-tab .connect-container {{
            background: #1B3C53;
            border: 3px solid #00FF7F;
            border-radius: 8px;
            padding: 15px;
            margin: 50px 0;
            text-align: center;
            box-sizing: border-box;
        }}
        .team-advisors-tab .connect-section .section-title {{
            color: #FFFFFF;
        }}
        .team-advisors-tab .connect-links {{
            display: flex;
            justify-content: center;
            gap: 70px;
            margin-top: 15px;
        }}
        .team-advisors-tab .connect-button {{
            background: #00FF7F;
            color: #1B3C53;
            border: none;
            border-radius: 20px;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: 600;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 5px;
            transition: background 0.3s ease, transform 0.3s ease;
        }}
        .team-advisors-tab .connect-button:hover {{
            background: #A8F1FF;
            transform: scale(1.05);
        }}
        .team-advisors-tab .connect-icon {{
            font-size: 16px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Cache image loading with base64 encoding for both local files and URLs
    @st.cache_data
    def load_image(image_name):
        # Check if the image_name is a URL
        if image_name.startswith("http"):
            try:
                response = requests.get(image_name)
                if response.status_code == 200:
                    encoded = base64.b64encode(response.content).decode()
                    # Determine MIME type based on file extension
                    ext = image_name.lower().split('.')[-1]
                    mime_type = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"
                    return f"data:{mime_type};base64,{encoded}"
                else:
                    st.warning(f"Failed to fetch image from {image_name}. Status code: {response.status_code}")
                    return "https://via.placeholder.com/200"
            except Exception as e:
                st.error(f"Error loading image {image_name}: {str(e)}")
                return "https://via.placeholder.com/200"
        else:
            # Handle local files
            base_path = r"C:\Users\ranji\OneDrive - Switch\Switch\Dashboards\Pitch Dashboard"
            image_path = Path(base_path) / image_name
            try:
                if image_path.is_file():
                    with open(image_path, "rb") as f:
                        encoded = base64.b64encode(f.read()).decode()
                    ext = image_path.suffix.lower()
                    mime_type = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
                    return f"data:{mime_type};base64,{encoded}"
                else:
                    st.warning(f"Image not found: {image_name}")
                    return "https://via.placeholder.com/200"
            except Exception as e:
                st.error(f"Error loading image {image_name}: {e}")
                return "https://via.placeholder.com/200"

    # --- Core Team Section ---
    st.markdown('<div class="team-advisors-tab"><h2 class="section-title" style="text-align:center;">Core Team</h2></div>', unsafe_allow_html=True)
    team_members = [
        {"name": "Vineeth Muthanna", "role": "Technical Head", "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/Vineeth.png", "linkedin": "https://linkedin.com/in/vineethmuthanna", "bio": "Vineeth leads product development..."},
        {"name": "Ranjit B C", "role": "Business & Operations", "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/Ranjit.jpeg", "linkedin": "https://linkedin.com/in/ranjit-b-c-a3981215a", "bio": "Ranjit drives operational excellence..."},
        {"name": "Vinay Sharma", "role": "Marketing & Finance", "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/vinay.png", "linkedin": "https://linkedin.com/in/vinay-sharma-0563a816a", "bio": "Vinay drives brand growth..."},
        {"name": "Shravan Aiyappa", "role": "Production Head", "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/Shravan.png", "linkedin": "https://linkedin.com/in/shravan-aiyappa-kadiamada-b8958ab9", "bio": "Shravan oversees production..."},
        {"name": "Rohit Kuttappa", "role": "Strategy & GTM", "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/Rohit.jpg", "linkedin": "https://linkedin.com/in/rohit-kuttappa-a6256439", "bio": "Rohit shapes go-to-market strategies..."},
        {"name": "Abbishek Bharadwaj", "role": "Sales & OEM Partnerships", "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/Abbishek.jpg", "linkedin": "https://linkedin.com/in/abbishek-v-bharadwaj-21171911", "bio": "Abbishek drives sales..."}
    ]
    for i in range(0, len(team_members), 3):
        cols = st.columns(3)
        for j, member in enumerate(team_members[i:i+3]):
            with cols[j]:
                st.markdown(f"""
                    <a href="{member['linkedin']}" target="_blank" style="text-decoration: none;">
                        <div class="team-advisors-tab profile-container">
                            <img src="{load_image(member['image'])}" class="profile-image">
                            <div class="profile-name">{member['name']}</div>
                            <div class="profile-role">{member['role']}</div>
                        </div>
                    </a>
                """, unsafe_allow_html=True)
                with st.expander(f"About {member['name']}"):
                    st.markdown(f'<div class="team-advisors-tab profile-details">{member["bio"]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="team-advisors-tab summary-text">Our core team drives innovation and execution to lead our e-mobility revolution.</div>', unsafe_allow_html=True)

    # --- Team Collaboration Section ---
    team_images = ["https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/team1.jpg", "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/team2.jpg", "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/team3.jpg", "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/team4.jpg", "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/team5.jpg"]
    images_html = ""
    for img_file in team_images:
        img_data = load_image(img_file)
        images_html += f'<img src="{img_data}" class="collage-image">'
    st.markdown(
        f"""
        <div class="team-advisors-tab">
            <div class="collage-grid">
                {images_html}
            </div>
            <div class="summary-text">Our team collaborates at events and workshops to drive our mission forward.</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<hr class="team-advisors-tab section-divider">', unsafe_allow_html=True)

    # --- Advisory Board Section ---
    st.markdown('<div class="team-advisors-tab"><h2 class="section-title" style="text-align:center;">Advisory Board</h2></div>', unsafe_allow_html=True)
    advisors = [
        {"name": "Supria Dhanda", "role": "CEO, WYSER", "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/Supria.jpeg", "linkedin": "https://linkedin.com/in/supriadhanda", "bio": "Supria brings expertise in AI..."},
        {"name": "Satyakam Mohanty", "role": "Entrepreneur", "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/Satyakam.png", "linkedin": "https://linkedin.com/in/satymohanty", "bio": "Satyakam brings expertise in building AI-driven startups..."},
        {"name": "Krishna Prasad", "role": "Tech Manager, CeNSE IISc", "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/krishna.png", "linkedin": "https://linkedin.com/in/placeholder", "bio": "Krishna guides in integrating advanced sensor systems..."},
        {"name": "Dr. Vijay Mishra", "role": "Ex-CTO, CeNSE IISc", "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/Vijay.jpg", "linkedin": "https://linkedin.com/in/placeholder", "bio": "Dr. Vijay Mishra brings decades of leadership..."},
        {"name": "Rohan Ganapathy", "role": "CEO, Bellatrix Aerospace", "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/rohan.png", "linkedin": "https://linkedin.com/in/rohanmganapathy", "bio": "Rohan brings deep-tech startup expertise..."},
        {"name": "Sandeep Bahl", "role": "Vice President, NASSCOM", "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/Sandeep.png", "linkedin": "https://linkedin.com/in/sandeepbahl1", "bio": "Sandeep provides access to a vast network..."}
    ]
    for i in range(0, len(advisors), 3):
        cols = st.columns(3)
        for j, advisor in enumerate(advisors[i:i+3]):
            with cols[j]:
                st.markdown(f"""
                    <a href="{advisor['linkedin']}" target="_blank" style="text-decoration: none;">
                        <div class="team-advisors-tab profile-container">
                            <img src="{load_image(advisor['image'])}" class="profile-image">
                            <div class="profile-name">{advisor['name']}</div>
                            <div class="profile-role">{advisor['role']}</div>
                        </div>
                    </a>
                """, unsafe_allow_html=True)
                with st.expander(f"About {advisor['name']}"):
                    st.markdown(f'<div class="team-advisors-tab profile-details">{advisor["bio"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="team-advisors-tab summary-text">Our advisors bring world-class expertise to propel our global impact.</div>', unsafe_allow_html=True)
    st.markdown('<hr class="team-advisors-tab section-divider">', unsafe_allow_html=True)

    # --- Supported By Section ---
    institutions = [
        {"name": "Indian Institute of Science (IISc)", "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/iisc.jpg"},
        {"name": "NSRCEL (IIM Bangalore)", "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/Nsrcel.jpg"},
        {"name": "Deshpande Foundation", "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/deshpande.png"},
        {"name": "CMRIT", "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/cmrit.png"}
    ]
    logos_html = ""
    for inst in institutions:
        logo_data = load_image(inst['image'])
        logos_html += f'<img src="{logo_data}" class="institution-logo-img" title="{inst["name"]}">'
    st.markdown(
        f"""
        <div class="team-advisors-tab">
            <div class="supported-by-section">
                <h2 class="section-title">Supported By</h2>
                <div class="institutions-grid">
                    {logos_html}
                </div>
                <div class="summary-text">Supported by top institutions, we are set to redefine e-mobility.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<hr class="team-advisors-tab section-divider">', unsafe_allow_html=True)

    # --- Media Coverage Section ---
    st.markdown(
        '<div class="team-advisors-tab media-container"><h2 class="section-title">Media Coverage</h2></div>',
        unsafe_allow_html=True
    )
    articles = [
        {
            "title": "The Other Switch Mobility in the EV Space: A Homegrown Solution for Smarter, Healthier E-Cycles",
            "url": "https://auto.economictimes.indiatimes.com/news/auto-components/the-other-switch-mobility-in-the-ev-space-a-homegrown-solution-for-smarter-healthier-e-cycles/113169775"
        },
        {
            "title": "How Innovations in Ebike Technology Are Changing the Way We Ride",
            "url": "https://www.linkedin.com/pulse/how-innovations-ebike-technology-changing-way-we-ride-1yxyc/?trackingId=RREz6SP9lSasyfAmbx%2Fruw%3D%3D"
        }
    ]
    for article in articles:
        st.markdown(
            f"""
            <div class="team-advisors-tab article-item">
                <a href="{article['url']}" target="_blank" class="article-title">{article['title']}</a>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown('<hr class="team-advisors-tab section-divider">', unsafe_allow_html=True)

    # --- Connect With Us Section ---
    st.markdown(
        '<div class="team-advisors-tab connect-container"><h2 class="section-title">Connect With Us</h2></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <div class="team-advisors-tab connect-links">
            <a href="https://www.linkedin.com/company/switchmobility/" target="_blank" class="connect-button"><span class="connect-icon">🔗</span> LinkedIn</a>
            <a href="https://www.switchmobility.in/" target="_blank" class="connect-button"><span class="connect-icon">🌐</span> Website</a>
        </div>
        <div class="team-advisors-tab summary-text">Follow our journey and connect with us on social media and our website!</div>
        """,
        unsafe_allow_html=True
    )
with tabs[9]:
    import streamlit as st
    import plotly.graph_objects as go
    import pandas as pd

    # --- Header ---
    st.header("💰 Funding Ask & Use", anchor=False)
    st.caption("Our Strategic Roadmap for Investment and Growth")

    # --- Data Preparation ---
    year1_data = [
        {"milestone": "Functional Version 1 Development", "timeline": "Month 1-2", "cost_lakh": 26.2, "category": "R&D"},
        {"milestone": "System Integration & Testing", "timeline": "Month 3-4", "cost_lakh": 18.5, "category": "R&D"},
        {"milestone": "Manufacturing Preparation & Supply Chain Setup (100 units)", "timeline": "Month 5-6", "cost_lakh": 17.72, "category": "Manufacturing"},
        {"milestone": "Production Scaling", "timeline": "Month 7-8", "cost_lakh": 22.0, "category": "Manufacturing"},
        {"milestone": "Business Expansion & OEM Partnerships", "timeline": "Month 9-10", "cost_lakh": 18.0, "category": "Business Expansion"},
        {"milestone": "Entry into Europe & US Markets", "timeline": "Month 11-12", "cost_lakh": 17.58, "category": "Business Expansion"},
    ]

    year2_data = [
        {"milestone": "Mass Manufacturing (10,000 units)", "timeline": "Month 13-15", "cost_lakh": 80.0, "category": "Manufacturing"},
        {"milestone": "Global Certifications & Compliance", "timeline": "Month 16-17", "cost_lakh": 40.0, "category": "Compliance"},
        {"milestone": "International OEM Partnerships", "timeline": "Month 18-19", "cost_lakh": 60.0, "category": "Business Expansion"},
        {"milestone": "Manufacturing Facility Expansion", "timeline": "Month 20-21", "cost_lakh": 50.0, "category": "Manufacturing"},
        {"milestone": "Final Scaling & Marketing Push", "timeline": "Month 22-24", "cost_lakh": 50.0, "category": "Business Expansion"},
    ]

    all_data = year1_data + year2_data
    df = pd.DataFrame(all_data)

    # --- CSS for Styling ---
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Figtree:wght@400;600;700&display=swap');

        .funding-tab {
            font-family: 'Figtree', sans-serif;
        }
        .funding-tab .funding-tab-container {
            background: #1E1E1E;
        }
        .funding-tab .milestone-card {
            background: linear-gradient(135deg, #2e2e2e, #1B3C53);
            border-left: 5px solid #00FF7F;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .funding-tab .milestone-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 255, 127, 0.3);
        }
        .funding-tab .milestone-title {
            font-size: 18px;
            font-weight: 600;
            color: #FFFFFF;
            margin: 0;
        }
        .funding-tab .milestone-cost {
            font-size: 20px;
            font-weight: 700;
            color: #00FF7F;
            margin: 0;
        }
        .funding-tab .milestone-timeline {
            font-size: 14px;
            color: #A8F1FF;
            opacity: 0.8;
        }
        .funding-tab .milestone-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }
        .funding-tab .st-emotion-cache-1r6slb0 { /* Expander header color */
            color: #A8F1FF !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- 1. Top-Line Metrics ---
    with st.container():
        st.markdown('<div class="funding-tab">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Total Funding Ask", value="₹ 4 Crore", delta="Pre-Seed Round")
        col2.metric(label="Implementation Timeline", value="24 Months")
        col3.metric(label="Primary Goal", value="Full Market Entry & Scale")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # --- 2. Visual Breakdown ---
    st.subheader("Visual Use of Proceeds")

    # Aggregate data for the donut chart
    category_costs = df.groupby('category')['cost_lakh'].sum().reset_index()
    category_costs['cost_crore'] = category_costs['cost_lakh'] / 100

    # Create the donut chart
    fig = go.Figure(data=[go.Pie(
        labels=category_costs['category'],
        values=category_costs['cost_lakh'],
        hole=.6,
        hoverinfo='label+percent',
        textinfo='label',
        texttemplate='%{label}<br>₹%{value:.2f}L',
        marker=dict(colors=['#00FF7F', '#A8F1FF', '#FFA500', '#1E90FF']),
        pull=[0.02, 0.02, 0.02, 0.02]
    )])

    fig.update_layout(
        showlegend=False,
        height=400,
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#FFFFFF")
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # --- 3. Interactive Timeline ---
    st.subheader("Milestone-Based Allocation")

    # Create tabs for Year 1 and Year 2
    tab1, tab2 = st.tabs(["🗓️ Year 1 Plan (Total: ₹ 1.2 Cr)", "🗓️ Year 2 Plan (Total: ₹ 2.8 Cr)"])

    with tab1:
        st.markdown('<div class="funding-tab">', unsafe_allow_html=True)
        for item in year1_data:
            st.markdown(
                f"""
                <div class="milestone-card">
                    <div class="milestone-header">
                        <div>
                            <p class="milestone-title">{item['milestone']}</p>
                            <p class="milestone-timeline">{item['timeline']}</p>
                        </div>
                        <p class="milestone-cost">₹ {item['cost_lakh']:.2f} L</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="funding-tab">', unsafe_allow_html=True)
        for item in year2_data:
            st.markdown(
                f"""
                <div class="milestone-card">
                    <div class="milestone-header">
                        <div>
                            <p class="milestone-title">{item['milestone']}</p>
                            <p class="milestone-timeline">{item['timeline']}</p>
                        </div>
                        <p class="milestone-cost">₹ {item['cost_lakh']:.2f} L</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)


with tabs[10]:
    st.header("🚀 Future Technology", anchor=False)
    st.caption("Our Strategic Roadmap for Innovation and Growth")

    # --- Data Preparation ---
    future_tech_data = {
        "Drive & Control": {
            "icon": "⚙️",
            "details": [
                "High Efficiency torque control systems",
                "Compact power sensors",
                "Purpose-built UI",
                "Environment sensor"
            ]
        },
        "Business": {
            "icon": "📈",
            "details": [
                "Partner with a European OEM",
                "Expand assembly facility",
                "Establish an R&D hub",
                "Develop next-gen power systems"
            ]
        },
        "Energy Management": {
            "icon": "🔋",
            "details": [
                "Battery Safety and protection",
                "Gauging Technology",
                "Regeneration/Efficiency Solutions",
                "Charging Hardware",
                "Docking & special Hardware Systems"
            ]
        },
        "Mobility Ecosystem Technology": {
            "icon": "🌐",
            "details": [
                "Intelligent illuminations / Road presence systems",
                "Theft proofing technology",
                "Frame building",
                "Shared vehicles",
                "Cargo Ebikes",
                "Ebike Fleet System",
                "Ebike Diagnostic tool"
            ]
        }
    }

    # --- CSS for the Detail Boxes ---
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Figtree:wght@400;600;700&display=swap');

        .future-tech-tab {
            font-family: 'Figtree', sans-serif;
        }
        .future-tech-tab .detail-box {
            background-color: #1E1E1E;
            border: 1px solid #00FF7F;
            border-radius: 8px;
            padding: 25px;
            margin-top: 20px;
            box-shadow: 0 0 15px rgba(0, 255, 127, 0.2);
            height: 100%; /* Make boxes in a row the same height */
        }
        .future-tech-tab .detail-box h3 {
            color: #00FF7F;
            margin-top: 0;
            border-bottom: 2px solid #A8F1FF;
            padding-bottom: 10px;
        }
        .future-tech-tab .detail-box ul {
            list-style-type: none;
            padding-left: 0;
        }
        .future-tech-tab .detail-box li {
            color: #FFFFFF;
            margin-bottom: 10px;
            padding-left: 25px;
            position: relative;
        }
        .future-tech-tab .detail-box li::before {
            content: '⚡';
            position: absolute;
            left: 0;
            color: #A8F1FF;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- Display All Categories in a 2x2 Grid ---
    # Create two columns for the top row
    col1, col2 = st.columns(2)

    # Data for the top row
    top_row_keys = ["Drive & Control", "Business"]
    # Data for the bottom row
    bottom_row_keys = ["Energy Management", "Mobility Ecosystem Technology"]

    # Populate the top row
    with col1:
        key = top_row_keys[0]
        data = future_tech_data[key]
        details_html = ''.join([f"<li>{item}</li>" for item in data['details']])
        st.markdown(
            f"""
            <div class="future-tech-tab">
                <div class="detail-box">
                    <h3>{data['icon']} {key}</h3>
                    <ul>{details_html}</ul>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        key = top_row_keys[1]
        data = future_tech_data[key]
        details_html = ''.join([f"<li>{item}</li>" for item in data['details']])
        st.markdown(
            f"""
            <div class="future-tech-tab">
                <div class="detail-box">
                    <h3>{data['icon']} {key}</h3>
                    <ul>{details_html}</ul>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Create two columns for the bottom row
    col3, col4 = st.columns(2)

    # Populate the bottom row
    with col3:
        key = bottom_row_keys[0]
        data = future_tech_data[key]
        details_html = ''.join([f"<li>{item}</li>" for item in data['details']])
        st.markdown(
            f"""
            <div class="future-tech-tab">
                <div class="detail-box">
                    <h3>{data['icon']} {key}</h3>
                    <ul>{details_html}</ul>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        key = bottom_row_keys[1]
        data = future_tech_data[key]
        details_html = ''.join([f"<li>{item}</li>" for item in data['details']])
        st.markdown(
            f"""
            <div class="future-tech-tab">
                <div class="detail-box">
                    <h3>{data['icon']} {key}</h3>
                    <ul>{details_html}</ul>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

with tabs[11]:
    import streamlit as st
    from pathlib import Path

    st.header("🎙️ Audio Pitch", anchor=False)
    st.caption("Listen to Our Vision for the Future of E-Mobility")

    # --- CSS for Audio Pitch ---
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Figtree:wght@400;600;700&display=swap');
        .audio-pitch-tab {
            font-family: 'Figtree', sans-serif;
            text-align: center;
        }
        .audio-pitch-tab .audio-container {
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #1B3C53, #2e2e2e);
            border: 3px solid #00FF7F;
            border-radius: 8px;
            padding: 20px;
            margin: 20px auto;
            max-width: 600px;
            box-shadow: 0 0 15px rgba(0, 255, 127, 0.2);
        }
        .audio-pitch-tab .audio-player {
            width: 100%;
            max-width: 500px;
        }
        .audio-pitch-tab .summary-text {
            color: #A8F1FF;
            font-size: 16px;
            max-width: 500px;
            margin: 20px auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- Load and Display Audio ---
    audio_path = Path(r"https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/audio\powerpedal_audio_pitch.mp3")
    try:
        if audio_path.is_file():
            st.markdown('<div class="audio-pitch-tab audio-container">', unsafe_allow_html=True)
            st.audio(str(audio_path), format="audio/mp3")
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('<div class="audio-pitch-tab summary-text">Hear our pitch to discover how we’re revolutionizing e-mobility.</div>', unsafe_allow_html=True)
        else:
            st.warning("Audio file 'powerpedal_audio_pitch.mp3' not found. Please ensure the file is in the correct directory.")
    except Exception as e:
        st.error(f"Error loading audio file: {e}")
