# YouTube Data Harvesting & Analytics Platform

## Project Overview

A data analytics and warehousing project that collects YouTube channel and video data using the YouTube Data API, stores and processes the data using MongoDB, MySQL, and Pandas, and presents interactive insights through a Streamlit dashboard.

## Objectives

- Collect YouTube channel and video data using the YouTube Data API
- Store raw data in MongoDB
- Transform and organize the data using Python and Pandas
- Store structured data in MySQL
- Perform data analysis using SQL
- Build an interactive dashboard using Streamlit and Plotly
- Analyze channel performance, video views, and upload trends

## Technologies Used

- Python
- YouTube Data API
- Pandas
- MongoDB
- MySQL
- SQL
- Streamlit
- Plotly
- HTML
- CSS
- Jupyter Notebook

## Project Workflow

YouTube Data API  
↓  
Data Collection using Python  
↓  
MongoDB  
↓  
Data Transformation using Pandas  
↓  
MySQL Data Warehouse  
↓  
SQL Analysis  
↓  
Streamlit Dashboard  
↓  
Interactive Insights

## Key Features

### YouTube Data Collection

- Channel information
- Video details
- Playlist information
- Comments
- Video statistics

### Data Warehousing

The collected data is initially stored in MongoDB and then transformed and structured before being stored in MySQL for analytical querying.

### Data Analysis

SQL and Pandas are used to analyze:

- Channel statistics
- Video performance
- View counts
- Upload trends
- Top-performing videos
- Average views per video

### Interactive Dashboard

The Streamlit dashboard provides:

- Channel selection
- Channel statistics
- Subscriber and view metrics
- Video performance analysis
- Views by video
- Upload trend analysis
- Data exploration

## Project Structure

```text
youtube-data-harvesting-analytics/
│
├── app.py
├── youtube_functions.py
├── yt_test.ipynb
├── requirements.txt
├── README.md
├── .gitignore
│
└── assets/
    └── screenshots/
