var builder = WebApplication.CreateBuilder(args);

// Add services to the container
builder.Services.AddControllers();          // 👈 IMPORTANT (for controllers)
builder.Services.AddEndpointsApiExplorer(); // 👈 for Swagger
builder.Services.AddSwaggerGen();           // 👈 for Swagger UI

builder.Services.AddHttpClient();           // 👈 for calling Python service

var app = builder.Build();

// Configure the HTTP request pipeline
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers(); // 👈 IMPORTANT (maps your AiController)

app.Run();