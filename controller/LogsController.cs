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
    public async Task<IActionResult> AddLog(Log log)
    {
        log.Timestamp = DateTime.UtcNow;

        _context.Logs.Add(log);
        await _context.SaveChangesAsync();

        return Ok(log);
    }

    [HttpGet]
    public IActionResult GetLogs()
    {
        return Ok(_context.Logs.ToList());
    }
}