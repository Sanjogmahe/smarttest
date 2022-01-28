import pandas as pd
import xlsxwriter
import ctypes  # An included library with Python install.

def Mbox(text, title='Smart Test', style=0):
    # return ctypes.windll.user32.MessageBoxW(0, text, title, style)
    return 1

## SmarTest using test Prioritization Method
## Reading The Data file
Mbox("The master file is ready for execution..!")
# dataset = pd.read_excel('SampleTestData.xlsx')
dataset = pd.read_excel('TestData _MasterInput_0.3.xlsx')

modules = input("Insert Selected Modules or leave it blank : ") #['TNT', 'CFE']
modules = modules.split(sep=',')
if modules != '':
    dataset = dataset[dataset.Module.isin(modules)]

## Extracting The release ID
unique_release = dataset['Release ID'].unique()

# Fetching total test count from the data
total_num_test = dataset['ID'].count()
print("Total number of Test Cases =", total_num_test)
Mbox("Test cases available in master sheet is " + str(total_num_test))

#Assigning all input variables
#Mbox("Assigning all input variables..!")
release = dataset['Release ID']
test_id = dataset['ID']
test_case_title = dataset['Test Case Title ']
t_priority = dataset['Test Case Priority']
n_defects = dataset['Linked Defects']
e_pron_test = dataset['Error Prone Test case']
s_defects = dataset['Severity of Defects']
automation_script_name = dataset['Automation script']
module = dataset['Module']
# print(release)

## Selecting latest release=7.1

current_release = 8.2
Mbox("Filtering test cases from current release - rls.ver.: "+str(current_release))

## Initialising the output dataset
## For identifiying the prioritised test cases, we are applying some combination on the input data ,for selection of TCs.
current_release_P0_P1 = []
current_release_P2_P3 = []
previous_releases_P0_P1 = []
previous_releases_P2_P3 = []
## Identified test cases for Regression count initialising with 0
count = 0

## Setting the test case count limit, if required.
number_test_cases_current_release = 600
if number_test_cases_current_release == 0:
    number_test_cases_current_release = total_num_test

##Processing of data is based on the test case priority, linked defects and error prone nature of the test cases
#Mbox("Taking the combinations for the input paramenters such as test priority, severity, defect linked, error pron")
for t_id,tc_title,rel,t_pri, n_def, e_p_test,s_def,a_script_name,mod in \
        zip(test_id,test_case_title,release,t_priority, n_defects, e_pron_test,s_defects,automation_script_name,module):

#Process the data the latest(nth) release
#Generate the prioritsed test case list based on relevant condition.

    if rel == current_release:
        count += 1
        if t_pri == 'P0' or t_pri == 'P1' and n_def >= 0 and e_p_test == 'Yes' and s_def in ('High', 'Medium'):
            current_release_P0_P1.append((t_id, tc_title, a_script_name, t_pri, n_def, s_def, mod))
        if t_pri == 'P2' or t_pri == 'P3' and n_def >= 2 and e_p_test == 'Yes' and s_def == 'High':
            current_release_P2_P3.append((t_id, tc_title, a_script_name, t_pri, n_def, s_def, mod))

##Process the data for remaining releases and generate the prioritised test case list

    if rel != current_release:
        if t_pri == 'P0' or t_pri == 'P1' and n_def >= 0 and e_p_test == 'Yes' and s_def in ('High', 'Medium'):
            previous_releases_P0_P1.append((t_id, tc_title, a_script_name, t_pri, n_def, s_def, mod))
        if t_pri == 'P2' or t_pri == 'P3' and n_def >= 2 and e_p_test == 'Yes' and s_def == 'High':
            previous_releases_P2_P3.append((t_id, tc_title, a_script_name, t_pri, n_def, s_def, mod))

## Displaying the various test case count in each section.

print("Total number of current release test cases =", count)
Mbox("Current release test cases - "+ str(count))
print("Current release P0, P1 test case count =", len(current_release_P0_P1))
print("Current release P2, P3 test case count =", len(current_release_P2_P3))
Mbox("Filtering test cases from previous releases")
Mbox("Previous release test cases - " + str(total_num_test-count))
print("Previous releases P0, P1 test case count =", len(previous_releases_P0_P1))
print("Previous releases P2, P3 test case count =", len(previous_releases_P2_P3))


