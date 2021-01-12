# Intro to Apache Beam

This is a **Introduction to Apache Beam using Python** Repository. Here we will try to learn basics of Apache Beam to create **Batch** and **Streaming** pipelines. We will follow the learn step by step how to create a pipeline and what are the outputs after each phase:

1. **Introduction to Apache Beam Model**
2. **Basic Codes**
3. **Batch Pipelines**
4. **Streaming Pipeplines**
5. **Conclusion**


## Motivation
For the last two years, I have been part of a great learning curve wherein I have upskilled myself to move into a Machine Learning and Cloud Computing. This project was practice project for all the learnings I have had. This is first of the many more to come. 
 

## Libraries/frameworks used

<b>Built with</b>
- [Apache Beam](https://beam.apache.org/documentation/programming-guide/)
- [Anaconda](https://www.anaconda.com/)
- [Python](https://www.python.org/)

## Code Example

```bash
    # clone this repo, removing the '-' to allow python imports:
    git clone https://github.com/adityasolanki205/Intro-to-Apache-Beam.git
```

## Apache Beam

Below are the steps to setup the enviroment and run the codes:

1. **Introduction to Apache Beam Model**: Apache Beam is an open source model for creating both batch and streaming data-parallel processing pipelines. we will use python to build a program that defines the pipeline. The pipeline is then executed by one of Beam’s supported distributed processing back-ends like Google Cloud Dataflow.

    Beam is particularly useful for Embarrassingly Parallel data processing tasks, for Extract, Transform, and Load (ETL) tasks and pure data integration. These tasks are useful for moving data between different storage media and data sources, transforming data into a more desirable format, or loading data onto a new system.

    Everything in Apache beam are done in form of abstractions like pipelines, Pcollections and Ptransforms. Ptransforms are performed on Pcollections and this process is called pipeline.


2. **Basic Codes**: Now we go step by step to learn Apache beam coding:
    
    i. First is to define the Pipeline options

```python
    # All the codes are written in Jupyter Notebooks

    # Checking if there are any missing values
    customers.isnull().sum()
     
    # Checking how skewed is the data in the two classes of credit worthy and non credit worthy customers
    classification_count = customers.groupby('Classification').count()
    classification_count['Existing account']
    
    # Using group by we will try to capture various hidden details in the data
    grouped_data = df.groupby([column]).get_group(value)
    
    # Using various graphs we will try to see the details of the data
    sns.factorplot(data=customers, 
                   col='Number of credits', 
                   x='Credit history', 
                   y='Age', 
                   hue='Classification', 
                   kind='swarm', size=11, aspect=0.4, s=7)
```

3. **Data Wrangling**:  Now we will clean the data to be used by the Machine learning algorithms. Using Logrithmic transforms, Min Max Scaling and One Hot Encoding we will make the data machine readable and more relavant,

```python
    # Logrithmic transform to remove the outliers
    customers[numeric_columns].apply(lambda x: np.log(x + 1))
    
    # Min Max scaling to normalize the data
    customers_log_transformed[numeric_columns] = scaler.fit_transform(customers_log_transformed[numeric_columns])
    
    # One Hot Encoding for the Data becomes machine readable
    customers_final = pd.get_dummies(customers_log_transformed)
```

4. **Model Selection**: Now we will train 3 different types of Models and see which one is preforming better.

```python
    # First is Random Forest Algorithm
    Randon_forest_pred  = RandomForestClassifier().fit(X_train, y_train).predict(X_test)
    
    # Second is Logistic Regression Algorithm
    Logistic_regression_pred   = LogisticRegression().fit(X_train, y_train).predict(X_test)
    
    # Third is Support Vector Machine
    SVC_pred  = SVC(kernel = 'linear',probability = True).fit(X_train, y_train).predict(X_test)
```

5. **Model Evaluation**: After selecting top 2 models we will try to evaluate which one is better on the given model. Also as per the given problem we will find Fbeta score.

```python
   # First we will try to find the ROC curve for both the models
   roc_curve(y_test, lr_probs, pos_label=2)
   
   # Then we will try to the Best Classifier using Grid Search CV
   GridSearchCV(clf, parameters, scoring = scorer).fit(X_train, y_train).best_estimator_
```

6. **Conclusion**: Atlast we will conclude about everything we found out. 


## How to use?
To test the code we need to do the following:

    1. Copy the german.data in the current folder
    
    2. Open the 'German credit.ipynb'
    
    3. Run all the cells
    
## Repository Content

    1. German Credit.ipynb

    2. German Credit.html
    
    3. German Credit-Tensorflow.ipynb

    2. German Credit-Tensorflow.html
    
    3. german.data    
    
    4. german.data-numeric
    
    5. german.doc
    

## Credits
1. Akash Nimare's [README.md](https://gist.github.com/akashnimare/7b065c12d9750578de8e705fb4771d2f#file-readme-md)
2. [Machine Learning Mastery](https://machinelearningmastery.com/imbalanced-classification-of-good-and-bad-credit/)