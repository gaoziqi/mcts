function str2list(s) {
    return eval(s.replace(/&#39;/g, "'").replace(/None/g, "null").replace(/\(/g, "[").replace(/\)/g, "]"))
}


function getOption(id, real, predict) {
    // 指定图表的配置项和数据
    real = str2list(real)
    
    predict = str2list(predict)
    var option = {
        title: {
            text: '预测/实际曲线图 CODE＝' + id
        },
        tooltip: {
            trigger: 'axis',
            showDelay: 0,
            axisPointer: {
                show: true,
                type: 'cross',
                lineStyle: {
                    type: 'dashed',
                    width: 1
                }
            },
            zlevel: 1
        },
        legend: {
            data: ['real', 'predict']
        },
        grid: {

        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        xAxis: [{
            type: 'time',
        }],
        yAxis: [{
            type: 'value',
            scale: true
        }],
        series: [{
                name: 'real',
                type: 'line',
                large: true,
                symbolSize: 3,
                data: real
            },
            {
                name: 'predict',
                type: 'line',
                large: true,
                symbolSize: 3,
                data: predict
            }

        ]
    };


    return option
}