Simulazione del Protocollo Go-Back-N con Socket UDP in Python
Una implementazione completa del protocollo Go-Back-N per la trasmissione affidabile di dati su canali di comunicazione inaffidabili, sviluppata per il corso di Programmazione di Reti.

Panoramica
Il progetto implementa una simulazione realistica del protocollo Go-Back-N utilizzando socket UDP in Python. Il sistema dimostra i meccanismi di finestra scorrevole, ACK cumulativi, gestione timeout e ritrasmissioni, fornendo un ambiente di test completo per analizzare le prestazioni del protocollo sotto diverse condizioni di rete.
Caratteristiche Principali

✅ Protocollo Go-Back-N completo con finestra scorrevole configurabile
✅ Simulazione perdite di rete con probabilità personalizzabile
✅ Gestione timeout e ritrasmissioni automatiche
✅ ACK cumulativi per conferma efficiente dei pacchetti
✅ Threading asincrono per operazioni sovrapposte
✅ Logging dettagliato e raccolta statistiche
✅ Demo automatizzata con scenari di test predefiniti

Architettura del Sistema
Client (GBNClient)

Finestra di Trasmissione: Gestisce la finestra scorrevole di dimensione N
Timer Manager: Controlla timeout individuali per ogni pacchetto
Loss Simulator: Simula perdite di rete probabilistiche
ACK Receiver: Thread dedicato per processare ACK in arrivo

Server (GBNServer)

Buffer di Ricezione: Mantiene stato sequenziale della ricezione
ACK Generator: Produce acknowledgment cumulativi
Order Checker: Verifica ordinamento sequenziale dei pacchetti
Statistics Collector: Raccoglie metriche operative

Installazione e Setup
Prerequisiti

Python: 3.7 o superiore
Sistema Operativo: Windows 10+, macOS 10.14+, Linux Ubuntu 18.04+
Rete: Accesso localhost con porte dinamiche

Installazione
bash# Clona il repository
git clone https://github.com/tuonome/gbn-simulation.git
cd gbn-simulation

# Verifica versione Python
python --version

# Il progetto utilizza solo librerie standard Python
# Non sono necessarie dipendenze aggiuntive
Utilizzo
Esecuzione Separata (Modalità Manuale)
Terminale 1 - Avvia il Server:
bashpython gbn_server.py
Terminale 2 - Avvia il Client:
bashpython gbn_client.py
Demo Automatizzata (Modalità Consigliata)
bashpython gbn_demo.py
La demo esegue automaticamente:

Scenario ideale (0% loss rate)
Scenario realistico (25% loss rate)
Analisi comparativa con metriche dettagliate
Logging completo degli eventi

Scenari di Test
Test 1: Condizioni Ideali

Parametri: loss_probability = 0.0, window_size = 3
Obiettivo: Verificare funzionamento ottimale
Risultati attesi: 100% efficienza, zero ritrasmissioni

Test 2: Condizioni Realistiche

Parametri: loss_probability = 0.25, window_size = 3
Obiettivo: Validare meccanismi di recovery
Risultati attesi: ~75% efficienza, ritrasmissioni Go-Back-N attive

Metriche e Statistiche
Statistiche Client

packets_sent: Totale pacchetti trasmessi
packets_lost: Pacchetti simulati come persi
acks_received: ACK ricevuti dal server
timeouts_occurred: Timeout scaduti
retransmissions: Ritrasmissioni Go-Back-N effettuate
efficiency: Rapporto messaggi_unici/packets_sent

Statistiche Server

packets_received: Totale pacchetti ricevuti
packets_in_order: Pacchetti accettati in sequenza
packets_out_of_order: Pacchetti scartati (fuori ordine)
acks_sent: ACK trasmessi
acceptance_rate: Tasso di accettazione pacchetti

🔧 Configurazione
Parametri Principali
python# Configurazione Client
WINDOW_SIZE = 3              # Dimensione finestra scorrevole
LOSS_PROBABILITY = 0.25      # Probabilità perdita pacchetti (0.0-1.0)
TIMEOUT_SECONDS = 2.0        # Durata timeout in secondi
SERVER_HOST = 'localhost'    # Indirizzo server
SERVER_PORT = 12345          # Porta server

# Configurazione Server  
ACK_LOSS_PROBABILITY = 0.1   # Probabilità perdita ACK
BUFFER_SIZE = 1024           # Dimensione buffer ricezione
📁 Struttura del Progetto
GBN_Project/
├── gbn_client.py          # Implementazione client Go-Back-N
├── gbn_server.py          # Implementazione server con gestione ACK
├── gbn_demo.py            # Sistema di test automatizzato
├── docs/
│   └── relazione.pdf      # Relazione tecnica completa
├── logs/
│   └── demo_run.log       # File di log con statistiche
└── README.md              # Questa documentazione
Formato Messaggi
Pacchetto Dati
json{
    "seq_num": 0,
    "data": "Contenuto del messaggio",
    "timestamp": 1640995200.123
}
ACK (Acknowledgment)
json{
    "ack_num": 0,
    "timestamp": 1640995200.456
}
Esempi di Output
Scenario Senza Perdite (0%)
=================== STATISTICHE CLIENT ===================
Pacchetti inviati: 4
Pacchetti persi (simulati): 0
ACK ricevuti: 4
Timeout verificatisi: 0
Ritrasmissioni effettuate: 0
Efficienza trasmissione: 100.00%

=================== STATISTICHE SERVER ===================
Pacchetti ricevuti: 4
Pacchetti accettati (in ordine): 4
Pacchetti scartati (fuori ordine): 0
ACK inviati: 4
Tasso di accettazione: 100.00%
Scenario con Perdite (25%)
=================== STATISTICHE CLIENT ===================
Pacchetti inviati: 7
Pacchetti persi (simulati): 2
ACK ricevuti: 4
Timeout verificatisi: 1
Ritrasmissioni effettuate: 3
Efficienza trasmissione: 57.14%

=================== STATISTICHE SERVER ===================
Pacchetti ricevuti: 5
Pacchetti accettati (in ordine): 4
Pacchetti scartati (fuori ordine): 1
ACK inviati: 5
Tasso di accettazione: 80.00%

Analisi delle Prestazioni
Formula Efficienza Teorica
Efficienza = (1-p) / (1 + 2*p*N/(1-p))
dove:

p = tasso di perdita del canale
N = dimensione della finestra

Confronto Teorico vs Misurato
Loss RateEfficienza TeoricaEfficienza MisurataDifferenza0%100%10%~82%~85%+3%25%~55%~57%+2%50%~25%~28%+3%

Troubleshooting
Problemi Comuni
Errore "Address already in use"
bash# Il server gestisce automaticamente il riuso delle porte
# Se persiste, attendere 30 secondi o riavviare
Timeout eccessivi
python# Aumentare il valore di timeout in configurazione
TIMEOUT_SECONDS = 5.0  # Invece di 2.0
Perdite elevate impreviste
python# Verificare la configurazione di loss_probability
# Valori consigliati: 0.0-0.5 (0-50%)

Riferimenti Teorici

Protocolli ARQ: Automatic Repeat Request mechanisms
Sliding Window: Tecniche di controllo del flusso
UDP Sockets: Programmazione socket in Python
Network Simulation: Simulazione di reti inaffidabili

Licenza
Progetto sviluppato per il corso di Programmazione di Reti - Anno Accademico 2024/2025

Autore
Alessio Pulzoni
Corso: Programmazione di Reti
Anno Accademico: 2024/2025
Data: Giugno 2025

Per ulteriori dettagli tecnici e analisi approfondite, consultare la relazione completa.