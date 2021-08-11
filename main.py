import sys

import numpy as np
from scipy.stats import norm

import qtmodern.windows
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QToolTip
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtChart import QChart, QChartView, QBarSet, QValueAxis, QPercentBarSeries, QBarCategoryAxis, QBarSeries, QHorizontalPercentBarSeries
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtCore import Qt

from bayesiannet import BayesianNet


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        uic.loadUi("mainwindow.ui", self)

        # Generate checkboxes based on length of data in model
        # for datapoint in range(self._model.datapoints):
        #     self.tempCheck = QtWidgets.QCheckBox(self.scenarioGroupBox)
        #     self.tempCheck.setFont(QtGui.QFont('SansSerif', 13))
        #     self.tempCheck.setObjectName(str(datapoint))
        #     self.tempCheck.toggled.connect(self.updateGraph)
        #     self.verticalLayout.addWidget(self.tempCheck, alignment=QtCore.Qt.AlignTop)
        #     self.tempCheck.setText(
        #         QtCore.QCoreApplication.translate(
        #             "MainWindow", f"Scenario {datapoint+1}"
        #         )
        #     )

        self.bnet = BayesianNet()

        self.var_observe = []
        self.var_evidences = {}

        # TODO: Automate creation/population of sets
        sets = []

        # Testing barchart
        set0 = QBarSet("PofS")
        set1 = QBarSet("Bob")
        set2 = QBarSet("Tom")
        set3 = QBarSet("Logan")
        set4 = QBarSet("Karim")


        set0 << 8 << 55 << 0 << 0 << 0 << 100 << 0 << 0 << 0#= self.bnet.doInference(self.bnet.bn, 'PofS').toarray() * 100
        set1 << 2 << 45 << 0 << 4 << 0 << 0 << 100 << 0 << 0
        set2 << 0 << 0 << 8 << 13 << 8 << 0 << 0 << 100 << 0
        set3 << 0 << 0 << 7 << 3 << 4 << 0 << 0 << 0 << 100
        set4 << 0 << 0 << 5 << 3 << 1 << 0 << 0 << 0 << 0
        # set4 << 0 << 7 << 5 << 3 << 1 << 0 << 0 << 0 << 0
        # set4 << 0 << 7 << 5 << 3 << 1 << 0 << 0 << 0 << 0
        # set4 << 0 << 7 << 5 << 3 << 1 << 0 << 0 << 0 << 0
        # set4 << 0 << 7 << 5 << 3 << 1 << 0 << 0 << 0 << 0
        # set4 << 0 << 7 << 5 << 3 << 1 << 0 << 0 << 0 << 0
        # set4 << 0 << 7 << 5 << 3 << 1 << 0 << 0 << 0 << 0
        # set4 << 0 << 7 << 5 << 3 << 1 << 0 << 0 << 0 << 0
        # set4 << 0 << 7 << 5 << 3 << 1 << 0 << 0 << 0 << 0
        # set4 << 0 << 7 << 5 << 3 << 1 << 0 << 0 << 0 << 0
        # set4 << 0 << 7 << 5 << 3 << 1 << 0 << 0 << 0 << 0
        # set4 << 0 << 7 << 5 << 3 << 1 << 0 << 0 << 0 << 0

        series = QPercentBarSeries()
        series.append(set0)
        series.append(set1)
        series.append(set2)
        series.append(set3)
        series.append(set4)

        #series2 = QPercentBarSeries()
        

        chart = QChart()
        #chart.setTheme(QChart.ChartThemeQt)
        chart.addSeries(series)
        #chart.addSeries(series2)
        chart.setTitle("DSS - Diamond Princess cruise ship")

        font = QFont()
        font.setPixelSize(14)
        font.setBold(True)

        chart.setTitleFont(font)
        chart.setAnimationOptions(QChart.SeriesAnimations)

        categories = ['Age', 'Gender', 'PofS', 'IPR', 'FNR', 'FPR', 'CovS', 'TPos', 'IFR']
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        axisX.setLabelsAngle(-45)
        axisX.setTitleText('Variables')
        #chart.createDefaultAxes()
        chart.addAxis(axisX, Qt.AlignBottom)
        

        axisY = QValueAxis()
        axisY.setRange(0,100)
        axisY.setTickCount(11)
        axisY.setLabelFormat('%d')
        axisY.setTickType(QValueAxis.TicksFixed)
        axisY.setTitleText('Percentage')

        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        # TODO: Y-axis set tick interval 10
        # TODO: Y-axis horizontal lines

        chart.legend().setVisible(False)
        chart.legend().setAlignment(Qt.AlignBottom)

        
        #chartView = QChartView(chart)
        #chartView.setRenderHint(QPainter.Antialiasing)

        self.widget.setChart(chart) 


        # TODO: age plot
        total_age = [16, 23, 347, 428, 334, 398, 923, 1015, 216, 11]
        total_age = np.divide(total_age, np.sum(total_age)) * 100
        print(total_age)

        self.series = QHorizontalPercentBarSeries()
        self.series.setLabelsVisible(False)

        for a in total_age:
            setAge = QBarSet('')
            setAge.append(a)
            self.series.append(setAge)

        chart = QChart()
        #chart.setTheme(QChart.ChartThemeQt)
        chart.addSeries(self.series)
        self.series.setLabelsVisible(False)
        #chart.addSeries(series2)
        #chart.setTitle("DSS - Diamond Princess cruise ship")

        #font = QFont()
       # font.setPixelSize(14)
        #font.setBold(True)
        #chart.setTitleFont(font)
        #chart.setAnimationOptions(QChart.SeriesAnimations)

        # categories = ['Age', 'Gender', 'PofS', 'IPR', 'FNR', 'FPR', 'CovS', 'TPos', 'IFR']
        # axisX = QBarCategoryAxis()
        # axisX.append(categories)
        # axisX.setTitleText('Variables')
        # axisX.setVisible(False)
        # chart.createDefaultAxes()
        # chart.addAxis(axisX, Qt.AlignBottom)

        # TODO: Y-axis set tick interval 10
        # TODO: Y-axis horizontal lines

        chart.legend().setVisible(False)
        #chart.legend().setAlignment(Qt.AlignBottom)

        
        #chartView = QChartView(chart)
        #chartView.setRenderHint(QPainter.Antialiasing)
        self.plotAge.setChart(chart) 







        # connecting signals to slots
        self.btnAnalyze.clicked.connect(self.Analyze)
        #self.btnReset.clicked.connect(self.Reset)

        self.series.hovered.connect(self.MouseOnBar)

        self.ckbAge.stateChanged.connect(self.SetObserve)
        self.ckbGender.stateChanged.connect(self.SetObserve)
        self.ckbCovS.stateChanged.connect(self.SetObserve)

        self.sldrAge.valueChanged.connect(self.AgeSliderChanged)
        self.sldrCovS.valueChanged.connect(self.CovSSliderChanged)
        self.sldrTPos.valueChanged.connect(self.TPosSliderChanged)
        self.sldrIFR.valueChanged.connect(self.IFRSliderChanged)
        self.sldrIPR.valueChanged.connect(self.IPRSliderChanged)

        self.actionExit.triggered.connect(self.Exit)
        self.actionAbout.triggered.connect(self.About)
        self.actionAbout_Qt.triggered.connect(self.AboutQt)

    def ResetSetup(self):
        # reset interface and variables
        print('--> Reset')

    def DoReport(self, txt):
        txt = '<b>Date</b>: February, 2020.<br><br>' +\
              '<b>Subject</b>: Diamond Princess cruise ship.<br>' +\
              '<b>Warning level</b>: <i><font color="red">Low</font></i>.<br>' +\
              '<b>Specification</b>: The risk of false-positive ' +\
              'outcomes in testing is moderately <i><font color="red">low</font></i>.<br>'
        print(txt)
        self.txtEdtReport.clear()
        self.txtEdtReport.setHtml(txt)


    def Analyze(self):
        res = self.bnet.doInference(self.bnet.bn, 
                                    var_obs=self.var_observe, 
                                    evs=self.var_evidences)
        print(res)

        report_str = ''
        for k in res:
            print(k, res[k])
            report_str += '<b><font color="red">' + k +\
                          '</font></b>:<br>' + str(res[k]) + '<br><br>' 
        self.DoReport(report_str)


    def MouseOnBar(self, status, index, barset):
        if status:
            #print(barset[index])
            self.statusbar.showMessage('Value: {:.2f}'.format(barset[index]))


    def SetObserve(self, state):
        widget_name = self.sender().objectName()
        var_name = widget_name.split('ckb')[1]

        # if var_name == 'CovS':
        #     var_name = ''

        # FIX: avoid duplicates

        # add/remove itens from the list as necessary
        if var_name in self.var_observe and state == 0:
            self.var_observe.remove(var_name)
        elif var_name not in self.var_observe and state == 2:
            self.var_observe.append(var_name)

        print('Observe:', self.var_observe)
        # remove from dict:
        # self.var_evidences.pop('Age')

    

    def AgeSliderChanged(self, v):
        # total_age = [16, 23, 347, 428, 334, 398, 923, 1015, 216, 11]
        age_states = {-1: ['unset'],
                      0: ['0-9', 16],
                      1: ['10-19', 23],
                      2: ['20-29', 347],
                      3: ['30-39', 428],
                      4: ['40-49', 334],
                      5: ['50-59', 398],
                      6: ['60-69', 923],
                      7: ['70-79', 1015],
                      8: ['80-89', 216],
                      9: ['90-99', 11]}

        lblText = f'Age: {age_states[v][0]}'
        if v != -1:
            lblText = '<b>Age: <font color="red">{} ({} people - {:.1f}%)</font></b>'.format(
                                                                age_states[v][0], 
                                                                age_states[v][1],
                                                                age_states[v][1]/3711*100)

        self.lblAge.setText(lblText)


    def CovSSliderChanged(self, v):
        covs_states = {-1: 'unset',
                      0: 'Infected w/ Symp.',
                      1: 'Infected w/o Symp.',
                      2: 'Not Infected'}

        # unset situation
        lblText = f'Covid-19 Status (CovS): {covs_states[v]}'
        if 'COVID-19 Status' in self.var_evidences:
            del self.var_evidences['COVID-19 Status']
        # diff from unset
        if v != -1:
            lblText = f'<b>Covid-19 Status (CovS): <font color="red">{covs_states[v]}</font></b>'
            self.var_evidences['COVID-19 Status'] = v

        print('CovS', v)
        self.lblCovS.setText(lblText)


    def TPosSliderChanged(self, v):
        tpos_states = {-1: 'unset',
                      0: 'No',
                      1: 'Yes'}

        lblText = f'Tested Positive (TPos): {tpos_states[v]}'
        if v != -1:
            lblText = f'<b>Tested Positive (TPos):<font color="red"> {tpos_states[v]}</font></b>'

        self.lblTPos.setText(lblText)


    def IFRSliderChanged(self, v):
        ifr_states = {-1: 'unset',
                       0: '0.0%',
                       1: '0.1%', 
                       2: '0.2%', 
                       3: '0.3%', 
                       4: '0.4%', 
                       5: '0.5%', 
                       6: '0.6%', 
                       7: '0.7%', 
                       8: '0.8%', 
                       9: '0.9%', 
                       10: '1.0%', 
                       }

        lblText = f'Infection Fatality Rate (IFR): {ifr_states[v]}'
        if v != -1:
            lblText = f'<b>Infection Fatality Rate (IFR):<font color="red"> {ifr_states[v]}</font></b>'

        self.lblIFR.setText(lblText)
        

    def IPRSliderChanged(self, v):
        #'<=13%|14%|15%|16%|17%|18%|19%|20%|21%|22%|23%|24%|>=25%'

        ipr_states = {-1: 'unset',
                       0: ']13%',
                       1: '14%', 
                       2: '15%', 
                       3: '16%', 
                       4: '17%', 
                       5: '18%', 
                       6: '19%', 
                       7: '20%', 
                       8: '21%', 
                       9: '22%', 
                       10: '23%',
                       11: '24%',
                       12: '>=25%'}

        lblText = f'Infection Prevalence Rate (IPR): {ipr_states[v]}'
        if v != -1:
            lblText = f'<b>Infection Prevalence Rate (IPR):<font color="red"> {ipr_states[v]}</font></b>'

        self.lblIPR.setText(lblText)


    def About(self):
        QMessageBox.about(self,
                    'About...',
                    'by Helder')

    def AboutQt(self):
        QMessageBox.aboutQt(self)

    def Exit(self):
        # QtWidgets.qApp.quit
        self.close()

    # TODO: Maybe this will be necessary when plotting new graphs
    def updateGraph(self):
        """Updates graph respective to status of toggled checkbox.

        Retrieves sender (toggled checkbox) reference and if it is checked, retrieves data from model 
        and passes it to drawLine(). If not checked, references line respective to checkbox and removes
        it.
        """
        checkbox = self.sender()
        checkboxNumber = int(checkbox.objectName())
        if checkbox.isChecked():
            peak = self._model.get_peak(checkboxNumber)
            duration = self._model.get_duration(checkboxNumber)
            self.drawLine(peak=peak, checkboxNumber=checkboxNumber, duration=duration)
        else:
            for line in self.graphWidget.canvas.ax.lines:
                if line.get_label() == f"Scenario {checkboxNumber+1}":
                    self.graphWidget.canvas.ax.lines.remove(line)
            # TODO: Resize after removal of line
        self.graphWidget.canvas.ax.legend()
        # NOTE: Legend is not ordered, not too sure if worth addressing or not.
        self.graphWidget.canvas.draw()

    def drawLine(self, peak, checkboxNumber, duration=100.0):
        """Generates gaussian wave based off given peak and duration data in order to model disease spread. 

        Processes gaussian wave off peak and duration data, passes x and y arrays to MplWidget.plot(). 
        Assigns labels to lines for referenced removal.

        Parameters
        ----------
        peak : float
            Desired peak (%) of wave
        duration : float, optional
            Desired duration of wave (days), by default 100.0
        """
        X = np.linspace(0, duration, 100)
        y = norm.pdf(X, duration / 2, duration / 6)
        y = peak / max(y) * y  # Stretches curve to reach peak point
        self.graphWidget.plot(X, y, label=f"Scenario {checkboxNumber+1}")


def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main = qtmodern.windows.ModernWindow(main)
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
