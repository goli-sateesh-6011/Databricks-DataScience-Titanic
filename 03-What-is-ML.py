# Databricks notebook source
# MAGIC %md
# MAGIC ![x](https://zdnet4.cbsistatic.com/hub/i/r/2017/12/17/e9b8f576-8c65-4308-93fa-55ee47cdd7ef/resize/370xauto/30f614c5879a8589a22e57b3108195f3/databricks-logo.png)

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2019 Databricks, Inc. All rights reserved.<br/>

# COMMAND ----------

# MAGIC %md
# MAGIC # What is Machine Learning?
# MAGIC 
# MAGIC Machine learning discovers patterns within data without being explicitly programmed.  This lesson introduces machine learning, explores the main topics in the field, and builds an end-to-end pipeline in Spark.
# MAGIC 
# MAGIC #### Agenda:
# MAGIC * Define machine learning
# MAGIC * Differentiate supervised and unsupervised tasks
# MAGIC * Identify regression and classification tasks
# MAGIC * Train a model, interpret the results, and create predictions

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## Learning from Data
# MAGIC 
# MAGIC Machine learning refers to a diverse set of tools for understanding data.  More technically, **machine learning is the process of _learning from data_ without being _explicitly programmed_**.  Let's unpack what that means.
# MAGIC 
# MAGIC Take a dataset of Boston home values in the 1970's for example.  The dataset consists of the value of homes as well as the number of rooms, crime per capita, and percent of the population considered lower class.  Home value is the _output variable_, also known as the _label_.  The other variables are known as _input variables_ or _features_.
# MAGIC 
# MAGIC A machine learning model would _learn_ the relationship between housing price and the various features without being explicitly programmed.  In more technical terms, our model would estimate a function `f()` that maps the relationship between input features and the output variable.
# MAGIC 
# MAGIC The following image shows the relation between our features and house value.  A good model `f()` would learn from the data that the number of rooms in a home is positively correlated to the house value while crime and percent of the neighborhood that is lower class is negatively correlated.  
# MAGIC 
# MAGIC <div><img src="https://files.training.databricks.com/images/eLearning/ML-Part-1/boston-housing.png" style="height: 400px; margin: 20px"/></div>
# MAGIC 
# MAGIC The lines above represent the best fit for the data where our model's best guess for a house price given a feature value on the X axis is the corresponding point on the line.
# MAGIC 
# MAGIC **Machine learning is the set of approaches for estimating this function `f()` that maps features to an output.**  The inputs to this function can range from stock prices and customer information to images and DNA sequences.  Many of the same statistical techniques apply regardless of the domain.  This makes machine learning a generalizable skill set that drives decision-making in modern businesses.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## Supervised vs Unsupervised Learning
# MAGIC 
# MAGIC Machine learning problems are roughly categorized into two main types:<br><br>
# MAGIC 
# MAGIC * **Supervised learning** looks to predict the value of some outcome based on one or more input measures
# MAGIC   - Our example of the Boston Housing Dataset is an example of supervised learning
# MAGIC   - In this case, the output is the price of a home and the input is features such as number of rooms
# MAGIC * **Unsupervised learning** describes associations and patterns in data without a known outcome
# MAGIC   - An example of this would be clustering customer data to find the naturally occurring customer segments
# MAGIC   - In this case, no known output is used as an input.  Instead, the goal is to discover how the data are organized into natural segments or clusters
# MAGIC 
# MAGIC This course will cover supervised learning, which is the vast majority of machine learning use cases in industry.  Later courses will look at unsupervised approaches.
# MAGIC 
# MAGIC <div><img src="https://files.training.databricks.com/images/eLearning/ML-Part-1/regression.png" style="height: 400px; margin: 20px"/><img src="https://files.training.databricks.com/images/eLearning/ML-Part-1/clustering.png" style="height: 400px; margin: 20px"/></div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## Regression vs Classification
# MAGIC 
# MAGIC Variables can either be quantitative or qualitative:<br><br>
# MAGIC 
# MAGIC * **Quantitative** values are numeric and generally unbounded, taking any positive or negative value
# MAGIC * **Qualitative** values take on a set number of classes or categories
# MAGIC 
# MAGIC | Variable type    | Also known as         | Examples                                                          |
# MAGIC |:-----------------|:----------------------|:------------------------------------------------------------------|
# MAGIC | quantitative     | continuous, numerical | age, salary, temperature                                          |
# MAGIC | qualitative      | categorical, discrete | gender, whether or a not a patient has cancer, state of residence |
# MAGIC 
# MAGIC Machine learning models operate on numbers so a qualitative variable like gender, for instance, would need to be encoded as `0` for male or `1` for female.  In this case, female isn't "one more" than male, so this variable is handled differently compared to a quantitative variable.
# MAGIC 
# MAGIC Generally speaking, **a supervised model learning a quantitative variable is called regression and a model learning a qualitative variable is called classification.**
# MAGIC 
# MAGIC <div><img src="https://files.training.databricks.com/images/eLearning/ML-Part-1/classification_v_regression.jpg" style="height: 400px; margin: 20px"/>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Feature Engineering
# MAGIC 
# MAGIC **What is a feature?**
# MAGIC 
# MAGIC A feature is an attribute or property shared by all of the independent units on which analysis or prediction is to be done. Any attribute could be a feature, as long as it is useful to the model.  
# MAGIC The purpose of a feature, other than being an attribute, would be much easier to understand in the context of a problem. A feature is a characteristic that might help when solving the problem.
# MAGIC 
# MAGIC **What is feature engineering?**  
# MAGIC 
# MAGIC Feature engineering is the process of using domain knowledge of the data to create features that make machine learning algorithms work. Feature engineering is fundamental to the application of machine learning, and is both difficult and expensive. The need for manual feature engineering can be obviated by automated feature learning.
# MAGIC 
# MAGIC The features in your data are important to the predictive models you use and will influence the results you are going to achieve. The quality and quantity of the features will have great influence on whether the model is good or not.

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC #### Commonly used terms:
# MAGIC 
# MAGIC ** Feature: **<BR>
# MAGIC &emsp;An attribute useful for your modeling task
# MAGIC   
# MAGIC ** Feature Importance: **<BR>
# MAGIC &emsp;An estimate of the usefulness of a feature
# MAGIC 
# MAGIC ** Feature Extraction: **<BR>
# MAGIC &emsp;The automatic construction of new features from raw data
# MAGIC 
# MAGIC ** Feature Selection: **<BR>
# MAGIC &emsp;From many features to a few that are useful
# MAGIC   
# MAGIC ** Feature Construction: **<BR>
# MAGIC &emsp;The manual construction of new features from raw data
# MAGIC   
# MAGIC ** Feature Learning: **<BR>
# MAGIC &emsp;The automatic identification and use of features in raw data

