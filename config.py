from pathlib import Path

base_path = Path(__file__).parent.absolute()
sample_file_path = base_path / "sample.json"

sql_engine_url = f'sqlite:///{base_path / "db.sqlite3"}'
