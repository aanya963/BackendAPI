# Create project : 
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

# Include Swagger libraries : 
    dotnet add package Swashbuckle.AspNetCore


# Connect .NET to DB : We'll use Entity Framework Core (ORM)
    dotnet add package Microsoft.EntityFrameworkCore
    dotnet add package Npgsql.EntityFrameworkCore.PostgreSQL
    dotnet add package Microsoft.EntityFrameworkCore.Tools


    Microsoft.EntityFrameworkCore 👉 This is the main ORM (Object Relational Mapper)
    💡 Meaning: Instead of writing SQL like:
    INSERT INTO Logs VALUES (...)
    You write C#: _context.Logs.Add(log);
    👉 EF converts it to SQL internally.

    Npgsql.EntityFrameworkCore.PostgreSQL 👉 This connects EF Core to PostgreSQL.
    Without this: EF doesn’t know how to talk to PostgreSQL
    Think:  EF = brain
            Npgsql = translator


    Microsoft.EntityFrameworkCore.Tools 👉 This gives you commands like:
            dotnet ef migrations add
            dotnet ef database update

            👉 Used for:
                creating tables
                updating schema

# Migration = “sync code → database”
dotnet ef migrations add InitialCreate
    
# Actually runs SQL → creates table
dotnet ef database update


# Install Redis
    brew install redis
    brew services start redis

# Install Python Client
    pip install redis



## LOAD TEST
1. brew install k6
2. Create load_test.js