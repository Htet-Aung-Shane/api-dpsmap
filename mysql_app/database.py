import mysql.connector

# Connection Created
conn = mysql.connector.connect(
    host='127.0.0.1',
    user='poi',
    password='password',
    database='poi',
    port=3306  # Default MySQL port
)

# Use dictionary cursor for easier data extraction
cursor = conn.cursor(dictionary=True)


def get_poi():
    try:
        cursor.execute(
            "SELECT * FROM db_business_list")
        result = cursor.fetchall()

        data = []
        for row in result:
            data.append({
                "type": row['Type'],
                "st_n_eng": row['St_N_Eng']
            })

        return data

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return {'Error': e}
    finally:
        conn.close()
