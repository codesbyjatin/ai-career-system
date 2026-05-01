import pymysql

def connect():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Jatin@123",
        database="career_ai"
    )


def save_result(name, score, skills):
    conn = connect()
    cursor = conn.cursor()

    query = """
    INSERT INTO results (name, score, skills)
    VALUES (%s, %s, %s)
    """

    cursor.execute(query, (name, score, ",".join(skills)))
    conn.commit()
    conn.close()