@echo off
echo Installing SambaNova requirements...
pip install Flask==2.3.3
pip install Flask-CORS==4.0.0
pip install python-dotenv==1.0.0
pip install openai>=1.0.0

echo.
echo Creating .env file...
if not exist .env (
    echo # SambaNova API Key
    echo SAMBA_API_KEY=5f583be5-0004-41b8-9300-50f2a35d52c5
    echo.
    echo # Flask settings
    echo FLASK_SECRET_KEY=your-generated-secret-key-here
    echo DEBUG=True
    echo PORT=5000
) > .env

echo.
echo Installation complete!
echo.
echo Next steps:
echo 1. Update .env file with your actual secret key
echo 2. Run: python test_sambanova.py
echo 3. Run: python app.py
pause