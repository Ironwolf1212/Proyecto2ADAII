% Parámetros de entrada
int: N;  % Número de clientes
int: M;  % Número de sitios posibles para instalaciones
array[1..M] of float: F;  % Costo fijo de apertura de la instalación i
array[1..M] of int: C;  % Capacidad máxima de producción de la instalación i
array[1..N] of float: D;  % Demanda del cliente c
array[1..N, 1..M] of float: B;  % Beneficio por unidad vendida al cliente c desde la instalación i

% Variables de decisión
array[1..M] of var 0..1: A;  % 1 si la instalación i está abierta, 0 si no
array[1..N, 1..M] of var 0.0..max(D): R;  % Cantidad de productos enviados al cliente c desde la instalación i

% Restricciones

% No negatividad
constraint
    forall(j in 1..N, i in 1..M) (
        R[j, i] >= 0.0
    );

constraint 
    % La producción total en cada instalación no debe exceder su capacidad máxima
    forall(i in 1..M) (
        sum(j in 1..N) (R[j, i]) <= A[i] * C[i]
    );

constraint 
    % La suma de productos enviados a cada cliente debe satisfacer su demanda
    forall(j in 1..N) (
        sum(i in 1..M) (R[j, i]) == D[j]
    );

constraint 
    % Asegurar que A[i] sea 1 si alguna cantidad es producida en la instalación i, de lo contrario 0
    forall(i in 1..M) (
        (sum(j in 1..N) (R[j, i]) > 0.0) -> (A[i] = 1)
    );
    
% Función objetivo: maximizar la utilidad total
var float: total_benefit = sum(j in 1..N, i in 1..M) (R[j, i] * B[j, i]) - sum(i in 1..M) (F[i] * A[i]);

solve maximize total_benefit;

% Restricciones Extra - Mejoran la eficiencia de Gecode, pero inutilizan Coin-BC
%constraint
%    Restringir la apertura de instalaciones a las que pueden satisfacer la demanda de al menos un cliente
%    forall(i in 1..M) (
%       A[i] <= sum(j in 1..N) (D[j] <= C[i])
%   );

%constraint
%    Restringir la apertura de instalaciones a las que pueden generar beneficio
%    forall(j in 1..M) (
%        A[i] <= sum(j ion 1..N) (B[j, i] > 0)
%   );

% Restricciones para romper la simetría

%constraint 
%    Restringir el orden de apertura de las instalaciones
%    forall(i in 1..M-1) (
%        A[i] >= A[i+1]
%    );

%constraint
%    Restringir el orden de asignación de productos a los clientes
%    forall(j in 1..N-1) (
%       forall(i in 1..M) (
%           R[j, i] >= R[j+1, i]
%       )
%   );

% Salida
output ["R = ", show(R), "\n", "A = ", show(A), "\n", "Total Benefit = ", show(total_benefit)];
