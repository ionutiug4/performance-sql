from db_helpers import create_speedrun_database, create_user, create_users_table

def run_db_setup():
    print("--- Starting database setup ---")
    create_speedrun_database()
    
    create_users_table()
    
    create_user(
        first_name="Ion",
        last_name="Iuga",
        email_address="ionutiuga285@gmail.com",
        is_available=True
    )
    
    print("--- Setup complete ---")
    
if __name__ == "__main__":
    run_db_setup()