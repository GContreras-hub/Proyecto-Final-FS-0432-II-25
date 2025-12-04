import numpy as np
import matplotlib.pyplot as plt
import math

class TrafficSimulation:
    def __init__(self):
        # Parámetros Globales
        self.N = 20
        self.CIRC = 230.0
        self.DT = 0.05
        self.SIM_TIME = 1200.0

        # Parámetros Físicos
        self.L_VEHICLE = 4.0
        self.S0 = 2.0

        # Modelo IDM
        self.V0 = 15.0
        self.A_MAX = 0.8
        self.B_DECEL = 4.0
        self.T_HEADWAY = 1.6

        # Eventos de parada
        self.STOP_DURATION = 6.0 # Duración del frenazo (suficiente para parar la fila)
        self.FIRST_STOP = 2.0
        self.REPEAT_INTERVAL = 15.0

        # Estado inicial
        self.s = np.linspace(0, self.CIRC, self.N, endpoint=False)
        self.v = np.ones(self.N) * self.V0

        # Visualización
        self.fig, self.ax = None, None

    #  FUNCIONES DEL MODELO

    def get_gap(self, i, s_curr):
        """Distancia al vehículo de adelante."""
        leader_idx = (i - 1 + self.N) % self.N
        dist = s_curr[leader_idx] - s_curr[i]
        if dist < 0:
            dist += self.CIRC
        return dist - self.L_VEHICLE

    def idm_accel(self, v_curr, v_leader, gap):
        """Aceleración IDM."""
        delta_v = v_curr - v_leader

        s_star = self.S0 + max(
            0.0,
            v_curr * self.T_HEADWAY + (v_curr * delta_v) / (2 * math.sqrt(self.A_MAX * self.B_DECEL))
        )

        effective_gap = max(0.01, gap)

        accel = self.A_MAX * (1 - (v_curr / self.V0)**4 - (s_star / effective_gap)**2)
        return accel

    def leader_stopped(self, t):
        """Determina si el líder debe detenerse."""
        time_since_start = t - self.FIRST_STOP
        if time_since_start >= 0:
            cycle_pos = time_since_start % self.REPEAT_INTERVAL
            return cycle_pos < self.STOP_DURATION
        return False

    def run_step(self, t):
        s_new = np.copy(self.s)
        v_new = np.copy(self.v)

        accel = np.zeros(self.N)
        p0_is_stopped = self.leader_stopped(t)

        #  Cálculo de aceleraciones
        for i in range(self.N):
            if i == 0:
                # LÍDER
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
                leader_v = self.v[leader_idx]
                accel[i] = self.idm_accel(self.v[i], leader_v, gap)

        #  Integración (Euler)
        for i in range(self.N):
            if i == 0 and p0_is_stopped and v_new[i] == 0:
                continue

            v_new[i] = max(0.0, self.v[i] + accel[i] * self.DT)
            s_new[i] = (self.s[i] + v_new[i] * self.DT) % self.CIRC

            if i != 0:
                gap = self.get_gap(i, self.s)
                if (v_new[i] * self.DT) > (gap - 0.5):
                    v_new[i] = max(0.0, (gap - 0.5) / self.DT)
                    s_new[i] = (self.s[i] + v_new[i] * self.DT) % self.CIRC

        self.s = s_new
        self.v = v_new

    #  VISUALIZACIÓN
    def setup_draw(self):
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(7, 7))

    def draw(self, t):
        R = self.CIRC / (2 * np.pi)
        self.ax.clear()
        self.ax.set_box_aspect(1)
        self.ax.set_xlim(-R * 1.3, R * 1.3)
        self.ax.set_ylim(-R * 1.3, R * 1.3)
        self.ax.axis('off')

        circle = plt.Circle((0, 0), R, color='gray', fill=False, linestyle='--', linewidth=1.5)
        self.ax.add_artist(circle)

        angles = self.s / R
        X = R * np.cos(angles)
        Y = R * np.sin(angles)

        colors = ['blue' if i == 0 else '#d62728' for i in range(self.N)]
        self.ax.scatter(X, Y, s=100, c=colors, edgecolors='black', zorder=10)

        self.ax.set_title(f"Simulación de Tráfico\nTiempo: {t:.1f} s", fontsize=14)
        plt.pause(0.001)

    #  LOOP PRINCIPAL
    def run(self):
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