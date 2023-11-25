from plugins.database import Connect

create_total_files = """
CREATE TABLE IF NOT EXISTS total_file (
    id SERIAL PRIMARY KEY,
    file_id TEXT NOT NULL,
    user_id BIGINT NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

create_deleted_files = """
CREATE TABLE IF NOT EXISTS deleted_file (
    id SERIAL PRIMARY KEY,
    file_id TEXT NOT NULL,
    user_id BIGINT NOT NULL,
    delete_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

Connect(create_total_files)
Connect(create_deleted_files)

def add_total_files(file_id, user_id):
    query = "INSERT INTO total_file (file_id, user_id) VALUES (%s, %s);"
    Connect(query, (file_id, user_id))

def add_deleted_files(file_id, user_id):
    query = "INSERT INTO deleted_file (file_id, user_id) VALUES (%s, %s);"
    Connect(query, (file_id, user_id))

def get_total_files_count():
    query = "SELECT COUNT(*) FROM total_file;"
    result = Connect(query, fetch=True)
    return result[0][0] if result else 0

def get_deleted_files_count():
    query = "SELECT COUNT(*) FROM deleted_file;"
    result = Connect(query, fetch=True)
    return result[0][0] if result else 0
