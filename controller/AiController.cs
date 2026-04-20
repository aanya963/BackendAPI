using Microsoft.AspNetCore.Mvc;
using System.Net.Http;
using System.Threading.Tasks;

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
    }
}