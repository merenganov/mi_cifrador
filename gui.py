import customtkinter as ctk
from cifrado import cifrar_cesar, descifrar_cesar, cifrar_atbash, detectar_cifrado

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class DashboardCifrado(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CYBER-DASHBOARD. // SISTEMA DE CIFRADO")
        self.geometry("1000x750")

        # Layout Principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR (Panel de Configuración) ---
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="CIPHER\nPRO", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo.pack(pady=30)

        # Controles de Alfabeto
        self.lbl_config = ctk.CTkLabel(self.sidebar, text="CONFIGURACIÓN DE LENGUAJE", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_config.pack(pady=(20, 10))

        self.switch_custom = ctk.CTkSwitch(self.sidebar, text="Modo Personalizado", command=self.toggle_custom)
        self.switch_custom.pack(pady=10, padx=20, anchor="w")

        self.ent_alfabeto = ctk.CTkEntry(self.sidebar, placeholder_text="Ej: 0123456789abc", state="disabled")
        self.ent_alfabeto.pack(pady=5, padx=20, fill="x")

        self.var_enie = ctk.BooleanVar(value=True)
        self.check_enie = ctk.CTkCheckBox(self.sidebar, text="Incluir Ñ (Alfabeto 27)", variable=self.var_enie)
        self.check_enie.pack(pady=15, padx=20, anchor="w")

        self.btn_limpiar = ctk.CTkButton(self.sidebar, text="Limpiar Todo", fg_color="#444", command=self.limpiar)
        self.btn_limpiar.pack(pady=40, padx=20)

        # --- CONTENIDO PRINCIPAL ---
        self.main = ctk.CTkFrame(self, fg_color="transparent")
        self.main.grid(row=0, column=1, sticky="nsew", padx=40, pady=30)

        self.txt_entrada = ctk.CTkTextbox(self.main, height=150, border_width=2, border_color="#333")
        self.txt_entrada.pack(fill="x", pady=10)

        # Panel César
        self.cesar_frame = ctk.CTkFrame(self.main, fg_color="transparent")
        self.cesar_frame.pack(fill="x")
        ctk.CTkLabel(self.cesar_frame, text="Desplazamiento:").grid(row=0, column=0, padx=10)
        self.spin_desp = ctk.CTkOptionMenu(self.cesar_frame, values=[str(i) for i in range(1, 31)], width=90)
        self.spin_desp.grid(row=0, column=1)

        # Botones de Acción
        self.actions = ctk.CTkFrame(self.main, fg_color="transparent")
        self.actions.pack(pady=20)
        ctk.CTkButton(self.actions, text="CIFRAR CÉSAR", fg_color="#2ecc71", command=self.op_cifrar).grid(row=0, column=0, padx=10)
        ctk.CTkButton(self.actions, text="DESCIFRAR CÉSAR", fg_color="#3498db", command=self.op_descifrar).grid(row=0, column=1, padx=10)
        ctk.CTkButton(self.actions, text="ATBASH (C/D)", fg_color="#9b59b6", command=self.op_atbash).grid(row=0, column=2, padx=10)

        self.btn_auto = ctk.CTkButton(self.main, text="AUTO-DETECTAR Y DESCIFRAR", height=55, fg_color="#e67e22", command=self.op_auto)
        self.btn_auto.pack(fill="x", pady=10)

        self.txt_salida = ctk.CTkTextbox(self.main, height=220, fg_color="#000", text_color="#2ecc71", font=("Consolas", 13))
        self.txt_salida.pack(fill="x", pady=10)

    # --- LÓGICA ---
    def toggle_custom(self):
        if self.switch_custom.get():
            self.ent_alfabeto.configure(state="normal")
            self.check_enie.configure(state="disabled")
        else:
            self.ent_alfabeto.configure(state="disabled")
            self.check_enie.configure(state="normal")

    def obtener_params(self):
        custom = self.ent_alfabeto.get().strip() if self.switch_custom.get() else None
        enie = self.var_enie.get()
        return custom, enie

    def op_cifrar(self):
        t = self.txt_entrada.get("1.0", "end-1c")
        c, e = self.obtener_params()
        if t: self.escribir_salida(cifrar_cesar(t, int(self.spin_desp.get()), c, e))

    def op_descifrar(self):
        t = self.txt_entrada.get("1.0", "end-1c")
        c, e = self.obtener_params()
        if t: self.escribir_salida(descifrar_cesar(t, int(self.spin_desp.get()), c, e))

    def op_atbash(self):
        t = self.txt_entrada.get("1.0", "end-1c")
        c, e = self.obtener_params()
        if t: self.escribir_salida(cifrar_atbash(t, c, e))

    def op_auto(self):
        t = self.txt_entrada.get("1.0", "end-1c")
        if not t: return
        c, e = self.obtener_params()
        tipo = detectar_cifrado(t, c, e)
        
        if "César" in tipo:
            d = int(tipo.split()[-1])
            final = descifrar_cesar(t, d, c, e)
        else:
            final = cifrar_atbash(t, c, e) if tipo == "Atbash" else "No se pudo identificar el cifrado."
            
        self.escribir_salida(f"--- ANÁLISIS AUTOMÁTICO ---\nMÉTODO DETECTADO: {tipo.upper()}\n\nRESULTADO:\n{final}")

    def escribir_salida(self, t):
        self.txt_salida.delete("1.0", "end")
        self.txt_salida.insert("1.0", t)

    def limpiar(self):
        self.txt_entrada.delete("1.0", "end")
        self.txt_salida.delete("1.0", "end")

if __name__ == "__main__":
    app = DashboardCifrado()
    app.mainloop()