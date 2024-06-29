import pandas as pd
from datetime import datetime
from IPython.display import display
import calendar

class MoneySpendings:
    def __init__(self, df=None):
        '''
        Initializing 

        Args:
            df (DataFrame): File with spending records
        '''
        self.df = df
        
    def process_columns(self):
        '''
        Here we process the column names
        '''
        self.df = self.df.rename({column: column.strip() for column in self.df.columns}, axis=1)
        
    def info_by_month_manually(self, month="", date_beg="", date_end="", price_apt=5700):
        '''
        Here we get tabular information on spending in a particular month. 
        This fuction works manually. We can adjust the dates ourselves. 
        This is convenient if, for example, the month is counted from a certain date to a certain date.
        
        Args:
            month (str): The name of the month in English.
            date_beg (str): The starting date from which the beginning of the month will be considered.
            date_end (str): The end date from which the end of the month will be considered. 
            price_apt (int): Сost of rent for an apartment per month in shekels. Default: 5700
        '''
        month = month.capitalize()
        date_beg_dt = datetime.strptime(date_beg, "%d/%m/%Y")
        date_end_dt = datetime.strptime(date_end, "%d/%m/%Y")    
        df_cut = self.df[(self.df["Date"] >= date_beg_dt) & (self.df["Date"] <= date_end_dt)] #we get a dataframe in the given dates
        print(f"Spendings in {month}: {df_cut['Price'].sum().round(2)} sheckels")
        print(f"Spendings in {month} with the appartment: {df_cut['Price'].sum().round(2) + price_apt} sheckels")

        category = df_cut.groupby("Category").agg({"Price": "sum"}).sort_values("Price", ascending=False)
        display(category)

        #total expenses grouped by name
        final = df_cut.groupby("Who").agg({"Price": "sum"}).sort_values("Price", ascending=False) 
        final["Price_apt"] = final["Price"] + price_apt / 2
        display(final)
        
    def start(self):
        """
        Start the whole process
        """
        self.process_columns()