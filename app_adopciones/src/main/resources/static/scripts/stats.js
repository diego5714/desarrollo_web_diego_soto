// Esperamos a que el DOM esté cargado para empezar a dibujar
document.addEventListener("DOMContentLoaded", () => {
  // Llamamos a las funciones para cargar cada gráfico
  loadDailyPublicationsChart();
  loadPetTypeChart();
  loadMonthlyAdoptionsChart();
});

/**
 * GRÁFICO 1: Publicaciones Diarias (Gráfico de Línea)
 * Endpoint: /api/statistics/daily_publications
 * JSON: [{"fecha": "2025-10-24", "cantidad": 5}, ...]
 */
async function loadDailyPublicationsChart() {
  try {
    const response = await fetch("/api/statistics/daily_publications");
    const data = await response.json();

    // Transformamos los datos al formato de HighCharts: [timestamp, valor]
    const chartData = data
      .map((item) => [
        new Date(item.fecha).getTime(), // Eje X: Convertir "YYYY-MM-DD" a timestamp
        item.cantidad, // Eje Y: Cantidad
      ])
      .sort((a, b) => a[0] - b[0]); // Ordenar por fecha (ascendente)

    // Creamos el gráfico
    Highcharts.chart("chart-container-daily", {
      chart: {
        type: "line",
      },
      title: {
        text: "Publicaciones Diarias",
      },
      xAxis: {
        type: "datetime",
        title: { text: "Fecha" },
      },
      yAxis: {
        title: {
          text: "Cantidad de Avisos",
        },
      },
      series: [
        {
          name: "Avisos por día",
          data: chartData,
        },
      ],
    });
  } catch (error) {
    console.error("Error al cargar gráfico diario:", error);
  }
}

/**
 * GRÁFICO 2: Proporción de Tipos de Mascota (Gráfico de torta)
 * Endpoint: /api/statistics/pet_type_proportion
 * JSON: [{"tipo": "gato", "porcentaje": 25.0}, {"tipo": "perro", "porcentaje": 75.0}]
 */
async function loadPetTypeChart() {
  try {
    const response = await fetch("/api/statistics/pet_type_proportion");
    const data = await response.json();

    // Transformar datos al formato de Highcharts: { name, y }
    const chartData = data.map((item) => ({
      name: item.tipo.charAt(0).toUpperCase() + item.tipo.slice(1), // "gato" -> "Gato"
      y: item.porcentaje,
    }));

    // Creamos el gráfico
    Highcharts.chart("chart-container-proportion", {
      chart: {
        type: "pie",
      },
      title: {
        text: "Proporción de Tipos de Mascota",
      },
      tooltip: {
        // Muestra "Gato: 25.0%"
        pointFormat: "{series.name}: <b>{point.percentage:.1f}%</b>",
      },
      plotOptions: {
        pie: {
          allowPointSelect: true,
          cursor: "pointer",
          dataLabels: {
            enabled: true,
            format: "<b>{point.name}</b>: {point.percentage:.1f} %",
          },
        },
      },
      series: [
        {
          name: "Proporción",
          colorByPoint: true,
          data: chartData,
        },
      ],
    });
  } catch (error) {
    console.error("Error al cargar gráfico de proporción:", error);
  }
}

/**
 * GRÁFICO 3: Adopciones Mensuales (Gráfico de Barras)
 * Endpoint: /api/statistics/monthly_adoptions
 * JSON: {"categories": ["2024-11", ...], "series": [{"name": "Gatos", "data": [5, ...]}, ...]}
 */
async function loadMonthlyAdoptionsChart() {
  try {
    const response = await fetch("/api/statistics/monthly_adoptions");
    const data = await response.json();

    // Creamos el gráfico
    Highcharts.chart("chart-container-monthly", {
      chart: {
        type: "column",
      },
      title: {
        text: "Publicaciones en los Últimos 12 Meses",
      },
      xAxis: {
        categories: data.categories,
        title: { text: "Mes" },
      },
      yAxis: {
        min: 0,
        title: {
          text: "Cantidad de Publicaciones",
        },
      },
      series: data.series,
    });
  } catch (error) {
    console.error("Error al cargar gráfico mensual:", error);
  }
}
