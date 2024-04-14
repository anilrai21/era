build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

shell:
	docker-compose exec web python manage.py shell_plus

test:
	docker-compose exec web python manage.py test

deprecation:
	docker-compose exec web python -Wa manage.py test

makemigrations:
	docker-compose exec web python manage.py makemigrations

migrate:
	docker-compose exec web python manage.py migrate

showmigrations:
	docker-compose exec web python manage.py showmigrations

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

isort:
	docker-compose exec web isort .

black:
	docker-compose exec web black .

lint:
	make isort && make black

pip-freeze:
	docker-compose exec web pip freeze

coverage-run:
	docker-compose run web coverage run --source='.' manage.py test

coverage-report:
	docker-compose run web coverage report


# BUILD
prod-build:
	docker-compose -f docker-compose.prod.yml build

prod-up:
	docker-compose -f docker-compose.prod.yml up

prod-makemigrations:
	docker-compose exec web python manage.py makemigrations --settings=config.settings.production

prod-migrate:
	docker-compose exec web python manage.py migrate --settings=config.settings.production

prod-collectstatic:
	docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --settings=config.settings.production

prod-createsuperuser:
	docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser --settings=config.settings.production
