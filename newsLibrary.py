import requests

API_KEY = "adf407c2161aebfd1353a5043d4dc010"

def get_news():
    url = f"https://gnews.io/api/v4/top-headlines?country=in&lang=en&token={API_KEY}"
    articles_data = []

    try:
        response = requests.get(url, timeout=5)
        data = response.json()


        #print("GNEWS RESPONSE:",data)


        articles = data.get("articles",[])[:5]

       
        for article in articles:
            articles_data.append({
                "title": article.get("title", "No title available"),
                "description": article.get("description", "No description available")
             })
    except Exception as e:
        print("News API error:", e)

    return articles_data
