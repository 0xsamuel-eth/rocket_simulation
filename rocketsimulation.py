# Using RocketPy Library

from rocketpy import Environment, Rocket, LiquidMotor, Flight
from math import exp
from rocketpy import Fluid, LiquidMotor, CylindricalTank, MassFlowRateBasedTank

import datetime

#Create an environment object
env = Environment(
    latitude=32.990254,
    longitude=-106.974998,
    elevation=1400,
)

tomorrow = datetime.date.today() + datetime.timedelta(days=1)

env.set_date(
  (tomorrow.year, tomorrow.month, tomorrow.day, 12), timezone="America/Denver"
) # Tomorrow's date in year, month, day, hour UTC format

env.set_atmospheric_model(type='Forecast', file='GFS')

example_liquid = LiquidMotor(
    thrust_source=lambda t: 4000 - 100 * t**2,
    dry_mass=2,
    dry_inertia=(0.125, 0.125, 0.002),
    nozzle_radius=0.075,
    center_of_dry_mass_position=1.75,
    nozzle_position=0,
    burn_time=5,
    coordinate_system_orientation="nozzle_to_combustion_chamber",
)
# example_liquid.add_tank(tank=oxidizer_tank, position=1.0)
# example_liquid.add_tank(tank=fuel_tank, position=2.5)

#Create a rocket object
calisto = Rocket(
    radius=0.0635,
    mass=14.426,  # without motor
    inertia=(6.321, 6.321, 0.034),
    power_off_drag=.02,
    power_on_drag=.03,
    center_of_mass_without_motor=0,
    coordinate_system_orientation="tail_to_nose",
)

buttons = calisto.set_rail_buttons(
    upper_button_position=0.0818,
    lower_button_position=-0.6182,
    angular_position=45,
)

calisto.add_motor(example_liquid, position=-1.255)

nose = calisto.add_nose(
    length=0.55829, kind="vonKarman", position=1.278
)

fins = calisto.add_trapezoidal_fins(
    n=4,
    root_chord=0.120,
    tip_chord=0.040,
    span=0.100,
    sweep_length=None,
    cant_angle=0,
    position=-1.04956,
)

tail = calisto.add_tail(
    top_radius=0.0635, bottom_radius=0.0435, length=0.060, position=-1.194656
)

#Add parachute to rocket object
main = calisto.add_parachute(
    name="main",
    cd_s=10.0,
    trigger=800,  # ejection altitude in meters
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)

drogue = calisto.add_parachute(
    name="drogue",
    cd_s=1.0,
    trigger="apogee",  # ejection at apogee
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)

#Create flight object
test_flight = Flight(
  rocket=calisto, environment=env, rail_length=5.2, inclination=85, heading=0
)

#Get summary of results
test_flight.info()

#Get summary of all available results
test_flight.all_info()

#Export KML file to view on Google Earth
test_flight.export_kml(file_name="test_flight.kml")
