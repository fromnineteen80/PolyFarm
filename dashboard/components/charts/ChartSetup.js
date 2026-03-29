import {
  Chart as ChartJS,
  CategoryScale, LinearScale, LogarithmicScale,
  PointElement, LineElement, BarElement,
  ArcElement, Title, Tooltip, Legend, Filler,
} from 'chart.js'
import { MatrixController, MatrixElement } from 'chartjs-chart-matrix'

ChartJS.register(
  CategoryScale, LinearScale, LogarithmicScale,
  PointElement, LineElement, BarElement,
  ArcElement, Title, Tooltip, Legend, Filler,
  MatrixController, MatrixElement
)

// Register zoom plugin client-side only (hammerjs needs window)
if (typeof window !== 'undefined') {
  import('chartjs-plugin-zoom').then(mod => {
    ChartJS.register(mod.default)
  })
}

export default ChartJS
