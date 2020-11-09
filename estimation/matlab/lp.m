function [x,fval, exitflag, output] = lp(f,A,b,Aeq,beq,lb,ub)
tic
load(f)
load(A)
load(b)
load(Aeq)
load(beq)
load(lb)
load(ub)

f = double(f);
A = double(A);
b = double(b);
Aeq = double(Aeq);
beq = double(beq);
lb = double(lb);
ub = double(ub);

[x, fval, exitflag, output] = linprog(f, A,b,Aeq,beq,lb,ub);
toc