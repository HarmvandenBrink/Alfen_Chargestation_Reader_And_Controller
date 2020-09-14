# Alfen Charge station Reader And Controller
A charge station reader and controller for Alfen NG9xx chargers

This code was used in a home built Home Energy Management System (HEMS), to include an Alfen NG9xx charge station into a smart home. You can read more about it in my blog post: [How I built a HEMS with solar, a battery and a charge station (in Python)](https://medium.com/@harmvandenbrink/how-i-built-a-hems-with-solar-a-battery-and-a-charge-station-in-python-d5b51e60fd1c?source=friends_link&sk=f5e9302a02ea29065c3f677ecf1b8ed8)

# How to use the code
## Show all values of the charge station

```python
print("-" * 60)
print("All registers")
print("-" * 60)
for name, value in iteritems(z):
	print("%s" % name, value if isinstance(value, int) else value)
```

## Show a single value

```python
print(z['actualappliedmaxcurrent'])
```

## Control the charge station

```python
# Sets the current to 15 amps
changeChargeStationCurrent(15)
```

# Disclaimer

The code within this repository comes with no guarantee, the use of this code is your responsibility.

I take NO responsibility and/or liability for how you choose to use any of the source code available here. By using any of the files available in this repository, you understand that you are AGREEING TO USE AT YOUR OWN RISK.
