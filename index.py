import os
import json
import sys, time

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "credentials.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    data = {}
    countries = ['au', 'pe', 'us', 'gb', 'in', 'de', 'ca', 'fr', 'kr', 'ru', 'jp', 'br', 'mx']
    for country in countries:
        countryData = []
        categories = getCategories(youtube, country);
        categories = categories.get('items')
        print("fetching data from country: " + country)

        for cat in categories:
            catId = cat.get('id')
            print("cat => " + catId)
            catSnippet = cat.get('snippet')
            print(catSnippet.get('assignable'))
            if (catSnippet.get('assignable') == True or catSnippet.get('assignable') == 'True'):
                print('------------------------')
                countryData += getDataByCountry(youtube, catId, country);
            else:
                print("skip cat" + catId)
        data[country] = countryData;

    outDir = 'data.json'
    with open(outDir, "w+", encoding='utf-8') as file:
        file.write(json.dumps(data))
        print("done!")

def getDataByCountry(youtube, catId, country):
    nextPageToken = '&';
    data = []
    while nextPageToken is not None:
        request = youtube.videos().list(
            part="snippet",
            chart="mostPopular",
            maxResults=50,
            regionCode=country,
            pageToken=nextPageToken,
            videoCategoryId=catId
        )
        response = request.execute()
        data += response.get('items')
        nextPageToken = response.get("nextPageToken", None);
        print(nextPageToken)
    return data

def getCategories(youtube, country):
    request = youtube.videoCategories().list(
        part="snippet",
        regionCode=country
    )
    response = request.execute()
    return response

if __name__ == "__main__":
    main()
