using Newtonsoft.Json;

namespace ConfigurationAPI.Models
{
    public class Config
    {
        [JsonProperty("brew_target_temp")]
        public float BrewTargetTemp { get; set; }
        [JsonProperty("steam_target_temp")]
        public float SteamTargetTemp { get; set; }
        [JsonProperty("p")]
        public float P { get; set; }
        [JsonProperty("i")]
        public float I { get; set; }
        [JsonProperty("d")]
        public float D { get; set; }
        [JsonProperty("cycle_time")]
        public float CycleTime { get; set; }
    }
}
