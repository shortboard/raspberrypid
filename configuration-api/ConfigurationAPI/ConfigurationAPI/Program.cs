using ConfigurationAPI.Models;
using ConfigurationAPI.Helpers;

var builder = WebApplication.CreateBuilder(args);
const string configPath = "/config/pid.config.json";

// Add services to the container.
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

//app.Urls.Add("http://localhost:3000");
//app.Urls.Add("http://0.0.0.0:443");

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.MapGet("/", () => "Welcome to RasberryPID");

app.MapGet("/config", () =>
{
    return Results.Ok(FileHelper.LoadConfig(configPath));
})
.WithName("GetConfig");

app.MapPost("/config/brewtemp", (float brewTemp) =>
{
    var config = FileHelper.LoadConfig(configPath);
    config.BrewTargetTemp = brewTemp;
    FileHelper.WriteConfig(configPath, config);
    return Results.Ok(config);
})
.WithName("SetBrewTemp");

app.MapPost("/config/steamtemp", (float steamTemp) =>
{
    var config = FileHelper.LoadConfig(configPath);
    config.BrewTargetTemp = steamTemp;
    FileHelper.WriteConfig(configPath, config);
    return Results.Ok(config);
})
.WithName("SetSteamTemp");

app.MapPost("/config/cycletime", (float cycleTime) =>
{
    var config = FileHelper.LoadConfig(configPath);
    config.BrewTargetTemp = cycleTime;
    FileHelper.WriteConfig(configPath, config);
    return Results.Ok(config);
})
.WithName("SetCycleTime");

app.Run();

internal record WeatherForecast(DateTime Date, int TemperatureC, string? Summary)
{
    public int TemperatureF => 32 + (int)(TemperatureC / 0.5556);
}
