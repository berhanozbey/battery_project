namespace BatteryVisualizer.Models
{
    public class BatteryData
    {
        public int Cycle { get; set; }
        public double Capacity { get; set; }
        public double SOH { get; set; }
        public double RUL { get; set; }
        public string Group { get; set; }
    }
}
