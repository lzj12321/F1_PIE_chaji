import pymysql
from yamlTool import Yaml_Tool
from PyQt5.QtCore import *
import datetime

class MysqlTool:
    def __init__(self):
        self.yamlTool=Yaml_Tool()
        self.params=self.yamlTool.getValue('configure.yaml')['mysql']
        self.timeStamp=self.yamlTool.getValue('configure.yaml')['timeStamp']
        self.deviceInfo=self.yamlTool.getValue('configure.yaml')['devices']
        self._connectState=self.connectServer()
        pass

    def connectServer(self):
        try:
            self.db = pymysql.connect(self.params['ip'],
                                  self.params['user'],
                                  self.params['password'],
                                  self.params['database'])
            self.cursor = self.db.cursor()
            return True
        except Exception as ex:
            print(ex)
            return False

    def executeSql(self,sql):
        if not self.connectServer():
            print('failed connect to mysql server')
            return False,-1
        try:
            self.cursor.execute(sql)
            result=self.cursor.fetchall()
           # print('result:'+str(len(result)))
            self.db.commit()
            self.db.close()
            return True,result
        except:
            self.db.rollback()
            self.db.close()
            return False,-1
        pass

    def saveDeviceProductionData(self,_device,_production):
        _productModel=self.yamlTool.getValue('configure.yaml')['devices'][_device]['productModel']
        _productMulti=self.yamlTool.getValue('configure.yaml')['devices'][_device]['productMulti']
        _hourProduction=self.yamlTool.getValue('configure.yaml')['devices'][_device]['hourProduction']
        _production*=_productMulti
        print("save production data:"+_productModel)
        _currDate=""
        _currHour=int(datetime.datetime.now().strftime('%H'))
        if _currHour>=8:
            _currDate=QDateTime.currentDateTime().toString('yyyy-MM-dd')
        else:
            _currDate=QDateTime.currentDateTime().addDays(-1).toString('yyyy-MM-dd')
        _timeStamp=self.timeStamp['hour_'+str(_currHour)]
        _dataTable="chajiProductionData"
        sql1="select "+_timeStamp+" from "+_dataTable+" \
            where product=\'"+_productModel+"\' and device=\'"+_device+"\' and date=\'"+_currDate+"\';"
        flag,result=self.executeSql(sql1)
        if flag and len(result)!=0:
            sql2="update "+_dataTable+" set "+_timeStamp+"="+_timeStamp+"+"+str(_production)+",hourProduction="+str(_hourProduction)+"\
             where product=\'"+_productModel+"\' and device=\'"+_device+"\' and date=\'"+_currDate+"\';"
            #print(sql2)
            flag2,result2=self.executeSql(sql2)
            if not flag2:
                print('execute sql error:'+sql2)
        elif flag and len(result)==0:
            sql2="insert "+_dataTable+"(product,device,date,hourProduction,"+_timeStamp+\
                ") value(\'"+_productModel+"\',\'"+_device+"\',\'"+_currDate+"\',"+str(_hourProduction)+","+str(_production)+");"
            #print(sql2)
            flag2,result2=self.executeSql(sql2)
            if not flag2:
                print('execute sql error:'+sql2)
        else:
            print('execute sql error:'+sql1)
        pass

    def saveDeviceState(self,_workshop,_robotSerial,_robotState,_description):
        prevTime,SN=self.getPrevTimeAndSn(_workshop,_robotSerial)
        currTime=self.getServerTime()
        if not(prevTime=='null' or SN=='null'):
            if currTime=='null':
                return False
            timeInterval=self.getTimeInterval(prevTime,currTime)
            updateDeviceElaspeSql='update robotMonitorLog set elaspe='+str(timeInterval)+' where SN='+str(SN)+';'
            flag,result=self.executeSql(updateDeviceElaspeSql)
            if not flag:
                print('exetute sql error:'+updateDeviceElaspeSql)
                pass
            
        addRecordSql="insert into robotMonitorLog(workshop,robotSerial,robotState,description,elaspe) values(\'"+_workshop+"\',\'"+_robotSerial+"\',\'"+_robotState+"\',\'"+_description+"\',-1);"
        flag,result=self.executeSql(addRecordSql)
        if not flag:
            print('exetute sql error:'+addRecordSql)
            pass
        return True

    def getPrevTimeAndSn(self,_workshop,_robotSerial):
        getTimeAndSnSql = 'select SN,time from robotMonitorLog where robotSerial=\''+_robotSerial+'\' and workshop=\''+_workshop+'\' order by SN desc limit 1;'
        flag,result=self.executeSql(getTimeAndSnSql)
        if flag:
            if len(result)==0:
                return 'null','null'
            prevTime=str(result[0][1])
            sn=result[0][0]
            return prevTime,sn
        else:
            return 'null','null'

    def getServerTime(self):
        sql='select current_timestamp as time;'
        flag,result=self.executeSql(sql)
        if flag:
            return str(result[0][0])
        else:
            print('execute sql error:'+sql)
            return 'null'
        pass

    def getTimeInterval(self,prevTime,currTime):
        time1=QDateTime.fromString(prevTime,'yyyy-MM-dd hh:mm:ss')
        time2=QDateTime.fromString(currTime,'yyyy-MM-dd hh:mm:ss')
        interval=time1.msecsTo(time2)/60000
        return round(interval,2)
        pass



if __name__=='__main__':
    print('test')

    time1=QDateTime.fromString('2020-07-08 02:02:02','yyyy-MM-dd hh:mm:ss')
    time2=QDateTime.fromString('2020-07-08 02:04:02','yyyy-MM-dd hh:mm:ss')
    print(time1.msecsTo(time2)/1000)
    mysqltool=MysqlTool()
    print(mysqltool.getServerTime())
