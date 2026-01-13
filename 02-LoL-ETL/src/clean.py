import pandas as pd
from pathlib import Path


PROCESSED_PATH = Path("data/processed/lol_player_matches_2025.csv")
CLEAN_PATH = Path("data/clean/matches_clean.csv")


def load_data() -> pd.DataFrame:
    print("Loading processed data...")
    df = pd.read_csv(PROCESSED_PATH)
    print(f"Loaded {len(df)} rows")
    return df


def clean_strings(df: pd.DataFrame) -> pd.DataFrame:
    print("Cleaning string columns...")

    string_cols = [
        "match_id",
        "puuid",
        "summoner_name",
        "champion_name",
        "team_position",
    ]

    for col in string_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .replace({"": pd.NA, "nan": pd.NA})
        )

    return df


def convert_timestamps(df: pd.DataFrame) -> pd.DataFrame:
    print("Converting timestamps to datetime...")

    df["game_start_ts"] = pd.to_datetime(
        df["game_start_ts"], unit="ms", errors="coerce"
    )
    df["game_end_ts"] = pd.to_datetime(
        df["game_end_ts"], unit="ms", errors="coerce"
    )

    return df


def validate_queues(df: pd.DataFrame) -> pd.DataFrame:
    print("Validating queue IDs...")

    VALID_QUEUES = {400, 420, 440}
    df = df[df["queue_id"].isin(VALID_QUEUES)]

    return df


def filter_invalid_games(df: pd.DataFrame) -> pd.DataFrame:
    print("Filtering invalid or incomplete games...")

    initial_len = len(df)

    # not useful games (less than 5 min)
    df = df[df["game_duration_min"] > 5]

    # without position
    df = df[df["team_position"].notna()]

    print(f"Removed {initial_len - len(df)} rows")

    return df


def enforce_numeric_types(df: pd.DataFrame) -> pd.DataFrame:
    print("Enforcing numeric types...")

    numeric_cols = [
        "queue_id",
        "game_duration_min",
        "kills",
        "deaths",
        "assists",
        "gold",
        "cs",
        "damage_to_champions",
        "damage_to_objectives",
        "damage_taken",
        "epic_monster_steals",
        "epic_monster_steals_with_smite",
        "dodge_skillshots_small_window",
        "total_heal",
        "damage_self_mitigated",
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    print("Creating derived features...")

    # KDA
    df["kda"] = (df["kills"] + df["assists"]) / df["deaths"].replace(0, 1)

    # CS per min
    df["cs_per_min"] = df["cs"] / df["game_duration_min"]

    # Damage
    df["damage_per_min"] = (df["damage_to_champions"] / df["game_duration_min"])

    df["damage_per_gold"] = df["damage_to_champions"] / df["gold"].replace(0, 1)

    df["aggression_score"] = (df["kills"] + df["assists"]) / df["game_duration_min"]

    df["tankiness"] = (df["damage_taken"] + df["damage_self_mitigated"]) / df["game_duration_min"]

    df["tankiness"] = (df["damage_taken"] + df["damage_self_mitigated"]) / df["game_duration_min"]

    df["mechanics_score"] = (df["dodge_skillshots_small_window"]) / df["game_duration_min"]

    df["risk_ratio"] = df["deaths"] / (df["kills"] + df["assists"]).replace(0, 1)



    return df


def save_data(df: pd.DataFrame):
    CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_PATH, index=False)
    print(f"Clean data saved to {CLEAN_PATH}")


def main():
    df = load_data()

    df = clean_strings(df)
    df = convert_timestamps(df)
    df = validate_queues(df)
    df = filter_invalid_games(df)
    df = enforce_numeric_types(df)
    df = feature_engineering(df)

    print("\nFinal dataset:")
    print(df.info())

    save_data(df)


if __name__ == "__main__":
    main()
