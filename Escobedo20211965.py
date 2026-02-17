"""
Práctica 0: Mecánica pulmonar

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Nombres y Apellidos
Número de control: 12345678
Correo institucional: xxx.xxx@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math as m
import control as ctrl
import matplotlib.pyplot as plt  

# Datos de la simulación
x0,t0,tend,dt,w,h=0,0,10,1E-3,7,3.5
N =round (tend/dt) + 1
t= np.linspace(t0,tend,N)
u1 = np.ones(N)#step
u2 = np.zeros(N);u2[round(1/dt):round(2/dt)]=1 #impulse
u3 = t/tend 
u4 = np.sin(m.pi/2*t)


# Componentes del circuito RLC y función de transferencia
R,L,C,= 10e3, 330E-6, 470E-6
num =[1]
den =[C*L,C*R,1]
sys = ctrl.tf(num,den)
print(f"funcion de transferencia del sistema: {sys}")
# Componentes del controlador
kP,kI,kD = 6883.75,1867081.418,0.85158
Cr = 1E-6
Re= 1/(Cr*kI)
Rr= kP*Re
Ce=kD/Rr
print(f"El valor de la capacitancia Cr es de  {Cr} Faradios.\n")
print(f"El valor de la resistencia de {Re} Ohms.\n ")
print(f"El valor de la resistencia de {Rr}Ohms.\n")
print(f"El valor de la capacitancia Ce es de  {Ce} Faradios.\n")

numPID = [Re*Rr*Ce*Cr,Re*Ce+Rr*Cr,1]
denPID =[Re*Cr,0]
PID = ctrl.tf(numPID,denPID)
print(f"Funcion de transferencia del controlados PID: {PID}.\n")

# Sistema de control en lazo cerrado

x= ctrl.series(PID, sys)
sysPID = ctrl.feedback (x,1,sign=-1)
print(f"Funcion de trransferencia del sistema de control en lazo cerrado: {sysPID}.\n")




# Respuesta del sistema en lazo abierto y en lazo cerrado

_,PAu1 = ctrl.forced_response(sys,t,u1,x0)
_,PAu2 = ctrl.forced_response(sys,t,u2,x0)
_,PAu3 = ctrl.forced_response(sys,t,u3,x0)
_,PAu4 = ctrl.forced_response(sys,t,u4,x0)

_,PIDu1 = ctrl.forced_response(sysPID,t,u1,x0)
_,PIDu2 = ctrl.forced_response(sysPID,t,u2,x0)
_,PIDu3 = ctrl.forced_response(sysPID,t,u3,x0)
_,PIDu4 = ctrl.forced_response(sysPID,t,u4,x0)

clr0 = np.array([168, 223, 142])/255
clr1 =np.array([168, 223, 142])/255
clr2 =np.array([240, 255, 223])/255
clr3 =np.array([255, 216, 223])/255
clr4 =np.array([255, 170, 184])/255
clr5 =np.array([250, 92, 92])/255


fg1= plt.figure()#respuesta escalon
plt.plot(t,u1,'-', color = clr1, label='Pao(t)')#escalo
plt.plot(t,PAu1,'--', color = clr4, label='PA(t)')#respuesta en lazo abierto
plt.plot(t,PIDu1,':', color = clr5, label='PID(t)')#respuesta en lazo CERRADO
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(0,1.1);plt.yticks(np.arange(0,1.2,0.1))
plt.xlabel('t[s]', fontsize=11)
plt.ylabel('vi(t)[v]',fontsize=11)
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center',ncol=3, 
            fontsize=9, frameon= True)
plt.show()
fg1.savefig('step_python.pdf', bbox_inches= 'tight')





fg2= plt.figure()#respuesta impulso
plt.plot(t,u2,'-', color = clr1, label='Pao(t)')#escalo
plt.plot(t,PAu2,'--', color = clr4, label='PA(t)')#respuesta en lazo abierto
plt.plot(t,PIDu2,':', color = clr5, label='PID(t)')#respuesta en lazo CERRADO
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(0,1.1);plt.yticks(np.arange(0,1.2,0.1))
plt.xlabel('t[s]', fontsize=11)
plt.ylabel('vi(t)[v]',fontsize=11)
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center',ncol=3, 
            fontsize=9, frameon= True)
plt.show()
fg2.savefig('impul_python.pdf', bbox_inches= 'tight')




fg3= plt.figure()#respuesta rampa
plt.plot(t,u3,'-', color = clr1,label='Pao(t)')#escalo
plt.plot(t,PAu3,'--', color = clr4,label='PA(t)')#respuesta en lazo abierto
plt.plot(t,PIDu3,':', color = clr5,label='PID(t)')#respuesta en lazo CERRADO
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(0,1.1);plt.yticks(np.arange(0,1.2,0.1))
plt.xlabel('t[s]', fontsize=11)
plt.ylabel('vi(t)[v]',fontsize=11)
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center',ncol=3, 
            fontsize=9, frameon= True)
plt.show()
fg3.savefig('ram_python.pdf', bbox_inches= 'tight')




fg4= plt.figure()#respuesta sinusoidal
plt.plot(t,u4,'-', color = clr1,label='Pao(t)')#escalo
plt.plot(t,PAu4,'--', color = clr4,label='PA(t)')#respuesta en lazo abierto
plt.plot(t,PIDu4,':', color = clr5,label='PID(t)')#respuesta en lazo CERRADO

plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(1,0,-1);plt.yticks(np.arange(0,1.2,0.1))
plt.xlabel('t[s]', fontsize=11)
plt.ylabel('vi(t)[v]', fontsize=11)
plt.legend(bbox_to_anchor=(1.5,-1.5),loc='center',ncol=3, 
            fontsize=9, frameon= True)

plt.show()
fg4.savefig('sin_python.pdf', bbox_inches= 'tight')

