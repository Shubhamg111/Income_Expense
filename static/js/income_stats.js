const renderIncomeChart=(data,labels)=>{

var ctx = document.getElementById("myIncomeChart").getContext('2d');
var myIncomeChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: labels,
        datasets: [{
            label: 'Last 6 Month Income ',
            data: data,
            backgroundColor: [
                'rgba(255, 99, 132, 0.5)',
                'rgba(54, 162, 235, 0.5)',
                'rgba(255, 206, 86, 0.5)',
                'rgba(75, 192, 192, 0.5)',
                'rgba(153, 102, 255, 0.5)',
                'rgba(255, 159, 64, 0.5)'
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        title: {
            display: true,
            text: 'Income Per Source In Pie Chart'
        }
        
    }
});
}
const renderIncomeChartsecond=(data,labels)=>{

    var ctx = document.getElementById("myIncomeChartsecond").getContext('2d');
    var myIncomeChartsecond = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Last 6 Month Income ',
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(153, 102, 255, 0.5)',
                    'rgba(255, 159, 64, 0.5)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Income Per Source In Line Graph'
            }
            
        }
    });
    }

const renderIncomeChartthird=(data,labels)=>{

    var ctx = document.getElementById("myIncomeChartthird").getContext('2d');
    var myIncomeChartthird = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Last 6 Month Income ',
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(153, 102, 255, 0.5)',
                    'rgba(255, 159, 64, 0.5)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Income Per Source In Bar Graph'
            }
            
        }
    });
    }

  

const getIncomeChartData=()=>{
    console.log("fetching...")
    fetch('/income/income_summary')
    .then(res=>res.json())
    .then(result=>{
        console.log("result",result)
        const source_data = result.income_source_data
        const [labels,data] = [
            Object.keys(source_data),
            Object.values(source_data)
        ]
        renderIncomeChart(data,labels)
        renderIncomeChartsecond(data,labels)
        renderIncomeChartthird(data,labels)


    })

}
document.onload = getIncomeChartData()