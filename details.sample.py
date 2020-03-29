import json
import requests

TOKEN = "..."

def get_lectures(course_id="1865304", page=1, page_size=1000):
    """Retrive data from Udemy"""
    
    data = requests.get(
        url=f"https://www.udemy.com/api-2.0/courses/{course_id}/public-curriculum-items/?page={page}&page_size={page_size}",
        headers = {     
            "Accept": "application/json, text/plain, */*",
            "Authorization": f"Basic {TOKEN}",
            "Content-Type": "application/json;charset=utf-8"
        }
    ).json()

    processed = [
        {
            "title": i.get("title", None), 
            "track": i['asset']['title']
        } 
            for i in data['results'] 
            if i["_class"] == "lecture"
        ]
    
    for k,j in enumerate(processed): 
        print(k + 1, j)
    return processed

def write_load(_data):
    """Write lectures to a file"""
    _data = {k:j for k,j in enumerate(_data)}
    
    with open('output.txt', 'w') as f:
        json.dump(_data, f)


if __name__ == "__main__": 
    print("Printing lectures:")
    data = get_lectures()
    write_load(data)

# cat output.txt | jq | grep -E '.*\".*\.mp4.*'