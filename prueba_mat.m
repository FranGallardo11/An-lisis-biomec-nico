% clear all; close all;
% 
% syms L1; syms L2; syms L3;
% syms Teta1; syms Teta2; syms Teta3;

% x = L1*cos(Teta1) + L2*cos(Teta1 + Teta2) + L3*cos(Teta1 + Teta2 + Teta3);
% disp(x);
% y = L1*sin(Teta1) + L2*sin(Teta1 + Teta2) + L3*sin(Teta1 + Teta2 + Teta3);
% disp(y);

clc;
clear;
syms a b c theta alpha phi

% --- Matrices de traslación ---
Transx = [1 0 0 a;
           0 1 0 0;
           0 0 1 0;
           0 0 0 1];

Transy = [1 0 0 0;
           0 1 0 b;
           0 0 1 0;
           0 0 0 1];

Transz = [1 0 0 0;
           0 1 0 0;
           0 0 1 c;
           0 0 0 1];

% --- Matrices de rotación ---
Rotx = [1 0 0 0;
        0 cos(alpha) -sin(alpha) 0;
        0 sin(alpha)  cos(alpha) 0;
        0 0 0 1];

Roty = [cos(phi) 0 sin(phi) 0;
        0 1 0 0;
       -sin(phi) 0 cos(phi) 0;
        0 0 0 1];

Rotz = [cos(theta) -sin(theta) 0 0;
        sin(theta)  cos(theta) 0 0;
        0 0 1 0;
        0 0 0 1];

% --- Matriz de transformación total ---
T = Rotz * Transz * Transx * Rotx;

disp('Matriz de transformación total: ')
pretty(T)
