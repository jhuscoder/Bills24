from . import *

# Database Settings (e.g., PostgreSQL)
DB_NAME=env('DB_NAME', default='the3prime_Bills24')
DB_USER=env('DB_USER', default='postgres')
DB_PASSWORD=env('DB_PASSWORD', default='(@#postgres@#)')
DB_HOST=env('DB_HOST', default='localhost')
DB_PORT=5432