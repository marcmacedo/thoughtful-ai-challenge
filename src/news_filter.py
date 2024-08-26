from datetime import datetime

class NewsFilter:
    def __init__(self, news_data, months):
        self.news_data = news_data
        self.months = months
    
    def filter_by_date(self):
        filtered_news = []
        current_month = datetime.now().month
        current_year = datetime.now().year

        for news in self.news_data:
            news_date = datetime.strptime(news['date'], '%Y-%m-%d')
            if (current_year == news_date.year and current_month - news_date.month <= self.months):
                filtered_news.append(news)
        
        return filtered_news