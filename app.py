from flask import Flask, jsonify, request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import os


app = Flask(__name__)

# Load environment variables from .env
load_dotenv()

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = os.getenv("API_KEY")
debug_mode = os.getenv("DEBUG")

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def youtube_search(query, max_results):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    print(query)
    # Call the search.list method to retrieve results matching the specified query term.
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults=max_results
    ).execute()

    videos = []

    # Add each result to the list.
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append({
                'title': search_result['snippet']['title'],
                'videoId': search_result['id']['videoId']
            })

    return videos


@app.route('/search', methods=['POST', 'GET'])
def search():    
    query = request.args.get('query')
    #query=request.form.get("query")
    print (query)
    max_results = int(request.args.get('max_results', 25))  # Default max results if not provided
    
    try:
        results = youtube_search(query, max_results)
        return jsonify({'videos': results})
    except HttpError as e:
        return jsonify({'error': f'An HTTP error {e.resp.status} occurred: {e.content}'})


if __name__ == '__main__':
    app.run(debug=True)    
