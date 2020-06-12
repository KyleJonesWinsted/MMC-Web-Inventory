# Must have psql installed and an inventory named mmc_test_inventory

export SECRET_KEY=$RANDOM
export DATABASE_URL=postgresql://localhost/mmc_test_inventory
python3 app.py