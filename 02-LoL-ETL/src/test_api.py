from src.riot_api import (
    get_puuid_by_riot_id,
    get_match_ids,
    get_match_details
)


if __name__ == "__main__":
    game_name = "capybara Lover"
    tag_line = "DANI"

    puuid = get_puuid_by_riot_id(game_name, tag_line)
    print("PUUID:", puuid)

    match_ids = get_match_ids(puuid, count=3)
    print("Match IDs:", match_ids)

    match_data = get_match_details(match_ids[0])
    print("Match keys:", match_data.keys())
