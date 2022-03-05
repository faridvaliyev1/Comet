import Utils.Helper as helper

print("---------Application is starting----------------------")

print("CSV is importing to the database")
helper.Helper.Save_Csv_To_Sql("Data/wpt.csv")

print("End of the operation")