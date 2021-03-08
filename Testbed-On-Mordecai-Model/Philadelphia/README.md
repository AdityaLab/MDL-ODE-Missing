This is the testbed code on Mordecai's Model

alpha.py: Step 1: Sweep the alpha to find the alpha*.
D.py: Step 2: Start from the D_reported/alpha* to find the D* that minimizes the MDL(D,p).
average.py: For each alpha, calibrate 20 times and save the corresponding p' and D(p').
