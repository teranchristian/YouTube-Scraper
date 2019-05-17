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

    test = getDataByCountry(youtube);

    outDir = 'test.json'
    with open(outDir, "w+", encoding='utf-8') as file:
        file.write(json.dumps(test))

def getDataByCountry(youtube):
    nextPageToken = '&';
    data = []
    while nextPageToken is not None:
        request = youtube.videos().list(
            part="snippet",
            chart="mostPopular",
            maxResults=50,
            regionCode="AU",
            pageToken=nextPageToken
        )
        response = request.execute()
        data += response.get('items')
        nextPageToken = response.get("nextPageToken", None);
        nextPageToken = None
        print(nextPageToken)
    return data

if __name__ == "__main__":
    main()
