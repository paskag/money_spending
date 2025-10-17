import pandas as pd
from datetime import datetime
from IPython.display import display
import calendar

class MoneySpendings:
    def __init__(self, df=None, price_apt=5850, subscriptions=None):
        '''
        Initializing 

        Args:
            df (DataFrame): File with spending records
            price_apt (int): Сost of rent for an apartment per month in shekels. Default: 5700
            subscriptions (list): List of dictionary of subscription costs. Default: None
        '''
        self.df = df
        self._price_apt = price_apt
        self.df = self.df.rename({column: column.strip() for column in self.df.columns}, axis=1)
        self._subscriptions = subscriptions
            
    def info_by_period(self, date_beg="", date_end="", price_apt=None):
        '''
        Here we get tabular information on spending for a given period of time
        This fuction works manually. We can adjust the dates ourselves. 
        
        Args:
            date_beg (str): The starting date from which the beginning of the month will be considered.
            date_end (str): The end date from which the end of the month will be considered. 
            price_apt (int): Сost of rent for an apartment per month in shekels. Default: None
        '''
        if price_apt is None:
            price_apt = self._price_apt
        period = f'{date_beg} - {date_end}'
        date_beg_dt = datetime.strptime(date_beg, "%d/%m/%Y")
        date_end_dt = datetime.strptime(date_end, "%d/%m/%Y")    
        df_cut = self.df[(self.df["Date"] >= date_beg_dt) & (self.df["Date"] <= date_end_dt)] #we get a dataframe in the given dates
        self.show_result(df_cut, period=period)
        
    def info_by_month(self, year=2024, month=1, price_apt=None):
        '''
        Here we get tabular information on spending in a particular month. 
        
        Args:
            month (int, str): The number of the month or the name of the month in English.
            year (int): The year
            price_apt (int): Сost of rent for an apartment per month in shekels. Default: None
        '''
        if type(month) == str:
            month = month.capitalize()
            month = list(calendar.month_name).index(month)
        month_title = list(calendar.month_name)[month]
        period = f'{month_title} {year}'
        date_beg = datetime(year, month, 1)    
        last_day = calendar.monthrange(year, month)[-1]
        date_end = datetime(year, month, last_day) 
        df_cut = self.df[(self.df["Date"] >= date_beg) & (self.df["Date"] <= date_end)]
        self.show_result(df_cut, period=period)
        
    def info_by_year(self, year=2024, price_apt=None):
        '''
        Here we get tabular information on spending in a particular year. 
        
        Args:
            year (int, str): The number of the year
            price_apt (int): Сost of rent for an apartment per month in shekels. Default: None
        '''
        year = int(year)
        date_beg = datetime(year, 1, 1)
        date_end = datetime(year, 12, 31)
        df_cut = self.df[(self.df["Date"] >= date_beg) & (self.df["Date"] <= date_end)]
        self.show_result(df_cut, period=year, yearly=True) 
                
    def annual_report(self, year=2024):
        '''
        Here we get a detailed annual report. Information will be provided for each month.
        
        Args:
            year (int, str): The number of the year
        '''
        year = int(year)
        date_beg = datetime(year, 1, 1)
        date_end = datetime(year, 12, 31)
        df_cut = self.df[(self.df["Date"] >= date_beg) & (self.df["Date"] <= date_end)]
        first_month = df_cut.iloc[0]['Date'].month
        last_month = df_cut.iloc[-1]['Date'].month
        months = {i: list(calendar.month_name)[i] for i in range(first_month, last_month + 1)}
        categories = sorted(df_cut["Category"].unique())
        report = pd.DataFrame(index=categories)
        data_name = []
        for idx, month in months.items():
            month_beg = datetime(year, idx, 1)
            last_day = calendar.monthrange(year, idx)[-1]
            month_end = datetime(year, idx, last_day)
            month_cut = df_cut[(df_cut["Date"] >= month_beg) & (df_cut["Date"] <= month_end)]
            data_name.append((month, "Pasha", month_cut[month_cut["Who"] == 'Pasha']["Price"].sum().round(2)))
            data_name.append((month, "Alona", month_cut[month_cut["Who"] == 'Alona']["Price"].sum().round(2)))
            grouped = month_cut.groupby("Category").agg({"Price": "sum"}).rename({"Price": month}, axis=1)
            report = report.join(grouped)
        report = report.fillna(0).round().astype(int)
        report_name = pd.DataFrame(data_name, columns=['Month', 'Name', 'Price'])
        self.show_annual_report(year=year, report=report, report_name=report_name)
    
    def show_result(self, df_cut=None, period=None, yearly=False):
        '''
        Here we show the result
        
        Args:
            df_cut (DataFrame): Dataframe in giving dates
            period (str): The time period for which the result is calculated.
            yearly (bool): A marker that indicates whether it is an annual report or not: Default: False
        '''
        price_apt = self._price_apt * [1, df_cut['Date'].dt.to_period('M').nunique()][yearly] #count how many months
        final_price = df_cut['Price'].sum().round(2)
        
        if self._subscriptions is not None:
            df_subscriptions_show = pd.DataFrame(self._subscriptions)
            df_subscriptions_show = df_subscriptions_show.sort_values("Price", ascending=False)
            df_subscriptions = df_subscriptions_show.copy()
            df_subscriptions_show = df_subscriptions_show.set_index("What")
            
            final_price_subscriptions = df_subscriptions["Price"].sum()
            final_price += final_price_subscriptions
            
            df_subscriptions["Category"] = "Subscriptions"
            df_subscriptions["Date"] = 'Date'
            df_subscriptions = df_subscriptions[["Date", "Who", "What", "Category", "Price"]]
            df_cut = pd.concat([df_cut, df_subscriptions], ignore_index=True)
             
        final_price_apt = final_price + price_apt
        
        print(f"Spendings in {period}: {final_price:.2f} sheckels")
        print(f"Spendings in {period} with the appartment: {final_price_apt:.2f} sheckels")

        category_who = df_cut.groupby(["Category", 'Who']).agg({"Price": "sum", "Category": "count"})
        category_who = category_who.rename({"Category": "Count"}, axis=1)
        category_who = category_who.sort_values(["Category", 'Who'])
        category_who['Total'] = category_who.groupby('Category')['Price'].transform('sum')
        category_who = category_who.sort_values(['Total', 'Price'], ascending=False)
        category_who['Total'] = category_who['Total'].transform(lambda x: x.mask(x.duplicated(), ''))
        display(category_who)

        if self._subscriptions is not None:
            display(df_subscriptions_show)
       
        #total expenses grouped by name
        total = df_cut.groupby("Who").agg({"Price": "sum"}).sort_values("Price", ascending=False) 
        total["Price_apt"] = total["Price"] + price_apt / 2
        display(total)
        
    def show_annual_report(self, year=None, report=None, report_name=None):
        '''
        Here we show the anual report
        
        Args:
            year (int): The number of the year
            report (DataFrame): Dataframe grouped by category with information for each month of the year
            report_name (DataFrame): Dataframe grouped by name with information for each month of the year
        '''
        print(f"Annual report {year}")
        display(report)
        
        report_name["Price_apt"] = report_name["Price"] + self._price_apt / 2
        report_name = report_name.set_index(['Month', 'Name'])
        display(report_name)