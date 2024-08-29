1. Install docker desktop

2. Build docker image:

   docker build --pull --rm -f "dockerfile" -t restaurants:latest "."

3. Docker compose up:

   docker compose -f "docker-compose.yml" up -d --build

4. Go to Airflow: http://localhost:8080/home

   Username: admin

   Password: Go to your folder. airflow > logs > standalone_admin_password.txt
