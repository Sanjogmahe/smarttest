# importing required libraries
import pandas as pd
import evalml



# dataset = pd.read_excel('TestData _MasterInput_0.4 - Copy.xlsx')
# dataset = pd.read_excel('test8.2.xltx')
# dataset = dataset.tail(60)
# dataset = pd.read_excel('SampleTestData V0.2 113.xlsx')
# dataset = pd.read_excel('Dummy Dataset0.3.xlsx')
# dataset = pd.read_excel('SDMaster_input_Sheet.xlsx')
dataset = pd.read_excel('SDMaster_input_Sheet_f.xlsx')
final = dataset


from sklearn.preprocessing import LabelEncoder, OneHotEncoder

labelencoder = LabelEncoder()
dataset['Release ID'] = labelencoder.fit_transform(dataset['Release ID'].astype(str))

dataset.head()
dataset.reset_index(inplace=True)


import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
# nltk.download('stopwords')

corpus_title = []
pstem = PorterStemmer()
for i in range(dataset['Test Case Title'].shape[0]):
    # Remove unwanted words
    text = re.sub("[^a-zA-Z]", ' ', dataset['Test Case Title'][i])
    # Transform words to lowercase
    text = text.lower()
    text = text.split()
    # Remove stopwords then Stemming it
    text = [pstem.stem(word) for word in text if not word in set(stopwords.words('english'))]
    text = ' '.join(text)
    # Append cleaned tweet to corpus
    corpus_title.append(text)

print("**Corpus created successfully**")

# Creating the Bag of Words model
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
text_vectors= cv.fit_transform(corpus_title).toarray()

#Convert text vectors into data frame
text_vectors_df=pd.DataFrame(text_vectors)
print("**Dimension for Text features are {}**".format(text_vectors_df.shape))

#Getting Target variable into Y variable
y=dataset[['Target']].values
#Converting 2 dimensional y and y_pred array into single dimension
y=y.ravel()

#Removing 'Target' and 'TestCaseTitle' columns from actual dataset
dataset=dataset.drop(['Target','Test Case Title'],axis=1)

#Creating new data frame with all categorical feature and Text features for training classifier models
X=pd.concat([dataset,text_vectors_df],axis=1).values
print("**Dimension for features data frame are {}**".format(X.shape))
#X.head()

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)
X_train, X_test, y_train, y_test = evalml.preprocessing.split_data(X, y, problem_type='binary', test_size=0.2, random_seed=0)
final_data = X_test
# EvalMl code

automl = evalml.automl.AutoMLSearch(X_train=X_train, y_train=y_train, problem_type='binary',verbose=True,max_batches=1,
                                    allowed_model_families=["XGBOOST"])
automl.search()

from evalml.model_understanding.graphs import confusion_matrix
import pickle


best_pipeline = automl.best_pipeline
automl.describe_pipeline(automl.rankings.iloc[0]["id"])

scores = best_pipeline.score(X_test, y_test,  objectives=evalml.objectives.get_core_objectives('binary'))


# print(f'Accuracy Binary: {scores["Accuracy Binary"]}')

y_pred = best_pipeline.predict(X)

#writing file temporary format
output = pd.DataFrame(y_pred)
output.rename(columns={1:'Target'},inplace=True)
# output = pd.concat([dataset1[dataset1.ID.isin(pd.DataFrame(X_test)[1])], output], axis=1)
output = pd.concat([pd.DataFrame(X)[[1,7,9]],output], axis=1)

output.dropna(inplace=True)
output.drop_duplicates(subset=[1], inplace=True)
output.rename(columns={1:'ID',7:"Modules",9:"Scripts",'Target':"Target"},inplace=True)
master_dataframe = output
# master_dataframe = master_dataframe.astype({"ID": int})

master_dataframe = pd.merge(left=final[['ID', 'Test Case Title']], right=master_dataframe, how='right', left_on='ID', right_on='ID')
master_dataframe.drop_duplicates(subset=['ID'], inplace=True)
delete_row = master_dataframe[master_dataframe["Target"]==0].index
master_dataframe = master_dataframe.drop(delete_row)

#Final format

from datetime import datetime
now = datetime.now()
timestamp = str(now.strftime("%Y%m%d_%H-%M-%S"))
date = str(now.strftime("%Y%m%d"))

#creating output folder as per the today's date
import os
output_folder = '../'+'output_'+date
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


