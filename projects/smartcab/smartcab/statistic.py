import pandas
a = pandas.read_csv('output.csv')
Num_Succeed = a[a['Succeed']== True]['Succeed'].sum()
print 'reached destination {} times'.format(Num_Succeed)