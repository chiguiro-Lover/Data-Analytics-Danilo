# London Housing Price Analysis – Interpretable Regression Models

## Business Context
Understanding the factors that drive housing prices is critical for real estate valuation, investment analysis, and market decision-making. This project analyzes housing data from London to identify the key variables influencing property prices and to build an interpretable predictive model.

## Objective
- Identify the most influential features affecting housing prices
- Build an interpretable regression model for price estimation
- Validate statistical assumptions to ensure model reliability
- Translate analytical results into actionable insights

## Data Overview
- Dataset: London Housing dataset
- Observations: ~1,000 properties
- Features: Property characteristics, amenities, materials, and location-related variables
- Target variable: Property price

## Methodology
- Data cleaning and preprocessing
- Exploratory data analysis (EDA)
- Feature encoding and selection
- Linear regression modeling
- Assumption validation (linearity, multicollinearity, independence, homoscedasticity, normality)
- Log-transformation of the target variable to improve model stability and performance

## Key Insights
- Property size and type are the strongest drivers of housing prices
- Location-related variables have a significant impact even after controlling for other features
- Log-transformation of prices improved residual behavior and model generalization
- Several features contribute marginal value and could be removed without significant loss in performance

## Model Performance
- Adjusted R² (log-transformed model): ~0.77 on the test set
- RMSE remained stable between training and test data
- The model shows good interpretability and consistent predictive behavior within the observed price range

## Limitations & Next Steps
- The model captures only linear relationships
- Performance may degrade for extreme or luxury properties
- Predictions should be used as decision support, not as final appraisals
- Future work could include interaction terms, non-linear models, or additional location-level data

## Tools
Python, pandas, numpy, scikit-learn, statsmodels, matplotlib, seaborn
