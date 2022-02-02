var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => "Hello World!");

app.MapPost("/SetBrewTemp/", (temp) => $"heelo {temp}");

app.Run("http://localhost:3000");