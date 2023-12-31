from rocketpy import Environment, SolidMotor, Rocket, Flight, Function
from datetime import datetime
from time import process_time, perf_counter, time
import glob

import numpy as np
from numpy.random import normal, uniform, choice
from IPython.display import display


# ------------------------------------------------------------------------ Environment Setting
Env = Environment(
    # railLength=5.2,
    latitude=32.990254,
    longitude=-106.974998,
    elevation=1400
)

# import datetime

# tomorrow = datetime.date.today() + datetime.timedelta(days=1)

# Env.setDate((tomorrow.year, tomorrow.month, tomorrow.day, 12)) # Hour given in UTC time

# Env.setAtmosphericModel(type='Forecast', file='GFS')
# Env.setAtmosphericModel(type='StandardAtmosphere')

# Env.info()


URL = 'https://rucsoundings.noaa.gov/get_raobs.cgi?data_source=RAOB&latest=latest&start_year=2019&start_month_name=Feb&start_mday=5&start_hour=12&start_min=0&n_hrs=1.0&fcst_len=shortest&airport=83779&text=Ascii%20text%20%28GSD%20format%29&hydrometeors=false&start=latest'

Env.set_atmospheric_model(type='NOAARucSounding', file=URL)

# --------------------------------------------------------------------------Motor Setting
Pro75M1670 = SolidMotor(
    thrust_source="Cesaroni_M1670.eng",
    # burnOut=3.9,
    dry_mass=1.815,
    dry_inertia=(0.125, 0.125, 0.002),
    nozzle_radius=33 / 1000,
    grain_number=5,
    grain_density=1815,
    grain_outer_radius=33 / 1000,
    grain_initial_inner_radius=15 / 1000,
    grain_initial_height=120 / 1000,
    grain_separation=5 / 1000,
    grains_center_of_mass_position=0.397,
    center_of_dry_mass_position=0.317,
    nozzle_position=0,
    burn_time=3.9,
    throat_radius=11 / 1000,
    coordinate_system_orientation="nozzle_to_combustion_chamber",
)

# Pro75M1670.info()

# ------------------------------------------------------------------------Initializing Rocket
calisto = Rocket(
    radius=127 / 2000,
    mass=14.426,
    inertia=(6.321, 6.321, 0.034),
    power_off_drag="../data/calisto/powerOffDragCurve.csv",
    power_on_drag="../data/calisto/powerOnDragCurve.csv",
    center_of_mass_without_motor=0,
    coordinate_system_orientation="tail_to_nose",
)

Calisto.setRailButtons([0.2, -0.5])
# help(Function)


# -----------------------------------------------------------------------Aerodynamic Surfaces
NoseCone = Calisto.addNose(length=0.55829, kind="vonKarman", distanceToCM=0.71971)

FinSet = Calisto.addFins(4, span=0.100, rootChord=0.120, tipChord=0.040, distanceToCM=-1.04956)

Tail = Calisto.addTail(topRadius=0.0635, bottomRadius=0.0435, length=0.060, distanceToCM=-1.194656)


# -----------------------------------------------------------------------Parachute Parameters 
def drogueTrigger(p, y):
    # p = pressure
    # y = [x, y, z, vx, vy, vz, e0, e1, e2, e3, w1, w2, w3]
    # activate drogue when vz < 0 m/s.
    return True if y[5] < 0 else False

def mainTrigger(p, y):
    # p = pressure
    # y = [x, y, z, vx, vy, vz, e0, e1, e2, e3, w1, w2, w3]
    # activate main when vz < 0 m/s and z < 800 m.  
    return True if y[5] < 0 and y[2] < 800 else False

Main = Calisto.addParachute('Main',
                            CdS=10.0,
                            trigger=mainTrigger,
                            samplingRate=105,
                            lag=1.5,
                            noise=(0, 8.3, 0.5))

Drogue = Calisto.addParachute('Drogue',
                              CdS=1.0,
                              trigger=drogueTrigger,
                              samplingRate=105,
                              lag=1.5,
                              noise=(0, 8.3, 0.5))

Calisto.parachutes.remove(Drogue)
Calisto.parachutes.remove(Main)


# ----------------------------------------------------------------------Flight Test
TestFlight = Flight(rocket=Calisto, environment=Env, inclination=85, heading=0)
TestFlight.allInfo()

# --------------------------------------------------------------------Test Monte Carlo