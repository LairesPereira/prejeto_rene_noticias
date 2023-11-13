import psycopg2


con = psycopg2.connect(host='dpg-cl5v0ps72pts73af17m0-a.oregon-postgres.render.com', database='my_app_db_d3aj',
user='my_app_user', password='MedlZen0ZlU6owtyW4AAPPsGijPvgfi8')

cur = con.cursor()
# sql = "delete from adm_cadastrados"
sql = "insert into adm_cadastrados values (1, 'Laires', '123', 'Laires Pereira', '43394170841', true, 'lairespsoares@gmail.com')"
cur.execute(sql)
con.commit()

con.close()
