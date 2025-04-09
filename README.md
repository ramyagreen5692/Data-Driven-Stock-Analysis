# Data-Driven-Stock-Analysis
📈 Stock Performance Dashboard
This project focuses on analyzing and visualizing the performance of Nifty 50 stocks using Python, Streamlit, and Power BI. It extracts data from YAML files, processes it to compute key metrics, stores them in a SQL database, and builds interactive visualizations.

🧩 Key Features
Data Extraction & Cleaning

Parses raw YAML stock data stored by date and symbol.

Cleans and transforms the data into a usable format for analysis.

Five Key Metrics Computed

📊 Volatility Analysis: Standard deviation of daily returns to measure stock price fluctuations.

📈 Cumulative Returns: Shows the growth of each stock over time.

🏭 Sector-wise Performance: Aggregates performance based on sectors like IT, Pharma, Finance, etc.

🔗 Stock Price Correlation (Planned): Matrix showing how stock prices move together.

🚀 Top Gainers & Losers (Monthly): Highlights best and worst performing stocks each month.

Data Storage

Each metric is stored as a CSV file.

All CSVs are inserted into a TiDB Cloud MySQL database for persistence and visualization.

Visualization

🔍 Streamlit: For interactive, web-based analysis.

📊 Power BI: For executive-level dashboards and reports.

