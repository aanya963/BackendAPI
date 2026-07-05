using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container
builder.Services.AddControllers();         
builder.Services.AddEndpointsApiExplorer(); 
builder.Services.AddSwaggerGen();          

builder.Services.AddHttpClient();           

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql("Host=localhost;Database=logsdb;Username=postgres;Password=admin"));


// Add this BEFORE app.UseHttpsRedirection()
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowFrontend", policy =>
    {
        policy.WithOrigins("http://127.0.0.1:5500", "http://localhost:5500")
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});

var app = builder.Build();

// Add this BEFORE app.UseAuthorization()
app.UseCors("AllowFrontend");

// Configure the HTTP request pipeline
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers(); // 👈 IMPORTANT (maps your AiController)
Console.WriteLine("branch -2 ");
app.Run();