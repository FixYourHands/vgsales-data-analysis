import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import os

def loadFile(filePath):
    try:
        df = pd.read_csv('vgsales.csv')
        print("Load successful")
        return df
    except FileNotFoundError:
        print(f"Error: File {filePath} not found.")
        return None
    except Exception as e:
        print(f"An error occurred while loading the data: {e}")
        return None
    
def cleanFile(df):
    if df is None:
        return None
    
    df_cleaned = df.dropna().copy() #rows missing values
    df_cleaned.drop_duplicates(inplace=True)

    df_cleaned['Year'] = df_cleaned['Year'].astype(int) #convert year to int
    df_cleaned.reset_index(drop=True, inplace=True)

    return df_cleaned

def plotSalesByGenre(df):
    if df is None:
        print("Cannot plot. df is empty.")
        return
    
    genre_sales = df.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False)
    plt.figure(figsize=(12, 6))
    genre_sales.plot(kind='bar', color='skyblue')
    plt.title('Total Global Sales by Genre', fontsize=16)
    plt.xlabel('Genre', fontsize=12)
    plt.ylabel('Total Global Sales (in millions)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Save the plot
    plot_path = 'sales_by_genre.png'
    plt.savefig(plot_path)
    print(f"\nPlot saved as '{plot_path}'")

    plt.show()

def plotSalesOverTime(df):
    if df is None:
        print("Cannot plot. df is empty.")
        return
    yearly_sales = df.groupby('Year')['Global_Sales'].sum()
    
    plt.figure(figsize=(12, 6))
    yearly_sales.plot(kind='line', marker='o', linestyle='-', color='blue')
    plt.title('Global Sales By Time', fontsize=16)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Total Global Sales (in millions)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Save the plot
    plot_path = 'sales_over_time.png'
    plt.savefig(plot_path)
    print(f"\nPlot saved as '{plot_path}'")

    plt.show()

def plotPublisherComparison(df, top_n=10):
    if df is None:
        print("Cannot plot. df is empty.")
        return
    
    publisher_sales = df.groupby('Publisher')['Global_Sales'].sum().nlargest(top_n)
    
    plt.figure(figsize=(12, 8))
    publisher_sales.plot(kind='bar', color='green')
    plt.title(f'Top {top_n} Publishers by Global Sales', fontsize=16)
    plt.xlabel('Publisher', fontsize=12)
    plt.ylabel('Total Global Sales (in millions)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Save the plot
    plot_path = 'top_publishers.png'
    plt.savefig(plot_path)
    print(f"\nPlot saved as '{plot_path}'")

    plt.show()

def plotScatterSalesGlobal(df):
    if df is None:
        print("Cannot plot. df is empty.")
        return
    filtered_df = df[(df['Global_Sales'] > 0) | (df['NA_Sales'] > 0)].copy()
    fig = px.scatter(
        filtered_df, 
        x='NA_Sales', 
        y='Global_Sales', 
        color='Genre',
        size='Global_Sales', 
        hover_name='Name', 
        hover_data=['Platform', 'Year', 'Publisher'], 
        title='Global Sales vs. North American Sales by Genre',
        labels={
            "NA_Sales": "North American Sales (in millions)",
            "Global_Sales": "Global Sales (in millions)"
        },
        template='plotly_white' 
    )
    
    fig.update_layout(
        title_font_size=18,
        xaxis_title_font_size=14,
        yaxis_title_font_size=14,
        legend_title_font_size=12
    )

    print("\nDisplaying interactive scatter plot...")
    fig.show()

def plotScatterSalesPlatform(df, top_n=15):
    if df is None:
        print("Cannot plot. df is empty.")
        return
    platform_sales = df.groupby('Platform')['Global_Sales'].sum().nlargest(top_n).reset_index()

    fig = px.bar(
        platform_sales,
        x='Platform',
        y='Global_Sales',
        color='Platform', # Color bars by platform
        title=f'Top {top_n} Platforms by Global Sales (Interactive)',
        labels={
            "Platform": "Gaming Platform",
            "Global_Sales": "Total Global Sales (in millions)"
        },
        template='plotly_white'
    )
    
    fig.update_layout(
        title_font_size=18,
        xaxis_title_font_size=14,
        yaxis_title_font_size=14,
        showlegend=False # No need for a legend if bars are colored by platform name
    )

    print(f"\nDisplaying interactive bar chart for top {top_n} platforms...")
    fig.show()

file_name = 'vgsales.csv' #name of dataset
if not os.path.exists(file_name):
        print(f"Dataset '{file_name}' not found.")
else:
    sales_df = loadFile(file_name)
    cleaned_df = cleanFile(sales_df)

    if cleaned_df is not None:
            plotSalesByGenre(cleaned_df)
            plotSalesOverTime(cleaned_df)
            plotPublisherComparison(cleaned_df)
            plotScatterSalesGlobal(cleaned_df)
            plotScatterSalesPlatform(cleaned_df)