###Final output : No of TCS for regression testing send to excel
final_output_file = output_folder + '/FinalOutput_'+timestamp+'.xlsx'
writer = pd.ExcelWriter(final_output_file, engine='xlsxwriter')


pd.DataFrame(master_dataframe.iloc[:, 0:3]).to_excel(writer,
    sheet_name="Master_Output",
    index=False)

df = master_dataframe
m_tc = []
a_tc = []
# if limit == 0:
for i in range(len(df.iloc[:,0])):
    if df.iloc[i,3] == "Manual Testing":
        m_tc.append((df.iloc[i,0], df.iloc[i,1], df.iloc[i,2]))
        # m_tc.append((df.iloc[i,0], df.iloc[i,1]))
    else:
        a_tc.append((df.iloc[i,2], df.iloc[i,3]))
        # a_tc.append((df.iloc[i,1], df.iloc[i,2]))


df_auto = pd.DataFrame(set(a_tc), columns=["Module", "Automation Script Name"])
df_auto.drop_duplicates(subset=["Automation Script Name"],inplace=True)
df_auto.index += 1
df_auto.index.name="S.No."
df_auto.to_excel(writer, sheet_name="Automation_Scripts")
df_manual = pd.DataFrame(m_tc, columns=["Test ID","Test Case Title", "Module"])
# df_manual = pd.DataFrame(m_tc, columns=["Test ID","Module"])
df_manual.index += 1
df_manual.index.name = "S.No."
df_manual.to_excel(writer, sheet_name="Manual_TC")

writer.save()










