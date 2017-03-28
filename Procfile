heroku ps:scale web=1
heroku addons:add heroku-postgresql:dev
heroku pg:promote HEROKU_POSTGRESQL_COLOR
web: python transfix_api.py