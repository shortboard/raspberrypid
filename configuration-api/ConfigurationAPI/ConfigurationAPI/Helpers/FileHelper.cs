using ConfigurationAPI.Models;
using Newtonsoft.Json;

namespace ConfigurationAPI.Helpers
{
    public static class FileHelper
    {
        public static string Load(string file)
        {
            using (StreamReader r = new StreamReader(file))
            {
                return r.ReadToEnd();
            }
        }

        public static Config LoadConfig(string file)
        {
            return JsonConvert.DeserializeObject<Config>(Load(file)) ?? new Config();
        }

        public static void WriteFile(string file, string content)
        {
            File.WriteAllText(file, content);
        }

        public static void WriteConfig(string file, Config config)
        {
            WriteFile(file, JsonConvert.SerializeObject(config));
        }

    }
}
