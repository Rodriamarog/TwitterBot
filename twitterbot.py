import tweepy
import time
from selenium import webdriver

# Authenticate using the API key and secret
api_key = 'INSERT YOUR API KEY HERE'
api_key_secret = 'INSERT YOUR API KEY SECRET HERE'
access_token = 'INSERT YOUR ACCESS TOKEN HERE'
access_token_secret = 'INSERT YOUR ACCESS TOKEN SECRET HERE'
auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
api = tweepy.API(auth)

while True:
    try:
        # Create a ChromeOptions instance to set the headless flag
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        
        # Create a webdriver instance with the headless flag
        driver = webdriver.Chrome(chrome_options=options)

        # Navigate to the website
        driver.get("https://www.smartbordercoalition.com/border-wait-times")

        # Wait for the page to load
        driver.implicitly_wait(10)

        # Use JavaScript to get the wait times
        wait_times = driver.execute_script("""
            let times = [];
            let tickerItems = document.querySelectorAll("div.ticker__item:nth-of-type(2) span");
            tickerItems.forEach(function(item) {
                times.push(item.innerText);
            });
            return times;
        """)

        # Create a list with the lane names to be accessed by a counter
        lanes = ['All Traffic >>','Ready Lanes >>','Sentri >>']
        count = 0

        # Print the wait times to the console
        for wait_time in wait_times:
            if wait_time[-1] == ":":
                continue
            elif wait_time[0] == "N":
                continue
            else:
                if 'No Delay' in wait_time:
                    print(wait_time.replace('No Delay','0.05'))
                elif 'Status' in wait_time:
                    wait_time = 'Vehicles: 0.05'
                    print(wait_time)
                    continue
                else:
                    print(wait_time)
        # Every time we print 'Pedestrians' we want to print the next lane so we increase the counter by 1
                if 'Pedestrians' in wait_time:
                    count += 1
                    print("\n" + lanes[count])
        # format it as a string
        wait_times_str = "\n".join(wait_times)

        # Use the `tweepy` library to post the tweet on the bot account's timeline
        api.update_status(f"Border wait times: {wait_times_str}")
    except Exception as e:
        # Handle any errors that occur during the web scraping or tweeting
        print(f'An error occurred: {e}')
        
    finally:
      # Close the webdriver instance regardless of whether an  error occurred
      driver.quit()
      # Wait for 15 minutes before posting the next tweet
      time.sleep(900) 
