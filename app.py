import streamlit as st
import pymongo
import pandas as pd
import plotly.express as px
from youtube_functions import channel_details
import mysql.connector

def youtube_chart_theme(fig):

    fig.update_layout(
        paper_bgcolor="#0F0F0F",
        plot_bgcolor="#0F0F0F",
        font=dict(color="#FFFFFF"),

        xaxis=dict(
            color="#FFFFFF",
            gridcolor="#303030",
            zerolinecolor="#444444"
        ),

        yaxis=dict(
            color="#FFFFFF",
            gridcolor="#303030",
            zerolinecolor="#444444"
        ),

        legend=dict(
            font=dict(color="#FFFFFF")
        )
    )

    return fig

st.markdown("""
<style>

    /* =================================================
       MAIN APPLICATION
       ================================================= */

    .stApp {
        background-color: white;
        color: black;
    }


    /* =================================================
       SIDEBAR
       ================================================= */

    section[data-testid="stSidebar"] {
        background-color: red;
    }


    section[data-testid="stSidebar"] * {
        color: #FFFFFF;
    }


    section[data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.25);
    }


    /* =================================================
   SIDEBAR COLLAPSE / EXPAND BUTTON
   ================================================= */

/* Current Streamlit sidebar button */
[data-testid="stSidebarCollapseButton"] button {
    color: #FFFFFF !important;
    background-color: transparent !important;
}

[data-testid="stSidebarCollapseButton"] button svg {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
}


/* Collapsed sidebar button */
[data-testid="stSidebarCollapsedControl"] button {
    color: #FFFFFF !important;
    background-color: transparent !important;
}

[data-testid="stSidebarCollapsedControl"] button svg {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
}


/* Older Streamlit versions */
button[data-testid="baseButton-header"] {
    color: #FFFFFF !important;
}

button[data-testid="baseButton-header"] svg {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
}


/* Header button used by newer Streamlit versions */
button[data-testid="stBaseButton-headerNoPadding"] {
    color: #FFFFFF !important;
}

button[data-testid="stBaseButton-headerNoPadding"] svg {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
}

    /* =================================================
       BUTTONS
       ================================================= */

    .stButton > button {
        background-color: #FF0000;
        color: #FFFFFF;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }


    .stButton > button:hover {
        background-color: #CC0000;
        color: #FFFFFF;
    }


    /* =================================================
       METRIC CARDS
       ================================================= */

    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #303030;
        padding: 15px;
        border-radius: 10px;
    }


    div[data-testid="stMetricLabel"] {
        color: black;
    }


    div[data-testid="stMetricValue"] {
        color: black;
    }


    /* =================================================
       SELECT BOX
       ================================================= */

    div[data-baseweb="select"] > div {
        background-color: #212121 !important;
        color: #FFFFFF !important;
        border-color: #444444 !important;
    }


    div[data-baseweb="select"] span {
        color: #FFFFFF !important;
    }


    div[data-baseweb="select"] svg {
        fill: #FFFFFF !important;
    }


    ul[role="listbox"] {
        background-color: #212121 !important;
    }


    li[role="option"] {
        background-color: #212121 !important;
        color: #FFFFFF !important;
    }


    li[role="option"]:hover {
        background-color: #303030 !important;
        color: #FFFFFF !important;
    }


    /* =================================================
       TEXT INPUT / SEARCH BOX
       ================================================= */

    div[data-baseweb="input"] {
        background-color: #212121 !important;
        border-color: #444444 !important;
    }


    div[data-baseweb="input"] input {
        background-color: #212121 !important;
        color: #FFFFFF !important;
        caret-color: #FFFFFF;
    }


    div[data-baseweb="input"] input::placeholder {
        color: #AAAAAA !important;
    }


    /* =================================================
       DATAFRAME
       ================================================= */

    div[data-testid="stDataFrame"] {
        border-radius: 10px;
    }


    /* =================================================
       LINKS
       ================================================= */

    a {
        color: #FF4B4B;
    }


    a:hover {
        color: #FF0000;
    }


    /* =================================================
       STREAMLIT TOP HEADER
       ================================================= */

    header[data-testid="stHeader"] {
        background-color: #0F0F0F !important;
        border-bottom: none !important;
    }
    /* =================================================
   SIDEBAR COLLAPSE BUTTON - MAKE ICON WHITE
   ================================================= */

/* Header buttons */
header button {
    color: #FFFFFF !important;
    background-color: transparent !important;
}


/* Everything inside the header button */
header button svg,
header button span,
header button div {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
}


/* Force dark/black icon to become white */
header button svg {
    filter: invert(1) !important;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# MySQL Connection
# -----------------------------

def get_mysql_connection():

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="2005",
        database="youtube_data",
        port="3306"
    )

    return mydb


# =========================================================
# STREAMLIT PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="YouTube Data Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# MONGODB CONNECTION
# =========================================================

client = pymongo.MongoClient(
    "mongodb://localhost:27017"
)

db = client["youtube_data"]

collection = db["channel_details"]


# =========================================================
# NUMBER FORMATTING
# =========================================================

def format_number(number):

    try:
        number = float(number)

    except (TypeError, ValueError):
        return "0"

    if number >= 1_000_000_000:
        return f"{number / 1_000_000_000:.2f}B"

    elif number >= 1_000_000:
        return f"{number / 1_000_000:.2f}M"

    elif number >= 1_000:
        return f"{number / 1_000:.2f}K"

    else:
        return f"{number:,.0f}"


# =========================================================
# AXIS NUMBER FORMATTING
# =========================================================

def format_axis_number(number):

    try:
        number = float(number)

    except (TypeError, ValueError):
        return "0"

    if number >= 1_000_000_000:
        return f"{number / 1_000_000_000:.1f}B"

    elif number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"

    elif number >= 1_000:
        return f"{number / 1_000:.0f}K"

    else:
        return f"{number:.0f}"


# =========================================================
# DASHBOARD DATA
# =========================================================

def get_dashboard_data():

    channels = []
    videos = []
    comments = []

    # Channel information
    for data in collection.find(
        {},
        {"_id": 0, "channel_information": 1}
    ):

        if "channel_information" in data:
            channels.append(
                data["channel_information"]
            )

    # Video information
    for data in collection.find(
        {},
        {"_id": 0, "video_information": 1}
    ):

        if "video_information" in data:
            videos.extend(
                data["video_information"]
            )

    # Comment information
    for data in collection.find(
        {},
        {"_id": 0, "comment_information": 1}
    ):

        if "comment_information" in data:
            comments.extend(
                data["comment_information"]
            )

    # Metrics
    total_channels = len(channels)

    total_videos = len(videos)

    total_comments = len(comments)

    total_views = sum(
        int(video.get("total_views", 0) or 0)
        for video in videos
    )

    return (
        total_channels,
        total_videos,
        total_views,
        total_comments
    )


# =========================================================
# CHANNEL DATAFRAME
# =========================================================

def get_channel_dataframe():

    channel_list = []

    for data in collection.find(
        {},
        {"_id": 0, "channel_information": 1}
    ):

        if "channel_information" in data:

            channel_list.append(
                data["channel_information"]
            )

    df = pd.DataFrame(channel_list)

    if not df.empty:

        df["subscribers"] = pd.to_numeric(
            df["subscribers"],
            errors="coerce"
        ).fillna(0)

        df["views"] = pd.to_numeric(
            df["views"],
            errors="coerce"
        ).fillna(0)

        df["total_videos"] = pd.to_numeric(
            df["total_videos"],
            errors="coerce"
        ).fillna(0)

    return df


# =========================================================
# VIDEO DATAFRAME
# =========================================================

def get_video_dataframe():

    video_list = []

    for data in collection.find(
        {},
        {"_id": 0, "video_information": 1}
    ):

        if "video_information" in data:

            video_list.extend(
                data["video_information"]
            )

    df = pd.DataFrame(video_list)

    if not df.empty:

        df["total_views"] = pd.to_numeric(
            df["total_views"],
            errors="coerce"
        ).fillna(0)

        df["total_likes"] = pd.to_numeric(
            df["total_likes"],
            errors="coerce"
        ).fillna(0)

        df["total_comments"] = pd.to_numeric(
            df["total_comments"],
            errors="coerce"
        ).fillna(0)

    return df


# =========================================================
# GET DASHBOARD VALUES
# =========================================================

(
    total_channels,
    total_videos,
    total_views,
    total_comments
) = get_dashboard_data()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("📊 YouTube Analytics")

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📥 Data Collection",
            "📺 Channel Analysis",
            "🎬 Video Analysis",
            "📚 Playlist Analysis",
            "🔎 SQL Insights",
            "👤 About Me",
            "📝 Report"
            
        ]
    )

    st.markdown("---")

    st.caption("Built with")

    st.caption("🐍 Python")
    st.caption("📡 YouTube API")
    st.caption("🍃 MongoDB")
    st.caption("🐬 MySQL")
    st.caption("📊 Streamlit")


# =========================================================
# MAIN PAGE
# =========================================================

st.title(page)


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.title("📊 YouTube Data Intelligence")

    st.markdown(
        "### Analyze channels, videos, playlists and audience engagement"
    )

    st.markdown("---")


    # =====================================================
    # KPI CARDS
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            label="📺 Total Channels",
            value=format_number(
                total_channels
            )
        )

    with col2:

        st.metric(
            label="🎬 Total Videos",
            value=format_number(
                total_videos
            )
        )

    with col3:

        st.metric(
            label="👁️ Total Views",
            value=format_number(
                total_views
            )
        )

    with col4:

        st.metric(
            label="💬 Total Comments",
            value=format_number(
                total_comments
            )
        )


    st.markdown("---")


    # =====================================================
    # LOAD DATA
    # =====================================================

    channel_df = get_channel_dataframe()

    video_df = get_video_dataframe()


    if not channel_df.empty:

        # =================================================
        # CHANNEL FILTER
        # =================================================

        st.subheader("🎯 Channel Filter")

        channel_names = [
            "All Channels"
        ] + sorted(
            channel_df[
                "channel_name"
            ].unique().tolist()
        )

        selected_channel = st.selectbox(
            "Select a channel",
            channel_names
        )


        if selected_channel != "All Channels":

            selected_channel_df = channel_df[
                channel_df["channel_name"]
                == selected_channel
            ]

        else:

            selected_channel_df = channel_df


        st.markdown("---")


        # =================================================
        # CHANNEL PERFORMANCE
        # =================================================

        st.subheader(
            "📊 Channel Performance"
        )

        col1, col2 = st.columns(2)


        # =================================================
        # SUBSCRIBERS
        # =================================================

        with col1:

            st.markdown(
                "**👥 Subscribers by Channel**"
            )

            subscriber_df = (
                selected_channel_df
                .sort_values(
                    "subscribers",
                    ascending=True
                )
                .copy()
            )

            subscriber_df[
                "subscriber_label"
            ] = subscriber_df[
                "subscribers"
            ].apply(format_number)


            fig_subscribers = px.bar(
                subscriber_df,
                x="subscribers",
                y="channel_name",
                orientation="h",
                text="subscriber_label",
                labels={
                    "subscribers": "Subscribers",
                    "channel_name": ""
                }
            )
            fig_subscribers.update_layout(
                paper_bgcolor="#0F0F0F",
                plot_bgcolor="#0F0F0F",
                font=dict(color="#FFFFFF"),
                xaxis=dict(
                    color="#FFFFFF",
                    gridcolor="#303030"
                ),
                yaxis=dict(
                    color="#FFFFFF",
                    gridcolor="#303030"
                )
            )

            fig_subscribers.update_traces(
                marker_color="#FF4B4B"
            )


            fig_subscribers.update_traces(
                textposition="outside",
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Subscribers: %{x:,}"
                    "<extra></extra>"
                )
            )


            # Custom subscriber axis
            max_subscribers = (
                subscriber_df["subscribers"].max()
            )

            if max_subscribers >= 1_000_000:

                subscriber_step = 500_000

            elif max_subscribers >= 100_000:

                subscriber_step = 100_000

            elif max_subscribers >= 1_000:

                subscriber_step = 10_000

            else:

                subscriber_step = 100


            subscriber_ticks = list(
                range(
                    0,
                    int(max_subscribers * 1.2)
                    + subscriber_step,
                    subscriber_step
                )
            )


            subscriber_ticktext = [
                format_axis_number(x)
                for x in subscriber_ticks
            ]


            fig_subscribers.update_layout(
                height=400,
                showlegend=False,
                margin=dict(
                    l=20,
                    r=80,
                    t=30,
                    b=40
                ),
                xaxis=dict(
                    showgrid=True,
                    tickmode="array",
                    tickvals=subscriber_ticks,
                    ticktext=subscriber_ticktext
                )
            )


            st.plotly_chart(
                fig_subscribers,
                use_container_width=True
            )


        # =================================================
        # VIEWS
        # =================================================

        with col2:

            st.markdown(
                "**👁️ Total Views by Channel**"
            )

            views_df = (
                selected_channel_df
                .sort_values(
                    "views",
                    ascending=True
                )
                .copy()
            )

            views_df["view_label"] = (
                views_df["views"]
                .apply(format_number)
            )


            fig_views = px.bar(
                views_df,
                x="views",
                y="channel_name",
                orientation="h",
                text="view_label",
                labels={
                    "views": "Total Views",
                    "channel_name": ""
                }
            )
            fig_views.update_layout(
            paper_bgcolor="#0F0F0F",
            plot_bgcolor="#0F0F0F",
            font=dict(color="#FFFFFF"),
            xaxis=dict(
                color="#FFFFFF",
                gridcolor="#303030"
            ),
            yaxis=dict(
                color="#FFFFFF",
                gridcolor="#303030"
            )
        )

            fig_views.update_traces(
                marker_color="#FF4B4B"
            )


            fig_views.update_traces(
                textposition="outside",
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Views: %{x:,}"
                    "<extra></extra>"
                )
            )


            # =================================================
            # CUSTOM VIEW AXIS
            # =================================================

            max_views = views_df["views"].max()


            if max_views >= 1_000_000_000:

                view_step = 500_000_000

            elif max_views >= 100_000_000:

                view_step = 100_000_000

            elif max_views >= 1_000_000:

                view_step = 1_000_000

            elif max_views >= 1_000:

                view_step = 1_000

            else:

                view_step = 100


            view_ticks = list(
                range(
                    0,
                    int(max_views * 1.2)
                    + view_step,
                    view_step
                )
            )


            view_ticktext = [
                format_axis_number(x)
                for x in view_ticks
            ]


            fig_views.update_layout(
                height=400,
                showlegend=False,
                margin=dict(
                    l=20,
                    r=80,
                    t=30,
                    b=40
                ),

                # IMPORTANT:
                # This removes 1.0G
                # and shows 1.0B instead.
                xaxis=dict(
                    showgrid=True,
                    tickmode="array",
                    tickvals=view_ticks,
                    ticktext=view_ticktext
                )
            )


            st.plotly_chart(
                fig_views,
                use_container_width=True
            )


        st.markdown("---")


        # =================================================
        # VIDEOS BY CHANNEL
        # =================================================

        st.subheader(
            "🎬 Videos Published by Channel"
        )

        video_count_df = (
            selected_channel_df
            .sort_values(
                "total_videos",
                ascending=True
            )
            .copy()
        )


        video_count_df[
            "video_label"
        ] = video_count_df[
            "total_videos"
        ].apply(format_number)


        fig_video_count = px.bar(
            video_count_df,
            x="total_videos",
            y="channel_name",
            orientation="h",
            text="video_label",
            labels={
                "total_videos": "Number of Videos",
                "channel_name": ""
            }
        )
        fig_video_count.update_layout(
            paper_bgcolor="#0F0F0F",
            plot_bgcolor="#0F0F0F",
            font=dict(color="#FFFFFF"),
            xaxis=dict(
                color="#FFFFFF",
                gridcolor="#303030"
            ),
            yaxis=dict(
                color="#FFFFFF",
                gridcolor="#303030"
            )
        )

        fig_video_count.update_traces(
            marker_color="#FF4B4B"
        )


        fig_video_count.update_traces(
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Videos: %{x:,}"
                "<extra></extra>"
            )
        )


        fig_video_count.update_layout(
            height=400,
            showlegend=False,
            margin=dict(
                l=20,
                r=80,
                t=30,
                b=40
            ),
            xaxis=dict(
                showgrid=True
            )
        )


        st.plotly_chart(
            fig_video_count,
            use_container_width=True
        )


    else:

        st.info(
            "No channel data available."
        )

        selected_channel = "All Channels"


    st.markdown("---")


    # =====================================================
    # TOP PERFORMING VIDEOS
    # =====================================================

    st.subheader(
        "🏆 Top Performing Videos"
    )


    if not video_df.empty:

        if selected_channel != "All Channels":

            filtered_videos = video_df[
                video_df["channel_name"]
                == selected_channel
            ].copy()

        else:

            filtered_videos = video_df.copy()


        top_videos = (
            filtered_videos[
                [
                    "video_title",
                    "channel_name",
                    "total_views",
                    "total_likes",
                    "total_comments"
                ]
            ]
            .sort_values(
                by="total_views",
                ascending=False
            )
            .head(10)
            .copy()
        )


        top_videos[
            "total_views"
        ] = top_videos[
            "total_views"
        ].apply(format_number)


        top_videos[
            "total_likes"
        ] = top_videos[
            "total_likes"
        ].apply(format_number)


        top_videos[
            "total_comments"
        ] = top_videos[
            "total_comments"
        ].apply(format_number)


        top_videos = top_videos.rename(
            columns={
                "video_title": "Video Title",
                "channel_name": "Channel",
                "total_views": "Views",
                "total_likes": "Likes",
                "total_comments": "Comments"
            }
        )


        st.dataframe(
            top_videos,
            use_container_width=True,
            hide_index=True,
            height=420
        )


    else:

        st.info(
            "No video data available."
        )


# =========================================================
# DATA COLLECTION
# =========================================================

elif page == "📥 Data Collection":

    st.title("📥 YouTube Data Collection")

    st.markdown(
        "### Collect channel, video, playlist and comment data"
    )

    st.markdown("---")


    # =====================================================
    # CHANNEL ID INPUT
    # =====================================================

    st.subheader(
        "🔎 Enter YouTube Channel ID"
    )


    channel_id = st.text_input(
        "Channel ID",
        placeholder="Example: UCxxxxxxxxxxxxxxxxxxxxxx"
    )


    st.caption(
        "Enter the YouTube Channel ID you want to collect."
    )


    # =====================================================
    # COLLECT BUTTON
    # =====================================================

    if st.button(
        "🚀 Collect & Store Data",
        use_container_width=True
    ):

        if not channel_id:

            st.warning(
                "⚠️ Please enter a Channel ID."
            )


        else:

            # =================================================
            # CHECK WHETHER CHANNEL ALREADY EXISTS
            # =================================================

            existing_channel = collection.find_one(
                {
                    "channel_information.channel_id":
                    channel_id
                }
            )


            if existing_channel:

                st.warning(
                    "⚠️ This channel already exists in MongoDB."
                )


                channel_info = (
                    existing_channel[
                        "channel_information"
                    ]
                )


                st.info(
                    f"📺 Channel: "
                    f"{channel_info['channel_name']}"
                )


            else:

                # =================================================
                # COLLECT DATA
                # =================================================

                with st.spinner(
                    "📡 Collecting YouTube data..."
                ):

                    try:

                        result = channel_details(
                            channel_id
                        )


                        st.success(
                            "✅ Data collected and stored successfully!"
                        )


                        # =================================================
                        # GET NEW CHANNEL
                        # =================================================

                        new_channel = collection.find_one(
                            {
                                "channel_information.channel_id":
                                channel_id
                            },
                            {
                                "_id": 0,
                                "channel_information": 1
                            }
                        )


                        if new_channel:

                            channel_info = (
                                new_channel[
                                    "channel_information"
                                ]
                            )


                            st.markdown("---")


                            st.subheader(
                                "📺 Collected Channel"
                            )


                            col1, col2, col3, col4 = (
                                st.columns(4)
                            )


                            with col1:

                                st.metric(
                                    "Channel",
                                    channel_info[
                                        "channel_name"
                                    ]
                                )


                            with col2:

                                st.metric(
                                    "Subscribers",
                                    format_number(
                                        channel_info[
                                            "subscribers"
                                        ]
                                    )
                                )


                            with col3:

                                st.metric(
                                    "Total Views",
                                    format_number(
                                        channel_info[
                                            "views"
                                        ]
                                    )
                                )


                            with col4:

                                st.metric(
                                    "Total Videos",
                                    format_number(
                                        channel_info[
                                            "total_videos"
                                        ]
                                    )
                                )


                    except Exception as e:

                        st.error(
                            f"❌ Data collection failed: {e}"
                        )


# =========================================================
# OTHER PAGES
# =========================================================

elif page == "📺 Channel Analysis":

    

    st.markdown(
        "### Detailed performance analysis of YouTube channels"
    )

    st.markdown("---")

    # =====================================================
    # GET CHANNEL DATA
    # =====================================================

    channel_df = get_channel_dataframe()

    video_df = get_video_dataframe()


    if not channel_df.empty:

        # =================================================
        # CHANNEL SELECTOR
        # =================================================

        selected_channel = st.selectbox(
            "📺 Select a Channel",
            sorted(
                channel_df["channel_name"].unique()
            )
        )


        # =================================================
        # SELECTED CHANNEL DATA
        # =================================================

        selected_data = channel_df[
            channel_df["channel_name"]
            == selected_channel
        ].iloc[0]

         # =================================================
        # CHANNEL PROFILE
        # =================================================

        st.markdown("---")

        st.subheader("📺 Channel Profile")

        col1, col2 = st.columns([1, 3])


        with col1:

            if pd.notna(
                selected_data["channel_profile"]
            ):

                st.image(
                    selected_data["channel_profile"],
                    width=180
                )


        with col2:

            st.markdown(
                f"## {selected_data['channel_name']}"
            )

            st.write(
                f"**Channel ID:** "
                f"{selected_data['channel_id']}"
            )

            st.write(
                f"**Description:** "
                f"{selected_data['description']}"
            )


        # =================================================
        # FILTER VIDEOS
        # =================================================

        channel_videos = video_df[
            video_df["channel_name"]
            == selected_channel
        ].copy()


        st.markdown("---")


        # =================================================
        # CHANNEL KPI CARDS
        # =================================================

        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "👥 Subscribers",
                format_number(
                    selected_data["subscribers"]
                )
            )


        with col2:

            st.metric(
                "👁️ Total Views",
                format_number(
                    selected_data["views"]
                )
            )


        with col3:

            st.metric(
                "🎬 Total Videos",
                format_number(
                    selected_data["total_videos"]
                )
            )


        with col4:

            if selected_data["total_videos"] > 0:

                avg_views = (
                    selected_data["views"]
                    / selected_data["total_videos"]
                )

            else:

                avg_views = 0


            st.metric(
                "📊 Avg Views / Video",
                format_number(avg_views)
            )


        st.markdown("---")


        # =================================================
        # VIDEO PERFORMANCE
        # =================================================

        st.subheader(
            "🎬 Video Performance"
        )


        if not channel_videos.empty:

            # ---------------------------------------------
            # Convert numeric columns
            # ---------------------------------------------

            channel_videos["total_views"] = pd.to_numeric(
                channel_videos["total_views"],
                errors="coerce"
            ).fillna(0)


            channel_videos["total_likes"] = pd.to_numeric(
                channel_videos["total_likes"],
                errors="coerce"
            ).fillna(0)


            channel_videos["total_comments"] = pd.to_numeric(
                channel_videos["total_comments"],
                errors="coerce"
            ).fillna(0)


            # ---------------------------------------------
            # VIDEO KPIs
            # ---------------------------------------------

            total_channel_views = (
                channel_videos["total_views"].sum()
            )

            total_channel_likes = (
                channel_videos["total_likes"].sum()
            )

            total_channel_comments = (
                channel_videos["total_comments"].sum()
            )

            video_count = len(channel_videos)


            avg_video_views = (
                total_channel_views / video_count
                if video_count > 0
                else 0
            )

            avg_video_likes = (
                total_channel_likes / video_count
                if video_count > 0
                else 0
            )

            avg_video_comments = (
                total_channel_comments / video_count
                if video_count > 0
                else 0
            )


            # ---------------------------------------------
            # PERFORMANCE METRICS
            # ---------------------------------------------

            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "👁️ Avg Views",
                    format_number(
                        avg_video_views
                    )
                )


            with col2:

                st.metric(
                    "❤️ Avg Likes",
                    format_number(
                        avg_video_likes
                    )
                )


            with col3:

                st.metric(
                    "💬 Avg Comments",
                    format_number(
                        avg_video_comments
                    )
                )


            st.markdown("---")


            # =================================================
            # TOP PERFORMING VIDEOS
            # =================================================

            st.subheader(
                "🏆 Top Performing Videos"
            )


            top_videos = (
                channel_videos
                .sort_values(
                    "total_views",
                    ascending=False
                )
                .head(10)
                .copy()
            )


            top_videos[
                "Views"
            ] = top_videos[
                "total_views"
            ].apply(format_number)


            top_videos[
                "Likes"
            ] = top_videos[
                "total_likes"
            ].apply(format_number)


            top_videos[
                "Comments"
            ] = top_videos[
                "total_comments"
            ].apply(format_number)


            top_videos = top_videos[
                [
                    "video_title",
                    "Views",
                    "Likes",
                    "Comments"
                ]
            ]


            top_videos = top_videos.rename(
                columns={
                    "video_title":
                        "Video Title"
                }
            )


            st.dataframe(
                top_videos,
                use_container_width=True,
                hide_index=True,
                height=400
            )


            st.markdown("---")


            # =================================================
            # VIEWS BY VIDEO
            # =================================================

            st.subheader(
                "👁️ Views by Video"
            )


            chart_df = (
                channel_videos
                .sort_values(
                    "total_views",
                    ascending=True
                )
                .tail(10)
                .copy()
            )


            chart_df["view_label"] = (
                chart_df[
                    "total_views"
                ].apply(format_number)
            )


            fig = px.bar(
                chart_df,
                x="total_views",
                y="video_title",
                orientation="h",
                text="view_label",
                labels={
                    "total_views":
                        "Total Views",
                    "video_title":
                        ""
                }
            )
            fig.update_layout(
                paper_bgcolor="#0F0F0F",
                plot_bgcolor="#0F0F0F",
                font=dict(color="#FFFFFF"),
                xaxis=dict(
                    color="#FFFFFF",
                    gridcolor="#303030"
                ),
                yaxis=dict(
                    color="#FFFFFF",
                    gridcolor="#303030"
                )
            )

            fig.update_traces(
                marker_color="#FF4B4B"
            )


            fig.update_traces(
                textposition="outside",
                cliponaxis=False,
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Views: %{x:,}"
                    "<extra></extra>"
                )
            )


            fig.update_layout(
                height=500,
                showlegend=False,
                margin=dict(
                    l=20,
                    r=80,
                    t=30,
                    b=40
                )
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )


        else:

            st.info(
                "No video data available for this channel."
            )


        st.markdown("---")


        # =================================================
        # CHANNEL INFORMATION
        # =================================================

        st.subheader(
            "📋 Channel Information"
        )


        col1, col2 = st.columns(2)


        with col1:

            st.write(
                f"**Channel Name:** "
                f"{selected_data['channel_name']}"
            )

            st.write(
                f"**Channel ID:** "
                f"{selected_data['channel_id']}"
            )

            st.write(
                f"**Playlist ID:** "
                f"{selected_data['playlist_id']}"
            )


        with col2:

            st.markdown(
                "**Description:**"
            )

            st.info(
                selected_data["description"]
            )


    else:

        st.info(
            "No channel data available."
        )
        


elif page == "🎬 Video Analysis":

   

    st.markdown(
        "### Detailed performance analysis of individual videos"
    )

    st.markdown("---")

    # =====================================================
    # GET VIDEO DATA
    # =====================================================

    video_df = get_video_dataframe()


    if not video_df.empty:

        # =================================================
        # CHANNEL SELECTOR
        # =================================================

        st.subheader("📺 Select Channel")

        channel_names = sorted(
            video_df["channel_name"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_channel = st.selectbox(
            "Choose a channel",
            channel_names
        )


        # =================================================
        # FILTER VIDEOS
        # =================================================

        filtered_videos = video_df[
            video_df["channel_name"]
            == selected_channel
        ].copy()


        # =================================================
        # VIDEO SELECTOR
        # =================================================

        st.subheader("🎬 Select Video")

        video_options = (
            filtered_videos[
                [
                    "video_id",
                    "video_title"
                ]
            ]
            .drop_duplicates()
        )


        selected_video_title = st.selectbox(
            "Choose a video",
            video_options["video_title"].tolist()
        )


        # =================================================
        # GET SELECTED VIDEO
        # =================================================

        selected_video = filtered_videos[
            filtered_videos["video_title"]
            == selected_video_title
        ].iloc[0]


        st.markdown("---")


        # =================================================
        # VIDEO INFORMATION
        # =================================================

        st.subheader("📋 Video Information")


        col1, col2 = st.columns([2, 1])


        # =================================================
        # VIDEO DETAILS
        # =================================================

        with col1:

            st.markdown(
                f"### 🎬 {selected_video['video_title']}"
            )

            st.write(
                f"**Channel:** "
                f"{selected_video['channel_name']}"
            )

            st.write(
                f"**Video ID:** "
                f"{selected_video['video_id']}"
            )

            st.write(
                f"**Published At:** "
                f"{selected_video['published_at']}"
            )

            st.write(
                f"**Duration:** "
                f"{selected_video['duration']}"
            )

            st.write(
                f"**Definition:** "
                f"{selected_video['definition']}"
            )

            st.write(
                f"**Caption Available:** "
                f"{selected_video['caption']}"
            )


        # =================================================
        # THUMBNAIL
        # =================================================

        with col2:

            if pd.notna(
                selected_video["thumbnails"]
            ):

                st.image(
                    selected_video["thumbnails"],
                    caption="Video Thumbnail",
                    use_container_width=True
                )


        st.markdown("---")
                # =================================================
        # VIDEO PERFORMANCE KPIs
        # =================================================

        st.subheader("📊 Video Performance")


        # Convert values to numbers
        views = pd.to_numeric(
            selected_video["total_views"],
            errors="coerce"
        )

        likes = pd.to_numeric(
            selected_video["total_likes"],
            errors="coerce"
        )

        comments = pd.to_numeric(
            selected_video["total_comments"],
            errors="coerce"
        )


        # Replace missing values with 0
        views = 0 if pd.isna(views) else views
        likes = 0 if pd.isna(likes) else likes
        comments = 0 if pd.isna(comments) else comments


        # Calculate engagement rates
        if views > 0:

            like_rate = (
                likes / views
            ) * 100

            comment_rate = (
                comments / views
            ) * 100

        else:

            like_rate = 0
            comment_rate = 0


        # =================================================
        # KPI CARDS
        # =================================================

        col1, col2, col3, col4, col5 = st.columns(5)


        with col1:

            st.metric(
                "👁️ Views",
                format_number(views)
            )


        with col2:

            st.metric(
                "❤️ Likes",
                format_number(likes)
            )


        with col3:

            st.metric(
                "💬 Comments",
                format_number(comments)
            )


        with col4:

            st.metric(
                "👍 Like Rate",
                f"{like_rate:.2f}%"
            )


        with col5:

            st.metric(
                "💬 Comment Rate",
                f"{comment_rate:.2f}%"
            )


        st.markdown("---")
        
                    # =================================================
        # UPLOAD TREND ANALYSIS
        # =================================================

        st.subheader("📅 Upload Trend Analysis")

        st.markdown(
            f"Analyze how frequently **{selected_channel}** uploaded videos over time."
        )


        # -------------------------------------------------
        # Use ONLY the selected channel's videos
        # -------------------------------------------------

        upload_df = filtered_videos.copy()


        # Make sure published_at is a datetime

        upload_df["published_at"] = pd.to_datetime(
            upload_df["published_at"],
            errors="coerce"
        )


        # Remove invalid dates

        upload_df = upload_df.dropna(
            subset=["published_at"]
        ).copy()


        # -------------------------------------------------
        # Time Period Selection
        # -------------------------------------------------

        period_option = st.selectbox(
            "Select Time Period",
            [
                "Monthly",
                "Quarterly",
                "Yearly"
            ],
            key="upload_period"
        )


        # -------------------------------------------------
        # Create Time Period
        # -------------------------------------------------

        if period_option == "Monthly":

            upload_df["period"] = (
                upload_df["published_at"]
                .dt.to_period("M")
                .astype(str)
            )

            period_title = (
                f"Monthly Video Uploads - {selected_channel}"
            )


        elif period_option == "Quarterly":

            upload_df["period"] = (
                upload_df["published_at"]
                .dt.to_period("Q")
                .astype(str)
            )

            period_title = (
                f"Quarterly Video Uploads - {selected_channel}"
            )


        else:

            upload_df["period"] = (
                upload_df["published_at"]
                .dt.year
                .astype(str)
            )

            period_title = (
                f"Yearly Video Uploads - {selected_channel}"
            )


        # -------------------------------------------------
        # Count Videos
        # -------------------------------------------------

        upload_trend = (
            upload_df
            .groupby("period")
            .size()
            .reset_index(name="video_count")
        )


        # -------------------------------------------------
        # Sort by Time
        # -------------------------------------------------

        upload_trend = upload_trend.sort_values(
            "period"
        )


        # -------------------------------------------------
        # Line Chart
        # -------------------------------------------------

        fig = px.line(
            upload_trend,
            x="period",
            y="video_count",
            markers=True,
            title=period_title
        )
        fig.update_layout(
            paper_bgcolor="#0F0F0F",
            plot_bgcolor="#0F0F0F",
            font=dict(color="#FFFFFF"),

            xaxis=dict(
                color="#FFFFFF",
                gridcolor="#303030"
            ),

            yaxis=dict(
                color="#FFFFFF",
                gridcolor="#303030"
            )
        )

        fig.update_traces(
            line=dict(
                color="#FF4B4B",
                width=3
            ),
            marker=dict(
                color="#FF4B4B"
            )
        )


        fig.update_layout(
            xaxis_title="Time Period",
            yaxis_title="Number of Videos",
            hovermode="x unified"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # =================================================
        # VIDEO DESCRIPTION
        # =================================================

        st.subheader("📝 Video Description")

        description = selected_video["description"]


        if description:

            st.write(description)

        else:

            st.info(
                "No description available."
            )


    else:

        st.info(
            "No video data available."
        )


elif page == "📚 Playlist Analysis":


    st.markdown(
        "### Analyze playlists and playlist video distribution"
    )

    st.markdown("---")
        # -----------------------------
    # Get Playlist Data
    # -----------------------------

    playlist_list = []

    for data in collection.find(
        {},
        {"_id": 0, "playlist_information": 1}
    ):

        playlist_list.extend(
            data.get("playlist_information", [])
        )


    playlist_df = pd.DataFrame(playlist_list)


    # -----------------------------
    # Playlist KPIs
    # -----------------------------

    if not playlist_df.empty:

        playlist_df["video_count"] = pd.to_numeric(
            playlist_df["video_count"],
            errors="coerce"
        ).fillna(0)


        total_playlists = len(playlist_df)

        total_playlist_videos = int(
            playlist_df["video_count"].sum()
        )


        largest_playlist = playlist_df.loc[
            playlist_df["video_count"].idxmax(),
            "title"
        ]

        largest_playlist_count = int(
            playlist_df["video_count"].max()
        )


        # Channel with most playlists

        channel_playlist_counts = (
            playlist_df
            .groupby("channel_name")
            .size()
            .sort_values(ascending=False)
        )

        top_playlist_channel = (
            channel_playlist_counts.index[0]
        )


        # -----------------------------
        # KPI Cards
        # -----------------------------

        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "📚 Total Playlists",
                format_number(total_playlists)
            )


        with col2:

            st.metric(
                "🎬 Playlist Videos",
                format_number(total_playlist_videos)
            )


        with col3:

            st.metric(
                "🏆 Largest Playlist",
                format_number(largest_playlist_count)
            )


        with col4:

            st.metric(
                "📺 Most Playlists",
                top_playlist_channel
            )


    else:

        st.info("No playlist data available.")

           # -----------------------------
    # Top Playlists
    # -----------------------------

    st.markdown("---")

    st.subheader("🏆 Top Playlists")

    if not playlist_df.empty:

        # Select required columns
        top_playlists = playlist_df[
            [
                "title",
                "channel_name",
                "video_count"
            ]
        ].copy()


        # Convert video count to numeric
        top_playlists["video_count"] = pd.to_numeric(
            top_playlists["video_count"],
            errors="coerce"
        ).fillna(0)


        # Create a readable label
        top_playlists["playlist_label"] = (
            '<b>'
            +top_playlists["channel_name"]
            + " </b>— "
            + top_playlists["title"]
        )


        # Sort and select top 10
        top_playlists = (
            top_playlists
            .sort_values(
                by="video_count",
                ascending=False
            )
            .head(10)
            .sort_values(
                by="video_count",
                ascending=True
            )
        )


        # -----------------------------
        # Horizontal Bar Chart
        # -----------------------------

        fig = px.bar(
            top_playlists,
            x="video_count",
            y="playlist_label",
            orientation="h",
            text="video_count",
            labels={
                "video_count": "Number of Videos",
                "playlist_label": "Channel — Playlist"
            },
            title="Top 10 Playlists by Video Count"
        )
        fig.update_layout(
                paper_bgcolor="#0F0F0F",
                plot_bgcolor="#0F0F0F",
                font=dict(color="#FFFFFF"),
                xaxis=dict(
                    color="#FFFFFF",
                    gridcolor="#303030"
                ),
                yaxis=dict(
                    color="#FFFFFF",
                    gridcolor="#303030"
                )
            )

        fig.update_traces(
            marker_color="#FF4B4B"
        )


        fig.update_traces(
            textposition="outside"
        )


        fig.update_layout(
            height=550,
            yaxis=dict(
                categoryorder="total ascending"
            )
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    else:

        st.info("No playlist data available.")
        # -----------------------------
    # Playlists by Channel
    # -----------------------------

    st.markdown("---")

    st.subheader("📺 Playlists by Channel")

    if not playlist_df.empty:

        channel_playlist_df = (
            playlist_df
            .groupby("channel_name")
            .size()
            .reset_index(name="playlist_count")
            .sort_values(
                by="playlist_count",
                ascending=True
            )
        )


        fig_channel = px.bar(
            channel_playlist_df,
            x="playlist_count",
            y="channel_name",
            orientation="h",
            text="playlist_count",
            labels={
                "playlist_count": "Number of Playlists",
                "channel_name": "Channel"
            },
            title="Number of Playlists by Channel"
        )
        fig_channel.update_layout(
                        paper_bgcolor="#0F0F0F",
                        plot_bgcolor="#0F0F0F",
                        font=dict(color="#FFFFFF"),
                        xaxis=dict(
                            color="#FFFFFF",
                            gridcolor="#303030"
                        ),
                        yaxis=dict(
                            color="#FFFFFF",
                            gridcolor="#303030"
                        )
                    )
        
        fig_channel.update_traces(marker_color="#FF4B4B")
        


        fig_channel.update_traces(
            textposition="outside"
        )


        fig_channel.update_layout(
            height=400
        )


        st.plotly_chart(
            fig_channel,
            use_container_width=True
        )

    else:

        st.info("No playlist data available.")


elif page == "🔎 SQL Insights":

    st.markdown(
        "### Explore YouTube data using SQL queries"
    )

    st.markdown("---")

    st.subheader("🔎 Select a Business Question")

    question = st.selectbox(
    "Choose a question",
    [
        "Select your query",
        "Which channel has the most subscribers?",
        "Which videos have the highest views?",
        "Which videos have the most likes?",
        "Which videos have the most comments?",
        "Which channel has the most videos?",
        "Which channel has the highest average views per video?",
        "Which channel uploads the most videos each year?",
        "Which channel has the highest total views?",
        "Which channel has the highest engagement rate?",
        "How many videos were uploaded each year?"
    ]
)

    st.markdown("---")

    if question == "Which channel has the most subscribers?":

        query = """
        SELECT
            channel_name,
            subscribers
        FROM channels
        ORDER BY subscribers DESC
        
        """

        try:

            mydb = get_mysql_connection()

            result = pd.read_sql(
                query,
                mydb
            )
            

            mydb.close()

            st.subheader("📊 Channel Subscribers")

            result["subscribers"] = pd.to_numeric(
                result["subscribers"],
                errors="coerce"
            ).fillna(0)

            display_result = result.copy()

            display_result["subscribers"] = (
                display_result["subscribers"]
                .apply(format_number)
            )

            display_result = display_result.rename(
                columns={
                    "channel_name": "Channel",
                    "subscribers": "Subscribers"
                }
            )

            st.dataframe(
                display_result,
                use_container_width=True,
                hide_index=True
            )

        except Exception as e:

            st.error(
                f"MySQL Error: {e}"
            )
                        # ---------------------------------
            # Top Channel KPI
            # ---------------------------------

        st.subheader("🏆 Top Channel")

        top_channel = result.iloc[0]

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "🏆 Top Channel",
                top_channel["channel_name"]
            )

        with col2:

            st.metric(
                "👥 Subscribers",
                format_number(
                    top_channel["subscribers"]
                )
            )

        st.markdown("---")

        



    elif question == "Which videos have the highest views?":

        query = """
        SELECT
            video_title,
            channel_name,
            total_views,
            total_likes,
            total_comments
        FROM videos
        ORDER BY total_views DESC
        LIMIT 10
        """

        try:

            mydb = get_mysql_connection()

            result = pd.read_sql(
                query,
                mydb
            )

            mydb.close()

            st.subheader("🏆 Top 10 Most Viewed Videos")

            # Convert values to numbers
            result["total_views"] = pd.to_numeric(
                result["total_views"],
                errors="coerce"
            ).fillna(0)

            result["total_likes"] = pd.to_numeric(
                result["total_likes"],
                errors="coerce"
            ).fillna(0)

            result["total_comments"] = pd.to_numeric(
                result["total_comments"],
                errors="coerce"
            ).fillna(0)


            # =============================
            # VIEWS DONUT CHART
            # =============================

            chart_df = result.copy()

            fig = px.pie(
                chart_df,
                names="video_title",
                values="total_views",
                hole=0.45,
                title="Top 10 Videos by Views"
            )
            fig.update_layout(
    paper_bgcolor="#0F0F0F",
    plot_bgcolor="#0F0F0F",
    font=dict(color="#FFFFFF"),

    legend=dict(
        font=dict(color="#FFFFFF")
    )
)

            fig.update_traces(
    marker=dict(
        colors=[
            "#FF4B4B",
            "#FF7A7A",
            "#FF9999",
            "#FFB3B3",
            "#E60000",
            "#CC0000",
            "#FF3333",
            "#FF6666",
            "#B30000",
            "#990000"
        ]
    ),
    textfont=dict(
        color="#FFFFFF"
    )
)

            fig.update_traces(
                textinfo="percent",
                hovertemplate="<b>%{label}</b><br>" +
                            "Views: %{value}<br>" +
                            "Share: %{percent}<extra></extra>"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.markdown("---")


            # =============================
            # VIDEO RANKING TABLE
            # =============================

            st.subheader("📊 Video Ranking")

            # Format numbers only for table
            result["total_views"] = result["total_views"].apply(
                format_number
            )

            result["total_likes"] = result["total_likes"].apply(
                format_number
            )

            result["total_comments"] = result["total_comments"].apply(
                format_number
            )

            # Rename columns
            result = result.rename(
                columns={
                    "video_title": "Video Title",
                    "channel_name": "Channel",
                    "total_views": "Views",
                    "total_likes": "Likes",
                    "total_comments": "Comments"
                }
            )

            st.dataframe(
                result,
                use_container_width=True,
                hide_index=True
            )

        except Exception as e:

            st.error(
                f"MySQL Error: {e}"
            )
            st.subheader("🏆 Top 10 Most Viewed Videos")


        

    elif question == "Which videos have the most likes?":

        query = """
        SELECT
            video_title,
            channel_name,
            total_likes,
            total_views,
            total_comments
        FROM videos
        ORDER BY total_likes DESC
        LIMIT 10
        """

        try:

            mydb = get_mysql_connection()

            result = pd.read_sql(
                query,
                mydb
            )

            mydb.close()

            st.subheader("❤️ Top 10 Most Liked Videos")

            # Convert values to numbers
            result["total_likes"] = pd.to_numeric(
                result["total_likes"],
                errors="coerce"
            ).fillna(0)

            result["total_views"] = pd.to_numeric(
                result["total_views"],
                errors="coerce"
            ).fillna(0)

            result["total_comments"] = pd.to_numeric(
                result["total_comments"],
                errors="coerce"
            ).fillna(0)


            # =============================
            # VERTICAL BAR CHART
            # =============================

            chart_df = result.copy()

            # Short video titles for X-axis
            chart_df["short_title"] = (
                chart_df["video_title"]
                .str.slice(0, 20)
            )

            fig = px.bar(
                chart_df,
                x="short_title",
                y="total_likes",
                title="Top 10 Videos by Likes",
                labels={
                    "short_title": "Video",
                    "total_likes": "Likes"
                },
                hover_data={
                    "video_title": True,
                    "channel_name": True,
                    "total_likes": True
                }
            )
            fig.update_layout(
    paper_bgcolor="#0F0F0F",
    plot_bgcolor="#0F0F0F",
    font=dict(color="#FFFFFF"),

    xaxis=dict(
        color="#FFFFFF",
        gridcolor="#303030"
    ),

    yaxis=dict(
        color="#FFFFFF",
        gridcolor="#303030"
    )
)

            fig.update_traces(
    marker_color="#FF4B4B"
)

            fig.update_layout(
                xaxis_title="Video",
                yaxis_title="Likes",
                xaxis_tickangle=-45,
                hovermode="x"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


            st.markdown("---")


            # =============================
            # VIDEO RANKING TABLE
            # =============================

            st.subheader("📊 Video Ranking")

            result["total_likes"] = result["total_likes"].apply(
                format_number
            )

            result["total_views"] = result["total_views"].apply(
                format_number
            )

            result["total_comments"] = result["total_comments"].apply(
                format_number
            )

            result = result.rename(
                columns={
                    "video_title": "Video Title",
                    "channel_name": "Channel",
                    "total_likes": "Likes",
                    "total_views": "Views",
                    "total_comments": "Comments"
                }
            )

            st.dataframe(
                result,
                use_container_width=True,
                hide_index=True
            )

        except Exception as e:

            st.error(
                f"MySQL Error: {e}"
            )
    elif question == "Which videos have the most comments?":

        query = """
        SELECT
            video_title,
            channel_name,
            total_comments,
            total_views,
            total_likes
        FROM videos
        ORDER BY total_comments DESC
        LIMIT 10
        """

        try:

            mydb = get_mysql_connection()

            result = pd.read_sql(
                query,
                mydb
            )

            mydb.close()

            st.subheader("💬 Top 10 Most Commented Videos")

            # Convert values to numbers
            result["total_comments"] = pd.to_numeric(
                result["total_comments"],
                errors="coerce"
            ).fillna(0)

            result["total_views"] = pd.to_numeric(
                result["total_views"],
                errors="coerce"
            ).fillna(0)

            result["total_likes"] = pd.to_numeric(
                result["total_likes"],
                errors="coerce"
            ).fillna(0)


            # =============================
            # VERTICAL BAR CHART
            # =============================

            chart_df = result.copy()

            chart_df["short_title"] = (
                chart_df["video_title"]
                .str.slice(0, 20)
            )

            fig = px.bar(
                chart_df,
                x="short_title",
                y="total_comments",
                title="Top 10 Videos by Comments",
                labels={
                    "short_title": "Video",
                    "total_comments": "Comments"
                },
                hover_data={
                    "video_title": True,
                    "channel_name": True,
                    "total_comments": True
                }
            )
            fig.update_layout(
    paper_bgcolor="#0F0F0F",
    plot_bgcolor="#0F0F0F",
    font=dict(color="#FFFFFF"),

    xaxis=dict(
        color="#FFFFFF",
        gridcolor="#303030"
    ),

    yaxis=dict(
        color="#FFFFFF",
        gridcolor="#303030"
    )
)

            fig.update_traces(
    marker_color="#FF4B4B"
)

            fig.update_layout(
                xaxis_title="Video",
                yaxis_title="Comments",
                xaxis_tickangle=-45,
                hovermode="x"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


            st.markdown("---")


            # =============================
            # VIDEO RANKING TABLE
            # =============================

            st.subheader("📊 Video Ranking")

            result["total_comments"] = result["total_comments"].apply(
                format_number
            )

            result["total_views"] = result["total_views"].apply(
                format_number
            )

            result["total_likes"] = result["total_likes"].apply(
                format_number
            )

            result = result.rename(
                columns={
                    "video_title": "Video Title",
                    "channel_name": "Channel",
                    "total_comments": "Comments",
                    "total_views": "Views",
                    "total_likes": "Likes"
                }
            )

            st.dataframe(
                result,
                use_container_width=True,
                hide_index=True
            )

        except Exception as e:

            st.error(
                f"MySQL Error: {e}"
            )
    elif question == "Which channel has the most videos?":

        query = """
        SELECT
            channel_name,
            total_videos
        FROM channels
        ORDER BY total_videos DESC
        """

        try:

            mydb = get_mysql_connection()

            result = pd.read_sql(
                query,
                mydb
            )

            mydb.close()

            st.subheader("📺 Videos by Channel")

            # Convert to numbers
            result["total_videos"] = pd.to_numeric(
                result["total_videos"],
                errors="coerce"
            ).fillna(0)


            # =============================
            # DONUT CHART
            # =============================

            fig = px.pie(
                result,
                names="channel_name",
                values="total_videos",
                hole=0.45,
                title="Video Distribution by Channel"
            )
            fig.update_layout(
    paper_bgcolor="#0F0F0F",
    plot_bgcolor="#0F0F0F",
    font=dict(color="#FFFFFF"),

    legend=dict(
        font=dict(color="#FFFFFF")
    )
)

            fig.update_traces(
    marker=dict(
        colors=[
            "#FF4B4B",
            "#FF7A7A",
            "#FF9999",
            "#FFB3B3",
            "#E60000",
            "#CC0000",
            "#FF3333",
            "#FF6666",
            "#B30000",
            "#990000"
        ]
    ),
    textfont=dict(
        color="#FFFFFF"
    )
)

            fig.update_traces(
                textinfo="percent",
                hovertemplate=
                    "<b>%{label}</b><br>" +
                    "Videos: %{value}<br>" +
                    "Share: %{percent}<extra></extra>"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


            st.markdown("---")


            # =============================
            # CHANNEL TABLE
            # =============================

            st.subheader("📊 Channel Video Count")

            result["total_videos"] = result["total_videos"].apply(
                format_number
            )

            result = result.rename(
                columns={
                    "channel_name": "Channel",
                    "total_videos": "Total Videos"
                }
            )

            st.dataframe(
                result,
                use_container_width=True,
                hide_index=True
            )

        except Exception as e:

            st.error(
                f"MySQL Error: {e}"
            )

    elif question == "Which channel has the highest average views per video?":

        query = """
        SELECT
            channel_name,
            AVG(total_views) AS average_views
        FROM videos
        GROUP BY channel_name
        ORDER BY average_views DESC
        """

        try:

            mydb = get_mysql_connection()

            result = pd.read_sql(
                query,
                mydb
            )

            mydb.close()

            st.subheader("📈 Average Views per Video")

            # Convert to numbers
            result["average_views"] = pd.to_numeric(
                result["average_views"],
                errors="coerce"
            ).fillna(0)


            # =============================
            # LINE CHART
            # =============================

            fig = px.line(
                result,
                x="channel_name",
                y="average_views",
                markers=True,
                title="Average Views per Video by Channel",
                labels={
                    "channel_name": "Channel",
                    "average_views": "Average Views"
                }
            )
            fig.update_layout(
    paper_bgcolor="#0F0F0F",
    plot_bgcolor="#0F0F0F",
    font=dict(color="#FFFFFF"),

    xaxis=dict(
        color="#FFFFFF",
        gridcolor="#303030"
    ),

    yaxis=dict(
        color="#FFFFFF",
        gridcolor="#303030"
    )
)

            fig.update_traces(
    line=dict(
        color="#FF4B4B",
        width=3
    ),
    marker=dict(
        color="#FF4B4B"
    )
)

            fig.update_layout(
                xaxis_title="Channel",
                yaxis_title="Average Views",
                hovermode="x unified"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


            st.markdown("---")


            # =============================
            # CHANNEL TABLE
            # =============================

            st.subheader("📊 Average Views Ranking")

            result["average_views"] = result["average_views"].apply(
                format_number
            )

            result = result.rename(
                columns={
                    "channel_name": "Channel",
                    "average_views": "Average Views"
                }
            )

            st.dataframe(
                result,
                use_container_width=True,
                hide_index=True
            )

        except Exception as e:

            st.error(
                f"MySQL Error: {e}"
            )
    
    elif question == "Which channel uploads the most videos each year?":

        query = """
        SELECT
            channel_name,
            YEAR(published_at) AS upload_year,
            COUNT(*) AS video_count
        FROM videos
        WHERE published_at IS NOT NULL
        GROUP BY channel_name, YEAR(published_at)
        ORDER BY upload_year, video_count DESC
        """

        try:

            mydb = get_mysql_connection()

            result = pd.read_sql(
                query,
                mydb
            )

            mydb.close()

            st.subheader("📅 Yearly Video Uploads by Channel")

            # Convert values to numbers
            result["upload_year"] = pd.to_numeric(
                result["upload_year"],
                errors="coerce"
            )

            result["video_count"] = pd.to_numeric(
                result["video_count"],
                errors="coerce"
            ).fillna(0)


            # =============================
            # MULTI-LINE CHART
            # =============================

            fig = px.line(
                result,
                x="upload_year",
                y="video_count",
                color="channel_name",
                markers=True,
                title="Yearly Video Uploads by Channel",
                labels={
                    "upload_year": "Year",
                    "video_count": "Videos Uploaded",
                    "channel_name": "Channel"
                }
            )
            fig.update_layout(
    paper_bgcolor="#0F0F0F",
    plot_bgcolor="#0F0F0F",
    font=dict(color="#FFFFFF"),

    xaxis=dict(
        color="#FFFFFF",
        gridcolor="#303030"
    ),

    yaxis=dict(
        color="#FFFFFF",
        gridcolor="#303030"
    ),

    legend=dict(
        font=dict(color="#FFFFFF")
    )
)

            fig.update_traces(
    line=dict(
        width=3
    ),
    marker=dict(
        size=6
    )
)

            fig.update_layout(
                xaxis_title="Year",
                yaxis_title="Videos Uploaded",
                hovermode="x unified"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


            st.markdown("---")


            # =============================
            # YEARLY UPLOAD TABLE
            # =============================

            st.subheader("📊 Yearly Upload Details")

            table_result = result.copy()

            table_result["upload_year"] = (
                table_result["upload_year"]
                .astype(int)
            )

            table_result["video_count"] = (
                table_result["video_count"]
                .apply(format_number)
            )

            table_result = table_result.rename(
                columns={
                    "channel_name": "Channel",
                    "upload_year": "Year",
                    "video_count": "Videos Uploaded"
                }
            )

            st.dataframe(
                table_result,
                use_container_width=True,
                hide_index=True
            )
        except Exception as e:

            st.error(
                f"MySQL Error: {e}"
            )

    elif question == "Which channel has the highest total views?":

        query = """
        SELECT
            channel_name,
            views
        FROM channels
        ORDER BY views DESC
        """

        try:

            mydb = get_mysql_connection()

            result = pd.read_sql(
                query,
                mydb
            )

            mydb.close()

            st.subheader("👁️ Total Views by Channel")

            # Convert views to numbers
            result["views"] = pd.to_numeric(
                result["views"],
                errors="coerce"
            ).fillna(0)


            # =============================
            # HORIZONTAL BAR CHART
            # =============================

            fig = px.bar(
                result,
                x="views",
                y="channel_name",
                orientation="h",
                title="Total Views by Channel",
                labels={
                    "views": "Total Views",
                    "channel_name": "Channel"
                }
            )
            fig.update_layout(
                paper_bgcolor="#0F0F0F",
                plot_bgcolor="#0F0F0F",
                font=dict(color="#FFFFFF"),
                xaxis=dict(
                    color="#FFFFFF",
                    gridcolor="#303030"
                ),
                yaxis=dict(
                    color="#FFFFFF",
                    gridcolor="#303030"
                )
            )

            fig.update_traces(
                marker_color="#FF4B4B"
            )

            fig.update_layout(
                yaxis=dict(
                    categoryorder="total ascending"
                ),
                xaxis_title="Total Views",
                yaxis_title="Channel"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


            st.markdown("---")


            # =============================
            # CHANNEL TABLE
            # =============================

            st.subheader("📊 Channel View Ranking")

            result["views"] = result["views"].apply(
                format_number
            )

            result = result.rename(
                columns={
                    "channel_name": "Channel",
                    "views": "Total Views"
                }
            )

            st.dataframe(
                result,
                use_container_width=True,
                hide_index=True
            )

        except Exception as e:

            st.error(
                f"MySQL Error: {e}"
            )

    elif question == "Which channel has the highest engagement rate?":

        query = """
        SELECT
            channel_name,
            SUM(total_views) AS total_views,
            SUM(total_likes) AS total_likes,
            SUM(total_comments) AS total_comments,
            (
                (SUM(total_likes) + SUM(total_comments))
                / NULLIF(SUM(total_views), 0)
            ) * 100 AS engagement_rate
        FROM videos
        GROUP BY channel_name
        ORDER BY engagement_rate DESC
        """

        try:

            mydb = get_mysql_connection()

            result = pd.read_sql(
                query,
                mydb
            )

            mydb.close()

            st.subheader("📈 Channel Engagement Rate")

            # Convert engagement rate to number
            result["engagement_rate"] = pd.to_numeric(
                result["engagement_rate"],
                errors="coerce"
            ).fillna(0)


            # =============================
            # HORIZONTAL BAR CHART
            # =============================

            fig = px.bar(
                result,
                x="engagement_rate",
                y="channel_name",
                orientation="h",
                title="Engagement Rate by Channel",
                labels={
                    "engagement_rate": "Engagement Rate (%)",
                    "channel_name": "Channel"
                },
                hover_data={
                    "engagement_rate": ":.2f"
                }
            )
            fig.update_layout(
                paper_bgcolor="#0F0F0F",
                plot_bgcolor="#0F0F0F",
                font=dict(color="#FFFFFF"),
                xaxis=dict(
                    color="#FFFFFF",
                    gridcolor="#303030"
                ),
                yaxis=dict(
                    color="#FFFFFF",
                    gridcolor="#303030"
                )
            )

            fig.update_traces(
                marker_color="#FF4B4B"
            )

            fig.update_layout(
                yaxis=dict(
                    categoryorder="total ascending"
                ),
                xaxis_title="Engagement Rate (%)",
                yaxis_title="Channel"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


            st.markdown("---")


            # =============================
            # ENGAGEMENT TABLE
            # =============================

            st.subheader("📊 Engagement Rate Ranking")

            table_result = result.copy()

            table_result["engagement_rate"] = (
                table_result["engagement_rate"]
                .apply(lambda x: f"{x:.2f}%")
            )

            table_result = table_result.rename(
                columns={
                    "channel_name": "Channel",
                    "engagement_rate": "Engagement Rate"
                }
            )

            st.dataframe(
                table_result[
                    ["Channel", "Engagement Rate"]
                ],
                use_container_width=True,
                hide_index=True
            )

        except Exception as e:

            st.error(
                f"MySQL Error: {e}"
            )

    elif question == "How many videos were uploaded each year?":

        query = """
        SELECT
            YEAR(published_at) AS upload_year,
            COUNT(*) AS video_count
        FROM videos
        WHERE published_at IS NOT NULL
        GROUP BY YEAR(published_at)
        ORDER BY upload_year
        """

        try:

            mydb = get_mysql_connection()

            result = pd.read_sql(
                query,
                mydb
            )

            mydb.close()

            st.subheader("📅 Yearly Video Uploads")

            # Convert values to numbers
            result["upload_year"] = pd.to_numeric(
                result["upload_year"],
                errors="coerce"
            )

            result["video_count"] = pd.to_numeric(
                result["video_count"],
                errors="coerce"
            ).fillna(0)


            # =============================
            # LINE CHART
            # =============================

            fig = px.line(
                result,
                x="upload_year",
                y="video_count",
                markers=True,
                title="Videos Uploaded Each Year",
                labels={
                    "upload_year": "Year",
                    "video_count": "Videos Uploaded"
                }
            )
            fig.update_layout(
    paper_bgcolor="#0F0F0F",
    plot_bgcolor="#0F0F0F",
    font=dict(color="#FFFFFF"),

    xaxis=dict(
        color="#FFFFFF",
        gridcolor="#303030"
    ),

    yaxis=dict(
        color="#FFFFFF",
        gridcolor="#303030"
    )
)

            fig.update_traces(
    line=dict(
        color="#FF4B4B",
        width=3
    ),
    marker=dict(
        color="#FF4B4B"
    )
)

            fig.update_layout(
                xaxis_title="Year",
                yaxis_title="Videos Uploaded",
                hovermode="x unified"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


            st.markdown("---")


            # =============================
            # YEARLY UPLOAD TABLE
            # =============================

            st.subheader("📊 Yearly Upload Details")

            table_result = result.copy()

            table_result["upload_year"] = (
                table_result["upload_year"]
                .astype(int)
            )

            table_result["video_count"] = (
                table_result["video_count"]
                .apply(format_number)
            )

            table_result = table_result.rename(
                columns={
                    "upload_year": "Year",
                    "video_count": "Videos Uploaded"
                }
            )

        # =====================================================
        # YEARLY UPLOAD TABLE
        # =====================================================

            styled_table = table_result.style.set_table_styles(
                    [
                        {
                            "selector": "th",
                            "props": [
                                ("font-weight", "bold")
                            ]
                        }
                    ]
                )


            st.dataframe(
                    styled_table,
                    use_container_width=True,
                    hide_index=True,

                    # Reduce height so there are no unnecessary empty rows
                    height=320,

                    column_config={

                        "Year": st.column_config.Column(
                            "Year",
                            width="small",
                            alignment="center"
                        ),

                        "Videos Uploaded": st.column_config.NumberColumn(
                            "Videos Uploaded",
                            alignment="center",
                            width="small",
                            format="%d"
                        )
                    }
                )

        except Exception as e:

            st.error(
                f"MySQL Error: {e}"
            )

elif page == "👤 About Me":

    # =====================================================
    # ABOUT ME
    # =====================================================

    st.markdown(
        ""
    )

    st.markdown(
        "### Hi, I'm R. Sastha 👋"
    )

    st.write(
        "I am a B.Sc. IT student with a strong interest in "
        "Data Analytics, Python, SQL, and data visualization."
    )

    st.markdown("---")


    # =====================================================
    # PROFILE
    # =====================================================

    col1, col2 = st.columns([1, 2])


    with col1:

        st.markdown(
            """
            ### 🎓 Education

            **B.Sc. Information Technology**

            Interested in building practical
            projects 
            using 
            data and technology.
            """
        )


    with col2:

        st.markdown(
            """
            ### 💡 Career Interest

            **Data Analyst**

            I enjoy working with data, finding useful
            insights, creating visualizations, and solving
            business problems using data.
            """
        )


    st.markdown("---")


    # =====================================================
    # TECHNICAL SKILLS
    # =====================================================

    st.subheader("🛠️ Technical Skills")


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.markdown(
            """
            ### 🐍 Python

            • Pandas  
            • Data Analysis  
            • Data Processing
            """
        )


    with col2:

        st.markdown(
            """
            ### 🗄️ SQL

            • MySQL  
            • Queries  
            • Joins  
            • Aggregations
            """
        )


    with col3:

        st.markdown(
            """
            ### 📊 Visualization

            • Power BI  
            • Plotly  
            • Streamlit
            """
        )


    with col4:

        st.markdown(
            """
            ### 🍃 Databases

            • MongoDB  
            • MySQL  
            • Data Storage
            """
        )


    st.markdown("---")


    # =====================================================
    # PROJECT
    # =====================================================

    st.subheader("🚀 Project")


    st.markdown(
        """
        ### 📺 YouTube Data Analytics

        This project collects YouTube channel, video,
        playlist, and comment data using the YouTube API.

        The collected data is stored in MongoDB and
        transferred to MySQL for analysis.

        The application provides interactive dashboards
        using Streamlit and Plotly to explore channel
        performance, video performance, upload trends,
        and SQL-based business insights.
        """
    )


    st.markdown("---")


    # =====================================================
    # PROJECT TECHNOLOGIES
    # =====================================================

    st.subheader("⚙️ Technologies Used")


    technologies = [
        "🐍 Python",
        "📊 Pandas",
        "🗄️ MySQL",
        "🍃 MongoDB",
        "📈 Plotly",
        "🎨 Streamlit",
        "▶️ YouTube Data API"
    ]


    st.write(
        " • ".join(technologies)
    )


    st.markdown("---")


    # =====================================================
    # CLOSING
    # =====================================================

    st.markdown(
        """
        ### 🎯 Career Goal

        My goal is to start my career as a **Data Analyst**
        and continue improving my skills in data analysis,
        visualization, SQL, and Python.

        **Thank you for exploring my project! 🙌**
        """
    )

elif page == "📝 Report":

    # =====================================================
    # REPORT
    # =====================================================

    st.markdown(
        "## 📄 YouTube Analytics Report"
    )

    st.markdown(
        "### Summary of collected YouTube channel and video data"
    )

    st.markdown("---")


    # =====================================================
    # GET DATA
    # =====================================================

    channel_df = get_channel_dataframe()
    video_df = get_video_dataframe()


    if not channel_df.empty:

        # Convert numeric columns
        channel_df["subscribers"] = pd.to_numeric(
            channel_df["subscribers"],
            errors="coerce"
        ).fillna(0)

        channel_df["views"] = pd.to_numeric(
            channel_df["views"],
            errors="coerce"
        ).fillna(0)

        channel_df["total_videos"] = pd.to_numeric(
            channel_df["total_videos"],
            errors="coerce"
        ).fillna(0)


        # =================================================
        # PROJECT OVERVIEW
        # =================================================

        st.subheader("📊 Project Overview")

        total_channels = len(channel_df)

        total_videos = len(video_df)

        total_subscribers = channel_df[
            "subscribers"
        ].sum()

        total_views = channel_df[
            "views"
        ].sum()


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "📺 Channels",
                format_number(total_channels)
            )


        with col2:

            st.metric(
                "🎬 Videos",
                format_number(total_videos)
            )


        with col3:

            st.metric(
                "👥 Total Subscribers",
                format_number(total_subscribers)
            )


        with col4:

            st.metric(
                "👁️ Total Views",
                format_number(total_views)
            )


        st.markdown("---")


        # =================================================
        # CHANNEL PERFORMANCE
        # =================================================

        st.subheader("🏆 Channel Performance")


        top_subscriber_channel = (
            channel_df
            .sort_values(
                "subscribers",
                ascending=False
            )
            .iloc[0]
        )


        top_view_channel = (
            channel_df
            .sort_values(
                "views",
                ascending=False
            )
            .iloc[0]
        )


        top_video_channel = (
            channel_df
            .sort_values(
                "total_videos",
                ascending=False
            )
            .iloc[0]
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "👑 Most Subscribers",
                top_subscriber_channel[
                    "channel_name"
                ],
                format_number(
                    top_subscriber_channel[
                        "subscribers"
                    ]
                )
            )


        with col2:

            st.metric(
                "👁️ Most Views",
                top_view_channel[
                    "channel_name"
                ],
                format_number(
                    top_view_channel[
                        "views"
                    ]
                )
            )


        with col3:

            st.metric(
                "🎬 Most Videos",
                top_video_channel[
                    "channel_name"
                ],
                format_number(
                    top_video_channel[
                        "total_videos"
                    ]
                )
            )


        st.markdown("---")


        # =================================================
        # CHANNEL SUMMARY TABLE
        # =================================================

        st.subheader("📋 Channel Summary")


        report_channels = channel_df[
            [
                "channel_name",
                "subscribers",
                "views",
                "total_videos"
            ]
        ].copy()


        report_channels[
            "subscribers"
        ] = report_channels[
            "subscribers"
        ].apply(format_number)


        report_channels[
            "views"
        ] = report_channels[
            "views"
        ].apply(format_number)


        report_channels[
            "total_videos"
        ] = report_channels[
            "total_videos"
        ].apply(format_number)


        report_channels = report_channels.rename(
            columns={
                "channel_name": "Channel",
                "subscribers": "Subscribers",
                "views": "Total Views",
                "total_videos": "Videos"
            }
        )


        st.dataframe(
            report_channels,
            use_container_width=True,
            hide_index=True
        )


        st.markdown("---")


        # =================================================
        # PROJECT INSIGHTS
        # =================================================

        st.subheader("💡 Key Insights")


        st.markdown(
            f"""
            • **{top_subscriber_channel['channel_name']}**
            has the highest number of subscribers with
            **{format_number(top_subscriber_channel['subscribers'])}**.

            • **{top_view_channel['channel_name']}**
            has the highest total channel views with
            **{format_number(top_view_channel['views'])}**.

            • **{top_video_channel['channel_name']}**
            has the highest number of uploaded videos with
            **{format_number(top_video_channel['total_videos'])}**.

            • The project currently contains data from
            **{format_number(total_channels)} channels**
            and **{format_number(total_videos)} videos**.
            """
        )


        st.markdown("---")


        # =================================================
        # TECHNOLOGY & DATA FLOW
        # =================================================

        st.subheader("⚙️ Project Technology & Data Flow")


        st.markdown(
            """
            ### 🔄 Data Pipeline

            **YouTube Data API**
            ↓  
            **MongoDB**
            ↓  
            **Python / Pandas**
            ↓  
            **MySQL**
            ↓  
            **Streamlit Dashboard**
            ↓  
            **Interactive Analysis & Reports**

            ### 🛠️ Technologies

            - 🐍 Python
            - 📊 Pandas
            - 🍃 MongoDB
            - 🗄️ MySQL
            - 📈 Plotly
            - 🎨 Streamlit
            - ▶️ YouTube Data API
            """
        )


        st.markdown("---")


        # =================================================
        # CONCLUSION
        # =================================================

        st.subheader("📝 Conclusion")


        st.write(
            "This YouTube Analytics project demonstrates how "
            "data can be collected from the YouTube API, stored "
            "in MongoDB, transferred to MySQL, and analyzed "
            "using Python, Pandas, SQL, and interactive "
            "Streamlit visualizations."
        )

        st.success(
            "🎯 The dashboard provides a complete view of "
            "channel, video, playlist, comment, and SQL-based "
            "business analysis."
        )


    else:

        st.info(
            "No channel data available to generate the report."
        )