# -*- coding: utf-8 -*-
"""MEE.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1aOhDr6gFMi9Z28dblouXkFVlGY64kOPx
"""

# import necessary modules
import numpy as np
from iapws import IAPWS97
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Ask for feed and product condition
F = float(input("Enter feed flow (kg/h): "))
xf = float(input("Enter feed concentration (mass fraction): "))
xp = float(input("Enter product concentration (mass fraction): "))
Tf = float(input("Enter feed temperature (deg Celsius): "))

# Ask for concentrations leaving each effect
concentrations = np.array([float(input(f"Enter concentration leaving effect {i+1} (mass fraction): ")) for i in range(5)])

# Ask for pressures of each effect in Mpa
P_effect = np.array([float(input(f"Enter pressure of effect {i+1} (Mpa): ")) for i in range(6)])
T = np.array([IAPWS97(P=p, x=0).T - 273.15 for p in P_effect])  # deg celcius

# calculate enthalpy of saturated vapor and saturated liquid for each effect
Hv = np.array([IAPWS97(P=p, x=1).h for p in P_effect]) # kJ/kg
Hl = np.array([IAPWS97(P=p, x=0).h for p in P_effect]) # kJ/kg

# calculate latent heat of vaporization of steam (Hv - Hl) for each effect
lamda = Hv - Hl # kJ/kg

# calculate the enthalpy of the feed liquid at the feed temperature
Hf = IAPWS97(T=Tf+273.15, x=0).h # kJ/kg

# calculate specific evaporation coefficient for each effect
e = np.array([0.0008 * (100 - x*100) * (t - 54) for x, t in zip(concentrations, T)])

# calculate the temperature difference between each effect
deltaT = np.diff(-T)

# Initialize arrays to store the values of Product flow, Vapor flow, Steam Required,
# Heating Surface Area and Overall Heat Transfer Coefficient for each effect
P = np.zeros(len(concentrations))
V = np.zeros(len(concentrations))
S = np.zeros(len(concentrations))
A = np.zeros(len(concentrations))
U = np.zeros(len(concentrations))
Q = np.zeros(len(concentrations))
Se = np.zeros(len(concentrations))

# Loop over each effect
for i in range(len(concentrations)):
    # Calculate the product flow for the current effect
    P[i] = F * xf / concentrations[i]
    # Calculate the vapor flow for the current effect
    V[i] = F - P[i]
    S[i] = (V[i]*Hv[i] + P[i]*Hl[i] - F*Hf) / lamda[i]
    # Calculate the heating surface area for the current effect
    A[i] = V[i] / (e[i] * deltaT[i])
    # Calculate the overall heat transfer coefficient for the current effect
    U[i] = ((S[i] * lamda[i] / (A[i] * deltaT[i]))/3600)
    # Calculate the heat duty for the current effect
    Q[i] = ((U[i] * A[i] * deltaT[i])/1000)
    # Calculate the Steam Economy for the current effect
    Se[i] = (V[i]/S[i])
    # Update the feed flow for the next effect
    F = P[i]
    xf = concentrations[i]
    Hf = Hl[i]

# Print the product and vapor flows, steam required, heating surface area and
# overall heat transfer coefficient for each effect
for i in range(len(P)):
    print(f"Effect {i+1}:\n Product flow = {P[i]} kg/h\n Vapor flow = {V[i]} kg/h\n  Steam required = {S[i]} kg/h\n  Heating surface area = {A[i]} m^2\n  Overall heat transfer coefficient = {U[i]} kW/m^2K\n Heat duty = {Q[i]} MW\n Steam economy = {Se[i]}")


# Define the effects
effects = np.arange(1, len(concentrations) + 1)

# Plot the product and vapor flows for each effect
plt.figure(figsize=(10, 6))
plt.plot(effects, P, label='Product flow (kg/h)')
plt.plot(effects, V, label='Vapor flow (kg/h)')
plt.xlabel('No. of Effect')
plt.ylabel('Flow (kg/h)')
plt.title('Product and Vapor Flows for Each Effect')
plt.legend()
plt.grid(True)
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
plt.show()

# Plot the steam required for each effect
plt.figure(figsize=(10, 6))
plt.plot(effects, S, label='Steam required (kg/h)')
plt.xlabel('No. of Effect')
plt.ylabel('Steam required (kg/h)')
plt.title('Steam Required for Each Effect')
plt.legend()
plt.grid(True)
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
plt.show()

# Plot the heating surface area for each effect
plt.figure(figsize=(10, 6))
plt.plot(effects, A, label='Heating surface area (m^2)')
plt.xlabel('No. of Effect')
plt.ylabel('Heating surface area (m^2)')
plt.title('Heating Surface Area for Each Effect')
plt.legend()
plt.grid(True)
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
plt.show()

# Plot the overall heat transfer coefficient for each effect
plt.figure(figsize=(10, 6))
plt.plot(effects, U, label='Overall heat transfer coefficient (kW/m^2K)')
plt.xlabel('No. of Effect')
plt.ylabel('Overall heat transfer coefficient (kW/m^2K)')
plt.title('Overall Heat Transfer Coefficient for Each Effect')
plt.legend()
plt.grid(True)
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
plt.show()

# Plot the heat duty for each effect
plt.figure(figsize=(10, 6))
plt.plot(effects, Q, label='Heat duty (MW)')
plt.xlabel('No. of Effect')
plt.ylabel('Heat duty (MW)')
plt.title('Heat Duty for Each Effect')
plt.legend()
plt.grid(True)
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
plt.show()

# Plot the heat duty for each effect
plt.figure(figsize=(10, 6))
plt.plot(effects, Se, label='Steam Economy')
plt.xlabel('No. of Effect')
plt.ylabel('Steam Economy')
plt.title('Steam Economy for Each Effect')
plt.legend()
plt.grid(True)
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
plt.show()