#Removing duplicates test cases from the list.

unique_test_titles = set(current_release_P0_P1+current_release_P2_P3)

#If the processed data for (n-1) releases is more, then we can limit the test case count and most recent release and
# higher priority test cases will be executed first.
master_dataframe = pd.DataFrame()


if number_test_cases_current_release >= len(unique_test_titles):
    l = number_test_cases_current_release - len(unique_test_titles)
    previous_releases_P0_P1 = set(previous_releases_P0_P1)
    previous_releases_P0_P1 = list(previous_releases_P0_P1)[:l]
    unique_test_titles = set(current_release_P0_P1+current_release_P2_P3+previous_releases_P0_P1)

#Duplicate test case removed
master_dataframe = pd.DataFrame(unique_test_titles).drop_duplicates([0])
master_dataframe.reset_index(inplace=True)


##Final test case count
print("Total unique test cases", len(master_dataframe))
Mbox("Prioritized test case count - " + str(len(master_dataframe)))

from datetime import datetime
now = datetime.now()
timestamp = str(now.strftime("%Y%m%d_%H-%M-%S"))
date =  str(now.strftime("%Y%m%d"))

#creating output folder as per the today's date
import os
output_folder = '../'+'output_'+date
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Mbox("Writing Output in Excel workbook..!")
###Final output : No of TCS for regression testing send to excel
final_output_file = output_folder + '/FinalOutput_'+timestamp+'.xlsx'
writer = pd.ExcelWriter(final_output_file, engine='xlsxwriter')

all_tc = []
all_info_tc = []
for i in range(len(master_dataframe[1])):
    # if df[2][i] == "Manual Test Case":
        all_tc.append((master_dataframe[0][i], master_dataframe[1][i], master_dataframe[2][i], master_dataframe[6][i]))
        all_info_tc.append((master_dataframe[0][i], master_dataframe[1][i], master_dataframe[2][i],
                            master_dataframe[3][i], master_dataframe[4][i], master_dataframe[5][i],
                            master_dataframe[6][i]))

limit = int(input("Insert the Limit: "))

if limit == 0:
    pd.DataFrame(all_tc, columns=["Test ID", "Test case Title", "Automation Script Name", 'Module']).to_excel(writer,
                                                                                  sheet_name="Master_Output",
                                                                                  index=False)
else:
    limited_test = pd.DataFrame(all_info_tc, columns=["Test ID", "Test case Title", "Automation Script Name","Test Priority",
                                               "Linked Defects", "Severity Defects", 'Module'])
    master = limited_test.sort_values(by=["Test Priority",  "Severity Defects","Linked Defects"], ignore_index=False)
    final = []
    for i in range(len(master["Test ID"])):
        final.append((master["Test ID"][i], master["Test case Title"][i],master["Automation Script Name"][i], master['module'])[i])
    master_dataframe = pd.DataFrame(final, columns=["Test ID", "Test case Title", "Automation Script Name",'Module'])
    master_dataframe = master_dataframe.head(limit)
    master_dataframe.to_excel(writer, sheet_name="Master_Output",index=False)


df = master_dataframe
m_tc = []
a_tc = []
if limit == 0:
    for i in range(len(df[0])):
        if df[2][i] == "Manual Testing":
            m_tc.append((df[0][i], df[1][i], df[6][i]))
        else:
            a_tc.append((df[2][i], df[6][i]))
else:
    for i in range(len(df['Test ID'])):
        if df['Automation Script Name'][i] == "Manual Testing":
            m_tc.append((df['Test ID'][i], df['Test case Title'][i], df['Module'][i]))
        else:
            a_tc.append(df['Automation Script Name'][i], df['Module'][i])

df_auto = pd.DataFrame(set(a_tc), columns=["Automation Script Name", "Module"])
df_auto.index += 1
df_auto.index.name="S.No."
df_auto.to_excel(writer, sheet_name="Automation_Scripts")
df_manual = pd.DataFrame(m_tc, columns=["Test ID", "Manual Test Case", "Module"])
df_manual.index += 1
df_manual.index.name = "S.No."
df_manual.to_excel(writer, sheet_name="Manual_TC")

writer.save()
# Mbox("Output Excel Generated with Master Output, Automation Scripts and Manual TC sheets in "+final_output_file)