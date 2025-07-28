import numpy as np
import math
import pandas as pd
from scipy.stats import norm


df = pd.read_csv('eurusd_1M_sabr_parameters.txt')

dates = df["date"].values

k_atm = df["k_atm"].values

alpha = df["alpha"].values

beta = df["beta"].values

nu = df["nu"].values

rho = df["rho"].values

tau = df["tau"].values

forward = df["forward"].values

def z(i):
    return (nu[i] * math.pow(forward[i] * k_atm[i], (1 - beta[i]) / 2)) / alpha[i] * math.log10(forward[i]/k_atm[i])

def chi(i, z):
    return math.log10((math.sqrt(1 - (2 * rho[i] * z) + z**2) + z - rho[i]) / 1- rho[i])

def sigmax(i,z,chi):
    T = 30/360
    first = alpha[i] / (math.pow(forward[i] * k_atm[i], (1 - beta[i]) / 2) * (1 + (((1 - beta[i])**2) / 24) * (math.log10(forward[i]/k_atm[i]) ** 2) + (((1 - beta[i])**4) / 1920) * (math.log10(forward[i]/k_atm[i])**4)))
    second = z / chi
    third = 1 + (((((1 - beta[i])**2) / 24) * (alpha ** 2) / math.pow(forward[i] * k_atm[i],1-beta[i])) + (rho[i] * beta[i] * nu[i] * alpha[i]) / (math.pow(forward[i] * k_atm[i], (1-beta[i]) / 2)) + ((2 - 3 * (rho[i]**2)) * (nu[i]**2) / 24)) * T
    return first * second * third




def d1(i, sigma):
    return (math.log(forward[i] / k_atm[i]) + (sigma ** 2)/ (2 * (30/360))) / (sigma * 30 / 360)
def d2(sigma,d1):
    return d1 - (sigma * math.sqrt(30/360))


def c(r,i, d1, d2):
    return math.exp(-r * 30/360) * (forward[i] * norm.cdf(d1) - k_atm[i] * norm.cdf(d2))

def p(r, i, d1, d2):
    return math.exp(-r * 30/360) * (k_atm[i] * norm.cdf(-d2) - forward[i] * norm.cdf(d1))


# Since r isn't given, I left it as a parameter
def output(r):
    length = len(dates)
    out = np.zeros((5,length))
    for i in range(length):
        z = z(i)
        chi = chi(i,z)
        sigma = sigmax(i)
        d1 = d1(i, sigma)
        d2 = d2(sigma, d1)
        c = c(r, i, d1, d2)
        p = p(r, i, d1, d2)
        out[i][0] = dates[i], out[i][1] = k_atm[i], out[i][2] = sigma, out[i][3] = c, out[i][4] = p
        
    return out

np.savetxt('output.csv',output(r),delimiter=',')