# COMMAND ----------

# MAGIC %md 
# MAGIC ## ![Spark Logo Tiny](https://kpistoropen.blob.core.windows.net/collateral/roadshow/logo_spark_tiny.png) What is Spark MLlib?
# MAGIC 
# MAGIC **MLlib is Spark’s machine learning (ML) library. Its goal is to make practical machine learning scalable and easy.**
# MAGIC 
# MAGIC **At a high level, it provides tools such as:**
# MAGIC * ML Algorithms: common learning algorithms such as classification, regression, clustering, and collaborative filtering
# MAGIC * Featurization: feature extraction, transformation, dimensionality reduction, and selection
# MAGIC * Pipelines: tools for constructing, evaluating, and tuning ML Pipelines
# MAGIC * Persistence: saving and load algorithms, models, and Pipelines
# MAGIC * Utilities: linear algebra, statistics, data handling, etc.
# MAGIC 
# MAGIC See [MLlib Guide](https://spark.apache.org/docs/latest/ml-guide.html)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Next Step
# MAGIC 
# MAGIC [ML Workflows]($./04-ML-Workflows)

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2019 Databricks, Inc. All rights reserved.<br/>
# MAGIC Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="http://www.apache.org/">Apache Software Foundation</a>.<br/>
# MAGIC <br/>
# MAGIC <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="http://help.databricks.com/">Support</a>