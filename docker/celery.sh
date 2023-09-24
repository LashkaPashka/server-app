#!/bin/bash

celery --app=app.tasks.app_celery:celery worker -l INFO
