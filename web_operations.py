from dotenv import load_dotenv
import os
import requests
from urllib.parse import quote_plus
from snapshot_operations import download_snapshot, poll_snapshot_status

load_dotenv()

dataset_id = "gd_lvz8ah06191smkebj4"


def _make_api_request(url, **kwargs):
    api_key = os.getenv("BRIGHTDATA_API_KEY")

    header = {
        "Authorization": f"Bearer {api_key}",
        "Content-type": "application/json"
    }

    try:
        response = requests.post(url, headers=header, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Api request failed: {e}")
        return None
    except Exception as e:
        print(f"Unknown Error: {e}")
        return None


def serp_search(query, engine="google"):
    if engine == "google":
        base_url = "https://www.google.com/search"
    elif engine == "bing":
        base_url = "https://www.bing.com/search"
    else:
        raise ValueError(f"Unknown engine {engine}")

    url = "https://api.brightdata.com/request"

    payload = {
        "zone": "serp_api1",
        "url": f"{base_url}?q={quote_plus(query)}&brd_json=1",
        "format": "raw"
    }

    full_response = _make_api_request(url, json=payload)

    if not full_response:
        return None

    extracted_data = {
        "knowledge": full_response.get("knowledge", {}),
        "organic": full_response.get("organic", {})
    }
    return extracted_data


def _trigger_and_download_snapshot(trigger_url, params, data, operation_name="operation"):
    trigger_result = _make_api_request(trigger_url, params=params, json=data)
    if not trigger_result:
        return None

    snapshot_id = trigger_result.get("snapshot_id")
    if not snapshot_id:
        return None

    if not poll_snapshot_status(snapshot_id):
        return None

    raw_data = download_snapshot(snapshot_id)
    return raw_data


def reddit_search_api(keyword, date="All time", sort_by="Hot", num_of_posts=80):
    trigger_url = "https://api.brightdata.com/datasets/v3/trigger"

    params = {
        "dataset_id": "gd_mgnh0p8w16o65lmhp",
        "include_errors": "true",
        "type": "discover_new",
        "discover_by": "keyword"
    }

    data = [
        {
            "keyword": keyword,
            "date": date,
            "sort_by": sort_by,
            "num_of_posts": num_of_posts
        }
    ]

    raw_data = _trigger_and_download_snapshot(
        trigger_url, params, data, operation_name="reddit"
    )

    if not raw_data:
        return None

    parsed_data = []
    for post in raw_data:
        parsed_post = {
            "title": post.get("title"),
            "url": post.get("url")
        }
        parsed_data.append(parsed_post)

    return {"parsed_post": parsed_data, "total_found": len(parsed_data)}


def reddit_post_retrieval(urls, days_back=10, load_all_replies=False, comment_limit=""):
    if not urls:
        return None

    trigger_url = "https://api.brightdata.com/datasets/v3/trigger"

    params = {
        "dataset_id": "gd_lvzdpsdlw09j6t702",
        "include_error": "true"
    }

    data = [
        {
            "urls": url,
            "day_back": days_back,
            "load_all_replies": load_all_replies,
            "comment_limits": comment_limit
        }
        for url in urls
    ]

    raw_data = _trigger_and_download_snapshot(
        trigger_url, params, data, operation_name="reddit_comments"
    )

    if not raw_data:
        return None

    # BUG FIX: 'parsed_comment' was used as BOTH the accumulator list AND the dict
    # inside the loop, overwriting itself each iteration, then appending a dict
    # to itself. Renamed to 'parsed_comments' (list) and 'post_entry' (dict).
    parsed_comments = []
    for comment in raw_data:
        post_entry = {
            "comment_id": comment.get("comments"),
            "content": comment.get("comment"),
            "date": comment.get("date_posted"),
            "post_title": comment.get("post_title")
        }
        parsed_comments.append(post_entry)

    return {"comments": parsed_comments, "total_retrieved": len(parsed_comments)}