import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt


class DataScraper:
    def __init__(self, url):
        self.url = url

    def scrape_data(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            data = []
            rows = soup.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                if len(columns) == 2:
                    country = columns[0].text.strip()
                    population = columns[1].text.strip().replace(',', '')
                    data.append((country, population))
            return data

        except requests.exceptions.RequestException as e:
            raise Exception(f"An error occurred while scraping data: {e}")


class DataAnalyzer:
    def __init__(self, data):
        self.data = data

    def analyze_data(self):
        try:
            df = pd.DataFrame(self.data, columns=['Country', 'Population'])
            df['Population'] = pd.to_numeric(df['Population'])
            total_population = df['Population'].sum()
            df['Percentage'] = (df['Population'] / total_population) * 100
            df = df.sort_values('Population', ascending=False)
            return df

        except ValueError as e:
            raise Exception(f"An error occurred while analyzing data: {e}")


class DataPlotter:
    def __init__(self, df):
        self.df = df

    def plot_data(self):
        try:
            plt.figure(figsize=(10, 6))
            plt.bar(self.df['Country'], self.df['Population'])
            plt.title('Population by Country')
            plt.xlabel('Country')
            plt.ylabel('Population')
            plt.xticks(rotation=90)
            plt.show()

        except Exception as e:
            raise Exception(f"An error occurred while plotting data: {e}")


def main():
    url = 'https://www.example.com/population'

    try:
        scraper = DataScraper(url)
        data = scraper.scrape_data()

        analyzer = DataAnalyzer(data)
        df = analyzer.analyze_data()

        plotter = DataPlotter(df)
        plotter.plot_data()

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
