using System.Windows;
using BatteryVisualizer.ViewModels;

namespace BatteryVisualizer
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            DataContext = new MainViewModel();
        }
    }
}
