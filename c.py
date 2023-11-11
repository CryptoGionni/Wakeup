# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 12:12:52 2023

@author: gio

++++++++++
+ CLIENT +
++++++++++

"""

import threading
import socket
import re
import os
import time

############################ CLIENT FUNCTIONS ################################

#function per gestire l'input di messaggi
def client_receive():
    while True:
        try:    #decodifica il messaggio ricevuto
            message = client.recv(1024).decode('utf-8')
            
            #se il server ci chiede l'alias (quando ci risponde "alias?"), noi glielo mandiamo
            if message == "alias?":
                client.send(alias.encode('utf-8'))
            #altrimenti invia normalmente il messaggio
            else:
                print(message)
                
        except:     #altrimenti errore
            print('Error in client_recive!')
            client.close()
            break


#function per intercettare il comando "meme/" se digitato da tastiera
def check_meme_command(string1_message, string2_command):
	
    #vedi se matcha
    pattern = re.compile(string2_command)
    match = re.search(pattern, string1_message)

    if match:       #se il comando c'è
        
        #find meme string
        path = "ASCII-art\\"
        filename = string1_message.split("/")     #ignora ciò che c'è prima di /
        file = filename[1].lstrip(meme_command).rstrip('\n')   #togli la stringa comando e il d'accapo      
        
        if file == "":      #se il comando è seguito da una stringa vuota
            
            #print list meme
            print(os.listdir(path))
            print("\nnota:\n1) non usare il .txt che vedi nella lista per invocare un meme\n2) per una migliore visualizzazione ridurre la font-size del terminale\n3) esempio corretto: meme/theRock\n")
            
        else:       #se invece è seguito da qualcosa
        
            try:        #prova a vedere se quel qualcosa è effettivamente un nome di un file corretto
                #print meme inviando una stringa alla volta
                file_object = open(path + file + ".txt", "r", encoding="utf-8")
                temp_alias = f"[{alias}]:"
                client.send(temp_alias.encode('utf-8'))
                for string in file_object:
                    #print(string.rstrip())
                    client.send(string.rstrip().encode('utf-8'))
                    time.sleep(0.2)
                file_object.close()
                
            except:         #se invece dà errore la open, significa che il nome dato dopo il comando non è corretto
                print("\nmeme not found!\n1) controlla se questo meme esiste nella lista digitando solo: meme/\n2) non usare il .txt che vedi nella lista per invocare un meme\n")
                
    else:       #se invece il comando non c'è, allora stampa normalmente il messaggio
        client.send(string1_message.encode('utf-8'))




#function per gestire l'output di messaggi
def client_send():
    while True:
        message = f'[{alias}]: {input("")}\n'
        check_meme_command(message, meme_command)


def print_head():
    # Give the correct filename with path in the following line.
    head_path = "ASCII-art\\head.txt"
    file_object = open(head_path, "r", encoding="utf-8")
    
    # Loop over and print each line in the file object.
    for string in file_object:
        print(string.rstrip())
    
    # Close the file object.
    file_object.close()

############################ END CLIENT FUNCTIONS ################################


meme_command = "meme/"
serverIP = '' #server al quale ti vuoi connettere (tutti i client devono collegarsi allo stesso server)
print_head()
alias = input('[Server] Choose an alias >>> ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((serverIP, 59000))


#creo 2 tred: per input e per output
receive_thread = threading.Thread(target=client_receive)
receive_thread.start()
#
send_thread = threading.Thread(target=client_send)
send_thread.start()