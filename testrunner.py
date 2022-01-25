import pandas as pd
output_read = pd.read_csv('notebooks/output.csv')

# test cases run
from datetime import date
from common_function import url, iframe, justCli, hover, clear, justEnt, quit, default_iframe, CancelAlert, wait

for i in range(len(output_read['Test Case Title '])):
    j = output_read['Test Case Title '][i]
    today = date.today()
    d1 = today.strftime("%m/%d/%Y")

    url("https://www.google.com/")
    # url("https://www.google.com/search?q=Allianz&ei=r6nWYcrFOKHF4-EPv8iyuAE&start=10&sa=N&ved=2ahUKEwiK2eL125z1AhWh4jgGHT-kDBcQ8tMDegQIAxA3&biw=1600&bih=789&dpr="+str(i))
    justEnt("//input[@name='q']", j)
    justCli("//body/div[1]/div[3]/form[1]/div[1]/div[1]/div[3]/center[1]/input[1]")
    wait(30)

    if i >= 10:
        quit()
        break
    # quit()
    # wait(20)