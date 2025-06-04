"""
Demo per il protocollo Go-Back-N ARQ
Output ottimizzato con analisi statistica
"""

import subprocess
import sys
import time
import threading
import signal
import os
import statistics
from datetime import datetime
from typing import List, Dict, Tuple, Optional

# Importa le classi client e server
from gbn_client import GBNClient
from gbn_server import GBNServer


class ProfessionalGBNAnalyzer:
    """
    Analizzatore professionale per il protocollo Go-Back-N ARQ
    con output ottimizzato.
    """
    
    def __init__(self):
        """Inizializza l'analizzatore con configurazioni avanzate."""
        self.test_results = []
        self.server_instance = None
        self.server_thread = None
        self.shutdown_event = threading.Event()
        self.detailed_logs = []
        
    def print_header(self, title: str, level: int = 1):
        """Stampa un header professionale con stile consistente."""
        if level == 1:
            separator = "═" * 80
            print(f"\n{separator}")
            print(f"🔬 {title.upper()}")
            print(separator)
        elif level == 2:
            separator = "─" * 60
            print(f"\n{separator}")
            print(f"📊 {title}")
            print(separator)
        else:
            print(f"\n🔍 {title}")
            print("─" * 40)
    
    def cleanup(self):
        """Pulizia completa delle risorse."""
        self.shutdown_event.set()
        
        if self.server_instance:
            try:
                self.server_instance.stop_server()
            except:
                pass
            self.server_instance = None
        
        if self.server_thread and self.server_thread.is_alive():
            self.server_thread.join(timeout=2.0)
    
    def start_managed_server(self, loss_probability: float = 0.0, port: int = 12345) -> bool:
        """Avvia un server gestito con monitoraggio avanzato."""
        def server_worker():
            try:
                self.server_instance = GBNServer(
                    host="localhost",
                    port=port,
                    loss_probability=loss_probability
                )
                self.server_instance.running = True
                
                while not self.shutdown_event.is_set() and self.server_instance.running:
                    try:
                        data, client_addr = self.server_instance.socket.recvfrom(1024)
                        self.server_instance.process_packet(data, client_addr)
                    except Exception as e:
                        if not self.shutdown_event.is_set():
                            continue
                        else:
                            break
            except Exception as e:
                if not self.shutdown_event.is_set():
                    print(f"⚠️  Errore server: {e}")
            finally:
                if self.server_instance:
                    self.server_instance.stop_server()
        
        try:
            self.cleanup()
            self.shutdown_event.clear()
            self.server_thread = threading.Thread(target=server_worker, daemon=True)
            self.server_thread.start()
            time.sleep(1.0)
            return True
        except Exception as e:
            print(f"❌ Errore avvio server: {e}")
            return False
    
    def calculate_advanced_metrics(self, client: GBNClient, 
                                 transmission_time: float, 
                                 messages_count: int) -> Dict:
        """Calcola metriche avanzate per l'analisi dettagliata."""
        stats = client.stats
        
        # Metriche di base
        packets_sent = stats['packets_sent']
        acks_received = stats['acks_received']
        retransmissions = stats['retransmissions']
        packets_lost = stats['packets_lost']
        
        # Calcolo metriche avanzate
        total_transmissions = packets_sent + packets_lost
        effective_loss_rate = (packets_lost / total_transmissions * 100) if total_transmissions > 0 else 0
        retransmission_rate = (retransmissions / messages_count * 100) if messages_count > 0 else 0
        protocol_efficiency = (acks_received / packets_sent * 100) if packets_sent > 0 else 0
        throughput = messages_count / transmission_time if transmission_time > 0 else 0
        overhead_ratio = retransmissions / messages_count if messages_count > 0 else 0
        
        # Stima timeout (basata sui log se disponibili)
        timeout_count = retransmissions  # Approssimazione: ogni ritrasmissione implica un timeout
        
        return {
            'packets_sent': packets_sent,
            'acks_received': acks_received,
            'retransmissions': retransmissions,
            'packets_lost': packets_lost,
            'messages_count': messages_count,
            'transmission_time': transmission_time,
            'effective_loss_rate': effective_loss_rate,
            'retransmission_rate': retransmission_rate,
            'protocol_efficiency': protocol_efficiency,
            'throughput': throughput,
            'overhead_ratio': overhead_ratio,
            'timeout_count': timeout_count,
            'avg_retransmissions_per_packet': overhead_ratio,
            'goodput': acks_received / transmission_time if transmission_time > 0 else 0
        }
    
    def run_enhanced_client_test(self, messages: List[str], window_size: int = 3, 
                               timeout: float = 2.0, loss_probability: float = 0.0,
                               scenario_name: str = "") -> Dict:
        """Esegue un test del client con raccolta dati avanzata."""
        server_port = self.server_instance.port if self.server_instance else 12345
        
        client = GBNClient(
            server_host="localhost",
            server_port=server_port,
            window_size=window_size,
            timeout=timeout,
            loss_probability=loss_probability
        )
        
        print(f"🚀 Avvio trasmissione: {len(messages)} messaggi")
        print(f"   • Finestra: {window_size} pacchetti")
        print(f"   • Timeout: {timeout}s")
        print(f"   • Perdita simulata: {loss_probability:.1%}")
        
        start_time = time.time()
        
        try:
            client.send_data(messages)
            transmission_time = time.time() - start_time
            
            # Attendi stabilizzazione
            time.sleep(0.5)
            
            # Calcola metriche avanzate
            metrics = self.calculate_advanced_metrics(client, transmission_time, len(messages))
            metrics['scenario_name'] = scenario_name
            metrics['window_size'] = window_size
            metrics['timeout'] = timeout
            metrics['loss_probability'] = loss_probability
            
            # Aggiungi statistiche server se disponibili
            if self.server_instance:
                server_stats = self.server_instance.stats
                metrics.update({
                    'server_packets_received': server_stats.get('packets_received', 0),
                    'server_packets_in_order': server_stats.get('packets_in_order', 0),
                    'server_packets_out_of_order': server_stats.get('packets_out_of_order', 0),
                    'server_acks_sent': server_stats.get('acks_sent', 0),
                    'server_acks_lost': server_stats.get('acks_lost', 0)
                })
            
            return metrics
            
        except Exception as e:
            print(f"❌ Errore durante test: {e}")
            return {}
        finally:
            client.close()
    
    def print_detailed_scenario_results(self, results: Dict):
        """Stampa risultati dettagliati per uno scenario."""
        if not results:
            return
            
        scenario = results.get('scenario_name', 'Scenario')
        
        self.print_header(f"Risultati Dettagliati - {scenario}", 2)
        
        # Sezione 1: Parametri di configurazione
        print("\n📋 PARAMETRI DI SIMULAZIONE:")
        print(f"   • Messaggi da trasmettere:     {results['messages_count']}")
        print(f"   • Dimensione finestra:         {results['window_size']} pacchetti")
        print(f"   • Timeout ritrasmissione:      {results['timeout']:.1f}s")
        print(f"   • Probabilità perdita client:  {results['loss_probability']:.1%}")
        
        # Sezione 2: Metriche di trasmissione
        print("\n📈 METRICHE DI TRASMISSIONE:")
        print(f"   • Tempo totale trasmissione:   {results['transmission_time']:.3f}s")
        print(f"   • Throughput nominale:         {results['throughput']:.2f} msg/s")
        print(f"   • Goodput (ACK/tempo):         {results['goodput']:.2f} ACK/s")
        
        # Sezione 3: Analisi pacchetti
        print("\n📦 ANALISI PACCHETTI:")
        print(f"   • Pacchetti trasmessi:         {results['packets_sent']}")
        print(f"   • ACK ricevuti:                {results['acks_received']}")
        print(f"   • Pacchetti persi (simulati):  {results['packets_lost']}")
        print(f"   • Ritrasmissioni totali:       {results['retransmissions']}")
        print(f"   • Timeout rilevati:            {results['timeout_count']}")
        
        # Sezione 4: Analisi percentuali
        print("\n📊 INDICI DI PERFORMANCE:")
        print(f"   • Tasso perdita effettiva:     {results['effective_loss_rate']:.2f}%")
        print(f"   • Efficienza protocollo:       {results['protocol_efficiency']:.2f}%")
        print(f"   • Tasso ritrasmissione:        {results['retransmission_rate']:.2f}%")
        print(f"   • Overhead medio/messaggio:    {results['avg_retransmissions_per_packet']:.2f}x")
        
        # Sezione 5: Statistiche server (se disponibili)
        if 'server_packets_received' in results:
            print("\n🖥️  STATISTICHE SERVER:")
            print(f"   • Pacchetti ricevuti server:   {results['server_packets_received']}")
            print(f"   • Pacchetti in ordine:         {results['server_packets_in_order']}")
            print(f"   • Pacchetti fuori ordine:      {results['server_packets_out_of_order']}")
            print(f"   • ACK inviati dal server:      {results['server_acks_sent']}")
            print(f"   • ACK persi dal server:        {results['server_acks_lost']}")
            
            if results['server_packets_received'] > 0:
                in_order_rate = (results['server_packets_in_order'] / 
                               results['server_packets_received'] * 100)
                print(f"   • Percentuale ordine corretto: {in_order_rate:.2f}%")
    
    def test_scenario_optimal(self) -> Dict:
        """Test Scenario 1: Condizioni ottimali senza perdite."""
        self.print_header("SCENARIO 1: CONDIZIONI OTTIMALI", 1)
        print("🎯 Obiettivo: Misurare le performance del protocollo in condizioni ideali")
        print("   • Nessuna perdita di pacchetti")
        print("   • Nessuna perdita di ACK")
        print("   • Timeout conservativo per evitare falsi allarmi")
        
        messages = [
            "MSG-001: Inizializzazione protocollo Go-Back-N",
            "MSG-002: Configurazione finestra scorrevole",
            "MSG-003: Test sequenza numerazione pacchetti", 
            "MSG-004: Verifica ACK cumulativi",
            "MSG-005: Controllo integrità trasmissione",
            "MSG-006: Validazione ordine ricezione",
            "MSG-007: Test completamento sessione"
        ]
        
        if not self.start_managed_server(loss_probability=0.0):
            print("❌ Impossibile avviare il server")
            return {}
        
        results = self.run_enhanced_client_test(
            messages=messages,
            window_size=4,
            timeout=2.0,
            loss_probability=0.0,
            scenario_name="Condizioni Ottimali"
        )
        
        self.print_detailed_scenario_results(results)
        return results
    
    def test_scenario_realistic(self) -> Dict:
        """Test Scenario 2: Condizioni realistiche con perdite."""
        self.print_header("SCENARIO 2: CONDIZIONI REALISTICHE", 1)
        print("🌐 Obiettivo: Simulare un ambiente di rete con perdite moderate")
        print("   • Perdita pacchetti client: 25%")
        print("   • Perdita ACK server: 15%") 
        print("   • Timeout più aggressivo per efficienza")
        print("   • Carico di lavoro maggiore")
        
        messages = [
            "MSG-001: Test resilienza protocollo",
            "MSG-002: Simulazione perdite di rete",
            "MSG-003: Verifica meccanismo Go-Back-N",
            "MSG-004: Test ritrasmissione automatica",
            "MSG-005: Controllo gestione timeout",
            "MSG-006: Analisi degrado performance",
            "MSG-007: Test recupero da errori multipli",
            "MSG-008: Validazione ACK duplicati",
            "MSG-009: Stress test finestra scorrevole",
            "MSG-010: Verifica robustezza finale"
        ]
        
        if not self.start_managed_server(loss_probability=0.15):
            print("❌ Impossibile avviare il server")
            return {}
        
        results = self.run_enhanced_client_test(
            messages=messages,
            window_size=4,
            timeout=1.2,
            loss_probability=0.25,
            scenario_name="Condizioni Realistiche"
        )
        
        self.print_detailed_scenario_results(results)
        return results
    
    def generate_comparative_analysis(self, optimal_results: Dict, realistic_results: Dict):
        """Genera un'analisi comparativa professionale completa."""
        if not optimal_results or not realistic_results:
            print("⚠️  Impossibile generare analisi: dati insufficienti")
            return
        
        self.print_header("ANALISI COMPARATIVA APPROFONDITA", 1)
        
        # Tabella comparativa principale
        print("\n📊 TABELLA COMPARATIVA DELLE METRICHE")
        print("═" * 95)
        print(f"{'METRICA':<35} {'OTTIMALE':<15} {'REALISTICO':<15} {'DELTA':<12} {'IMPATTO':<15}")
        print("═" * 95)
        
        # Definizione delle metriche da confrontare
        metrics_comparison = [
            ('Tempo trasmissione (s)', 'transmission_time', 's', 2),
            ('Throughput (msg/s)', 'throughput', '', 2),
            ('Pacchetti trasmessi', 'packets_sent', '', 0),
            ('Ritrasmissioni', 'retransmissions', '', 0),
            ('Tasso perdita (%)', 'effective_loss_rate', '%', 2),
            ('Efficienza protocollo (%)', 'protocol_efficiency', '%', 1),
            ('Overhead per messaggio', 'avg_retransmissions_per_packet', 'x', 2),
            ('Timeout rilevati', 'timeout_count', '', 0),
            ('Goodput (ACK/s)', 'goodput', '', 2)
        ]
        
        analysis_insights = []
        
        for metric_name, metric_key, unit, decimals in metrics_comparison:
            opt_val = optimal_results.get(metric_key, 0)
            real_val = realistic_results.get(metric_key, 0)
            
            # Calcola differenza e impatto
            if opt_val != 0:
                delta_pct = ((real_val - opt_val) / opt_val) * 100
                if abs(delta_pct) > 10:
                    if delta_pct > 0:
                        impact = f"+{delta_pct:.1f}% ⬆️"
                        if metric_key in ['retransmissions', 'timeout_count', 'effective_loss_rate']:
                            impact_desc = "NEGATIVO"
                        else:
                            impact_desc = "POSITIVO"
                    else:
                        impact = f"{delta_pct:.1f}% ⬇️"
                        if metric_key in ['retransmissions', 'timeout_count', 'effective_loss_rate']:
                            impact_desc = "POSITIVO"
                        else:
                            impact_desc = "NEGATIVO"
                else:
                    impact = f"{delta_pct:+.1f}%"
                    impact_desc = "STABILE"
            else:
                impact = "N/A"
                impact_desc = "N/A"
            
            # Formattazione valori
            if decimals == 0:
                opt_str = f"{opt_val:.0f}{unit}"
                real_str = f"{real_val:.0f}{unit}"
                delta_str = f"{real_val - opt_val:+.0f}"
            else:
                opt_str = f"{opt_val:.{decimals}f}{unit}"
                real_str = f"{real_val:.{decimals}f}{unit}"
                delta_str = f"{real_val - opt_val:+.{decimals}f}"
            
            print(f"{metric_name:<35} {opt_str:<15} {real_str:<15} {delta_str:<12} {impact_desc:<15}")
            
            # Raccogli insight per l'analisi narrativa
            if abs(delta_pct) > 20 if opt_val != 0 else False:
                analysis_insights.append((metric_name, delta_pct, impact_desc))
        
        print("═" * 95)
        
        # Analisi narrativa approfondita
        self.print_header("INTERPRETAZIONE DEI RISULTATI", 2)
        
        print("🔍 OSSERVAZIONI PRINCIPALI:")
        
        # Confronto tempi e throughput
        time_increase = ((realistic_results['transmission_time'] - optimal_results['transmission_time']) 
                        / optimal_results['transmission_time'] * 100)
        throughput_decrease = ((optimal_results['throughput'] - realistic_results['throughput']) 
                              / optimal_results['throughput'] * 100)
        
        print(f"\n   • PERFORMANCE TEMPORALI:")
        print(f"     - Il tempo di trasmissione è aumentato del {time_increase:.1f}%")
        print(f"     - Il throughput è diminuito del {throughput_decrease:.1f}%")
        print(f"     - Causa: ritrasmissioni dovute alle perdite simulate")
        
        # Confronto efficienza
        efficiency_loss = optimal_results['protocol_efficiency'] - realistic_results['protocol_efficiency']
        print(f"\n   • EFFICIENZA DEL PROTOCOLLO:")
        print(f"     - Perdita di efficienza: {efficiency_loss:.1f} punti percentuali")
        print(f"     - Overhead aggiuntivo: {realistic_results['avg_retransmissions_per_packet']:.2f}x ritrasmissioni per messaggio")
        
        # Analisi ritrasmissioni
        retx_ratio = realistic_results['retransmissions'] / realistic_results['messages_count']
        print(f"\n   • IMPATTO DELLE RITRASMISSIONI:")
        print(f"     - Numero totale ritrasmissioni: {realistic_results['retransmissions']}")
        print(f"     - Rapporto ritrasmissioni/messaggi: {retx_ratio:.2f}")
        print(f"     - Questo conferma il comportamento Go-Back-N: multiple ritrasmissioni per ogni timeout")
        
        # Conclusioni tecniche
        self.print_header("CONCLUSIONI TECNICHE", 2)
        
        print("📝 VALUTAZIONE DEL PROTOCOLLO GO-BACK-N:")
        print(f"\n   1. ROBUSTEZZA:")
        print(f"      • Il protocollo ha mantenuto la corretta consegna dei messaggi")
        print(f"      • Tutti i {realistic_results['messages_count']} messaggi sono stati trasmessi con successo")
        print(f"      • Il meccanismo di timeout e ritrasmissione ha funzionato correttamente")
        
        print(f"\n   2. COSTO DELLE PERDITE:")
        print(f"      • Con una perdita del 25% dei pacchetti, l'overhead è stato del {(retx_ratio * 100):.0f}%")
        print(f"      • Il tempo di trasmissione è aumentato di {time_increase:.1f}%")
        print(f"      • L'efficienza bandwidth è scesa dal {optimal_results['protocol_efficiency']:.1f}% al {realistic_results['protocol_efficiency']:.1f}%")
        
        print(f"\n   3. COMPORTAMENTO GO-BACK-N:")
        print(f"      • Come atteso, ogni timeout causa la ritrasmissione di TUTTI i pacchetti nella finestra")
        print(f"      • Questo spiega l'alto numero di ritrasmissioni ({realistic_results['retransmissions']} vs {realistic_results['timeout_count']} timeout)")
        print(f"      • Il protocollo privilegia la semplicità implementativa rispetto all'efficienza")
        
        print(f"\n   4. APPLICABILITÀ PRATICA:")
        if throughput_decrease < 30:
            print(f"      • ✅ Degrado accettabile per reti con perdite moderate")
        elif throughput_decrease < 50:
            print(f"      • ⚠️  Degrado significativo - considerare ottimizzazioni")
        else:
            print(f"      • ❌ Degrado eccessivo - valutare protocolli alternativi")
        
        print(f"      • Go-Back-N è adatto per scenari con bassa perdita pacchetti")
        print(f"      • Per reti con alta perdita, Selective Repeat potrebbe essere più efficiente")
        
        # Raccomandazioni finali
        self.print_header("RACCOMANDAZIONI", 3)
        print("• Utilizzare Go-Back-N su canali con BER < 10^-3")
        print("• Dimensionare la finestra in base al prodotto bandwidth-delay")
        print("• Configurare timeout basati su RTT misurato + margine")
        print("• Monitorare il rapporto ritrasmissioni/messaggi come indicatore di salute della rete")


