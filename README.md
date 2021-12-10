# Python for Data Analysis - Project-Drug Consumption
*LEDUC Bastien - LE CHEVALIER Jean - LE FOCH Pierrick*

# Python for data analysis - Drug Consumption Data set

As part of our Data Science curriculum at ESILV, the Python for Data Analysis course is offered to broaden our knowledge of the well-known Python language, to help us discover and deepen all the possibilities it offers. From data processing to data visualization through machine learning, the final project pushes teams of 3 students to understand the stakes of manipulating a data set. 
We are Jean Le Chevalier, Pierrick Le Floch and Bastien Leduc and together we explored the [Drug Consumption Data Set](https://archive.ics.uci.edu/ml/datasets/Drug+consumption+%28quantified%29) from UCI Machine Learning repository. 
The data set is derived from an online survey conducted between 2011 and 2012 with 1,885 respondents (number of rows) aged 18 and over from English-speaking countries.
This survey collected personality characteristics and demographic information (input variables), as well as their legal and illegal drug use (target variables).

Our strategy is broken down into the following steps:
- **Data set analysis**
Finding out what its stake, how the data was collected, what are the input variables and the target variables types and shape.
- **Data processing**
Finding out which variables are biased and therefore need to be removed, which interesting correlations can be observed from the start. 
- **Modeling**
Creating a multi-output classifier, i.e. a model that predicts combinations of classes (here, combinations of drug use).
Transforming the problem into a binary classification prediction.
- **Interpreting**
Use of an XAI (EXplainable AI) library, allowing us to understand the decision process of the model, and to explain why it predicts such or such class
- **Presenting results**
Creation of the showcase of our project, which presents some data visualization graphs and a form to make predictions according to the binary classification model.

To quickly summarize our results (more details can be found in the notebook and the PowerPoint):

**For the data processing part:**
We removed the following variables:
"Country" because it is very unequally represented (more than a thousand individuals in the UK against about fifty individuals in other countries)
"Gender" because the data set presents more men than women, which does not reflect reality.
"Ethnicity" because the data set is also very unevenly represented (more than 80% "white" people).
We also removed the individuals who claimed to use "Semeron", a fictitious drug inserted in the questionnaire to 'trap' liars. There are only 8/1880=0.4% of them in the data set. We observed that these individuals gave exaggerated answers to the survey which could therefore create a bias.

**For the Modeling part:**
With the implementation of the multi-output classifier model having to answer the problem "Which drugs has the individual with the characteristics X consumed recently", we obtained a very low precision (around 10%). We tried to enter by hand individuals with "extreme characteristics" whose prediction is supposed to be obvious, but the results were very close to those of a "normal" individual. These inequalities in the predictions could be due to the fact that the data set is very small, so the model lacks a lot of information to perform such a powerful algorithm.

We therefore turned to a binary classification problem:
Predict whether or not an individual has used an illegal drug in the past 30 days. We tested many algorithms, the most accurate being Logistic Regression which delivers accuracies close to 80%.

**For the presentation part :**
This is the model we implemented in our Django application, in the form of a form (Bootstrap) to fill out.
To be able to run the api: download the "drugConsumption" folder, open your Anaconda Prompt (or any python supported cmd ) and go to the drugConsumption folder (cd .\drugConsumption) then enter **python manage.py runserver**, wait about fifteen seconds and copy the localhost link (like http://127.0.0.1:8000/) in your browser. 

Enjoy our project !

