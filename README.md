## Disclaimer
This system is a mock web api for creating orders on Binance, based on the user's trading ideas. It is important to note that the user is fully responsible for any outcomes that may result from using this system. It is recommended to test the system thoroughly and understand the risks before using it for actual trading. 

#### JSON data looks like this.    
  
{   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"type":"Entry",  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"side":"BUY",   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"leverage":3,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"symbol":"BTCUSDT"  
}   
  
## Deploment Idea 
In my case, I used Heroku for deployment.  
1, Push to Github.  
2, Go to Heroku and set "Reveal Config Vars". Check "env.todo" file for required env vals.   
3, Select your repository to deploy.   

 
