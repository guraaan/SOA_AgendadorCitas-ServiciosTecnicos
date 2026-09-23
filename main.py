import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from servicios import Servicio, guardar_servicio, listar_servicios, actualizar_servicio, eliminar_servicio
from citas import Cita, es_feriado, guardar_cita, listar_citas, eliminar_cita


class App:
    def __init__(self, root):
        self.root = root
        root.title("Gestor de Servicios Técnicos")
        root.geometry("900x550")

        # Pestañas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Pestaña Servicios
        self.tab_servicios = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_servicios, text="Servicios")
        self.construir_tab_servicios()

        # Pestaña Citas
        self.tab_citas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_citas, text="Citas")
        self.construir_tab_citas()

        # Actualizar el combobox de servicios al cambiar de pestaña
        self.notebook.bind("<<NotebookTabChanged>>", self.al_cambiar_pestana)



    def al_cambiar_pestana(self, evento):
        if self.notebook.index(self.notebook.select()) == 1:
            self.actualizar_combobox_servicios()

    def construir_tab_servicios(self):
        # Campos
        tk.Label(self.tab_servicios, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.nombre = tk.Entry(self.tab_servicios, width=20)
        self.nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.tab_servicios, text="Descripción:").grid(row=0, column=2, padx=5, pady=5)
        self.descripcion = tk.Entry(self.tab_servicios, width=30)
        self.descripcion.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(self.tab_servicios, text="Precio:").grid(row=0, column=4, padx=5, pady=5)
        self.precio = tk.Entry(self.tab_servicios, width=10)
        self.precio.grid(row=0, column=5, padx=5, pady=5)

        # Botones
        self.btn_guardar_servicio = tk.Button(self.tab_servicios, text="Guardar", command=self.guardar_servicio)




        self.btn_guardar_servicio.grid(row=0, column=6, padx=5, pady=5)
        self.btn_editar_servicio = tk.Button(self.tab_servicios, text="Editar", command=self.editar_servicio,


                                                                     state="disabled")
        self.btn_editar_servicio.grid(row=0, column=7, padx=5, pady=5)
        self.btn_eliminar_servicio = tk.Button(self.tab_servicios, text="Eliminar", command=self.eliminar_servicio,


                                                                              state="disabled")
        self.btn_eliminar_servicio.grid(row=0, column=8, padx=5, pady=5)
        tk.Button(self.tab_servicios, text="Limpiar", command=self.limpiar_campos_servicio).grid(row=0, column=9, padx=5, pady=5)



        # Tabla de servicios
        self.tabla_servicios = ttk.Treeview(self.tab_servicios, columns=("nombre", "descripcion", "precio"), show="headings")
        self.tabla_servicios.heading("nombre", text="Nombre")
        self.tabla_servicios.heading("descripcion", text="Descripción")
        self.tabla_servicios.heading("precio", text="Precio")
        self.tabla_servicios.grid(row=1, column=0, columnspan=10, padx=10, pady=10, sticky="nsew")
        self.tabla_servicios.bind("<<TreeviewSelect>>", self.seleccionar_servicio)


        self.actualizar_tabla_servicios()

    def construir_tab_citas(self):
        # Campos
        tk.Label(self.tab_citas, text="Servicio:").grid(row=0, column=0, padx=5, pady=5)
        self.cita_servicio = ttk.Combobox(self.tab_citas, width=20, state="readonly")
        self.cita_servicio.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.tab_citas, text="Cliente:").grid(row=0, column=2, padx=5, pady=5)
        self.cita_cliente = tk.Entry(self.tab_citas, width=20)




        self.cita_cliente.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(self.tab_citas, text="Fecha (AAAA-MM-DD):").grid(row=0, column=4, padx=5, pady=5)
        self.cita_fecha = tk.Entry(self.tab_citas, width=12)


        self.cita_fecha.grid(row=0, column=5, padx=5, pady=5)


        # Botones
        self.btn_agendar_cita = tk.Button(self.tab_citas, text="Agendar", command=self.agendar_cita)


        self.btn_agendar_cita.grid(row=0, column=6, padx=5, pady=5)
        self.btn_eliminar_cita = tk.Button(self.tab_citas, text="Eliminar", command=self.eliminar_cita,


                                                                          state="disabled")
        self.btn_eliminar_cita.grid(row=0, column=7, padx=5, pady=5)
        tk.Button(self.tab_citas, text="Limpiar", command=self.limpiar_campos_cita).grid(row=0, column=8, padx=5, pady=5)



        # Tabla de citas
        self.tabla_citas = ttk.Treeview(self.tab_citas, columns=("servicio", "cliente", "fecha"), show="headings")
        self.tabla_citas.heading("servicio", text="Servicio")
        self.tabla_citas.heading("cliente", text="Cliente")
        self.tabla_citas.heading("fecha", text="Fecha")
        self.tabla_citas.grid(row=1, column=0, columnspan=9, padx=10, pady=10, sticky="nsew")
        self.tabla_citas.bind("<<TreeviewSelect>>", self.seleccionar_cita)


        self.actualizar_tabla_citas()
        self.actualizar_combobox_servicios()

    def actualizar_combobox_servicios(self):
        servicios = listar_servicios()
        nombres = [s.nombre for s in servicios]
        self.cita_servicio["values"] = nombres
        if nombres:
            self.cita_servicio.set(nombres[0])
        else:
            self.cita_servicio.set("")

    # ---- Métodos de Servicios ----
    def seleccionar_servicio(self, evento):
        seleccion = self.tabla_servicios.selection()
        if not seleccion:
            return
        self.indice_servicio = self.tabla_servicios.index(seleccion[0])
        valores = self.tabla_servicios.item(seleccion[0], "values")
        self.nombre.delete(0, tk.END)
        self.nombre.insert(0, valores[0])
        self.descripcion.delete(0, tk.END)
        self.descripcion.insert(0, valores[1])
        self.precio.delete(0, tk.END)
        self.precio.insert(0, valores[2].replace("$", ""))
        self.btn_guardar_servicio.config(state="disabled")
        self.btn_editar_servicio.config(state="normal")
        self.btn_eliminar_servicio.config(state="normal")

    def guardar_servicio(self):
        nombre = self.nombre.get()
        descripcion = self.descripcion.get()
        try:
            precio = float(self.precio.get())
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número")
            return

        if not nombre or not descripcion:
            messagebox.showerror("Error", "Nombre y descripción son obligatorios")
            return

        guardar_servicio(Servicio(nombre, descripcion, precio))


        messagebox.showinfo("Éxito", "Servicio guardado correctamente")
        self.limpiar_campos_servicio()
        self.actualizar_tabla_servicios()

    def editar_servicio(self):
        if not hasattr(self, "indice_servicio") or self.indice_servicio is None:
            messagebox.showerror("Error", "Selecciona un servicio de la tabla primero")
            return

        nombre = self.nombre.get()
        descripcion = self.descripcion.get()
        try:
            precio = float(self.precio.get())
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número")
            return

        if not nombre or not descripcion:
            messagebox.showerror("Error", "Nombre y descripción son obligatorios")
            return

        actualizar_servicio(self.indice_servicio, Servicio(nombre, descripcion, precio))
        messagebox.showinfo("Éxito", "Servicio actualizado correctamente")
        self.limpiar_campos_servicio()
        self.actualizar_tabla_servicios()

    def eliminar_servicio(self):
        if not hasattr(self, "indice_servicio") or self.indice_servicio is None:
            messagebox.showerror("Error", "Selecciona un servicio de la tabla primero")
            return

        if not messagebox.askyesno("Confirmar", "¿Seguro que quieres eliminar este servicio?"):
            return

        eliminar_servicio(self.indice_servicio)
        messagebox.showinfo("Éxito", "Servicio eliminado correctamente")
        self.limpiar_campos_servicio()
        self.actualizar_tabla_servicios()

    def limpiar_campos_servicio(self):
        self.nombre.delete(0, tk.END)
        self.descripcion.delete(0, tk.END)
        self.precio.delete(0, tk.END)
        self.indice_servicio = None
        self.btn_guardar_servicio.config(state="normal")
        self.btn_editar_servicio.config(state="disabled")
        self.btn_eliminar_servicio.config(state="disabled")

    def actualizar_tabla_servicios(self):
        for item in self.tabla_servicios.get_children():
            self.tabla_servicios.delete(item)
        for s in listar_servicios():
            self.tabla_servicios.insert("", tk.END, values=(s.nombre, s.descripcion, f"${s.precio:.2f}"))

    # ---- Métodos de Citas ----
    def seleccionar_cita(self, evento):
        seleccion = self.tabla_citas.selection()
        if not seleccion:
            return
        self.indice_cita = self.tabla_citas.index(seleccion[0])
        valores = self.tabla_citas.item(seleccion[0], "values")
        self.cita_servicio.set(valores[0])
        self.cita_cliente.delete(0, tk.END)
        self.cita_cliente.insert(0, valores[1])
        self.cita_fecha.delete(0, tk.END)
        self.cita_fecha.insert(0, valores[2])
        self.btn_agendar_cita.config(state="disabled")
        self.btn_eliminar_cita.config(state="normal")

    def agendar_cita(self):
        servicio = self.cita_servicio.get()
        cliente = self.cita_cliente.get()
        fecha = self.cita_fecha.get()

        if not servicio or not cliente:
            messagebox.showerror("Error", "Servicio y cliente son obligatorios")
            return

        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "La fecha debe tener formato AAAA-MM-DD")
            return

        feriado = es_feriado(fecha)
        if feriado is None:
            messagebox.showerror("Error", "No se pudo consultar la API de feriados. Verifica tu conexión.")
            return
        if feriado:
            messagebox.showerror("Día no laborable", f"No se puede agendar: {fecha} es feriado ({feriado}).")
            return

        guardar_cita(Cita(servicio, cliente, fecha))
        messagebox.showinfo("Éxito", "Cita agendada correctamente")
        self.limpiar_campos_cita()
        self.actualizar_tabla_citas()

    def eliminar_cita(self):
        if not hasattr(self, "indice_cita") or self.indice_cita is None:

            messagebox.showerror("Error", "Selecciona una cita de la tabla primero")
            return

        if not messagebox.askyesno("Confirmar", "¿Seguro que quieres eliminar esta cita?"):
            return

        eliminar_cita(self.indice_cita)
        messagebox.showinfo("Éxito", "Cita eliminada correctamente")
        self.limpiar_campos_cita()
        self.actualizar_tabla_citas()

    def limpiar_campos_cita(self):
        self.cita_servicio.set("")
        self.cita_cliente.delete(0, tk.END)
        self.cita_fecha.delete(0, tk.END)
        self.indice_cita = None
        self.btn_agendar_cita.config(state="normal")
        self.btn_eliminar_cita.config(state="disabled")

    def actualizar_tabla_citas(self):
        for item in self.tabla_citas.get_children():
            self.tabla_citas.delete(item)
        for c in listar_citas():
            self.tabla_citas.insert("", tk.END, values=(c.servicio, c.cliente, c.fecha))


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
