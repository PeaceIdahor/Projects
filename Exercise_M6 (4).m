% Peace Idahor
% 10/23/20
% Exercise M6 : three	carts	colliding, with user inputs
clear

%----------- Equations for later -------------
global p0
global E0
global m
c = 0;
m = input('Enter mass of cart in the form [m1,m2,m3]: ');% creates an array of mass
v0 = input('Enter velocity of carts in the form [v1,v2,v3]: ');% creates an array of velocities
p0 = sum(m.*v0);
E0 = sum(.5*m.*v0.^2);


%--------------- Creating function ---------------
again = 1;
while again == 1
    if v0(1)<=v0(2) && v0(2)<=v0(3)
        again = 0; % changing the value so that the loop of infinite
        fprintf('No more collisions\n')
        fprintf('Number of collisions = %g\n',c) 
    else
        if v0(1)>v0(2) % if cart 1 and 2 collides
            collision = 12;
    
        end
        if v0(2)>v0(3)% if cart 2 and 3 collide
           
            collision = 23;
        end   
        if v0(1)>v0(2) && v0(2)>v0(3)
            collision = input('which collision is first, 12 or 23: ');
        end
         c = c + 1; % adding 1 collision to my total
         fprintf('Collision number: %g',c)
        v0 = FindV(collision,v0)%initializing my v0
     end
 end

 function v0 = FindV(collision,vi)
 global m
 global E0
 global p0
 cutoff = 1*10^12;
 
 if collision == 12% if the collision is  between cart 1 and 2
    v0(1) = vf(vi(1),m(1),vi(2),m(2));
    v0(2) = vf(vi(2),m(2),vi(1),m(1));
    v0(3) = vi(3);
 end
 if collision == 23% if the collision is between cart 2 and 3
     v0(1) = vi(1);
     v0(2) = vf(vi(2),m(2),vi(3),m(3));
     v0(3) = vf(vi(3),m(3),vi(2),m(2));
 end
 checkEnergy = abs(sum(.5*m.*v0.^2) - E0);
 checkMomentum = abs(sum(m .* v0) - p0);
if checkEnergy > cutoff
    fprintf('there is a problem, checkEnergy = %g',checkEnergy)
end
if checkMomentum > cutoff
   fprint('there is a problem, checkMomentum = %g',checkMomentum)
end
 end
 
 function vout = vf(v1,m1,v2,m2)
  vout = ((m1-m2)*v1 + 2*m2*v2)/(m1+m2);
 end


