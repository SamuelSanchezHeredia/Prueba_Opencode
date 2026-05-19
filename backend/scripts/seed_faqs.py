import argparse
from pathlib import Path

import psycopg


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--database-url", required=True)
    parser.add_argument("--seed", default="../migrations/002_seed_faqs.sql")
    args = parser.parse_args()

    seed_path = Path(__file__).resolve().parent / args.seed
    sql = seed_path.read_text(encoding="utf-8")

    with psycopg.connect(args.database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()


if __name__ == "__main__":
    main()
