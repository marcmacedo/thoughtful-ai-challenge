import pandas as pd

class ExcelExporter:
    def __init__(self, news_data, output_path):
        self.news_data = news_data
        self.output_path = output_path
    
    def export_to_excel(self):
        df = pd.DataFrame(self.news_data)
        df.to_excel(self.output_path, index=False)