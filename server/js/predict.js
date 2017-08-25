function str2list(s) {
    return eval(s.replace(/&#39;/g, "'").replace(/None/g, "null").replace(/\(/g, "[").replace(/\)/g, "]"))
}


function getOption(id, real, predict) {
    // 指定图表的配置项和数据
    real = str2list(real)
    
    predict = str2list(predict)
    var option = {
        title: {
            text: '预测/实际曲线图 ID＝' + id
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
            data: ['real', 'p0', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6']
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
                name: 'p0',
                type: 'line',
                large: true,
                symbolSize: 3,
                data: predict[0]
            },
            {
                name: 'p1',
                type: 'line',
                large: true,
                symbolSize: 3,
                data: predict[1]
            },
            {
                name: 'p2',
                type: 'line',
                large: true,
                symbolSize: 3,
                data: predict[2]
            },
            {
                name: 'p3',
                type: 'line',
                large: true,
                symbolSize: 3,
                data: predict[3]
            },
            {
                name: 'p4',
                type: 'line',
                large: true,
                symbolSize: 3,
                data: predict[4]
            },
            {
                name: 'p5',
                type: 'line',
                large: true,
                symbolSize: 3,
                data: predict[5]
            },
            {
                name: 'p6',
                type: 'line',
                large: true,
                symbolSize: 3,
                data: predict[6]
            }

        ]
    };


    return option
}