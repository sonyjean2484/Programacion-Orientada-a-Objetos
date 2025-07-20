#        SISTEMA PARA AGENDAMIENTO DE CITAS MÉDICAS
#   Implementación de un sistema sencillo donde el paciente
#   puede agendar y verificar citas con médicos según disponibilidad..

#librería que presenta la hora actual del sistema
from datetime import datetime

class Paciente:
    def __init__(self, nombre, id_paciente): #método constructor
        self.nombre = nombre                #atributos de la clase paciente
        self.id_paciente = id_paciente
        self.citas = []

    def agendar_cita(self, cita): #método que presenta las citas agendadas
        self.citas.append(cita)
        ahora = datetime.now()
        print("\nCita agendada exitosamente")
        print(f"\nPaciente: {self.nombre}\nDoctor : {cita.medico.nombre} - {cita.medico.especialidad} \nDía : {cita.fecha} a las {cita.hora} ")
        print(f"\nUd agendó el día {ahora.strftime("%Y-%m-%d %H:%M:%S")}")

    def ver_citas(self):
        for cita in self.citas:
            print(cita.resumen_cita())

class Medico:
    def __init__(self, nombre, especialidad):
        self.nombre = nombre
        self.especialidad = especialidad
        self.horarios_disponibles = []

    def agregar_horario(self, fecha, hora):#agrega los horarios disponibles
        self.horarios_disponibles.append((fecha, hora))

    def mostrar_horarios(self):#presenta los horarios disponibles
        return self.horarios_disponibles

class Cita:
    def __init__(self, fecha, hora, paciente, medico): #método constructor
        self.fecha = fecha                             #atributos de la clase
        self.hora = hora
        self.paciente = paciente
        self.medico = medico

    def resumen_cita(self): #muestra las citas realizadas por el paciente
        return f"{self.fecha} - {self.hora}: {self.paciente.nombre} con el Dr. {self.medico.nombre}"

class Agenda: #crea una agenda donde se almcenan las citas
    def __init__(self):
        self.citas = [] #

    def agendar(self, fecha, hora, paciente, medico): # agendamiento de citas según la disponibilidad
        if (fecha, hora) in medico.horarios_disponibles:
            nueva_cita = Cita(fecha, hora, paciente, medico)
            self.citas.append(nueva_cita)
            paciente.agendar_cita(nueva_cita)
            medico.horarios_disponibles.remove((fecha, hora))
        else:
            print("Ese horario no está disponible.")

    def ver_todas(self):
        for cita in self.citas:
            print(cita.resumen_cita())

# --------------------------
# Simulación del sistema

# Instancia de los objetos de la clase médico y paciente
dr_carlos = Medico("Carlos Torres", "Cardiología")
paciente_sonia = Paciente("Sonia Vásquez", "P001")

# Agregar horarios disponibles
dr_carlos.agregar_horario("2025-07-01", "10:00")
dr_carlos.agregar_horario("2025-07-01", "11:00")

# Instancia de la clase agenda
agenda = Agenda()

# Agendar cita
agenda.agendar("2025-07-01", "10:00", paciente_sonia, dr_carlos)

# Ver citas del paciente
paciente_sonia.ver_citas()