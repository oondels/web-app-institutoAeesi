const ctx = document.getElementById("bolsa-porcentagem");
const ctx2 = document.getElementById("quantidade-por-curso");

const bolsaPorcentagem = new Chart(ctx, {
  type: "doughnut",
  data: {
    labels: ["Com Bolsa", "Sem Bolsa"],
    datasets: [
      {
        data: [
          chartVariable.porcentagem_bolsa,
          100 - chartVariable.porcentagem_bolsa,
        ],
        borderWidth: 1,
      },
    ],
  },
  options: {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  },
});

const quantidadeCurso = new Chart(ctx2, {
  type: "bar",
  data: {
    labels: ["Academia", "Jiu-Jitsu", "Boxe", "HitBox"],
    datasets: [
      {
        data: [
          chartVariable.academia,
          chartVariable.jiuJitsu,
          chartVariable.boxe,
          chartVariable.ritbox,
        ],
        borderWidth: 1,
      },
    ],
  },
  options: {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  },
});
