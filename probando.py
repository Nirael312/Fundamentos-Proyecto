from automata.fa.dfa import DFA
try:
    farmacia_automata = DFA.from_jflap('farmacia.jff')
except FileNotFoundError:
    print("Error: No se encontró el archivo 'farmacia.jff'.")
    print("Asegúrate de que el archivo está en la misma carpeta que tu script.")
    exit()

contadores = {'P': 0, 'S': 0, 'C': 0}

def generar_turno(tipo):
    """Genera un nuevo número de turno y lo formatea."""
    contadores[tipo] += 1
    return f"{tipo} {contadores[tipo]:02d}"

def iniciar_atencion():
    """Función principal que guía al usuario a través del autómata."""
    estado_actual = farmacia_automata.initial_state
    print("\n--- Bienvenido a la Farmacia ---")

    while True:
        if estado_actual == 'q0':
            print("\nPor favor, seleccione una opción:")
            print("1. Perfumería")
            print("2. Medicamentos sin receta")
            print("3. Medicamentos con receta")
            entrada = input(">> ")
        
        elif estado_actual == 'q3':
            print("\n¿Cuenta con obra social? (S/N)")
            entrada = input(">> ").upper()

        elif estado_actual == 'q4':
            print("\n¿Tiene la receta médica? (S/N)")
            entrada = input(">> ").upper()
        
        else: # Si algo sale mal o llega a un estado no esperado
            print("Ha ocurrido un error. Reiniciando.")
            estado_actual = farmacia_automata.initial_state
            continue

        try:
            # Usamos el autómata para saber a qué estado movernos
            estado_actual = farmacia_automata.read_input_stepwise(estado_actual, entrada)
        except KeyError:
            print("Opción no válida. Por favor, intente de nuevo.")
            continue # Vuelve al inicio del bucle sin cambiar de estado

        # Comprobar si hemos llegado a un estado final
        if estado_actual in farmacia_automata.final_states:
            if estado_actual == 'q1': # Perfumería
                turno = generar_turno('P')
                print(f"\n¡Listo! Su turno es {turno}. Será atendido en la sección de PERFUMERÍA.")
            elif estado_actual == 'q2': # Sin Receta
                turno = generar_turno('S')
                print(f"\n¡Listo! Su turno es {turno}. Será atendido en la ventanilla de VENTA LIBRE.")
            elif estado_actual == 'q5': # Con Receta
                turno = generar_turno('C')
                print(f"\n¡Listo! Su turno es {turno}. Será atendido en la ventanilla de OBRAS SOCIALES.")
            break # Termina el bucle while

        # Comprobar si se llegó a un estado de error
        if estado_actual == 'q_error':
            print("\nNo cumple los requisitos necesarios para esta opción. No se puede generar un turno.")
            break # Termina el bucle while

# Iniciar el programa
if __name__ == "__main__":
    # Bucle para atender a múltiples clientes
    while True:
        iniciar_atencion()
        continuar = input("\n¿Desea atender a otro cliente? (S/N): ").upper()
        if continuar != 'S':
            print("Cerrando sistema de turnos.")
            break