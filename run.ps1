Write-Host "Starting Dabi Jutti House..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Make sure PostgreSQL is running first. Run: .\setup_db.ps1" -ForegroundColor Yellow
Write-Host ""
python manage.py migrate
python manage.py seed_data
python manage.py runserver
