import requests
import json
import datetime
import sys

##### 식당 스크래핑
def scrapingRestaurant(headers, databaseId):
    def createPageToRestaurant(headers, databaseId, data):
        createdUrl = "https://api.notion.com/v1/pages"

        newPageData = {
            "parent": {
                "database_id": databaseId
            },
            "properties":  {
                "NAME": {
                    "title": [
                        {
                            "text": {
                                "content": data['BUILDING_NAME'] + " " + data['RESTAURANT_NAME']
                            }
                        }
                    ]
                },
                "MENU_DATE": {
                    "rich_text": [
                        {
                            "text": {
                                "content": data['MENU_DATE']
                            }
                        }
                    ]
                },
                "BUILDING_NAME": {
                    "rich_text": [
                        {
                            "text": {
                                "content": data['BUILDING_NAME']
                            }
                        }
                    ]
                },
                "RESTAURANT_NAME": {
                    "rich_text": [
                        {
                            "text": {
                                "content": data['RESTAURANT_NAME']
                            }
                        }
                    ]
                },
                "RESTAURANT_CODE": {
                    "rich_text": [
                        {
                            "text": {
                                "content": data['RESTAURANT_CODE']
                            }
                        }
                    ]
                },
                "MENU_TYPE": {
                    "rich_text": [
                        {
                            "text": {
                                "content": data['MENU_TYPE']
                            }
                        }
                    ]
                },
                "MENU_TITLE": {
                    "rich_text": [
                        {
                            "text": {
                                "content": data['MENU_TITLE']
                            }
                        }
                    ]
                },
                "MENU_CONTENT": {
                    "rich_text": [
                        {
                            "text": {
                                "content": data['MENU_CONTENT']
                            }
                        }
                    ]
                },
                "BREAKFAST_TIME": {
                    "rich_text": [
                        {
                            "text": {
                                "content": data['BREAKFAST_TIME']
                            }
                        }
                    ]
                },
                "LUNCH_TIME": {
                    "rich_text": [
                        {
                            "text": {
                                "content": data['LUNCH_TIME']
                            }
                        }
                    ]
                },
                "DINNER_TIME": {
                    "rich_text": [
                        {
                            "text": {
                                "content": data['DINNER_TIME']
                            }
                        }
                    ]
                },
                "TEL": {
                    "rich_text": [
                        {
                            "text": {
                                "content": data['TEL']
                            }
                        }
                    ]
                }
            }
        }

        data = json.dumps(newPageData)
        res = requests.post(createdUrl, headers=headers, data=data)

    deletePageFromDatabase(headers, databaseId)

    restaurant = ["Geumjeong", "Saesbeol", "Pusan", "Miryang", "Yangsan"]
    delta = range(-7, 9)

    for r in restaurant:
        url = "https://m.pusan.ac.kr/ko/process/pusan/getMeal" + r

        for d in delta:
            date = (datetime.datetime.now() + datetime.timedelta(days=d)).strftime("%Y-%m-%d")
            params = {'date': date}
            
            response = requests.post(url, params)

            for data in response.json()['lists']:
                createPageToRestaurant(headers, databaseId, data)
#####

##### 기숙사 스크래핑
def scrapingDomitory(headers, databaseId):
    def createPageToDomitory(n, headers, databaseId, data):
        createdUrl = "https://api.notion.com/v1/pages"

        newPageData = {
            "parent": {
                "database_id": databaseId
            },
            "properties":  {
                "no": {
                    "title": [
                        {
                            "text": {
                                "content": n
                            }
                        }
                    ]
                },
                "mealDate": {
                    "rich_text": [
                        {
                            "text": {
                                "content": data['mealDate']
                            }
                        }
                    ]
                },
                "mealKindGcd": {
                    "rich_text": [
                        {
                            "text": {
                                "content": data['mealKindGcd']
                            }
                        }
                    ]
                },
                "codeNm": {
                    "rich_text": [
                        {
                            "text": {
                                "content": data['codeNm']
                            }
                        }
                    ]
                },
                "mealNm": {
                    "rich_text": [
                        {
                            "text": {
                                "content": data['mealNm']
                            }
                        }
                    ]
                }
            }
        }

        data = json.dumps(newPageData)
        res = requests.post(createdUrl, headers=headers, data=data)
        
    deletePageFromDatabase(headers, databaseId)

    no = ["2", "11", "13", "3", "12"]
    delta = range(-7, 9)

    for n in no:
        startDt = (datetime.datetime.now() + datetime.timedelta(days=delta[0])).strftime("%Y-%m-%d")
        endDt = (datetime.datetime.now() + datetime.timedelta(days=delta[-1])).strftime("%Y-%m-%d")

        url = "https://middle.pusan.ac.kr:8443/meal/sub?" + "no=" + n + "&" + "startDt=" + startDt + "&" + "endDt=" + endDt
        
        response = requests.get(url)

        if response.status_code == 200:
            for data in response.json():
                createPageToDomitory(n, headers, databaseId, data)
#####
                    
##### 페이지 삭제
def deletePageFromDatabase(headers, databaseId):
    url = "https://api.notion.com/v1/databases/" + databaseId + "/query"
    response = requests.request("POST", url, headers=headers)
    
    payload = json.dumps({"archived": True})
    
    while len(response.json()['results']) != 0:       
        for list in response.json()['results']:
            pageUrl = "https://api.notion.com/v1/pages/" + list['id']
            pageResponse = requests.request("PATCH", pageUrl, headers=headers, data=payload)

        response = requests.request("POST", url, headers=headers)
#####

##### 배포 상태 변경
def changeDeploymentStatus(headers, databaseId, status):
    url = "https://api.notion.com/v1/databases/" + databaseId + "/query?filter_properties=title"
    
    response = requests.request("POST", url, headers=headers)
    payload = json.dumps({
        "properties": {
            "Status": {
                "rich_text": [{
                    "text": {
                        "content": status
                    }
                }]
            }
        }
    })
    
    for list in response.json()['results']:
        pageUrl = "https://api.notion.com/v1/pages/" + list['id']
        pageResponse = requests.request("PATCH", pageUrl, headers=headers, data=payload)
#####

token = sys.argv[1]
deployDatabaseId = sys.argv[2]
restaurantDatabaseId = sys.argv[3]
domitoryDatabaseId = sys.argv[4]
backupRestaurantDatabaseId = sys.argv[5]
backupDomitoryDatabaseId = sys.argv[6]


headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}


changeDeploymentStatus(headers, deployDatabaseId, "Update")
scrapingRestaurant(headers, restaurantDatabaseId)
scrapingDomitory(headers, domitoryDatabaseId)

changeDeploymentStatus(headers, deployDatabaseId, "Done")
scrapingRestaurant(headers, backupRestaurantDatabaseId)
scrapingDomitory(headers, backupDomitoryDatabaseId)
