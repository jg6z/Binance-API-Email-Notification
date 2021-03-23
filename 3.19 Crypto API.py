#!/usr/bin/env python
# coding: utf-8

# In[1]:


from binance.client import Client


# In[2]:


#retrieve api key from text file
a = open("api_key.txt","r")
api_key = a.read().strip()

#retrieve api secret key from text file
b = open("api_secret.txt","r")
api_secret = b.read().strip()

a.close()
b.close()


# In[3]:


#Launching Binance API client
client = Client(api_key, api_secret)
print("Logged in")


# In[4]:


#Asking user various questions for how they would like the program to run

print("How many market checks would you like this program to perform per hour?")
checks_freq = input()

print("For how many hours would you like this program to be running?")
checks_hours = input()

print("At what percentage change, in any stock in your listed portfolio, would you like to be notified of (assuming 24 hr data)?")
change_thresh = input()

print("What message would you like to be notified with if a crypto in your portfolio moves outside of your % change threshold?")
message = input()

print("What is your email?")
email = input()


# In[5]:


#Cryptocurrency portfolio with corresponding 24h percentage change values (initalized to 0 as a default)
portfolio = {'ADABTC':'0','LTCBTC':'0','UNIBTC':'0','ETHBTC':'0'}

#updates portfolio with current 24 hr %change data
def update_portfolio():
    
    #makes request to Binance platform to retrieve current 24h ticker info
    tickers = client.get_ticker()
    
    for row in tickers:
            for asset in portfolio:
                if row['symbol'] == asset:
                    portfolio[asset] = row['priceChangePercent']
    
    #prints current portfolio percent changes               
    for x,y in portfolio.items():
        print(x,y)
        
    #writes current portfolio percent changes to a txt file
    file1 = open('crypto_api_output.txt','w')
    for x,y in portfolio.items():
        file1.writelines([x,': ',y,'\n'])
    file1.close()


# In[6]:


#The following lines of code are used to define a function that can email a user using gmail's SMTP_SSL protocol
import smtplib, ssl

def email_user(message, email):
    #Gmail's SSL Port
            port = 465 

            #Retrieving password
            a = open('password.txt','r')
            password = a.read()
            a.close()

            #Create a secure SSL context
            context = ssl.create_default_context()
            
            #Launches local server so email can be sent
            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                server.login(email, password)
                server.sendmail(email, email, message)


# In[ ]:


import time

#variable for tracking time 
current_run = 0
#variable constant
seconds_in_hour = 3600

#loop runs until user's time request is reached
while (int(current_run) <= (int(checks_hours)*int(checks_freq))):
     
    #retrieves current asset data   
    update_portfolio()
   
    #if any of the price percent changes go over the threshold, the user is emailed with an alert
    for item in portfolio:
        if (int(float(portfolio.get(item))) >= int(change_thresh) or int(float(portfolio.get(item))) <= int(change_thresh) * -1):
            email_user(message, email)
    
    current_run+=1
    
    #used to spread out when iterations of the loop are ran
    time.sleep(seconds_in_hour/int(checks_freq))
    
    


# In[ ]:




