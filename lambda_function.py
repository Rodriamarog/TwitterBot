import tweepy
from datetime import datetime
from selenium import webdriver

def lambda_handler():
    # Authenticate using the API key and secret
    api_key = 'YOUR-API-KEY'
    api_key_secret = 'YOUR-API-KEY-SECRET'
    access_token = 'ACCESS-TOKEN'
    access_token_secret = 'ACCESS-TOKEN-SECRET'
    auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
    api = tweepy.API(auth)
    Client ID: YOUR-CLIENT-ID
    Client Secret: CLIENT-ID-SECRET

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
        filtered_wait_times = ['Normal Lanes >>']

        # Print the wait times to the console
        for wait_time in wait_times:
            if wait_time[-1] == ":" or wait_time[0] == "N":
                continue
            else:
                if 'No Delay' in wait_time:
                    filtered_wait_times.append(wait_time)                 
                elif 'Status' in wait_time:
                    wait_time = 'Vehicles: 0.05'
                    filtered_wait_times.append(wait_time)                   
                    continue
                else:
                    filtered_wait_times.append(wait_time)                  
                if 'Pedestrians' in wait_time:
                    count += 1
                    filtered_wait_times.append("\n" + lanes[count])
        
        #Timestamp function
        timestamp = datetime.now()

        month_dict = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio', 7: 'Julio',
                8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}

        month_name = month_dict[timestamp.month]
        hour = timestamp.hour
        minute = timestamp.minute
        ampm = 'AM' if hour < 12 else 'PM'
        if hour > 12:
            hour -= 12
        if hour == 0:
            hour = 12
        if minute < 10:
            minute = '0' + str(minute)
        
        timestamp_str = f'{month_name} {timestamp.day} {timestamp.year}, {hour}:{minute}{ampm}'
                    
        # format it as a string
        filtered_wait_times.append("\n#ComoEstaLaLineaTijuana #Tijuana #LineaTijuana #SanYsidro")
        wait_times_str = "\n".join(filtered_wait_times)
        
        # Use the `tweepy` library to post the tweet on the bot account's timeline
        print("¿Como esta la linea Tijuana?\n\n" + timestamp_str + "\n\n" + str(wait_times_str))
        api.update_status("¿Como esta la linea Tijuana?\n\n" + timestamp_str + "\n\n" + str(wait_times_str))
        
    except Exception as e:
        # Handle any errors that occur during the web scraping or tweeting
        print(f'An error occurred: {e}')
        
    finally:
        # Close the webdriver instance regardless of whether an  error occurred
        driver.quit()
