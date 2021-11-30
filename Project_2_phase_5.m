% Peace Idahor
% 11/27/20
% Project 2 phase 5
% Exploring the effects of drag

clear; clf;

% ----- define given information -----
m = 0.145; % mass of a baseball in kg

x0 = 0; y0 = 0;   % because we don't really care where it starts

v0mph = 112;   % exit velocity in mph, from baseballsavant.mlb.com
phi0deg = 32;   % launch angle in degrees
                  
g = 10;   % gravitational constant in N/kg (1 N/kg = 1 m/s^2), i.e., ay = -g
         
% ----- set up more variables -----

mph2mps = 5280 * 12 * 2.54 / 100 / 3600;   % mph to m/s conversion
deg2rad = pi()/180;   % degrees to radians conversion

v0 = v0mph * mph2mps;   % initial speed in m/s (no units in the variable name)
phi0 = phi0deg * deg2rad;   % initial angle in rad (no units in the variable name)

v0x = v0 * cos(phi0);   % x-component of initial velocity in m/s
v0y = v0 * sin(phi0);   % y-component of initial velocity in m/s


% ----- compute useful characteristics of the trajectory -----

% This will help interpret the output, make sure that it makes sense

tH = v0y/g;  % time to reach max. height, in m
t_land = 2*tH;   % time of flight, in s

H = v0y^2/2*g;   % maximum height, in m
R = v0x * t_land;   % range, in m 
R_ft = R*3.3 ;  % multiplying by 3.3 to estimate range in ft
               
% *** This will be very different from what you are expected to do. ***
tmin = 0; tmax = t_land;   % stop when the ball lands
N = 2000;    % intervals
t = linspace(tmin, tmax, 1+N);
xt = x0 + v0x*t;   % x(t), ax = 0
yt = y0 + v0y*t - (1/2)*g*t.^2;    % y(t), ay = -g
dt = (tmax-tmin)/N;% initializing the change in time
x = zeros(1, 1+N); % initialize x(t)
y = zeros(1, 1+N);   % initialize y(t)
C = input('Put the dimensional constant for baseball: '); % dimensional consttant for baseball
P = 1.225; % Kg/m^3
r = 0.038; % radius of a baseball in m
A = pi()*r^2;
y(1) = y0;% the first value of array is y0
vy = v0y;   % vy(1) = v0y, but we DON'T need an array for vy
x(1) = x0; % first value of array  is x0
vx = v0x;
Dragc = 0.5*C*P*A; % constant terms for drag
m2ft = 3.281;% this is my conversion factor for m -> ft
Ei = m*(vy^2 + vx^2)/2; % the initial energy in the system
mph_ms = 2.237; % conversion factor to go from m/s to mph
for n = 1:N   % N intervals
    v = sqrt(vy^2 + vx^2); % velocity v in m/s
    Fy = -m*g - Dragc*vy*v; % the net force in the y direction
    Fx = 0-Dragc*v*vx; % v0x*vx net force in the x direction
    
    ay = Fy/m; % acceleration in the y direction
    y(n+1) = y(n) +vy*dt +(1/2)*ay*dt^2; % the next y position
    vy = vy + ay*dt; % this updates the vertical velocity
    
    ax = Fx/m;% acceleration in the x direction
    x(n+1) = x(n) + vx*dt + (1/2)*ax*dt^2;
    vx = vx + ax*dt; % updates the horzontal velocity
    if y(n+1)/y(n) <0
        Range = x(n)*m2ft % Range in feet
        Time_F = t(n) % time to hit ground in s
        VF = v; % final velocity in m/s
        EF = m*VF^2/2; % Final energy in the system in Joules
        E_Lost = abs(EF - Ei)% Energy Lost in Joules
    end
end
VF_mph = VF*mph_ms  % velocity of ball before it hits the ground in mph  
MaxHeight = max(y)*m2ft % max height of the baseball in feet
VE = 446; % this is the expected value of the range in ft
PE = abs(100*(Range - VE)/VE) % this is the percent error of my expected value and my actual value
%----------------------Part c--------------
DiagramH = 114; % max height of the baseball in the diagram in ft
DiagramT = 5.7; % time of flight of the baseball in the diagram in s
PE_H = abs(100*(MaxHeight - DiagramH)/DiagramH) % percent error of the max height in the diagram vs my value
PE_T = abs(100*(Time_F - DiagramT)/DiagramT) % percent error of the time of flight between the diagram and my value
% Except for the range the baseball goes to, there is a large difference
% between the values from the diagram and the values I got. I got smaller
% values for the max height of the baseball and the time of flight for the
% baseball.
% ----- compare analytic to numeric -----

checkSumy = sum(abs(y-yt));  % We don't need to define check = y-yt.
                            % Use ABS to make each element positive
                            % before summing.  If the sum of 2001 
                            % positive numbers is 2.6e-10, then that's 
                            % a convincing check!
checkSumx = sum(abs(x-xt));
%-------------Plotting---------------------
% turning my values from meters to feet
xtft = xt*m2ft;% turning my xt distance to feet
ytft = yt*m2ft;% turning my yt height to feet
xft = x*m2ft; 
yft = y*m2ft;

p1 = plot(xtft,ytft,xft,yft,'Linewidth',2);
grid on
ax = gca;
ax.GridAlpha = 1;
grid minor
ax.MinorGridAlpha = 0.5;
ax.FontSize =18;
ylim([0 120]);
xlabel('Distance (ft)','FontSize',18)
ylabel('Height (ft)','FontSize',18)
title('Project 2 Phase 3: Trajectory of a baseball,  drag vs no drag ','FontSize',20)
legend('No Drag',sprintf('Drag C =%g ',C),'FontSize',18)