from pathlib import Path

base_path = Path(__file__).parent.absolute()

sql_engine_url = f'sqlite:///{base_path / "db.sqlite3"}'
