import requests

def get_prayer_times(city="Karachi", country="Pakistan"):
    url = f"https://api.aladhan.com/v1/timingsByCity?city={city}&country={country}&method=2"
    response = requests.get(url)
    
    if response.status_code == 200:
        timings = response.json().get("data", {}).get("timings", {})
        return timings
    else:
        return {"error": "Unable to fetch prayer times"}

# Example usage
prayer_times = get_prayer_times()
print(prayer_times)
