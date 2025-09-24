using System.Collections.Generic;
using LiveChartsCore;
using LiveChartsCore.SkiaSharpView;

namespace BatteryVisualizer.ViewModels
{
    public class MainViewModel
    {
        public IEnumerable<ISeries> CapacitySeries { get; }
        public IEnumerable<ISeries> SOHSeries { get; }

        public List<Axis> CapacityXAxes { get; }
        public List<Axis> CapacityYAxes { get; }
        public List<Axis> SOHXAxes { get; }
        public List<Axis> SOHYAxes { get; }

        public MainViewModel()
        {
            // Örnek veriler
            CapacitySeries = new ISeries[]
            {
                new LineSeries<double>
                {
                    Values = new double[] { 100, 96, 93, 90, 86, 83, 80 }
                }
            };

            SOHSeries = new ISeries[]
            {
                new LineSeries<double>
                {
                    Values = new double[] { 1.00, 0.97, 0.95, 0.92, 0.89, 0.86, 0.83 }
                }
            };

            CapacityXAxes = new() { new Axis { Name = "Cycle" } };
            CapacityYAxes = new() { new Axis { Name = "Capacity (Ah)" } };
            SOHXAxes = new() { new Axis { Name = "Cycle" } };
            SOHYAxes = new() { new Axis { Name = "SOH" } };
        }
    }
}
