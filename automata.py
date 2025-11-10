import tkinter as tk
from tkinter import messagebox

class AutomataGUI:
    def __init__(self, master):
        self.master = master
        master.title("Autómata Finito - Atención Farmacéutica")
        master.geometry("460x400")
        master.config(bg="#f7f7f7")

        # Estados de aceptación
        self.accepting_states = {"qP", "qS", "qZ"}

        self.state = "q0"

        # Etiqueta del estado actual
        self.state_label = tk.Label(
            master,
            text="Estado actual: q0 (Inicio)",
            font=("Arial", 12, "bold"),
            bg="#f7f7f7",
            fg="red"  # rojo porque q0 no es aceptor, verde si es que lo fuese
        )
        self.state_label.pack(pady=15)

        # --- Botones principales ---
        tk.Label(master, text="Seleccione tipo de atención:", bg="#f7f7f7", font=("Arial", 10, "bold")).pack()

        frame_main = tk.Frame(master, bg="#f7f7f7")
        frame_main.pack(pady=10)

        tk.Button(frame_main, text="PERFUMERÍA (P01)", width=20, bg="#d9ead3",
                  command=self.to_perfumeria).grid(row=0, column=0, padx=10, pady=5)

        tk.Button(frame_main, text="SIN RECETA (S01)", width=20, bg="#fff2cc",
                  command=self.to_sin_receta).grid(row=0, column=1, padx=10, pady=5)

        tk.Button(frame_main, text="CON RECETA (C01)", width=20, bg="#cfe2f3",
                  command=self.to_con_receta).grid(row=1, column=0, columnspan=2, pady=10)

        # --- Subbotones para el flujo "CON RECETA" ---
        self.frame_con_receta = tk.Frame(master, bg="#eef3f8")
        self.label_sub = tk.Label(self.frame_con_receta, text="Verificación de requisitos:", bg="#eef3f8", font=("Arial", 10, "bold"))
        self.label_sub.pack(pady=5)

        # Frame para los botones de requisitos para poder usar grid
        button_frame = tk.Frame(self.frame_con_receta, bg="#eef3f8")
        button_frame.pack(pady=3)

        tk.Button(button_frame, text="OBRA SOCIAL", width=18, bg="#c9daf8",
                  command=self.to_obra_social).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="RECETA MÉDICA", width=18, bg="#c9daf8",
                  command=self.to_receta_medica).grid(row=0, column=1, padx=5)

        # --- Botón Reiniciar ---
        tk.Button(master, text="Reiniciar", width=15, bg="#f4cccc", command=self.reset).pack(pady=15)

        # --- Salida ---
        self.output_label = tk.Label(master, text="", font=("Arial", 11), fg="blue", bg="#f7f7f7")
        self.output_label.pack(pady=10)

    # ----------------- Métodos de transición -----------------
    def update_state_label(self, text):
        """Actualiza el color y texto del título según el estado."""
        color = "green" if self.state in self.accepting_states else "red"
        self.state_label.config(text=text, fg=color)

    def to_perfumeria(self):
        if self.state == "q0":
            self.state = "qP"
            self.update_state_label("Estado actual: qP (PERFUMERÍA)")
            self.output_label.config(text="✅ SE ATIENDE EN X (PERFUMERÍA)")
        else:
            self.invalid_transition()

    def to_sin_receta(self):
        if self.state == "q0":
            self.state = "qS"
            self.update_state_label("Estado actual: qS (SIN RECETA)")
            self.output_label.config(text="✅ SE ATIENDE EN Y (SIN RECETA)")
        else:
            self.invalid_transition()

    def to_con_receta(self):
        if self.state == "q0":
            self.state = "qC"
            self.update_state_label("Estado actual: qC (CON RECETA)")
            self.output_label.config(text="🔍 Requiere verificación: OBRA SOCIAL y RECETA MÉDICA")
            self.frame_con_receta.pack(pady=10)
        else:
            self.invalid_transition()

    def to_obra_social(self):
        if self.state == "qC":
            self.state = "qC_OBRA"
            self.update_state_label("Estado actual: qC_OBRA (OBRA SOCIAL recibida)")
            self.output_label.config(text="✔ OBRA SOCIAL registrada. Falta RECETA MÉDICA.")
        elif self.state == "qC_REC":
            self.state = "qZ"
            self.update_state_label("Estado actual: qZ (Verificación completa)")
            self.output_label.config(text="✅ SE ATIENDE EN Z (CON RECETA)")
            self.frame_con_receta.pack_forget()
        else:
            self.invalid_transition()

    def to_receta_medica(self):
        if self.state == "qC":
            self.state = "qC_REC"
            self.update_state_label("Estado actual: qC_REC (RECETA MÉDICA recibida)")
            self.output_label.config(text="✔ RECETA MÉDICA registrada. Falta OBRA SOCIAL.")
        elif self.state == "qC_OBRA":
            self.state = "qZ"
            self.update_state_label("Estado actual: qZ (Verificación completa)")
            self.output_label.config(text="✅ SE ATIENDE EN Z (CON RECETA)")
            self.frame_con_receta.pack_forget()
        else:
            self.invalid_transition()

    def reset(self):
        self.state = "q0"
        self.update_state_label("Estado actual: q0 (Inicio)")
        self.output_label.config(text="")
        self.frame_con_receta.pack_forget()

    def invalid_transition(self):
        messagebox.showwarning("Transición inválida", f"No se puede transicionar desde {self.state}.")
        self.output_label.config(text="⚠️ Transición inválida")

# ----------------- MAIN -----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AutomataGUI(root)
    root.mainloop()
