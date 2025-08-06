<template>
  <div>
    <Bar v-if="isValidChartData" :data="chartData" :options="chartOptions" />
    <p v-else>No hay datos para mostrar.</p>
  </div>
</template>

<script>
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js';
import { Bar } from 'vue-chartjs';

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
);

export default {
  name: 'BarChart',
  components: { Bar },
  props: {
    chartData: {
      type: Object,
      default: null,
    },
  },
  computed: {
    chartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
        },
      };
    },
    isValidChartData() {
      return (
        this.chartData &&
        typeof this.chartData === 'object' &&
        Array.isArray(this.chartData.datasets) &&
        this.chartData.datasets.length > 0
      );
    },
  },
};
</script>

<style scoped>
div {
  height: 300px;
}
</style>
