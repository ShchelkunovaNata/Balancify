# обычно я использую poetry, поэтому пока не разобралась как использовать файл, чтоб он использовал env
# поэтому пока это можно использовать чтоб скопировать и вставить =)

# Run the server
serve:
	python3  manage.py runserver --settings wallet_wise.settings_local

# Make migrations and migrate
migrate:
	python3 manage.py migrate --fake --settings wallet_wise.settings_local
	python3 manage.py makemigrations --settings wallet_wise.settings_local
	python3 manage.py migrate --settings wallet_wise.settings_local
