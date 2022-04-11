import os

os.system(
    "docker-compose exec -T mysql mysqldump -uroot -proot barber_dev > initdb/dumps/barber_dev.sql"
)
os.system("gzip -f initdb/dumps/barber_dev.sql")
