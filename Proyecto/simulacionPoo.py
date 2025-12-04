import numpy as np
import matplotlib.pyplot as plt
import math


class TrafficSimulation:
    """
    Simulación de tráfico vehicular en una carretera circular utilizando
    el modelo IDM (Intelligent Driver Model) y eventos de frenado periódico
    del vehículo líder.

    Esta clase encapsula toda la lógica del sistema: parámetros del modelo,
    estado dinámico, reglas de actualización, detección de frenados,
    mecanismo anti-colisión y visualización animada.

    La simulación contiene N vehículos distribuidos sobre un circuito circular,
    donde el vehículo 0 actúa como líder y se detiene periódicamente según
    un patrón configurable.
    """

    def __init__(self):
        """
        Inicializa los parámetros físicos, modelo IDM, configuración de
        frenazos del líder y el estado inicial de posiciones y velocidades.
        """

        # Parámetros Globales
        self.N = 22
        """int: Número total de vehículos en el circuito."""

        self.CIRC = 230.0
        """float: Longitud total del circuito en metros."""

        self.DT = 0.05
        """float: Paso de tiempo de integración (Euler)."""

        self.SIM_TIME = 1200.0
        """float: Tiempo total de simulación en segundos."""

        # Parámetros Físicos
        self.L_VEHICLE = 4.0
        """float: Longitud de cada vehículo en metros."""

        self.S0 = 2.0
        """float: Distancia mínima permisible (jam distance)."""

        # Modelo IDM
        self.V0 = 10.0
        """float: Velocidad deseada."""

        self.A_MAX = 1.0
        """float: Aceleración máxima permitida."""

        self.B_DECEL = 4.0
        """float: Desaceleración cómoda."""

        self.T_HEADWAY = 1.6
        """float: Tiempo de separación deseado entre vehículos."""

        # Eventos de parada del líder
        self.STOP_DURATION = 2.0
        """float: Duración de cada frenazo del líder."""

        self.FIRST_STOP = 2.0
        """float: Momento en que ocurre el primer frenazo."""

        self.REPEAT_INTERVAL = 10.0
        """float: Intervalo entre frenazos consecutivos."""

        # Estado inicial
        self.s = np.linspace(0, self.CIRC, self.N, endpoint=False)
        """np.ndarray: Posiciones iniciales sobre el circuito circular."""

        self.v = np.ones(self.N) * self.V0
        """np.ndarray: Velocidades iniciales."""

        # Visualización
        self.fig, self.ax = None, None

    #  MÉTODOS DEL MODELO

    def get_gap(self, i, s_curr):
        """
        Calcula la distancia disponible entre el vehículo `i` y su líder.

        Args:
            i (int): Índice del vehículo.
            s_curr (np.ndarray): Vector actual de posiciones.

        Returns:
            float: Distancia libre efectiva al vehículo de adelante.
        """
        leader_idx = (i - 1 + self.N) % self.N
        dist = s_curr[leader_idx] - s_curr[i]
        if dist < 0:
            dist += self.CIRC
        return dist - self.L_VEHICLE

    def idm_accel(self, v_curr, v_leader, gap):
        """
        Calcula la aceleración según el modelo IDM (Intelligent Driver Model).

        Args:
            v_curr (float): Velocidad del vehículo actual.
            v_leader (float): Velocidad del vehículo líder inmediato.
            gap (float): Distancia libre al líder.

        Returns:
            float: Aceleración resultante según el modelo.
        """
        delta_v = v_curr - v_leader

        s_star = self.S0 + max(
            0.0,
            v_curr * self.T_HEADWAY +
            (v_curr * delta_v) / (2 * math.sqrt(self.A_MAX * self.B_DECEL))
        )

        effective_gap = max(0.01, gap)

        accel = self.A_MAX * (
            1 - (v_curr / self.V0)**4 - (s_star / effective_gap)**2
        )
        return accel

    def leader_stopped(self, t):
        """
        Determina si el vehículo líder debe estar detenido en el tiempo `t`.

        Los frenazos ocurren en:
        - FIRST_STOP
        - FIRST_STOP + REPEAT_INTERVAL
        - FIRST_STOP + 2*REPEAT_INTERVAL
        etc.

        Y duran STOP_DURATION segundos cada uno.

        Args:
            t (float): Tiempo actual de la simulación.

        Returns:
            bool: True si el líder debe estar frenando o detenido.
        """
        time_since_start = t - self.FIRST_STOP
        if time_since_start >= 0:
            cycle_pos = time_since_start % self.REPEAT_INTERVAL
            return cycle_pos < self.STOP_DURATION
        return False

    def run_step(self, t):
        """
        Ejecuta un paso de simulación: calcula aceleraciones, actualiza
        velocidades y posiciones, y aplica la regla anti-colisión.

        Args:
            t (float): Tiempo actual.
        """
        s_new = np.copy(self.s)
        v_new = np.copy(self.v)
        accel = np.zeros(self.N)

        p0_is_stopped = self.leader_stopped(t)

        # Calcular aceleraciones
        for i in range(self.N):
            if i == 0:
                if p0_is_stopped:
                    if self.v[i] > 0:
                        accel[i] = -10.0
                    else:
                        accel[i] = 0.0
                        v_new[i] = 0.0
                else:
                    accel[i] = self.A_MAX * (1 - (self.v[i] / self.V0)**4)
            else:
                leader_idx = (i - 1 + self.N) % self.N
                gap = self.get_gap(i, self.s)
                accel[i] = self.idm_accel(self.v[i], self.v[leader_idx], gap)

        # Actualizar posiciones y velocidades (Euler)
        for i in range(self.N):
            if i == 0 and p0_is_stopped and v_new[i] == 0:
                continue

            v_new[i] = max(0.0, self.v[i] + accel[i] * self.DT)
            s_new[i] = (self.s[i] + v_new[i] * self.DT) % self.CIRC

            # Regla anti-colisión
            if i != 0:
                gap = self.get_gap(i, self.s)
                if (v_new[i] * self.DT) > (gap - 0.5):
                    v_new[i] = max(0.0, (gap - 0.5) / self.DT)
                    s_new[i] = (self.s[i] + v_new[i] * self.DT) % self.CIRC

        self.s = s_new
        self.v = v_new

    #  VISUALIZACIÓN
    def setup_draw(self):
        """
        Inicializa la ventana y ejes de Matplotlib para la animación.
        """
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(7, 7))

    def draw(self, t):
        """
        Dibuja el estado actual de la simulación: posiciones de vehículos,
        circuito circular y título con tiempo.

        Args:
            t (float): Tiempo actual de la simulación.
        """
        R = self.CIRC / (2 * np.pi)
        self.ax.clear()
        self.ax.set_box_aspect(1)
        self.ax.set_xlim(-R * 1.3, R * 1.3)
        self.ax.set_ylim(-R * 1.3, R * 1.3)
        self.ax.axis('off')

        circle = plt.Circle((0, 0), R, color='gray', fill=False,
                            linestyle='--', linewidth=1.5)
        self.ax.add_artist(circle)

        angles = self.s / R
        X = R * np.cos(angles)
        Y = R * np.sin(angles)

        colors = ['blue' if i == 0 else '#d62728' for i in range(self.N)]
        self.ax.scatter(X, Y, s=100, c=colors,
                        edgecolors='black', zorder=10)

        self.ax.set_title(
            f"Simulación de Tráfico\nTiempo: {t:.1f} s",
            fontsize=14
        )
        plt.pause(0.001)

    #  LOOP PRINCIPAL

    def run(self):
        """
        Ejecuta el ciclo principal de la simulación con visualización animada.

        - Inicializa la figura
        - Itera sobre la dinámica
        - Dibuja cada cierto número de pasos
        - Finaliza mostrando la animación detenida
        """
        self.setup_draw()

        t = 0.0
        print("Iniciando simulación...")
        print(f"P0 frena a los {self.FIRST_STOP}s y cada {self.REPEAT_INTERVAL}s.")

        while t < self.SIM_TIME:
            self.run_step(t)

            if int(t / self.DT) % 2 == 0:
                self.draw(t)

            t += self.DT

        plt.ioff()
        plt.show()

#  MAIN
if __name__ == "__main__":
    sim = TrafficSimulation()
    sim.run()