Create project : 
    Step 1 — Setup Backend (.NET)

        dotnet new webapi -n BackendAPI
        cd BackendAPI
        dotnet run

        check the port from Properties -> lauchSettings.json

    Step 2 — Setup Python AI Service
        pip install fastapi uvicorn
        Create file: main.py
        uvicorn main:app --reload --port 8000
        running on : http://localhost:8000

        fastapiThe web framework — lets you define API routes with Python functionsuvicornThe ASGI server that actually runs your FastAPI app (like IIS/Kestrel for .NET)

Include Swagger libraries : 
    dotnet add package Swashbuckle.AspNetCore

