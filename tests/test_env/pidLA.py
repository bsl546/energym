# PID Class
# Authors:  v.1: Altug Bitlislioglu - Jan2015
#         v.1.1: Altug Bitlislioglu - Feb2015
#         v.1.2: Tomasz Gorecki - Aug 2019
#
#
import numpy as np
import time
import matplotlib.pyplot as plot
# remove matplotlib later for deployment

class pidLA:	
	    	
    #       / --Kd-------[Ns/(s+N)]----\	
    # e --- ---Kp---------------------[+]--- u --[sat]-- u_sat	
    #       \ --Ki---[+]--[1/s]---------/     |            |	
    #                 |                        ----[-,+]---	
    #                  \-----------------------------/	
    #	
    # s = (Ts/2)*(1 - z^-1) / (1 + z^-1)	
        
    # to do: validate backtracking (similar output as simulink block but not exactly same)	
        
    def __init__(self,Kp,Ki,Kd):	
            
        # check if int or float	
        self.u = 0.0	
        self.e = 0.0	
        self.e_sat = 0.0	
        self.Ki = Ki	
        self.Kd = Kd	
        self.Kp = Kp	
        self.u_max = 0.0	
        self.u_min = 0.0	
        self.can_saturate = False	
        self.is_saturated = False	
        self.is_awindup = False	
        self.K_backtr = 0.0	
        self.awindup_method = 'clamp'	
        self.r = None	
        self.offset = 0.0	
            
        self.P = 0.0	
        self.I = 0.0	
        self.D = 0.0	
        self.Kdfilt = 10	
        self.Ts = 0.0	
        self.dynamic_sampling = True	
        self.t = time.time()	
        self.t_y = 0	
        self.t = time.time()	
        
    def calculate_u(self, y, r=None, t_y=None):	
        # y - measurement, r-reference, t_y measurement timestamp	
            
        # Input management	
        if r is None:	
            if self.r is None:	
                raise ValueError('No reference has been specified yet. Specify reference or give value for parameter r')	
            else:	
                r = self.r	
        if t_y is None and self.dynamic_sampling:	
            raise ValueError('The PID uses a dynamic sampling time, t_y needs to be specified')	
    
        # sampling time	
        if self.dynamic_sampling:	
            if self.t_y == 0:	
                self.t_y = t_y	
                return 0	
            else:	
                # needs to be checked for initial step	
                t_prev = self.t_y	
                self.t_y = t_y	
                #print('internal time', t)	
                dt = self.t_y - t_prev	
        #print('time step', dt)	
        else:	
            dt = self.Ts	
            
        # print("dt is : %.2f" % dt)	
            
        I_prev = self.I	
        D_prev = self.D	
        e_prev = self.e	
            
        # error	
        self.e = r-y	
            
        # proportional channel	
        self.P = self.Kp * self.e	
            
        # integral channel	
            
        self.I = dt * self.Ki * (self.e + e_prev)/2 + I_prev;  # trapezoidal	
        #print "self.I set to %.1f" % self.I	
        # derivative channel	
        if self.Kd != 0:	
            self.D = (self.Kdfilt * self.Kd*(self.e-e_prev) - (self.Kdfilt*dt/2 - 1)*D_prev) / (self.Kdfilt*dt / 2 + 1)	
        # y(n) = (N*(u(n)-u(n-1))-(N*Ts/2-1)*(y(n-1)))/(N*Ts/2+1);	
            
        # total control signal	
        u = self.offset + self.P + self.I + self.D	
            
            
        # saturation	
        if self.can_saturate:	
            u_sat = self.saturate(u)	
            self.e_sat_prev = self.e_sat	
            self.e_sat = u_sat - u	
                
            if self.is_saturated:	
            # anti wind-up	
                if self.Ki != 0:	
                    if self.awindup_method == 'clamp':	
                        # cancel integration	
                        if self.e*self.e_sat < 0:  # if the error and the saturation has the same direction	
                            #Stop the integrator
                            self.I = I_prev
                            #cap integrator
                            # if self.I >= self.u_max - self.offset:	
                            #     #print("winding back from %.1f to %.1f" % (self.I,self.u_max))	
                            #     self.I = self.u_max - self.offset	
                            # elif self.I <= self.u_min - self.offset:	
                            #     #print("winding back from %.1f to %.1f" % (self.I,self.u_min))	
                            #     self.I = self.u_min - self.offset	
                            # else:	
                            #     #print("winding back from %.1f to %.1f" % (self.I,I_prev))	
                            #     self.I = I_prev	
                        elif self.awindup_method == 'backtrack':	
                            if self.offset != 0.0:	
                                raise NotImplementedError('need to update to consider non zero offset')	
                            self.I = dt*self.K_backtr*(self.e_sat+self.e_sat_prev)/2 + dt*self.Ki*(self.e + e_prev)/2 + I_prev	
    
            self.u = u_sat	
        else:	
            self.u = u	
    
    def get_u(self):	
        return self.u	
        
    def set_reference(self, r):	
        self.r = r	
        
    def set_offset(self, offset):	
        self.offset = offset	
    
    def set_Kdfilt(self, K):	
        # sets derivative filter coefficient (N in simulink)	
        self.Kdfilt = K	
        
    def set_Ts(self, dt):	
        # sets static sampling time	
        self.Ts = dt	
        self.dynamic_sampling = False	
        
    def set_saturation(self, u_min, u_max):	
        self.u_min = u_min	
        self.u_max = u_max	
        self.can_saturate = True	
        
    def saturate(self,u):	
            
        if u > self.u_max:	
            u = self.u_max	
            self.is_saturated = True	
        elif u < self.u_min:	
            u = self.u_min	
            self.is_saturated = True	
        else:	
            self.is_saturated = False	
        return u	
        
    def set_awindup(self, awindup_method):	
            
        if awindup_method == 'clamp':	
            self.awindup_method = 'clamp'	
        elif awindup_method == 'backtrack':	
            self.awindup_method = 'backtrack'	
            self.K_backtr = self.Ki	
        else:	
            print('unrecognized anti windup method. default is clamping')	
        
        
    def set_backtrack_gain(self, K_bt):	
            
        if K_bt >= 0:  # check if positive	
            self.K_backtr=K_bt	
        else:	
            print('Backtracking gain should be positive')	


