import { HorizontalBar } from 'vue-chartjs'
export default {
  extends: HorizontalBar,
  props: ['datas'],
  mounted () {
    var type = this.datas[2]
    var color = '#00f25A'
    if (type == 'i') color = '#00f25A'
    if (type == 's') color = '#007bff'

    this.renderChart({
        datasets: [{
            backgroundColor: [color],
            borderWidth: 0,
            data: [this.datas[0]]
            // data: [50]
        },
        {
            backgroundColor: ['yellow'],
            borderWidth: 0,
            data: [this.datas[1]]
            // data: [50]
        }
        //  { 
        //     backgroundColor: ['yellow'],
        //     borderWidth: 2,
        //     data: [this.datas[2]]
        //     // data: [50]
        // }
        ]
    },{
    legend: { //hides the legend
         display: false,
    },
       
tooltips: {
      mode: false
      // callbacks: {
      //   title: function() {},
      //   label: function() {}
      // }
    },
  animation: {
          duration: 0
      },

      scales: {
         xAxes: [
                {
         stacked: true,
          categoryPercentage: 2,
                    display: false,
                    ticks: {
                        beginAtZero: true,
                        min: 0,
                        suggestedMin: 0
                    }
                }
            ],
            yAxes: [
                {stacked: true,
                    display: false,
                    ticks: {
                        beginAtZero: true,
                        min: 0,
                        suggestedMin: 0
                    }
                }
            ],
        yAxes: [{
          stacked: true,
          barPercentage: 2,
          gridLines: {
                display:false
          }
        }]
      }

    })
},
  watch: {
  datas () {
    var type = this.datas[2]
    var color = '#00f25A'
    if (type == 'i') color = '#00f25A'
    if (type == 's') color = '#007bff'
    this.renderChart({
        datasets: [{
            backgroundColor: [color],
            borderWidth: 0,
            data: [this.datas[0]]
            // data: [50]
        },
        {
            backgroundColor: ['yellow'],
            borderWidth: 0,
            data: [this.datas[1]]
            // data: [50]
        }
        //  { 
        //     backgroundColor: ['yellow'],
        //     borderWidth: 2,
        //     data: [this.datas[2]]
        //     // data: [50]
        // }
        ]
    },{
    legend: { //hides the legend
         display: false,
    },
tooltips: {
      mode: false
      // callbacks: {
      //   title: function() {},
      //   label: function() {}
      // }
    },
  animation: {
          duration: 0
      },
      scales: {
         xAxes: [
                {
         stacked: true,
          categoryPercentage: 2,
                    display: false,
                    ticks: {
                        beginAtZero: true,
                        min: 0,
                        suggestedMin: 0
                    }
                }
            ],
            yAxes: [
                {stacked: true,
                    display: false,
                    ticks: {
                        beginAtZero: true,
                        min: 0,
                        suggestedMin: 0
                    }
                }
            ],
        yAxes: [{
          stacked: true,
          barPercentage: 2,
          gridLines: {
                display:false
          }
        }]
      }

    })
  }
}
}