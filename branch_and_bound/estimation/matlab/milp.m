function [x,fval, exitflag, output] = milp(f,intcon,A,b,Aeq,beq,lb,ub)
%tic
load(f)
load(intcon)
load(A)
load(b)
load(Aeq)
load(beq)
load(lb)
load(ub)

f = double(f);
intcon = double(intcon);
A = double(A);
b = double(b);
Aeq = double(Aeq);
beq = double(beq);
lb = double(lb);
ub = double(ub);

opts = optimoptions('intlinprog','Display','off');
[x,fval, exitflag, output] = intlinprog(f,intcon,A,b,Aeq,beq,lb,ub, opts);
%toc