class doublePid():

    def __init__(self, pid1, pid2):
        self.pid1 = pid1
        self.pid2 = pid2

    def get_u(self):
        u1 = self.pid1.get_u()
        u2 = self.pid2.get_u()
        return u1, u2
    
    def calculate_u(self, y1, y2):
        self.pid1.calculate_u(y1)
        self.pid2.calculate_u(y2)

    
if __name__ == '__main__':	
        
        
    dt=0.1	
    pid=pidLA(1,1.0,0.0)	
    pid.set_saturation(-0.2,0.2)	
    pid.set_awindup('backtrack')	
    pid.set_awindup('clamp')	
    #pid.set_Ts(0.1)         # set static sampling time	
    #pid.set_backtrack_gain(0)	
    #pid.set_Kdfilt(2)	
    pid	
    u = 0.0	
    #a=1.01	
    a = 1.01	
    x = 0.0	
    t = 0.0	
    X = []	
    X.append(x)	
    U = []	
    U.append(u)	
    T = []	
    T.append(t)	
    r = 1	
    i = 0	
    time.sleep(1)	
    U_I = []	
    U_I.append(0)	
    U_P = []	
    U_P.append(0)	
    U_D = []	
    U_D.append(0)	
        
    while i < 150:	
        #t=time.clock()	
        #print('real time', t)	
        i=i+1	
        t=t+dt	
        
        x=a*x+0.2*u	
        u=pid.get_u(x,r,t)	
        print(t)	
        print(u)	
        #x = -np.sin(1*np.pi*t)	
            
        U_P.append(pid.P)	
        U_I.append(pid.I)	
        U_D.append(pid.D)	
        X.append(x)	
        U.append(u)	
        T.append(t)	
    #print('input', u)	
    #print('output', x)	
    #time.sleep(0.1)	
    #	
        
    fig = plot.figure()	
        
    ax1 = fig.add_subplot(211)	
        
    #ax1.set_title("Plot title...")	
    ax1.set_xlabel('Time')	
    ax1.set_ylabel('Temperature')	
        
    ax1.plot(T,X, c='r', label='')	
        
    ax2 = fig.add_subplot(212)	
        
    #ax2.set_title("Plot title...")	
    ax2.set_xlabel('Time')	
    ax2.set_ylabel('PWM duty')	
        
    ax2.plot(T,U, c='g', label='u')	
    ax2.plot(T,U_P, c='b', label='u_P')	
    ax2.plot(T,U_I, c='c', label='u_I')	
    ax2.plot(T,U_D, c='m', label='u_D')	
    ax2.plot(T,[sum(x) for x in zip(U_I, U_P,U_D)], c='r', label='u_tot')	
        
    ax2.legend(loc=1)	
        
        
    plot.show()