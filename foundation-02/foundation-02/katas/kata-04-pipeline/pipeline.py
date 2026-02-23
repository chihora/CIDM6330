import csv
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Generator, Iterable, Optional, Tuple


@dataclass(frozen=True)
class GdpRow:
    date: str
    value: float


def extract_rows(csv_path: Path) -> Generator[Tuple[int, dict], None, None]:
    """
    Generator that yields (row_number, row_dict) to support large files.
    """
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):  # header line is 1
            yield i, row


def validate_and_transform(rows: Iterable[Tuple[int, dict]], log_path: Path) -> Generator[GdpRow, None, None]:
    """
    Validates rows; logs malformed records; converts types.
    """
    log_path.parent.mkdir(parents=True, exist_ok=True)

    def log(msg: str) -> None:
        with log_path.open("a", encoding="utf-8") as lf:
            lf.write(msg + "\n")

    for line_no, row in rows:
        date = (row.get("date") or "").strip()
        value_raw = (row.get("value") or "").strip()

        if not date:
            log(f"[INVALID] line {line_no}: missing date -> {row}")
            continue

        try:
            value = float(value_raw)
        except ValueError:
            log(f"[INVALID] line {line_no}: invalid value '{value_raw}' -> {row}")
            continue

        yield GdpRow(date=date, value=value)


def init_db(db_path: Path, schema_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    schema_sql = schema_path.read_text(encoding="utf-8")
    with sqlite3.connect(db_path) as conn:
        conn.executescript(schema_sql)
        conn.commit()


def load_rows(db_path: Path, data: Iterable[GdpRow]) -> int:
    """
    Idempotent load: INSERT OR REPLACE by PRIMARY KEY (date).
    Returns number of rows written.
    """
    rows = list(data)  # small example; still OK. For huge files, batch insert in chunks.
    with sqlite3.connect(db_path) as conn:
        conn.executemany(
            "INSERT OR REPLACE INTO gdp_observations(date, value) VALUES (?, ?)",
            [(r.date, r.value) for r in rows],
        )
        conn.commit()
    return len(rows)


def compute_growth_rates(db_path: Path) -> None:
    """
    Calculates growth rate compared to previous row and updates table.
    """
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT date, value FROM gdp_observations ORDER BY date ASC")
        data = cur.fetchall()

        prev_value: Optional[float] = None
        updates = []
        for date, value in data:
            if prev_value is None:
                growth = None
            else:
                growth = ((value - prev_value) / prev_value) * 100.0 if prev_value != 0 else None
            updates.append((growth, date))
            prev_value = value

        cur.executemany("UPDATE gdp_observations SET growth_rate = ? WHERE date = ?", updates)
        conn.commit()


def generate_report(db_path: Path, report_path: Path) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM gdp_observations")
        count = cur.fetchone()[0]

        cur.execute("SELECT MIN(value), MAX(value), AVG(value) FROM gdp_observations")
        min_v, max_v, avg_v = cur.fetchone()

        cur.execute("SELECT MIN(growth_rate), MAX(growth_rate), AVG(growth_rate) FROM gdp_observations WHERE growth_rate IS NOT NULL")
        gr = cur.fetchone()
        min_gr, max_gr, avg_gr = gr if gr else (None, None, None)

    md = []
    md.append("# Kata 4 — Data Transformation Pipeline Report\n")
    md.append(f"- Total rows in SQLite: **{count}**\n")
    md.append("## GDP Value Stats\n")
    md.append(f"- Min: **{min_v:.2f}**\n- Max: **{max_v:.2f}**\n- Avg: **{avg_v:.2f}**\n")
    md.append("\n## Growth Rate Stats\n")
    if min_gr is None:
        md.append("- Not enough data to compute growth rates.\n")
    else:
        md.append(f"- Min: **{min_gr:.2f}%**\n- Max: **{max_gr:.2f}%**\n- Avg: **{avg_gr:.2f}%**\n")

    report_path.write_text("".join(md), encoding="utf-8")


def run_pipeline(
    raw_csv: Path,
    db_path: Path,
    schema_path: Path,
    report_path: Path,
    log_path: Path,
    dry_run: bool = False,
) -> int:
    init_db(db_path, schema_path)

    extracted = extract_rows(raw_csv)
    transformed = validate_and_transform(extracted, log_path)

    if dry_run:
        # Count how many valid rows would be loaded
        rows = list(transformed)
        print(f"[DRY RUN] Would load {len(rows)} valid rows into {db_path}")
        return 0

    written = load_rows(db_path, transformed)
    compute_growth_rates(db_path)
    generate_report(db_path, report_path)

    print(f"Loaded {written} rows into {db_path}")
    print(f"Wrote report to {report_path}")
    print(f"Validation log at {log_path}")
    return 0


if __name__ == "__main__":
    base = Path("foundation-02/katas/kata-04-pipeline")
    raise SystemExit(
        run_pipeline(
            raw_csv=base / "data" / "raw_gdp.csv",
            db_path=base / "output" / "gdp.db",
            schema_path=base / "schema.sql",
            report_path=base / "report.md",
            log_path=base / "output" / "validation.log",
            dry_run=False,
        )
    )
