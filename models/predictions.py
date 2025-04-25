# from models.database import get_db
# import pandas as pd
#
#
# def get_predictions():
#     db = get_db()
#     predictions = db.execute(
#         'SELECT timestamp, power_consumption FROM predictions ORDER BY timestamp'
#     ).fetchall()
#
#     return predictions
#
#
# def get_todays_predictions():
#     db = get_db()
#     predictions = db.execute(
#         'SELECT timestamp, power_consumption FROM predictions WHERE DATE(timestamp) = DATE("now") ORDER BY timestamp'
#     ).fetchall()
#
#     return predictions
#
#
# def get_hourly_average():
#     db = get_db()
#     predictions = db.execute('''
#         SELECT
#             strftime('%H', timestamp) as hour,
#             AVG(power_consumption) as avg_power
#         FROM predictions
#         WHERE DATE(timestamp) = DATE("now")
#         GROUP BY strftime('%H', timestamp)
#         ORDER BY hour
#     ''').fetchall()
#
#     return predictions

# Updated models/predictions.py
from models.database import get_db
import pandas as pd
from datetime import datetime, timedelta


def get_predictions():
    db = get_db()
    predictions = db.execute(
        'SELECT timestamp, power_consumption FROM predictions ORDER BY timestamp LIMIT 1000'
    ).fetchall()

    return predictions


def get_next_days_predictions(days=7):
    db = get_db()
    today = datetime.now().strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')

    predictions = db.execute('''
        SELECT timestamp, power_consumption FROM predictions 
        WHERE DATE(timestamp) >= DATE(?) AND DATE(timestamp) <= DATE(?)
        ORDER BY timestamp
    ''', (today, end_date)).fetchall()

    return predictions


def get_todays_predictions():
    db = get_db()
    today = datetime.now().strftime('%Y-%m-%d')

    predictions = db.execute('''
        SELECT timestamp, power_consumption FROM predictions 
        WHERE DATE(timestamp) = DATE(?)
        ORDER BY timestamp
    ''', (today,)).fetchall()

    return predictions


def get_hourly_average():
    db = get_db()
    today = datetime.now().strftime('%Y-%m-%d')

    predictions = db.execute('''
        SELECT 
            strftime('%H', timestamp) as hour,
            AVG(power_consumption) as avg_power
        FROM predictions 
        WHERE DATE(timestamp) = DATE(?)
        GROUP BY strftime('%H', timestamp)
        ORDER BY hour
    ''', (today,)).fetchall()

    return predictions