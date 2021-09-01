import sys

import numpy as np
from scipy.stats import norm

import qtmodern.windows
import qtmodern.styles

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QToolTip
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtChart import QChart, QChartView, QBarSet, QValueAxis, QPercentBarSeries, QBarCategoryAxis, QBarSeries, QHorizontalPercentBarSeries
from PyQt5.QtGui import QPainter, QFont, QColor
from PyQt5.QtCore import Qt

from bayesiannet import BayesianNet
from utils import AllGraph, Data, AgeGraph

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

        # Data considered
        self.total_population = 3711
        # total_age = [16, 23, 347, 428, 334, 398, 923, 1015, 216, 11]
        self.age_states = {-1: ['unset'],
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

        #'<=13%|14%|15%|16%|17%|18%|19%|20%|21%|22%|23%|24%|>=25%'
        self.ipr_states = {-1: ['unset'],
                            0: ['\u2264 13%', 0.13],
                            1: ['14%', 0.14], 
                            2: ['15%', 0.15], 
                            3: ['16%', 0.16],
                            4: ['17%', 0.17], 
                            5: ['18%', 0.18], 
                            6: ['19%', 0.19], 
                            7: ['20%', 0.20], 
                            8: ['21%', 0.21], 
                            9: ['22%', 0.22], 
                            10: ['23%', 0.23],
                            11: ['24%', 0.24],
                            12: ['\u2265 25%', 0.25]}

        self.ifr_states = {-1: ['unset'],
                           0: ['0.0%', 0],
                           1: ['0.1%', 0.001], 
                           2: ['0.2%', 0.002], 
                           3: ['0.3%', 0.003], 
                           4: ['0.4%', 0.004], 
                           5: ['0.5%', 0.005], 
                           6: ['0.6%', 0.006], 
                           7: ['0.7%', 0.007], 
                           8: ['0.8%', 0.008], 
                           9: ['0.9%', 0.009], 
                           10: ['1.0%', 0.01]}



        self.bnet = BayesianNet()

        self.var_observe = []
        self.var_evidences = {}

        # initial plotting
        self.plotAll(self.plotAreaLeft)
        self.plotAge(self.plotAreaRight)

        # connecting signals to slots
        self.btnAnalyze.clicked.connect(self.Analyze)
        #self.btnReset.clicked.connect(self.Reset)

        # TODO: to be used for tooltips
        #self.series.hovered.connect(self.MouseOnBar)

        self.ckbAge.stateChanged.connect(self.SetObserve)
        self.ckbGender.stateChanged.connect(self.SetObserve)
        self.ckbCovS.stateChanged.connect(self.SetObserve)

        self.sldrAge.valueChanged.connect(self.AgeSliderChanged)
        self.sldrCovS.valueChanged.connect(self.CovSSliderChanged)
        self.sldrTPos.valueChanged.connect(self.TPosSliderChanged)
        self.sldrIFR.valueChanged.connect(self.IFRSliderChanged)
        self.sldrIPR.valueChanged.connect(self.IPRSliderChanged)

        self.actionProtocol_1.triggered.connect(self.preDefProtocol1)
        self.actionProtocol_2.triggered.connect(self.preDefProtocol2)
        self.actionProtocol_3.triggered.connect(self.preDefProtocol3)

        self.actionExit.triggered.connect(self.Exit)
        self.actionAbout.triggered.connect(self.About)
        self.actionAbout_Qt.triggered.connect(self.AboutQt)

    def ResetSetup(self):
        # reset interface and variables
        print('--> Reset')

    def DoReport(self, txt):
        txt2 = '<b>Date</b>: February, 2020.<br><br>' +\
              '<b><u>Subject</u></b>: Diamond Princess cruise ship.<br>' +\
              '<b><u>Warning level</u></b>: <i><font color="red">Low</font></i>.<br>' +\
              '<b><u>Specification</u></b>: The risk of false-positive ' +\
              'outcomes in testing is moderately <i><font color="red">low</font></i>.'
        #print(txt)
        txt_reasoning = '<u>Reasoning</u>:<br>' +\
                        'P(TPos = yes IF<br>&nbsp;&nbsp;' +\
                        'CovS = Not Infected) = <i><font color="red">14.46%</b></font></i>.'
        txt_final = txt2 + '<hr>' + txt_reasoning + txt
        self.txtEdtReport.clear()
        self.txtEdtReport.setHtml(txt_final)


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

    def plotAll(self, widget_area):
        # don't need to do inference        
        vars_values = Data().getAll()
        chart_left = AllGraph(vars_values).getGraph()

        widget_area.setChart(chart_left) 


    def plotAge(self, widget_area, evs={}):

        inf_res = self.bnet.doInference(self.bnet.bn, 
                                        var_obs=['Age'],
                                        evs=evs)
        age_graph = AgeGraph(inf_res['Age']).getGraph()

        widget_area.setChart(age_graph) 




    
    def preDefProtocol1(self):

        inf_res = self.bnet.doInference(self.bnet.bn,
                                        var_obs=['Tested Positive'],
                                        evs={'COVID-19 Status': 1})

        print('Protocolol 1.1: Tested Positive', inf_res['Tested Positive'])
        
        colorsRedGreen = ['#E5B4CD', '#ABE594']
        series = QBarSeries()
        var_values = inf_res['Tested Positive']

        for k,s in enumerate(var_values):
            #print(k, len(s))
            setI = QBarSet('{}'.format(k))
            setI.setColor(QColor(colorsRedGreen[k]))
            #print(s[0], s[1] * 100)
            #print(s[0,4] * 100)
            #test.append(s[0,4] * 100)

            print(k, s)

            values = s * 100
            setI.append(values)
            series.append(setI)        

        chart = QChart()
        #chart.setTheme(QChart.ChartThemeQt)
        chart.addSeries(series)
        #chart.addSeries(series2)
        chart.setTitle("DSS - Diamond Princess cruise ship\nTested Positive")

        font = QFont()
        font.setPixelSize(16)
        font.setBold(True)

        chart.setTitleFont(font)
        chart.setAnimationOptions(QChart.SeriesAnimations)

        categories = ['No', 'Yes']
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        axisX.setLabelsAngle(-45)
        axisX.setTitleText('Variables')
        axisX.setFont(font)
        
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

        self.widget.setChart(chart) 






    def preDefProtocol2(self):
        self.NotAvailable()

    def preDefProtocol3(self):
        self.NotAvailable()


    def setInitalData(self):
        pass

    def MouseOnBar(self, status, index, barset):
        if status:
            #print(index, barset.label(), barset[index])
            txt = '{} / {:.1f}%'.format(barset.label(),barset[index])
            self.statusbar.showMessage(txt)
            self.plotAge.setToolTip(txt)


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
        lblText = f'Age: {self.age_states[v][0]}'
        if v != -1:
            lblText = '<b>Age: <font color="red">{} ({:.1f}%, {} people)</font></b>'.format(
                                                                self.age_states[v][0], 
                                                                self.age_states[v][1]/3711*100,
                                                                self.age_states[v][1])
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
        lblText = f'Infection Fatality Rate (IFR): {self.ifr_states[v][0]}'
        if v != -1:
            qtt_fatality = int(self.ifr_states[v][1] * self.total_population)
            lblText = '<b>Infection Fatality Rate (IFR):<font color="red"> ' +\
                      '{}, {:d} people</font></b>'.format(
                                                        self.ifr_states[v][0],
                                                        qtt_fatality)
        self.lblIFR.setText(lblText)
        

    def IPRSliderChanged(self, v):
        lblText = f'Infection Prevalence Rate (IPR): {self.ipr_states[v][0]}'
        if v != -1:
            qtt_infected = int(self.ipr_states[v][1] * self.total_population)
            
            lblText = '<b>Infection Prevalence Rate (IPR):<font color="red">' +\
                      ' {}, {:d} people</font></b>'.format(
                                                        self.ipr_states[v][0], 
                                                        qtt_infected)

        self.lblIPR.setText(lblText)


    def NotAvailable(self):
        QMessageBox.warning(self,
                    'Not available...',
                    'This function is not available yet.')

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
    #qtmodern.styles.light(app)
    main = qtmodern.windows.ModernWindow(MainWindow())
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
