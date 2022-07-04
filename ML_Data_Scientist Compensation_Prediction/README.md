# Machine Learning: Annual Compensation Prediction for Data Scientist
-------

## Overview

The main motivation for this project is to create machine learning models that help data scientists identify a salary range for their salary negotiations when looking for or switching jobs. The objective is to predict annual compensation bands based on specific features such as the number of years with professional coding experience, education level, data science skill sets (i.e. programming languages known, web frameworks learned, database, etc.) and other demographics information.

See below for a framework of how to interact with this repository. 

## Project Organization

    │
    ├── README.md          <- The top-level README describing the project aims
    │
    └── Report             <- .ipynb notebooks used for EDA and model generation, evaluation

## Project Summary

- *Outcome Variable*: in this project, I used the raw data of annual compensation values from 0 - 250,000 USD (continuous scale) for prediction.
<br>

- *Model Evaluation Objective*: find the best ML model with highest R-squared score, and lowest Root Mean Square Error (RMSE).
<br><br>

#### Baseline Model
- Using Linear Regression with all 75 features for all countries in the dataset. 
- Baseline model performance:

|       Model       | RMSE Dev Data | R2 Score Dev Data |
|:------------------|--------------:|------------------:|
| Linear Regression |     30,144.14 |             0.632 |

<br><br>

#### Best Model
- Using XGBoost Regressor with all 75 features for all countries in the dataset. 
- Best model performance:

<br>


|       Model          | RMSE Test Data | R2 Score Test Data |
|:---------------------|---------------:|-------------------:|
| XGBoosting Regressor |      26,919.16 |              0.714 |

<br>

|         Model        | RMSE Dev Data | R2 Score Dev Data |                                      Hyperparameters Tuning                                 |
|:---------------------|--------------:|------------------:|:--------------------------------------------------------------------------------------------|
| XGBoosting Regressor |     29,166.97 |             0.656 | max_depth=10, n_estimators=150, <br>colsample_bytree=0.5, lambda=100, <br>learning_rate=0.1 |


<br><br>

####  Model Comparison
I've also ran different models and evaluated their performance, summary of these models with hyperparameters tuning are as following. 

| Model                                   | RMSE Dev Data | R2 Score Dev Data | Hyperparameters Tuning                                                                                        |
|-----------------------------------------|--------------:|------------------:|---------------------------------------------------------------------------------------------------------------|
| XGBoosting Regressor (Best Model)       |     29,166.97 |             0.656 | max_depth=10, n_estimators=150, <br>colsample_bytree=0.5, lambda=100, <br>learning_rate=0.1                 |
| OLS Regression (Baseline)               |     30,144.14 |             0.632 |                                                                                                               |
| OLS Regression Log Transformed          |     32,153.94 |             0.495 |                                                                                                               |
| Ridge Regression                        |     30,161.06 |             0.632 | alpha=2                                                                                                       |
| Lasso Regression                        |     30,144.72 |             0.632 | alpha=10                                                                                                      |
| Random Forest Regressor                 |     29,907.63 |             0.638 | max_depth=30, n_estimators=150,<br>min_samples_split=30, min_samples_leaf=3                                 |
| ADA Boosting Regressor                  |     29,986.60 |             0.636 | max_depth=30, n_estimators=150,<br>min_samples_split=20, min_samples_leaf=3                                 |
| Gradient Boosting Regressor             |     29,683.04 |             0.644 | max_depth=3, n_estimators=150, <br>min_samples_split=20, min_samples_leaf=5                               |
| Support Vector Regressor                |     30,439.58 |             0.625 | kernel=linear, C=100, epsilon=0.001                                                                           |
| Regression with PCA                     |     31,449.84 |             0.600 | n_components = 50                                                                                             |
| XGBoosting Regressor with PCA           |     30,720.91 |             0.618 | n_components = 50, max_depth=3, <br>colsample_bytree=0.3, lambda=1,   <br>learning_rate=0.3, n_estimators=150 |
| Regression with Top n Important Features |     30,311.20 |             0.628 | n_features=50                                                                                                 |

<br><br>

#### Limitation
- I've looked at subsetting the data for United States Only, however, the predicting power - RMSE and R2 score performance was much lower than using all countries. The limitation was due to lacking of several key features like State, industry information and number of working hours weekly in the dataset, and low sample counts which could result in high bias and underfitting in our models.  
- The models are sensitive with out-liers, records with salary over 250,000 USD negatively impact the performance of the models and therefore we decided to drop them from our model data. 