#!/bin/bash

#Exit script if error occurs
set -e


cd /home/nishil/eia-pipeline


echo "[$(date '+%Y-%m-%d %H:%M:%S UTC')] Pipeline Started"



/home/nishil/eia-pipeline/venv/bin/python \
     /home/nishil/eia-pipeline/src/scripts/ingest_daily.py

echo "[$(date '+%Y-%m-%d %H:%M:%S UTC')] Ingestion Complete"


#Version DVC

/home/nishil/eia-pipeline/venv/bin/dvc add data/raw/ercot_demand.csv

git add data/raw/ercot_demand.csv.dvc


if ! git diff --staged --quiet; then
    git commit -m "Data: Daily Ingest $(date '+%Y-%m-%d')"
    echo "[$(date '+%Y-%m-%d %H:%M:%S UTC')] New data version committed"

    /home/nishil/eia-pipeline/venv/bin/dvc push
    echo "[$(date '+%Y-%m-%d %H:%M:%S UTC')] Pushed to S3"

    git push origin master
    echo "[$(date '+%Y-%m-%d %H:%M:%S UTC')] Pushed to GitHub"

    echo "[$(date '+%Y-%m-%d %H:%M:%S UTC')] Pipeline Complete"

else
    echo "[$(date '+%Y-%m-%d %H:%M:%S UTC')] No new data - skip commit and push"
fi
