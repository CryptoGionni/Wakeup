# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 12:12:13 2023

@author: gio

++++++++++
+ SERVER +
++++++++++

"""

import threading
import socket

hostname = socket.gethostname()             #nome di questo PC
serverIP = socket.gethostbyname(hostname)   #IPv4 private di questo PC
port = 59000        #scegli una porta libera guardando nell'elenco che compare digitando "netstat" nel cmd
clients = []
aliases = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((serverIP, port))
server.listen()

############################ SERVER FUNCTIONS ################################

#function to iteratee messages
def broadcast(message):
    for client in clients:
        client.send(message)


# Function to handle clients'connections: FORWARDING
def handle_client(client):
    while True:
        try:    #prova a inviare (broadcast) agli altri client quello che hai ricevuto da "client"
            
            message = client.recv(1024) #n. max di byte inviabili: 1024
            broadcast(message)
            
        except: #altrimenti espelli il "client" e rimuovi il suo alias
        
            #gestisco il client index
            index = clients.index(client)
            clients.remove(client)
            client.close()
            
            #gestisco l'alias: ci serve l'encode perchè sono bit, non stringhe
            alias = aliases[index]
            broadcast(f'[{alias}] has left the chat room!'.encode('utf-8')) 
            print(f'[{alias}] has left the chat room! \n')
            aliases.remove(alias)
            
            break


# Main function to receive the clients connection: RECIVING
def receive():
    while True:
        
        print(f'\nServer {serverIP} is running and listening ...\n')
        client, address = server.accept() #accept() is running constantly
        print(f'connection is established with [{str(address)}]')
        client.send('alias?'.encode('utf-8'))   #il server manderà questo messaggio al client "alias?"
        
        #gestisco l'alias: creo un buffer da 1024
        alias = client.recv(1024) 
        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this new client is {alias}')
        
        #usiamo la f broadcast di prima per avvisare tutti i client già connessi
        broadcast(f'[Server] {alias} has connected to the chat room'.encode('utf-8')) 
        
        #avvisa il nuovo client che si è aggiunto correttamente
        client.send('[Server] you are now connected!'.encode('utf-8'))   
        
        #via al multithreading: ogni thread si occuperà di gestire una singola chiamata a handle_client per gestire il FORWARDING
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()



def print_head():
    # Give the correct filename with path in the following line.
    head_path = "ASCII-art\\head.txt"
    file_object = open(head_path, "r", encoding="utf-8")
    
    # Loop over and print each line in the file object.
    for string in file_object:
        print(string.rstrip())
    
    # Close the file object.
    file_object.close()

############################ END SERVER FUNCTIONS ################################


#definisco il main in cui a ripetizione invoco la recive
if __name__ == "__main__":
    print_head()
    receive()