# Fitting Logistic Regression to the Training set
# from sklearn.linear_model import LogisticRegression
# from sklearn.metrics import confusion_matrix
# classifier_lr = LogisticRegression(solver='liblinear')
# classifier_lr.fit(X_train,y_train)
# # Predicting the Test set results
# y_pred_lr = classifier_lr.predict(X_test)
# # Making the Confusion Matrix
# cm_lr = confusion_matrix(y_test, y_pred_lr)
#
# from sklearn.naive_bayes import GaussianNB
#
# from sklearn.metrics import f1_score
#
# # Fitting Gausian to the Training set
# classifier_gnb = GaussianNB()
# classifier_gnb.fit(X_train, y_train)
# # Predicting the Test set results
# y_pred_gnb = classifier_gnb.predict(X_test)
# # Making the Confusion Matrix
# cm_gnb = confusion_matrix(y_test, y_pred_gnb)
#
# #print(y_pred_gnb)
# #print(X_test)
# output = pd.DataFrame(y_pred_gnb)
# output = pd.concat([pd.DataFrame(X_test), output], axis=1)
# output=output[1]
#
#
# #print(output)
# output.to_csv('output.csv')
# output_read = pd.read_csv('output.csv')
#
# from sklearn.naive_bayes import MultinomialNB
# # Fitting Naive Bayes to the Training set
# classifier_nb = MultinomialNB(alpha=0.1)
# classifier_nb.fit(X_train, y_train)
# # Predicting the Test set results
# y_pred_nb = classifier_gnb.predict(X_test)
# # Making the Confusion Matrix
# cm_nb = confusion_matrix(y_test, y_pred_nb)
#
# #Calculating Model Accuracy
# print('**Regression Classifier Accuracy Score is {} for Train Data Set**'.format(classifier_lr.score(X_train, y_train)))
# print('**Regression Classifier Accuracy Score is {} for Test Data Set**'.format(classifier_lr.score(X_test, y_test)))
# print('**Regression Classifier F1 Score is {}**'.format(f1_score(y_test, y_pred_lr)))
# print('**Confusion Matrix for Regression Classifer {}**'.format(cm_lr))
# print('**--------------------------------------------------------------------------------**')
# print('**GaussianNB Classifier Accuracy Score is {} for Train Data Set**'.format(classifier_gnb.score(X_train, y_train)))
# print('**GaussianNB Classifier Accuracy Score is {} for Test Data Set**'.format(classifier_gnb.score(X_test, y_test)))
# print('**GaussianNB Classifier F1 Score is {}**'.format(f1_score(y_test, y_pred_gnb)))
# print('**Confusion Matrix for GaussianNB Classifer {}**'.format(cm_gnb))
# print('**--------------------------------------------------------------------------------**')
# print('**MultinomialNB Classifier Accuracy Score is {} for Train Data Set**'.format(classifier_nb.score(X_train, y_train)))
# print('**MultinomialNB Classifier Accuracy Score is {} for Test Data Set**'.format(classifier_nb.score(X_test, y_test)))
# print('**MultinomialNB Classifier F1 Score is {}**'.format(f1_score(y_test, y_pred_nb)))
# print('**Confusion Matrix for MultinomialNB Classifer {}**'.format(cm_nb))
#
# from sklearn.tree import DecisionTreeClassifier
# # Fitting Decision Tree to the Training set
# classifier_dt = DecisionTreeClassifier()
# classifier_dt.fit(X_train, y_train)
# # Predicting the Test set results
# y_pred_dt = classifier_dt.predict(X_test)
# # Making the Confusion Matrix
# cm_dt = confusion_matrix(y_test, y_pred_dt)
# print('**--------------------------------------------------------------------------------**')
# print('**DecisionTree Classifier Accuracy Score is {} for Train Data Set**'.format(classifier_dt.score(X_train, y_train)))
# print('**DecisionTree Classifier Accuracy Score is {} for Test Data Set**'.format(classifier_dt.score(X_test, y_test)))
# print('**DecisionTree Classifier F1 Score is {}**'.format(f1_score(y_test, y_pred_dt)))
# print('**Confusion Matrix for DecisionTree Classifer {}**'.format(cm_dt))
#
# from sklearn.ensemble import GradientBoostingClassifier
# # Fitting Gradient Boosting Model to the Training set
# classifier_gb = GradientBoostingClassifier()
# classifier_gb.fit(X_train, y_train)
# # Predicting the Test set results
# y_pred_gb = classifier_gb.predict(X_test)
# # Making the Confusion Matrix
# cm_gb = confusion_matrix(y_test, y_pred_gb)
# print('**--------------------------------------------------------------------------------**')
# print('**GradientBoosting Classifier Accuracy Score is {} for Train Data Set**'.format(classifier_gb.score(X_train, y_train)))
# print('**GradientBoosting Classifier Accuracy Score is {} for Test Data Set**'.format(classifier_gb.score(X_test, y_test)))
# print('**GradientBoosting Classifier F1 Score is {}**'.format(f1_score(y_test, y_pred_gb)))
# print('**Confusion Matrix for GradientBoosting Classifer {}**'.format(cm_gb))
#
# from sklearn.neighbors import KNeighborsClassifier
# # Fitting K-Nearest Neighbors Model Model to the Training set
# classifier_kn = KNeighborsClassifier()
# classifier_kn.fit(X_train, y_train)
# # Predicting the Test set results
# y_pred_kn = classifier_kn.predict(X_test)
# # Making the Confusion Matrix
# cm_kn = confusion_matrix(y_test, y_pred_kn)
# print('**--------------------------------------------------------------------------------**')
# print('**KNearestNeighbors Classifier Accuracy Score is {} for Train Data Set**'.format(classifier_kn.score(X_train, y_train)))
# print('**KNearestNeighbors Classifier Accuracy Score is {} for Test Data Set**'.format(classifier_kn.score(X_test, y_test)))
# print('**KNearestNeighbors Classifier F1 Score is {}**'.format(f1_score(y_test, y_pred_kn)))
# print('**Confusion Matrix for KNearestNeighbors Classifer {}**'.format(cm_kn))
#
# from sklearn.ensemble import RandomForestClassifier
# # Fitting RandomForest Model to the Training set
# classifier_rf = RandomForestClassifier()
# classifier_rf.fit(X_train, y_train)
# # Predicting the Test set results
# y_pred_rf = classifier_rf.predict(X_test)
# # Making the Confusion Matrix
# cm_rf = confusion_matrix(y_test, y_pred_rf)
# print('**--------------------------------------------------------------------------------**')
# print('**RandomForest Classifier Accuracy Score is {} for Train Data Set**'.format(classifier_rf.score(X_train, y_train)))
# print('**RandomForest Classifier Accuracy Score is {} for Test Data Set**'.format(classifier_rf.score(X_test, y_test)))
# print('**RandomForest Classifier F1 Score is {}**'.format(f1_score(y_test, y_pred_rf)))
# print('**Confusion Matrix for RandomForest Classifer {}**'.format(cm_rf))
#
