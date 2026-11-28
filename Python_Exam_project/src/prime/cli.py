from datetime import date
import typer
from loguru import logger
from prime.config import Settings

app = typer.Typer(help="Система мониторинга ПРАЙМ")

@app.command()
def report(report_date: date = typer.Argument(..., help="Дата отчёта в формате ГГГГ-ММ-ДД")) -> None:
    """Полный отчет за конкретную дату."""
    settings = Settings()
    logger.info(f"Запуск report за дату {report_date}")
    typer.echo(f"Отчет за {report_date} сформирован (заглушка).")

@app.command()
def replay() -> None:
    """Обработка следующего дня из истории."""
    settings = Settings()
    logger.info("Запуск replay")
    typer.echo("Replay выполнен (заглушка).")

@app.command()
def backfill(start: date = typer.Argument(...), end: date = typer.Argument(...)) -> None:
    """Пересчет периода без отправки в Telegram."""
    settings = Settings()
    logger.info(f"Запуск backfill с {start} по {end}")
    typer.echo(f"Backfill {start} → {end} выполнен (заглушка).")