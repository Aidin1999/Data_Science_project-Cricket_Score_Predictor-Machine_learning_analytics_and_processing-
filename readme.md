# Data Science Project: Cricket Score Prediction

## Repository Overview

This repository contains all the files and scripts used for building a cricket score prediction model. The directory structure is as follows:

- **`all_json.zip`**: Source data in JSON format.
- **`data.csv`**: Output file containing processed and feature-engineered data ready for machine learning applications.
- **`match.csv` & `player_data.csv`**: Raw input files containing detailed cricket match and player data.
- **Python Files**:
  - **`import_data_to_mongodb.py`**: Script to import JSON data into MongoDB for efficient querying and analysis.
  - **`qury-mongo.py`**: Script to query MongoDB and retrieve subsets of data for further analysis.
  - **`test.py` & `test2.py`**: Validation scripts to compare the model output with real-world data and ensure accuracy.
- **Notebooks**:
  - **`part1_data_analysis_visualisation_processing_and_processing.ipynb`**: Notebook for data preprocessing, feature engineering, and visualization.
  - **`Part_2_Model_training.ipynb`**: Notebook for training machine learning models on processed data.
- **`to day.csv`**: Normalized player statistics for the current day, generated as part of the pipeline.

---
## Part 0: Validation and Extensions

### 1. Validation
- **Scripts**:
  - **`test.py` & `test2.py`**:
    - Validate the predictive model's outputs using real-world cricket data.
    - Ensure predictions align with actual outcomes from historical matches.
- **Methods**:
  - Compare predicted scores with actual scores using statistical metrics.
  - Generate confusion matrices and residual plots to identify areas for improvement.

### 2. Possible Extensions
- **Win Probability Model**:
  - Combine predicted scores with historical win rates to calculate the probability of a team's victory.
  - Initial results indicate 85% accuracy.
- **Player Value Model**:
  - Generate player rankings based on performance metrics.
  - Use rankings to identify key contributors and strategize team compositions.

---

## Part 1: Data Engineering

### 1. Extracting and Merging Data
- **Source**: The primary data source is **Cricsheet**, provided in the **`all_json.zip`** archive. These files contain match-level cricket data, including player and team statistics.
- **Objective**:
  - Parse and preprocess the JSON files to extract relevant features.
  - Merge multiple datasets (`match.csv`, `player_data.csv`) to form a comprehensive dataset.
- **Scripts Used**:
  - **`import_data_to_mongodb.py`**:
    - Uploads JSON files into a MongoDB database for structured storage and efficient querying.
    - Ensures data integrity by verifying schema consistency during the upload process.
  - **`qury-mongo.py`**:
    - Queries MongoDB to extract filtered datasets (e.g., matches from specific years, players' performance summaries).
    - Outputs the queried data in a tabular format for downstream processing.

### 2. Preprocessing and Feature Engineering
- **Notebook**: `part1_data_analysis_visualisation_processing_and_processing.ipynb`
- **Key Steps**:
  - **Data Cleaning**:
    - Handled missing values in player and match statistics.
    - Standardized date formats and match identifiers.
  - **Feature Engineering**:
    - **Player-Level Features**:
      - Batting: Runs scored, strike rate.
      - Bowling: Dot balls, economy rate.
      - Fielding: Player of the Match awards.
      - Career stats: Total matches played (experience).
    - **Team-Level Features**:
      - Team and opponent strength based on player aggregates.
      - Win history: Cumulative wins and seasonal trends.
      - Match context: Type of match, gender, month of play.
  - **Normalization**:
    - Player metrics were normalized to a scale of 0-100 to ensure consistency across features.

### 3. Outputs
- **Intermediate Outputs**:
  - `to day.csv`: Contains normalized player statistics for real-time analysis.
- **Final Output**:
  - `data.csv`: Fully processed and feature-engineered dataset, ready for machine learning applications.

---

## Part 2: Model Training

### 1. Objectives
- Train a predictive model to estimate the final innings score based on match and player statistics.
- Evaluate model performance and explore improvements through hyperparameter tuning.

### 2. Workflow
- **Notebook**: `Part_2_Model_training.ipynb`
- **Steps**:
  1. **Load Processed Data**:
     - The cleaned dataset (`data.csv`) is loaded into the notebook for training.
  2. **Train-Test Split**:
     - The data is split into training and testing sets (80:20) to evaluate model performance.
  3. **Model Training**:
     - Multiple regression models were trained, including:
       - DecisionTreeRegressor
       - RandomForestRegressor
       - GradientBoostingRegressor
       - CatBoostRegressor
       - XGBoostRegressor
     - Custom evaluation metrics were used to balance overfitting, underfitting, and accuracy.
  4. **Hyperparameter Tuning**:
     - GridSearchCV was applied to optimize model parameters like tree depth, learning rate, and number of estimators.
  5. **Model Evaluation**:
     - Performance metrics (R², RMSE) and residual analysis were used to assess models.

### 3. Outputs
- **Best Model**: GradientBoostingRegressor
  - R²: 0.92
  - RMSE: 18.5
  - Custom Metric: 0.84

---


## Conclusion

This repository successfully demonstrates the end-to-end process of building a cricket score prediction model, from data engineering to model training and validation. The use of MongoDB for structured data storage and the implementation of advanced regression models highlight the project's scalability and robustness. Extensions like win probability and player value modeling further showcase its potential for real-world applications.
