import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QToolTip
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtChart import QChart, QChartView, QBarSet, QValueAxis, QPercentBarSeries, QBarCategoryAxis, QBarSeries, QHorizontalPercentBarSeries
from PyQt5.QtGui import QPainter, QFont, QColor
from PyQt5.QtCore import Qt

from bayesiannet import BayesianNet
from utils import AllGraph, Data, AgeGraph, CustomTab, BNTab


class MainWindow(QMainWindow):
    # HTML space
    spc = '&nbsp;&nbsp;'

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        uic.loadUi("mainwindow.ui", self)

        self.set_inital_data()
        # to show sentences predefined according to the protocol
        self.protocol = -1

        self.reset()
        self.bnet = BayesianNet()

        # TODO: Show a tab with the BN
        #bntab = BNTab(self, bn=self.bnet.getBN())
        #self.tabWidget.addTab(bntab, 'BayesNet')
        #bntab.update()


        # initial plotting
        tabs_lst = ['All', 'Age', 'Gender', 'PofS', 'IPR', 'FNR', 'FPR', 
                    'CovS', 'TPos', 'IFR']
        for t in tabs_lst:
            self.tabWidget.addTab(CustomTab(self, t), t)

        #self.plotAll(self.plotAreaLeft)
        #self.plotAge(self.plotAreaRight)

        # connecting signals to slots
        self.btnAnalyze.clicked.connect(self.analyze)
        self.btnReset.clicked.connect(self.reset)

        # Evidences
        self.sldrAge.valueChanged.connect(self.AgeSliderChanged)
        self.bgrpCovS.buttonToggled.connect(self.rdbCovS)
        self.bgrpTPos.buttonToggled.connect(self.rdbTPos)
        self.sldrIFR.valueChanged.connect(self.IFRSliderChanged)
        self.sldrIPR.valueChanged.connect(self.IPRSliderChanged)
        
        # Variables to be OBSERVED
        self.ckbPofS.stateChanged.connect(self.set_observe)
        self.ckbAge.stateChanged.connect(self.set_observe)
        self.ckbIPR.stateChanged.connect(self.set_observe)
        self.ckbGender.stateChanged.connect(self.set_observe)
        self.ckbCovS.stateChanged.connect(self.set_observe)
        self.ckbFPR.stateChanged.connect(self.set_observe)
        self.ckbFNR.stateChanged.connect(self.set_observe)
        self.ckbTPos.stateChanged.connect(self.set_observe)
        self.ckbIFR.stateChanged.connect(self.set_observe)

        self.actionProtocol_1.triggered.connect(self.preDefProtocol1)
        self.actionProtocol_2.triggered.connect(self.preDefProtocol2)
        self.actionProtocol_3.triggered.connect(self.preDefProtocol3)

        self.actionExit.triggered.connect(self.Exit)
        self.actionAbout.triggered.connect(self.About)
        self.actionAbout_Qt.triggered.connect(self.AboutQt)
        

    def reset(self) -> None:
        '''
        Reset interface and variables

        Returns
        -------
        None.

        ''' 
        self.sldrAge.setSliderPosition(-1)
        self.sldrIFR.setSliderPosition(-1)
        self.sldrIPR.setSliderPosition(-1)
        
        self.rdbCovSNone.setChecked(True)
        self.rdbTPosNone.setChecked(True)
                
        self.ckbPofS.setChecked(False)
        self.ckbAge.setChecked(False)
        self.ckbIPR.setChecked(False)
        self.ckbGender.setChecked(False)
        self.ckbCovS.setChecked(False)
        self.ckbFPR.setChecked(False)
        self.ckbFNR.setChecked(False)
        self.ckbTPos.setChecked(False)
        self.ckbIFR.setChecked(False)

        self.txtEdtReport.clear()
        
        # Reseting variables
        self.var_observe = []
        self.var_evidences = {}
        self.protocol = -1

    def update_plots(self):
        # loop trhough all variables

        # get the values and put as list

        # send to respective plot function

        pass

        
    def rdbCovS(self, btn, checked):
        if checked:
            btn_lbl = btn.objectName()
            
            if btn_lbl == 'rdbCovSNone':
                idx = -1
            elif btn_lbl == 'rdbCovSInfSymp':
                idx = 0
            elif btn_lbl == 'rdbCovSInfAsymp':
                idx = 1
            elif btn_lbl == 'rdbCovSNotInf':
                idx = 2
            else:
                print('ERROR (rdbCovS): State not found')
                return

            # unset situation
            lblText = f'Covid-19 Status (CovS): {self.covs_states[idx]}'
            # diff from unset
            if idx != -1:
                lblText = f'<b>Covid-19 Status (CovS): <font color="red">{self.covs_states[idx]}</font></b>'

            self.lblCovS.setText(lblText)
            self.set_evidence('COVID-19 Status', idx)


    def rdbTPos(self, btn, checked):
        if checked:
            btn_lbl = btn.objectName()
            
            if btn_lbl == 'rdbTPosNone':
                idx = -1
            elif btn_lbl == 'rdbTPosNo':
                idx = 0
            elif btn_lbl == 'rdbTPosYes':
                idx = 1
            else:
                print('ERROR (rdbTPos): State not found')
                return

            lblText = f'Tested Positive (TPos): {self.tpos_states[idx]}'
            if idx != -1:
                lblText = f'<b>Tested Positive (TPos):<font color="red"> {self.tpos_states[idx]}</font></b>'
    
            self.lblTPos.setText(lblText)
            self.set_evidence('Tested Positive', idx)


    def do_report(self, txt, txt_spec, warning_lvl='') -> None:
        #warning_lvl = 'Low'

        txt_template_header = '<b>Date</b>: February, 2020.<br><br>' +\
            '<b>Subject</b>: Diamond Princess cruise ship.<br>'

        txt_template_01 = \
            '<b>Warning level</b>: <i><font color="red"><b>' +\
            warning_lvl +\
            '</b></font></i>.<br><b>Specification</b>: '

        txt2 = txt_template_header + txt_template_01 + txt_spec
        #print(txt)

        txt_final = txt2 + '<hr><b>Reasoning</b>:' + txt
        self.txtEdtReport.clear()
        self.txtEdtReport.setHtml(txt_final)


    def analyze(self):
        res = self.bnet.doInference(self.bnet.bn, 
                                    var_obs=self.var_observe, 
                                    evs=self.var_evidences)
        print('Evs:', self.var_evidences)
        print('Anayze:', res)

        warning_lvl = ''
        report_str = '<ul>'
        txt_spec = ''
        txt_ev = ''
        
        if (len(self.var_evidences) != 0):
            for evk in self.var_evidences:
                print('ev:', evk)
                txt_parsed = self.parse_state(evk, self.var_evidences[evk])
                txt_ev += '{} = {}, '.format(evk, txt_parsed)
            # removing last ', '
            txt_ev = txt_ev[:-2]
        # dict empty
        else:
            txt_ev = 'No evidence'
        
        for k in res:
            print('k:', k, res[k])
            for i,v in enumerate(res[k]):
                i_txt = self.parse_state(k, i)
                # FIX: if '>=' or '<=' remove the '=' symbol
                report_str += '<li>P(<b>{} = {}</b> | <b>{}</b>) = {:.2f}.</li>'.format(k, i_txt, txt_ev, v)

            # Protocol #1:
            #       - P(TPos = NO | CovS = SYM
            # Observe: ['Tested Positive']
            # Evs: {'COVID-19 Status': 1}
            if self.protocol == 1:
                if ('COVID-19 Status' in self.var_evidences):
                    ev_CovS = self.var_evidences['COVID-19 Status']
                    if (ev_CovS == 0):
                        # from the TPos node get the P(TPos = NO)
                        obs_TPos = res['Tested Positive'][0]
                        print('obs_TPos:', obs_TPos)
                        if (obs_TPos < 0.25):
                            warning_lvl = 'Low'
                        elif (0.25 <= obs_TPos < 0.50):
                            warning_lvl = 'Moderate'
                        elif (0.50 <= obs_TPos < 0.75):
                            warning_lvl = 'High'
                        elif (obs_TPos >= 0.75):
                            warning_lvl = 'Very High'
                        txt_spec = 'The risk of the test coming back as negative ' +\
                                'when a subject is infected is ' +\
                                '<i><font color="red"><b>{}</b></font></i>.'.format(warning_lvl)
            elif self.protocol == 2:
                warning_lvl = 'Moderate'
                txt_spec = 'The risk of a subject been infected with or without ' +\
                    'symptoms is <i><font color="red"><b>Low</b></font></i> ' +\
                    'considering a negative test and a ' +\
                    '<i><font color="red"><b>Low</b></font></i> ' +\
                    'fatality rate.'
            elif self.protocol == 3:
                warning_lvl = 'High'
                txt_spec = 'When IPR is higher than 25%, the risk that ' +\
                    'the fatality rate stays at 4 people per 1,000 is 23.76%, ' +\
                    'and the risk of a subject contract COVID-19 with symptoms ' +\
                    'is 33.33%.'
        report_str += '</ul>'
        
        self.do_report(report_str, txt_spec, warning_lvl=warning_lvl)


    def parse_state(self, node:str, state:int):
        if (node == 'PofS'):
            txt_state = self.pofs_states[state]
        elif (node == 'Age'):
            txt_state = self.age_states[state][0]
        elif (node == 'IPR'):
            txt_state = self.ipr_states[state][0]
        elif (node == 'Gender'):
            txt_state = self.gender_states[state] 
        elif (node == 'COVID-19 Status'):
            txt_state = self.covs_states[state]
        elif (node == 'FPR'):
            txt_state = self.fpr_states[state]
        elif (node == 'FNR'):
            txt_state = self.fnr_states[state]
        elif (node == 'Tested Positive'):
            txt_state = self.tpos_states[state]
        elif (node == 'IFR'):
            txt_state = self.ifr_states[state][0]
        else:
            txt_state = 'Not found!'
            
        return txt_state

    def plotAge(self, widget_area, evs={}):

        inf_res = self.bnet.doInference(self.bnet.bn, 
                                        var_obs=['Age'],
                                        evs=evs)
        age_graph = AgeGraph(inf_res['Age'])

        widget_area.setChart(age_graph) 


    def preDefProtocol1(self):
        """ Protocol #1 according to IEEE SSCI/CBIM 2021 paper
        """        
        self.reset()
        self.rdbCovSInfSymp.setChecked(True)
        self.ckbTPos.setChecked(True)
        self.protocol = 1


    def preDefProtocol2(self):
        """ Protocol #2 according to IEEE SSCI/CBIM 2021 paper
        """  
        self.reset()
        self.rdbTPosNo.setChecked(True)
        self.sldrIFR.setSliderPosition(1)
        self.ckbCovS.setChecked(True)
        self.protocol = 2
        

    def preDefProtocol3(self):
        """ Protocol #3 according to IEEE SSCI/CBIM 2021 paper
        """  
        self.reset()
        self.sldrIPR.setSliderPosition(12)
        self.ckbCovS.setChecked(True)
        self.ckbIFR.setChecked(True)
        self.protocol = 3


    def set_inital_data(self):
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

        self.covs_states = {-1: 'unset',
                        0: 'Infected w/ Symp.',
                        1: 'Infected w/o Symp.',
                        2: 'Not Infected'}

        self.fnr_states = ['1%', '2%', '3%', '4%', '5%', '6%', '7%', '8%', 
                    '9%', '10%', '11%', '12%', '13%', '14%', '15%']
        
        self.fpr_states = ['0.25%', '0.50%', '0.75%', '1.00%', '1.25%', '1.50%',
                    '1.75%', '2.00%', '2.25%', '2.50%', '2.75%', '3.00%']

        self.tpos_states = {-1: 'unset',
                        0: 'No',
                        1: 'Yes'}
        
        self.gender_states = ['Male', 'Female']

        self.pofs_states = ['Not susc.', 'Susc.']


    def set_observe(self, state):
        widget_name = self.sender().objectName()
        var_name = widget_name.split('ckb')[1]

        # 'TPos' in the BN is called 'Tested Positive'
        if var_name == 'TPos':
            var_name = 'Tested Positive'
        elif var_name == 'CovS':
            var_name = 'COVID-19 Status'

        # add/remove itens from the list as necessary
        if var_name in self.var_observe and state == 0:
            self.var_observe.remove(var_name)
        elif var_name not in self.var_observe and state == 2:
            self.var_observe.append(var_name)

        print('Observe:', self.var_observe)
        # remove from dict:
        # self.var_evidences.pop('Age')


    def set_evidence(self, node:str, state:int):
            
        # unset situation
        if node in self.var_evidences:
            del self.var_evidences[node]
        # diff from unset
        if state != -1:
            self.var_evidences[node] = state

        print('Evs:', self.var_evidences)
    

    def AgeSliderChanged(self, idx):
        lblText = f'Age: {self.age_states[idx][0]}'
        if idx != -1:
            lblText = '<b>Age: <font color="red">{} ({:.1f}%, {} people)</font></b>'.format(
                                                                self.age_states[idx][0], 
                                                                self.age_states[idx][1]/3711*100,
                                                                self.age_states[idx][1])
        self.lblAge.setText(lblText)
        self.set_evidence('Age', idx)


    def IFRSliderChanged(self, idx):
        lblText = f'Infection Fatality Rate (IFR): {self.ifr_states[idx][0]}'
        if idx != -1:
            qtt_fatality = int(self.ifr_states[idx][1] * self.total_population)
            lblText = '<b>Infection Fatality Rate (IFR):<font color="red"> ' +\
                      '{}, {:d} people</font></b>'.format(
                                                        self.ifr_states[idx][0],
                                                        qtt_fatality)
        self.lblIFR.setText(lblText)
        self.set_evidence('IFR', idx)
        

    def IPRSliderChanged(self, idx):
        lblText = f'Infection Prevalence Rate (IPR): {self.ipr_states[idx][0]}'
        if idx != -1:
            qtt_infected = int(self.ipr_states[idx][1] * self.total_population)
            
            lblText = '<b>Infection Prevalence Rate (IPR):<font color="red">' +\
                      ' {}, {:d} people</font></b>'.format(
                                                        self.ipr_states[idx][0], 
                                                        qtt_infected)

        self.lblIPR.setText(lblText)
        self.set_evidence('IPR', idx)


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
       self.close()


def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
