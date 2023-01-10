#!/bin/bash
gcloud functions deploy python-http-function \
--gen2 \
--runtime=python310 \
--region=us-central1 \
--source=. \
--entry-point=update_youtube_data \
--trigger-http \
--allow-unauthenticated