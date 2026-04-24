import socket

HOST        = '127.0.0.1'
PORT        = 9999
BUFFER_SIZE = 1024

clienti_conectati = {}
mesaje            = [] # [{ "id": 1, "author": (ip, port), "text": "Salut" }]
id_counter        = 1

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print("=" * 50)
print(f"  SERVER UDP pornit pe {HOST}:{PORT}")
print("  Asteptam mesaje de la clienti...")
print("=" * 50)

while True:
    try:
        date_brute, adresa_client = server_socket.recvfrom(BUFFER_SIZE)
        mesaj_primit = date_brute.decode('utf-8').strip()

        parti = mesaj_primit.split(' ', 1)
        comanda = parti[0].upper()
        argumente = parti[1] if len(parti) > 1 else ''

        print(f"\n[PRIMIT] De la {adresa_client}: '{mesaj_primit}'")

        if comanda == 'CONNECT':
            if adresa_client in clienti_conectati:
                raspuns = "EROARE: Esti deja conectat la server."
            else:
                clienti_conectati[adresa_client] = True
                nr_clienti = len(clienti_conectati)
                raspuns = f"OK: Conectat cu succes. Clienti activi: {nr_clienti}"
                print(f"[SERVER] Client nou conectat: {adresa_client}")

        elif comanda == 'DISCONNECT':
            if adresa_client in clienti_conectati:
                del clienti_conectati[adresa_client]
                raspuns = "OK: Deconectat cu succes. La revedere!"
                print(f"[SERVER] Client deconectat: {adresa_client}")
            else:
                raspuns = "EROARE: Nu esti conectat la server."

        # --- Verificare Conectare Pentru Restul Comenzilor ---
        elif comanda in ['PUBLISH', 'DELETE', 'LIST']:
            if adresa_client not in clienti_conectati:
                raspuns = "EROARE: Trebuie sa fii conectat pentru a folosi aceasta comanda."
            else:
                if comanda == 'PUBLISH':
                    if not argumente:
                        raspuns = "EROARE: Mesajul nu poate fi gol."
                    else:
                        mesaje.append({
                            "id": id_counter,
                            "author": adresa_client,
                            "text": argumente
                        })
                        raspuns = f"OK: Mesaj publicat cu ID={id_counter}"
                        print(f"[SERVER] Mesaj nou de la {adresa_client}: {argumente} (ID={id_counter})")
                        id_counter += 1

                elif comanda == 'DELETE':
                    try:
                        id_de_sters = int(argumente)
                        gasit = False
                        for i, msg in enumerate(mesaje):
                            if msg['id'] == id_de_sters:
                                gasit = True
                                if msg['author'] == adresa_client:
                                    del mesaje[i]
                                    raspuns = f"OK: Mesajul cu ID={id_de_sters} a fost sters."
                                    print(f"[SERVER] Mesaj sters (ID={id_de_sters}) de catre {adresa_client}")
                                else:
                                    raspuns = "EROARE: Nu poti sterge un mesaj care nu iti apartine."
                                break
                        
                        if not gasit:
                            raspuns = f"EROARE: ID-ul {id_de_sters} nu a fost gasit."
                    except ValueError:
                        raspuns = "EROARE: ID-ul trebuie sa fie un numar intreg."

                elif comanda == 'LIST':
                    if not mesaje:
                        raspuns = "OK: Nu exista mesaje publicate."
                    else:
                        linii = [f"ID={m['id']} | Autor={m['author']} | Mesaj='{m['text']}'" for m in mesaje]
                        raspuns = "OK:\n" + "\n".join(linii)

        else:
            raspuns = f"EROARE: Comanda '{comanda}' este necunoscuta. Comenzi valide: CONNECT, DISCONNECT, PUBLISH, DELETE, LIST"

        server_socket.sendto(raspuns.encode('utf-8'), adresa_client)
        print(f"[TRIMIS]  Catre {adresa_client}: '{raspuns}'")

    except KeyboardInterrupt:
        print("\n[SERVER] Oprire server...")
        break
    except Exception as e:
        print(f"[EROARE] {e}")

server_socket.close()
print("[SERVER] Socket inchis.")
