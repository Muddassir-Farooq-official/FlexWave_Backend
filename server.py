from fastapi import FastAPI
import pymysql

config = {
    'host': 'srv865.hstgr.io',
    'user': 'u441049818_SDP',
    'password': 'Flexwave@193708',
    'database': 'u441049818_SDP',
}
app=FastAPI()

def create_registration_table():
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS Registration (
                id INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(255) NOT NULL,
                Email VARCHAR(255) NOT NULL,
                Phone VARCHAR(15) NOT NULL,
                Select_Field VARCHAR(255) NOT NULL,
                Preference VARCHAR(255),
                Coupon_Code VARCHAR(50),
                Total_Amount DECIMAL(10, 2) NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(create_table_query)
            connection.commit()
            print("Table 'Registration' ensured to exist.")
    except pymysql.MySQLError as e:
        print(f"Error creating table: {e}")
    finally:
        connection.close()

@app.post("/register")
async def register(
    Name: str,
    Email: str,
    Phone: str,
    Select_Field: str,
    Preference: str = None,
    Coupon_Code: str = None,
    Total_Amount: float = 0.0
):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            insert_query = """
            INSERT INTO Registration (Name, Email, Phone, Select_Field, Preference, Coupon_Code, Total_Amount)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (Name, Email, Phone, Select_Field, Preference, Coupon_Code, Total_Amount))
            connection.commit()
            return {"message": "Registration successful!"}
    except pymysql.MySQLError as e:
        return {"error": str(e)}
    finally:
        connection.close()
   


@app.get("/Fields")
async def Fields():
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            # Correct query to fetch all values from SDP_Fields table
            query = "SELECT * FROM SDP_Fields"
            cursor.execute(query)
            
            # Fetch all the results from the query
            fields = cursor.fetchall()

            
            return {"fields": fields}
        
    except pymysql.MySQLError as e:
        return {"error": str(e)}
    finally:
        connection.close()
