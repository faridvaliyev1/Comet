class Formulas(object):

    @staticmethod
    def Find_Null_Threshold(wpt):
        pass
    
    @staticmethod
    def Find_Support_Threshold(wpt):
        pass
    
    @staticmethod
    def metric_total_null(total_nulls,column,row):
        return total_nulls/(column*row)
    
    @staticmethod
    def metric_total_null_column(total_nulls,column):
        return total_nulls/column
    
    @staticmethod
    def metric_total_null_row(total_nulls,row):
        return total_nulls/row
