"""
Marcela Torro - 557658
Gustavo - 559098
Matheus - 555177
Rodrigo - 550266

"""

import random
import csv
import datetime
import statistics
import sys
from typing import List, Any, Callable, Optional, Dict
from colorama import Fore, Style, init

init(autoreset=True)

# ----------------------------
# Utilitários de exibição
# ----------------------------

def title(text):
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}{text.center(60)}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")

def section(text):
    print(f"\n{Fore.BLUE}{'-'*60}")
    print(f"{Fore.BLUE}{text}")
    print(f"{Fore.BLUE}{'-'*60}{Style.RESET_ALL}")

def success(msg):
    print(f"{Fore.GREEN}✔ {msg}{Style.RESET_ALL}")

def error(msg):
    print(f"{Fore.RED}✖ {msg}{Style.RESET_ALL}")

def info(msg):
    print(f"{Fore.YELLOW}• {msg}{Style.RESET_ALL}")

# ----------------------------
# Estruturas de Dados
# ----------------------------

class Queue:
    def __init__(self): self._data = []
    def enqueue(self, item): self._data.append(item)
    def dequeue(self): return self._data.pop(0) if self._data else None
    def peek(self): return self._data[0] if self._data else None
    def is_empty(self): return not self._data
    def as_list(self): return list(self._data)

class Stack:
    def __init__(self): self._data = []
    def push(self, item): self._data.append(item)
    def pop(self): return self._data.pop() if self._data else None
    def peek(self): return self._data[-1] if self._data else None
    def is_empty(self): return not self._data
    def as_list(self): return list(self._data)

# ----------------------------
# Ordenação
# ----------------------------

def merge_sort(arr, key=lambda x: x):
    if len(arr) <= 1: return arr[:]
    mid = len(arr)//2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:]); result.extend(right[j:])
    return result

def quick_sort(arr, key=lambda x: x):
    if len(arr) <= 1: return arr[:]
    pivot = random.choice(arr)
    return (
        quick_sort([x for x in arr if key(x) < key(pivot)], key)
        + [x for x in arr if key(x) == key(pivot)]
        + quick_sort([x for x in arr if key(x) > key(pivot)], key)
    )

# ----------------------------
# Buscas
# ----------------------------

def sequential_search(arr, pred): return [x for x in arr if pred(x)]

def binary_search(arr, target, key=lambda x: x):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi)//2
        val = key(arr[mid])
        if val == target: return mid
        elif val < target: lo = mid + 1
        else: hi = mid - 1
    return -1

# ----------------------------
# Simulação de dados
# ----------------------------

ITEMS = [
    {"name": "Reagente A", "unit": "ml"},
    {"name": "Reagente B", "unit": "ml"},
    {"name": "Ponteira 200ul", "unit": "un"},
    {"name": "Lâmina", "unit": "un"},
    {"name": "Capa descartável", "unit": "un"},
    {"name": "Tubo coletor", "unit": "un"},
    {"name": "Álcool 70%", "unit": "L"},
]

def simulate_data(days=30):
    start = datetime.date.today() - datetime.timedelta(days=days)
    data = []
    for d in range(days):
        date = start + datetime.timedelta(days=d)
        for _ in range(random.randint(3, 6)):
            item = random.choice(ITEMS)
            qty = random.randint(1, 50)
            val = random.choice([30, 60, 90, 180, 365])
            data.append({
                "date": date.isoformat(),
                "item": item["name"],
                "quantity": qty,
                "validity": val
            })
    return data

def pretty_records(records, limit=6):
    for i, r in enumerate(records[:limit], 1):
        print(f"{Fore.WHITE}{i:>2}. {r['date']} | {r['item']:<20} | {r['quantity']:>3} un | validade {r['validity']} dias")
    if len(records) > limit:
        print(f"{Fore.MAGENTA}... e mais {len(records)-limit} registros{Style.RESET_ALL}")

# ----------------------------
# Relatório
# ----------------------------

def report(data):
    with open("report.md", "w", encoding="utf-8") as f:
        f.write("# Relatório — Simulação de Consumo\n\n")
        f.write("- Fila: registra consumos na ordem cronológica.\n")
        f.write("- Pilha: consultas dos últimos consumos.\n")
        f.write("- MergeSort & QuickSort: ordenação de quantidades/validade.\n")
        f.write("- Buscas: localizar insumos específicos.\n")
        f.write("\n---\n")
        f.write(f"Total de registros: {len(data)}\n")

# ----------------------------
# Menu principal
# ----------------------------

def main():
    title("💡 Dynamic Programming — Controle de Insumos")
    consumos = []
    fila = Queue()
    pilha = Stack()

    while True:
        print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════╗
║ 1) Gerar dados simulados                         ║
║ 2) Mostrar primeiros registros (Fila)            ║
║ 3) Mostrar últimos registros (Pilha)             ║
║ 4) Ordenar dados (Merge / Quick)                 ║
║ 5) Buscar item (Sequencial / Binária)            ║
║ 6) Gerar relatório                               ║
║ 0) Sair                                          ║
╚══════════════════════════════════════════════════╝{Style.RESET_ALL}
""")
        choice = input(Fore.YELLOW + "→ Escolha uma opção: " + Style.RESET_ALL).strip()

        if choice == "1":
            consumos = simulate_data()
            fila = Queue(); pilha = Stack()
            for c in consumos:
                fila.enqueue(c)
                pilha.push(c)
            success(f"{len(consumos)} registros simulados com sucesso!")

        elif choice == "2":
            if not consumos: error("Gere dados primeiro!"); continue
            section("📦 Primeiros Registros (Fila - Ordem Cronológica)")
            pretty_records(fila.as_list())

        elif choice == "3":
            if not consumos: error("Gere dados primeiro!"); continue
            section("🔄 Últimos Registros (Pilha - Ordem Inversa)")
            pretty_records(list(reversed(pilha.as_list())))

        elif choice == "4":
            if not consumos: error("Gere dados primeiro!"); continue
            m = input("Método (merge/quick): ").lower()
            if m not in ["merge", "quick"]: error("Método inválido."); continue
            key = input("Campo (quantity/validity/item): ").lower()
            if key not in ["quantity", "validity", "item"]: error("Campo inválido."); continue
            keyfunc = (lambda r: r[key]) if key != "quantity" else (lambda r: int(r["quantity"]))
            sorted_list = merge_sort(consumos, keyfunc) if m == "merge" else quick_sort(consumos, keyfunc)
            section(f"📊 Registros Ordenados por {key} ({m.title()} Sort)")
            pretty_records(sorted_list)

        elif choice == "5":
            if not consumos: error("Gere dados primeiro!"); continue
            mode = input("Busca (s = sequencial / b = binária): ").lower()
            term = input("Nome do item (ex: Lâmina): ").strip()
            if mode == "s":
                res = sequential_search(consumos, lambda r: r["item"].lower() == term.lower())
            else:
                arr = merge_sort(consumos, key=lambda r: r["item"])
                idx = binary_search(arr, term, key=lambda r: r["item"])
                res = [arr[idx]] if idx != -1 else []
            if res:
                success(f"{len(res)} resultado(s) encontrado(s):")
                pretty_records(res)
            else:
                error("Nenhum resultado encontrado.")

        elif choice == "6":
            if not consumos: error("Gere dados primeiro!"); continue
            report(consumos)
            success("Relatório 'report.md' gerado!")

        elif choice == "0":
            print(Fore.CYAN + "\nEncerrando o sistema...")
            break
        else:
            error("Opção inválida!")

# ----------------------------
# Execução
# ----------------------------
if __name__ == "__main__":
    main()
''