import requests
import smtplib
my_email = #your email
gmail = # access key of your mail

connection = smtplib.SMTP("smtp.gmail.com", port=587)
connection.starttls()
connection.login(user=my_email, password= gmail)

link = "https://icanhazdadjoke.com/"

headers = {
  "Accept": "application/json"
}
url = "https://icanhazdadjoke.com"

r = requests.get(url, headers = headers)
params = {"q":"joke"}
dadjoke = requests.get(url= link, headers= headers, params = params)
dadjoke.raise_for_status()
joke = dadjoke.json()["joke"]
print(joke)




connection.sendmail(from_addr=my_email, to_addrs=#where to send it,
                        msg = f"Subject: Joke of the day \n\n {joke}")

connection.close()
#meta property="og:description"
#print(joke.json()["joke"])
#print(joke.content)
