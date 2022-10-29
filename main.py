from dist.FunctionsClass import *

def main():
    running = True
    functions = Functions()

    while running == True:
        option = str(input('SunB (main):$ '))

        if(option.lower() == 'exit'):
            running = False
        elif(option.lower() == 'add'):
            functions.addBackup()
        elif(option.lower() == 'bl'):
            verification = functions.backupList()

            if(verification == False):
                running = False
        elif(option.lower() == 'help'):
            functions.help()
        else:
            print('Comando não encontrado. Digite "help" para ver os comandos disponíveis.')

if __name__ == "__main__":
    main()
    