def metal_year(first_column):
    metal = list()
    month = list()
    for first in first_column:
        metal.append(first[0:2])
        month.append(first[2:])
        s1 = pd.Series(np.array(metal))
        s2 = pd.Series(np.array(month))
        return s1, s2

array1, array2 = GetTwoTable() #firsttable->array1  secondtable->array2

table1_dataframe, table1_sort_1, table1_sort_2, table2_dataframe  = deal_func(array1, array2)

table1_dataframe.to_csv('table_one.csv')
table2_dataframe.to_csv('table_second.csv')
table1_sort_1.to_csv('ups_and_downs.csv')
table1_sort_2.to_csv('VOL.csv')

print table1_dataframe
print table2_dataframe
print table1_sort_1
print table1_sort_2 
