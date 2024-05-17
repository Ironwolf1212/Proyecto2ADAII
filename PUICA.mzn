int: N;
int: M;
array [1..M] of int: F;
array [1..M] of int: C;
array [1..N] of float: D;
array [1..M, 1..N] of float: B;


array [1..M] of var 0..1: A;
array [1..M, 1..N] of var 0..max(C): R;

constraint forall(i in 1..M)(sum(j in 1..N)(R[i,j]) = C[i] \/ sum(j in 1..N)(R[i,j]) = 0) ;
constraint forall(j in 1..N)((sum(i in 1..M)(R[i,j]))>=D[j]);
constraint forall(i in 1..M)(A[i] = (sum(j in 1..N)(abs(R[i,j])))/(abs((sum(j in 1..N)(abs(R[i,j])))-1)+1));

%Redundantes


%Rompe simetrias

%solve satisfy;
solve maximize sum(i in 1..M)((sum(j in 1..N)(R[i,j]*B[i,j]))-(F[i]*A[i]));

