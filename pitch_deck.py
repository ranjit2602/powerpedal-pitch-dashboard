import streamlit as st
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from io import BytesIO
from PIL import Image

st.set_page_config(
    page_title="PowerPedal Interactive Pitch Deck",
    layout="wide",
    page_icon="https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/logo.png"
)

# Use st.markdown with HTML to embed the image and text as a single title element
st.markdown(
    """
    <h1 class='main-title'>
        <div class='main-title-logo-container'>
            <img src="https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/logo.png" style="height: 40px; vertical-align: text-bottom;">
            <span class='powerpedal-wordmark'><i>powerpedal</i></span>
        </div>
        <div class='main-title-tagline'>
            <i>- The Future of Smart Urban Mobility</i>
        </div>
    </h1>
    """,
    unsafe_allow_html=True
)

st.caption("Switch Mobility | Interactive Investor Deck")

st.markdown(
    """
    <details>
      <summary style="font-size:16px; font-weight:bold; cursor:pointer;">
        👋 A Quick Guide to Navigating Our Dashboard
      </summary>
      <div style="margin-top:10px;">
        <p>
        This isn't a traditional static presentation. This interactive pitch deck is designed for you to explore our vision and business in depth, at your own pace.
        </p>
        <h4>Here’s how to get the most out of it:</h4>
        <ol>
          <li><b>Navigate with the Tabs:</b> The tabs at the top of the page act as your table of contents. Click on any tab to jump to a specific section of our pitch, from our <b>Vision</b> to our <b>Financials</b>.</li>
          <li><b>Look for Interactive Elements:</b> Many sections contain interactive charts, sliders, and dropdown menus. These tools allow you to dive deeper into our market analysis, play with our financial projections, and see our data in real-time.</li>
          <li><b>Explore the Problem:</b> Don't miss our detailed breakdown of the market challenges. You can click on each challenge to see our specific solutions and how they directly address the pain points.</li>
          <li><b>Listen to the Audio Pitch:</b> For a quick, narrated summary of our entire presentation, click on the <b>Audio Pitch</b> tab at any time.</li>
        </ol>
        <p>Enjoy the presentation! We're excited to show you the future of smart urban mobility.</p>
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

# ---- Global CSS for the entire app, including responsive styles ----
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@700&display=swap" rel="stylesheet">
    <style>
        /* Import Figtree and Oswald fonts */
        @import url('https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@700&display=swap');

        /* Apply Figtree globally to all elements */
        * {
            font-family: 'Figtree', sans-serif !important;
        }

        /* Specific font and consistent color/weight for the wordmark and tagline */
        .powerpedal-wordmark, .main-title-tagline {
            font-family: 'Oswald', sans-serif !important;
            font-weight: 700 !important;
            color: #E0E0E0 !important; /* Light Grey */
            opacity: 1 !important; /* Ensure full opacity */
        }

        /* --- Global styles for the title (desktop) --- */
        .main-title {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .main-title-tagline {
            font-size: 1em;
            margin-left: 10px;
        }
        .main-title-logo-container img {
            height: 40px;
            vertical-align: text-bottom;
        }
        .powerpedal-wordmark {
            font-size: 1.1em; /* Slightly increases the wordmark size */
        }
        
        /* --- Mobile-specific styles (on screens <= 768px) --- */
        @media (max-width: 768px) {
            .st-emotion-cache-1dumvfu {
                padding-top: 0.5rem !important;
            }
            .st-emotion-cache-z5in97 {
                margin-top: -20px !important; 
            }
            .main-title {
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
                font-size: 7vw !important; /* Increased font size */
            }
            .main-title-logo-container {
                display: flex;
                align-items: center;
                gap: 5px;
                white-space: nowrap; /* Keep logo and 'powerpedal' on one line */
            }
            .main-title-logo-container img {
                height: 6.5vw !important; /* Increased logo size */
                vertical-align: text-bottom !important;
            }
            .powerpedal-wordmark {
                font-size: 1.4em !important; /* Increased wordmark size */
                transform: translateY(-8px) !important; /* Pushes the text up for better alignment */
            }
            .main-title-tagline {
                font-size: 0.6em !important; /* Relative to the h1 font size */
                margin-left: 0;
            }
            .stTabs [data-baseweb="tab-list"] {
                flex-wrap: wrap !important;
                gap: 5px !important;
            }
            .stTabs [data-baseweb="tab"] {
                font-size: 8px !important;
                font-weight: 500 !important;
                padding: 4px 6px !important;
                flex: 1 1 auto !important;
            }
            .stTabs [data-baseweb="tab"] > div {
                font-size: 8px !important;
            }
            summary {
                font-size: 8px !important; /* Reduced to half size on mobile */
            }
            /* Sets the content inside the details tag to the same size as the summary */
            details div p, details div h4, details div ul, details div li {
                font-size: 8px !important;
            }
            .challenge-button-card {
                padding: 10px;
                border-radius: 10px;
                text-align: center;
                color: #E0E0E0;
                background-color: #1B3C53;
                border: 2px solid #1B3C53;
                cursor: pointer;
                transition: all 0.3s;
                margin-bottom: 10px;
            }
            .challenge-button-card:hover {
                border-color: #A8F1FF;
            }
            .challenge-button-card.active {
                border-color: #78C841;
                transform: scale(1.05);
            }
        }
        /* --- End of mobile styles --- */

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
        
        /* New CSS for the Business Model & Problem containers */
        .details-card {
            background: linear-gradient(135deg, #1B3C53, #2e2e2e);
            border: 2px solid #78C841;
            border-radius: 12px;
            max-width: 1200px;
            margin: 20px auto;
        }
        .details-card[open] {
            background: linear-gradient(135deg, #2e2e2e, #1B3C53);
            border: 3px solid #A8F1FF !important;
            box-shadow: 0 0 15px rgba(120, 200, 65, 0.6);
        }
        .details-card summary {
            font-size: 18px;
            font-weight: 600;
            color: #78C841;
            cursor: pointer;
            outline: none;
            padding: 15px;
        }
        .details-card .expander-content-body {
            padding: 15px;
        }
        .details-card .expander-content-body h3 {
            font-size: 20px;
            color: #78C841;
            margin: 10px 0;
        }
        .details-card .expander-content-body p, .details-card .expander-content-body ul, .details-card .expander-content-body li {
            font-size: 14px;
            line-height: 1.5;
            margin: 5px 0;
            color: #A8F1FF;
        }
        .details-card .expander-content-body ul {
            padding-left: 20px;
        }

        /* Styles for the Vision & Mission and Problem cards */
        .info-card {
            border: 1px solid #1B3C53;
            border-radius: 10px;
            padding: 20px;
            background-color: #1B3C53;
            margin-top: 10px;
            margin-bottom: 10px;
        }
        .info-card h3 {
            color: #78C841;
            margin-top: 0;
            margin-bottom: 10px;
        }
        .info-card p {
            font-size: 20px;
            font-style: italic;
            color: #FFF5F2;
            margin-bottom: 0;
        }
        
        .problem-card-static {
            background: linear-gradient(135deg, #1B3C53, #2e2e2e);
            border: 2px solid #78C841;
            border-radius: 12px;
            padding: 15px;
            margin: 10px 0;
        }
        .problem-card-static h3 {
            color: #78C841;
            margin: 0 0 10px 0;
            font-size: 18px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .problem-card-static p {
            color: #A8F1FF;
            font-size: 14px;
            line-height: 1.5;
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
        response = requests.get(file_name)
        response.raise_for_status()
        df = pd.read_excel(BytesIO(response.content))
        if not all(col in df.columns for col in expected_columns):
            st.warning(f"Expected columns {expected_columns} not found in {file_name}. Using fallback data.")
            if transpose and isinstance(fallback_data, pd.DataFrame):
                return fallback_data, f"Column mismatch in {file_name}"
            elif not transpose and isinstance(fallback_data, pd.DataFrame):
                return fallback_data, f"Column mismatch in {file_name}"
            else:
                return pd.DataFrame(fallback_data), f"Column mismatch in {file_name}"
        return df, None
    except Exception as e:
        st.warning(f"Error loading {file_name}: {str(e)}. Using fallback data.")
        if transpose and isinstance(fallback_data, pd.DataFrame):
            return fallback_data, str(e)
        elif not transpose and isinstance(fallback_data, pd.DataFrame):
            return fallback_data, str(e)
        else:
            return pd.DataFrame(fallback_data), str(e)

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

    # Display problem.png (centered and smaller)
    problem_image_path = "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/problem.png"
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(problem_image_path, use_container_width=True, width=700)

    st.markdown(
        """
        <p class='problem-text' style='font-size: 18px; color: #e0e0e0; text-align: center; margin: 20px 0;'>
            Current e-bike drive systems face significant hurdles that limit performance, affordability, and scalability. Below are the key challenges our solution addresses.
        </p>
        """,
        unsafe_allow_html=True
    )

    # Challenge data with proper Markdown formatting
    challenges = [
        {
            "icon": "🚲",
            "title": "Inefficient Ride",
            "detailed_desc": """
                ### Poor cadence sensors, expensive torque sensors

                In many low-cost Chinese drive systems, cadence-based pedal assist dominates. Cadence sensors only detect if the pedals are turning — they don’t measure how hard the rider is pedaling.

                - This results in delayed motor activation, abrupt surges, and assistance that feels disconnected from rider effort.
                - While torque sensors provide a much smoother and more natural ride by measuring actual pedaling force, they are significantly more expensive, which pushes up system cost.
                - In practice, OEMs often opt for cadence sensors to keep prices low, sacrificing efficiency and ride quality.
            """
        },
        {
            "icon": "💰",
            "title": "High Costs",
            "detailed_desc": """
                ### Japanese and European systems are too expensive

                Japanese and European drive systems deliver top-tier refinement, reliability, and performance — but at a price that’s out of reach for many OEMs in emerging markets.

                - The drive unit cost alone can make up 30–50% of an eBike’s retail price.
                - This pricing model locks out small to mid-size manufacturers and limits the spread of high-performance eBikes in cost-sensitive regions.
            """
        },
        {
            "icon": "⚙️⚙️",
            "title": "Integration Issues",
            "detailed_desc": """
                ### Lack of interoperability, difficult to integrate, no diagnostics, causing downtime

                - Many existing systems are closed ecosystems, making them hard to integrate with third-party components.
                - Limited compatibility with different displays, batteries, and controllers forces OEMs into vendor lock-in.
                - Integration can require custom wiring harnesses, firmware changes, and long trial-and-error cycles.
                - The absence of built-in self-diagnostics means even small issues require manual troubleshooting, increasing downtime and service costs.
            """
        },
        {
            "icon": "📉",
            "title": "Limited Features",
            "detailed_desc": """
                ### Lack of affordable remote diagnostics and smart analytics

                While premium systems offer connected apps, cloud analytics, and remote troubleshooting, affordable drive systems rarely include these features.
                
                - Without remote diagnostics, problems are identified only after a manual inspection, delaying repairs.
                - The absence of usage analytics means there’s no visibility into rider behavior, battery health trends, or early signs of failure.
                - This results in reactive maintenance, higher operational costs, and missed opportunities to improve performance over time.
            """
        }
    ]

    # Display each problem in a static, colored container
    for challenge in challenges:
        with st.container():
            st.markdown(
                f"""
                <div class="problem-card-static">
                    <h3 style='color: #78C841; margin-top: 0;'>{challenge['icon']} &nbsp;&nbsp;{challenge['title']}</h3>
                    <div style='color: #A8F1FF; font-size: 16px;'>
                        {challenge['detailed_desc']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import pi

# Helper function to load data from URL
def load_excel_data(url, expected_columns, fallback_data, transpose=False):
    """Loads data from a specified URL, with fallback."""
    try:
        df = pd.read_excel(url)
        if transpose:
            df = df.T
            df.columns = df.iloc[0]
            df = df[1:]
        
        # Check if the columns match the expected ones
        if list(df.columns) != expected_columns:
            st.warning(f"Columns in the Excel file at {url} do not match the expected structure. Using fallback data.")
            if isinstance(fallback_data, pd.DataFrame):
                return fallback_data, "Using fallback data due to column mismatch."
            else:
                return pd.DataFrame(fallback_data, columns=expected_columns), "Using fallback data due to column mismatch."
        return df, None
    except Exception as e:
        st.error(f"Error loading data from {url}: {e}. Using fallback data.")
        if isinstance(fallback_data, pd.DataFrame):
            return fallback_data, f"Error loading data: {e}. Using fallback."
        else:
            return pd.DataFrame(fallback_data, columns=expected_columns), f"Error loading data: {e}. Using fallback."

# Helper function to create HTML table
def create_html_table(df, title):
    html_output = f"<h5 style='color:#e0e0e0;'>{title}</h5>"
    html_output += "<table style='width:100%; border-collapse: collapse;'>"
    html_output += "<thead style='background-color: #333333; color: #ffffff;'>"
    html_output += "<tr>"
    for col in df.columns:
        html_output += f"<th style='padding: 8px; border: 1px solid #444; text-align: left;'>{col}</th>"
    html_output += "</tr>"
    html_output += "</thead>"
    html_output += "<tbody>"
    for _, row in df.iterrows():
        html_output += "<tr>"
        for item in row:
            html_output += f"<td style='padding: 8px; border: 1px solid #444; text-align: left; color:#e0e0e0;'>{item}</td>"
        html_output += "</tr>"
    html_output += "</tbody>"
    html_output += "</table>"
    return html_output

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
        "Average Price": ["Average price ~ €1,200-1,500", "Average price ~ €3,000-3-500", "Average price ~ €1,400-2-000"]
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
            .market-opportunity-tab .table-viz-container {
                display: flex;
                align-items: flex-start;
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
                justify-content: flex-start;
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
        
        # New layout for SVG and Selectbox
        col_svg, col_select = st.columns([1, 1])
        with col_svg:
            st.markdown(
                """
                <div style="display: flex; justify-content: center; align-items: center; margin: 0; padding: 0;">
                    <div class="svg-container" style="position: relative; width: 450px; height: 300px;">
                        <svg width="450" height="300" viewBox="-225 -150 500 300">
                            <circle id="pam" cx="0" cy="0" r="150" fill="#3E3F29" opacity="0.7"></circle>
                            <circle id="tam" cx="0" cy="0" r="110" fill="#819067" opacity="0.7"></circle>
                            <circle id="sam" cx="0" cy="0" r="70" fill="#A08963" opacity="0.7"></circle>
                            <circle id="som" cx="0" cy="0" r="30" fill="#2E2E2E" opacity="0.7"></circle>
                            <text x="0" y="-125" text-anchor="middle" font-size="17" fill="#e0e0e0" font-weight="bold">PAM</text>
                            <text x="0" y="-80" text-anchor="middle" font-size="15" fill="#e0e0e0">TAM</text>
                            <text x="0" y="-42" text-anchor="middle" font-size="13" fill="#e0e0e0">SAM</text>
                            <text x="0" y="-10" text-anchor="middle" font-size="12" fill="#e0e0e0">SOM</text>
                            <text x="0" y="135" text-anchor="middle" font-size="15" fill="#000000" font-weight="bold">$50.8B</text>
                            <text x="0" y="95" text-anchor="middle" font-size="13" fill="#000000" font-weight="bold">$7.16B</text>
                            <text x="0" y="52" text-anchor="middle" font-size="11" fill="#000000" font-weight="bold">$2.7B</text>
                            <text x="0" y="10" text-anchor="middle" font-size="10" fill="#000000" font-weight="bold">$0.25B</text>
                        </svg>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_select:
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
                            <p style='color: #e0e0e0; font-size: 14px; margin: 0 0 2px 0;'>{market["full_desc"]}</p>
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
            align-items: flex-start;
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
            justify-content: flex-start;
            align-items: center;
            min-height: 10px;
            box-sizing: border-box;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Tables and Visualizations Section
    
    # 1. Ebike Drive Segmentation: Dual Pie Charts
    st.markdown("---")
    st.subheader("1. Market Segmentation: Global vs. India")
    st.markdown(
        """
        <p style='color: #e0e0e0; font-size: 16px;'>
        <b>Hub drives</b> dominate the global e-bike market, and their dominance is even more pronounced in India. This is a critical finding, as PowerPedal is designed to upgrade this massive, cost-sensitive segment.
        </p>
        """, unsafe_allow_html=True
    )
    st.markdown('<div class="table-viz-container">', unsafe_allow_html=True)
    col_table1, col_viz1 = st.columns([2, 1], vertical_alignment="top")
    with col_table1:
        st.markdown(create_html_table(df_seg, "E-bike Drivetrain Segmentation and Comparison"), unsafe_allow_html=True)
        if error_seg:
            st.warning(error_seg)
    
    with col_viz1:
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
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. E-Bike Drivetrain Positioning: Spider Chart
    st.markdown("---")
    st.subheader("2. Drivetrain Positioning: Where PowerPedal Sits")
    st.markdown(
        """
        <p style='color: #e0e0e0; font-size: 16px;'>
        PowerPedal is strategically positioned as a <b>"bridge technology"</b> between the low-cost, low-performance hub drive and the expensive, high-performance mid-drive. It offers the performance and features of premium systems at a fraction of the cost.
        </p>
        """, unsafe_allow_html=True
    )

    st.markdown('<div class="table-viz-container">', unsafe_allow_html=True)
    col_table2, col_viz2 = st.columns([2, 1], vertical_alignment="top")
    with col_table2:
        st.markdown(create_html_table(df_pos.T, "E-Bike Drivetrain Positioning"), unsafe_allow_html=True)
        if error_pos:
            st.warning(error_pos)

    with col_viz2:
        # Data for spider chart
        categories = ['Cost', 'Performance', 'Efficiency', 'Features']
        
        # A mapping of qualitative values to a numerical scale
        value_map = {
            'Low cost': 3, 'Slight premium over hub e-bikes(€150-200)': 2, 'Expensive': 1,
            'Poor performance': 1, 'Amazing performance': 3,
            'Low efficiency': 1, 'High efficiency': 3,
            'No Features': 1, 'Feature rich': 3, 'Usually feature rich': 3,
        }

        # Re-map the data for the radar chart
        data_to_plot = {
            'Hub driven e-bike': [value_map.get(df_pos.loc[cat, 'Hub driven e-bike'], 0) for cat in categories],
            'Mid driven e-bike': [value_map.get(df_pos.loc[cat, 'Mid driven e-bike'], 0) for cat in categories],
            'PowerPedal driven e-bike': [value_map.get(df_pos.loc[cat, 'PowerPedal driven e-bike'], 0) for cat in categories]
        }
        
        # Spider chart creation
        fig, ax = plt.subplots(figsize=(6.5, 6), subplot_kw=dict(polar=True))
        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')

        # Adjust subplot position to create more space for labels
        fig.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)

        # Number of variables we're plotting.
        num_vars = len(categories)
        # Calculate angle for each axis.
        angles = np.linspace(0, 2 * pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]
        
        # Brighter, more distinct colors
        colors = {'Hub driven e-bike': '#FF6347', 'Mid driven e-bike': '#FFD700', 'PowerPedal driven e-bike': '#00BFFF'}
        
        for name, values in data_to_plot.items():
            values += values[:1]
            ax.plot(angles, values, color=colors[name], linewidth=2, linestyle='solid', label=name)
            ax.fill(angles, values, color=colors[name], alpha=0.45)

        # Draw axis lines and labels
        ax.set_theta_offset(pi / 2)
        ax.set_theta_direction(-1)
        ax.set_rlabel_position(0)
        
        # Corrected method for setting labels and padding
        ax.set_thetagrids(np.degrees(angles[:-1]), labels=categories, color='#e0e0e0', fontsize=9)
        ax.tick_params(axis='x', which='both', pad=30)
        
        ax.set_yticklabels([])
        ax.set_ylim(0, 3)
        ax.grid(color='#555555')

        # Add a custom legend
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=8, frameon=False, labelcolor='#e0e0e0')
        
        st.pyplot(fig)
        
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. PowerPedal's Market Positioning: Visual Checklist
    st.markdown("---")
    st.subheader("3. PowerPedal’s Core Advantages")
    st.markdown(
        """
        <p style='color: #e0e0e0; font-size: 16px;'>
        PowerPedal's unique selling points create a strong competitive advantage by targeting the largest e-bike market segment and providing superior features at an accessible price.
        </p>
        """, unsafe_allow_html=True
    )
    st.markdown('<div class="table-viz-container">', unsafe_allow_html=True)
    col_table3, col_viz3 = st.columns([2, 1], vertical_alignment="top")
    with col_table3:
        st.markdown(create_html_table(df_market, "PowerPedal’s Market Positioning"), unsafe_allow_html=True)
        if error_market:
            st.warning(error_market)
    
    with col_viz3:
        st.markdown(
            """
            <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 20px;">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 24px; color: #78C841; margin-right: 10px;">✅</span>
                    <h6 style="margin: 0; color: #e0e0e0;"><b>Bridging the Gap</b></h6>
                </div>
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 24px; color: #78C841; margin-right: 10px;">✅</span>
                    <h6 style="margin: 0; color: #e0e0e0;"><b>Cost-Effective</b></h6>
                </div>
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 24px; color: #78C841; margin-right: 10px;">✅</span>
                    <h6 style="margin: 0; color: #e0e0e0;"><b>High Efficiency</b></h6>
                </div>
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 24px; color: #78C841; margin-right: 10px;">✅</span>
                    <h6 style="margin: 0; color: #e0e0e0;"><b>Retrofittable</b></h6>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

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

with tabs[3]:
    # ---- Main Product Page Layout ----
    st.header("Meet PowerPedal")
    st.caption("The Smart, Affordable, and High-Performance eBike Drive System")

    # Main Banner with Image and Tagline - Centered
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.image("https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/product.png", use_container_width=True)
        st.markdown(
            '<div style="text-align: center; font-size: 22px; font-weight: 600; color: #FFF5F2; background: linear-gradient(45deg, #1B3C53, #78C841); padding: 10px 20px; border-radius: 8px; margin: 0 auto;">Mid-drive experience. Rear hub affordability.</div>',
            unsafe_allow_html=True
        )
    st.markdown("""
    <div style="text-align: center; max-width: 800px; margin: 20px auto; padding: 20px; background: linear-gradient(135deg, #1B3C53, #2e2e2e); border: 2px solid #78C841; border-radius: 12px; color: #FFF5F2;">
        PowerPedal is a revolutionary eBike drive system that combines mid-drive performance with rear hub affordability. Designed for efficiency and compatibility, it offers a seamless riding experience with advanced torque-sensing technology.
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.header("Product Components")

    # Power Sensor Card - Centered
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown(f'<div style="text-align: center; border: 2px solid #78C841; border-radius: 12px; padding: 20px; background: linear-gradient(135deg, #1B3C53, #2e2e2e);"><h3>Power Sensor – The “muscle detector” of the rider’s eBike</h3><img src="https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/powersense.png" style="max-width: 250px; border-radius: 8px; margin-top: 15px;" /><p style="color: #A8F1FF; margin-top: 15px;">Picture a clever little device tucked inside the rider’s pedal system—the PowerPedal Power Sensor—measuring every bit of force applied with stunning ±2% accuracy. In less than 10 milliseconds, it whisks this data to the controller, painting a vivid picture of the rider’s journey. Unlike basic cadence-based systems that merely tally pedal spins, this sensor knows whether the rider is gliding effortlessly or conquering a steep hill, ensuring the motor responds instantly with just the right boost. Say goodbye to jerky starts or wasted battery—every ride becomes a smooth, natural dance with the road!</p></div>', unsafe_allow_html=True)

    # Controller Card - Centered
    col4, col5, col6 = st.columns([1, 4, 1])
    with col5:
        st.markdown(f'<div style="text-align: center; border: 2px solid #78C841; border-radius: 12px; padding: 20px; background: linear-gradient(135deg, #1B3C53, #2e2e2e);"><h3>Controller – The brain that makes split-second decisions</h3><img src="https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/powerdrive.png" style="max-width: 250px; border-radius: 8px; margin-top: 15px;" /><p style="color: #A8F1FF; margin-top: 15px;">Step into the mind of the rider’s eBike with the Controller—a brilliant brain processing live data from the power sensor, battery, and motor hundreds of times per second. It calculates torque, speed, and efficiency, delivering a power-packed 250W to 350W of assistance with a 1:1 to 3:1 ratio—meaning it can amplify the rider’s effort up to three times! Hills and headwinds melt away, doubling the rider’s range on a single charge. This versatile genius works with nearly any eBike motor, hub or mid-drive, and its remote diagnostics let the support team troubleshoot or fix issues online.</p></div>', unsafe_allow_html=True)

    # HMI Control Unit Card - Centered
    col7, col8, col9 = st.columns([1, 4, 1])
    with col8:
        st.markdown(f'<div style="text-align: center; border: 2px solid #78C841; border-radius: 12px; padding: 20px; background: linear-gradient(135deg, #1B3C53, #2e2e2e);"><h3>HMI (Human–Machine Interface) – The rider’s handlebar command center</h3><img src="https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/powershift.png" style="max-width: 250px; border-radius: 8px; margin-top: 15px;" /><p style="color: #A8F1FF; margin-top: 15px;">Meet the HMI, the rider’s sleek handlebar command center that puts control in their hands. Twist the throttle for 0–100% variable control—though OEM-set speed limits keep it safe—and flip the assist level selector from eco cruising to a full-power boost. A battery State of Charge indicator, accurate to ±1%, reveals the rider’s range at a glance, while the horn switch delivers quick safety alerts in traffic. Plus, the built-in USB port powers the rider’s lights or charges their phone mid-ride—it’s a multitasking marvel!</p></div>', unsafe_allow_html=True)
    st.header("PowerPedal Mobile App – Your eBike Companion")
    cols = st.columns(4)
    app_screenshots = [
        ("https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/app_live.jpg", "Ride Dashboard: Live stats and real-time feedback."),
        ("https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/app_ride_history.jpg", "Ride History: Your personal cycling time machine."),
        ("https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/app_analytics.jpg", "Performance Analytics: Data-driven insights to ride smarter."),
        ("https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/app_diagnostic.jpg", "Remote Diagnostics: AI-powered bike mechanic in your pocket."),
    ]

    for idx, (url, desc) in enumerate(app_screenshots):
        with cols[idx]:
            st.image(url, width=150)
            st.markdown(f'<p style="font-size: 12px; color: #A8F1FF; text-align: center;">{desc}</p>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; padding: 20px; max-width: 800px; margin: 20px auto; background: linear-gradient(135deg, #1B3C53, #2e2e2e); border: 2px solid #78C841; border-radius: 12px; color: #FFF5F2;">
        <p>The PowerPedal Mobile App transforms your smartphone into a powerful control center for your eBike. Explore key features like real-time ride tracking, historical data, performance analytics, and AI-powered diagnostics. Designed for seamless integration, the app connects via Bluetooth to deliver live stats, customize settings, and provide proactive maintenance alerts—all in an intuitive interface that enhances every ride.</p>
        <p>Key highlights include the dynamic <b>Ride Dashboard</b> for instant feedback, detailed <b>Ride History</b> to track progress, insightful <b>Performance Analytics</b> for optimization, and our standout <b>Remote Diagnostics</b> feature, which uses AI to predict and resolve issues before they arise. Whether you're a casual commuter or a dedicated cyclist, this app makes your PowerPedal experience smarter and more engaging.</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.header("Testing & Performance")
    st.caption("Putting PowerPedal to the Test")

    col_tl1, col_tl2, col_tl3 = st.columns([1, 2, 1])
    with col_tl2:
        st.markdown(
            f'<div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #1B3C53, #2e2e2e); border: 2px solid #78C841; border-radius: 12px;"><h3 style="color: #78C841;">Test Lab</h3><a href="https://powerpedaltestdashboard-4tmrensx9crg9j7ezjytog.streamlit.app/" target="_blank" style="display: inline-block; padding: 10px 20px; background: linear-gradient(45deg, #78C841, #A8F1FF); color: #000000; text-decoration: none; border-radius: 8px; font-size: 18px; font-weight: 600;">Visit PowerPedal Test Dashboard</a></div>',
            unsafe_allow_html=True
        )

    st.divider()

    # Center videos and text side by side with space between
    st.markdown("""
        <div style="display: flex; flex-direction: row; justify-content: center; gap: 20px; max-width: 700px; margin: 20px auto;">
            <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #1B3C53, #2e2e2e); border: 2px solid #78C841; border-radius: 12px; width: 330px;">
                <h4 style="color: #78C841;">Efficiency Testing</h4>
                <video src="https://www.dropbox.com/scl/fi/twxuhmmg0wgpnbx8fsqnz/powerpedal_efficiency_testing.mp4?rlkey=he1nnr7mqicrovk3655gg8w2j&st=bltkehlt&dl=1" width="300" controls style="display: block; margin: 0 auto;"></video>
                <p style="color: #A8F1FF; margin-top: 15px;">Explore how PowerPedal optimizes energy use across various riding conditions, showcasing its superior efficiency and range extension.</p>
            </div>
            <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #1B3C53, #2e2e2e); border: 2px solid #78C841; border-radius: 12px; width: 330px;">
                <h4 style="color: #78C841;">Terrain Testing</h4>
                <video src="https://www.dropbox.com/scl/fi/2nv6z20pfnnrg9skipljs/powerpedal_terrain_testing.mp4?rlkey=gh5tannj0jx5l2lohen09xc4z&st=x3oep0fy&dl=1" width="300" controls style="display: block; margin: 0 auto;"></video>
                <p style="color: #A8F1FF; margin-top: 15px;">Witness PowerPedal’s performance across diverse terrains, from steep hills to rough trails, proving its versatility and durability.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
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

    # CSS
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
        .details-card {
            background: linear-gradient(135deg, #1B3C53, #2e2e2e);
            border: 2px solid #78C841;
            border-radius: 12px;
            padding: 15px;
            color: #A8F1FF;
            margin: 20px auto;
            max-width: 800px;
        }
        .details-card[open] {
            background: linear-gradient(135deg, #2e2e2e, #1B3C53);
            border: 3px solid #A8F1FF !important;
            box-shadow: 0 0 15px rgba(120, 200, 65, 0.6);
        }
        .details-card summary {
            font-size: 18px;
            font-weight: 600;
            color: #78C841;
            cursor: pointer;
            outline: none;
        }
        .details-card h3 {
            font-size: 20px;
            color: #78C841;
            margin: 10px 0;
        }
        .details-card p {
            font-size: 16px; /* Increased from 14px to 16px */
            line-height: 1.5;
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
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # First Expander - Hardware Sales
    st.markdown(
        """
        <details class="details-card">
          <summary>Hardware Sales 💰</summary>
          <h3>Hardware Sales</h3>
          <p>🛠 Sold in bulk to OEMs as the core revenue driver.</p>
          <p>📦 Each PowerPedal system is a premium, one-time purchase.</p>
          <p>
          At the heart of PowerPedal’s business model is hardware sales to eBike OEMs. 
          Our PowerPedal system — including the sensor, controller, and HMI — is supplied directly 
          to manufacturers for seamless integration into their eBike models. 
          This OEM-first approach ensures predictable, scalable revenue, 
          while positioning our technology as part of the bike’s DNA rather than an add-on.
          </p>
        </details>
        """,
        unsafe_allow_html=True
    )

    # Second Expander - AI Diagnostics Subscription
    st.markdown(
        """
        <details class="details-card">
          <summary>AI Diagnostics Subscription 📈</summary>
          <h3>AI Diagnostics Subscription</h3>
          <p>🤖 Remote monitoring, predictive maintenance, and troubleshooting.</p>
          <p>💳 Monthly per-bike fee — keeps bikes running and customers happy.</p>
          <p>
          Once our hardware is in the field, we expand the value chain through AI-powered Remote Diagnostics. 
          OEMs, dealers, and fleet operators can subscribe to our service for real-time health monitoring, 
          predictive maintenance alerts, and data-driven performance optimization. 
          These subscriptions create a steady, recurring revenue stream 
          while lowering service costs and improving rider satisfaction.
          </p>
        </details>
        """,
        unsafe_allow_html=True
    )

    # Bottom Section
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
        .gtm-tab .placeholder-image {
            width: 200px;
            height: 150px;
            background: linear-gradient(135deg, #1B3C53, #78C841);
            border: 1px solid #78C841;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
            color: #A8F1FF;
            font-size: 12px;
            text-align: center;
            padding: 10px;
            box-sizing: border-box;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    def load_image(image_url):
        """Load remote image as PIL Image or return None if fails."""
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            return image
        except Exception:
            return None

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
        image_path = load_image(year_data["image"])
        if image_path:
            st.image(image_path, use_container_width=True)
        else:
            try:
                st.image(year_data["image"], use_container_width=True)
            except Exception:
                st.markdown(
                    '<div class="placeholder-image">Year Placeholder<br><small>Image Loading...</small></div>',
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
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ---- TAB 6: Financial Projections ----
with tabs[6]:
    st.header("📈 Financial Projections")
    st.caption("From 1,000 units in 2025 → 1 Million units by 2030")
    st.markdown("**Revenue grows from ₹0.85 Cr in 2025 to ₹1,467.5 Cr in 2030, driven by PowerPedal adoption in India and Europe.**")

    # Initialize Session State
    if 'financials' not in st.session_state:
        st.session_state.financials = {
            'scenario': 'Base Case',
            'asp_powerpedal': 10000,
            'cogs_powerpedal': 6000,
            'opex_percent': 0.15,
            'fixed_costs': 2.4e7
        }

    # Simplified CSS for Key Elements
    st.markdown(
        """
        <style>
        .financial-tab {
            font-family: Arial, sans-serif;
            color: #FFFFFF;
        }
        .data-table-container {
            background: #D6DAC8;
            border: 2px solid #9CAFAA;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
        }
        .data-table-container h5 {
            color: #000000;
        }
        .data-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            border-radius: 10px;
            overflow: hidden;
            color: #000000;
        }
        .data-table th {
            background: #EE791F;
            color: #000000;
            font-weight: 600;
            padding: 10px;
            text-align: center;
            border-bottom: 1px solid #9CAFAA;
            border-right: 1px solid #9CAFAA;
        }
        .data-table td {
            color: #000000;
            padding: 10px;
            text-align: center;
            border-bottom: 1px solid #9CAFAA;
            border-right: 1px solid #9CAFAA;
        }
        .data-table tr:nth-child(even) {
            background: #F5F5F5;
        }
        .data-table tr:nth-child(odd) {
            background: #FFFFFF;
        }
        .data-table tr:hover {
            background: #FFD6BA;
        }
        .data-table td.highlight {
            background: #FFF9BD;
            font-weight: 600;
        }
        .scenario-highlight {
            background: #9CAFAA;
            border: 2px solid #9CAFAA;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 20px;
            text-align: center;
            font-weight: 600;
            color: #000000;
        }
        .headline-container {
            background: #FFF9BD;
            border: 2px solid #9CAFAA;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            min-height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .headline-container h4 {
            color: #000000;
            font-size: 14px;
            margin: 0 0 8px;
        }
        .headline-container p {
            color: #000000;
            font-size: 18px;
            font-weight: 600;
            margin: 0;
        }
        .highlights-section {
            background: #D6DAC8;
            border: 2px solid #9CAFAA;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            color: #000000;
        }
        .highlights-section p {
            color: #000000;
            font-size: 16px;
            font-weight: 600;
            margin: 0;
        }
        .highlights-section ul li {
            color: #000000;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="financial-tab">', unsafe_allow_html=True)

    # Image in Centered Column
    _, col_img, _ = st.columns([1, 4, 1])
    with col_img:
        image_url = "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/financial.png"
        try:
            st.image(image_url, caption="PowerPedal Growth Vision", use_container_width=True)
            # This button opens the image in a new tab for native zoom/pan
            st.markdown(
                f'<a href="{image_url}" target="_blank" style="text-decoration: none;">'
                f'<button style="background-color: #2E2E2E; color: #FFFFFF; border: none; padding: 10px 20px; border-radius: 5px;">'
                f'View Full-Size Image</button></a>',
                unsafe_allow_html=True
            )
        except Exception:
            st.warning("Image file not found at: " + image_url)
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
    fixed_cogs_2025 = 8500
    asp_powerpedal = 10000
    cogs_powerpedal = 6000
    opex_percent = 0.15
    fixed_costs = 2.4e7

    # Financial Calculations for all scenarios
    def calculate_scenario(scenario_factor):
        unit_sales = [int(u * scenario_factor) for u in unit_sales_base]
        cogs_decline_rate = 0.02
        base_tax_rate = 0.25
        tax_exemption_years = [2025, 2026, 2027]
        cogs_powerpedal_list = [fixed_cogs_2025] + [cogs_powerpedal * (1 - cogs_decline_rate) ** i for i in range(1, len(years))]
        
        if scenario_factor == 1.0:
            revenue = revenue_base
        else:
            revenue = [u * asp_powerpedal for u in unit_sales]
        
        gross_profit = [r - (u * c) for r, u, c in zip(revenue, unit_sales, cogs_powerpedal_list)]
        
        opex = [0.35e7, 2.3e7, 15e7]
        for i in range(3, len(years)):
            opex.append(revenue[i] * opex_percent + fixed_costs)
        
        ebitda = [gp - o for gp, o in zip(gross_profit, opex)]
        tax_rate = [0 if year in tax_exemption_years else base_tax_rate for year in years]
        net_income = [e * (1 - tr) for e, tr in zip(ebitda, tax_rate)]
        
        return unit_sales, revenue, cogs_powerpedal_list, gross_profit, opex, ebitda, net_income

    unit_sales_cons, revenue_cons, cogs_cons, gross_profit_cons, opex_cons, ebitda_cons, net_income_cons = calculate_scenario(0.8)
    unit_sales_base_case, revenue_base_case, cogs_base_case, gross_profit_base_case, opex_base_case, ebitda_base_case, net_income_base_case = calculate_scenario(1.0)
    unit_sales_agg, revenue_agg, cogs_agg, gross_profit_agg, opex_agg, ebitda_agg, net_income_agg = calculate_scenario(1.2)

    scenario_data = {
        'Conservative': {
            'unit_sales': unit_sales_cons, 'revenue': revenue_cons, 'cogs': cogs_cons,
            'gross_profit': gross_profit_cons, 'opex': opex_cons,
            'ebitda': ebitda_cons, 'net_income': net_income_cons
        },
        'Base Case': {
            'unit_sales': unit_sales_base_case, 'revenue': revenue_base_case, 'cogs': cogs_base_case,
            'gross_profit': gross_profit_base_case, 'opex': opex_base_case,
            'ebitda': ebitda_base_case, 'net_income': net_income_base_case
        },
        'Aggressive': {
            'unit_sales': unit_sales_agg, 'revenue': revenue_agg, 'cogs': cogs_agg,
            'gross_profit': gross_profit_agg, 'opex': opex_agg,
            'ebitda': ebitda_agg, 'net_income': net_income_agg
        }
    }

    st.subheader("Choose a Scenario")
    col_sc1, col_sc2, col_sc3 = st.columns(3)
    
    with col_sc1:
        if st.button("Conservative", key="conservative_btn", use_container_width=True):
            st.session_state.financials['scenario'] = 'Conservative'
            st.rerun()
    with col_sc2:
        if st.button("Base Case", key="base_case_btn", use_container_width=True):
            st.session_state.financials['scenario'] = 'Base Case'
            st.rerun()
    with col_sc3:
        if st.button("Aggressive", key="aggressive_btn", use_container_width=True):
            st.session_state.financials['scenario'] = 'Aggressive'
            st.rerun()

    selected_scenario = st.session_state.financials['scenario']
    data = scenario_data[selected_scenario]
    unit_sales, revenue, gross_profit, opex, ebitda, net_income, cogs_powerpedal_list = (
        data['unit_sales'], data['revenue'], data['gross_profit'],
        data['opex'], data['ebitda'], data['net_income'], data['cogs']
    )

    with st.container():
        st.markdown(
            f'<div class="scenario-highlight">'
            f'Active Scenario: <strong>{selected_scenario}</strong>'
            f'</div>',
            unsafe_allow_html=True
        )
        col1, col2, col3, col4 = st.columns(4)
        
        metrics = [
            {"title": "Total Revenue (2025–2030)", "value": sum(revenue) / 1e7, "color": "#FFF9BD"},
            {"title": "Total Gross Profit (2025–2030)", "value": sum(gross_profit) / 1e7, "color": "#FFD6BA"},
            {"title": "Total Net Profit (2025–2030)", "value": sum(net_income) / 1e7, "color": "#D6DAC8"},
            {"title": "Break-even Year", "value": "2026", "color": "#9CAFAA", "is_year": True}
        ]

        for col, metric in zip([col1, col2, col3, col4], metrics):
            with col:
                value_to_display = metric["value"] if metric.get("is_year") else f"₹{metric['value']:.2f} Cr"
                st.markdown(
                    f'<div class="headline-container" style="background: {metric["color"]};">'
                    f'<h4 style="color: #000000; margin: 0 0 8px;">{metric["title"]}</h4>'
                    f'<p style="color: #000000; font-size: 18px; font-weight: 600; margin: 0;">{value_to_display}</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )

    chart_data = pd.DataFrame({
        'Year': years,
        'Revenue': [r / 1e7 for r in revenue],
        'Gross Profit': [gp / 1e7 for gp in gross_profit],
        'Net Income': [ni / 1e7 for ni in net_income]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=chart_data['Year'], y=chart_data['Revenue'], mode='lines+markers', name='Revenue', line=dict(color='#EE791F', width=3)))
    fig.add_trace(go.Scatter(x=chart_data['Year'], y=chart_data['Gross Profit'], mode='lines+markers', name='Gross Profit', line=dict(color='#FFD6BA', width=3)))
    fig.add_trace(go.Scatter(x=chart_data['Year'], y=chart_data['Net Income'], mode='lines+markers', name='Net Income', line=dict(color='#D6DAC8', width=3)))

    fig.update_layout(
        title_text='Financial Projections (₹ Cr) for ' + selected_scenario,
        title_font_color='white',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickvals=years, showgrid=False, color='white', title_font_color='white', title='Year'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.2)', color='white', title_font_color='white', title='₹ Cr'),
        legend=dict(font=dict(color='white')),
        hovermode='x unified',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})

    st.markdown('---')
    st.subheader(f"Detailed Financial Table for {selected_scenario}")
    st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
    try:
        df_table = pd.DataFrame({
            'Year': years,
            'Units Sold': [f'{u:,}' for u in unit_sales],
            'Revenue (₹ Cr)': [f'₹{round(r / 1e7, 2):,.2f}' for r in revenue],
            'COGS (₹ Cr)': [f'₹{round(c * u / 1e7, 2):,.2f}' for u, c in zip(unit_sales, cogs_powerpedal_list)],
            'Gross Profit (₹ Cr)': [f'₹{round(gp / 1e7, 2):,.2f}' for gp in gross_profit],
            'Opex (₹ Cr)': [f'₹{round(o / 1e7, 2):,.2f}' for o in opex],
            'EBITDA (₹ Cr)': [f'₹{round(e / 1e7, 2):,.2f}' for e in ebitda],
            'Net Income (₹ Cr)': [f'<span class="highlight">₹{round(ni / 1e7, 2):,.2f}</span>' for ni in net_income],
            'EBITDA Margin (%)': [f'<span class="highlight">{round((e / r) * 100, 1)}%</span>' if r > 0 else '0.0%'
                                 for e, r in zip(ebitda, revenue)]
        })
        headers = df_table.columns.tolist()
        html = '<table class="data-table">'
        html += '<tr>' + ''.join(f'<th>{h}</th>' for h in headers) + '</tr>'
        for idx, row in df_table.iterrows():
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


    # Key Investor Highlights
    st.markdown('---')
    st.subheader("Key Investor Highlights")
    st.markdown(
        """
        <div class="highlights-section">
            <ul style="list-style-type: none; padding-left: 0;">
                <li style="margin-bottom: 5px; color: #000000;">💡 <b>Capital Efficiency:</b> Foundation built on grant money with minimal dilution—R&D, patents, and pilots were achieved capital-efficiently.</li>
                <li style="margin-bottom: 5px; color: #000000;">🤝 <b>Strategic Partnership:</b> Equity was given only to a strategic partner, securing early distribution and go-to-market strength.</li>
                <li style="margin-bottom: 5px; color: #000000;">📈 <b>Early Profitability:</b> Profitability is achieved at just 10K units (2026), making the company EBITDA positive far earlier than typical hardware startups.</li>
                <li style="margin-bottom: 5px; color: #000000;">🚀 <b>Scalable Growth:</b> A 10x growth is projected in 2027, driven by strategic European expansion and OEM adoption.</li>
                <li style="margin-bottom: 5px; color: #000000;">🏭 <b>Lean Operations:</b> The capital-light scaling model uses contract manufacturing to keep costs lean, with margins expanding towards ~30% by 2030.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

import streamlit as st
import base64
import os
from pathlib import Path

# --- Direct URL for the video ---
VIDEO_URL = "https://www.dropbox.com/scl/fi/nxb6h4r0d4vntdd9zp87a/design_clinic.mp4?rlkey=lcy831kcxq51jwh4hyfz3w43t&raw=1"

# Assuming 'tabs' is a list created with st.tabs() earlier in your script.
# Example: tabs = st.tabs(["Tab 1", "Tab 2", "...", "Milestones"])
with tabs[7]:
    # --- Data for Milestones ---
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
            "media": {
                "type": "embedded_video",
                "url": VIDEO_URL
            }
        },
        {
            "name": "Design Clinic Scheme",
            "type": "Funding",
            "value": "₹15 Lakh",
            "icon": "🏆",
            "details": "Received a grant of ₹15 Lakh from the Indian Institute of Science's Design Clinic Scheme.",
            "media": None
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
            "media": ["https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/functional_proto1.jpg", "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/functional_proto.jpg"]
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

    # --- Page Layout ---
    st.title("📍 Our Journey of Traction & Milestones")
    st.markdown("---")

    # Use HTML to center the timeline image.
    st.markdown("""
        <div style="text-align: center;">
            <img src="https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/timeline.png" style="width: 600px;">
        </div>
    """, unsafe_allow_html=True)
    
    # Introduction Section
    st.markdown(
        """
        <div style="background-color: #1B3C53; border: 2px solid #78C841; border-radius: 12px; padding: 20px; text-align: center; margin: 20px auto; max-width: 800px;">
            <h3 style="color: #78C841;">The Spark That Started It All</h3>
            <p style="color: #A8F1FF; font-size: 16px; line-height: 1.6;">Our journey began in a college lab, where we built an award-winning electric skateboard, igniting our passion for redefining mobility. Driven by curiosity, we explored urban transportation—bicycles emerged as the perfect fusion of efficiency, practicality, and sustainability.</p>
            <p style="color: #A8F1FF; font-size: 16px; line-height: 1.6;">We fearlessly experimented, creating a powered wheelchair attachment for accessibility, a Hybrid Energy Storage System (HESS), road presence lighting, and custom drivetrains. Each project honed our skills, but our focus crystallized on advanced drive technology. Today, Switch Mobility is a B2B leader, delivering responsive, efficient, and cost-effective eBike drive systems to OEMs worldwide, transforming urban mobility.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.subheader("Our Journey, Step by Step")
    st.write("Explore our product breakthroughs and funding achievements below.")

    # --- Product Milestones Container ---
    st.header("Product Milestones")
    
    # This loop creates a new, separate container for each product milestone
    for milestone in milestones_data:
        if milestone['type'] == 'Product':
            product_html = f"""
            <style>
                .product-milestone-container {{
                    background-color: #1A3636; 
                    border: 2px solid #78C841;
                    border-radius: 12px;
                    padding: 20px;
                    margin: 15px 0;
                }}
            </style>
            """
            title = f"{milestone['icon']} {milestone['name']}"
            
            # --- Build media HTML string
            media_html = ""
            if milestone['media']:
                media = milestone['media']
                if isinstance(media, dict) and media.get("type") == "embedded_video":
                    media_html = f"""<div style="text-align: center;">
                                       <video width="250" controls style="border-radius: 8px; border: 1px solid #78C841;">
                                           <source src="{media.get('url')}" type="video/mp4">
                                           Your browser does not support the video tag.
                                       </video>
                                   </div>"""
                elif isinstance(media, str):
                    media_html = f"""<div style="text-align: center;">
                                       <img src="{media}" width="250" style="border-radius: 8px; border: 1px solid #78C841;">
                                   </div>"""
                elif isinstance(media, list):
                    images_html = "".join([f'<img src="{url}" width="250" style="border-radius: 8px; border: 1px solid #78C841; margin: 5px;">' for url in media])
                    media_html = f"""<div style="display: flex; justify-content: center; flex-wrap: wrap;">{images_html}</div>"""
            
            product_html += f"""
            <div class="product-milestone-container">
                <h4 style="font-size: 1.2em; font-weight: 600; color: #A8F1FF; padding: 0; margin: 0 0 8px 0;">{title}</h4>
                <p style="font-size: 1em; color: #FFF5F2; margin: 0; padding: 0;">{milestone['details']}</p>
                {media_html}
            </div>
            """
            st.markdown(product_html, unsafe_allow_html=True)

    # --- Funding Milestones Container ---
    st.header("Funding Milestones")
    
    # This loop creates a new, separate container for each funding milestone
    for milestone in milestones_data:
        if milestone['type'] == 'Funding':
            funding_html = f"""
            <style>
                .funding-milestone-container {{
                    background-color: #40534C; 
                    border: 2px solid #78C841;
                    border-radius: 12px;
                    padding: 20px;
                    margin: 15px 0;
                }}
            </style>
            """
            title = f"{milestone['icon']} {milestone['name']}"
            if milestone['value'] != 'N/A':
                title += f" — {milestone['value']}"
            
            funding_html += f"""
            <div class="funding-milestone-container">
                <h4 style="font-size: 1.2em; font-weight: 600; color: #A8F1FF; padding: 0; margin: 0 0 8px 0;">{title}</h4>
                <p style="font-size: 1em; color: #FFF5F2; margin: 0; padding: 0;">{milestone['details']}</p>
            </div>
            """
            st.markdown(funding_html, unsafe_allow_html=True)

with tabs[8]:
    st.header("🧑‍🤝‍🧑 Team & Advisors", anchor=False)
    st.caption("Meet the Visionaries Powering Our Mission")

    # --- CSS (Updated to style <details> elements and maintain original styling) ---
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
            background: linear-gradient(135deg, #1B3C53, #2e2e2e);
            border: 2px solid #78C841;
            border-radius: 12px;
            padding: 15px !important;
            margin: 15px;
            max-width: 250px !important;
            width: 100%;
            box-sizing: border-box;
            transition: transform 0.4s ease, box-shadow 0.4s ease, border 0.4s ease;
            text-align: center;
            text-decoration: none;
        }}
        .team-advisors-tab .profile-container:hover {{
            transform: scale(1.07);
            background: linear-gradient(135deg, #2e2e2e, #1B3C53);
            border: 3px solid #A8F1FF;
            box-shadow: 0 0 15px rgba(120, 200, 65, 0.6);
        }}
        .team-advisors-tab .profile-image.core-team-image {{
            width: 100px !important;
            height: 100px !important;
        }}
        .team-advisors-tab .profile-image {{
            width: 120px !important;
            height: 120px !important;
            border-radius: 50%;
            object-fit: cover;
            border: 2px solid #A8F1FF;
            padding: 2px;
            background: #FFFFFF;
            display: block;
            margin: 0 auto;
        }}
        .team-advisors-tab .profile-name {{
            color: #78C841;
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
            color: #A8F1FF;
            font-size: 14px;
            line-height: 1.5;
            margin: 5px 0;
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
        
        /* Styling for <details> elements to match original expanders */
        .team-advisors-tab .details-card {{
            background: linear-gradient(135deg, #1B3C53, #2e2e2e);
            border: 2px solid #78C841;
            border-radius: 12px;
            padding: 15px;
            color: #A8F1FF;
            margin: 10px 0;
            max-width: 250px;
        }}
        .team-advisors-tab .details-card[open] {{
            background: linear-gradient(135deg, #2e2e2e, #1B3C53);
            border: 3px solid #A8F1FF !important;
            box-shadow: 0 0 15px rgba(120, 200, 65, 0.6);
        }}
        .team-advisors-tab .details-card summary {{
            font-size: 18px;
            font-weight: 600;
            color: #78C841;
            cursor: pointer;
            outline: none;
            list-style: none; /* Remove default marker */
        }}
        .team-advisors-tab .details-card summary::-webkit-details-marker {{
            display: none; /* Hide default arrow in WebKit browsers */
        }}
        .team-advisors-tab .details-card p {{
            font-size: 14px;
            line-height: 1.5;
            margin: 5px 0;
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
        {
            "name": "Vineeth Muthanna",
            "role": "Technical Head",
            "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/Vineeth.png",
            "linkedin": "https://linkedin.com/in/vineethmuthanna",
            "bio": "Vineeth leads Product Development and Engineering at Switch. With deep expertise in hardware and prototyping, he ensures PowerPedal’s technology is reliable, scalable, and globally competitive. His focus is on translating concepts into robust systems that meet real-world needs."
        },
        {
            "name": "Ranjit B C",
            "role": "Business & Operations",
            "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/Ranjit.jpeg",
            "linkedin": "https://linkedin.com/in/ranjit-b-c-a3981215a",
            "bio": "Ranjit drives Business Operations and Strategic Planning at Switch. He develops business plans, digital platforms, and growth strategies, while managing the operational backbone including supply chain and execution. By blending creative thinking with structured problem-solving, he ensures Switch remains agile while powering the success of PowerPedal."
        },
        {
            "name": "Vinay Sharma",
            "role": "Marketing & Finance",
            "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/vinay.png",
            "linkedin": "https://linkedin.com/in/vinay-sharma-0563a816a",
            "bio": "Vinay oversees Marketing and Finance at Switch, combining storytelling with financial discipline. He builds market strategies that amplify PowerPedal’s reach while ensuring long-term sustainability through sound financial planning."
        },
        {
            "name": "Shravan Aiyappa",
            "role": "Production Head",
            "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/Shravan.png",
            "linkedin": "https://linkedin.com/in/shravan-aiyappa-kadiamada-b8958ab9",
            "bio": "Shravan manages Production and Quality Control at Switch. He leads manufacturing processes, tooling, and testing to ensure PowerPedal products meet international standards. His detail-oriented approach guarantees consistency and reliability at scale."
        },
        {
            "name": "Rohit Kuttappa",
            "role": "Strategy & GTM",
            "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/Rohit.jpg",
            "linkedin": "https://linkedin.com/in/rohit-kuttappa-a6256439",
            "bio": "Rohit heads Go-To-Market Strategy and Partnerships at Switch. He shapes brand positioning, fundraising narratives, and market-entry plans, ensuring that PowerPedal is well-positioned in both domestic and global markets."
        },
        {
            "name": "Abbishek Bharadwaj",
            "role": "Sales & OEM Partnerships",
            "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/Abbishek.jpg",
            "linkedin": "https://linkedin.com/in/abbishek-v-bharadwaj-21171911",
            "bio": "Abbishek drives Sales, OEM Partnerships, and After-Sales Ecosystems at Switch. He focuses on expanding distribution networks and building strong customer relationships, enabling PowerPedal to achieve sustained market growth."
        }
    ]
    for i in range(0, len(team_members), 3):
        cols = st.columns(3)
        for j, member in enumerate(team_members[i:i+3]):
            with cols[j]:
                st.markdown(f"""
                    <a href="{member['linkedin']}" target="_blank" style="text-decoration: none;">
                        <div class="team-advisors-tab profile-container">
                            <img src="{load_image(member['image'])}" class="profile-image core-team-image">
                            <div class="profile-name">{member['name']}</div>
                            <div class="profile-role">{member['role']}</div>
                        </div>
                    </a>
                    <details class="team-advisors-tab details-card">
                        <summary>About</summary>
                        <p class="profile-details">{member['bio']}</p>
                    </details>
                """, unsafe_allow_html=True)

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
        {
            "name": "Supria Dhanda",
            "role": "CEO, WYSER",
            "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/Supria.jpeg",
            "linkedin": "https://linkedin.com/in/supriadhanda",
            "bio": "Supria contributes expertise in strategy, governance, and corporate leadership. With experience spanning Western Digital, ABS India, and 50+ startup investments, she guides Switch in scaling PowerPedal with a sharp focus on innovation and sustainable growth."
        },
        {
            "name": "Satyakam Mohanty",
            "role": "Entrepreneur",
            "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/Satyakam.png",
            "linkedin": "https://linkedin.com/in/satymohanty",
            "bio": "Satyakam brings over 23 years of experience in data, AI, and startup innovation. As founder of Lymbyc and now part of WYSER, he advises Switch on disruptive technologies and zero-to-one journeys, helping PowerPedal carve its space in the mobility ecosystem."
        },
        {
            "name": "Krishna Prasad",
            "role": "Tech Manager, CeNSE IISc",
            "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/krishna.png",
            "linkedin": "https://linkedin.com/in/placeholder",
            "bio": "Krishna advises Switch on sensor integration and advanced technology adoption. As a Technology Manager at CeNSE, IISc, his expertise ensures PowerPedal stays at the forefront of innovation and practical engineering applications."
        },
        {
            "name": "Dr. Vijay Mishra",
            "role": "Ex-CTO, CeNSE IISc",
            "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/Vijay.jpg",
            "linkedin": "https://linkedin.com/in/placeholder",
            "bio": "Dr. Mishra provides guidance on technology translation and scalability. With decades of experience as CTO at CeNSE, IISc, he helps Switch move advanced research into market-ready, reliable products like PowerPedal."
        },
        {
            "name": "Rohan Ganapathy",
            "role": "CEO, Bellatrix Aerospace",
            "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/rohan.png",
            "linkedin": "https://linkedin.com/in/rohanmganapathy",
            "bio": "Rohan brings deep-tech entrepreneurship insights to Switch. As founder of Bellatrix Aerospace, his experience in scaling engineering ventures supports PowerPedal’s journey toward becoming a globally competitive mobility solution."
        },
        {
            "name": "Sandeep Bahl",
            "role": "Vice President, NASSCOM",
            "image": "https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/images/Sandeep.png",
            "linkedin": "https://linkedin.com/in/sandeepbahl1",
            "bio": "Sandeep strengthens Switch with ecosystem connections and strategic guidance. As VP at NASSCOM, he helps position PowerPedal within the larger technology and startup landscape, enabling access to critical networks and opportunities."
        }
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
                    <details class="team-advisors-tab details-card">
                        <summary>About</summary>
                        <p class="profile-details">{advisor['bio']}</p>
                    </details>
                """, unsafe_allow_html=True)
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
    import numpy as np

    # --- Header ---
    st.header("💰 Funding Ask & Use", anchor=False)
    st.caption("Our Strategic Roadmap for Investment and Growth")

    # --- Data Preparation ---
    year1_data = [
        {"milestone": "Functional Version 1 Development", "timeline": "Month 1-2", "cost_lakh": 26.2, "category": "R&D", "year": "Year 1"},
        {"milestone": "System Integration & Testing", "timeline": "Month 3-4", "cost_lakh": 18.5, "category": "R&D", "year": "Year 1"},
        {"milestone": "Manufacturing Preparation & Supply Chain Setup (100 units)", "timeline": "Month 5-6", "cost_lakh": 17.72, "category": "Manufacturing", "year": "Year 1"},
        {"milestone": "Production Scaling", "timeline": "Month 7-8", "cost_lakh": 22.0, "category": "Manufacturing", "year": "Year 1"},
        {"milestone": "Business Expansion & OEM Partnerships", "timeline": "Month 9-10", "cost_lakh": 18.0, "category": "Business Expansion", "year": "Year 1"},
        {"milestone": "Entry into Europe & US Markets", "timeline": "Month 11-12", "cost_lakh": 17.58, "category": "Business Expansion", "year": "Year 1"},
    ]

    year2_data = [
        {"milestone": "Mass Manufacturing (10,000 units)", "timeline": "Month 13-15", "cost_lakh": 80.0, "category": "Manufacturing", "year": "Year 2"},
        {"milestone": "Global Certifications & Compliance", "timeline": "Month 16-17", "cost_lakh": 40.0, "category": "Compliance", "year": "Year 2"},
        {"milestone": "International OEM Partnerships", "timeline": "Month 18-19", "cost_lakh": 60.0, "category": "Business Expansion", "year": "Year 2"},
        {"milestone": "Manufacturing Facility Expansion", "timeline": "Month 20-21", "cost_lakh": 50.0, "category": "Manufacturing", "year": "Year 2"},
        {"milestone": "Final Scaling & Marketing Push", "timeline": "Month 22-24", "cost_lakh": 50.0, "category": "Business Expansion", "year": "Year 2"},
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
        .funding-tab .st-emotion-cache-1c7y3v2 { /* stTabs container */
            background-color: #1E1E1E;
            border-radius: 10px;
            padding: 10px;
        }
        .funding-tab .st-emotion-cache-1r6slb0 { /* Expander header color */
            color: #A8F1FF !important;
        }
        .funding-tab .st-emotion-cache-13k9f44, .st-emotion-cache-s1h49r { /* Expander content styling */
            background-color: #2e2e2e;
            padding: 1rem;
            border-radius: 8px;
            margin-top: 10px;
        }
        .funding-tab .st-emotion-cache-16j0542 { /* Expander arrow color */
            color: #A8F1FF;
        }
        .milestone-title {
            font-size: 18px;
            font-weight: 600;
            color: #FFFFFF;
            margin: 0;
        }
        .milestone-cost {
            font-size: 20px;
            font-weight: 700;
            color: #00FF7F;
            margin: 0;
        }
        .milestone-timeline {
            font-size: 14px;
            color: #A8F1FF;
            opacity: 0.8;
        }
        .milestone-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
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

    # --- 2. Visual Breakdown: Donut Chart ---
    st.subheader("Visual Use of Proceeds")

    # Aggregate data for the donut chart
    category_costs = df.groupby('category')['cost_lakh'].sum().reset_index()

    # Create the donut chart
    fig_donut = go.Figure(data=[go.Pie(
        labels=category_costs['category'],
        values=category_costs['cost_lakh'],
        hole=.6,
        hoverinfo='label+percent',
        textinfo='label+percent',
        texttemplate='%{label}<br>₹%{value:.2f}L',
        marker=dict(colors=['#00FF7F', '#A8F1FF', '#FFA500', '#1E90FF']),
        pull=[0.02, 0.02, 0.02, 0.02]
    )])

    # Add the total value in the center of the donut chart
    fig_donut.add_annotation(
        text="₹4 Cr",
        x=0.5, y=0.5,
        font_size=24,
        font_color="#FFFFFF",
        font_weight="bold",
        showarrow=False
    )

    fig_donut.update_layout(
        showlegend=False,
        height=400,
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#FFFFFF")
    )
    st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("---")

    # --- 3. Interactive Timeline with Expanders ---
    st.subheader("Interactive Milestone Timeline")

    year1_total = sum(d['cost_lakh'] for d in year1_data)
    year2_total = sum(d['cost_lakh'] for d in year2_data)
    
    # Define a consistent color map for categories
    color_map = {
        "R&D": '#00FF7F',
        "Manufacturing": '#FFA500',
        "Business Expansion": '#1E90FF',
        "Compliance": '#A8F1FF'
    }

    all_milestones = [
        ("Year 1: Building the Foundation (Total: ₹ 1.2 Cr)", year1_data, year1_total),
        ("Year 2: Scaling for Growth (Total: ₹ 2.8 Cr)", year2_data, year2_total)
    ]

    for title, data, total in all_milestones:
        st.markdown(f"### {title}")
        for item in data:
            with st.expander(f"🗓️ {item['timeline']}: {item['milestone']} - ₹ {item['cost_lakh']:.2f} L"):
                st.write(f"**Category:** {item['category']}")
                st.write(f"**Cost as % of {title.split(':')[0]} Budget:** {item['cost_lakh'] / total * 100:.2f}%")
                
                fig_bar = go.Figure(go.Bar(
                    x=[item['cost_lakh']],
                    y=[''],
                    orientation='h',
                    marker_color=color_map[item['category']],
                    showlegend=False,
                    hoverinfo='none',
                    width=0.2
                ))
                fig_bar.update_layout(
                    xaxis_title="Cost in Lakhs (₹)",
                    xaxis_range=[0, max(d['cost_lakh'] for d in data)],
                    height=100,
                    margin=dict(t=20, b=20, l=0, r=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="#FFFFFF")
                )
                st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown("---")

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
    audio_path = Path(r"https://raw.githubusercontent.com/ranjit2602/powerpedal-pitch-dashboard/main/assets/audio/powerpedal_audio_pitch.mp3")
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
