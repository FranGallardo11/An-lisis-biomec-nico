clc;clear;

x=[5 1.4 6 3 5 7
    9 2 30 7 5 9
    8 1.8 11 5 7 5
    12 2.5 18 7 5 5];
lamda = [1,1,1,1,1,1];% --- Modificación de derechos humanos, 1 significa que el peso del índice calculado no se modifica
[m,n]=size(x);
for i=1:n
         x (:, i) = (x (:, i) -min(x (:, i))) / (max(x (:, i)) - min(x (:, i))) + 1; % Procesamiento no negativo y normalizado de los datos originales, el valor está entre 1-2
end
for i=1:m
    for j=1:n
        p(i,j)=x(i,j)/sum(x(:,j));
    end 
end
k=1/log(m);
for i=1:m
    for j=1:n
        if p(i,j)~=0
            e(i,j)=p(i,j)*log(p(i,j));
        else
            e(i,j)=0;
        end
    end 
end
for j=1:n
    E(j)=-k*sum(e(:,j));
end
d=1-E;
for j=1:n
         w(j) = d(j) / sum(d); % cálculo del peso del indicador%
end
for j=1:n
         w(j) = w(j) * lamda(j) / sum(w.* lamda); % Modificar peso del indicador
end
for i=1:m
         score(i, 1) = sum(x (i, :).* w);%
end
 disp('El peso de cada indicador es:')
disp(w*100)
 disp('El puntaje integral de cada marca es:')
disp(score)