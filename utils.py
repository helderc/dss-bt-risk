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

from PyQt5.QtWidgets import QMessageBox, QToolTip, QWidget, QVBoxLayout
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtChart import QChart, QChartView, QBarSet, QValueAxis, \
                          QPercentBarSeries, QBarCategoryAxis, QBarSeries, \
                          QHorizontalPercentBarSeries
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt


class CustomTab(QChartView):
    def __init__(self, parent, tab_name) -> None:
        super().__init__(parent=parent)
        
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        if tab_name == 'All':
            data = Data().getAll()
            chart = AllGraph(data_values=data)
        elif tab_name == 'Age':
            #data = [16, 23, 347, 428, 334, 398, 923, 1015, 216, 11]
            data = [0.0043, 0.0062, 0.0933, 0.1151, 0.0898,
                    0.1071, 0.2490, 0.2740, 0.0581, 0.0029]

            chart = AgeGraph(data_values=data)
        elif tab_name == 'Gender':
            return
        elif tab_name == 'PofS':
            return
        elif tab_name == 'IPR':
            return
        elif tab_name == 'FNR':
            return
        elif tab_name == 'FPR':
            return
        elif tab_name == 'CovS':
            return
        elif tab_name == 'TPos':
            return
        elif tab_name == 'IFR':
            return
        else:
            QMessageBox.warning(self,
                                'Not available...',
                                'This function is not available yet.')
            return
        self.setChart(chart)

        pass


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


class BaseGraph(QChart):
    def __init__(self) -> None:
        super().__init__()

        # the default color palette is not enough, so I defined my own with 20 colors
        self.colors = ['#C977D9', '#A18AE6', '#8AA2E6', '#8BD1E7', '#8AF3CF', 
                        '#85F38E', '#BDF385', '#EDE485', '#F0B086', '#DE9F8B', 
                        '#74A3B3', '#99CC70', '#DCD68E', '#EDDFAD', '#F7E8CA', 
                        '#FFF9F3', '#FFF9F6', '#FFFBF9', '#FFFCFA', '#FFFEFD']
    
        self.label_lst = [] 

    def MouseOnBar(self, status, index, barset):
        if status:
            txt = '{} / {:.1f}%'.format(self.label_lst[index],barset[index])
            #self.statusbar.showMessage(txt)
            self.setToolTip(txt)


class AllGraph(BaseGraph):
    def __init__(self, data_values) -> None:
        super().__init__()

        # TODO: fill the list of labels
        self.label_lst = [''] * 100

        series = QPercentBarSeries()
        series.hovered.connect(self.MouseOnBar)
        
        for k,s in enumerate(data_values):
            #print(k, len(s))
            setI = QBarSet('{}'.format(k))
            setI.setColor(QColor(self.colors[k]))

            values = (s[0] * 100).tolist()[0]
            setI.append(values)
            series.append(setI)  

        # QChart properties
        #self.chart = QChart()
        #chart.setTheme(QChart.ChartThemeQt)
        self.addSeries(series)
        #chart.addSeries(series2)
        self.setTitle("DSS - Diamond Princess cruise ship")

        font = QFont()
        font.setPixelSize(14)
        font.setBold(True)

        self.setTitleFont(font)
        self.setAnimationOptions(QChart.SeriesAnimations)

        categories = ['Age', 'Gender', 'PofS', 'IPR', 'FNR', 'FPR', 'CovS', 'TPos', 'IFR']
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        axisX.setLabelsAngle(-45)
        axisX.setTitleText('Variables')
        
        #chart.createDefaultAxes()
        self.addAxis(axisX, Qt.AlignBottom)
        

        axisY = QValueAxis()
        axisY.setRange(0,100)
        axisY.setTickCount(11)
        axisY.setLabelFormat('%d')
        axisY.setTickType(QValueAxis.TicksFixed)
        axisY.setTitleText('Percentage')

        self.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        # TODO: Y-axis set tick interval 10
        # TODO: Y-axis horizontal lines

        self.legend().setVisible(False)
        self.legend().setAlignment(Qt.AlignBottom)


class AgeGraph(BaseGraph):
    def __init__(self, data_values) -> None:
        super().__init__()

        # used in the tooltips and X-labels
        self.label_lst = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', 
                          '60-69', '70-79', '80-89', '90-99']
        
        series = QBarSeries()
        series.hovered.connect(self.MouseOnBar)

        setI = QBarSet('age')
        setI.setColor(QColor(self.colors[3]))
        for k,s in enumerate(data_values):
            #values = s/3711 * 100
            v = s * 100
            #print(k, values)
            setI.append(v)
        series.append(setI)        

        self.addSeries(series)
        self.setTitle('Age')

        font = QFont()
        font.setPixelSize(16)
        font.setBold(True)

        self.setTitleFont(font)
        self.setAnimationOptions(QChart.SeriesAnimations)
        
        axisX = QBarCategoryAxis()
        axisX.append(self.label_lst)
        axisX.setLabelsAngle(-45)
        axisX.setTitleText('Variables')
        
        self.addAxis(axisX, Qt.AlignBottom)
        
        axisY = QValueAxis()
        axisY.setRange(0,30)
        axisY.setTickCount(11)
        axisY.setLabelFormat('%d')
        axisY.setTickType(QValueAxis.TicksFixed)
        axisY.setTitleText('Percentage')

        self.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        # TODO: Y-axis set tick interval 10
        # TODO: Y-axis horizontal lines

        self.legend().setVisible(False)
        self.legend().setAlignment(Qt.AlignBottom)
        