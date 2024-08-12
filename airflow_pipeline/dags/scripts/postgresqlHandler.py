from sqlalchemy import create_engine


def save_data(data):
    engine = create_engine('postgresql://dsa:dsa@192.168.2.79:5432/dsafinal')

    data.to_sql('sales', engine, if_exists='replace', index=False)

    print("data stored in postgresql")
