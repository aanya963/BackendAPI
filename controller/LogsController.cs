using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("api/[controller]")]

public class LogsController : ControllerBase
{
    private readonly AppDbContext _context;

    public LogsController(AppDbContext context)
    {
        _context = context;
    }

    [HttpPost]
    public async Task<IActionResult> AddLog([FromBody] Log log)
    {
        Console.WriteLine($"\n👉 [.NET] Received log: {log.Service} | {log.Message} | {log.Latency}");

        log.Timestamp = DateTime.UtcNow;

        _context.Logs.Add(log);
        await _context.SaveChangesAsync();

        Console.WriteLine("👉 [.NET] Saved to DB");

        return Ok(log);
    }
    
    [HttpGet]
    public IActionResult GetLogs()
    {
        return Ok(_context.Logs.ToList());
    }
    //Query optimization
    //Filters logs where latency > 1000 ms
    // Sorts latest first

    [HttpGet("slow")]
    public IActionResult GetSlowLogs()
    {
        var slowLogs = _context.Logs
            .Where(log => log.Latency > 1000)
            .OrderByDescending(log => log.Timestamp)
            .ToList();

        return Ok(slowLogs);
    }

    [HttpGet("service/{serviceName}")]
    public IActionResult GetLogsByService(string serviceName)
    {
        var logs = _context.Logs
            .Where(log => log.Service.ToLower() == serviceName.ToLower())
            .OrderByDescending(log => log.Timestamp)
            .ToList();

        return Ok(logs);
    }

    [HttpDelete("all")]
    public async Task<IActionResult> DeleteAllLogs()
    {
        _context.Logs.RemoveRange(_context.Logs);
        await _context.SaveChangesAsync();

        return Ok("All logs deleted");
    }
}