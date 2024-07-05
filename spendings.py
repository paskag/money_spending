import pandas as pd
from datetime import datetime
from IPython.display import display
import calendar

class MoneySpendings:
    def __init__(self, df=None, price_apt=5700):
        '''
        Initializing 

        Args:
            df (DataFrame): File with spending records
            price_apt (int): Сost of rent for an apartment per month in shekels. Default: 5700
        '''
        self.df = df
        self._price_apt = price_apt
        
    def process_columns(self):
        '''
        Here we process the column names
        '''
        self.df = self.df.rename({column: column.strip() for column in self.df.columns}, axis=1)
        
    def info_by_month_manual(self, month="", date_beg="", date_end="", price_apt=None):
        '''
        Here we get tabular information on spending in a particular month. 
        This fuction works manually. We can adjust the dates ourselves. 
        This is convenient if, for example, the month is counted from a certain date to a certain date.
        
        Args:
            month (str): The name of the month in English.
            date_beg (str): The starting date from which the beginning of the month will be considered.
            date_end (str): The end date from which the end of the month will be considered. 
            price_apt (int): Сost of rent for an apartment per month in shekels. Default: None
        '''
        if price_apt is None:
            price_apt = self._price_apt
        month = month.capitalize()
        date_beg_dt = datetime.strptime(date_beg, "%d/%m/%Y")
        date_end_dt = datetime.strptime(date_end, "%d/%m/%Y")    
        df_cut = self.df[(self.df["Date"] >= date_beg_dt) & (self.df["Date"] <= date_end_dt)] #we get a dataframe in the given dates
        self.show_result(df_cut, month=month)
        
    def info_by_month_automatic(self, year=2024, month=1, price_apt=None):
        '''
        Here we get tabular information on spending in a particular month. 
        This fuction works automatically. We just need to specify the month and the year
        
        Args:
            month (int, str): The number of the month or the name of the month in English.
            year (int): The year
            price_apt (int): Сost of rent for an apartment per month in shekels. Default: None
        '''
        if price_apt is None:
            price_apt = self._price_apt
        if type(month) == str:
            month = month.capitalize()
            month = list(calendar.month_name).index(month)
        month_title = list(calendar.month_name)[month]
        date_beg = datetime(year, month, 1)    
        last_day = calendar.monthrange(year, month)[-1]
        date_end = datetime(year, month, last_day) 
        df_cut = self.df[(self.df["Date"] >= date_beg) & (self.df["Date"] <= date_end)]
        self.show_result(df_cut, month=month_title)
        
    def show_result(self, df_cut=None, month=None):
        '''
        Here we show the result
        
        Args:
            df (DataFrame): Dataframe in giving dates
            month (str): The name of the month in English.
        '''
        print(f"Spendings in {month}: {df_cut['Price'].sum().round(2)} sheckels")
        print(f"Spendings in {month} with the appartment: {df_cut['Price'].sum().round(2) + self._price_apt} sheckels")

        category = df_cut.groupby("Category").agg({"Price": "sum", "Category": "count"}).sort_values("Price", ascending=False)
        category = category.rename({"Category": "Count"}, axis=1)
        display(category)

        #total expenses grouped by name
        final = df_cut.groupby("Who").agg({"Price": "sum"}).sort_values("Price", ascending=False) 
        final["Price_apt"] = final["Price"] + self._price_apt / 2
        display(final)        
    
    def start(self):
        """
        Start the whole process
        """
        self.process_columns()