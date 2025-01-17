import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import pandas as pd

def get_ton_to_usd_rate():
    """
    Fetch the current exchange rate of 1 TON to USD from CoinCodex.
    """
    try:
        response = requests.get("https://coincodex.com/api/coincodex/get_coin/toncoin")
        if response.status_code == 200:
            data = response.json()
            return data.get("last_price_usd", 0)
        else:
            print("Failed to fetch exchange rate. Using default value of $2.0 per TON.")
            return 2.0  # Default value if the API call fails
    except Exception as e:
        print(f"Error fetching exchange rate: {e}. Using default value of $2.0 per TON.")
        return 2.0


def fetch_usernames(search_term, sort_option):
    url = "https://fragment.com/api?hash=6bc2314d461dbf7309"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://fragment.com",
        "DNT": "1",
        "Sec-GPC": "1",
        "Connection": "keep-alive",
        "Referer": f"https://fragment.com/?query={search_term}",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=0",
    }

    load_dotenv()

    cookies = {
        "stel_ssid": os.getenv("STEL_SSDI"),  # Replace with actual cookie
    }

    data = {
        "type": "usernames",
        "query": search_term,
        "filter": "sold",
        "sort": sort_option,
        "method": "searchAuctions",
    }

    response = requests.post(url, headers=headers, data=data, cookies=cookies)

    if response.status_code == 200:
        try:
            response_json = response.json()
            if response_json.get("ok"):
                html_content = response_json.get("html", "")
                soup = BeautifulSoup(html_content, "html.parser")

                # Locate all rows containing data
                rows = soup.select(".tm-row-selectable")
                if not rows:
                    print("No results found.")
                    return

                # Prepare data for DataFrame
                data_list = []
                for row in rows:
                    # Extract username
                    username_element = row.select_one(".table-cell .tm-value")
                    username = username_element.text.strip() if username_element else "N/A"

                    # Extract price
                    price_element = row.select_one(".icon-before")
                    price = (
                        float(price_element.text.strip().replace(",", ""))
                        if price_element
                        else None
                    )

                    # Extract status
                    status_element = row.select_one(
                        ".tm-status-unavail, .tm-status-avail, .table-cell-status-thin"
                    )
                    status = status_element.text.strip() if status_element else "N/A"

                    # Append row data
                    data_list.append({"Username": username, "Price": price, "Status": status})

                # Create a DataFrame
                df = pd.DataFrame(data_list)

                # Calculate statistics
                average_price = df["Price"].mean()
                min_price = df["Price"].min()
                max_price = df["Price"].max()

                min_price_username = df[df["Price"] == min_price]["Username"].values[0]
                max_price_username = df[df["Price"] == max_price]["Username"].values[0]

                ton_to_usd_rate = get_ton_to_usd_rate()

                # Display statistics
                print(f"\nAverage Price of Sold Usernames: {average_price:.2f} TON (~${average_price * ton_to_usd_rate:.2f})")
                print(f"Minimum Price: {min_price:.2f} TON (~${min_price * ton_to_usd_rate:.2f}) (Username: {min_price_username})")
                print(f"Maximum Price: {max_price:.2f} TON (~${max_price * ton_to_usd_rate:.2f}) (Username: {max_price_username})")

                print("\nSales Data:")
                print(df)

                # Save DataFrame to a file (optional)
                output_file = f"sales_data_{search_term}.csv"
                df.to_csv(output_file, index=False)
                print(f"\nData saved to {output_file}")
            else:
                print("Error in response:", response_json.get("error"))
        except ValueError:
            print("Invalid JSON response:", response.text)
    else:
        print(f"Failed to fetch data. Status Code: {response.status_code}, Response: {response.text}")


def prompt_sort_option():
    print("Choose a sorting option:")
    print("1. Price high to low (default)")
    print("2. Price low to high")
    print("3. Recently listed")
    print("4. End time")

    choice = input("Enter your choice (1-4): ").strip()
    if choice == "2":
        return "price_asc"
    elif choice == "3":
        return "listed"
    elif choice == "4":
        return "ending"
    else:
        return "price_desc"  # Default to "price high to low"

if __name__ == "__main__":
    search_term = input("Enter a search term: ").strip()
    if search_term:
        sort_option = prompt_sort_option()
        fetch_usernames(search_term, sort_option)
    else:
        print("Please enter a valid search term.")