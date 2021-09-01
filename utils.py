#!/usr/bin/env python
# -*-coding:utf-8 -*-
 
'''
File      :   utils.py
Created on:   2021/08/31 18:59:58
 
@Author   :   Helder C. R. Oliveira
@Version  :   1.0
@Contact  :   helder.ro@outlook.com
@License  :   (C) Copyright 2021, Helder C. R. Oliveira
@Desc     :   None
'''

import numpy as np

from PyQt5.QtWidgets import QMessageBox, QToolTip
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtChart import QChart, QChartView, QBarSet, QValueAxis, QPercentBarSeries, QBarCategoryAxis, QBarSeries, QHorizontalPercentBarSeries
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class Data(object):
    def __init__(self) -> None:
        super().__init__()

    def getAll(self):
        # Organization by column:
        # 0: 'Age', 1: 'Gender', 2: 'PofS', 3: 'IPR', 
        # 4: 'FNR', 5: 'FPR', 6: 'CovS', 7: 'TPos', 8: 'IFR'
        # values in %
        vars_values = [
            [0.0043, 0.45, 0.54, 0.00000000, 0.000, 0.0000e+00, 0.08584559, 0.85189975, 0.00745049],
            [0.0062, 0.55, 0.46, 0.00003596, 0.000, 1.5000e-04, 0.09385208, 0.14810025, 0.04381822],
            [0.0933, 0.0,  0.0,  0.01018150, 0.000, 3.0700e-03, 0.82030234, 0,          0.16182437],
            [0.1151, 0.0,  0.0,  0.00278046, 0.001, 3.0730e-02, 0,          0,          0.30627996],
            [0.0898, 0.0,  0.0,  0.01126105, 0.00037, 1.4692e-01, 0,          0,          0.28288477],
            [0.1071, 0.0,  0.0,  0.02618763, 0.00549, 3.1922e-01, 0,          0,          0.13483421],
            [0.2490, 0.0,  0.0,  0.89844829, 0.02719, 3.1805e-01, 0,          0,          0.04193988],
            [0.2740, 0.0,  0.0,  0.02624331, 0.08864, 1.4792e-01, 0,          0,          0.01408657],
            [0.0581, 0.0,  0.0,  0.01132949, 0.18668, 3.0510e-02, 0,          0,          0.00501753],
            [0.0029, 0.0,  0.0,  0.00276422, 0.25495, 3.2700e-03, 0,          0,          0.00146225],
            [0.0,    0.0,  0.0,  0.01073674, 0.23243, 1.5000e-04, 0,          0,          0.00040176],
            [0.0,    0.0,  0.0,  0.00002783, 0.13685, 1.0000e-05, 0,          0,          0],
            [0.0,    0.0,  0.0,  0.00000347, 0.05174, 0,          0,          0,          0],
            [0.0,    0.0,  0.0,    0.0,      0.01264, 0,          0,          0,          0],
            [0.0,    0.0,  0.0,    0.0,      0.00245, 0.0,          0.0,          0.0,          0.0]]

        vars_values = np.matrix(data=vars_values, dtype=np.float64)

        return vars_values


class BaseGraph(object):
    def __init__(self) -> None:
        super().__init__()

        # the default color palette is not enough, so I defined my own with 20 colors
        self.colors = ['#C977D9', '#A18AE6', '#8AA2E6', '#8BD1E7', '#8AF3CF', 
                        '#85F38E', '#BDF385', '#EDE485', '#F0B086', '#DE9F8B', 
                        '#74A3B3', '#99CC70', '#DCD68E', '#EDDFAD', '#F7E8CA', 
                        '#FFF9F3', '#FFF9F6', '#FFFBF9', '#FFFCFA', '#FFFEFD']


class AllGraph(BaseGraph):
    def __init__(self, data_values) -> None:
        super().__init__()

        series = QPercentBarSeries()
        #test = []
        for k,s in enumerate(data_values):
            #print(k, len(s))
            setI = QBarSet('{}'.format(k))
            setI.setColor(QColor(self.colors[k]))
            #print(s[0], s[1] * 100)
            #print(s[0,4] * 100)
            #test.append(s[0,4] * 100)

            values = (s[0] * 100).tolist()[0]
            setI.append(values)
            series.append(setI)  


        self.chart = QChart()
        #chart.setTheme(QChart.ChartThemeQt)
        self.chart.addSeries(series)
        #chart.addSeries(series2)
        self.chart.setTitle("DSS - Diamond Princess cruise ship")

        font = QFont()
        font.setPixelSize(14)
        font.setBold(True)

        self.chart.setTitleFont(font)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        categories = ['Age', 'Gender', 'PofS', 'IPR', 'FNR', 'FPR', 'CovS', 'TPos', 'IFR']
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        axisX.setLabelsAngle(-45)
        axisX.setTitleText('Variables')
        
        #chart.createDefaultAxes()
        self.chart.addAxis(axisX, Qt.AlignBottom)
        

        axisY = QValueAxis()
        axisY.setRange(0,100)
        axisY.setTickCount(11)
        axisY.setLabelFormat('%d')
        axisY.setTickType(QValueAxis.TicksFixed)
        axisY.setTitleText('Percentage')

        self.chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        # TODO: Y-axis set tick interval 10
        # TODO: Y-axis horizontal lines

        self.chart.legend().setVisible(False)
        self.chart.legend().setAlignment(Qt.AlignBottom)


    def getGraph(self):
        return self.chart


class AgeGraph(BaseGraph):
    def __init__(self, data_values) -> None:
        super().__init__()


        series = QBarSeries()
        for k,s in enumerate(data_values):
            setI = QBarSet('{}'.format(k))
            setI.setColor(QColor(self.colors[k]))

            values = s/3711 * 100
            print(k, values)
            setI.append(values)
            series.append(setI)        

        self.chart = QChart()
        #chart.setTheme(QChart.ChartThemeQt)
        self.chart.addSeries(series)
        #chart.addSeries(series2)
        self.chart.setTitle('Age')

        font = QFont()
        font.setPixelSize(16)
        font.setBold(True)

        self.chart.setTitleFont(font)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        categories = ['0-9','10-19','20-29','30-39','40-49','50-59','60-69','70-79','80-89','90-99']
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        axisX.setLabelsAngle(-45)
        axisX.setTitleText('Variables')
        
        self.chart.addAxis(axisX, Qt.AlignBottom)
        
        axisY = QValueAxis()
        axisY.setRange(0,100)
        axisY.setTickCount(11)
        axisY.setLabelFormat('%d')
        axisY.setTickType(QValueAxis.TicksFixed)
        axisY.setTitleText('Percentage')

        self.chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        # TODO: Y-axis set tick interval 10
        # TODO: Y-axis horizontal lines

        self.chart.legend().setVisible(False)
        self.chart.legend().setAlignment(Qt.AlignBottom)

    def getGraph(self):
        return self.chart
        