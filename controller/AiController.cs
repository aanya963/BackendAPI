using Microsoft.AspNetCore.Mvc;
using System.Net.Http;
using System.Threading.Tasks;
using System.Net.Http.Json;

namespace BackendAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class AiController : ControllerBase
    {
        private readonly HttpClient _httpClient;

        public AiController(IHttpClientFactory httpClientFactory)
        {
            _httpClient = httpClientFactory.CreateClient();
        }

        [HttpGet("test")]
        public async Task<IActionResult> TestPythonService()
        {
            var response = await _httpClient.GetAsync("http://localhost:8000/");
            var content = await response.Content.ReadAsStringAsync();

            return Ok(new { pythonResponse = content });
        }
        [HttpPost("analyze")]
        public async Task<IActionResult> Analyze()
        {
            var requestData = new
            {
                query = "Why is login slow?",
                logs = new List<string>
                {
                    "login API took 1200ms",
                    "DB query slow",
                    "timeout error"
                }
            };

            var response = await _httpClient.PostAsJsonAsync(
                "http://localhost:8000/analyze",
                requestData
            );

            var content = await response.Content.ReadAsStringAsync();

            return Ok(new { pythonResponse = content });
        }
    }
}