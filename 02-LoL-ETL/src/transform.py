import json
import os
import pandas as pd

# ===============================
# Paths
# ===============================
RAW_DATA_PATH = "data/raw"
OUTPUT_PATH = "data/processed/lol_player_matches_2025.csv"


# ===============================
# Load raw match JSON files
# ===============================
def load_raw_matches():
    matches = []

    for file in os.listdir(RAW_DATA_PATH):
        if file.endswith(".json"):
            with open(os.path.join(RAW_DATA_PATH, file), "r", encoding="utf-8") as f:
                matches.append(json.load(f))

    return matches


# ===============================
# Transform raw matches to tabular format
# ===============================
def transform_matches(matches):
    rows = []

    for match in matches:
        info = match["info"]
        metadata = match["metadata"]

        match_id = metadata["matchId"]
        queue_id = info.get("queueId")

        game_duration_min = info.get("gameDuration", 0) / 60
        game_start_ts = info.get("gameStartTimestamp")
        game_end_ts = info.get("gameEndTimestamp")

        for p in info["participants"]:
            challenges = p.get("challenges", {})

            rows.append({
                # ===============================
                # Match-level data
                # ===============================
                "match_id": match_id,
                "queue_id": queue_id,
                "game_duration_min": round(game_duration_min, 2),
                "game_start_ts": game_start_ts,
                "game_end_ts": game_end_ts,

                # ===============================
                # Player identity
                # ===============================
                "puuid": p.get("puuid"),
                "summoner_name": p.get("riotIdGameName"),  # summonerName puede venir vacío
                "champion_name": p.get("championName"),
                "team_position": p.get("teamPosition"),
                "win": p.get("win"),

                # ===============================
                # Core performance
                # ===============================
                "kills": p.get("kills", 0),
                "deaths": p.get("deaths", 0),
                "assists": p.get("assists", 0),
                "gold": p.get("goldEarned", 0),
                "cs": p.get("totalMinionsKilled", 0) + p.get("neutralMinionsKilled", 0),

                # ===============================
                # Damage metrics
                # ===============================
                "damage_to_champions": p.get("totalDamageDealtToChampions", 0),
                "damage_to_objectives": p.get("damageDealtToObjectives", 0),
                "damage_taken": p.get("totalDamageTaken", 0),

                # ===============================
                # Objectives / Smite mechanics
                # ===============================
                "epic_monster_steals": challenges.get("epicMonsterSteals", 0),
                "epic_monster_steals_with_smite": challenges.get("epicMonsterStealsWithSmite", 0),

                # ===============================
                # Advanced mechanics
                # ===============================
                "dodge_skillshots_small_window": challenges.get("dodgeSkillShotsSmallWindow", 0),
                "total_heal": p.get("totalHeal", 0),
                "damage_self_mitigated": p.get("damageSelfMitigated", 0)
            })

    return pd.DataFrame(rows)


# ===============================
# Main execution
# ===============================
def main():
    print("Loading raw matches...")
    matches = load_raw_matches()
    print(f"Loaded {len(matches)} matches")

    print("Transforming matches...")
    df = transform_matches(matches)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Transformed dataset saved to: {OUTPUT_PATH}")
    print(f"Total rows: {len(df)}")
    print(df.head())


if __name__ == "__main__":
    main()