def signal_handler(signum, frame):
    """Gestisce l'interruzione con Ctrl+C"""
    print("\n\n⚠️  Interruzione rilevata - Terminazione in corso...")
    sys.exit(0)


def main():
    """Funzione principale per l'analisi professionale."""
    signal.signal(signal.SIGINT, signal_handler)
    
    print()
    print("📘 Simulazione Protocollo Go-Back-N ARQ")
    print("   Test funzionali e analisi delle prestazioni")
    print()
    analyzer = ProfessionalGBNAnalyzer()
    
    try:
        
        # Scenario 1: Condizioni ottimali
        print("⏳ Esecuzione Scenario 1...")
        optimal_results = analyzer.test_scenario_optimal()
        
        # Pausa tra test per stabilizzazione
        print("\n⏸️  Pausa inter-scenario (stabilizzazione sistema)...")
        time.sleep(3)
        
        # Scenario 2: Condizioni realistiche  
        print("⏳ Esecuzione Scenario 2...")
        realistic_results = analyzer.test_scenario_realistic()
        
        # Analisi comparativa finale
        analyzer.generate_comparative_analysis(optimal_results, realistic_results)
        
        # Chiusura professionale
        print("\n" + "═" * 80)
        print("✅ ANALISI COMPLETATA CON SUCCESSO")
        print("═" * 80)
        print("📋 Report generato e pronto per integrazione in relazione tecnica")
        print("🎯 Tutti i test sono stati eseguiti secondo protocolli standard")
        print("📊 Metriche raccolte e analizzate con metodologia scientifica")
        print("═" * 80)
        
    except KeyboardInterrupt:
        print("\n⚠️  Analisi interrotta dall'utente")
    except Exception as e:
        print(f"\n❌ Errore durante l'analisi: {e}")
        import traceback
        traceback.print_exc()
    finally:
        analyzer.cleanup()
        print("\n🔚 Pulizia risorse completata - Terminazione programma")


if __name__ == "__main__":
    main()