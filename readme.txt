Hallo! This script is written to download RockyRaccoons demos from csc cs website.

Make sure to install python, 
    then run the following command on your command line:

    pip install psycopg2 requests python-dotenv

This tells the python package manager to install a PostgreSQL adapter for Python,
    and installing "requests" helps us to parse data from the URL in our script.
    Installing python-dotenv adds security so only you can see your database info.


In the .env file, add your database information. This file adds security to your
    database information. Other programs cannot read the .env file.

    for example: 
        DB_NAME="my-database-name"
        DB_USER="my-username"
        DB_PASSWORD="password1234"
        DB_HOST="localhost"
        DB_PORT="5432"

Finally, make sure to edit the following to the appropriate directory:
    CS_DM_PATH
    DEMO_SAVE_DIR