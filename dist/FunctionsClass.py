import shutil, os, stat
from .BackupClass import Backup

class Functions:
    running = True
    backupsList = list()
    namesList = list()
    originsList = list()
    pathsList = list()
    statusList = list()
    lastBackupList = list()

    def __init__(self):
        try:
            backups = open('./db/backups.txt', 'r')
            status = open('./db/status.txt', 'r', encoding='utf-8')
        except:
            os.mkdir('db')
            backups = open('./db/backups.txt', 'a')
            status = open('./db/status.txt', 'a', encoding='utf-8')
            backups.close()
            status.close()

        backups = open('./db/backups.txt', 'r')
        status = open('./db/status.txt', 'r', encoding='utf-8')
        backupsLines = backups.readlines()
        statusLines = status.readlines()
  
        for line in statusLines[1::2]:
            self.lastBackupList.append(line[:-1])
        
        for name in backupsLines[0::3]:
            self.namesList.append(name[:-1])
        
        for origin in backupsLines[1::3]:
            self.originsList.append(origin[:-1])
        
        for path in backupsLines[2::3]:
            self.pathsList.append(path[:-1])

        for name in self.namesList:
            src = self.originsList[self.namesList.index(name)]
            des = self.pathsList[self.namesList.index(name)]
            self.backupsList.append(Backup(name, src, des))

        for line in self.backupsList:
            self.backupsList[self.backupsList.index(line)].updateLastBackup(self.lastBackupList[self.backupsList.index(line)])
            self.backupsList[self.backupsList.index(line)].setLastModification()
            self.backupsList[self.backupsList.index(line)].updateStatus()

            self.statusList.append(self.backupsList[self.backupsList.index(line)].getStatus())

        backups.close()
        status.close()

    def addBackup(self):
        name = input('\nNome: ')
        
        if(name in self.namesList):
            print('Já existe um backup com esse nome. Tente novamente.')
        else:
            src = input('Origem: ').replace('\\', '/')
            path = input('Destino: ').replace('\\', '/')
            des = path + '/' + name

            try:
                hexa = 0
                for folder in os.listdir(path):
                    if(name == folder[:-4]):
                        if(folder[-1] == ']'):
                            if(int(folder[folder.find('[') +1:folder.find(']')], 16) > hexa):
                                hexa = int(folder[folder.find('[') +1:folder.find(']')], 16)
                    elif(name == folder):
                        des = des + ' [1]'
                        
                if(hexa != 0):
                    des = des[:-2] + hex(hexa+1)[2:].upper() + ']'

                if(src == path):
                    print('A origem não pode ser igual ao destino.')
                else:
                    self.backupsList.append(Backup(name, src, des))
                
                    self.newBackup(self.backupsList[len(self.backupsList)-1].getOrigin(), self.backupsList[len(self.backupsList)-1].getPath())
                    self.backupsList[len(self.backupsList)-1].setLastModification()
                    self.backupsList[len(self.backupsList)-1].setLastBackup()
                    self.backupsList[len(self.backupsList)-1].updateStatus()

                    self.statusList.append(self.backupsList[len(self.backupsList)-1].getStatus())
                    self.lastBackupList.append(self.backupsList[len(self.backupsList)-1].getLastBackup())
                    self.namesList.append(name)

                    if(len(self.statusList) > 0):
                        self.statusList[len(self.backupsList)-1] = self.backupsList[len(self.backupsList)-1].getStatus()
                        self.lastBackupList[len(self.backupsList)-1] = self.backupsList[len(self.backupsList)-1].getLastBackup()

                    with open('./db/backups.txt', 'a') as backup:
                        backup.writelines(name + '\n')
                        backup.writelines(src + '\n')
                        backup.writelines(des + '\n')

                    self.saveStatus()
                    print('Backup adicionado com sucesso!')
            except FileNotFoundError:
                print('Caminho não encontrado.')
            
    def newBackup(self, src, des):
        # Verifica se o diretório de destino existe
        try:
            os.mkdir(des)
        except:
            pass
        
        for file in os.listdir(src):
            if(os.path.isfile(src + '/' + file)):
                shutil.copy2(src + '/' + file.replace('\'', ''), des)
            else:
                try:
                    os.mkdir(des + '/' + file)
                except:
                    pass
                
                newDes = des + '/' + file
                newSrc = src + '/' + file
                self.newBackup(newSrc, newDes)

    def backupList(self):
        # Procura por atualizações
        for line in self.backupsList:
            self.backupsList[self.backupsList.index(line)].setLastModification()
            self.backupsList[self.backupsList.index(line)].updateStatus()
            self.statusList[self.backupsList.index(line)] = self.backupsList[self.backupsList.index(line)].getStatus()
        
        if(len(self.backupsList) == 0):
            print('Ainda não há backups programados.')
        else:
            for line in self.backupsList:
                print(line.getName())

            option = str(input('SunB (Backup List):$ '))

            if(option.lower() == 'exit'):
                self.running = False
            else:
                for backup in self.backupsList:                        
                    if(option.lower() == backup.getName().lower()):
                        print(f'\nNome: {backup.getName()}')
                        print(f'Origem: \'{backup.getOrigin()}\'')
                        print(f'Destino: \'{backup.getPath()}\'')

                        print(f'Última modificação: {backup.getLastModification()} ({self.statusList[self.backupsList.index(backup)]})')
                        print('\nFazer backup? (s/n)')

                        confirmation = str(input('SunB (Backup List):$ '))
                        if(confirmation.lower() == 's'):
                            print('\nCarregando...')

                            try:
                                self.newBackup(backup.getOrigin(), backup.getPath())
                                backup.setLastBackup()
                                backup.updateStatus()
                                
                                self.lastBackupList[self.backupsList.index(backup)] = backup.getLastBackup()
                                self.statusList[self.backupsList.index(backup)] = backup.getStatus()
                                self.saveStatus()
                                print('Backup Concluído.')
                            except PermissionError:
                                print('Erro: Permissão negada.')
                        elif(confirmation.lower() == 'exit'):
                            self.running = False
                            
        return self.running

    # def redo_with_write(self, redo_func, path):
    #     os.chmod(path, stat.S_IWRITE)
    #     redo_func(path)

    def saveStatus(self):
        with open('./db/status.txt', 'w', encoding='utf-8') as status:
            for i in range(len(self.backupsList)):
                status.write(self.statusList[i] + '\n')
                status.write(self.lastBackupList[i] + '\n')

    def help(self):
        print('\nadd      Adiciona um novo backup')
        print('bl       Lista todos os backups programados')
        print('exit     Finaliza o programa')
        print('help     Lista todos os comandos disponíveis\n')
