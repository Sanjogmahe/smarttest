import pandas as pd
import xlsxwriter
import ctypes  # An included library with Python install.
def Mbox(text, title='Smart Test', style=0):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


## SmarTest using test Prioritization Method
## Reading The Data file
Mbox("Reading The Data file..!")
dataset = pd.read_excel('SampleTestData1.xlsx')

## Extracting The release ID
unique_release = dataset['Release ID'].unique()

# Fetching total test count from the data
total_num_test = dataset['ID'].count()
print("Total number of Test Cases =", total_num_test)
Mbox("Total number of Test Cases "+ str(total_num_test))

#Assigning all input variables
Mbox("Assigning all input variables..!")
release = dataset['Release ID']
test_id = dataset['ID']
test_case_title = dataset['Test Case Title ']
t_priority = dataset['Test Case Priority']
n_defects = dataset['Linked Defects']
e_pron_test = dataset['Error Prone Test case']
s_defects = dataset['Severity of Defects']
automation_script_name = dataset['Automation Script Name']
# print(release)

## Selecting latest release=7.1

current_release = 7.1
Mbox("Selecting Latest Release "+str(current_release))

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

##Processing of data is based on the test case priority, linked defects and error prone nature of the test cases
Mbox("Taking the combinations for the input paramenters such as test priority, severity, defect linked, error pron")
for t_id,tc_title,rel,t_pri, n_def, e_p_test,s_def,a_script_name in \
        zip(test_id,test_case_title,release,t_priority, n_defects, e_pron_test,s_defects,automation_script_name):

#Process the data the latest(nth) release
#Generate the prioritsed test case list based on relevant condition.

    if rel == current_release:
        count += 1
        if t_pri == 'P0' or t_pri == 'P1' and n_def >= 0 and e_p_test == 'Yes' and s_def in ('High', 'Medium'):
            current_release_P0_P1.append((t_id, tc_title, a_script_name))
        if t_pri == 'P2' or t_pri == 'P3' and n_def >= 2 and e_p_test == 'Yes' and s_def == 'High':
            current_release_P2_P3.append((t_id, tc_title, a_script_name))

##Process the data for remaining releases and generate the prioritised test case list

    if rel != current_release:
        if t_pri == 'P0' or t_pri == 'P1' and n_def >= 0 and e_p_test == 'Yes' and s_def in ('High', 'Medium'):
            previous_releases_P0_P1.append((t_id, tc_title, a_script_name))
        if t_pri == 'P2' or t_pri == 'P3' and n_def >= 2 and e_p_test == 'Yes' and s_def == 'High':
            previous_releases_P2_P3.append((t_id, tc_title, a_script_name))

## Displaying the various test case count in each section.

print("Total number of current release test cases =", count)
Mbox("Total number of current release test cases "+ str(count))
print("Current release P0, P1 test case count =", len(current_release_P0_P1))
Mbox("Current release P0, P1 test case count "+ str(len(current_release_P0_P1)))
print("Current release P2, P3 test case count =", len(current_release_P2_P3))
Mbox("Current release P2, P3 test case count "+ str(len(current_release_P2_P3)))
print("Previous releases P0, P1 test case count =", len(previous_releases_P0_P1))
Mbox("Previous releases P0, P1 test case count "+ str(len(previous_releases_P0_P1)))
print("Previous releases P2, P3 test case count =", len(previous_releases_P2_P3))
Mbox("Previous releases P2, P3 test case count "+ str(len(previous_releases_P2_P3)))


#Removing duplicates test cases from the list.

unique_test_titles = set(current_release_P0_P1+current_release_P2_P3)
##unique_test_titles = set(P0+P1+P2+P3)
#print("unique test case title",len(unique_test_titles))


#If the processed data for (n-1) releases is more, then we can limit the test case count and most recent release and
# higher priority test cases will be executed first.
if number_test_cases_current_release >= len(unique_test_titles):
    l = number_test_cases_current_release - len(unique_test_titles)
    # print("l",l)
    previous_releases_P0_P1 = set(previous_releases_P0_P1)
    # print(list(P2))
    previous_releases_P0_P1 = list(previous_releases_P0_P1)[:l]
    # print(len(P2))
    unique_test_titles = set(current_release_P0_P1+current_release_P2_P3+previous_releases_P0_P1)

##Final test case count
print("Total unique test cases", len(unique_test_titles))
Mbox("Total unique test cases "+ str(len(unique_test_titles)))

from datetime import datetime
now = datetime.now()
timestamp = str(now.strftime("%Y%m%d_%H-%M-%S"))



Mbox("Writing Output in Excel workbook..!")
###Final output : No of TCS for regression testing send to excel
final_output_file = 'FinalOutput_'+timestamp+'.xlsx'
writer = pd.ExcelWriter(final_output_file, engine='xlsxwriter')

pd.DataFrame(unique_test_titles, columns=["Test ID", "Test case Title", "Automation Script Name"]).to_excel(writer,
                                                                                  sheet_name="Master_Output",
                                                                                  index=False)

# Exctracting information of automation scripts name and manual test case names
df = pd.DataFrame(unique_test_titles)
m_tc = []
a_tc = []
for i in range(len(df[1])):
    if df[2][i] == "Manual Test Case":
        m_tc.append(( df[0][i], df[1][i]))
    else:
        a_tc.append(df[2][i])

pd.DataFrame(a_tc, columns=["Automation Script Name"]).to_excel(writer, sheet_name="Automation_Scripts", index=True, index_label='S.No.')
pd.DataFrame(m_tc, columns=["Test ID", "Manual Test Case"]).to_excel(writer, sheet_name="Manual_TC", index=True, index_label='S.No.')
writer.save()
Mbox("Output Excel Generated with Master Output, Automation Scripts and Manual TC sheets in "+final_output_file)