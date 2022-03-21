# import pandas as pd
# output_read = pd.read_csv('notebooks/output.csv')

# test cases run
from datetime import date
from common_function import url, iframe, justCli, hover, clear, justEnt, quit, default_iframe, CancelAlert, wait, ewait

url("https://jmp.allianz.net/secure/RapidBoard.jspa?rapidView=1714")
ewait(4)
justEnt("//input[@id='login-form-username']","extern.maheshwari_sanjog@allianz.de")
justEnt("//input[@id='login-form-password']","mulberry2@")
justCli("//input[@id='login-form-submit']")
ewait(30)
# input("Insert Any Key..")
# url("https://jmp.allianz.net/browse/AZA-116972?jql=project%20%3D%20%22ABS%20Sahara%20%22")
yrl = "https://jmp.allianz.net/browse/AZA-114965?jql=project%20%3D%20%22ABS%20Sahara%20%22%20AND%20fixVersion%20in%20(%22Release%20"+str(20)+"%22)%20AND%20type%20not%20in%20(Task%2CEpic%2CTest%2CSub-task)%20AND%20status%20not%20in%20(Descoped)"
# print(yrl)
url(yrl)
ewait(2)

##Bugs
for i in range(16,20):

    clear("//textarea[@id='advanced-search']")
    ewait(1)
    justEnt("//textarea[@id='advanced-search']","project = \"ABS Sahara \" AND fixVersion in (\"Release "+str(i)+"\") AND type not in (Story,Task,Epic,Test,Sub-task,\"Incident-SNOW \",\"Incident (Sub-task)\",Incident) AND status not in (Descoped)")
    ewait(1)
    justCli("//button[contains(text(),'Search')]")
    ewait(4)

    justCli("//button[@id='AJS_DROPDOWN__81']")
    ewait(2)
    justCli("//a[@id='allExcelFields']")
    ewait(2)
    # justCli("//button[@id='csv-export-dialog-export-button']")
    ewait(35)


##Story
for i in range(16,20):

    clear("//textarea[@id='advanced-search']")
    ewait(1)
    justEnt("//textarea[@id='advanced-search']","project = \"ABS Sahara \" AND fixVersion in (\"Release "+str(i)+"\") AND type not in (Bug,Task,Epic,Test,Sub-task,\"Incident-SNOW \",\"Incident (Sub-task)\",Incident) AND status not in (Descoped)")
    ewait(1)
    justCli("//button[contains(text(),'Search')]")
    ewait(4)

    justCli("//button[@id='AJS_DROPDOWN__81']")
    ewait(2)
    justCli("//a[@id='allExcelFields']")
    ewait(2)
    # justCli("//button[@id='csv-export-dialog-export-button']")
    ewait(35)
# quit()

# execution summary
# justCli("//a[@id='aui-responsive-header-dropdown-0-trigger']")
start_dates = ['01/Jun/21', '01/Jul/21', '01/Aug/21', '01/Sep/21', '01/Oct/21', '01/Nov/21', '01/Dec/21', '01/Jan/22']
end_dates = ['30/Jun/21', '31/Jul/21', '31/Aug/21', '30/Sep/21', '31/Oct/21', '30/Nov/21', '31/Dec/21', '31/Jan/22']

for i, j in zip(start_dates, end_dates):

        justCli("//a[contains(text(),'Tests')]")
        ewait(3)
        justCli("//button[@id='ktm-module-report']")
        ewait(3)
        justCli("//span[contains(text(),'Test Execution')]")
        ewait(3)
        justCli("//a[contains(text(),'Test execution results (list)')]")
        ewait(3)
        clear("//body/div[@id='page']/div[@id='content']/div[1]/div[1]/reports-form[1]/div[1]/div[2]/div[1]/section[1]/reports-filters[1]/div[1]/reports-form-section[1]/div[1]/div[1]/reports-filter-none-condition[1]/div[1]/reports-form-section[1]/div[1]/div[1]/reports-form-box[1]/div[1]/reports-filter-by-date[1]/div[1]/reports-filter-by-date-between[1]/div[1]/aui-date-picker[1]/input[1]")
        ewait(1)
        justEnt("//body/div[@id='page']/div[@id='content']/div[1]/div[1]/reports-form[1]/div[1]/div[2]/div[1]/section[1]/reports-filters[1]/div[1]/reports-form-section[1]/div[1]/div[1]/reports-filter-none-condition[1]/div[1]/reports-form-section[1]/div[1]/div[1]/reports-form-box[1]/div[1]/reports-filter-by-date[1]/div[1]/reports-filter-by-date-between[1]/div[1]/aui-date-picker[1]/input[1]",
                i)
        ewait(1)
        clear("//body/div[@id='page']/div[@id='content']/div[1]/div[1]/reports-form[1]/div[1]/div[2]/div[1]/section[1]/reports-filters[1]/div[1]/reports-form-section[1]/div[1]/div[1]/reports-filter-none-condition[1]/div[1]/reports-form-section[1]/div[1]/div[1]/reports-form-box[1]/div[1]/reports-filter-by-date[1]/div[1]/reports-filter-by-date-between[1]/div[2]/aui-date-picker[1]/input[1]")
        ewait(1)
        justEnt("//body/div[@id='page']/div[@id='content']/div[1]/div[1]/reports-form[1]/div[1]/div[2]/div[1]/section[1]/reports-filters[1]/div[1]/reports-form-section[1]/div[1]/div[1]/reports-filter-none-condition[1]/div[1]/reports-form-section[1]/div[1]/div[1]/reports-form-box[1]/div[1]/reports-filter-by-date[1]/div[1]/reports-filter-by-date-between[1]/div[2]/aui-date-picker[1]/input[1]",
                j)
        ewait(1)
        justCli("//input[@id='allTestResults']")
        ewait(3)
        justCli("//button[contains(text(),'Generate')]")
        ewait(3)
        justCli("//body/div[@id='page']/div[@id='content']/div[1]/div[1]/reports-view[1]/reports-view-actions[1]/div[1]/div[1]/reports-data-set-export[1]/button[1]")
        ewait(3)
        justCli("//a[contains(text(),'Excel (dataset)')]")
        ewait(100)

# for i in range(len(output_read['Test Case Title '])):
#     j = output_read['Test Case Title '][i]
#     today = date.today()
#     d1 = today.strftime("%m/%d/%Y")
#
#     url("https://www.google.com/")
#     # url("https://www.google.com/search?q=Allianz&ei=r6nWYcrFOKHF4-EPv8iyuAE&start=10&sa=N&ved=2ahUKEwiK2eL125z1AhWh4jgGHT-kDBcQ8tMDegQIAxA3&biw=1600&bih=789&dpr="+str(i))
#     justEnt("//input[@name='q']", j)
#     justCli("//body/div[1]/div[3]/form[1]/div[1]/div[1]/div[3]/center[1]/input[1]")
#     wait(30)
#
#     if i >= 10:
#         quit()
#         break
#     # quit()
#     # wait(20)