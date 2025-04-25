from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()
ROOT_PATH = os.getenv("ROOT_PATH")

devices_path = f"file:///{os.path.join(ROOT_PATH, 'devices.csv').replace(os.sep, '/')}"
realtime_path = f"file:///{os.path.join(ROOT_PATH, 'realtime_simulated.csv').replace(os.sep, '/')}"


# Set up the Flink environment
env = StreamExecutionEnvironment.get_execution_environment()
settings = EnvironmentSettings.in_streaming_mode()
t_env = StreamTableEnvironment.create(env, environment_settings=settings)

# Register real-time energy table with corrected timestamp handling and watermarking
t_env.execute_sql(f"""
    CREATE TEMPORARY TABLE real_time_energy (
        switch_id STRING,
        timestamp TIMESTAMP(3),  -- Use TIMESTAMP type with precision
        power_consumption DOUBLE,
        WATERMARK FOR timestamp AS timestamp - INTERVAL '5' SECOND  -- Proper watermark definition
    ) WITH (
        'connector' = 'filesystem',
        'path' = '{realtime_path}',
        'format' = 'csv'
    )
""")

# Register devices table
t_env.execute_sql(f"""
    CREATE TEMPORARY TABLE devices (
        switch_id STRING,
        name STRING,
        location STRING,
        device_type STRING,
        max_power_rating DOUBLE
    ) WITH (
        'connector' = 'filesystem',
        'path' = '{devices_path}',
        'format' = 'csv'
    )
""")

# Anomaly detection query: Join real-time energy data with devices and detect anomalies
anomalies = t_env.sql_query("""
    SELECT 
        r.switch_id,
        d.name,
        d.location,
        r.timestamp,
        r.power_consumption,
        d.max_power_rating
    FROM real_time_energy AS r
    JOIN devices AS d
    ON r.switch_id = d.switch_id
    WHERE r.power_consumption > d.max_power_rating
""")

# Execute the query and print detected anomalies
anomalies.execute().print()
