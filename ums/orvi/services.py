from numpy import zeros, sqrt, cos, sin, deg2rad, tan, arctan, pi, arange, fromiter

class OrbitalSolution:
    def __init__(self):
        self.NAME = ''
        self.RA = 0
        self.DEC = 0
        self.P = 0
        self.err_P = 0 
        self.T0 = 0
        self.err_T0 = 0 
        self.a = 0
        self.a_err = 0
        self.e = 0
        self.e_err = 0
        self.w = 0
        self.w_err = 0
        self.W = 0
        self.w_err = 0
        self.i = 0
        self.i_err = 0
    
    def setParametersWithErrors(self, P, P_e, T0, T0_e, a, a_e, e, e_e, W, W_e, w, w_e, i, i_e):
        self.P = P
        self.T0 = T0
        self.a = a
        self.e = e
        self.W = W
        self.W_rad = deg2rad(W)
        self.w = w
        self.w_rad = deg2rad(w)
        self.i = i
        self.i_rad = deg2rad(i)
        self.P_err = P_e
        self.T0_err = T0_e
        self.a_err = a_e
        self.e_err = e_e
        self.W_err = W_e
        self.w_err = w_e
        self.i_err = i_e
    
    def setParameters(self, P, T0, a, e, W, w, i):
        self.P = P
        self.T0 = T0
        self.a = a
        self.e = e
        self.W = W
        self.w = w
        self.i = i

    def setInfo(self, parameter, value):
        if parameter == 'name':
            self.NAME = value
        elif parameter == 'RA':
            self.RA = value
        elif parameter == 'DEC':
            self.DEC = value

class Point:
    def __init__(self, epoch, theta, rho, weight, koeff):
        self.epoch = epoch
        self.theta = theta
        self.rho = rho
        self.weight = weight
        self.koeff = koeff

def ephemeris(orb_sol, epoch_list, rho=False, rv=False):
    output_ephemeris = []
    A = orb_sol.a * (+cos(orb_sol.w_rad) * cos(orb_sol.W_rad) - sin(orb_sol.w_rad) * sin(orb_sol.W_rad) * cos(orb_sol.i_rad))
    B = orb_sol.a * (+cos(orb_sol.w_rad) * sin(orb_sol.W_rad) + sin(orb_sol.w_rad) * cos(orb_sol.W_rad) * cos(orb_sol.i_rad))
    F = orb_sol.a * (-sin(orb_sol.w_rad) * cos(orb_sol.W_rad) - cos(orb_sol.w_rad) * sin(orb_sol.W_rad) * cos(orb_sol.i_rad))
    G = orb_sol.a * (-sin(orb_sol.w_rad) * sin(orb_sol.W_rad) + cos(orb_sol.w_rad) * cos(orb_sol.W_rad) * cos(orb_sol.i_rad))
    for epoch in epoch_list:
        time_delta = epoch - orb_sol.T0
        phase = (time_delta / orb_sol.P) % 1
        if phase < 0:
            phase += 1
        anomaly = phase * 2 * pi
        E = float(anomaly)
        E1 = E + (anomaly + orb_sol.e * sin(E) - E) / (1 - orb_sol.e * cos(E))
        while abs(E1 - E) > 1e-5:
            E = float(E1)
            E1 = E + (anomaly + orb_sol.e * sin(E) - E) / (1 - orb_sol.e * cos(E))
        V = 2 * arctan(sqrt((1 + orb_sol.e) / (1 - orb_sol.e)) * tan(E1 / 2))
        R = (1 - orb_sol.e**2) / (1. + orb_sol.e * cos(V))
        X = R * cos(V)
        Y = R * sin(V)
        output_ephemeris.append((A * X + F * Y, B * X + G * Y))
    return output_ephemeris


def correct(points, T0):
    for number, point in enumerate(points):
        if point.epoch < 3e3 and T0 > 3e3:
            points[number].epoch = 365.242198781 * (point.epoch - 1900.) + 15020.31352
        if point.epoch > 3e3 and T0 < 3e3:
            points[number].epoch = 1900.0 + (point.epoch - 15020.31352) / 365.242198781
    return points

def getPoints(fName, orbital_solution):
    points = []

    with open(fName) as f:
        data = f.read().split('\n')
        bdata = data[13:]

    for line in bdata:
        if not line or line.startswith('#'):
            continue
        splitted_line = line.split()
        if splitted_line[-1].startswith('I1'):
            points.append(Point(*map(float, splitted_line[:-1])))

    points = correct(points.copy(), orbital_solution.T0)
    PR = 0.0057 * sin(deg2rad(orbital_solution.RA)) / cos(deg2rad(orbital_solution.DEC))
    for number, point in enumerate(points):
        points[number].theta += (2000 - point.epoch) * PR
    return points

def findExt(data, t):
    if t=='min':
        if min(data[0]) < min(data[1]):
            return min(data[0])
        else:
            return min(data[1])
    elif t=='max':
        if max(data[0]) > max(data[1]):
            return max(data[0])
        else:
            return max(data[1])

def getOrbit(points, orb_sol):
    num_of_points = 500

    epochs = fromiter((point.epoch for point in points), dtype='float32')
    rhos = fromiter((point.rho for point in points), dtype='float32')
    thetas = fromiter((deg2rad(point.theta) for point in points), dtype='float32')

    mod_epochs = arange(num_of_points) / (num_of_points - 1) * orb_sol.P + orb_sol.T0
    xye = ephemeris(orb_sol, mod_epochs)
    xobs =  -rhos * sin(thetas)
    yobs = rhos * cos(thetas)
    xy0 = ephemeris(orb_sol, epochs)
    return xye, xy0, xobs, yobs

