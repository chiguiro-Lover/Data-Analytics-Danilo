# League of Legends ETL Pipeline & Analytics

## Overview
This project implements an end-to-end **ETL (Extract, Transform, Load) pipeline**
using the **Riot Games API** to collect, process, and prepare League of Legends
match data for analytical and visualization purposes.

The objective of this project is to simulate a real-world data pipeline scenario,
working with external APIs, semi-structured JSON data, and analytical datasets
ready for Exploratory Data Analysis (EDA) and Business Intelligence tools.

---

## Data Source

**Riot Games API – Match-V5**

- Official API provided by Riot Games
- Data retrieved using the Match-V5 endpoint
- Player-level and match-level statistics

### Match Types Included
- **Normal Draft (Queue ID: 400)**
- **Ranked Solo/Duo (Queue ID: 420)**
- **Ranked Flex (Queue ID: 440)**

### Time Window
- Matches played **from January 1st, 2025 onward**
- All available matches per player within this period

---

## Pipeline Architecture

The project follows a modular ETL design:

## ⚙️ Pipeline Components

### 1. Extract
- Retrieves match IDs per summoner and queue type
- Fetches detailed match data
- Stores raw match data as JSON files
- Handles:
  - Multiple summoners
  - Multiple queue types
  - API rate limits
  - Duplicate match prevention

**Key files:**
- `src/riot_api.py`
- `src/extract.py`

---

### 2. Transform
- Parses raw JSON match files
- Extracts relevant match-level and player-level features
- Produces a structured dataset suitable for analysis

**Output:**
- `data/processed/matches_processed.csv`

**Key file:**
- `src/transform.py`

---

### 3. Load (Initial Stage)
- Saves transformed data into a CSV file
- Serves as the foundation for:
  - Data cleaning
  - Feature engineering
  - EDA
  - BI dashboards