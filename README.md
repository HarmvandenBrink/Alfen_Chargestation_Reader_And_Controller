# Alfen Charge station Reader And Controller
A charge station reader and controller for **Alfen NG9xx** chargers 

This code was used in a home built Home Energy Management System (HEMS), to include an Alfen NG9xx charge station into a smart home. You can read more about it in my blog post: [How I built a HEMS with solar, a battery and a charge station (in Python)](https://medium.com/@harmvandenbrink/how-i-built-a-hems-with-solar-a-battery-and-a-charge-station-in-python-d5b51e60fd1c?source=friends_link&sk=f5e9302a02ea29065c3f677ecf1b8ed8)

# How to use the code
## Import the class and connect to an Alfen Chargestation

```python
from alfenChargestation import alfenCharger
chargestation = alfenCharger('ICU-00001', '192.168.1.X', 0, 20)

```

## Show a single value

```python
chargestation.readMeasurements()
print(chargestation.voltage_l1n)
```

## Control the charge station (single)

```python
# Sets the current to 10 amps
chargestation.changeCurrent(10)
```

## Control a set of chargers in a Smart Charging Network (SCN)

```python
# Set the current of the entire charging plaza to 42 amps
chargestation.changeCurrentSCN(42,42,42)
```

## Change charge using 1 or 3 phases

```python
# Set the number of phases to charge on
# !! Please verify that your car is capable of phase switching during charging !!
changeChargeNumberOfPhases(3)
```

```python
# Set the current of the entire charging plaza to 42 amps
chargestation.changeCurrentSCN(42,42,42)
```

# Disclaimer

The code within this repository comes with no guarantee, the use of this code is your responsibility.

I take NO responsibility and/or liability for how you choose to use any of the source code available here. By using any of the files available in this repository, you understand that you are AGREEING TO USE AT YOUR OWN RISK.
