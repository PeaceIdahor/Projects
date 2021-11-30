% Peace Idahor
% 11/16/20
% Project 2 phase 4
% hitting a baseball, with drag, comparing excel and matlab

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
for n = 1:N   % N intervals
    
    v = sqrt(vy^2 + vx^2); % velocity v in m/s
    Fy = -m*g - Dragc*vy*v; % the net force in the y direction
    Fx = 0-Dragc*v*vx/2; % v0x*vx net force in the x direction
    
    ay = Fy/m; % acceleration in the y direction
    y(n+1) = y(n) +vy*dt +(1/2)*ay*dt^2; % the next y position
    vy = vy + ay*dt; % this updates the vertical velocity
    
    ax = Fx/m;% acceleration in the x direction
    x(n+1) = x(n) + vx*dt + (1/2)*ax*dt^2;
    vx = vx + ax*dt; % updates the horzontal velocity
    if n>1
        ydt = y(n)/(y(n-1) +vy*dt +(1/2)*ay*dt^2)
    end
    
end
row = min(ydt)

% ----- compare analytic to numeric -----

checkSumy = sum(abs(y-yt))  % We don't need to define check = y-yt.
                            % Use ABS to make each element positive
                            % before summing.  If the sum of 2001 
                            % positive numbers is 2.6e-10, then that's 
                            % a convincing check!
checkSumx = sum(abs(x-xt))
%-------------Plotting---------------------
% turning my values from meters to feet

xtft = xt*m2ft;% turning my xt distance to feet
ytft = yt*m2ft;% turning my yt height to feet
xft = x*m2ft; 
yft = y*m2ft;
Export = [t;xft;yft].'; % creating 3 columns of data of time x values and y values
writematrix(Export, 'Peace5.csv', 'delimiter', 'tab') % export the array as a csv files
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