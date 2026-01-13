import time
import datetime
import requests
from typing import List, Dict

from src.config import RIOT_API_KEY, REGION



# start and end date
start_date = datetime.datetime(2025, 1, 1)
end_date   = datetime.datetime(2025, 12, 31, 23, 59, 59)
start_timestamp = int(time.mktime(start_date.timetuple()))
end_timestamp   = int(time.mktime(end_date.timetuple()))




BASE_URL = f"https://{REGION}.api.riotgames.com"


def _get_headers() -> Dict[str, str]:
    return {
        "X-Riot-Token": RIOT_API_KEY
    }


def _request(url: str, params: Dict = None) -> Dict:
    response = requests.get(url, headers=_get_headers(), params=params)

    if response.status_code == 429:
        # Rate limit hit
        retry_after = int(response.headers.get("Retry-After", 1))
        time.sleep(retry_after)
        return _request(url, params)

    if response.status_code != 200:
        raise RuntimeError(
            f"Riot API error {response.status_code}: {response.text}"
        )

    return response.json()


def get_puuid_by_riot_id(game_name: str, tag_line: str) -> str:
    url = f"{BASE_URL}/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    data = _request(url)
    return data["puuid"]


def get_puuid(summoner_name: str) -> str:
    url = f"{BASE_URL}/lol/summoner/v4/summoners/by-name/{summoner_name}"
    data = _request(url)
    return data["puuid"]


def get_match_ids(puuid: str, count: int = 10, queue: int = None, start_time: int = None, end_time: int = None) -> List[str]:
    url = f"{BASE_URL}/lol/match/v5/matches/by-puuid/{puuid}/ids"
    params = {"count": count}
    if queue is not None:
        params["queue"] = queue
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time

    return _request(url, params)


def get_match_details(match_id: str) -> Dict:
    url = f"{BASE_URL}/lol/match/v5/matches/{match_id}"
    return _request(url)
