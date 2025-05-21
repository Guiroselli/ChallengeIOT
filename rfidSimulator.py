"""
Simulação de Sistema RFID para Mapeamento e Gestão de Motos da Mottu

Este protótipo simula um sistema de rastreamento baseado em RFID para o mapeamento
e gestão das motos da Mottu em seus pátios. O sistema permite o rastreamento em tempo real
da localização das motos, monitoramento de entrada/saída e visualização do layout do pátio.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import random
import time
from datetime import datetime, timedelta
import uuid

# Configurações do pátio
PATIO_WIDTH = 100  # largura do pátio em metros
PATIO_HEIGHT = 80  # altura do pátio em metros

# Áreas do pátio
AREAS = {
    'entrada': {'x': 0, 'y': 35, 'width': 10, 'height': 10, 'color': 'lightblue'},
    'saida': {'x': 90, 'y': 35, 'width': 10, 'height': 10, 'color': 'lightgreen'},
    'estacionamento': {'x': 20, 'y': 10, 'width': 60, 'height': 60, 'color': 'lightgray'},
    'manutencao': {'x': 20, 'y': 70, 'width': 30, 'height': 10, 'color': 'lightyellow'}
}

# Configurações dos leitores RFID
READERS = [
    {'id': 1, 'x': 5, 'y': 40, 'range': 15, 'color': 'red'},  # Entrada
    {'id': 2, 'x': 95, 'y': 40, 'range': 15, 'color': 'green'},  # Saída
    {'id': 3, 'x': 30, 'y': 30, 'range': 20, 'color': 'blue', 'name': 'Setor A'},  # Estacionamento 1
    {'id': 4, 'x': 60, 'y': 30, 'range': 20, 'color': 'blue', 'name': 'Setor B'},  # Estacionamento 2
    {'id': 5, 'x': 30, 'y': 60, 'range': 20, 'color': 'blue', 'name': 'Setor C'},  # Estacionamento 3
    {'id': 6, 'x': 60, 'y': 60, 'range': 20, 'color': 'blue', 'name': 'Setor D'},  # Estacionamento 4
    {'id': 7, 'x': 35, 'y': 75, 'range': 15, 'color': 'orange'}  # Manutenção
]

# Modelos de motos disponíveis
MOTO_MODELS = [
    'Sport 110i', 'CG 160', 'Factor 125', 'Biz 125', 'NMax 160', 'PCX 150'
]

class Moto:
    """Classe que representa uma moto com tag RFID"""
    
    def __init__(self, moto_id=None):
        self.id = moto_id if moto_id else str(uuid.uuid4())[:8]
        self.model = random.choice(MOTO_MODELS)
        self.status = random.choice(['disponível', 'reservada', 'em manutenção'])
        self.fuel_level = random.randint(10, 100)
        self.last_maintenance = datetime.now() - timedelta(days=random.randint(0, 90))
        
        # Posição inicial
        if self.status == 'em manutenção':
            self.x = AREAS['manutencao']['x'] + random.randint(5, AREAS['manutencao']['width'] - 5)
            self.y = AREAS['manutencao']['y'] + random.randint(2, AREAS['manutencao']['height'] - 2)
        else:
            self.x = AREAS['estacionamento']['x'] + random.randint(5, AREAS['estacionamento']['width'] - 5)
            self.y = AREAS['estacionamento']['y'] + random.randint(5, AREAS['estacionamento']['height'] - 5)
        
        # Histórico de movimentação
        self.movement_history = []
        self.record_position()
        
        # Cor baseada no status
        self.update_color()
    
    def update_color(self):
        """Atualiza a cor da moto baseada em seu status"""
        if self.status == 'disponível':
            self.color = 'green'
        elif self.status == 'reservada':
            self.color = 'blue'
        else:  # em manutenção
            self.color = 'orange'
    
    def move(self, dx, dy):
        """Move a moto em uma direção específica"""
        self.x += dx
        self.y += dy
        
        # Garantir que a moto permaneça dentro dos limites do pátio
        self.x = max(0, min(self.x, PATIO_WIDTH))
        self.y = max(0, min(self.y, PATIO_HEIGHT))
        
        self.record_position()
    
    def record_position(self):
        """Registra a posição atual no histórico"""
        self.movement_history.append({
            'timestamp': datetime.now(),
            'x': self.x,
            'y': self.y,
            'status': self.status,
            'fuel_level': self.fuel_level
        })
    
    def update_status(self, new_status):
        """Atualiza o status da moto"""
        self.status = new_status
        self.update_color()
        self.record_position()
    
    def update_fuel(self, amount):
        """Atualiza o nível de combustível"""
        self.fuel_level = max(0, min(100, self.fuel_level + amount))
        self.record_position()
    
    def perform_maintenance(self):
        """Realiza manutenção na moto"""
        self.last_maintenance = datetime.now()
        self.fuel_level = 100
        self.update_status('disponível')
    
    def __str__(self):
        return f"Moto {self.id} ({self.model}) - Status: {self.status}, Combustível: {self.fuel_level}%"


class RFIDReader:
    """Classe que representa um leitor RFID"""
    
    def __init__(self, reader_id, x, y, detection_range, color='red', name=None):
        self.id = reader_id
        self.x = x
        self.y = y
        self.range = detection_range
        self.color = color
        self.name = name
        self.detections = []
    
    def detect_motos(self, motos):
        """Detecta motos dentro do alcance do leitor"""
        detected = []
        for moto in motos:
            distance = np.sqrt((self.x - moto.x)**2 + (self.y - moto.y)**2)
            if distance <= self.range:
                detected.append(moto)
                self.record_detection(moto)
        return detected
    
    def record_detection(self, moto):
        """Registra uma detecção de moto"""
        self.detections.append({
            'timestamp': datetime.now(),
            'moto_id': moto.id,
            'moto_model': moto.model,
            'moto_status': moto.status,
            'moto_x': moto.x,
            'moto_y': moto.y,
            'distance': np.sqrt((self.x - moto.x)**2 + (self.y - moto.y)**2)
        })
    
    def get_recent_detections(self, seconds=60):
        """Retorna detecções recentes"""
        cutoff_time = datetime.now() - timedelta(seconds=seconds)
        return [d for d in self.detections if d['timestamp'] > cutoff_time]


class MottuPatioSimulation:
    """Classe principal para simulação do pátio da Mottu com sistema RFID"""
    
    def __init__(self, num_motos=30):
        self.motos = [Moto() for _ in range(num_motos)]
        self.readers = [RFIDReader(r['id'], r['x'], r['y'], r['range'], r['color'], r.get('name')) for r in READERS]
        self.events_log = []
        self.current_time = datetime.now()
        self.setup_visualization()
    
    def setup_visualization(self):
        """Configura a visualização do pátio"""
        self.fig, self.ax = plt.subplots(figsize=(12, 10))
        self.fig.suptitle('Simulação de Sistema RFID para Pátio da Mottu', fontsize=16)
        
        # Configurar limites do pátio
        self.ax.set_xlim(0, PATIO_WIDTH)
        self.ax.set_ylim(0, PATIO_HEIGHT)
        self.ax.set_xlabel('Posição X (metros)')
        self.ax.set_ylabel('Posição Y (metros)')
        
        # Desenhar áreas do pátio
        for name, area in AREAS.items():
            rect = patches.Rectangle(
                (area['x'], area['y']), area['width'], area['height'],
                linewidth=1, edgecolor='black', facecolor=area['color'], alpha=0.3
            )
            self.ax.add_patch(rect)
            self.ax.text(
                area['x'] + area['width']/2, area['y'] + area['height']/2,
                name.upper(), ha='center', va='center'
            )
        
        # Desenhar leitores RFID
        self.reader_points = []
        self.reader_ranges = []
        for reader in self.readers:
            point = self.ax.plot([reader.x], [reader.y], 's', color=reader.color, markersize=10)[0]
            range_circle = plt.Circle((reader.x, reader.y), reader.range, 
                                     color=reader.color, fill=False, alpha=0.3)
            self.ax.add_artist(range_circle)
            # Usar nome personalizado se disponível, caso contrário usar ID
            if hasattr(reader, 'name') and reader.name:
                display_name = reader.name
            else:
                display_name = f"Leitor {reader.id}"
            self.ax.text(reader.x, reader.y-5, display_name, ha='center')
            self.reader_points.append(point)
            self.reader_ranges.append(range_circle)
        
        # Desenhar motos
        self.moto_points = []
        for moto in self.motos:
            point = self.ax.plot([moto.x], [moto.y], 's', color=moto.color, markersize=8)[0]
            self.moto_points.append(point)
        
        # Informações de status - MOVIDA PARA A ESQUERDA
        self.status_text = self.ax.text(5, 5, '', fontsize=10, 
                                       bbox=dict(facecolor='white', alpha=0.7))
        
        # Legenda colorida - MOVIDA PARA PARTE INFERIOR DIREITA
        self.ax.text(80, 10, "Disponível", color='green', fontsize=10)
        self.ax.text(80, 15, "Reservada", color='blue', fontsize=10)
        self.ax.text(80, 20, "Manutenção", color='orange', fontsize=10)
    
    def update_visualization(self, frame):
        """Atualiza a visualização do pátio"""
        # Atualizar posição das motos
        for i, moto in enumerate(self.motos):
            if i < len(self.moto_points):
                self.moto_points[i].set_data([moto.x], [moto.y])
                self.moto_points[i].set_color(moto.color)
        
        # Detectar motos com leitores RFID
        all_detections = []
        for reader in self.readers:
            detected = reader.detect_motos(self.motos)
            all_detections.extend([{
                'reader_id': reader.id,
                'moto_id': moto.id,
                'timestamp': datetime.now()
            } for moto in detected])
        
        # Atualizar texto de status
        status_counts = {
            'disponível': sum(1 for moto in self.motos if moto.status == 'disponível'),
            'reservada': sum(1 for moto in self.motos if moto.status == 'reservada'),
            'em manutenção': sum(1 for moto in self.motos if moto.status == 'em manutenção')
        }
        
        status_text = f"Total de Motos: {len(self.motos)}\n"
        status_text += f"Disponíveis: {status_counts['disponível']}\n"
        status_text += f"Reservadas: {status_counts['reservada']}\n"
        status_text += f"Em Manutenção: {status_counts['em manutenção']}\n"
        status_text += f"Detecções RFID: {len(all_detections)}\n"
        status_text += f"(Uma moto pode ser detectada\npor múltiplos leitores)"
        
        self.status_text.set_text(status_text)
        
        # REMOVIDO: Não simular movimentos aleatórios para as motos ficarem estáticas
        # self.simulate_movements()
        
        return self.moto_points + [self.status_text]
    
    def simulate_movements(self):
        """Simula movimentos aleatórios das motos"""
        # Esta função não é mais chamada para manter as motos estáticas
        pass
    
    def run_simulation(self, frames=100, interval=200):
        """Executa a simulação animada"""
        self.animation = FuncAnimation(
            self.fig, self.update_visualization, frames=frames,
            interval=interval, blit=True
        )
        plt.tight_layout()
        plt.show()
    
    def generate_report(self):
        """Gera um relatório com estatísticas da simulação"""
        report = {
            'total_motos': len(self.motos),
            'status_counts': {
                'disponível': sum(1 for moto in self.motos if moto.status == 'disponível'),
                'reservada': sum(1 for moto in self.motos if moto.status == 'reservada'),
                'em manutenção': sum(1 for moto in self.motos if moto.status == 'em manutenção')
            },
            'fuel_levels': {
                'crítico (<20%)': sum(1 for moto in self.motos if moto.fuel_level < 20),
                'baixo (20-50%)': sum(1 for moto in self.motos if 20 <= moto.fuel_level < 50),
                'médio (50-80%)': sum(1 for moto in self.motos if 50 <= moto.fuel_level < 80),
                'alto (>80%)': sum(1 for moto in self.motos if moto.fuel_level >= 80)
            },
            'reader_detections': {reader.id: len(reader.detections) for reader in self.readers}
        }
        return report


# Função para executar a simulação
def run_mottu_rfid_simulation(num_motos=30, frames=200, interval=200):
    """Executa a simulação do sistema RFID da Mottu"""
    print("Iniciando simulação do sistema RFID para o pátio da Mottu...")
    print(f"Número de motos: {num_motos}")
    print(f"Número de leitores RFID: {len(READERS)}")
    
    simulation = MottuPatioSimulation(num_motos=num_motos)
    simulation.run_simulation(frames=frames, interval=interval)
    
    report = simulation.generate_report()
    print("\nRelatório da Simulação:")
    print(f"Total de motos: {report['total_motos']}")
    print("Status das motos:")
    for status, count in report['status_counts'].items():
        print(f"  - {status}: {count}")
    
    print("Níveis de combustível:")
    for level, count in report['fuel_levels'].items():
        print(f"  - {level}: {count}")
    
    print("Detecções por leitor RFID:")
    for reader_id, count in report['reader_detections'].items():
        print(f"  - Leitor {reader_id}: {count} detecções")
    
    return simulation


# Executar a simulação se o script for executado diretamente
if __name__ == "__main__":
    run_mottu_rfid_simulation(num_motos=30)