using Microsoft.AspNetCore.Mvc;
using System.Net.Http;
using System.Threading.Tasks;
using System.Net.Http.Json;
using System.Security.Authentication.ExtendedProtection;

namespace BackendAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class AiController : ControllerBase
    {
        private readonly HttpClient _httpClient;
        private readonly AppDbContext _context;

        public AiController(IHttpClientFactory httpClientFactory, AppDbContext context)
        {
            _httpClient = httpClientFactory.CreateClient();
            _context=context;
        }


        [HttpPost("analyze")]
        public async Task<IActionResult> AnalyzeWithLogs(string serviceName)
        {
            // Step 1: Fetch relevant logs
            //querying DB
            var logs = _context.Logs
                        .Where(log => log.Service.ToLower() == serviceName.ToLower())
                        .OrderByDescending(log => log.Timestamp)
                        .Take(5)
                        .ToList();
           
            // 2️⃣ Convert to string list
            //Converting structured data → readable text
            var logMessages = logs.Select(log =>
                $"{log.Service}: {log.Message}, latency: {log.Latency}ms"
            ).ToList();

            // 3️⃣ Prepare request for Python
            var requestData = new
            {
                query = $"Why is {serviceName} slow?",
                logs = logMessages
            };

            // 4️⃣ Call Python service
            var response = await _httpClient.PostAsJsonAsync(
                "http://localhost:8000/analyze",
                requestData
            );

            var content = await response.Content.ReadAsStringAsync();

            return Ok(new {aiResponse = content});
        }
    }
}