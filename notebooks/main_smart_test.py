# importing required libraries
import pandas as pd
import evalml



# dataset = pd.read_excel('TestData _MasterInput_0.4 - Copy.xlsx')
# dataset = pd.read_excel('test8.2.xltx')
# dataset = dataset.tail(60)
# dataset = pd.read_excel('SampleTestData V0.2 113.xlsx')
# dataset = pd.read_excel('Dummy Dataset0.3.xlsx')
# dataset = pd.read_excel('SDMaster_input_Sheet.xlsx')
dataset = pd.read_excel('SDMaster_input_Sheet2022_03_16_Train.xlsx')
final = dataset

# pred_data = pd.read_excel('InputSheet_Train_latest.xlsx')

from sklearn.preprocessing import LabelEncoder, OneHotEncoder

labelencoder = LabelEncoder()
dataset['Release ID'] = labelencoder.fit_transform(dataset['Release ID'].astype(str))
# pred_data['Release ID'] = labelencoder.fit_transform(pred_data['Release ID'].astype(str))
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
dataset=dataset.drop(['index','Target','Test Case Title'],axis=1)
# pred_data=pred_data.drop(['Test Case Title'], axis=1)
#Creating new data frame with all categorical feature and Text features for training classifier models
X=pd.concat([dataset,text_vectors_df],axis=1).values
print("**Dimension for features data frame are {}**".format(X.shape))


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

# Prediction Data Prepration

pred_data = pd.read_excel('SDMaster_input_Sheet2022_03_16_10_Test.xlsx')
# pred_data['Release ID'] = labelencoder.transform(pred_data['Release ID'].astype(str))


pred_corpus_title = []
# pstem = PorterStemmer()
for i in range(pred_data['Test Case Title'].shape[0]):
    # Remove unwanted words
    text = re.sub("[^a-zA-Z]", ' ', pred_data['Test Case Title'][i])
    # Transform words to lowercase
    text = text.lower()
    text = text.split()
    # Remove stopwords then Stemming it
    text = [pstem.stem(word) for word in text if not word in set(stopwords.words('english'))]
    text = ' '.join(text)
    # Append cleaned tweet to corpus
    pred_corpus_title.append(text)

print("**Prediction Corpus created successfully**")


pred_text_vectors= cv.transform(pred_corpus_title).toarray()

#Convert text vectors into data frame
pred_text_vectors_df=pd.DataFrame(pred_text_vectors)
print("**Dimension for Prediction Text features are {}**".format(pred_text_vectors_df.shape))

#Removing 'Target' and 'TestCaseTitle' columns from actual dataset
pred_data=pred_data.drop(['Test Case Title'], axis=1)
#Creating new data frame with all categorical feature and Text features for training classifier models
pred_X=pd.concat([pred_data,pred_text_vectors_df],axis=1).values
print("**Dimension for pred features data frame are {}**".format(pred_X.shape))

#MOdel Saving
best_pipeline.save("model.pkl")
# loading the model saved in pickel file
# check_model = automl.load('model.pkl')
# check_model.predict_proba(pred_X)


y_pred = best_pipeline.predict(pred_X)

#writing file temporary format
output = pd.DataFrame(y_pred)
output.rename(columns={1:'Target'},inplace=True)
# output = pd.concat([dataset1[dataset1.ID.isin(pd.DataFrame(X_test)[1])], output], axis=1)
output = pd.concat([pd.DataFrame(X)[[0,4,5]],output], axis=1)

output.dropna(inplace=True)
output.drop_duplicates(subset=[0], inplace=True)
output.rename(columns={0:'ID',4:"Modules",5:"Scripts",'Target':"Target"},inplace=True)
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
