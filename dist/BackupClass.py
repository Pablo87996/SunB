import os, time, datetime

class Backup:
    def __init__(self, name, origin, path):
        self.setName(name)
        self.setOrigin(origin)
        self.setPath(path)

    # Name
    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    # Origin
    def getOrigin(self):
        return self.origin

    def setOrigin(self, origin):
        self.origin = origin

    # Path
    def getPath(self):
        return self.path

    def setPath(self, path):
        self.path = path

    # Last modification
    def getLastModification(self):
        return self.lastModification
    
    def getModificationYear(self):
        return self.lastModification_year

    def getModificationMonth(self):
        return self.lastModification_month

    def getModificationDay(self):
        return self.lastModification_day

    def getModificationHour(self):
        return int(self.lastModification_hour)
    
    def getModificationMin(self):
        return int(self.lastModification_min)
    
    def getModificationSec(self):
        return int(self.lastModification_sec)

    def setLastModification(self):
        self.modification_time = os.path.getmtime(self.origin)
        lastTime = time.localtime(os.path.getmtime(self.origin))

        def verify(src, lastTime):
            for file in os.listdir(src):
                path = src + '/' + file

                if(os.path.isdir(path)):
                    lastTime = verify(path, lastTime)

                if(time.localtime(os.path.getmtime(path)).tm_year > lastTime.tm_year):
                    lastTime = time.localtime(os.path.getmtime(path))
                elif(time.localtime(os.path.getmtime(path)).tm_year == lastTime.tm_year):
                    if(time.localtime(os.path.getmtime(path)).tm_mon > lastTime.tm_mon):
                        lastTime = time.localtime(os.path.getmtime(path))
                    elif(time.localtime(os.path.getmtime(path)).tm_mon == lastTime.tm_mon):
                        if(time.localtime(os.path.getmtime(path)).tm_mday > lastTime.tm_mday):
                            lastTime = time.localtime(os.path.getmtime(path))
                        elif(time.localtime(os.path.getmtime(path)).tm_mday == lastTime.tm_mday):
                            if(time.localtime(os.path.getmtime(path)).tm_hour > lastTime.tm_hour):
                                lastTime = time.localtime(os.path.getmtime(path))
                            elif(time.localtime(os.path.getmtime(path)).tm_hour == lastTime.tm_hour):
                                if(time.localtime(os.path.getmtime(path)).tm_min > lastTime.tm_min):
                                    lastTime = time.localtime(os.path.getmtime(path))
                                elif(time.localtime(os.path.getmtime(path)).tm_min == lastTime.tm_min):
                                    if(time.localtime(os.path.getmtime(path)).tm_sec > lastTime.tm_sec):
                                        lastTime = time.localtime(os.path.getmtime(path))
                                    elif(time.localtime(os.path.getmtime(path)).tm_sec == lastTime.tm_sec):
                                        lastTime = time.localtime(os.path.getmtime(path))
                #                     else:
                #                         self.modification_time = os.path.getmtime(self.origin)
                #                 else:
                #                     self.modification_time = os.path.getmtime(self.origin)
                #             else:
                #                 self.modification_time = os.path.getmtime(self.origin)
                #         else:
                #             self.modification_time = os.path.getmtime(self.origin)
                #     else:
                #         self.modification_time = os.path.getmtime(self.origin)
                # else:
                #     self.modification_time = os.path.getmtime(self.origin)

            return lastTime

        local_time = verify(self.origin, lastTime)

        self.lastModification_year = local_time.tm_year
        self.lastModification_month = local_time.tm_mon
        self.lastModification_day = local_time.tm_mday
        self.lastModification_hour = local_time.tm_hour
        self.lastModification_min = local_time.tm_min
        self.lastModification_sec = local_time.tm_sec
        self.lastModification = f'{self.lastModification_day}/{self.lastModification_month}/{self.lastModification_year} - {self.lastModification_hour}:{self.lastModification_min}:{self.lastModification_sec}'
        
    # Last backup
    def getLastBackup(self):
        return self.lastBackupDatetime
    
    def getBackupYear(self):
        return self.lastBackup_year
    
    def getBackupMonth(self):
        return self.lastBackup_month
    
    def getBackupDay(self):
        return self.lastBackup_day
    
    def getBackupHour(self):
        return self.lastBackup_hour
        
    def getBackupMin(self):
        return self.lastBackup_min

    def getBackupSec(self):
        return self.lastBackup_sec

    def updateLastBackup(self, lastbackup):
        self.lastBackupDatetime = str(lastbackup)
        date = lastbackup[0:lastbackup.find('-')-1].split('/')
        time = lastbackup[lastbackup.find('-')+2:].split(':')

        self.lastBackup_year = int(date[2])
        self.lastBackup_month = int(date[1])
        self.lastBackup_day = int(date[0])
        self.lastBackup_hour = int(time[0])
        self.lastBackup_min = int(time[1])
        self.lastBackup_sec = int(time[2])

    def setLastBackup(self):
        todayDate = datetime.date.today()
        todayTime = datetime.datetime.now()

        self.lastBackup_year = todayDate.year
        self.lastBackup_month = todayDate.month
        self.lastBackup_day = todayDate.day
        self.lastBackup_hour = todayTime.hour
        self.lastBackup_min = todayTime.minute
        self.lastBackup_sec = todayTime.second
        self.lastBackupDatetime = f'{todayDate.day}/{todayDate.month}/{todayDate.year} - {self.lastBackup_hour}:{self.lastBackup_min}:{self.lastBackup_sec}'

    # Status
    def getStatus(self):
        return self.backupStatus

    def setStatus(self, status):
        self.backupStatus = status

    def updateStatus(self):
        if(self.getModificationYear() > self.getBackupYear()):
            self.backupStatus = 'Não salva'
        elif(self.getModificationYear() == self.getBackupYear()):
            if(self.getModificationMonth() > self.getBackupMonth()):
                self.backupStatus = 'Não salva'
            elif(self.getModificationMonth() == self.getBackupMonth()):
                if(self.getModificationDay() > self.getBackupDay()):
                    self.backupStatus = 'Não salva'
                elif(self.getModificationDay() == self.getBackupDay()):
                    if(self.getModificationHour() > self.getBackupHour()):
                        self.backupStatus = 'Não salva'
                    elif(self.getModificationHour() == self.getBackupHour()):
                        if(self.getModificationMin() > self.getBackupMin()):
                            self.backupStatus = 'Não salva'
                        elif(self.getModificationMin() == self.getBackupMin()):
                            if(self.getModificationSec() > self.getBackupSec()):
                                self.backupStatus = 'Não salva'
                            elif(self.getModificationSec() == self.getBackupSec()):
                                self.backupStatus = 'Não salva'
                            else:
                                self.backupStatus = 'Salva'
                        else:
                            self.backupStatus = 'Salva'
                    else:
                        self.backupStatus = 'Salva'
                else:
                    self.backupStatus = 'Salva'
            else:
                self.backupStatus = 'Salva'
        else:
            self.backupStatus = 'Salva'
