import csv
import json
from pathlib import Path
from typing import Set
import time
import datetime

from src.riot_api import (
    get_puuid_by_riot_id,
    get_match_ids,
    get_match_details
)


RAW_DIR = Path("data/raw")
INPUT_DIR = Path("data/input")

RAW_DIR.mkdir(parents=True, exist_ok=True)


def load_processed_matches() -> Set[str]:
    return {file.stem for file in RAW_DIR.glob("*.json")}


def load_summoners():
    with open(INPUT_DIR / "summoners.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_raw_match(match_id: str, data: dict) -> None:
    with open(RAW_DIR / f"{match_id}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

QUEUE_IDS = [420, 440, 400]  # SoloQ, Flex, Reclutamiento


def extract_all():
    """
    Extrae todas las partidas de los summoners dentro del año 2025,
    para las queues de interés, evitando duplicados.
    Maneja jugadores con miles de partidas usando paginación automática.
    """
    processed_matches = load_processed_matches()
    summoners = load_summoners()

    # Fechas de inicio y fin del año 2025
    start_date = datetime.datetime(2025, 1, 1)
    end_date   = datetime.datetime(2025, 12, 31, 23, 59, 59)
    start_ts = int(time.mktime(start_date.timetuple()))
    end_ts   = int(time.mktime(end_date.timetuple()))

    for s in summoners:
        riot_id = s["riot_id"]
        tag = s["tag"]

        print(f"\nProcessing {riot_id}#{tag}")
        puuid = get_puuid_by_riot_id(riot_id, tag)

        for qid in QUEUE_IDS:
            print(f"\nFetching matches from queue {qid}...")
            last_ts = end_ts  # Empezamos desde el final del año

            while True:
                # Pedimos hasta 100 partidas antes de last_ts
                match_ids = get_match_ids(puuid, count=100, queue=qid, end_time=last_ts)

                if not match_ids:
                    break  # No quedan partidas en este rango

                for match_id in match_ids:
                    if match_id in processed_matches:
                        print(f"Skipping {match_id} from queue {qid}")
                        continue

                    print(f"Extracting {match_id} from queue {qid}")
                    match_data = get_match_details(match_id)
                    save_raw_match(match_id, match_data)
                    processed_matches.add(match_id)

                # Ajustar el timestamp para la siguiente request
                # La API devuelve los matches en orden descendente, tomamos el último
                # Extraemos el timestamp de cada match (parte después del guion bajo en los ID)
                last_ts = min([int(match_id.split("_")[1]) for match_id in match_ids]) - 1

                # Si el último match es anterior al inicio del año, terminamos
                if last_ts < start_ts:
                    break

    print("\nExtraction complete!")



if __name__ == "__main__":
    extract_all()
