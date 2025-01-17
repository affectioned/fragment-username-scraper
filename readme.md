
# Fragment Username Sales Scraper

This program fetches information about sold Telegram usernames from the Fragment marketplace. It retrieves and displays statistics such as the average price, minimum price, maximum price, and corresponding usernames. The program also converts TON prices into USD based on real-time exchange rates.

## Prerequisites

1.  **Python**: Ensure you have Python 3.8 or higher installed.
2.  **Libraries**: Install the required Python libraries:
    
    ```bash
    pip install requests beautifulsoup4 python-dotenv pandas
    
    ```
    
3.  **Environment Variable**:
    -   The program requires a `stel_ssid` value for authentication. Obtain this value from the network tools in your browser (explained below).
    -   Create a `.env` file in the same directory as the script and add:
        
        ```
        STEL_SSDI=your_stel_ssid_value
        
        ```
        

## How to Obtain `stel_ssid`

1.  Open your browser go to the Fragment marketplace.
2.  Use the "Private Window" or "Incognito Mode."
3.  Open the developer tools (usually accessible with `F12` or `Ctrl+Shift+I`).
4.  Navigate to the "Network" tab.
5.  Perform a search or any interaction that makes a request to the `https://fragment.com` domain.
6.  Look for a request to the endpoint `https://fragment.com/api?hash=6bc2314d461dbf7309`.
7.  Under the "Cookies" section of the request, find `stel_ssid` and copy its value.
8.  Paste this value into your `.env` file as shown above.

## How to Use the Program

1.  **Run the Script**:
    
    -   Save the script to a `.py` file (e.g., `fragment_sales_scraper.py`).
    -   Run it from the command line:
        
        ```bash
        python fragment_sales_scraper.py
        
        ```
        
2.  **Input Search Term**:
    
    -   Enter a keyword to search for usernames (e.g., `search_term`).
3.  **Choose Sorting Option**:
    
    -   Select a sorting option when prompted:
        -   `1`: Price high to low (default).
        -   `2`: Price low to high.
        -   `3`: Recently listed.
        -   `4`: End time.

## Example Output

```
Enter a search term: test
Choose a sorting option:
1. Price high to low (default)
2. Price low to high
3. Recently listed
4. End time
Enter your choice (1-4): 2

Average Price of Sold Usernames: 50.25 TON (~$100.50)
Minimum Price: 20.00 TON (~$40.00) (Username: @example_min)
Maximum Price: 80.00 TON (~$160.00) (Username: @example_max)

Sales Data:
    Username  Price   Status
0  @example1   50.0  Sold
1  @example2   20.0  Sold
2  @example3   80.0  Sold

Data saved to sales_data_test.csv

```

## Notes

-   Ensure the `stel_ssid` is valid; otherwise, requests will fail.
-   The default exchange rate is $2.00 per TON if the real-time fetch fails.