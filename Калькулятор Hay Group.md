# Калькулятор Hay Group

Источник: `Калькулятор Hay Group.xlsm`

> Извлечено из Office Open XML внутри `.xlsm`: значения ячеек, формулы и ключевые листы. Макросы VBA не декомпилировались; макролист `macro d'éval` извлечен как ячейки/формулы, если присутствовал в книге.

## Листы, ячейки и формулы

```text
===== WORKBOOK SHEETS =====
Start -> xl/worksheets/sheet1.xml
Help -> xl/worksheets/sheet2.xml
Worksheet -> xl/worksheets/sheet3.xml
Matrix -> xl/worksheets/sheet4.xml
Jobgrades -> xl/worksheets/sheet5.xml
Matchcodes -> xl/worksheets/sheet6.xml
Validation -> xl/worksheets/sheet7.xml
macro d'éval -> xl/macrosheets/sheet1.xml
HWendt -> 

===== SHEET: Start (xl/worksheets/sheet1.xml) =====
A1	HayCalculator©
B8	Company name :
D8	Samruk - Kazyna
B10	Date:
D10	December 2013
E12	START
B14	Start with reading the instructions on:
E14	Help - sheet

===== SHEET: Help (xl/worksheets/sheet2.xml) =====

===== SHEET: Worksheet (xl/worksheets/sheet3.xml) =====
J1	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G1)=0,LEN(H1)=0,LEN(I1)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G1,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H1),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I1,1)))))
O1	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L1)=0,LEN(M1)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L1),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M1,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L1,1)="+",1,IF(RIGHT(Worksheet!L1,1)="-",-1,0))+IF(RIGHT(Worksheet!M1,1)="+",1,IF(RIGHT(Worksheet!M1,1)="-",-1,0))>0,1,0)))))
P1	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N1,Validation!$A$54:$B$69,2),HLOOKUP(K1,Validation!$D$51:$AD$52,2)))
U1	1	= ISERROR(VLOOKUP(LEFT(T1,LEN(T1)-IF(OR(RIGHT(T1)="-",RIGHT(T1)="+"),1,0)),IF(LEFT(Worksheet!S1,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
X1	#N/A	= VLOOKUP(W1,Jobgrades!$H$7:$L$46,4)
Z1		= LProf(N1,Y1)
A2	Nr.
B2	Match
C2	Area
D2	Department
E2	Jobtitle
G2	Знания и Умения
J2	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G2)=0,LEN(H2)=0,LEN(I2)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G2,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H2),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I2,1)))))
L2	Решение вопросов
O2	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L2)=0,LEN(M2)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L2),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M2,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L2,1)="+",1,IF(RIGHT(Worksheet!L2,1)="-",-1,0))+IF(RIGHT(Worksheet!M2,1)="+",1,IF(RIGHT(Worksheet!M2,1)="-",-1,0))>0,1,0)))))
P2	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(#REF!,Validation!$A$54:$B$69,2),HLOOKUP(#REF!,Validation!$D$51:$AD$52,2)))
R2	Ответственность
U2	1	= ISERROR(VLOOKUP(LEFT(T2,LEN(T2)-IF(OR(RIGHT(T2)="-",RIGHT(T2)="+"),1,0)),IF(LEFT(Worksheet!S2,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
W2	Total
X2	Grade
Y2	Profiles
AA2	Remarks
F3	а
J3	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G3)=0,LEN(H3)=0,LEN(I3)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G3,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H3),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I3,1)))))
K3	0	= COMP(G3,H3,I3)
N3	0	= IC(L3,M3)
O3	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L3)=0,LEN(M3)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L3),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M3,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L3,1)="+",1,IF(RIGHT(Worksheet!L3,1)="-",-1,0))+IF(RIGHT(Worksheet!M3,1)="+",1,IF(RIGHT(Worksheet!M3,1)="-",-1,0))>0,1,0)))))
P3	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N3,Validation!$A$54:$B$69,2),HLOOKUP(K3,Validation!$D$51:$AD$52,2)))
Q3	0	= PTSIC(K3,N3)
U3	1	= ISERROR(VLOOKUP(LEFT(T3,LEN(T3)-IF(OR(RIGHT(T3)="-",RIGHT(T3)="+"),1,0)),IF(LEFT(Worksheet!S3,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
V3	0	= FINALITE(R3,S3,T3)
W3	0	= IF(LEN(F3)<1,0,V3+Q3+K3)
X3	0	= VLOOKUP(W3,Jobgrades!_xlnm.Print_Area,4)
Y3	0	= PROFIL(Q3,V3)
F4	а
J4	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G4)=0,LEN(H4)=0,LEN(I4)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G4,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H4),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I4,1)))))
K4	0
N4	0
O4	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L4)=0,LEN(M4)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L4),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M4,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L4,1)="+",1,IF(RIGHT(Worksheet!L4,1)="-",-1,0))+IF(RIGHT(Worksheet!M4,1)="+",1,IF(RIGHT(Worksheet!M4,1)="-",-1,0))>0,1,0)))))
P4	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N4,Validation!$A$54:$B$69,2),HLOOKUP(K4,Validation!$D$51:$AD$52,2)))
Q4	0
U4	1	= ISERROR(VLOOKUP(LEFT(T4,LEN(T4)-IF(OR(RIGHT(T4)="-",RIGHT(T4)="+"),1,0)),IF(LEFT(Worksheet!S4,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
V4	0
W4	0
X4	0	= VLOOKUP(W4,Jobgrades!_xlnm.Print_Area,4)
Y4	0
F5	а
J5	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G5)=0,LEN(H5)=0,LEN(I5)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G5,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H5),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I5,1)))))
K5	0
N5	0
O5	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L5)=0,LEN(M5)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L5),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M5,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L5,1)="+",1,IF(RIGHT(Worksheet!L5,1)="-",-1,0))+IF(RIGHT(Worksheet!M5,1)="+",1,IF(RIGHT(Worksheet!M5,1)="-",-1,0))>0,1,0)))))
P5	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N5,Validation!$A$54:$B$69,2),HLOOKUP(K5,Validation!$D$51:$AD$52,2)))
Q5	0
U5	1	= ISERROR(VLOOKUP(LEFT(T5,LEN(T5)-IF(OR(RIGHT(T5)="-",RIGHT(T5)="+"),1,0)),IF(LEFT(Worksheet!S5,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
V5	0
W5	0
X5	0	= VLOOKUP(W5,Jobgrades!_xlnm.Print_Area,4)
Y5	0
F6	а
J6	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G6)=0,LEN(H6)=0,LEN(I6)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G6,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H6),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I6,1)))))
K6	0
N6	0
O6	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L6)=0,LEN(M6)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L6),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M6,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L6,1)="+",1,IF(RIGHT(Worksheet!L6,1)="-",-1,0))+IF(RIGHT(Worksheet!M6,1)="+",1,IF(RIGHT(Worksheet!M6,1)="-",-1,0))>0,1,0)))))
P6	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N6,Validation!$A$54:$B$69,2),HLOOKUP(K6,Validation!$D$51:$AD$52,2)))
Q6	0
U6	1	= ISERROR(VLOOKUP(LEFT(T6,LEN(T6)-IF(OR(RIGHT(T6)="-",RIGHT(T6)="+"),1,0)),IF(LEFT(Worksheet!S6,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
V6	0
W6	0
X6	0	= VLOOKUP(W6,Jobgrades!_xlnm.Print_Area,4)
Y6	0
F7	а
J7	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G7)=0,LEN(H7)=0,LEN(I7)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G7,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H7),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I7,1)))))
K7	0	= COMP(G7,H7,I7)
N7	0	= IC(L7,M7)
O7	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L7)=0,LEN(M7)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L7),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M7,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L7,1)="+",1,IF(RIGHT(Worksheet!L7,1)="-",-1,0))+IF(RIGHT(Worksheet!M7,1)="+",1,IF(RIGHT(Worksheet!M7,1)="-",-1,0))>0,1,0)))))
P7	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N7,Validation!$A$54:$B$69,2),HLOOKUP(K7,Validation!$D$51:$AD$52,2)))
Q7	0	= PTSIC(K7,N7)
U7	1	= ISERROR(VLOOKUP(LEFT(T7,LEN(T7)-IF(OR(RIGHT(T7)="-",RIGHT(T7)="+"),1,0)),IF(LEFT(Worksheet!S7,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
V7	0	= FINALITE(R7,S7,T7)
W7	0	= IF(LEN(F7)<1,0,V7+Q7+K7)
X7	0	= VLOOKUP(W7,Jobgrades!_xlnm.Print_Area,4)
Y7	0	= PROFIL(Q7,V7)
F8	а
J8	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G8)=0,LEN(H8)=0,LEN(I8)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G8,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H8),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I8,1)))))
K8	0
N8	0
O8	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L8)=0,LEN(M8)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L8),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M8,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L8,1)="+",1,IF(RIGHT(Worksheet!L8,1)="-",-1,0))+IF(RIGHT(Worksheet!M8,1)="+",1,IF(RIGHT(Worksheet!M8,1)="-",-1,0))>0,1,0)))))
P8	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N8,Validation!$A$54:$B$69,2),HLOOKUP(K8,Validation!$D$51:$AD$52,2)))
Q8	0
U8	1	= ISERROR(VLOOKUP(LEFT(T8,LEN(T8)-IF(OR(RIGHT(T8)="-",RIGHT(T8)="+"),1,0)),IF(LEFT(Worksheet!S8,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
V8	0
W8	0
X8	0	= VLOOKUP(W8,Jobgrades!_xlnm.Print_Area,4)
Y8	0
F9	а
J9	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G9)=0,LEN(H9)=0,LEN(I9)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G9,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H9),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I9,1)))))
K9	0
N9	0
O9	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L9)=0,LEN(M9)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L9),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M9,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L9,1)="+",1,IF(RIGHT(Worksheet!L9,1)="-",-1,0))+IF(RIGHT(Worksheet!M9,1)="+",1,IF(RIGHT(Worksheet!M9,1)="-",-1,0))>0,1,0)))))
P9	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N9,Validation!$A$54:$B$69,2),HLOOKUP(K9,Validation!$D$51:$AD$52,2)))
Q9	0
U9	1	= ISERROR(VLOOKUP(LEFT(T9,LEN(T9)-IF(OR(RIGHT(T9)="-",RIGHT(T9)="+"),1,0)),IF(LEFT(Worksheet!S9,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
V9	0
W9	0
X9	0	= VLOOKUP(W9,Jobgrades!_xlnm.Print_Area,4)
Y9	0
F10	а
J10	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G10)=0,LEN(H10)=0,LEN(I10)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G10,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H10),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I10,1)))))
K10	0
N10	0
O10	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L10)=0,LEN(M10)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L10),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M10,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L10,1)="+",1,IF(RIGHT(Worksheet!L10,1)="-",-1,0))+IF(RIGHT(Worksheet!M10,1)="+",1,IF(RIGHT(Worksheet!M10,1)="-",-1,0))>0,1,0)))))
P10	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N10,Validation!$A$54:$B$69,2),HLOOKUP(K10,Validation!$D$51:$AD$52,2)))
Q10	0
U10	1	= ISERROR(VLOOKUP(LEFT(T10,LEN(T10)-IF(OR(RIGHT(T10)="-",RIGHT(T10)="+"),1,0)),IF(LEFT(Worksheet!S10,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
V10	0
W10	0
X10	0	= VLOOKUP(W10,Jobgrades!_xlnm.Print_Area,4)
Y10	0
F11	а
J11	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G11)=0,LEN(H11)=0,LEN(I11)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G11,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H11),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I11,1)))))
K11	0
N11	0
O11	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L11)=0,LEN(M11)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L11),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M11,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L11,1)="+",1,IF(RIGHT(Worksheet!L11,1)="-",-1,0))+IF(RIGHT(Worksheet!M11,1)="+",1,IF(RIGHT(Worksheet!M11,1)="-",-1,0))>0,1,0)))))
P11	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N11,Validation!$A$54:$B$69,2),HLOOKUP(K11,Validation!$D$51:$AD$52,2)))
Q11	0
U11	1	= ISERROR(VLOOKUP(LEFT(T11,LEN(T11)-IF(OR(RIGHT(T11)="-",RIGHT(T11)="+"),1,0)),IF(LEFT(Worksheet!S11,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
V11	0
W11	0
X11	0	= VLOOKUP(W11,Jobgrades!_xlnm.Print_Area,4)
Y11	0
F12	а
J12	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G12)=0,LEN(H12)=0,LEN(I12)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G12,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H12),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I12,1)))))
K12	0
N12	0
Q12	0
V12	0
W12	0
X12	0	= VLOOKUP(W12,Jobgrades!_xlnm.Print_Area,4)
Y12	0
F13	а
J13	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G13)=0,LEN(H13)=0,LEN(I13)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G13,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H13),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I13,1)))))
K13	0
N13	0
Q13	0
V13	0
W13	0
X13	0	= VLOOKUP(W13,Jobgrades!_xlnm.Print_Area,4)
Y13	0
F14	а
J14	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G14)=0,LEN(H14)=0,LEN(I14)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G14,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H14),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I14,1)))))
K14	0
N14	0
Q14	0
V14	0
W14	0
X14	0	= VLOOKUP(W14,Jobgrades!_xlnm.Print_Area,4)
Y14	0
F15	а
J15	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G15)=0,LEN(H15)=0,LEN(I15)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G15,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H15),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I15,1)))))
K15	0
N15	0
Q15	0
V15	0
W15	0
X15	0	= VLOOKUP(W15,Jobgrades!_xlnm.Print_Area,4)
Y15	0
F16	а
J16	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G16)=0,LEN(H16)=0,LEN(I16)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G16,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H16),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I16,1)))))
K16	0
N16	0
Q16	0
V16	0
W16	0
X16	0	= VLOOKUP(W16,Jobgrades!_xlnm.Print_Area,4)
Y16	0
F17	а
J17	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G17)=0,LEN(H17)=0,LEN(I17)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G17,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H17),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I17,1)))))
K17	0
N17	0
Q17	0
V17	0
W17	0
X17	0	= VLOOKUP(W17,Jobgrades!_xlnm.Print_Area,4)
Y17	0
F18	а
J18	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G18)=0,LEN(H18)=0,LEN(I18)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G18,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H18),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I18,1)))))
K18	0
N18	0
Q18	0
V18	0
W18	0
X18	0	= VLOOKUP(W18,Jobgrades!_xlnm.Print_Area,4)
Y18	0
F19	а
J19	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G19)=0,LEN(H19)=0,LEN(I19)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G19,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H19),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I19,1)))))
K19	0
N19	0
Q19	0
V19	0
W19	0
X19	0	= VLOOKUP(W19,Jobgrades!_xlnm.Print_Area,4)
Y19	0
F20	а
J20	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G20)=0,LEN(H20)=0,LEN(I20)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G20,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H20),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I20,1)))))
K20	0
N20	0
Q20	0
V20	0
W20	0
X20	0	= VLOOKUP(W20,Jobgrades!_xlnm.Print_Area,4)
Y20	0
F21	а
J21	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G21)=0,LEN(H21)=0,LEN(I21)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G21,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H21),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I21,1)))))
K21	0
N21	0
Q21	0
V21	0
W21	0
X21	0	= VLOOKUP(W21,Jobgrades!_xlnm.Print_Area,4)
Y21	0
F22	а
J22	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G22)=0,LEN(H22)=0,LEN(I22)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G22,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H22),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I22,1)))))
K22	0
N22	0
Q22	0
V22	0
W22	0
X22	0	= VLOOKUP(W22,Jobgrades!_xlnm.Print_Area,4)
Y22	0
F23	а
J23	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G23)=0,LEN(H23)=0,LEN(I23)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G23,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H23),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I23,1)))))
K23	0
N23	0
O23	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L23)=0,LEN(M23)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L23),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M23,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L23,1)="+",1,IF(RIGHT(Worksheet!L23,1)="-",-1,0))+IF(RIGHT(Worksheet!M23,1)="+",1,IF(RIGHT(Worksheet!M23,1)="-",-1,0))>0,1,0)))))
P23	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N23,Validation!$A$54:$B$69,2),HLOOKUP(K23,Validation!$D$51:$AD$52,2)))
Q23	0
U23	1	= ISERROR(VLOOKUP(LEFT(T23,LEN(T23)-IF(OR(RIGHT(T23)="-",RIGHT(T23)="+"),1,0)),IF(LEFT(Worksheet!S23,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
V23	0
W23	0
X23	0	= VLOOKUP(W23,Jobgrades!_xlnm.Print_Area,4)
Y23	0
F24	а
J24	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G24)=0,LEN(H24)=0,LEN(I24)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G24,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H24),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I24,1)))))
K24	0
N24	0
O24	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L24)=0,LEN(M24)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L24),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M24,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L24,1)="+",1,IF(RIGHT(Worksheet!L24,1)="-",-1,0))+IF(RIGHT(Worksheet!M24,1)="+",1,IF(RIGHT(Worksheet!M24,1)="-",-1,0))>0,1,0)))))
P24	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N24,Validation!$A$54:$B$69,2),HLOOKUP(K24,Validation!$D$51:$AD$52,2)))
Q24	0
U24	1	= ISERROR(VLOOKUP(LEFT(T24,LEN(T24)-IF(OR(RIGHT(T24)="-",RIGHT(T24)="+"),1,0)),IF(LEFT(Worksheet!S24,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
V24	0
W24	0
X24	0	= VLOOKUP(W24,Jobgrades!_xlnm.Print_Area,4)
Y24	0
J25	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G25)=0,LEN(H25)=0,LEN(I25)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G25,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H25),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I25,1)))))
O25	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L25)=0,LEN(M25)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L25),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M25,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L25,1)="+",1,IF(RIGHT(Worksheet!L25,1)="-",-1,0))+IF(RIGHT(Worksheet!M25,1)="+",1,IF(RIGHT(Worksheet!M25,1)="-",-1,0))>0,1,0)))))
P25	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N25,Validation!$A$54:$B$69,2),HLOOKUP(K25,Validation!$D$51:$AD$52,2)))
U25	1	= ISERROR(VLOOKUP(LEFT(T25,LEN(T25)-IF(OR(RIGHT(T25)="-",RIGHT(T25)="+"),1,0)),IF(LEFT(Worksheet!S25,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J26	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G26)=0,LEN(H26)=0,LEN(I26)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G26,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H26),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I26,1)))))
O26	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L26)=0,LEN(M26)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L26),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M26,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L26,1)="+",1,IF(RIGHT(Worksheet!L26,1)="-",-1,0))+IF(RIGHT(Worksheet!M26,1)="+",1,IF(RIGHT(Worksheet!M26,1)="-",-1,0))>0,1,0)))))
P26	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N26,Validation!$A$54:$B$69,2),HLOOKUP(K26,Validation!$D$51:$AD$52,2)))
U26	1	= ISERROR(VLOOKUP(LEFT(T26,LEN(T26)-IF(OR(RIGHT(T26)="-",RIGHT(T26)="+"),1,0)),IF(LEFT(Worksheet!S26,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J27	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G27)=0,LEN(H27)=0,LEN(I27)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G27,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H27),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I27,1)))))
O27	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L27)=0,LEN(M27)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L27),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M27,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L27,1)="+",1,IF(RIGHT(Worksheet!L27,1)="-",-1,0))+IF(RIGHT(Worksheet!M27,1)="+",1,IF(RIGHT(Worksheet!M27,1)="-",-1,0))>0,1,0)))))
P27	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N27,Validation!$A$54:$B$69,2),HLOOKUP(K27,Validation!$D$51:$AD$52,2)))
U27	1	= ISERROR(VLOOKUP(LEFT(T27,LEN(T27)-IF(OR(RIGHT(T27)="-",RIGHT(T27)="+"),1,0)),IF(LEFT(Worksheet!S27,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J28	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G28)=0,LEN(H28)=0,LEN(I28)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G28,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H28),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I28,1)))))
O28	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L28)=0,LEN(M28)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L28),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M28,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L28,1)="+",1,IF(RIGHT(Worksheet!L28,1)="-",-1,0))+IF(RIGHT(Worksheet!M28,1)="+",1,IF(RIGHT(Worksheet!M28,1)="-",-1,0))>0,1,0)))))
P28	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N28,Validation!$A$54:$B$69,2),HLOOKUP(K28,Validation!$D$51:$AD$52,2)))
U28	1	= ISERROR(VLOOKUP(LEFT(T28,LEN(T28)-IF(OR(RIGHT(T28)="-",RIGHT(T28)="+"),1,0)),IF(LEFT(Worksheet!S28,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J29	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G29)=0,LEN(H29)=0,LEN(I29)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G29,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H29),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I29,1)))))
O29	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L29)=0,LEN(M29)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L29),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M29,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L29,1)="+",1,IF(RIGHT(Worksheet!L29,1)="-",-1,0))+IF(RIGHT(Worksheet!M29,1)="+",1,IF(RIGHT(Worksheet!M29,1)="-",-1,0))>0,1,0)))))
P29	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N29,Validation!$A$54:$B$69,2),HLOOKUP(K29,Validation!$D$51:$AD$52,2)))
U29	1	= ISERROR(VLOOKUP(LEFT(T29,LEN(T29)-IF(OR(RIGHT(T29)="-",RIGHT(T29)="+"),1,0)),IF(LEFT(Worksheet!S29,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J30	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G30)=0,LEN(H30)=0,LEN(I30)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G30,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H30),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I30,1)))))
O30	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L30)=0,LEN(M30)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L30),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M30,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L30,1)="+",1,IF(RIGHT(Worksheet!L30,1)="-",-1,0))+IF(RIGHT(Worksheet!M30,1)="+",1,IF(RIGHT(Worksheet!M30,1)="-",-1,0))>0,1,0)))))
P30	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N30,Validation!$A$54:$B$69,2),HLOOKUP(K30,Validation!$D$51:$AD$52,2)))
U30	1	= ISERROR(VLOOKUP(LEFT(T30,LEN(T30)-IF(OR(RIGHT(T30)="-",RIGHT(T30)="+"),1,0)),IF(LEFT(Worksheet!S30,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J31	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G31)=0,LEN(H31)=0,LEN(I31)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G31,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H31),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I31,1)))))
O31	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L31)=0,LEN(M31)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L31),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M31,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L31,1)="+",1,IF(RIGHT(Worksheet!L31,1)="-",-1,0))+IF(RIGHT(Worksheet!M31,1)="+",1,IF(RIGHT(Worksheet!M31,1)="-",-1,0))>0,1,0)))))
P31	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N31,Validation!$A$54:$B$69,2),HLOOKUP(K31,Validation!$D$51:$AD$52,2)))
U31	1	= ISERROR(VLOOKUP(LEFT(T31,LEN(T31)-IF(OR(RIGHT(T31)="-",RIGHT(T31)="+"),1,0)),IF(LEFT(Worksheet!S31,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J32	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G32)=0,LEN(H32)=0,LEN(I32)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G32,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H32),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I32,1)))))
O32	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L32)=0,LEN(M32)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L32),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M32,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L32,1)="+",1,IF(RIGHT(Worksheet!L32,1)="-",-1,0))+IF(RIGHT(Worksheet!M32,1)="+",1,IF(RIGHT(Worksheet!M32,1)="-",-1,0))>0,1,0)))))
P32	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N32,Validation!$A$54:$B$69,2),HLOOKUP(K32,Validation!$D$51:$AD$52,2)))
U32	1	= ISERROR(VLOOKUP(LEFT(T32,LEN(T32)-IF(OR(RIGHT(T32)="-",RIGHT(T32)="+"),1,0)),IF(LEFT(Worksheet!S32,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J33	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G33)=0,LEN(H33)=0,LEN(I33)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G33,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H33),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I33,1)))))
O33	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L33)=0,LEN(M33)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L33),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M33,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L33,1)="+",1,IF(RIGHT(Worksheet!L33,1)="-",-1,0))+IF(RIGHT(Worksheet!M33,1)="+",1,IF(RIGHT(Worksheet!M33,1)="-",-1,0))>0,1,0)))))
P33	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N33,Validation!$A$54:$B$69,2),HLOOKUP(K33,Validation!$D$51:$AD$52,2)))
U33	1	= ISERROR(VLOOKUP(LEFT(T33,LEN(T33)-IF(OR(RIGHT(T33)="-",RIGHT(T33)="+"),1,0)),IF(LEFT(Worksheet!S33,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J34	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G34)=0,LEN(H34)=0,LEN(I34)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G34,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H34),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I34,1)))))
O34	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L34)=0,LEN(M34)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L34),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M34,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L34,1)="+",1,IF(RIGHT(Worksheet!L34,1)="-",-1,0))+IF(RIGHT(Worksheet!M34,1)="+",1,IF(RIGHT(Worksheet!M34,1)="-",-1,0))>0,1,0)))))
P34	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N34,Validation!$A$54:$B$69,2),HLOOKUP(K34,Validation!$D$51:$AD$52,2)))
U34	1	= ISERROR(VLOOKUP(LEFT(T34,LEN(T34)-IF(OR(RIGHT(T34)="-",RIGHT(T34)="+"),1,0)),IF(LEFT(Worksheet!S34,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J35	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G35)=0,LEN(H35)=0,LEN(I35)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G35,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H35),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I35,1)))))
O35	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L35)=0,LEN(M35)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L35),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M35,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L35,1)="+",1,IF(RIGHT(Worksheet!L35,1)="-",-1,0))+IF(RIGHT(Worksheet!M35,1)="+",1,IF(RIGHT(Worksheet!M35,1)="-",-1,0))>0,1,0)))))
P35	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N35,Validation!$A$54:$B$69,2),HLOOKUP(K35,Validation!$D$51:$AD$52,2)))
U35	1	= ISERROR(VLOOKUP(LEFT(T35,LEN(T35)-IF(OR(RIGHT(T35)="-",RIGHT(T35)="+"),1,0)),IF(LEFT(Worksheet!S35,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J36	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G36)=0,LEN(H36)=0,LEN(I36)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G36,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H36),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I36,1)))))
O36	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L36)=0,LEN(M36)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L36),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M36,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L36,1)="+",1,IF(RIGHT(Worksheet!L36,1)="-",-1,0))+IF(RIGHT(Worksheet!M36,1)="+",1,IF(RIGHT(Worksheet!M36,1)="-",-1,0))>0,1,0)))))
P36	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N36,Validation!$A$54:$B$69,2),HLOOKUP(K36,Validation!$D$51:$AD$52,2)))
U36	1	= ISERROR(VLOOKUP(LEFT(T36,LEN(T36)-IF(OR(RIGHT(T36)="-",RIGHT(T36)="+"),1,0)),IF(LEFT(Worksheet!S36,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J37	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G37)=0,LEN(H37)=0,LEN(I37)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G37,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H37),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I37,1)))))
O37	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L37)=0,LEN(M37)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L37),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M37,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L37,1)="+",1,IF(RIGHT(Worksheet!L37,1)="-",-1,0))+IF(RIGHT(Worksheet!M37,1)="+",1,IF(RIGHT(Worksheet!M37,1)="-",-1,0))>0,1,0)))))
P37	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N37,Validation!$A$54:$B$69,2),HLOOKUP(K37,Validation!$D$51:$AD$52,2)))
U37	1	= ISERROR(VLOOKUP(LEFT(T37,LEN(T37)-IF(OR(RIGHT(T37)="-",RIGHT(T37)="+"),1,0)),IF(LEFT(Worksheet!S37,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J38	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G38)=0,LEN(H38)=0,LEN(I38)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G38,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H38),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I38,1)))))
O38	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L38)=0,LEN(M38)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L38),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M38,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L38,1)="+",1,IF(RIGHT(Worksheet!L38,1)="-",-1,0))+IF(RIGHT(Worksheet!M38,1)="+",1,IF(RIGHT(Worksheet!M38,1)="-",-1,0))>0,1,0)))))
P38	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N38,Validation!$A$54:$B$69,2),HLOOKUP(K38,Validation!$D$51:$AD$52,2)))
U38	1	= ISERROR(VLOOKUP(LEFT(T38,LEN(T38)-IF(OR(RIGHT(T38)="-",RIGHT(T38)="+"),1,0)),IF(LEFT(Worksheet!S38,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J39	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G39)=0,LEN(H39)=0,LEN(I39)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G39,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H39),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I39,1)))))
O39	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L39)=0,LEN(M39)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L39),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M39,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L39,1)="+",1,IF(RIGHT(Worksheet!L39,1)="-",-1,0))+IF(RIGHT(Worksheet!M39,1)="+",1,IF(RIGHT(Worksheet!M39,1)="-",-1,0))>0,1,0)))))
P39	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N39,Validation!$A$54:$B$69,2),HLOOKUP(K39,Validation!$D$51:$AD$52,2)))
U39	1	= ISERROR(VLOOKUP(LEFT(T39,LEN(T39)-IF(OR(RIGHT(T39)="-",RIGHT(T39)="+"),1,0)),IF(LEFT(Worksheet!S39,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J40	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G40)=0,LEN(H40)=0,LEN(I40)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G40,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H40),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I40,1)))))
O40	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L40)=0,LEN(M40)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L40),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M40,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L40,1)="+",1,IF(RIGHT(Worksheet!L40,1)="-",-1,0))+IF(RIGHT(Worksheet!M40,1)="+",1,IF(RIGHT(Worksheet!M40,1)="-",-1,0))>0,1,0)))))
P40	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N40,Validation!$A$54:$B$69,2),HLOOKUP(K40,Validation!$D$51:$AD$52,2)))
U40	1	= ISERROR(VLOOKUP(LEFT(T40,LEN(T40)-IF(OR(RIGHT(T40)="-",RIGHT(T40)="+"),1,0)),IF(LEFT(Worksheet!S40,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J41	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G41)=0,LEN(H41)=0,LEN(I41)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G41,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H41),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I41,1)))))
O41	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L41)=0,LEN(M41)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L41),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M41,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L41,1)="+",1,IF(RIGHT(Worksheet!L41,1)="-",-1,0))+IF(RIGHT(Worksheet!M41,1)="+",1,IF(RIGHT(Worksheet!M41,1)="-",-1,0))>0,1,0)))))
P41	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N41,Validation!$A$54:$B$69,2),HLOOKUP(K41,Validation!$D$51:$AD$52,2)))
U41	1	= ISERROR(VLOOKUP(LEFT(T41,LEN(T41)-IF(OR(RIGHT(T41)="-",RIGHT(T41)="+"),1,0)),IF(LEFT(Worksheet!S41,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J42	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G42)=0,LEN(H42)=0,LEN(I42)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G42,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H42),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I42,1)))))
O42	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L42)=0,LEN(M42)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L42),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M42,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L42,1)="+",1,IF(RIGHT(Worksheet!L42,1)="-",-1,0))+IF(RIGHT(Worksheet!M42,1)="+",1,IF(RIGHT(Worksheet!M42,1)="-",-1,0))>0,1,0)))))
P42	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N42,Validation!$A$54:$B$69,2),HLOOKUP(K42,Validation!$D$51:$AD$52,2)))
U42	1	= ISERROR(VLOOKUP(LEFT(T42,LEN(T42)-IF(OR(RIGHT(T42)="-",RIGHT(T42)="+"),1,0)),IF(LEFT(Worksheet!S42,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J43	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G43)=0,LEN(H43)=0,LEN(I43)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G43,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H43),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I43,1)))))
O43	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L43)=0,LEN(M43)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L43),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M43,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L43,1)="+",1,IF(RIGHT(Worksheet!L43,1)="-",-1,0))+IF(RIGHT(Worksheet!M43,1)="+",1,IF(RIGHT(Worksheet!M43,1)="-",-1,0))>0,1,0)))))
P43	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N43,Validation!$A$54:$B$69,2),HLOOKUP(K43,Validation!$D$51:$AD$52,2)))
U43	1	= ISERROR(VLOOKUP(LEFT(T43,LEN(T43)-IF(OR(RIGHT(T43)="-",RIGHT(T43)="+"),1,0)),IF(LEFT(Worksheet!S43,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J44	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G44)=0,LEN(H44)=0,LEN(I44)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G44,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H44),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I44,1)))))
O44	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L44)=0,LEN(M44)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L44),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M44,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L44,1)="+",1,IF(RIGHT(Worksheet!L44,1)="-",-1,0))+IF(RIGHT(Worksheet!M44,1)="+",1,IF(RIGHT(Worksheet!M44,1)="-",-1,0))>0,1,0)))))
P44	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N44,Validation!$A$54:$B$69,2),HLOOKUP(K44,Validation!$D$51:$AD$52,2)))
U44	1	= ISERROR(VLOOKUP(LEFT(T44,LEN(T44)-IF(OR(RIGHT(T44)="-",RIGHT(T44)="+"),1,0)),IF(LEFT(Worksheet!S44,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J45	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G45)=0,LEN(H45)=0,LEN(I45)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G45,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H45),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I45,1)))))
O45	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L45)=0,LEN(M45)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L45),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M45,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L45,1)="+",1,IF(RIGHT(Worksheet!L45,1)="-",-1,0))+IF(RIGHT(Worksheet!M45,1)="+",1,IF(RIGHT(Worksheet!M45,1)="-",-1,0))>0,1,0)))))
P45	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N45,Validation!$A$54:$B$69,2),HLOOKUP(K45,Validation!$D$51:$AD$52,2)))
U45	1	= ISERROR(VLOOKUP(LEFT(T45,LEN(T45)-IF(OR(RIGHT(T45)="-",RIGHT(T45)="+"),1,0)),IF(LEFT(Worksheet!S45,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J46	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G46)=0,LEN(H46)=0,LEN(I46)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G46,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H46),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I46,1)))))
O46	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L46)=0,LEN(M46)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L46),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M46,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L46,1)="+",1,IF(RIGHT(Worksheet!L46,1)="-",-1,0))+IF(RIGHT(Worksheet!M46,1)="+",1,IF(RIGHT(Worksheet!M46,1)="-",-1,0))>0,1,0)))))
P46	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N46,Validation!$A$54:$B$69,2),HLOOKUP(K46,Validation!$D$51:$AD$52,2)))
U46	1	= ISERROR(VLOOKUP(LEFT(T46,LEN(T46)-IF(OR(RIGHT(T46)="-",RIGHT(T46)="+"),1,0)),IF(LEFT(Worksheet!S46,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J47	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G47)=0,LEN(H47)=0,LEN(I47)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G47,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H47),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I47,1)))))
O47	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L47)=0,LEN(M47)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L47),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M47,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L47,1)="+",1,IF(RIGHT(Worksheet!L47,1)="-",-1,0))+IF(RIGHT(Worksheet!M47,1)="+",1,IF(RIGHT(Worksheet!M47,1)="-",-1,0))>0,1,0)))))
P47	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N47,Validation!$A$54:$B$69,2),HLOOKUP(K47,Validation!$D$51:$AD$52,2)))
U47	1	= ISERROR(VLOOKUP(LEFT(T47,LEN(T47)-IF(OR(RIGHT(T47)="-",RIGHT(T47)="+"),1,0)),IF(LEFT(Worksheet!S47,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J48	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G48)=0,LEN(H48)=0,LEN(I48)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G48,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H48),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I48,1)))))
O48	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L48)=0,LEN(M48)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L48),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M48,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L48,1)="+",1,IF(RIGHT(Worksheet!L48,1)="-",-1,0))+IF(RIGHT(Worksheet!M48,1)="+",1,IF(RIGHT(Worksheet!M48,1)="-",-1,0))>0,1,0)))))
P48	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N48,Validation!$A$54:$B$69,2),HLOOKUP(K48,Validation!$D$51:$AD$52,2)))
U48	1	= ISERROR(VLOOKUP(LEFT(T48,LEN(T48)-IF(OR(RIGHT(T48)="-",RIGHT(T48)="+"),1,0)),IF(LEFT(Worksheet!S48,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J49	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G49)=0,LEN(H49)=0,LEN(I49)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G49,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H49),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I49,1)))))
O49	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L49)=0,LEN(M49)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L49),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M49,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L49,1)="+",1,IF(RIGHT(Worksheet!L49,1)="-",-1,0))+IF(RIGHT(Worksheet!M49,1)="+",1,IF(RIGHT(Worksheet!M49,1)="-",-1,0))>0,1,0)))))
P49	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N49,Validation!$A$54:$B$69,2),HLOOKUP(K49,Validation!$D$51:$AD$52,2)))
U49	1	= ISERROR(VLOOKUP(LEFT(T49,LEN(T49)-IF(OR(RIGHT(T49)="-",RIGHT(T49)="+"),1,0)),IF(LEFT(Worksheet!S49,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J50	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G50)=0,LEN(H50)=0,LEN(I50)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G50,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H50),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I50,1)))))
O50	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L50)=0,LEN(M50)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L50),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M50,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L50,1)="+",1,IF(RIGHT(Worksheet!L50,1)="-",-1,0))+IF(RIGHT(Worksheet!M50,1)="+",1,IF(RIGHT(Worksheet!M50,1)="-",-1,0))>0,1,0)))))
P50	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N50,Validation!$A$54:$B$69,2),HLOOKUP(K50,Validation!$D$51:$AD$52,2)))
U50	1	= ISERROR(VLOOKUP(LEFT(T50,LEN(T50)-IF(OR(RIGHT(T50)="-",RIGHT(T50)="+"),1,0)),IF(LEFT(Worksheet!S50,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J51	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G51)=0,LEN(H51)=0,LEN(I51)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G51,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H51),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I51,1)))))
O51	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L51)=0,LEN(M51)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L51),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M51,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L51,1)="+",1,IF(RIGHT(Worksheet!L51,1)="-",-1,0))+IF(RIGHT(Worksheet!M51,1)="+",1,IF(RIGHT(Worksheet!M51,1)="-",-1,0))>0,1,0)))))
P51	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N51,Validation!$A$54:$B$69,2),HLOOKUP(K51,Validation!$D$51:$AD$52,2)))
U51	1	= ISERROR(VLOOKUP(LEFT(T51,LEN(T51)-IF(OR(RIGHT(T51)="-",RIGHT(T51)="+"),1,0)),IF(LEFT(Worksheet!S51,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J52	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G52)=0,LEN(H52)=0,LEN(I52)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G52,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H52),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I52,1)))))
O52	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L52)=0,LEN(M52)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L52),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M52,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L52,1)="+",1,IF(RIGHT(Worksheet!L52,1)="-",-1,0))+IF(RIGHT(Worksheet!M52,1)="+",1,IF(RIGHT(Worksheet!M52,1)="-",-1,0))>0,1,0)))))
P52	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N52,Validation!$A$54:$B$69,2),HLOOKUP(K52,Validation!$D$51:$AD$52,2)))
U52	1	= ISERROR(VLOOKUP(LEFT(T52,LEN(T52)-IF(OR(RIGHT(T52)="-",RIGHT(T52)="+"),1,0)),IF(LEFT(Worksheet!S52,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J53	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G53)=0,LEN(H53)=0,LEN(I53)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G53,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H53),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I53,1)))))
O53	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L53)=0,LEN(M53)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L53),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M53,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L53,1)="+",1,IF(RIGHT(Worksheet!L53,1)="-",-1,0))+IF(RIGHT(Worksheet!M53,1)="+",1,IF(RIGHT(Worksheet!M53,1)="-",-1,0))>0,1,0)))))
P53	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N53,Validation!$A$54:$B$69,2),HLOOKUP(K53,Validation!$D$51:$AD$52,2)))
U53	1	= ISERROR(VLOOKUP(LEFT(T53,LEN(T53)-IF(OR(RIGHT(T53)="-",RIGHT(T53)="+"),1,0)),IF(LEFT(Worksheet!S53,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J54	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G54)=0,LEN(H54)=0,LEN(I54)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G54,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H54),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I54,1)))))
O54	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L54)=0,LEN(M54)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L54),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M54,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L54,1)="+",1,IF(RIGHT(Worksheet!L54,1)="-",-1,0))+IF(RIGHT(Worksheet!M54,1)="+",1,IF(RIGHT(Worksheet!M54,1)="-",-1,0))>0,1,0)))))
P54	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N54,Validation!$A$54:$B$69,2),HLOOKUP(K54,Validation!$D$51:$AD$52,2)))
U54	1	= ISERROR(VLOOKUP(LEFT(T54,LEN(T54)-IF(OR(RIGHT(T54)="-",RIGHT(T54)="+"),1,0)),IF(LEFT(Worksheet!S54,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J55	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G55)=0,LEN(H55)=0,LEN(I55)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G55,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H55),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I55,1)))))
O55	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L55)=0,LEN(M55)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L55),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M55,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L55,1)="+",1,IF(RIGHT(Worksheet!L55,1)="-",-1,0))+IF(RIGHT(Worksheet!M55,1)="+",1,IF(RIGHT(Worksheet!M55,1)="-",-1,0))>0,1,0)))))
P55	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N55,Validation!$A$54:$B$69,2),HLOOKUP(K55,Validation!$D$51:$AD$52,2)))
U55	1	= ISERROR(VLOOKUP(LEFT(T55,LEN(T55)-IF(OR(RIGHT(T55)="-",RIGHT(T55)="+"),1,0)),IF(LEFT(Worksheet!S55,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J56	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G56)=0,LEN(H56)=0,LEN(I56)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G56,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H56),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I56,1)))))
O56	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L56)=0,LEN(M56)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L56),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M56,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L56,1)="+",1,IF(RIGHT(Worksheet!L56,1)="-",-1,0))+IF(RIGHT(Worksheet!M56,1)="+",1,IF(RIGHT(Worksheet!M56,1)="-",-1,0))>0,1,0)))))
P56	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N56,Validation!$A$54:$B$69,2),HLOOKUP(K56,Validation!$D$51:$AD$52,2)))
U56	1	= ISERROR(VLOOKUP(LEFT(T56,LEN(T56)-IF(OR(RIGHT(T56)="-",RIGHT(T56)="+"),1,0)),IF(LEFT(Worksheet!S56,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J57	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G57)=0,LEN(H57)=0,LEN(I57)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G57,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H57),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I57,1)))))
O57	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L57)=0,LEN(M57)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L57),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M57,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L57,1)="+",1,IF(RIGHT(Worksheet!L57,1)="-",-1,0))+IF(RIGHT(Worksheet!M57,1)="+",1,IF(RIGHT(Worksheet!M57,1)="-",-1,0))>0,1,0)))))
P57	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N57,Validation!$A$54:$B$69,2),HLOOKUP(K57,Validation!$D$51:$AD$52,2)))
U57	1	= ISERROR(VLOOKUP(LEFT(T57,LEN(T57)-IF(OR(RIGHT(T57)="-",RIGHT(T57)="+"),1,0)),IF(LEFT(Worksheet!S57,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J58	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G58)=0,LEN(H58)=0,LEN(I58)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G58,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H58),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I58,1)))))
O58	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L58)=0,LEN(M58)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L58),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M58,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L58,1)="+",1,IF(RIGHT(Worksheet!L58,1)="-",-1,0))+IF(RIGHT(Worksheet!M58,1)="+",1,IF(RIGHT(Worksheet!M58,1)="-",-1,0))>0,1,0)))))
P58	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N58,Validation!$A$54:$B$69,2),HLOOKUP(K58,Validation!$D$51:$AD$52,2)))
U58	1	= ISERROR(VLOOKUP(LEFT(T58,LEN(T58)-IF(OR(RIGHT(T58)="-",RIGHT(T58)="+"),1,0)),IF(LEFT(Worksheet!S58,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J59	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G59)=0,LEN(H59)=0,LEN(I59)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G59,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H59),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I59,1)))))
O59	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L59)=0,LEN(M59)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L59),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M59,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L59,1)="+",1,IF(RIGHT(Worksheet!L59,1)="-",-1,0))+IF(RIGHT(Worksheet!M59,1)="+",1,IF(RIGHT(Worksheet!M59,1)="-",-1,0))>0,1,0)))))
P59	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N59,Validation!$A$54:$B$69,2),HLOOKUP(K59,Validation!$D$51:$AD$52,2)))
U59	1	= ISERROR(VLOOKUP(LEFT(T59,LEN(T59)-IF(OR(RIGHT(T59)="-",RIGHT(T59)="+"),1,0)),IF(LEFT(Worksheet!S59,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J60	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G60)=0,LEN(H60)=0,LEN(I60)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G60,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H60),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I60,1)))))
O60	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L60)=0,LEN(M60)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L60),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M60,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L60,1)="+",1,IF(RIGHT(Worksheet!L60,1)="-",-1,0))+IF(RIGHT(Worksheet!M60,1)="+",1,IF(RIGHT(Worksheet!M60,1)="-",-1,0))>0,1,0)))))
P60	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N60,Validation!$A$54:$B$69,2),HLOOKUP(K60,Validation!$D$51:$AD$52,2)))
U60	1	= ISERROR(VLOOKUP(LEFT(T60,LEN(T60)-IF(OR(RIGHT(T60)="-",RIGHT(T60)="+"),1,0)),IF(LEFT(Worksheet!S60,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J61	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G61)=0,LEN(H61)=0,LEN(I61)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G61,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H61),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I61,1)))))
O61	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L61)=0,LEN(M61)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L61),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M61,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L61,1)="+",1,IF(RIGHT(Worksheet!L61,1)="-",-1,0))+IF(RIGHT(Worksheet!M61,1)="+",1,IF(RIGHT(Worksheet!M61,1)="-",-1,0))>0,1,0)))))
P61	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N61,Validation!$A$54:$B$69,2),HLOOKUP(K61,Validation!$D$51:$AD$52,2)))
U61	1	= ISERROR(VLOOKUP(LEFT(T61,LEN(T61)-IF(OR(RIGHT(T61)="-",RIGHT(T61)="+"),1,0)),IF(LEFT(Worksheet!S61,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J62	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G62)=0,LEN(H62)=0,LEN(I62)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G62,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H62),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I62,1)))))
O62	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L62)=0,LEN(M62)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L62),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M62,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L62,1)="+",1,IF(RIGHT(Worksheet!L62,1)="-",-1,0))+IF(RIGHT(Worksheet!M62,1)="+",1,IF(RIGHT(Worksheet!M62,1)="-",-1,0))>0,1,0)))))
P62	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N62,Validation!$A$54:$B$69,2),HLOOKUP(K62,Validation!$D$51:$AD$52,2)))
U62	1	= ISERROR(VLOOKUP(LEFT(T62,LEN(T62)-IF(OR(RIGHT(T62)="-",RIGHT(T62)="+"),1,0)),IF(LEFT(Worksheet!S62,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J63	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G63)=0,LEN(H63)=0,LEN(I63)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G63,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H63),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I63,1)))))
O63	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L63)=0,LEN(M63)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L63),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M63,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L63,1)="+",1,IF(RIGHT(Worksheet!L63,1)="-",-1,0))+IF(RIGHT(Worksheet!M63,1)="+",1,IF(RIGHT(Worksheet!M63,1)="-",-1,0))>0,1,0)))))
P63	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N63,Validation!$A$54:$B$69,2),HLOOKUP(K63,Validation!$D$51:$AD$52,2)))
U63	1	= ISERROR(VLOOKUP(LEFT(T63,LEN(T63)-IF(OR(RIGHT(T63)="-",RIGHT(T63)="+"),1,0)),IF(LEFT(Worksheet!S63,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J64	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G64)=0,LEN(H64)=0,LEN(I64)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G64,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H64),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I64,1)))))
O64	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L64)=0,LEN(M64)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L64),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M64,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L64,1)="+",1,IF(RIGHT(Worksheet!L64,1)="-",-1,0))+IF(RIGHT(Worksheet!M64,1)="+",1,IF(RIGHT(Worksheet!M64,1)="-",-1,0))>0,1,0)))))
P64	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N64,Validation!$A$54:$B$69,2),HLOOKUP(K64,Validation!$D$51:$AD$52,2)))
U64	1	= ISERROR(VLOOKUP(LEFT(T64,LEN(T64)-IF(OR(RIGHT(T64)="-",RIGHT(T64)="+"),1,0)),IF(LEFT(Worksheet!S64,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J65	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G65)=0,LEN(H65)=0,LEN(I65)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G65,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H65),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I65,1)))))
O65	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L65)=0,LEN(M65)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L65),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M65,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L65,1)="+",1,IF(RIGHT(Worksheet!L65,1)="-",-1,0))+IF(RIGHT(Worksheet!M65,1)="+",1,IF(RIGHT(Worksheet!M65,1)="-",-1,0))>0,1,0)))))
P65	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N65,Validation!$A$54:$B$69,2),HLOOKUP(K65,Validation!$D$51:$AD$52,2)))
U65	1	= ISERROR(VLOOKUP(LEFT(T65,LEN(T65)-IF(OR(RIGHT(T65)="-",RIGHT(T65)="+"),1,0)),IF(LEFT(Worksheet!S65,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J66	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G66)=0,LEN(H66)=0,LEN(I66)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G66,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H66),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I66,1)))))
O66	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L66)=0,LEN(M66)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L66),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M66,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L66,1)="+",1,IF(RIGHT(Worksheet!L66,1)="-",-1,0))+IF(RIGHT(Worksheet!M66,1)="+",1,IF(RIGHT(Worksheet!M66,1)="-",-1,0))>0,1,0)))))
P66	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N66,Validation!$A$54:$B$69,2),HLOOKUP(K66,Validation!$D$51:$AD$52,2)))
U66	1	= ISERROR(VLOOKUP(LEFT(T66,LEN(T66)-IF(OR(RIGHT(T66)="-",RIGHT(T66)="+"),1,0)),IF(LEFT(Worksheet!S66,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J67	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G67)=0,LEN(H67)=0,LEN(I67)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G67,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H67),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I67,1)))))
O67	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L67)=0,LEN(M67)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L67),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M67,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L67,1)="+",1,IF(RIGHT(Worksheet!L67,1)="-",-1,0))+IF(RIGHT(Worksheet!M67,1)="+",1,IF(RIGHT(Worksheet!M67,1)="-",-1,0))>0,1,0)))))
P67	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N67,Validation!$A$54:$B$69,2),HLOOKUP(K67,Validation!$D$51:$AD$52,2)))
U67	1	= ISERROR(VLOOKUP(LEFT(T67,LEN(T67)-IF(OR(RIGHT(T67)="-",RIGHT(T67)="+"),1,0)),IF(LEFT(Worksheet!S67,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J68	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G68)=0,LEN(H68)=0,LEN(I68)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G68,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H68),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I68,1)))))
O68	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L68)=0,LEN(M68)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L68),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M68,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L68,1)="+",1,IF(RIGHT(Worksheet!L68,1)="-",-1,0))+IF(RIGHT(Worksheet!M68,1)="+",1,IF(RIGHT(Worksheet!M68,1)="-",-1,0))>0,1,0)))))
P68	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N68,Validation!$A$54:$B$69,2),HLOOKUP(K68,Validation!$D$51:$AD$52,2)))
U68	1	= ISERROR(VLOOKUP(LEFT(T68,LEN(T68)-IF(OR(RIGHT(T68)="-",RIGHT(T68)="+"),1,0)),IF(LEFT(Worksheet!S68,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J69	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G69)=0,LEN(H69)=0,LEN(I69)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G69,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H69),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I69,1)))))
O69	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L69)=0,LEN(M69)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L69),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M69,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L69,1)="+",1,IF(RIGHT(Worksheet!L69,1)="-",-1,0))+IF(RIGHT(Worksheet!M69,1)="+",1,IF(RIGHT(Worksheet!M69,1)="-",-1,0))>0,1,0)))))
P69	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N69,Validation!$A$54:$B$69,2),HLOOKUP(K69,Validation!$D$51:$AD$52,2)))
U69	1	= ISERROR(VLOOKUP(LEFT(T69,LEN(T69)-IF(OR(RIGHT(T69)="-",RIGHT(T69)="+"),1,0)),IF(LEFT(Worksheet!S69,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J70	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G70)=0,LEN(H70)=0,LEN(I70)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G70,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H70),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I70,1)))))
O70	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L70)=0,LEN(M70)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L70),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M70,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L70,1)="+",1,IF(RIGHT(Worksheet!L70,1)="-",-1,0))+IF(RIGHT(Worksheet!M70,1)="+",1,IF(RIGHT(Worksheet!M70,1)="-",-1,0))>0,1,0)))))
P70	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N70,Validation!$A$54:$B$69,2),HLOOKUP(K70,Validation!$D$51:$AD$52,2)))
U70	1	= ISERROR(VLOOKUP(LEFT(T70,LEN(T70)-IF(OR(RIGHT(T70)="-",RIGHT(T70)="+"),1,0)),IF(LEFT(Worksheet!S70,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J71	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G71)=0,LEN(H71)=0,LEN(I71)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G71,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H71),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I71,1)))))
O71	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L71)=0,LEN(M71)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L71),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M71,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L71,1)="+",1,IF(RIGHT(Worksheet!L71,1)="-",-1,0))+IF(RIGHT(Worksheet!M71,1)="+",1,IF(RIGHT(Worksheet!M71,1)="-",-1,0))>0,1,0)))))
P71	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N71,Validation!$A$54:$B$69,2),HLOOKUP(K71,Validation!$D$51:$AD$52,2)))
U71	1	= ISERROR(VLOOKUP(LEFT(T71,LEN(T71)-IF(OR(RIGHT(T71)="-",RIGHT(T71)="+"),1,0)),IF(LEFT(Worksheet!S71,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J72	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G72)=0,LEN(H72)=0,LEN(I72)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G72,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H72),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I72,1)))))
O72	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L72)=0,LEN(M72)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L72),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M72,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L72,1)="+",1,IF(RIGHT(Worksheet!L72,1)="-",-1,0))+IF(RIGHT(Worksheet!M72,1)="+",1,IF(RIGHT(Worksheet!M72,1)="-",-1,0))>0,1,0)))))
P72	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N72,Validation!$A$54:$B$69,2),HLOOKUP(K72,Validation!$D$51:$AD$52,2)))
U72	1	= ISERROR(VLOOKUP(LEFT(T72,LEN(T72)-IF(OR(RIGHT(T72)="-",RIGHT(T72)="+"),1,0)),IF(LEFT(Worksheet!S72,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J73	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G73)=0,LEN(H73)=0,LEN(I73)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G73,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H73),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I73,1)))))
O73	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L73)=0,LEN(M73)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L73),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M73,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L73,1)="+",1,IF(RIGHT(Worksheet!L73,1)="-",-1,0))+IF(RIGHT(Worksheet!M73,1)="+",1,IF(RIGHT(Worksheet!M73,1)="-",-1,0))>0,1,0)))))
P73	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N73,Validation!$A$54:$B$69,2),HLOOKUP(K73,Validation!$D$51:$AD$52,2)))
U73	1	= ISERROR(VLOOKUP(LEFT(T73,LEN(T73)-IF(OR(RIGHT(T73)="-",RIGHT(T73)="+"),1,0)),IF(LEFT(Worksheet!S73,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J74	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G74)=0,LEN(H74)=0,LEN(I74)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G74,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H74),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I74,1)))))
O74	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L74)=0,LEN(M74)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L74),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M74,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L74,1)="+",1,IF(RIGHT(Worksheet!L74,1)="-",-1,0))+IF(RIGHT(Worksheet!M74,1)="+",1,IF(RIGHT(Worksheet!M74,1)="-",-1,0))>0,1,0)))))
P74	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N74,Validation!$A$54:$B$69,2),HLOOKUP(K74,Validation!$D$51:$AD$52,2)))
U74	1	= ISERROR(VLOOKUP(LEFT(T74,LEN(T74)-IF(OR(RIGHT(T74)="-",RIGHT(T74)="+"),1,0)),IF(LEFT(Worksheet!S74,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J75	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G75)=0,LEN(H75)=0,LEN(I75)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G75,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H75),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I75,1)))))
O75	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L75)=0,LEN(M75)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L75),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M75,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L75,1)="+",1,IF(RIGHT(Worksheet!L75,1)="-",-1,0))+IF(RIGHT(Worksheet!M75,1)="+",1,IF(RIGHT(Worksheet!M75,1)="-",-1,0))>0,1,0)))))
P75	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N75,Validation!$A$54:$B$69,2),HLOOKUP(K75,Validation!$D$51:$AD$52,2)))
U75	1	= ISERROR(VLOOKUP(LEFT(T75,LEN(T75)-IF(OR(RIGHT(T75)="-",RIGHT(T75)="+"),1,0)),IF(LEFT(Worksheet!S75,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J76	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G76)=0,LEN(H76)=0,LEN(I76)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G76,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H76),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I76,1)))))
O76	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L76)=0,LEN(M76)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L76),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M76,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L76,1)="+",1,IF(RIGHT(Worksheet!L76,1)="-",-1,0))+IF(RIGHT(Worksheet!M76,1)="+",1,IF(RIGHT(Worksheet!M76,1)="-",-1,0))>0,1,0)))))
P76	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N76,Validation!$A$54:$B$69,2),HLOOKUP(K76,Validation!$D$51:$AD$52,2)))
U76	1	= ISERROR(VLOOKUP(LEFT(T76,LEN(T76)-IF(OR(RIGHT(T76)="-",RIGHT(T76)="+"),1,0)),IF(LEFT(Worksheet!S76,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J77	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G77)=0,LEN(H77)=0,LEN(I77)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G77,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H77),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I77,1)))))
O77	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L77)=0,LEN(M77)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L77),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M77,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L77,1)="+",1,IF(RIGHT(Worksheet!L77,1)="-",-1,0))+IF(RIGHT(Worksheet!M77,1)="+",1,IF(RIGHT(Worksheet!M77,1)="-",-1,0))>0,1,0)))))
P77	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N77,Validation!$A$54:$B$69,2),HLOOKUP(K77,Validation!$D$51:$AD$52,2)))
U77	1	= ISERROR(VLOOKUP(LEFT(T77,LEN(T77)-IF(OR(RIGHT(T77)="-",RIGHT(T77)="+"),1,0)),IF(LEFT(Worksheet!S77,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J78	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G78)=0,LEN(H78)=0,LEN(I78)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G78,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H78),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I78,1)))))
O78	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L78)=0,LEN(M78)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L78),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M78,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L78,1)="+",1,IF(RIGHT(Worksheet!L78,1)="-",-1,0))+IF(RIGHT(Worksheet!M78,1)="+",1,IF(RIGHT(Worksheet!M78,1)="-",-1,0))>0,1,0)))))
P78	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N78,Validation!$A$54:$B$69,2),HLOOKUP(K78,Validation!$D$51:$AD$52,2)))
U78	1	= ISERROR(VLOOKUP(LEFT(T78,LEN(T78)-IF(OR(RIGHT(T78)="-",RIGHT(T78)="+"),1,0)),IF(LEFT(Worksheet!S78,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J79	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G79)=0,LEN(H79)=0,LEN(I79)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G79,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H79),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I79,1)))))
O79	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L79)=0,LEN(M79)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L79),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M79,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L79,1)="+",1,IF(RIGHT(Worksheet!L79,1)="-",-1,0))+IF(RIGHT(Worksheet!M79,1)="+",1,IF(RIGHT(Worksheet!M79,1)="-",-1,0))>0,1,0)))))
P79	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N79,Validation!$A$54:$B$69,2),HLOOKUP(K79,Validation!$D$51:$AD$52,2)))
U79	1	= ISERROR(VLOOKUP(LEFT(T79,LEN(T79)-IF(OR(RIGHT(T79)="-",RIGHT(T79)="+"),1,0)),IF(LEFT(Worksheet!S79,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J80	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G80)=0,LEN(H80)=0,LEN(I80)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G80,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H80),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I80,1)))))
O80	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L80)=0,LEN(M80)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L80),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M80,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L80,1)="+",1,IF(RIGHT(Worksheet!L80,1)="-",-1,0))+IF(RIGHT(Worksheet!M80,1)="+",1,IF(RIGHT(Worksheet!M80,1)="-",-1,0))>0,1,0)))))
P80	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N80,Validation!$A$54:$B$69,2),HLOOKUP(K80,Validation!$D$51:$AD$52,2)))
U80	1	= ISERROR(VLOOKUP(LEFT(T80,LEN(T80)-IF(OR(RIGHT(T80)="-",RIGHT(T80)="+"),1,0)),IF(LEFT(Worksheet!S80,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J81	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G81)=0,LEN(H81)=0,LEN(I81)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G81,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H81),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I81,1)))))
O81	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L81)=0,LEN(M81)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L81),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M81,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L81,1)="+",1,IF(RIGHT(Worksheet!L81,1)="-",-1,0))+IF(RIGHT(Worksheet!M81,1)="+",1,IF(RIGHT(Worksheet!M81,1)="-",-1,0))>0,1,0)))))
P81	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N81,Validation!$A$54:$B$69,2),HLOOKUP(K81,Validation!$D$51:$AD$52,2)))
U81	1	= ISERROR(VLOOKUP(LEFT(T81,LEN(T81)-IF(OR(RIGHT(T81)="-",RIGHT(T81)="+"),1,0)),IF(LEFT(Worksheet!S81,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J82	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G82)=0,LEN(H82)=0,LEN(I82)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G82,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H82),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I82,1)))))
O82	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L82)=0,LEN(M82)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L82),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M82,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L82,1)="+",1,IF(RIGHT(Worksheet!L82,1)="-",-1,0))+IF(RIGHT(Worksheet!M82,1)="+",1,IF(RIGHT(Worksheet!M82,1)="-",-1,0))>0,1,0)))))
P82	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N82,Validation!$A$54:$B$69,2),HLOOKUP(K82,Validation!$D$51:$AD$52,2)))
U82	1	= ISERROR(VLOOKUP(LEFT(T82,LEN(T82)-IF(OR(RIGHT(T82)="-",RIGHT(T82)="+"),1,0)),IF(LEFT(Worksheet!S82,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J83	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G83)=0,LEN(H83)=0,LEN(I83)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G83,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H83),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I83,1)))))
O83	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L83)=0,LEN(M83)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L83),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M83,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L83,1)="+",1,IF(RIGHT(Worksheet!L83,1)="-",-1,0))+IF(RIGHT(Worksheet!M83,1)="+",1,IF(RIGHT(Worksheet!M83,1)="-",-1,0))>0,1,0)))))
P83	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N83,Validation!$A$54:$B$69,2),HLOOKUP(K83,Validation!$D$51:$AD$52,2)))
U83	1	= ISERROR(VLOOKUP(LEFT(T83,LEN(T83)-IF(OR(RIGHT(T83)="-",RIGHT(T83)="+"),1,0)),IF(LEFT(Worksheet!S83,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J84	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G84)=0,LEN(H84)=0,LEN(I84)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G84,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H84),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I84,1)))))
O84	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L84)=0,LEN(M84)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L84),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M84,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L84,1)="+",1,IF(RIGHT(Worksheet!L84,1)="-",-1,0))+IF(RIGHT(Worksheet!M84,1)="+",1,IF(RIGHT(Worksheet!M84,1)="-",-1,0))>0,1,0)))))
P84	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N84,Validation!$A$54:$B$69,2),HLOOKUP(K84,Validation!$D$51:$AD$52,2)))
U84	1	= ISERROR(VLOOKUP(LEFT(T84,LEN(T84)-IF(OR(RIGHT(T84)="-",RIGHT(T84)="+"),1,0)),IF(LEFT(Worksheet!S84,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J85	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G85)=0,LEN(H85)=0,LEN(I85)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G85,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H85),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I85,1)))))
O85	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L85)=0,LEN(M85)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L85),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M85,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L85,1)="+",1,IF(RIGHT(Worksheet!L85,1)="-",-1,0))+IF(RIGHT(Worksheet!M85,1)="+",1,IF(RIGHT(Worksheet!M85,1)="-",-1,0))>0,1,0)))))
P85	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N85,Validation!$A$54:$B$69,2),HLOOKUP(K85,Validation!$D$51:$AD$52,2)))
U85	1	= ISERROR(VLOOKUP(LEFT(T85,LEN(T85)-IF(OR(RIGHT(T85)="-",RIGHT(T85)="+"),1,0)),IF(LEFT(Worksheet!S85,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J86	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G86)=0,LEN(H86)=0,LEN(I86)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G86,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H86),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I86,1)))))
O86	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L86)=0,LEN(M86)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L86),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M86,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L86,1)="+",1,IF(RIGHT(Worksheet!L86,1)="-",-1,0))+IF(RIGHT(Worksheet!M86,1)="+",1,IF(RIGHT(Worksheet!M86,1)="-",-1,0))>0,1,0)))))
P86	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N86,Validation!$A$54:$B$69,2),HLOOKUP(K86,Validation!$D$51:$AD$52,2)))
U86	1	= ISERROR(VLOOKUP(LEFT(T86,LEN(T86)-IF(OR(RIGHT(T86)="-",RIGHT(T86)="+"),1,0)),IF(LEFT(Worksheet!S86,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J87	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G87)=0,LEN(H87)=0,LEN(I87)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G87,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H87),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I87,1)))))
O87	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L87)=0,LEN(M87)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L87),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M87,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L87,1)="+",1,IF(RIGHT(Worksheet!L87,1)="-",-1,0))+IF(RIGHT(Worksheet!M87,1)="+",1,IF(RIGHT(Worksheet!M87,1)="-",-1,0))>0,1,0)))))
P87	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N87,Validation!$A$54:$B$69,2),HLOOKUP(K87,Validation!$D$51:$AD$52,2)))
U87	1	= ISERROR(VLOOKUP(LEFT(T87,LEN(T87)-IF(OR(RIGHT(T87)="-",RIGHT(T87)="+"),1,0)),IF(LEFT(Worksheet!S87,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J88	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G88)=0,LEN(H88)=0,LEN(I88)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G88,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H88),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I88,1)))))
O88	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L88)=0,LEN(M88)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L88),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M88,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L88,1)="+",1,IF(RIGHT(Worksheet!L88,1)="-",-1,0))+IF(RIGHT(Worksheet!M88,1)="+",1,IF(RIGHT(Worksheet!M88,1)="-",-1,0))>0,1,0)))))
P88	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N88,Validation!$A$54:$B$69,2),HLOOKUP(K88,Validation!$D$51:$AD$52,2)))
U88	1	= ISERROR(VLOOKUP(LEFT(T88,LEN(T88)-IF(OR(RIGHT(T88)="-",RIGHT(T88)="+"),1,0)),IF(LEFT(Worksheet!S88,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J89	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G89)=0,LEN(H89)=0,LEN(I89)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G89,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H89),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I89,1)))))
O89	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L89)=0,LEN(M89)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L89),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M89,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L89,1)="+",1,IF(RIGHT(Worksheet!L89,1)="-",-1,0))+IF(RIGHT(Worksheet!M89,1)="+",1,IF(RIGHT(Worksheet!M89,1)="-",-1,0))>0,1,0)))))
P89	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N89,Validation!$A$54:$B$69,2),HLOOKUP(K89,Validation!$D$51:$AD$52,2)))
U89	1	= ISERROR(VLOOKUP(LEFT(T89,LEN(T89)-IF(OR(RIGHT(T89)="-",RIGHT(T89)="+"),1,0)),IF(LEFT(Worksheet!S89,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J90	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G90)=0,LEN(H90)=0,LEN(I90)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G90,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H90),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I90,1)))))
O90	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L90)=0,LEN(M90)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L90),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M90,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L90,1)="+",1,IF(RIGHT(Worksheet!L90,1)="-",-1,0))+IF(RIGHT(Worksheet!M90,1)="+",1,IF(RIGHT(Worksheet!M90,1)="-",-1,0))>0,1,0)))))
P90	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N90,Validation!$A$54:$B$69,2),HLOOKUP(K90,Validation!$D$51:$AD$52,2)))
U90	1	= ISERROR(VLOOKUP(LEFT(T90,LEN(T90)-IF(OR(RIGHT(T90)="-",RIGHT(T90)="+"),1,0)),IF(LEFT(Worksheet!S90,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J91	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G91)=0,LEN(H91)=0,LEN(I91)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G91,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H91),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I91,1)))))
O91	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L91)=0,LEN(M91)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L91),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M91,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L91,1)="+",1,IF(RIGHT(Worksheet!L91,1)="-",-1,0))+IF(RIGHT(Worksheet!M91,1)="+",1,IF(RIGHT(Worksheet!M91,1)="-",-1,0))>0,1,0)))))
P91	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N91,Validation!$A$54:$B$69,2),HLOOKUP(K91,Validation!$D$51:$AD$52,2)))
U91	1	= ISERROR(VLOOKUP(LEFT(T91,LEN(T91)-IF(OR(RIGHT(T91)="-",RIGHT(T91)="+"),1,0)),IF(LEFT(Worksheet!S91,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J92	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G92)=0,LEN(H92)=0,LEN(I92)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G92,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H92),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I92,1)))))
O92	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L92)=0,LEN(M92)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L92),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M92,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L92,1)="+",1,IF(RIGHT(Worksheet!L92,1)="-",-1,0))+IF(RIGHT(Worksheet!M92,1)="+",1,IF(RIGHT(Worksheet!M92,1)="-",-1,0))>0,1,0)))))
P92	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N92,Validation!$A$54:$B$69,2),HLOOKUP(K92,Validation!$D$51:$AD$52,2)))
U92	1	= ISERROR(VLOOKUP(LEFT(T92,LEN(T92)-IF(OR(RIGHT(T92)="-",RIGHT(T92)="+"),1,0)),IF(LEFT(Worksheet!S92,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J93	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G93)=0,LEN(H93)=0,LEN(I93)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G93,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H93),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I93,1)))))
O93	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L93)=0,LEN(M93)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L93),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M93,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L93,1)="+",1,IF(RIGHT(Worksheet!L93,1)="-",-1,0))+IF(RIGHT(Worksheet!M93,1)="+",1,IF(RIGHT(Worksheet!M93,1)="-",-1,0))>0,1,0)))))
P93	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N93,Validation!$A$54:$B$69,2),HLOOKUP(K93,Validation!$D$51:$AD$52,2)))
U93	1	= ISERROR(VLOOKUP(LEFT(T93,LEN(T93)-IF(OR(RIGHT(T93)="-",RIGHT(T93)="+"),1,0)),IF(LEFT(Worksheet!S93,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J94	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G94)=0,LEN(H94)=0,LEN(I94)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G94,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H94),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I94,1)))))
O94	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L94)=0,LEN(M94)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L94),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M94,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L94,1)="+",1,IF(RIGHT(Worksheet!L94,1)="-",-1,0))+IF(RIGHT(Worksheet!M94,1)="+",1,IF(RIGHT(Worksheet!M94,1)="-",-1,0))>0,1,0)))))
P94	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N94,Validation!$A$54:$B$69,2),HLOOKUP(K94,Validation!$D$51:$AD$52,2)))
U94	1	= ISERROR(VLOOKUP(LEFT(T94,LEN(T94)-IF(OR(RIGHT(T94)="-",RIGHT(T94)="+"),1,0)),IF(LEFT(Worksheet!S94,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J95	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G95)=0,LEN(H95)=0,LEN(I95)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G95,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H95),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I95,1)))))
O95	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L95)=0,LEN(M95)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L95),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M95,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L95,1)="+",1,IF(RIGHT(Worksheet!L95,1)="-",-1,0))+IF(RIGHT(Worksheet!M95,1)="+",1,IF(RIGHT(Worksheet!M95,1)="-",-1,0))>0,1,0)))))
P95	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N95,Validation!$A$54:$B$69,2),HLOOKUP(K95,Validation!$D$51:$AD$52,2)))
U95	1	= ISERROR(VLOOKUP(LEFT(T95,LEN(T95)-IF(OR(RIGHT(T95)="-",RIGHT(T95)="+"),1,0)),IF(LEFT(Worksheet!S95,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J96	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G96)=0,LEN(H96)=0,LEN(I96)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G96,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H96),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I96,1)))))
O96	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L96)=0,LEN(M96)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L96),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M96,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L96,1)="+",1,IF(RIGHT(Worksheet!L96,1)="-",-1,0))+IF(RIGHT(Worksheet!M96,1)="+",1,IF(RIGHT(Worksheet!M96,1)="-",-1,0))>0,1,0)))))
P96	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N96,Validation!$A$54:$B$69,2),HLOOKUP(K96,Validation!$D$51:$AD$52,2)))
U96	1	= ISERROR(VLOOKUP(LEFT(T96,LEN(T96)-IF(OR(RIGHT(T96)="-",RIGHT(T96)="+"),1,0)),IF(LEFT(Worksheet!S96,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J97	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G97)=0,LEN(H97)=0,LEN(I97)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G97,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H97),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I97,1)))))
O97	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L97)=0,LEN(M97)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L97),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M97,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L97,1)="+",1,IF(RIGHT(Worksheet!L97,1)="-",-1,0))+IF(RIGHT(Worksheet!M97,1)="+",1,IF(RIGHT(Worksheet!M97,1)="-",-1,0))>0,1,0)))))
P97	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N97,Validation!$A$54:$B$69,2),HLOOKUP(K97,Validation!$D$51:$AD$52,2)))
U97	1	= ISERROR(VLOOKUP(LEFT(T97,LEN(T97)-IF(OR(RIGHT(T97)="-",RIGHT(T97)="+"),1,0)),IF(LEFT(Worksheet!S97,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J98	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G98)=0,LEN(H98)=0,LEN(I98)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G98,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H98),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I98,1)))))
O98	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L98)=0,LEN(M98)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L98),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M98,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L98,1)="+",1,IF(RIGHT(Worksheet!L98,1)="-",-1,0))+IF(RIGHT(Worksheet!M98,1)="+",1,IF(RIGHT(Worksheet!M98,1)="-",-1,0))>0,1,0)))))
P98	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N98,Validation!$A$54:$B$69,2),HLOOKUP(K98,Validation!$D$51:$AD$52,2)))
U98	1	= ISERROR(VLOOKUP(LEFT(T98,LEN(T98)-IF(OR(RIGHT(T98)="-",RIGHT(T98)="+"),1,0)),IF(LEFT(Worksheet!S98,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J99	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G99)=0,LEN(H99)=0,LEN(I99)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G99,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H99),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I99,1)))))
O99	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L99)=0,LEN(M99)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L99),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M99,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L99,1)="+",1,IF(RIGHT(Worksheet!L99,1)="-",-1,0))+IF(RIGHT(Worksheet!M99,1)="+",1,IF(RIGHT(Worksheet!M99,1)="-",-1,0))>0,1,0)))))
P99	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N99,Validation!$A$54:$B$69,2),HLOOKUP(K99,Validation!$D$51:$AD$52,2)))
U99	1	= ISERROR(VLOOKUP(LEFT(T99,LEN(T99)-IF(OR(RIGHT(T99)="-",RIGHT(T99)="+"),1,0)),IF(LEFT(Worksheet!S99,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J100	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G100)=0,LEN(H100)=0,LEN(I100)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G100,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H100),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I100,1)))))
O100	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L100)=0,LEN(M100)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L100),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M100,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L100,1)="+",1,IF(RIGHT(Worksheet!L100,1)="-",-1,0))+IF(RIGHT(Worksheet!M100,1)="+",1,IF(RIGHT(Worksheet!M100,1)="-",-1,0))>0,1,0)))))
P100	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N100,Validation!$A$54:$B$69,2),HLOOKUP(K100,Validation!$D$51:$AD$52,2)))
U100	1	= ISERROR(VLOOKUP(LEFT(T100,LEN(T100)-IF(OR(RIGHT(T100)="-",RIGHT(T100)="+"),1,0)),IF(LEFT(Worksheet!S100,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J101	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G101)=0,LEN(H101)=0,LEN(I101)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G101,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H101),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I101,1)))))
O101	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L101)=0,LEN(M101)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L101),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M101,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L101,1)="+",1,IF(RIGHT(Worksheet!L101,1)="-",-1,0))+IF(RIGHT(Worksheet!M101,1)="+",1,IF(RIGHT(Worksheet!M101,1)="-",-1,0))>0,1,0)))))
P101	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N101,Validation!$A$54:$B$69,2),HLOOKUP(K101,Validation!$D$51:$AD$52,2)))
U101	1	= ISERROR(VLOOKUP(LEFT(T101,LEN(T101)-IF(OR(RIGHT(T101)="-",RIGHT(T101)="+"),1,0)),IF(LEFT(Worksheet!S101,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J102	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G102)=0,LEN(H102)=0,LEN(I102)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G102,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H102),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I102,1)))))
O102	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L102)=0,LEN(M102)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L102),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M102,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L102,1)="+",1,IF(RIGHT(Worksheet!L102,1)="-",-1,0))+IF(RIGHT(Worksheet!M102,1)="+",1,IF(RIGHT(Worksheet!M102,1)="-",-1,0))>0,1,0)))))
P102	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N102,Validation!$A$54:$B$69,2),HLOOKUP(K102,Validation!$D$51:$AD$52,2)))
U102	1	= ISERROR(VLOOKUP(LEFT(T102,LEN(T102)-IF(OR(RIGHT(T102)="-",RIGHT(T102)="+"),1,0)),IF(LEFT(Worksheet!S102,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J103	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G103)=0,LEN(H103)=0,LEN(I103)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G103,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H103),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I103,1)))))
O103	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L103)=0,LEN(M103)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L103),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M103,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L103,1)="+",1,IF(RIGHT(Worksheet!L103,1)="-",-1,0))+IF(RIGHT(Worksheet!M103,1)="+",1,IF(RIGHT(Worksheet!M103,1)="-",-1,0))>0,1,0)))))
P103	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N103,Validation!$A$54:$B$69,2),HLOOKUP(K103,Validation!$D$51:$AD$52,2)))
U103	1	= ISERROR(VLOOKUP(LEFT(T103,LEN(T103)-IF(OR(RIGHT(T103)="-",RIGHT(T103)="+"),1,0)),IF(LEFT(Worksheet!S103,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J104	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G104)=0,LEN(H104)=0,LEN(I104)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G104,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H104),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I104,1)))))
O104	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L104)=0,LEN(M104)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L104),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M104,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L104,1)="+",1,IF(RIGHT(Worksheet!L104,1)="-",-1,0))+IF(RIGHT(Worksheet!M104,1)="+",1,IF(RIGHT(Worksheet!M104,1)="-",-1,0))>0,1,0)))))
P104	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N104,Validation!$A$54:$B$69,2),HLOOKUP(K104,Validation!$D$51:$AD$52,2)))
U104	1	= ISERROR(VLOOKUP(LEFT(T104,LEN(T104)-IF(OR(RIGHT(T104)="-",RIGHT(T104)="+"),1,0)),IF(LEFT(Worksheet!S104,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J105	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G105)=0,LEN(H105)=0,LEN(I105)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G105,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H105),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I105,1)))))
O105	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L105)=0,LEN(M105)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L105),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M105,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L105,1)="+",1,IF(RIGHT(Worksheet!L105,1)="-",-1,0))+IF(RIGHT(Worksheet!M105,1)="+",1,IF(RIGHT(Worksheet!M105,1)="-",-1,0))>0,1,0)))))
P105	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N105,Validation!$A$54:$B$69,2),HLOOKUP(K105,Validation!$D$51:$AD$52,2)))
U105	1	= ISERROR(VLOOKUP(LEFT(T105,LEN(T105)-IF(OR(RIGHT(T105)="-",RIGHT(T105)="+"),1,0)),IF(LEFT(Worksheet!S105,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J106	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G106)=0,LEN(H106)=0,LEN(I106)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G106,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H106),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I106,1)))))
O106	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L106)=0,LEN(M106)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L106),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M106,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L106,1)="+",1,IF(RIGHT(Worksheet!L106,1)="-",-1,0))+IF(RIGHT(Worksheet!M106,1)="+",1,IF(RIGHT(Worksheet!M106,1)="-",-1,0))>0,1,0)))))
P106	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N106,Validation!$A$54:$B$69,2),HLOOKUP(K106,Validation!$D$51:$AD$52,2)))
U106	1	= ISERROR(VLOOKUP(LEFT(T106,LEN(T106)-IF(OR(RIGHT(T106)="-",RIGHT(T106)="+"),1,0)),IF(LEFT(Worksheet!S106,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J107	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G107)=0,LEN(H107)=0,LEN(I107)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G107,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H107),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I107,1)))))
O107	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L107)=0,LEN(M107)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L107),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M107,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L107,1)="+",1,IF(RIGHT(Worksheet!L107,1)="-",-1,0))+IF(RIGHT(Worksheet!M107,1)="+",1,IF(RIGHT(Worksheet!M107,1)="-",-1,0))>0,1,0)))))
P107	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N107,Validation!$A$54:$B$69,2),HLOOKUP(K107,Validation!$D$51:$AD$52,2)))
U107	1	= ISERROR(VLOOKUP(LEFT(T107,LEN(T107)-IF(OR(RIGHT(T107)="-",RIGHT(T107)="+"),1,0)),IF(LEFT(Worksheet!S107,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J108	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G108)=0,LEN(H108)=0,LEN(I108)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G108,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H108),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I108,1)))))
O108	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L108)=0,LEN(M108)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L108),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M108,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L108,1)="+",1,IF(RIGHT(Worksheet!L108,1)="-",-1,0))+IF(RIGHT(Worksheet!M108,1)="+",1,IF(RIGHT(Worksheet!M108,1)="-",-1,0))>0,1,0)))))
P108	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N108,Validation!$A$54:$B$69,2),HLOOKUP(K108,Validation!$D$51:$AD$52,2)))
U108	1	= ISERROR(VLOOKUP(LEFT(T108,LEN(T108)-IF(OR(RIGHT(T108)="-",RIGHT(T108)="+"),1,0)),IF(LEFT(Worksheet!S108,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J109	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G109)=0,LEN(H109)=0,LEN(I109)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G109,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H109),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I109,1)))))
O109	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L109)=0,LEN(M109)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L109),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M109,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L109,1)="+",1,IF(RIGHT(Worksheet!L109,1)="-",-1,0))+IF(RIGHT(Worksheet!M109,1)="+",1,IF(RIGHT(Worksheet!M109,1)="-",-1,0))>0,1,0)))))
P109	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N109,Validation!$A$54:$B$69,2),HLOOKUP(K109,Validation!$D$51:$AD$52,2)))
U109	1	= ISERROR(VLOOKUP(LEFT(T109,LEN(T109)-IF(OR(RIGHT(T109)="-",RIGHT(T109)="+"),1,0)),IF(LEFT(Worksheet!S109,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J110	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G110)=0,LEN(H110)=0,LEN(I110)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G110,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H110),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I110,1)))))
O110	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L110)=0,LEN(M110)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L110),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M110,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L110,1)="+",1,IF(RIGHT(Worksheet!L110,1)="-",-1,0))+IF(RIGHT(Worksheet!M110,1)="+",1,IF(RIGHT(Worksheet!M110,1)="-",-1,0))>0,1,0)))))
P110	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N110,Validation!$A$54:$B$69,2),HLOOKUP(K110,Validation!$D$51:$AD$52,2)))
U110	1	= ISERROR(VLOOKUP(LEFT(T110,LEN(T110)-IF(OR(RIGHT(T110)="-",RIGHT(T110)="+"),1,0)),IF(LEFT(Worksheet!S110,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J111	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G111)=0,LEN(H111)=0,LEN(I111)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G111,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H111),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I111,1)))))
O111	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L111)=0,LEN(M111)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L111),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M111,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L111,1)="+",1,IF(RIGHT(Worksheet!L111,1)="-",-1,0))+IF(RIGHT(Worksheet!M111,1)="+",1,IF(RIGHT(Worksheet!M111,1)="-",-1,0))>0,1,0)))))
P111	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N111,Validation!$A$54:$B$69,2),HLOOKUP(K111,Validation!$D$51:$AD$52,2)))
U111	1	= ISERROR(VLOOKUP(LEFT(T111,LEN(T111)-IF(OR(RIGHT(T111)="-",RIGHT(T111)="+"),1,0)),IF(LEFT(Worksheet!S111,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J112	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G112)=0,LEN(H112)=0,LEN(I112)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G112,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H112),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I112,1)))))
O112	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L112)=0,LEN(M112)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L112),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M112,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L112,1)="+",1,IF(RIGHT(Worksheet!L112,1)="-",-1,0))+IF(RIGHT(Worksheet!M112,1)="+",1,IF(RIGHT(Worksheet!M112,1)="-",-1,0))>0,1,0)))))
P112	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N112,Validation!$A$54:$B$69,2),HLOOKUP(K112,Validation!$D$51:$AD$52,2)))
U112	1	= ISERROR(VLOOKUP(LEFT(T112,LEN(T112)-IF(OR(RIGHT(T112)="-",RIGHT(T112)="+"),1,0)),IF(LEFT(Worksheet!S112,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J113	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G113)=0,LEN(H113)=0,LEN(I113)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G113,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H113),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I113,1)))))
O113	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L113)=0,LEN(M113)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L113),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M113,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L113,1)="+",1,IF(RIGHT(Worksheet!L113,1)="-",-1,0))+IF(RIGHT(Worksheet!M113,1)="+",1,IF(RIGHT(Worksheet!M113,1)="-",-1,0))>0,1,0)))))
P113	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N113,Validation!$A$54:$B$69,2),HLOOKUP(K113,Validation!$D$51:$AD$52,2)))
U113	1	= ISERROR(VLOOKUP(LEFT(T113,LEN(T113)-IF(OR(RIGHT(T113)="-",RIGHT(T113)="+"),1,0)),IF(LEFT(Worksheet!S113,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J114	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G114)=0,LEN(H114)=0,LEN(I114)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G114,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H114),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I114,1)))))
O114	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L114)=0,LEN(M114)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L114),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M114,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L114,1)="+",1,IF(RIGHT(Worksheet!L114,1)="-",-1,0))+IF(RIGHT(Worksheet!M114,1)="+",1,IF(RIGHT(Worksheet!M114,1)="-",-1,0))>0,1,0)))))
P114	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N114,Validation!$A$54:$B$69,2),HLOOKUP(K114,Validation!$D$51:$AD$52,2)))
U114	1	= ISERROR(VLOOKUP(LEFT(T114,LEN(T114)-IF(OR(RIGHT(T114)="-",RIGHT(T114)="+"),1,0)),IF(LEFT(Worksheet!S114,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J115	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G115)=0,LEN(H115)=0,LEN(I115)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G115,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H115),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I115,1)))))
O115	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L115)=0,LEN(M115)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L115),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M115,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L115,1)="+",1,IF(RIGHT(Worksheet!L115,1)="-",-1,0))+IF(RIGHT(Worksheet!M115,1)="+",1,IF(RIGHT(Worksheet!M115,1)="-",-1,0))>0,1,0)))))
P115	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N115,Validation!$A$54:$B$69,2),HLOOKUP(K115,Validation!$D$51:$AD$52,2)))
U115	1	= ISERROR(VLOOKUP(LEFT(T115,LEN(T115)-IF(OR(RIGHT(T115)="-",RIGHT(T115)="+"),1,0)),IF(LEFT(Worksheet!S115,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J116	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G116)=0,LEN(H116)=0,LEN(I116)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G116,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H116),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I116,1)))))
O116	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L116)=0,LEN(M116)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L116),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M116,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L116,1)="+",1,IF(RIGHT(Worksheet!L116,1)="-",-1,0))+IF(RIGHT(Worksheet!M116,1)="+",1,IF(RIGHT(Worksheet!M116,1)="-",-1,0))>0,1,0)))))
P116	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N116,Validation!$A$54:$B$69,2),HLOOKUP(K116,Validation!$D$51:$AD$52,2)))
U116	1	= ISERROR(VLOOKUP(LEFT(T116,LEN(T116)-IF(OR(RIGHT(T116)="-",RIGHT(T116)="+"),1,0)),IF(LEFT(Worksheet!S116,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J117	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G117)=0,LEN(H117)=0,LEN(I117)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G117,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H117),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I117,1)))))
O117	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L117)=0,LEN(M117)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L117),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M117,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L117,1)="+",1,IF(RIGHT(Worksheet!L117,1)="-",-1,0))+IF(RIGHT(Worksheet!M117,1)="+",1,IF(RIGHT(Worksheet!M117,1)="-",-1,0))>0,1,0)))))
P117	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N117,Validation!$A$54:$B$69,2),HLOOKUP(K117,Validation!$D$51:$AD$52,2)))
U117	1	= ISERROR(VLOOKUP(LEFT(T117,LEN(T117)-IF(OR(RIGHT(T117)="-",RIGHT(T117)="+"),1,0)),IF(LEFT(Worksheet!S117,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J118	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G118)=0,LEN(H118)=0,LEN(I118)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G118,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H118),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I118,1)))))
O118	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L118)=0,LEN(M118)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L118),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M118,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L118,1)="+",1,IF(RIGHT(Worksheet!L118,1)="-",-1,0))+IF(RIGHT(Worksheet!M118,1)="+",1,IF(RIGHT(Worksheet!M118,1)="-",-1,0))>0,1,0)))))
P118	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N118,Validation!$A$54:$B$69,2),HLOOKUP(K118,Validation!$D$51:$AD$52,2)))
U118	1	= ISERROR(VLOOKUP(LEFT(T118,LEN(T118)-IF(OR(RIGHT(T118)="-",RIGHT(T118)="+"),1,0)),IF(LEFT(Worksheet!S118,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J119	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G119)=0,LEN(H119)=0,LEN(I119)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G119,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H119),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I119,1)))))
O119	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L119)=0,LEN(M119)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L119),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M119,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L119,1)="+",1,IF(RIGHT(Worksheet!L119,1)="-",-1,0))+IF(RIGHT(Worksheet!M119,1)="+",1,IF(RIGHT(Worksheet!M119,1)="-",-1,0))>0,1,0)))))
P119	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N119,Validation!$A$54:$B$69,2),HLOOKUP(K119,Validation!$D$51:$AD$52,2)))
U119	1	= ISERROR(VLOOKUP(LEFT(T119,LEN(T119)-IF(OR(RIGHT(T119)="-",RIGHT(T119)="+"),1,0)),IF(LEFT(Worksheet!S119,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J120	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G120)=0,LEN(H120)=0,LEN(I120)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G120,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H120),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I120,1)))))
O120	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L120)=0,LEN(M120)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L120),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M120,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L120,1)="+",1,IF(RIGHT(Worksheet!L120,1)="-",-1,0))+IF(RIGHT(Worksheet!M120,1)="+",1,IF(RIGHT(Worksheet!M120,1)="-",-1,0))>0,1,0)))))
P120	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N120,Validation!$A$54:$B$69,2),HLOOKUP(K120,Validation!$D$51:$AD$52,2)))
U120	1	= ISERROR(VLOOKUP(LEFT(T120,LEN(T120)-IF(OR(RIGHT(T120)="-",RIGHT(T120)="+"),1,0)),IF(LEFT(Worksheet!S120,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J121	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G121)=0,LEN(H121)=0,LEN(I121)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G121,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H121),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I121,1)))))
O121	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L121)=0,LEN(M121)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L121),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M121,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L121,1)="+",1,IF(RIGHT(Worksheet!L121,1)="-",-1,0))+IF(RIGHT(Worksheet!M121,1)="+",1,IF(RIGHT(Worksheet!M121,1)="-",-1,0))>0,1,0)))))
P121	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N121,Validation!$A$54:$B$69,2),HLOOKUP(K121,Validation!$D$51:$AD$52,2)))
U121	1	= ISERROR(VLOOKUP(LEFT(T121,LEN(T121)-IF(OR(RIGHT(T121)="-",RIGHT(T121)="+"),1,0)),IF(LEFT(Worksheet!S121,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J122	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G122)=0,LEN(H122)=0,LEN(I122)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G122,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H122),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I122,1)))))
O122	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L122)=0,LEN(M122)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L122),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M122,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L122,1)="+",1,IF(RIGHT(Worksheet!L122,1)="-",-1,0))+IF(RIGHT(Worksheet!M122,1)="+",1,IF(RIGHT(Worksheet!M122,1)="-",-1,0))>0,1,0)))))
P122	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N122,Validation!$A$54:$B$69,2),HLOOKUP(K122,Validation!$D$51:$AD$52,2)))
U122	1	= ISERROR(VLOOKUP(LEFT(T122,LEN(T122)-IF(OR(RIGHT(T122)="-",RIGHT(T122)="+"),1,0)),IF(LEFT(Worksheet!S122,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J123	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G123)=0,LEN(H123)=0,LEN(I123)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G123,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H123),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I123,1)))))
O123	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L123)=0,LEN(M123)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L123),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M123,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L123,1)="+",1,IF(RIGHT(Worksheet!L123,1)="-",-1,0))+IF(RIGHT(Worksheet!M123,1)="+",1,IF(RIGHT(Worksheet!M123,1)="-",-1,0))>0,1,0)))))
P123	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N123,Validation!$A$54:$B$69,2),HLOOKUP(K123,Validation!$D$51:$AD$52,2)))
U123	1	= ISERROR(VLOOKUP(LEFT(T123,LEN(T123)-IF(OR(RIGHT(T123)="-",RIGHT(T123)="+"),1,0)),IF(LEFT(Worksheet!S123,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J124	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G124)=0,LEN(H124)=0,LEN(I124)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G124,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H124),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I124,1)))))
O124	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L124)=0,LEN(M124)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L124),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M124,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L124,1)="+",1,IF(RIGHT(Worksheet!L124,1)="-",-1,0))+IF(RIGHT(Worksheet!M124,1)="+",1,IF(RIGHT(Worksheet!M124,1)="-",-1,0))>0,1,0)))))
P124	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N124,Validation!$A$54:$B$69,2),HLOOKUP(K124,Validation!$D$51:$AD$52,2)))
U124	1	= ISERROR(VLOOKUP(LEFT(T124,LEN(T124)-IF(OR(RIGHT(T124)="-",RIGHT(T124)="+"),1,0)),IF(LEFT(Worksheet!S124,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J125	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G125)=0,LEN(H125)=0,LEN(I125)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G125,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H125),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I125,1)))))
O125	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L125)=0,LEN(M125)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L125),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M125,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L125,1)="+",1,IF(RIGHT(Worksheet!L125,1)="-",-1,0))+IF(RIGHT(Worksheet!M125,1)="+",1,IF(RIGHT(Worksheet!M125,1)="-",-1,0))>0,1,0)))))
P125	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N125,Validation!$A$54:$B$69,2),HLOOKUP(K125,Validation!$D$51:$AD$52,2)))
U125	1	= ISERROR(VLOOKUP(LEFT(T125,LEN(T125)-IF(OR(RIGHT(T125)="-",RIGHT(T125)="+"),1,0)),IF(LEFT(Worksheet!S125,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J126	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G126)=0,LEN(H126)=0,LEN(I126)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G126,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H126),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I126,1)))))
O126	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L126)=0,LEN(M126)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L126),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M126,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L126,1)="+",1,IF(RIGHT(Worksheet!L126,1)="-",-1,0))+IF(RIGHT(Worksheet!M126,1)="+",1,IF(RIGHT(Worksheet!M126,1)="-",-1,0))>0,1,0)))))
P126	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N126,Validation!$A$54:$B$69,2),HLOOKUP(K126,Validation!$D$51:$AD$52,2)))
U126	1	= ISERROR(VLOOKUP(LEFT(T126,LEN(T126)-IF(OR(RIGHT(T126)="-",RIGHT(T126)="+"),1,0)),IF(LEFT(Worksheet!S126,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J127	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G127)=0,LEN(H127)=0,LEN(I127)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G127,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H127),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I127,1)))))
O127	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L127)=0,LEN(M127)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L127),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M127,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L127,1)="+",1,IF(RIGHT(Worksheet!L127,1)="-",-1,0))+IF(RIGHT(Worksheet!M127,1)="+",1,IF(RIGHT(Worksheet!M127,1)="-",-1,0))>0,1,0)))))
P127	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N127,Validation!$A$54:$B$69,2),HLOOKUP(K127,Validation!$D$51:$AD$52,2)))
U127	1	= ISERROR(VLOOKUP(LEFT(T127,LEN(T127)-IF(OR(RIGHT(T127)="-",RIGHT(T127)="+"),1,0)),IF(LEFT(Worksheet!S127,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J128	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G128)=0,LEN(H128)=0,LEN(I128)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G128,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H128),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I128,1)))))
O128	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L128)=0,LEN(M128)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L128),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M128,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L128,1)="+",1,IF(RIGHT(Worksheet!L128,1)="-",-1,0))+IF(RIGHT(Worksheet!M128,1)="+",1,IF(RIGHT(Worksheet!M128,1)="-",-1,0))>0,1,0)))))
P128	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N128,Validation!$A$54:$B$69,2),HLOOKUP(K128,Validation!$D$51:$AD$52,2)))
U128	1	= ISERROR(VLOOKUP(LEFT(T128,LEN(T128)-IF(OR(RIGHT(T128)="-",RIGHT(T128)="+"),1,0)),IF(LEFT(Worksheet!S128,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J129	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G129)=0,LEN(H129)=0,LEN(I129)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G129,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H129),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I129,1)))))
O129	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L129)=0,LEN(M129)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L129),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M129,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L129,1)="+",1,IF(RIGHT(Worksheet!L129,1)="-",-1,0))+IF(RIGHT(Worksheet!M129,1)="+",1,IF(RIGHT(Worksheet!M129,1)="-",-1,0))>0,1,0)))))
P129	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N129,Validation!$A$54:$B$69,2),HLOOKUP(K129,Validation!$D$51:$AD$52,2)))
U129	1	= ISERROR(VLOOKUP(LEFT(T129,LEN(T129)-IF(OR(RIGHT(T129)="-",RIGHT(T129)="+"),1,0)),IF(LEFT(Worksheet!S129,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J130	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G130)=0,LEN(H130)=0,LEN(I130)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G130,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H130),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I130,1)))))
O130	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L130)=0,LEN(M130)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L130),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M130,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L130,1)="+",1,IF(RIGHT(Worksheet!L130,1)="-",-1,0))+IF(RIGHT(Worksheet!M130,1)="+",1,IF(RIGHT(Worksheet!M130,1)="-",-1,0))>0,1,0)))))
P130	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N130,Validation!$A$54:$B$69,2),HLOOKUP(K130,Validation!$D$51:$AD$52,2)))
U130	1	= ISERROR(VLOOKUP(LEFT(T130,LEN(T130)-IF(OR(RIGHT(T130)="-",RIGHT(T130)="+"),1,0)),IF(LEFT(Worksheet!S130,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J131	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G131)=0,LEN(H131)=0,LEN(I131)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G131,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H131),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I131,1)))))
O131	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L131)=0,LEN(M131)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L131),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M131,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L131,1)="+",1,IF(RIGHT(Worksheet!L131,1)="-",-1,0))+IF(RIGHT(Worksheet!M131,1)="+",1,IF(RIGHT(Worksheet!M131,1)="-",-1,0))>0,1,0)))))
P131	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N131,Validation!$A$54:$B$69,2),HLOOKUP(K131,Validation!$D$51:$AD$52,2)))
U131	1	= ISERROR(VLOOKUP(LEFT(T131,LEN(T131)-IF(OR(RIGHT(T131)="-",RIGHT(T131)="+"),1,0)),IF(LEFT(Worksheet!S131,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J132	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G132)=0,LEN(H132)=0,LEN(I132)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G132,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H132),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I132,1)))))
O132	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L132)=0,LEN(M132)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L132),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M132,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L132,1)="+",1,IF(RIGHT(Worksheet!L132,1)="-",-1,0))+IF(RIGHT(Worksheet!M132,1)="+",1,IF(RIGHT(Worksheet!M132,1)="-",-1,0))>0,1,0)))))
P132	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N132,Validation!$A$54:$B$69,2),HLOOKUP(K132,Validation!$D$51:$AD$52,2)))
U132	1	= ISERROR(VLOOKUP(LEFT(T132,LEN(T132)-IF(OR(RIGHT(T132)="-",RIGHT(T132)="+"),1,0)),IF(LEFT(Worksheet!S132,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J133	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G133)=0,LEN(H133)=0,LEN(I133)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G133,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H133),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I133,1)))))
O133	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L133)=0,LEN(M133)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L133),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M133,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L133,1)="+",1,IF(RIGHT(Worksheet!L133,1)="-",-1,0))+IF(RIGHT(Worksheet!M133,1)="+",1,IF(RIGHT(Worksheet!M133,1)="-",-1,0))>0,1,0)))))
P133	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N133,Validation!$A$54:$B$69,2),HLOOKUP(K133,Validation!$D$51:$AD$52,2)))
U133	1	= ISERROR(VLOOKUP(LEFT(T133,LEN(T133)-IF(OR(RIGHT(T133)="-",RIGHT(T133)="+"),1,0)),IF(LEFT(Worksheet!S133,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J134	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G134)=0,LEN(H134)=0,LEN(I134)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G134,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H134),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I134,1)))))
O134	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L134)=0,LEN(M134)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L134),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M134,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L134,1)="+",1,IF(RIGHT(Worksheet!L134,1)="-",-1,0))+IF(RIGHT(Worksheet!M134,1)="+",1,IF(RIGHT(Worksheet!M134,1)="-",-1,0))>0,1,0)))))
P134	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N134,Validation!$A$54:$B$69,2),HLOOKUP(K134,Validation!$D$51:$AD$52,2)))
U134	1	= ISERROR(VLOOKUP(LEFT(T134,LEN(T134)-IF(OR(RIGHT(T134)="-",RIGHT(T134)="+"),1,0)),IF(LEFT(Worksheet!S134,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J135	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G135)=0,LEN(H135)=0,LEN(I135)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G135,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H135),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I135,1)))))
O135	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L135)=0,LEN(M135)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L135),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M135,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L135,1)="+",1,IF(RIGHT(Worksheet!L135,1)="-",-1,0))+IF(RIGHT(Worksheet!M135,1)="+",1,IF(RIGHT(Worksheet!M135,1)="-",-1,0))>0,1,0)))))
P135	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N135,Validation!$A$54:$B$69,2),HLOOKUP(K135,Validation!$D$51:$AD$52,2)))
U135	1	= ISERROR(VLOOKUP(LEFT(T135,LEN(T135)-IF(OR(RIGHT(T135)="-",RIGHT(T135)="+"),1,0)),IF(LEFT(Worksheet!S135,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J136	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G136)=0,LEN(H136)=0,LEN(I136)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G136,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H136),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I136,1)))))
O136	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L136)=0,LEN(M136)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L136),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M136,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L136,1)="+",1,IF(RIGHT(Worksheet!L136,1)="-",-1,0))+IF(RIGHT(Worksheet!M136,1)="+",1,IF(RIGHT(Worksheet!M136,1)="-",-1,0))>0,1,0)))))
P136	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N136,Validation!$A$54:$B$69,2),HLOOKUP(K136,Validation!$D$51:$AD$52,2)))
U136	1	= ISERROR(VLOOKUP(LEFT(T136,LEN(T136)-IF(OR(RIGHT(T136)="-",RIGHT(T136)="+"),1,0)),IF(LEFT(Worksheet!S136,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J137	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G137)=0,LEN(H137)=0,LEN(I137)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G137,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H137),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I137,1)))))
O137	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L137)=0,LEN(M137)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L137),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M137,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L137,1)="+",1,IF(RIGHT(Worksheet!L137,1)="-",-1,0))+IF(RIGHT(Worksheet!M137,1)="+",1,IF(RIGHT(Worksheet!M137,1)="-",-1,0))>0,1,0)))))
P137	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N137,Validation!$A$54:$B$69,2),HLOOKUP(K137,Validation!$D$51:$AD$52,2)))
U137	1	= ISERROR(VLOOKUP(LEFT(T137,LEN(T137)-IF(OR(RIGHT(T137)="-",RIGHT(T137)="+"),1,0)),IF(LEFT(Worksheet!S137,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J138	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G138)=0,LEN(H138)=0,LEN(I138)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G138,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H138),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I138,1)))))
O138	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L138)=0,LEN(M138)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L138),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M138,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L138,1)="+",1,IF(RIGHT(Worksheet!L138,1)="-",-1,0))+IF(RIGHT(Worksheet!M138,1)="+",1,IF(RIGHT(Worksheet!M138,1)="-",-1,0))>0,1,0)))))
P138	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N138,Validation!$A$54:$B$69,2),HLOOKUP(K138,Validation!$D$51:$AD$52,2)))
U138	1	= ISERROR(VLOOKUP(LEFT(T138,LEN(T138)-IF(OR(RIGHT(T138)="-",RIGHT(T138)="+"),1,0)),IF(LEFT(Worksheet!S138,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J139	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G139)=0,LEN(H139)=0,LEN(I139)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G139,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H139),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I139,1)))))
O139	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L139)=0,LEN(M139)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L139),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M139,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L139,1)="+",1,IF(RIGHT(Worksheet!L139,1)="-",-1,0))+IF(RIGHT(Worksheet!M139,1)="+",1,IF(RIGHT(Worksheet!M139,1)="-",-1,0))>0,1,0)))))
P139	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N139,Validation!$A$54:$B$69,2),HLOOKUP(K139,Validation!$D$51:$AD$52,2)))
U139	1	= ISERROR(VLOOKUP(LEFT(T139,LEN(T139)-IF(OR(RIGHT(T139)="-",RIGHT(T139)="+"),1,0)),IF(LEFT(Worksheet!S139,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J140	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G140)=0,LEN(H140)=0,LEN(I140)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G140,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H140),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I140,1)))))
O140	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L140)=0,LEN(M140)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L140),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M140,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L140,1)="+",1,IF(RIGHT(Worksheet!L140,1)="-",-1,0))+IF(RIGHT(Worksheet!M140,1)="+",1,IF(RIGHT(Worksheet!M140,1)="-",-1,0))>0,1,0)))))
P140	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N140,Validation!$A$54:$B$69,2),HLOOKUP(K140,Validation!$D$51:$AD$52,2)))
U140	1	= ISERROR(VLOOKUP(LEFT(T140,LEN(T140)-IF(OR(RIGHT(T140)="-",RIGHT(T140)="+"),1,0)),IF(LEFT(Worksheet!S140,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J141	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G141)=0,LEN(H141)=0,LEN(I141)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G141,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H141),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I141,1)))))
O141	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L141)=0,LEN(M141)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L141),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M141,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L141,1)="+",1,IF(RIGHT(Worksheet!L141,1)="-",-1,0))+IF(RIGHT(Worksheet!M141,1)="+",1,IF(RIGHT(Worksheet!M141,1)="-",-1,0))>0,1,0)))))
P141	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N141,Validation!$A$54:$B$69,2),HLOOKUP(K141,Validation!$D$51:$AD$52,2)))
U141	1	= ISERROR(VLOOKUP(LEFT(T141,LEN(T141)-IF(OR(RIGHT(T141)="-",RIGHT(T141)="+"),1,0)),IF(LEFT(Worksheet!S141,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J142	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G142)=0,LEN(H142)=0,LEN(I142)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G142,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H142),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I142,1)))))
O142	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L142)=0,LEN(M142)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L142),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M142,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L142,1)="+",1,IF(RIGHT(Worksheet!L142,1)="-",-1,0))+IF(RIGHT(Worksheet!M142,1)="+",1,IF(RIGHT(Worksheet!M142,1)="-",-1,0))>0,1,0)))))
P142	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N142,Validation!$A$54:$B$69,2),HLOOKUP(K142,Validation!$D$51:$AD$52,2)))
U142	1	= ISERROR(VLOOKUP(LEFT(T142,LEN(T142)-IF(OR(RIGHT(T142)="-",RIGHT(T142)="+"),1,0)),IF(LEFT(Worksheet!S142,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J143	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G143)=0,LEN(H143)=0,LEN(I143)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G143,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H143),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I143,1)))))
O143	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L143)=0,LEN(M143)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L143),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M143,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L143,1)="+",1,IF(RIGHT(Worksheet!L143,1)="-",-1,0))+IF(RIGHT(Worksheet!M143,1)="+",1,IF(RIGHT(Worksheet!M143,1)="-",-1,0))>0,1,0)))))
P143	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N143,Validation!$A$54:$B$69,2),HLOOKUP(K143,Validation!$D$51:$AD$52,2)))
U143	1	= ISERROR(VLOOKUP(LEFT(T143,LEN(T143)-IF(OR(RIGHT(T143)="-",RIGHT(T143)="+"),1,0)),IF(LEFT(Worksheet!S143,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J144	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G144)=0,LEN(H144)=0,LEN(I144)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G144,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H144),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I144,1)))))
O144	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L144)=0,LEN(M144)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L144),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M144,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L144,1)="+",1,IF(RIGHT(Worksheet!L144,1)="-",-1,0))+IF(RIGHT(Worksheet!M144,1)="+",1,IF(RIGHT(Worksheet!M144,1)="-",-1,0))>0,1,0)))))
P144	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N144,Validation!$A$54:$B$69,2),HLOOKUP(K144,Validation!$D$51:$AD$52,2)))
U144	1	= ISERROR(VLOOKUP(LEFT(T144,LEN(T144)-IF(OR(RIGHT(T144)="-",RIGHT(T144)="+"),1,0)),IF(LEFT(Worksheet!S144,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J145	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G145)=0,LEN(H145)=0,LEN(I145)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G145,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H145),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I145,1)))))
O145	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L145)=0,LEN(M145)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L145),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M145,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L145,1)="+",1,IF(RIGHT(Worksheet!L145,1)="-",-1,0))+IF(RIGHT(Worksheet!M145,1)="+",1,IF(RIGHT(Worksheet!M145,1)="-",-1,0))>0,1,0)))))
P145	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N145,Validation!$A$54:$B$69,2),HLOOKUP(K145,Validation!$D$51:$AD$52,2)))
U145	1	= ISERROR(VLOOKUP(LEFT(T145,LEN(T145)-IF(OR(RIGHT(T145)="-",RIGHT(T145)="+"),1,0)),IF(LEFT(Worksheet!S145,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J146	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G146)=0,LEN(H146)=0,LEN(I146)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G146,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H146),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I146,1)))))
O146	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L146)=0,LEN(M146)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L146),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M146,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L146,1)="+",1,IF(RIGHT(Worksheet!L146,1)="-",-1,0))+IF(RIGHT(Worksheet!M146,1)="+",1,IF(RIGHT(Worksheet!M146,1)="-",-1,0))>0,1,0)))))
P146	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N146,Validation!$A$54:$B$69,2),HLOOKUP(K146,Validation!$D$51:$AD$52,2)))
U146	1	= ISERROR(VLOOKUP(LEFT(T146,LEN(T146)-IF(OR(RIGHT(T146)="-",RIGHT(T146)="+"),1,0)),IF(LEFT(Worksheet!S146,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J147	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G147)=0,LEN(H147)=0,LEN(I147)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G147,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H147),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I147,1)))))
O147	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L147)=0,LEN(M147)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L147),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M147,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L147,1)="+",1,IF(RIGHT(Worksheet!L147,1)="-",-1,0))+IF(RIGHT(Worksheet!M147,1)="+",1,IF(RIGHT(Worksheet!M147,1)="-",-1,0))>0,1,0)))))
P147	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N147,Validation!$A$54:$B$69,2),HLOOKUP(K147,Validation!$D$51:$AD$52,2)))
U147	1	= ISERROR(VLOOKUP(LEFT(T147,LEN(T147)-IF(OR(RIGHT(T147)="-",RIGHT(T147)="+"),1,0)),IF(LEFT(Worksheet!S147,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J148	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G148)=0,LEN(H148)=0,LEN(I148)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G148,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H148),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I148,1)))))
O148	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L148)=0,LEN(M148)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L148),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M148,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L148,1)="+",1,IF(RIGHT(Worksheet!L148,1)="-",-1,0))+IF(RIGHT(Worksheet!M148,1)="+",1,IF(RIGHT(Worksheet!M148,1)="-",-1,0))>0,1,0)))))
P148	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N148,Validation!$A$54:$B$69,2),HLOOKUP(K148,Validation!$D$51:$AD$52,2)))
U148	1	= ISERROR(VLOOKUP(LEFT(T148,LEN(T148)-IF(OR(RIGHT(T148)="-",RIGHT(T148)="+"),1,0)),IF(LEFT(Worksheet!S148,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J149	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G149)=0,LEN(H149)=0,LEN(I149)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G149,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H149),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I149,1)))))
O149	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L149)=0,LEN(M149)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L149),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M149,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L149,1)="+",1,IF(RIGHT(Worksheet!L149,1)="-",-1,0))+IF(RIGHT(Worksheet!M149,1)="+",1,IF(RIGHT(Worksheet!M149,1)="-",-1,0))>0,1,0)))))
P149	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N149,Validation!$A$54:$B$69,2),HLOOKUP(K149,Validation!$D$51:$AD$52,2)))
U149	1	= ISERROR(VLOOKUP(LEFT(T149,LEN(T149)-IF(OR(RIGHT(T149)="-",RIGHT(T149)="+"),1,0)),IF(LEFT(Worksheet!S149,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J150	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G150)=0,LEN(H150)=0,LEN(I150)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G150,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H150),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I150,1)))))
O150	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L150)=0,LEN(M150)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L150),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M150,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L150,1)="+",1,IF(RIGHT(Worksheet!L150,1)="-",-1,0))+IF(RIGHT(Worksheet!M150,1)="+",1,IF(RIGHT(Worksheet!M150,1)="-",-1,0))>0,1,0)))))
P150	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N150,Validation!$A$54:$B$69,2),HLOOKUP(K150,Validation!$D$51:$AD$52,2)))
U150	1	= ISERROR(VLOOKUP(LEFT(T150,LEN(T150)-IF(OR(RIGHT(T150)="-",RIGHT(T150)="+"),1,0)),IF(LEFT(Worksheet!S150,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J151	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G151)=0,LEN(H151)=0,LEN(I151)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G151,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H151),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I151,1)))))
O151	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L151)=0,LEN(M151)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L151),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M151,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L151,1)="+",1,IF(RIGHT(Worksheet!L151,1)="-",-1,0))+IF(RIGHT(Worksheet!M151,1)="+",1,IF(RIGHT(Worksheet!M151,1)="-",-1,0))>0,1,0)))))
P151	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N151,Validation!$A$54:$B$69,2),HLOOKUP(K151,Validation!$D$51:$AD$52,2)))
U151	1	= ISERROR(VLOOKUP(LEFT(T151,LEN(T151)-IF(OR(RIGHT(T151)="-",RIGHT(T151)="+"),1,0)),IF(LEFT(Worksheet!S151,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J152	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G152)=0,LEN(H152)=0,LEN(I152)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G152,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H152),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I152,1)))))
O152	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L152)=0,LEN(M152)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L152),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M152,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L152,1)="+",1,IF(RIGHT(Worksheet!L152,1)="-",-1,0))+IF(RIGHT(Worksheet!M152,1)="+",1,IF(RIGHT(Worksheet!M152,1)="-",-1,0))>0,1,0)))))
P152	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N152,Validation!$A$54:$B$69,2),HLOOKUP(K152,Validation!$D$51:$AD$52,2)))
U152	1	= ISERROR(VLOOKUP(LEFT(T152,LEN(T152)-IF(OR(RIGHT(T152)="-",RIGHT(T152)="+"),1,0)),IF(LEFT(Worksheet!S152,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J153	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G153)=0,LEN(H153)=0,LEN(I153)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G153,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H153),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I153,1)))))
O153	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L153)=0,LEN(M153)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L153),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M153,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L153,1)="+",1,IF(RIGHT(Worksheet!L153,1)="-",-1,0))+IF(RIGHT(Worksheet!M153,1)="+",1,IF(RIGHT(Worksheet!M153,1)="-",-1,0))>0,1,0)))))
P153	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N153,Validation!$A$54:$B$69,2),HLOOKUP(K153,Validation!$D$51:$AD$52,2)))
U153	1	= ISERROR(VLOOKUP(LEFT(T153,LEN(T153)-IF(OR(RIGHT(T153)="-",RIGHT(T153)="+"),1,0)),IF(LEFT(Worksheet!S153,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J154	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G154)=0,LEN(H154)=0,LEN(I154)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G154,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H154),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I154,1)))))
O154	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L154)=0,LEN(M154)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L154),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M154,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L154,1)="+",1,IF(RIGHT(Worksheet!L154,1)="-",-1,0))+IF(RIGHT(Worksheet!M154,1)="+",1,IF(RIGHT(Worksheet!M154,1)="-",-1,0))>0,1,0)))))
P154	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N154,Validation!$A$54:$B$69,2),HLOOKUP(K154,Validation!$D$51:$AD$52,2)))
U154	1	= ISERROR(VLOOKUP(LEFT(T154,LEN(T154)-IF(OR(RIGHT(T154)="-",RIGHT(T154)="+"),1,0)),IF(LEFT(Worksheet!S154,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J155	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G155)=0,LEN(H155)=0,LEN(I155)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G155,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H155),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I155,1)))))
O155	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L155)=0,LEN(M155)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L155),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M155,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L155,1)="+",1,IF(RIGHT(Worksheet!L155,1)="-",-1,0))+IF(RIGHT(Worksheet!M155,1)="+",1,IF(RIGHT(Worksheet!M155,1)="-",-1,0))>0,1,0)))))
P155	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N155,Validation!$A$54:$B$69,2),HLOOKUP(K155,Validation!$D$51:$AD$52,2)))
U155	1	= ISERROR(VLOOKUP(LEFT(T155,LEN(T155)-IF(OR(RIGHT(T155)="-",RIGHT(T155)="+"),1,0)),IF(LEFT(Worksheet!S155,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J156	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G156)=0,LEN(H156)=0,LEN(I156)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G156,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H156),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I156,1)))))
O156	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L156)=0,LEN(M156)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L156),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M156,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L156,1)="+",1,IF(RIGHT(Worksheet!L156,1)="-",-1,0))+IF(RIGHT(Worksheet!M156,1)="+",1,IF(RIGHT(Worksheet!M156,1)="-",-1,0))>0,1,0)))))
P156	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N156,Validation!$A$54:$B$69,2),HLOOKUP(K156,Validation!$D$51:$AD$52,2)))
U156	1	= ISERROR(VLOOKUP(LEFT(T156,LEN(T156)-IF(OR(RIGHT(T156)="-",RIGHT(T156)="+"),1,0)),IF(LEFT(Worksheet!S156,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J157	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G157)=0,LEN(H157)=0,LEN(I157)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G157,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H157),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I157,1)))))
O157	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L157)=0,LEN(M157)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L157),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M157,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L157,1)="+",1,IF(RIGHT(Worksheet!L157,1)="-",-1,0))+IF(RIGHT(Worksheet!M157,1)="+",1,IF(RIGHT(Worksheet!M157,1)="-",-1,0))>0,1,0)))))
P157	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N157,Validation!$A$54:$B$69,2),HLOOKUP(K157,Validation!$D$51:$AD$52,2)))
U157	1	= ISERROR(VLOOKUP(LEFT(T157,LEN(T157)-IF(OR(RIGHT(T157)="-",RIGHT(T157)="+"),1,0)),IF(LEFT(Worksheet!S157,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J158	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G158)=0,LEN(H158)=0,LEN(I158)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G158,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H158),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I158,1)))))
O158	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L158)=0,LEN(M158)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L158),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M158,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L158,1)="+",1,IF(RIGHT(Worksheet!L158,1)="-",-1,0))+IF(RIGHT(Worksheet!M158,1)="+",1,IF(RIGHT(Worksheet!M158,1)="-",-1,0))>0,1,0)))))
P158	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N158,Validation!$A$54:$B$69,2),HLOOKUP(K158,Validation!$D$51:$AD$52,2)))
U158	1	= ISERROR(VLOOKUP(LEFT(T158,LEN(T158)-IF(OR(RIGHT(T158)="-",RIGHT(T158)="+"),1,0)),IF(LEFT(Worksheet!S158,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J159	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G159)=0,LEN(H159)=0,LEN(I159)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G159,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H159),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I159,1)))))
O159	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L159)=0,LEN(M159)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L159),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M159,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L159,1)="+",1,IF(RIGHT(Worksheet!L159,1)="-",-1,0))+IF(RIGHT(Worksheet!M159,1)="+",1,IF(RIGHT(Worksheet!M159,1)="-",-1,0))>0,1,0)))))
P159	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N159,Validation!$A$54:$B$69,2),HLOOKUP(K159,Validation!$D$51:$AD$52,2)))
U159	1	= ISERROR(VLOOKUP(LEFT(T159,LEN(T159)-IF(OR(RIGHT(T159)="-",RIGHT(T159)="+"),1,0)),IF(LEFT(Worksheet!S159,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J160	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G160)=0,LEN(H160)=0,LEN(I160)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G160,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H160),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I160,1)))))
O160	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L160)=0,LEN(M160)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L160),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M160,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L160,1)="+",1,IF(RIGHT(Worksheet!L160,1)="-",-1,0))+IF(RIGHT(Worksheet!M160,1)="+",1,IF(RIGHT(Worksheet!M160,1)="-",-1,0))>0,1,0)))))
P160	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N160,Validation!$A$54:$B$69,2),HLOOKUP(K160,Validation!$D$51:$AD$52,2)))
U160	1	= ISERROR(VLOOKUP(LEFT(T160,LEN(T160)-IF(OR(RIGHT(T160)="-",RIGHT(T160)="+"),1,0)),IF(LEFT(Worksheet!S160,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J161	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G161)=0,LEN(H161)=0,LEN(I161)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G161,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H161),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I161,1)))))
O161	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L161)=0,LEN(M161)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L161),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M161,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L161,1)="+",1,IF(RIGHT(Worksheet!L161,1)="-",-1,0))+IF(RIGHT(Worksheet!M161,1)="+",1,IF(RIGHT(Worksheet!M161,1)="-",-1,0))>0,1,0)))))
P161	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N161,Validation!$A$54:$B$69,2),HLOOKUP(K161,Validation!$D$51:$AD$52,2)))
U161	1	= ISERROR(VLOOKUP(LEFT(T161,LEN(T161)-IF(OR(RIGHT(T161)="-",RIGHT(T161)="+"),1,0)),IF(LEFT(Worksheet!S161,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J162	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G162)=0,LEN(H162)=0,LEN(I162)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G162,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H162),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I162,1)))))
O162	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L162)=0,LEN(M162)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L162),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M162,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L162,1)="+",1,IF(RIGHT(Worksheet!L162,1)="-",-1,0))+IF(RIGHT(Worksheet!M162,1)="+",1,IF(RIGHT(Worksheet!M162,1)="-",-1,0))>0,1,0)))))
P162	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N162,Validation!$A$54:$B$69,2),HLOOKUP(K162,Validation!$D$51:$AD$52,2)))
U162	1	= ISERROR(VLOOKUP(LEFT(T162,LEN(T162)-IF(OR(RIGHT(T162)="-",RIGHT(T162)="+"),1,0)),IF(LEFT(Worksheet!S162,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J163	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G163)=0,LEN(H163)=0,LEN(I163)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G163,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H163),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I163,1)))))
O163	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L163)=0,LEN(M163)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L163),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M163,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L163,1)="+",1,IF(RIGHT(Worksheet!L163,1)="-",-1,0))+IF(RIGHT(Worksheet!M163,1)="+",1,IF(RIGHT(Worksheet!M163,1)="-",-1,0))>0,1,0)))))
P163	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N163,Validation!$A$54:$B$69,2),HLOOKUP(K163,Validation!$D$51:$AD$52,2)))
U163	1	= ISERROR(VLOOKUP(LEFT(T163,LEN(T163)-IF(OR(RIGHT(T163)="-",RIGHT(T163)="+"),1,0)),IF(LEFT(Worksheet!S163,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J164	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G164)=0,LEN(H164)=0,LEN(I164)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G164,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H164),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I164,1)))))
O164	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L164)=0,LEN(M164)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L164),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M164,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L164,1)="+",1,IF(RIGHT(Worksheet!L164,1)="-",-1,0))+IF(RIGHT(Worksheet!M164,1)="+",1,IF(RIGHT(Worksheet!M164,1)="-",-1,0))>0,1,0)))))
P164	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N164,Validation!$A$54:$B$69,2),HLOOKUP(K164,Validation!$D$51:$AD$52,2)))
U164	1	= ISERROR(VLOOKUP(LEFT(T164,LEN(T164)-IF(OR(RIGHT(T164)="-",RIGHT(T164)="+"),1,0)),IF(LEFT(Worksheet!S164,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J165	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G165)=0,LEN(H165)=0,LEN(I165)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G165,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H165),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I165,1)))))
O165	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L165)=0,LEN(M165)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L165),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M165,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L165,1)="+",1,IF(RIGHT(Worksheet!L165,1)="-",-1,0))+IF(RIGHT(Worksheet!M165,1)="+",1,IF(RIGHT(Worksheet!M165,1)="-",-1,0))>0,1,0)))))
P165	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N165,Validation!$A$54:$B$69,2),HLOOKUP(K165,Validation!$D$51:$AD$52,2)))
U165	1	= ISERROR(VLOOKUP(LEFT(T165,LEN(T165)-IF(OR(RIGHT(T165)="-",RIGHT(T165)="+"),1,0)),IF(LEFT(Worksheet!S165,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J166	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G166)=0,LEN(H166)=0,LEN(I166)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G166,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H166),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I166,1)))))
O166	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L166)=0,LEN(M166)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L166),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M166,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L166,1)="+",1,IF(RIGHT(Worksheet!L166,1)="-",-1,0))+IF(RIGHT(Worksheet!M166,1)="+",1,IF(RIGHT(Worksheet!M166,1)="-",-1,0))>0,1,0)))))
P166	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N166,Validation!$A$54:$B$69,2),HLOOKUP(K166,Validation!$D$51:$AD$52,2)))
U166	1	= ISERROR(VLOOKUP(LEFT(T166,LEN(T166)-IF(OR(RIGHT(T166)="-",RIGHT(T166)="+"),1,0)),IF(LEFT(Worksheet!S166,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J167	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G167)=0,LEN(H167)=0,LEN(I167)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G167,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H167),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I167,1)))))
O167	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L167)=0,LEN(M167)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L167),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M167,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L167,1)="+",1,IF(RIGHT(Worksheet!L167,1)="-",-1,0))+IF(RIGHT(Worksheet!M167,1)="+",1,IF(RIGHT(Worksheet!M167,1)="-",-1,0))>0,1,0)))))
P167	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N167,Validation!$A$54:$B$69,2),HLOOKUP(K167,Validation!$D$51:$AD$52,2)))
U167	1	= ISERROR(VLOOKUP(LEFT(T167,LEN(T167)-IF(OR(RIGHT(T167)="-",RIGHT(T167)="+"),1,0)),IF(LEFT(Worksheet!S167,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J168	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G168)=0,LEN(H168)=0,LEN(I168)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G168,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H168),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I168,1)))))
O168	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L168)=0,LEN(M168)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L168),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M168,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L168,1)="+",1,IF(RIGHT(Worksheet!L168,1)="-",-1,0))+IF(RIGHT(Worksheet!M168,1)="+",1,IF(RIGHT(Worksheet!M168,1)="-",-1,0))>0,1,0)))))
P168	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N168,Validation!$A$54:$B$69,2),HLOOKUP(K168,Validation!$D$51:$AD$52,2)))
U168	1	= ISERROR(VLOOKUP(LEFT(T168,LEN(T168)-IF(OR(RIGHT(T168)="-",RIGHT(T168)="+"),1,0)),IF(LEFT(Worksheet!S168,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J169	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G169)=0,LEN(H169)=0,LEN(I169)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G169,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H169),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I169,1)))))
O169	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L169)=0,LEN(M169)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L169),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M169,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L169,1)="+",1,IF(RIGHT(Worksheet!L169,1)="-",-1,0))+IF(RIGHT(Worksheet!M169,1)="+",1,IF(RIGHT(Worksheet!M169,1)="-",-1,0))>0,1,0)))))
P169	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N169,Validation!$A$54:$B$69,2),HLOOKUP(K169,Validation!$D$51:$AD$52,2)))
U169	1	= ISERROR(VLOOKUP(LEFT(T169,LEN(T169)-IF(OR(RIGHT(T169)="-",RIGHT(T169)="+"),1,0)),IF(LEFT(Worksheet!S169,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J170	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G170)=0,LEN(H170)=0,LEN(I170)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G170,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H170),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I170,1)))))
O170	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L170)=0,LEN(M170)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L170),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M170,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L170,1)="+",1,IF(RIGHT(Worksheet!L170,1)="-",-1,0))+IF(RIGHT(Worksheet!M170,1)="+",1,IF(RIGHT(Worksheet!M170,1)="-",-1,0))>0,1,0)))))
P170	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N170,Validation!$A$54:$B$69,2),HLOOKUP(K170,Validation!$D$51:$AD$52,2)))
U170	1	= ISERROR(VLOOKUP(LEFT(T170,LEN(T170)-IF(OR(RIGHT(T170)="-",RIGHT(T170)="+"),1,0)),IF(LEFT(Worksheet!S170,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J171	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G171)=0,LEN(H171)=0,LEN(I171)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G171,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H171),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I171,1)))))
O171	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L171)=0,LEN(M171)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L171),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M171,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L171,1)="+",1,IF(RIGHT(Worksheet!L171,1)="-",-1,0))+IF(RIGHT(Worksheet!M171,1)="+",1,IF(RIGHT(Worksheet!M171,1)="-",-1,0))>0,1,0)))))
P171	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N171,Validation!$A$54:$B$69,2),HLOOKUP(K171,Validation!$D$51:$AD$52,2)))
U171	1	= ISERROR(VLOOKUP(LEFT(T171,LEN(T171)-IF(OR(RIGHT(T171)="-",RIGHT(T171)="+"),1,0)),IF(LEFT(Worksheet!S171,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J172	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G172)=0,LEN(H172)=0,LEN(I172)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G172,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H172),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I172,1)))))
O172	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L172)=0,LEN(M172)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L172),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M172,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L172,1)="+",1,IF(RIGHT(Worksheet!L172,1)="-",-1,0))+IF(RIGHT(Worksheet!M172,1)="+",1,IF(RIGHT(Worksheet!M172,1)="-",-1,0))>0,1,0)))))
P172	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N172,Validation!$A$54:$B$69,2),HLOOKUP(K172,Validation!$D$51:$AD$52,2)))
U172	1	= ISERROR(VLOOKUP(LEFT(T172,LEN(T172)-IF(OR(RIGHT(T172)="-",RIGHT(T172)="+"),1,0)),IF(LEFT(Worksheet!S172,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J173	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G173)=0,LEN(H173)=0,LEN(I173)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G173,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H173),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I173,1)))))
O173	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L173)=0,LEN(M173)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L173),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M173,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L173,1)="+",1,IF(RIGHT(Worksheet!L173,1)="-",-1,0))+IF(RIGHT(Worksheet!M173,1)="+",1,IF(RIGHT(Worksheet!M173,1)="-",-1,0))>0,1,0)))))
P173	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N173,Validation!$A$54:$B$69,2),HLOOKUP(K173,Validation!$D$51:$AD$52,2)))
U173	1	= ISERROR(VLOOKUP(LEFT(T173,LEN(T173)-IF(OR(RIGHT(T173)="-",RIGHT(T173)="+"),1,0)),IF(LEFT(Worksheet!S173,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J174	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G174)=0,LEN(H174)=0,LEN(I174)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G174,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H174),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I174,1)))))
O174	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L174)=0,LEN(M174)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L174),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M174,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L174,1)="+",1,IF(RIGHT(Worksheet!L174,1)="-",-1,0))+IF(RIGHT(Worksheet!M174,1)="+",1,IF(RIGHT(Worksheet!M174,1)="-",-1,0))>0,1,0)))))
P174	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N174,Validation!$A$54:$B$69,2),HLOOKUP(K174,Validation!$D$51:$AD$52,2)))
U174	1	= ISERROR(VLOOKUP(LEFT(T174,LEN(T174)-IF(OR(RIGHT(T174)="-",RIGHT(T174)="+"),1,0)),IF(LEFT(Worksheet!S174,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J175	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G175)=0,LEN(H175)=0,LEN(I175)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G175,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H175),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I175,1)))))
O175	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L175)=0,LEN(M175)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L175),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M175,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L175,1)="+",1,IF(RIGHT(Worksheet!L175,1)="-",-1,0))+IF(RIGHT(Worksheet!M175,1)="+",1,IF(RIGHT(Worksheet!M175,1)="-",-1,0))>0,1,0)))))
P175	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N175,Validation!$A$54:$B$69,2),HLOOKUP(K175,Validation!$D$51:$AD$52,2)))
U175	1	= ISERROR(VLOOKUP(LEFT(T175,LEN(T175)-IF(OR(RIGHT(T175)="-",RIGHT(T175)="+"),1,0)),IF(LEFT(Worksheet!S175,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J176	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G176)=0,LEN(H176)=0,LEN(I176)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G176,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H176),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I176,1)))))
O176	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L176)=0,LEN(M176)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L176),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M176,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L176,1)="+",1,IF(RIGHT(Worksheet!L176,1)="-",-1,0))+IF(RIGHT(Worksheet!M176,1)="+",1,IF(RIGHT(Worksheet!M176,1)="-",-1,0))>0,1,0)))))
P176	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N176,Validation!$A$54:$B$69,2),HLOOKUP(K176,Validation!$D$51:$AD$52,2)))
U176	1	= ISERROR(VLOOKUP(LEFT(T176,LEN(T176)-IF(OR(RIGHT(T176)="-",RIGHT(T176)="+"),1,0)),IF(LEFT(Worksheet!S176,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J177	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G177)=0,LEN(H177)=0,LEN(I177)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G177,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H177),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I177,1)))))
O177	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L177)=0,LEN(M177)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L177),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M177,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L177,1)="+",1,IF(RIGHT(Worksheet!L177,1)="-",-1,0))+IF(RIGHT(Worksheet!M177,1)="+",1,IF(RIGHT(Worksheet!M177,1)="-",-1,0))>0,1,0)))))
P177	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N177,Validation!$A$54:$B$69,2),HLOOKUP(K177,Validation!$D$51:$AD$52,2)))
U177	1	= ISERROR(VLOOKUP(LEFT(T177,LEN(T177)-IF(OR(RIGHT(T177)="-",RIGHT(T177)="+"),1,0)),IF(LEFT(Worksheet!S177,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J178	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G178)=0,LEN(H178)=0,LEN(I178)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G178,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H178),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I178,1)))))
O178	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L178)=0,LEN(M178)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L178),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M178,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L178,1)="+",1,IF(RIGHT(Worksheet!L178,1)="-",-1,0))+IF(RIGHT(Worksheet!M178,1)="+",1,IF(RIGHT(Worksheet!M178,1)="-",-1,0))>0,1,0)))))
P178	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N178,Validation!$A$54:$B$69,2),HLOOKUP(K178,Validation!$D$51:$AD$52,2)))
U178	1	= ISERROR(VLOOKUP(LEFT(T178,LEN(T178)-IF(OR(RIGHT(T178)="-",RIGHT(T178)="+"),1,0)),IF(LEFT(Worksheet!S178,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J179	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G179)=0,LEN(H179)=0,LEN(I179)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G179,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H179),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I179,1)))))
O179	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L179)=0,LEN(M179)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L179),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M179,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L179,1)="+",1,IF(RIGHT(Worksheet!L179,1)="-",-1,0))+IF(RIGHT(Worksheet!M179,1)="+",1,IF(RIGHT(Worksheet!M179,1)="-",-1,0))>0,1,0)))))
P179	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N179,Validation!$A$54:$B$69,2),HLOOKUP(K179,Validation!$D$51:$AD$52,2)))
U179	1	= ISERROR(VLOOKUP(LEFT(T179,LEN(T179)-IF(OR(RIGHT(T179)="-",RIGHT(T179)="+"),1,0)),IF(LEFT(Worksheet!S179,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J180	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G180)=0,LEN(H180)=0,LEN(I180)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G180,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H180),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I180,1)))))
O180	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L180)=0,LEN(M180)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L180),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M180,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L180,1)="+",1,IF(RIGHT(Worksheet!L180,1)="-",-1,0))+IF(RIGHT(Worksheet!M180,1)="+",1,IF(RIGHT(Worksheet!M180,1)="-",-1,0))>0,1,0)))))
P180	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N180,Validation!$A$54:$B$69,2),HLOOKUP(K180,Validation!$D$51:$AD$52,2)))
U180	1	= ISERROR(VLOOKUP(LEFT(T180,LEN(T180)-IF(OR(RIGHT(T180)="-",RIGHT(T180)="+"),1,0)),IF(LEFT(Worksheet!S180,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J181	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G181)=0,LEN(H181)=0,LEN(I181)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G181,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H181),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I181,1)))))
O181	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L181)=0,LEN(M181)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L181),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M181,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L181,1)="+",1,IF(RIGHT(Worksheet!L181,1)="-",-1,0))+IF(RIGHT(Worksheet!M181,1)="+",1,IF(RIGHT(Worksheet!M181,1)="-",-1,0))>0,1,0)))))
P181	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N181,Validation!$A$54:$B$69,2),HLOOKUP(K181,Validation!$D$51:$AD$52,2)))
U181	1	= ISERROR(VLOOKUP(LEFT(T181,LEN(T181)-IF(OR(RIGHT(T181)="-",RIGHT(T181)="+"),1,0)),IF(LEFT(Worksheet!S181,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J182	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G182)=0,LEN(H182)=0,LEN(I182)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G182,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H182),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I182,1)))))
O182	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L182)=0,LEN(M182)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L182),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M182,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L182,1)="+",1,IF(RIGHT(Worksheet!L182,1)="-",-1,0))+IF(RIGHT(Worksheet!M182,1)="+",1,IF(RIGHT(Worksheet!M182,1)="-",-1,0))>0,1,0)))))
P182	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N182,Validation!$A$54:$B$69,2),HLOOKUP(K182,Validation!$D$51:$AD$52,2)))
U182	1	= ISERROR(VLOOKUP(LEFT(T182,LEN(T182)-IF(OR(RIGHT(T182)="-",RIGHT(T182)="+"),1,0)),IF(LEFT(Worksheet!S182,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J183	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G183)=0,LEN(H183)=0,LEN(I183)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G183,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H183),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I183,1)))))
O183	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L183)=0,LEN(M183)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L183),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M183,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L183,1)="+",1,IF(RIGHT(Worksheet!L183,1)="-",-1,0))+IF(RIGHT(Worksheet!M183,1)="+",1,IF(RIGHT(Worksheet!M183,1)="-",-1,0))>0,1,0)))))
P183	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N183,Validation!$A$54:$B$69,2),HLOOKUP(K183,Validation!$D$51:$AD$52,2)))
U183	1	= ISERROR(VLOOKUP(LEFT(T183,LEN(T183)-IF(OR(RIGHT(T183)="-",RIGHT(T183)="+"),1,0)),IF(LEFT(Worksheet!S183,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J184	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G184)=0,LEN(H184)=0,LEN(I184)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G184,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H184),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I184,1)))))
O184	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L184)=0,LEN(M184)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L184),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M184,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L184,1)="+",1,IF(RIGHT(Worksheet!L184,1)="-",-1,0))+IF(RIGHT(Worksheet!M184,1)="+",1,IF(RIGHT(Worksheet!M184,1)="-",-1,0))>0,1,0)))))
P184	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N184,Validation!$A$54:$B$69,2),HLOOKUP(K184,Validation!$D$51:$AD$52,2)))
U184	1	= ISERROR(VLOOKUP(LEFT(T184,LEN(T184)-IF(OR(RIGHT(T184)="-",RIGHT(T184)="+"),1,0)),IF(LEFT(Worksheet!S184,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J185	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G185)=0,LEN(H185)=0,LEN(I185)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G185,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H185),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I185,1)))))
O185	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L185)=0,LEN(M185)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L185),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M185,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L185,1)="+",1,IF(RIGHT(Worksheet!L185,1)="-",-1,0))+IF(RIGHT(Worksheet!M185,1)="+",1,IF(RIGHT(Worksheet!M185,1)="-",-1,0))>0,1,0)))))
P185	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N185,Validation!$A$54:$B$69,2),HLOOKUP(K185,Validation!$D$51:$AD$52,2)))
U185	1	= ISERROR(VLOOKUP(LEFT(T185,LEN(T185)-IF(OR(RIGHT(T185)="-",RIGHT(T185)="+"),1,0)),IF(LEFT(Worksheet!S185,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J186	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G186)=0,LEN(H186)=0,LEN(I186)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G186,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H186),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I186,1)))))
O186	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L186)=0,LEN(M186)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L186),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M186,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L186,1)="+",1,IF(RIGHT(Worksheet!L186,1)="-",-1,0))+IF(RIGHT(Worksheet!M186,1)="+",1,IF(RIGHT(Worksheet!M186,1)="-",-1,0))>0,1,0)))))
P186	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N186,Validation!$A$54:$B$69,2),HLOOKUP(K186,Validation!$D$51:$AD$52,2)))
U186	1	= ISERROR(VLOOKUP(LEFT(T186,LEN(T186)-IF(OR(RIGHT(T186)="-",RIGHT(T186)="+"),1,0)),IF(LEFT(Worksheet!S186,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J187	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G187)=0,LEN(H187)=0,LEN(I187)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G187,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H187),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I187,1)))))
O187	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L187)=0,LEN(M187)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L187),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M187,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L187,1)="+",1,IF(RIGHT(Worksheet!L187,1)="-",-1,0))+IF(RIGHT(Worksheet!M187,1)="+",1,IF(RIGHT(Worksheet!M187,1)="-",-1,0))>0,1,0)))))
P187	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N187,Validation!$A$54:$B$69,2),HLOOKUP(K187,Validation!$D$51:$AD$52,2)))
U187	1	= ISERROR(VLOOKUP(LEFT(T187,LEN(T187)-IF(OR(RIGHT(T187)="-",RIGHT(T187)="+"),1,0)),IF(LEFT(Worksheet!S187,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J188	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G188)=0,LEN(H188)=0,LEN(I188)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G188,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H188),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I188,1)))))
O188	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L188)=0,LEN(M188)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L188),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M188,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L188,1)="+",1,IF(RIGHT(Worksheet!L188,1)="-",-1,0))+IF(RIGHT(Worksheet!M188,1)="+",1,IF(RIGHT(Worksheet!M188,1)="-",-1,0))>0,1,0)))))
P188	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N188,Validation!$A$54:$B$69,2),HLOOKUP(K188,Validation!$D$51:$AD$52,2)))
U188	1	= ISERROR(VLOOKUP(LEFT(T188,LEN(T188)-IF(OR(RIGHT(T188)="-",RIGHT(T188)="+"),1,0)),IF(LEFT(Worksheet!S188,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J189	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G189)=0,LEN(H189)=0,LEN(I189)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G189,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H189),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I189,1)))))
O189	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L189)=0,LEN(M189)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L189),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M189,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L189,1)="+",1,IF(RIGHT(Worksheet!L189,1)="-",-1,0))+IF(RIGHT(Worksheet!M189,1)="+",1,IF(RIGHT(Worksheet!M189,1)="-",-1,0))>0,1,0)))))
P189	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N189,Validation!$A$54:$B$69,2),HLOOKUP(K189,Validation!$D$51:$AD$52,2)))
U189	1	= ISERROR(VLOOKUP(LEFT(T189,LEN(T189)-IF(OR(RIGHT(T189)="-",RIGHT(T189)="+"),1,0)),IF(LEFT(Worksheet!S189,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J190	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G190)=0,LEN(H190)=0,LEN(I190)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G190,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H190),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I190,1)))))
O190	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L190)=0,LEN(M190)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L190),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M190,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L190,1)="+",1,IF(RIGHT(Worksheet!L190,1)="-",-1,0))+IF(RIGHT(Worksheet!M190,1)="+",1,IF(RIGHT(Worksheet!M190,1)="-",-1,0))>0,1,0)))))
P190	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N190,Validation!$A$54:$B$69,2),HLOOKUP(K190,Validation!$D$51:$AD$52,2)))
U190	1	= ISERROR(VLOOKUP(LEFT(T190,LEN(T190)-IF(OR(RIGHT(T190)="-",RIGHT(T190)="+"),1,0)),IF(LEFT(Worksheet!S190,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J191	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G191)=0,LEN(H191)=0,LEN(I191)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G191,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H191),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I191,1)))))
O191	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L191)=0,LEN(M191)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L191),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M191,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L191,1)="+",1,IF(RIGHT(Worksheet!L191,1)="-",-1,0))+IF(RIGHT(Worksheet!M191,1)="+",1,IF(RIGHT(Worksheet!M191,1)="-",-1,0))>0,1,0)))))
P191	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N191,Validation!$A$54:$B$69,2),HLOOKUP(K191,Validation!$D$51:$AD$52,2)))
U191	1	= ISERROR(VLOOKUP(LEFT(T191,LEN(T191)-IF(OR(RIGHT(T191)="-",RIGHT(T191)="+"),1,0)),IF(LEFT(Worksheet!S191,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J192	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G192)=0,LEN(H192)=0,LEN(I192)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G192,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H192),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I192,1)))))
O192	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L192)=0,LEN(M192)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L192),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M192,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L192,1)="+",1,IF(RIGHT(Worksheet!L192,1)="-",-1,0))+IF(RIGHT(Worksheet!M192,1)="+",1,IF(RIGHT(Worksheet!M192,1)="-",-1,0))>0,1,0)))))
P192	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N192,Validation!$A$54:$B$69,2),HLOOKUP(K192,Validation!$D$51:$AD$52,2)))
U192	1	= ISERROR(VLOOKUP(LEFT(T192,LEN(T192)-IF(OR(RIGHT(T192)="-",RIGHT(T192)="+"),1,0)),IF(LEFT(Worksheet!S192,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J193	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G193)=0,LEN(H193)=0,LEN(I193)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G193,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H193),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I193,1)))))
O193	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L193)=0,LEN(M193)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L193),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M193,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L193,1)="+",1,IF(RIGHT(Worksheet!L193,1)="-",-1,0))+IF(RIGHT(Worksheet!M193,1)="+",1,IF(RIGHT(Worksheet!M193,1)="-",-1,0))>0,1,0)))))
P193	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N193,Validation!$A$54:$B$69,2),HLOOKUP(K193,Validation!$D$51:$AD$52,2)))
U193	1	= ISERROR(VLOOKUP(LEFT(T193,LEN(T193)-IF(OR(RIGHT(T193)="-",RIGHT(T193)="+"),1,0)),IF(LEFT(Worksheet!S193,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))
J194	2	= IF(NOT(Format2Print),2,IF(OR(LEN(G194)=0,LEN(H194)=0,LEN(I194)=0),2,OFFSET(Validation!$A$8,VLOOKUP(LEFT(Worksheet!G194,1),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Worksheet!H194),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(Worksheet!I194,1)))))
O194	2	= IF(NOT(Format2Print),2,MIN(3,IF(OR(LEN(L194)=0,LEN(M194)=0),2,OFFSET(Validation!$A$21,VLOOKUP(LEFT(UPPER(Worksheet!L194),1),Validation!$A$22:$L$30,12,FALSE),(VALUE(LEFT(Worksheet!M194,1))-1)*2+1+IF(IF(RIGHT(Worksheet!L194,1)="+",1,IF(RIGHT(Worksheet!L194,1)="-",-1,0))+IF(RIGHT(Worksheet!M194,1)="+",1,IF(RIGHT(Worksheet!M194,1)="-",-1,0))>0,1,0)))))
P194	2	= IF(NOT(Format2Print),2,OFFSET(Validation!$C$53,VLOOKUP(N194,Validation!$A$54:$B$69,2),HLOOKUP(K194,Validation!$D$51:$AD$52,2)))
U194	1	= ISERROR(VLOOKUP(LEFT(T194,LEN(T194)-IF(OR(RIGHT(T194)="-",RIGHT(T194)="+"),1,0)),IF(LEFT(Worksheet!S194,1)="N",'macro d''éval'!$N$36:$O$39,'macro d''éval'!$N$42:$O$45),2,FALSE))

===== SHEET: Matrix (xl/worksheets/sheet4.xml) =====

===== SHEET: Jobgrades (xl/worksheets/sheet5.xml) =====
M2	1
N2	0
O2	0
M3	1	= IF(M2,1,IF(N2,2,3))
B4	Standard Hay Buckets
C4	15% Steps
D4	Client Specific
I4	You chose the following jobgrades structure:
I5	Lower value
J5	Mid point
K5	Upper value
L5	Jobgrade
B6	0
C6	0
D6	0
I6	0
J6	14	= INT(AVERAGE(I6,K6))
K6	29	= I7-1
L6	0
B7	30
C7	16
D7	100
I7	30	= CHOOSE($M$3,B7,C7,MAX(I6,D7))
J7	34	= INT(AVERAGE(I7,K7))
K7	39
L7	1
B8	40
C8	19
D8	200
I8	40
J8	43
K8	46
L8	2
B9	47
C9	22
D9	300
I9	47
J9	50
K9	53
L9	3
B10	54
C10	25
D10	400
I10	54
J10	58
K10	62
L10	4
B11	63
C11	29
D11	500
I11	63
J11	67
K11	72
L11	5
B12	73
C12	33
D12	600
I12	73
J12	78
K12	84
L12	6
B13	85
C13	38
D13	700
I13	85
J13	91
K13	97
L13	7
B14	98
C14	43
D14	800
I14	98
J14	105
K14	113
L14	8
B15	114
C15	50
D15	900
I15	114
J15	124
K15	134
L15	9
B16	135
C16	57
D16	1000
I16	135
J16	147
K16	160
L16	10
B17	161
C17	66
D17	1100
I17	161
J17	176
K17	191
L17	11
B18	192
C18	76
D18	1200
I18	192
J18	209
K18	227
L18	12
B19	228
C19	87
D19	1300
I19	228
J19	248
K19	268
L19	13
B20	269
C20	100
D20	1400
I20	269
J20	291
K20	313
L20	14
B21	314
C21	115
D21	1500
I21	314
J21	342
K21	370
L21	15
B22	371
C22	132
D22	1600
I22	371
J22	404
K22	438
L22	16
B23	439
C23	152
D23	1700
I23	439
J23	478
K23	518
L23	17
B24	519
C24	175
D24	1800
I24	519
J24	566
K24	613
L24	18
B25	614
C25	200
D25	1900
I25	614
J25	674
K25	734
L25	19
B26	735
C26	230
D26	2000
I26	735
J26	807
K26	879
L26	20
B27	880
C27	264
D27	2100
I27	880
J27	967
K27	1055
L27	21
B28	1056
C28	304
D28	2200
I28	1056	= CHOOSE($M$3,B28,C28,MAX(I27,D28))
J28	1158
K28	1260
L28	22
B29	1261
C29	350
D29	2300
I29	1261
J29	1384
K29	1507
L29	23
B30	1508
C30	400
D30	2400
I30	1508
J30	1654
K30	1800
L30	24
B31	1801
C31	460
D31	2500
I31	1801
J31	1970
K31	2140
L31	25
B32	2141
C32	528
D32	2600
I32	2141
J32	2345	= INT(AVERAGE(I32,K32))
K32	2550	= I33-1
L32	26
B33	2551
C33	608
D33	2700
I33	2551
J33	2785	= INT(AVERAGE(I33,K33))
K33	3020	= I34-1
L33	27
B34	3021
C34	700
D34	2800
I34	3021
J34	3300
K34	3580
L34	28
B35	3581
C35	800
D35	2900
I35	3581
J35	3915
K35	4250
L35	29
B36	4251
C36	920
D36	3000
I36	4251
J36	4655
K36	5060
L36	30
B37	5061
C37	1056
D37	3100
I37	5061
J37	5540
K37	6020
L37	31
B38	6021
C38	1216
D38	3200
I38	6021
J38	6590
K38	7160
L38	32
B39	7161
C39	1400
D39	3300
I39	7161
J39	7740
K39	8320
L39	33
B40	8321
C40	1600
D40	3400
I40	8321
J40	8980
K40	9640
L40	34
B41	9641
C41	1840
D41	3500
I41	9641
J41	10410
K41	11180
L41	35
B42	11181
C42	2112
D42	3600
I42	11181
J42	12080
K42	12980
L42	36
B43	12981
C43	2432
D43	3700
I43	12981
J43	14030
K43	15080
L43	37
B44	15081
C44	2800
D44	3800
I44	15081
J44	16310
K44	17540
L44	38
B45	17541
C45	3200
D45	3900
I45	17541
L45	XX

===== SHEET: Matchcodes (xl/worksheets/sheet6.xml) =====
A1	HAY-LEVEL
B1	HAY-RANGE
C1	HAY-MIDPOINT
D1	FINANCE & ACCOUNTING
F1	IT & TELECOMMUNICATIONS
J1	HUMAN RESOURCES
L1	LEGAL
M1	MARKETING
P1	SALES
R1	CUSTOMER SERVICE
T1	RESEARCH & DEVELOPMENT
U1	ENGINEERING
V1	LOGISTICS/SUPPLY CHAIN
X1	PRODUCTION
Y1	ADMINISTRATION/SUPPORT/SERVICE
AB1	ENVIRONMENT/HEALTH/SAFETY
D2	Accounting (FA)
E2	Specialist (FB)
F2	Design & Development (IA)
G2	Infrastructure/
Support (IB)
H2	Operations (IC)
I2	Datamanagement (ID)
J2	HR Generalist (HA)
K2	HR Specialist (HB)
L2	(L)
M2	Market Research (MA)
N2	Brand Management (MB)
O2	Promotions (MC)
P2	Support & Training (SA)
Q2	Individual Contributor & Sales Management (SB)
R2	Technical (CA)
S2	Non Technical (CB)
T2	(R)
U2	(E)
V2	Acquisition (JA)
W2	Internal Operations & Delivery (JB)
X2	(P)
Y2	Clerical Services (AA)
Z2	Secretarial (AB)
AA2	Translation (AC)
AB2	(W)
A3	21
B3	878 - 1055
C3	954
F3	Head of Information Technology
(i9001)
A4	20
B4	735 - 879
C4	805
X4	Superintendent III/Production Manager (P0349)
A5	19
B5	614 - 734
C5	677
D5	Manager General Accounting
 (F0008M)
E5	 Financial Sub-section Mgr.
(F7442)
F5	Manager Systems & Programming 
(i7443)
G5	Network Integrator (LAN/WAN) 
(i0079M)
H5	Computer Services Manager II (i5153)
L5	Senior legal Advisor (L0154)
N5	Brand/Product
Manager IV
(M0178)
Q5	Regional Sales Manager (S0209M)
R5	Manager Customer Service (C0223M)
T5	Scientist/Researcher V (R0248)
W5	Manager Logistics Operations (J0329M)
X5	Plant Manager (P0350)                                            Superintendent II/Production Manager (P0348)
A6	18
B6	519 - 613
C6	571
E6	Senior Financial Analyst (F0026)
G6	Network Architect (i0080)                         Network Operations Manager 
(i0062M)
I6	Manager Database (i0075M)                                       
J6	Human Resources Manager
(H0106M)
K6	Training & Development Manager (H0110L)                          Compensation & Benefits Manager (H7446)
L6	Legal Advisor
(L0153)
M6	Market Research Manager
(M0173M)
N6	Brand/Product Manager III
(H0177)
T6	Scientist/Researcher IV                                 (R0237)                                    Research & Development Supervisor II (R0240)
U6	Engineer V (E0266)
V6	Purchasing Manager (J0323L)
W6	Manager Production Control (J0292M)
X6	Superintendent I/Production Manager (P0347)
AB6	Environmental Health & Safety Manager (W7459)
A7	17
B7	439 - 518
C7	479
E7	 Financial Analyst II (F0025)
Controller (F00231)  
F7	Senior Systems Analyst                          (i0048)                                             ERP Configurer (i0093)
G7	Group Ware Specialist (i7445)
H7	Computer Services Manager I (i5137)
I7	Senior Data Security Specialist (i0082M)                                    Database Analyst III (i0074)                                      Database Architect
(i5237)
J7	Personnel Manager II (H0104)
K7	Recruitment Manager                (H0119 L)                                          Employee/Labour Relations Representative III (H0120)
L7	Principal Legal Executive 
(L0162)
M7	Market Analyst/Business Development Officer III (M4012)
N7	Brand/Product Manager II
(M4009)
O7	Market Communication Representative (M0175)                                Public Relations Representative (M0403)
P7	Sales Training Manager (S6220) 
Q7	National Accounts/Key Accounts Manager
 (S0202)
Area/District Sales Manager 
(S0215)
R7	Technical Customer Service Teamleader (C0224M)
T7	Scientist/Researcher III                             (R0236)                                    Research & Development Supervisor I (R0239)
U7	Engineer IV (E0265)
X7	General Supervisor II (P0346)
AB7	Quality Assurance Manager (W7460)
A8	16
B8	371 - 438
C8	406
D8	Accounting Supervisor II/Chief Accountant II (F0007M)                          

E8	       Financial Analyst III
(F0025a)
F8	Principal Analyst Programmer (i7444)                                                        Systems Analyst (i0047)
G8	Network Planning Analyst (i0083)                         Network Administrator (multiple platform LAN/WAN) (i0078)      
H8	Senior Information Center  (or End User Computing Support) Analyst (i0056)
I8	Database Analyst II (i0073)                                     Database Administrator (i0053)
J8	Personnel Manager I (H0103)
K8	Training & Development Specialist II (H7447)                          Compensation & Benefits Specialist (H7448)
L8	Senior Legal Executive (L4704)
M8	Market Analyst/Business Development Officer II (M0172)
N8	Brand/Product Manager I
(M0185)
O8	Promotions Manager (M4013)
Q8	Sales Representative III (S0205)
T8	Scientist/Researcher II (R0235)
U8	Engineer III (E0264)
V8	Purchasing Agent (J0322M)
W8	Traffic Manager (L0295M)                                                  Warehouse Manager (J0294M)
X8	Unit Supervisor IV (P7456)                                     General Supervisor I (P0345)                             
AB8	Environmental Health & Safety Professional (W7461)
A9	15
B9	314 - 370
C9	342
D9	Accounting Supervisor I (F0022)                 
E9	 Financial Analyst I (F0024)
F9	Analyst Programmer IV (i5119)
G9	Network Administrator                       (single platform LAN/WAN) 
(i0077)      
I9	Database Analyst I (i0072)
K9	Recruitment Officer (H7449)
L9	Legal Executive (L0163)
M9	Market Analyst/Business Development Officer I (M4014)
N9	Assistant Brand/Product Manager
(M4007)
O9	Public Relations Assistant
(M0402)
Q9	Sales Representative II (S0204)
R9	Technical Customer Service Rep. II (C0220M)
S9	Customer Service Teamleader (C0222M)
T9	Scientist/Researcher I (R0234)
U9	Engineer II (E0263)
W9	Production Planner (J0291M)
X9	Unit Supervisor III (P0344) 
Y9	Office Manager III (A7458)
A10	14
B10	269 - 313
C10	291
D10	Accountant III (F0004)
F10	Analyst Programmer III (i5120)
G10	Network Administrator (LAN) (i0061)      
H10	Information Systems                (or End User Computing Support) Analyst (i0055)
K10	Training & Development Specialist I (H0108)                          Compensation & Benefits Analyst (H7450)
M10	Marketing Research Analyst II
(M7451)
P10	Telesales Supervisor (S7453)
Sales Trainer
(S6222)
Q10	Sales Representative I (S0203)
R10	Technical Customer Service Rep. I (C0221M)
U10	Engineer I (E0262)
V10	Buyer II (J0321)
X10	Unit Supervisor II (P0343) 
Y10	Administrative Assistant II (A5010)                                         Office Manager II (A7055)     
Z10	Secretary VI (reports to CEO) (A5004)
AA10	Translator II (A7733)
A11	13
B11	228 - 268
C11	252
D11	Accountant II (F0003)
F11	Analyst Programmer II (i5121)
J11	Human Resources Administrator 
(H0102)
K11	Recruiter
(H0118)
M11	Marketing Research Analyst I
(M7452)
O11	Promotions Assistant (M4016)
Q11	Sales Representative (S7455)
S11	Customer Service Rep. III 
(C0217M)
T11	Researcher/Technician (R0232)
U11	Design Drafter (E4120)
V11	Buyer I (J0324)
W11	Warehouse Supervisor (J0293M)
X11	Unit Supervisor I (P0342) 
Y11	Administrative Assistant I (A7056)                             Office Manager I (A5009)     
Z11	Secretary V (A5005)
AA11	Translator I (A7734)
AB11	Industrial Nurse (W0124)
A12	12
B12	192 - 227
C12	208
D12	Accountant I (F0002)
F12	Analyst Programmer I (i5122)
H12	PC Maintenance Technician (i0095)
P12	Telesales Operator (S1609)
S12	Customer Service Rep. II 
(C0218M)
T12	Laboratory Technician (R4107)
U12	Drafter (E4122)                                    Electronic Technician II (E4123)
X12	Maintenance Technician (P7457)
Y12	General Clerk V (A1087)
Z12	Secretary IV (A7054)
A13	11
B13	161 - 191
C13	173
D13	Accounts Clerk IV (F1040)
G13	Help Desk Analyst (i5150)
S13	Customer Service Rep. I (C0219M)
U13	Electronic Technician I (E4124)
X13	Production/Process Operator V (P4204)
Y13	General Clerk IV (A1088)
Z13	Secretary III (A5006)
A14	10
B14	135 - 160
C14	151
D14	Accounts Clerk III (F1039)
P14	Merchandiser
(S7454)
Y14	General Clerk III (A1089)                                       Receptionist/Telephonist II (A7736)
Z14	Secretary II (A5007)
A15	9
B15	114 - 134 
C15	125
D15	Accounts Clerk II (F1038)
X15	Production/Process Operator IV (P4212)
Y15	General Clerk II (A1090)                                       Chauffeur II (A5011)
Z15	Secretary I (A5008)
A16	8
B16	98 - 113
C16	104
I16	Data Entry Operator II
(i9002)
W16	Stock Clerk (J7752)
X16	Production/Process Operator III (P4216)
Y16	General Clerk I (A1091)                                       Receptionist/
Switchboard
 Operator (A7057)                                                   Chauffeur I (A5012)
A17	7
B17	85 - 97
C17	90
W17	Forklift Operator (J7756)

===== SHEET: Validation (xl/worksheets/sheet7.xml) =====
BA1	KH
BD1	PS
BF1	ACC
BB2	Khb
BC2	KhHrs
BD2	PSF
BE2	PSC
BF2	AcF
BG2	AcM
BH2	AcI
A3	D	= C_Khd
BA3	A-
BB3	T-
BC3	1
BD3	A-
BE3	1-
BF3	A-
BG3	N-
BH3	I-
A4	V	= C_Khb
BA4	A
BB4	T
BC4	2
BD4	A
BE4	1
BF4	A
BG4	N
BH4	I
A5	1	= C_KhHrs
B5	0	= OFFSET(Validation!$A$8,VLOOKUP(UPPER(LEFT(A3,1)),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(A4),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(A5,1)))
BA5	A+
BB5	T+
BC5	3
BD5	A+
BE5	1+
BF5	A+
BG5	N+
BH5	I+
BA6	B-
BB6	I-
BD6	B-
BE6	2-
BF6	B-
BG6	1-
BH6	II-
B7	T
E7	I
H7	II
K7	III
N7	IV
Q7	V
BA7	B
BB7	I
BD7	B
BE7	2
BF7	B
BG7	1
BH7	II
B8	1
C8	2
D8	3
E8	1
F8	2
G8	3
H8	1
I8	2
J8	3
K8	1
L8	2
M8	3
N8	1
O8	2
P8	3
Q8	1
R8	2
S8	3
BA8	B+
BB8	I+
BD8	B+
BE8	2+
BF8	B+
BG8	1+
BH8	II+
A9	A
B9	2
C9	1
D9	0
E9	1
F9	0
G9	0
H9	0
I9	0
J9	0
K9	0
L9	0
M9	0
N9	0
O9	0
P9	0
Q9	0
R9	0
S9	0
U9	1
BA9	C-
BB9	II-
BD9	C-
BE9	3-
BF9	C-
BG9	2-
BH9	III-
A10	B
B10	2
C10	2
D10	0
E10	2
F10	2
G10	1
H10	0
I10	0
J10	0
K10	0
L10	0
M10	0
N10	0
O10	0
P10	0
Q10	0
R10	0
S10	0
U10	2
BA10	C
BB10	II
BD10	C
BE10	3
BF10	C
BG10	2
BH10	III
A11	C
B11	2
C11	2
D11	0
E11	2
F11	2
G11	2
H11	0
I11	0
J11	0
K11	0
L11	0
M11	0
N11	0
O11	0
P11	0
Q11	0
R11	0
S11	0
U11	3
BA11	C+
BB11	II+
BD11	C+
BE11	3+
BF11	C+
BG11	2+
BH11	III+
A12	D
B12	1
C12	2
D12	0
E12	2
F12	2
G12	2
H12	0
I12	1
J12	1
K12	0
L12	0
M12	0
N12	0
O12	0
P12	0
Q12	0
R12	0
S12	0
U12	4
BA12	D-
BB12	III-
BD12	D-
BE12	4-
BF12	D-
BG12	3-
BH12	IV-
A13	E
B13	0
C13	0
D13	0
E13	2
F13	2
G13	2
H13	1
I13	2
J13	2
K13	0
L13	0
N13	0
O13	0
P13	0
Q13	0
R13	0
S13	0
U13	5
BA13	D
BB13	III
BD13	D
BE13	4
BF13	D
BG13	3
BH13	IV
A14	F
B14	0
C14	0
D14	0
E14	2
F14	2
G14	2
H14	1
I14	2
J14	2
K14	0
L14	1
M14	2
N14	0
O14	0
P14	1
Q14	0
R14	0
S14	0
U14	6
BA14	D+
BB14	III+
BD14	D+
BE14	4+
BF14	D+
BG14	3+
BH14	IV+
A15	G
B15	0
C15	0
D15	0
E15	2
F15	2
G15	2
H15	1
I15	2
J15	2
K15	0
L15	1
M15	2
N15	0
O15	0
P15	2
Q15	0
R15	0
U15	7
BA15	E-
BB15	IV-
BD15	E-
BE15	5-
BF15	E-
BG15	4-
BH15	V-
A16	H
B16	0
C16	0
D16	0
E16	2
F16	2
G16	1
H16	1
I16	2
J16	2
K16	0
L16	1
M16	2
N16	0
O16	0
P16	0
Q16	0
R16	0
S16	0
U16	8
BA16	E
BB16	IV
BD16	E
BE16	5
BF16	E
BG16	4
BH16	V
BA17	E+
BB17	IV+
BD17	E+
BE17	5+
BF17	E+
BG17	4+
BH17	V+
B18	0
C18	0
D18	0
E18	1
F18	1
G18	1
H18	2
I18	2
J18	2
K18	3
L18	3
M18	3
N18	4
O18	4
P18	4
Q18	5
R18	5
S18	5
BA18	F-
BB18	V-
BD18	F-
BF18	F-
BG18	5-
BH18	VI-
BA19	F
BB19	V
BD19	F
BF19	F
BG19	5
BH19	VI
BA20	F+
BB20	V+
BD20	F+
BF20	F+
BG20	5+
BH20	VI+
B21	1
C21	+
D21	2
E21	+
F21	3
G21	+
H21	4
I21	+
J21	5
K21	+
BA21	G-
BB21	VI-
BD21	G-
BF21	G-
BG21	6-
BH21	≡≡≡
A22	A
B22	2
C22	2
D22	1
E22	0
F22	0
G22	0
H22	0
I22	0
J22	0
K22	0
L22	1
BA22	G
BB22	VI
BD22	G
BF22	G
BG22	6
BH22	R-
A23	B
B23	1
C23	2
D23	2
E23	2
F23	0
G23	0
H23	0
I23	0
J23	0
K23	0
L23	2
BA23	G+
BB23	VI+
BD23	G+
BF23	G+
BG23	6+
BH23	R
A24	C
B24	0
C24	0
D24	2
E24	2
F24	2
G24	2
H24	0
I24	0
J24	0
K24	0
L24	3
BA24	H-
BB24	VII-
BD24	H-
BF24	H-
BH24	R+
A25	D
B25	0
C25	0
D25	0
E25	1
F25	2
G25	2
H25	2
I25	1
J25	0
K25	0
L25	4
BA25	H
BB25	VII
BD25	H
BF25	H
BH25	C-
A26	E
B26	0
C26	0
D26	0
E26	0
F26	2
G26	2
H26	2
I26	2
J26	0
K26	0
L26	5
BA26	H+
BB26	VII+
BD26	H+
BF26	H+
BH26	C
A27	F
B27	0
C27	0
D27	0
E27	0
F27	0
G27	1
H27	2
I27	2
J27	1
K27	0
L27	6
BA27	I-
BF27	I-
BH27	C+
A28	G
B28	0
C28	0
D28	0
E28	0
F28	0
G28	0
H28	2
I28	2
J28	2
K28	0
L28	7
BA28	I
BF28	I
BH28	S-
A29	H
B29	0
C29	0
D29	0
E29	0
F29	0
G29	0
H29	1
I29	1
J29	2
K29	0
L29	8
BA29	I+
BF29	I+
BH29	S
L30	9
BH30	S+
B31	0
F31	1
J31	2
N31	3
R31	4
V31	5
BH31	P-
B32	A
C32	B
D32	C
E32	D
F32	E
G32	F
H32	V
I32	B
J32	G
K32	P
L32	V
M32	B
N32	G
O32	P
P32	V
Q32	B
R32	G
S32	P
T32	V
U32	B
V32	G
W32	P
X32	V
Y32	B
Z32	G
AA32	P
BH32	P
A33	A
B33	2
C33	2
D33	1
E33	0
F33	0
G33	0
H33	2
I33	1
J33	0
K33	0
L33	0
M33	0
N33	0
O33	0
P33	0
Q33	0
R33	0
S33	0
T33	0
U33	0
V33	0
W33	0
X33	0
Y33	0
Z33	0
AA33	0
AC33	1
BH33	P+
A34	B
B34	2
C34	2
D34	2
E34	1
F34	0
G34	0
H34	2
I34	2
J34	2
K34	2
L34	2
M34	1
N34	0
O34	0
P34	0
Q34	0
R34	0
S34	0
T34	0
U34	0
V34	0
W34	0
X34	0
Y34	0
Z34	0
AA34	0
AC34	2
A35	C
B35	1
C35	2
D35	2
E35	2
F35	1
G35	0
H35	2
I35	2
J35	2
K35	2
L35	2
M35	2
N35	2
O35	1
P35	2
Q35	2
R35	0
S35	0
T35	2
U35	1
V35	0
W35	0
X35	0
Y35	0
Z35	0
AA35	0
AC35	3
A36	D
B36	0
C36	1
D36	2
E36	2
F36	2
G36	1
H36	1
I36	2
J36	2
K36	2
L36	2
M36	2
N36	2
O36	2
P36	2
Q36	2
R36	2
S36	2
T36	2
U36	2
V36	0
W36	0
X36	1
Y36	1
Z36	0
AA36	0
AC36	4
A37	E
B37	0
C37	0
D37	0
E37	0
F37	2
G37	2
H37	0
I37	1
J37	2
K37	2
L37	1
M37	2
N37	2
O37	2
P37	1
Q37	2
R37	2
S37	2
T37	2
U37	2
V37	2
W37	2
X37	2
Y37	2
Z37	0
AA37	0
AC37	5
A38	F
B38	0
C38	0
D38	0
E38	0
F38	0
G38	1
H38	0
I38	0
J38	1
K38	2
L38	0
M38	1
N38	1
O38	2
P38	0
Q38	1
R38	2
S38	2
T38	1
U38	2
V38	2
W38	2
X38	1
Y38	2
Z38	1
AA38	1
AC38	6
A39	G
B39	0
C39	0
D39	0
E39	0
F39	0
G39	0
H39	0
I39	0
J39	0
K39	0
L39	0
M39	0
N39	0
O39	1
P39	0
Q39	0
R39	1
S39	2
T39	0
U39	0
V39	2
W39	2
X39	0
Y39	1
Z39	2
AA39	2
AC39	7
A40	H
B40	0
C40	0
D40	0
E40	0
F40	0
G40	0
H40	0
I40	0
J40	0
K40	0
L40	0
M40	0
N40	0
O40	0
P40	0
Q40	0
R40	0
S40	0
T40	0
U40	0
V40	0
W40	0
X40	0
Y40	0
Z40	2
AA40	2
AC40	8
E41	UK
H41	NL
D42	Minimal
E42	A
F42	1
H42	A
I42	1
D43	Limited
E43	B
F43	2
H43	B
I43	2
D44	Important
E44	C
F44	3
H44	C
I44	2
D45	Critical
E45	D
F45	4
H45	D
I45	4
E46	N
F46	1
H46	N
I46	1
D47	Contribut.
E47	C
F47	2
D48	Prime
E48	P
F48	4
H48	P
I48	4
D49	Remote
E49	R
F49	1
H49	V
I49	1
D50	Shared
E50	S
F50	3
H50	G
I50	3
D51	38	= D53
E51	43	= E53
F51	50
G51	57
H51	66
I51	76
J51	87
K51	100
L51	115
M51	132
N51	152
O51	175
P51	200
Q51	230
R51	264
S51	304
T51	350
U51	400
V51	460
W51	528
X51	608
Y51	700
Z51	800
AA51	920
AB51	1056
AC51	1216
AD51	1400
D52	1
E52	2
F52	3
G52	4
H52	5
I52	6
J52	7
K52	8
L52	9
M52	10
N52	11
O52	12
P52	13
Q52	14
R52	15
S52	16
T52	17
U52	18
V52	19
W52	20
X52	21
Y52	22
Z52	23
AA52	24
AB52	25
AC52	26
AD52	27
D53	38
E53	43
F53	50
G53	57
H53	66
I53	76
J53	87
K53	100
L53	115
M53	132
N53	152
O53	175
P53	200
Q53	230
R53	264
S53	304
T53	350
U53	400
V53	460
W53	528
X53	608
Y53	700
Z53	800
AA53	920
AB53	1056
AC53	1216
AD53	1400
A54	10
B54	16
C54	87
D54	0
E54	0
F54	0
G54	0
H54	0
I54	0
J54	0
K54	0
L54	0
M54	0
N54	0
O54	0
P54	0
Q54	0
R54	0
S54	0
T54	0
U54	0
V54	0
W54	0
X54	0
Y54	0
Z54	0
AA54	0
AB54	0
AC54	1
AD54	1
A55	12
B55	15
C55	76
D55	0
E55	0
F55	0
G55	0
H55	0
I55	0
J55	0
K55	0
L55	0
M55	0
N55	0
O55	0
P55	0
Q55	0
R55	0
S55	0
T55	0
U55	0
V55	0
W55	0
X55	0
Y55	1
Z55	1
AA55	2
AB55	2
AC55	2
AD55	2
A56	14
B56	14
C56	66
D56	0
E56	0
F56	0
G56	0
H56	0
I56	0
J56	0
K56	0
L56	0
M56	0
N56	0
O56	0
P56	0
Q56	0
R56	0
S56	0
T56	0
U56	0
V56	0
W56	0
X56	1
Y56	2
Z56	2
AA56	2
AB56	2
AC56	2
AD56	2
A57	16
B57	13
C57	57
D57	0
E57	0
F57	0
G57	0
H57	0
I57	0
J57	0
K57	0
L57	0
M57	0
N57	0
O57	0
P57	0
Q57	0
R57	0
S57	0
T57	0
U57	1
V57	2
W57	2
X57	2
Y57	2
Z57	2
AA57	2
AB57	2
AC57	1
AD57	1
A58	19
B58	12
C58	50
D58	0
E58	0
F58	0
G58	0
H58	0
I58	0
J58	0
K58	0
L58	0
M58	0
N58	0
O58	0
P58	0
Q58	0
R58	0
S58	1
T58	2
U58	2
V58	2
W58	2
X58	2
Y58	1
Z58	0
AA58	0
AB58	0
AC58	0
AD58	0
A59	22
B59	11
C59	43
D59	0
E59	0
F59	0
G59	0
H59	0
I59	0
J59	0
K59	0
L59	0
M59	0
N59	0
O59	0
P59	0
Q59	1
R59	2
S59	2
T59	2
U59	2
V59	2
W59	1
X59	0
Y59	0
Z59	0
AA59	0
AB59	0
AC59	0
AD59	0
A60	25
B60	10
C60	38
D60	0
E60	0
F60	0
G60	0
H60	0
I60	0
J60	0
K60	0
L60	0
M60	0
N60	0
O60	0
P60	1
Q60	2
R60	2
S60	2
T60	2
U60	1
V60	0
W60	0
X60	0
Y60	0
Z60	0
AA60	0
AB60	0
AC60	0
AD60	0
A61	29
B61	9
C61	33
D61	0
E61	0
F61	0
G61	0
H61	0
I61	0
J61	0
K61	0
L61	0
M61	0
N61	1
O61	2
P61	2
Q61	2
R61	2
S61	2
T61	1
U61	0
V61	0
W61	0
X61	0
Y61	0
Z61	0
AA61	0
AB61	0
AC61	0
AD61	0
A62	33
B62	8
C62	29
D62	0
E62	0
F62	0
G62	0
H62	0
I62	0
J62	0
K62	0
L62	1
M62	2
N62	2
O62	2
P62	2
Q62	1
R62	0
S62	0
T62	0
U62	0
V62	0
W62	0
X62	0
Y62	0
Z62	0
AA62	0
AB62	0
AC62	0
AD62	0
A63	38
B63	7
C63	25
D63	0
E63	0
F63	0
G63	0
H63	0
I63	0
J63	0
K63	1
L63	2
M63	2
N63	2
O63	1
P63	0
Q63	0
R63	0
S63	0
T63	0
U63	0
V63	0
W63	0
X63	0
Y63	0
Z63	0
AA63	0
AB63	0
AC63	0
AD63	0
A64	43
B64	6
C64	22
D64	0
E64	0
F64	0
G64	0
H64	0
I64	0
J64	1
K64	2
L64	2
M64	2
N64	1
O64	0
P64	0
Q64	0
R64	0
S64	0
T64	0
U64	0
V64	0
W64	0
X64	0
Y64	0
Z64	0
AA64	0
AB64	0
AC64	0
AD64	0
A65	50
B65	5
C65	19
D65	0
E65	0
F65	0
G65	0
H65	0
I65	1
J65	2
K65	2
L65	2
M65	1
N65	1
O65	0
P65	0
Q65	0
R65	0
S65	0
T65	0
U65	0
V65	0
W65	0
X65	0
Y65	0
Z65	0
AA65	0
AB65	0
AC65	0
AD65	0
A66	57
B66	4
C66	16
D66	0
E66	0
F66	0
G66	1
H66	2
I66	2
J66	2
K66	2
L66	1
M66	0
N66	0
O66	0
P66	0
Q66	0
R66	0
S66	0
T66	0
U66	0
V66	0
W66	0
X66	0
Y66	0
Z66	0
AA66	0
AB66	0
AC66	0
AD66	0
A67	66
B67	3
C67	14
D67	0
E67	1
F67	2
G67	2
H67	2
I67	2
J67	1
K67	0
L67	0
M67	0
N67	0
O67	0
P67	0
Q67	0
R67	0
S67	0
T67	0
U67	0
V67	0
W67	0
X67	0
Y67	0
Z67	0
AA67	0
AB67	0
AC67	0
AD67	0
A68	76
B68	2
C68	12
D68	1
E68	2
F68	2
G68	2
H68	1
I68	0
J68	0
K68	0
L68	0
M68	0
N68	0
O68	0
P68	0
Q68	0
R68	0
S68	0
T68	0
U68	0
V68	0
W68	0
X68	0
Y68	0
Z68	0
AA68	0
AB68	0
AC68	0
AD68	0
A69	87
B69	1
C69	10
D69	2
E69	2
F69	1
G69	0
H69	0
I69	0
J69	0
K69	0
L69	0
M69	0
N69	0
O69	0
P69	0
Q69	0
R69	0
S69	0
T69	0
U69	0
V69	0
W69	0
X69	0
Y69	0
Z69	0
AA69	0
AB69	0
AC69	0
AD69	0

===== SHEET: macro d'éval (xl/macrosheets/sheet1.xml) =====
D1	COMP
G1	IC
J1	PTSIC
M1	FINALITE
P1	-20
Q1	XX
R1	Lprof
T1	ChkKh
A2	1
B2	4
D2	1	= ARGUMENT("Connaissances",,E2)
E2	0
G2	1	= ARGUMENT("Cadre_réflexion",,H2)
H2	0
J2	1	= ARGUMENT("compétences",,K2)
K2	0
M2	1	= ARGUMENT("Latitude_action",,N2)
N2	0
P2	-7
Q2	XX
R2	1	= ARGUMENT("PsPct",,S2)
S2	0
T2	1	= ARGUMENT("C_Khd",,U2)
U2	D
A3	2
B3	5
D3	1	= ARGUMENT("Management",,E3)
E3	0
G3	1	= ARGUMENT("Exigence_problèmes",,H3)
H3	0
J3	1	= ARGUMENT("pourcic",,K3)
K3	0
M3	1	= ARGUMENT("Ampleur",,N3)
N3	0
P3	-6
Q3	P6
R3	1	= ARGUMENT("Sprof",,S3)
S3	0
T3	1	= ARGUMENT("C_Khb",,U3)
U3	V
A4	3
B4	6
D4	1	= ARGUMENT("Relations_humaines",,E4)
E4	0
G4	1	= SET.VALUE(H2,TRIM(H2))
J4	#N/A	= MATCH(K2,Valeurs_hay,1)-(MATCH(100,Valeurs_hay,1)-MATCH(pourcic,Valeurs_hay,1))
M4	1	= ARGUMENT("Impact",,N4)
N4	0
P4	-5
Q4	P5
R4	#N/A	= VLOOKUP(PsPct,X11:Y26,2)
T4	1	= ARGUMENT("C_KhHrs",,U4)
U4	1
A5	4
B5	7
D5	1	= SET.VALUE(E2,TRIM(E2))
G5	1	= SET.VALUE(H3,TRIM(H3))
J5	#N/A	= VLOOKUP(J4,pas_hay,2)
M5	1	= SET.VALUE(N2,TRIM(N2))
N5	R
O5	R
P5	-4
Q5	P4
R5	#N/A	= HLOOKUP(Sprof,Y8:AI9,2,FALSE)
T5	1	= RETURN(Validation!B5)
U5	1	= Validation!B5
A6	5
B6	8
D6	1	= SET.VALUE(E3,TRIM(E3))
G6	0	= RIGHT(Cadre_réflexion,1)
J6	1	= RETURN(IF(ISNA(J5),0,J5))
M6	1	= SET.VALUE(N3,TRIM(N3))
N6	C
O6	C
P6	-3
Q6	P3
R6	#N/A	= OFFSET(OFF_LP,R4,R5)
A7	6
B7	9
D7	1	= SET.VALUE(E4,TRIM(E4))
G7	0	= RIGHT(Exigence_problèmes,1)
J7	PROFIL
M7	1	= SET.VALUE(N4,TRIM(N4))
N7	S
O7	S
P7	-2
Q7	P2
R7	1	= RETURN(IF(ISNA(R5),"",R6))
Z7	V4
AA7	V3
AB7	V2
AC7	V1
AD7	E
AE7	P1
AF7	P2
AG7	P3
AH7	P4
A8	7
B8	10
D8	0	= SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Management),"N","T"),"+",""),"-","")
G8	0	= IF(OR(G6="-",G7="-"),-1)
J8	1	= ARGUMENT("pointsIC",,K8)
K8	0
M8	0	= RIGHT(N2,1)
N8	P
O8	P
P8	-1
Q8	P1
Y8	xx
Z8	A4
AA8	A3
AB8	A2
AC8	A1
AD8	L
AE8	P1
AF8	P2
AG8	P3
AH8	P4
AI8	xx
A9	8
B9	12
C9	Var_conn
D9	0	= RIGHT(Connaissances)
G9	0	= IF(OR(G7="+",G6="+"),1)
J9	1	= ARGUMENT("finalité",,K9)
K9	0
M9	0	= RIGHT(N3,1)
N9	N
P9	0
Q9	L
Y9	10
Z9	1
AA9	2
AB9	3
AC9	4
AD9	5
AE9	6
AF9	7
AG9	8
AH9	9
AI9	10
A10	9
B10	14
C10	Var_Mgt
D10	0	= RIGHT(Management)
G10	-16	= (CODE(UPPER(LEFT(Cadre_réflexion)))-64)
J10	#N/A	= VLOOKUP(MATCH(K9,Valeurs_hay,1)-MATCH(K8,Valeurs_hay,1),P1:Q21,2)
M10	0	= RIGHT(N4,1)
N10	1
P10	1
Q10	A1
Y10	OFF_LP
Z10	4
AA10	3
AB10	2
AC10	1
AD10	0
AE10	-1
AF10	-2
AG10	-3
AH10	-4
AI10	-5
A11	10
B11	16
D11	0	= IF(Var_conn="+",1,IF(Var_conn="-",-1,0))
G11	0	= LEFT(H3,1)*2
J11	#N/A	= J10
M11	0	= IF(M8="+",1,IF(M8="-",-1,0))
N11	2
P11	2
Q11	A2
S11	P4
T11	V
U11	R
X11	10
Y11	1
Z11	77-08-15
AA11	79-08-13
AB11	80-09-11
AC11	81-09-10
AD11	82-09-09
AE11	83-09-08
AF11	84-09-07
AG11	85-10-05
AH11	86-09-05
AI11	 
A12	11
B12	19
D12	0	= IF(Var_Mgt="+",1,IF(Var_Mgt="-",-1,0))
G12	-12	= G11+G10+MAX(0,G9+G8)+4
J12	1	= RETURN(IF(ISNA(J11),0,J11))
M12	0	= IF(M9="+",1,IF(M9="-",-1,0))
N12	3
P12	3
Q12	A3
S12	P3
T12	B
U12	C
X12	12
Y12	2
Z12	75-09-16
AA12	76-09-15
AB12	77-10-13
AC12	79-10-11
AD12	80-10-10
AE12	81-10-09
AF12	82-10-08
AG12	83-11-06
AH12	84-11-05
AI12	 
A13	12
B13	22
D13	0	= MAX(MIN(D11+D12,1),-1)
G13	#N/A	= VLOOKUP(G12,pas_hay,2)
M13	0	= IF(M10="+",1,IF(M10="-",-1,0))
N13	4
P13	4
Q13	A4
S13	P2
T13	G
U13	S
X13	14
Y13	3
Z13	72-10-18
AA13	74-10-16
AB13	76-10-14
AC13	76-11-13
AD13	78-11-11
AE13	79-11-10
AF13	80-11-09
AG13	81-12-07
AH13	82-12-06
AI13	 
A14	13
B14	25
D14	-32	= (CODE(UPPER(LEFT(Connaissances)))-64)*2
G14	1	= RETURN(IF(ISNA(G13),0,G13))
M14	0	= MAX(MIN(M11+M12+M13,1),-1)
N14	5
P14	5
Q14	A5
S14	P1
T14	P
U14	P
X14	16
Y14	4
Z14	69-11-20
AA14	70-12-18
AB14	72-12-16
AC14	74-12-14
AD14	76-12-12
AE14	76-13-11
AF14	77-13-10
AG14	79-13-08
AH14	80-13-07
AI14	 
A15	14
B15	29
D15	#N/A	= MATCH(UPPER(D8),C19:C31,0)*2
M15	-48	= (CODE(UPPER(LEFT(Latitude_action)))-64)*3
N15	6
P15	6
Q15	A6
S15	E
X15	19
Y15	5
Z15	66-12-22
AA15	68-13-19
AB15	70-13-17
AC15	72-13-15
AD15	72-14-14
AE15	74-14-12
AF15	75-14-11
AG15	76-15-09
AH15	77-15-08
AI15	 
A16	15
B16	33
D16	#N/A	= VALUE(LEFT(Relations_humaines,1))+D15+D14+D13+12
M16	2	= VLOOKUP(UPPER(LEFT(Ampleur,1)),N25:O34,2)*2
N16	7
P16	7
Q16	A7
S16	V1
X16	22
Y16	6
Z16	62-14-24
AA16	65-14-21
AB16	66-15-19
AC16	68-15-17
AD16	70-15-15
AE16	72-15-13
AF16	72-16-12
AG16	74-16-10
AH16	75-16-09
AI16	 
A17	16
B17	38
D17	#N/A	= VLOOKUP(D16,pas_hay,2)
M17	10	= VLOOKUP(UPPER(LEFT(N4,LEN(N4)-ABS(M13))),N36:O45,2,FALSE)*2
N17	8
P17	8
Q17	A8
S17	V2
X17	25
Y17	7
Z17	59-15-26
AA17	62-15-23
AB17	63-16-21
AC17	65-16-19
AD17	66-17-17
AE17	68-17-15
AF17	70-17-13
AG17	70-18-12
AH17	72-18-10
AI17	 
A18	17
B18	43
D18	1	= RETURN(IF(ISNA(D17),0,D17))
M18	0	= IF(ISNA(M16),SET.VALUE(M16,MATCH(SUBSTITUTE(SUBSTITUTE(Ampleur,"+",""),"-",""),C19:C31,0)*2))
P18	9
Q18	A9
S18	V3
X18	29
Y18	8
Z18	56-16-28
AA18	58-17-25
AB18	60-17-23
AC18	62-18-20
AD18	64-18-18
AE18	65-19-16
AF18	66-19-15
AG18	68-19-13
AH18	69-20-11
AI18	 
A19	18
B19	50
C19	T
D19	1
M19	1	= IF(ISNA(M17),SET.VALUE(M17,10-SUBSTITUTE(SUBSTITUTE(Impact,"+",""),"-","")*2))
P19	10
Q19	XX
S19	V4
X19	33
Y19	9
Z19	53-17-30
AA19	55-18-27
AB19	56-19-25
AC19	59-19-22
AD19	60-20-20
AE19	62-20-18
AF19	63-21-16
AG19	65-21-14
AH19	66-22-12
AI19	 
A20	19
B20	57
C20	I
D20	2
M20	-37	= SUM(M14:M17)-1
P20	100
Q20	XX
S20	V5
X20	38
Y20	10
Z20	49-19-32
AA20	51-19-30
AB20	53-20-27
AC20	55-21-24
AD20	56-22-22
AE20	59-22-19
AF20	60-23-17
AG20	62-23-15
AH20	62-24-14
AI20	 
A21	20
B21	66
C21	II
D21	3
M21	#N/A	= VLOOKUP(M20,pas_hay,2)
S21	V6
X21	43
Y21	11
Z21	45-20-35
AA21	47-21-32
AB21	49-22-29
AC21	52-22-26
AD21	54-23-23
AE21	55-24-21
AF21	56-25-19
AG21	58-25-17
AH21	59-26-15
AI21	 
A22	21
B22	76
C22	III
D22	4
M22	1	= RETURN(IF(ISNA(M21),0,M21))
S22	V7
X22	50
Y22	12
Z22	42-21-37
AA22	44-22-34
AB22	46-23-31
AC22	48-24-28
AD22	50-25-25
AE22	52-26-22
AF22	53-27-20
AG22	55-27-18
AH22	56-28-16
AI22	 
A23	22
B23	87
C23	IV
D23	5
X23	57
Y23	13
Z23	39-22-39
AA23	41-23-36
AB23	43-25-32
AC23	45-26-29
AD23	46-27-27
AE23	48-28-24
AF23	49-29-22
AG23	51-30-19
AH23	53-30-17
AI23	 
A24	23
B24	100
C24	V
D24	6
X24	66
Y24	14
Z24	36-23-41
AA24	38-24-38
AB24	40-26-34
AC24	42-27-31
AD24	44-28-28
AE24	45-29-26
AF24	46-31-23
AG24	47-32-21
AH24	49-32-19
AI24	 
A25	24
B25	115
C25	VI
D25	7
N25	0
O25	1
X25	76
Y25	15
Z25	32-25-43
AA25	34-26-40
AB25	36-28-36
AC25	38-29-33
AD25	40-30-30
AE25	42-31-27
AF25	43-32-25
AG25	44-34-22
AH25	45-35-20
AI25	 
A26	25
B26	132
C26	VII
D26	8
N26	1
O26	2
X26	87
Y26	16
Z26	29-26-45
AA26	32-27-41
AB26	33-29-38
AC26	35-30-35
AD26	36-32-32
AE26	38-33-29
AF26	40-34-26
AG26	41-36-23
AH26	42-37-21
AI26	 
A27	26
B27	152
C27	VIII
D27	9
N27	2
O27	3
A28	27
B28	175
C28	IX
D28	10
N28	3
O28	4
A29	28
B29	200
C29	X
D29	11
N29	4
O29	5
A30	29
B30	230
C30	XI
D30	12
N30	5
O30	6
A31	30
B31	264
C31	XII
D31	13
N31	6
O31	7
A32	31
B32	304
N32	7
O32	8
A33	32
B33	350
N33	8
O33	9
A34	33
B34	400
N34	N
O34	1
A35	34
B35	460
A36	35
B36	528
N36	I
O36	1
A37	36
B37	608
N37	II
O37	2
A38	37
B38	700
N38	III
O38	3
A39	38
B39	800
N39	IV
O39	4
A40	39
B40	920
N40	V
O40	5
A41	40
B41	1056
N41	VI
O41	6
A42	41
B42	1216
N42	R
O42	1
A43	42
B43	1400
N43	C
O43	2
A44	43
B44	1600
N44	S
O44	3
A45	44
B45	1840
N45	P
O45	4
A46	45
B46	2112
A47	46
B47	2432
A48	47
B48	2800
A49	48
B49	3200
A50	49
B50	3680
A51	50
B51	4224
A52	51
B52	4864	= B47*2
A53	52
B53	5600	= B48*2
A54	53
B54	6400	= B49*2
A55	54
B55	7360	= B50*2
A56	55
B56	8448	= B51*2
A57	56
B57	9728	= B52*2
A58	57
B58	11200	= B53*2
A59	58
B59	12800	= B54*2
A60	59
B60	14720	= B55*2
C60	T
F60	I
I60	II
L60	III
R60	V
B61	1
C61	2
D61	3
E61	1
F61	2
G61	3
H61	1
I61	2
J61	3
K61	1
L61	2
M61	3
P61	3
Q61	1
R61	2
S61	3
A62	a
B62	2
C62	0
D62	0
E62	1
F62	0
G62	0
H62	0
I62	0
J62	0
K62	0
L62	0
M62	0
O62	IV
P62	0
Q62	0
R62	0
S62	0
U62	1
A63	b
B63	2
C63	1
D63	0
E63	2
F63	1
G63	2
H63	0
I63	0
J63	0
K63	0
L63	0
M63	0
N63	1
O63	2
P63	0
Q63	0
R63	0
S63	0
U63	2
A64	c
B64	2
C64	2
D64	0
E64	2
F64	1
G64	2
H64	0
I64	0
J64	0
K64	0
L64	0
M64	0
N64	0
O64	0
P64	0
Q64	0
R64	0
S64	0
U64	3
A65	d
B65	0
C65	2
D65	0
E65	2
F65	1
G65	1
H65	0
I65	1
J65	2
K65	0
L65	0
M65	0
N65	0
O65	0
P65	0
Q65	0
R65	0
S65	0
U65	4
A66	e
B66	0
C66	0
D66	2
E66	2
F66	1
G66	1
H66	0
I66	2
J66	2
K66	0
L66	0
M66	1
N66	0
O66	0
P66	0
Q66	0
R66	0
S66	0
U66	5
A67	f
B67	0
C67	0
D67	0
E67	2
F67	1
G67	1
H67	0
I67	2
J67	2
K67	0
L67	0
M67	2
N67	0
O67	0
P67	1
Q67	0
R67	0
S67	0
U67	6
A68	g
B68	0
C68	0
D68	0
E68	1
F68	1
G68	2
H68	0
I68	2
J68	2
K68	0
L68	0
M68	2
N68	0
O68	0
P68	2
Q68	0
R68	0
S68	2
U68	7
A69	h
B69	0
C69	0
D69	0
E69	1
F69	1
G69	2
H69	0
I69	2
J69	1
K69	0
L69	0
M69	0
N69	0
O69	0
P69	0
Q69	0
R69	0
S69	0
U69	8
N70	0
O70	0
B71	6	= VLOOKUP(LEFT(Worksheet!#REF!,1),A62:U69,21)
N71	0
O71	0
B72	ii+	= Worksheet!#REF!
C72	ii-	= Worksheet!#REF!
```


## Лист Jobgrades TSV

```tsv
row	A	B	C	D	E	F	G	H	I	J	K	L	M	N	O
2													1	0	0
3													1 =IF(M2,1,IF(N2,2,3))		
4		Standard Hay Buckets	15% Steps	Client Specific					You chose the following jobgrades structure:						
5									Lower value	Mid point	Upper value	Jobgrade			
6		0	0	0					0	14 =INT(AVERAGE(I6,K6))	29 =I7-1	0			
7		30	16	100					30 =CHOOSE($M$3,B7,C7,MAX(I6,D7))	34 =INT(AVERAGE(I7,K7))	39	1			
8		40	19	200					40	43	46	2			
9		47	22	300					47	50	53	3			
10		54	25	400					54	58	62	4			
11		63	29	500					63	67	72	5			
12		73	33	600					73	78	84	6			
13		85	38	700					85	91	97	7			
14		98	43	800					98	105	113	8			
15		114	50	900					114	124	134	9			
16		135	57	1000					135	147	160	10			
17		161	66	1100					161	176	191	11			
18		192	76	1200					192	209	227	12			
19		228	87	1300					228	248	268	13			
20		269	100	1400					269	291	313	14			
21		314	115	1500					314	342	370	15			
22		371	132	1600					371	404	438	16			
23		439	152	1700					439	478	518	17			
24		519	175	1800					519	566	613	18			
25		614	200	1900					614	674	734	19			
26		735	230	2000					735	807	879	20			
27		880	264	2100					880	967	1055	21			
28		1056	304	2200					1056 =CHOOSE($M$3,B28,C28,MAX(I27,D28))	1158	1260	22			
29		1261	350	2300					1261	1384	1507	23			
30		1508	400	2400					1508	1654	1800	24			
31		1801	460	2500					1801	1970	2140	25			
32		2141	528	2600					2141	2345 =INT(AVERAGE(I32,K32))	2550 =I33-1	26			
33		2551	608	2700					2551	2785 =INT(AVERAGE(I33,K33))	3020 =I34-1	27			
34		3021	700	2800					3021	3300	3580	28			
35		3581	800	2900					3581	3915	4250	29			
36		4251	920	3000					4251	4655	5060	30			
37		5061	1056	3100					5061	5540	6020	31			
38		6021	1216	3200					6021	6590	7160	32			
39		7161	1400	3300					7161	7740	8320	33			
40		8321	1600	3400					8321	8980	9640	34			
41		9641	1840	3500					9641	10410	11180	35			
42		11181	2112	3600					11181	12080	12980	36			
43		12981	2432	3700					12981	14030	15080	37			
44		15081	2800	3800					15081	16310	17540	38			
45		17541	3200	3900					17541			XX
```


## Лист Matchcodes TSV

```tsv
row	A	B	C	D	E	F	G	H	I	J	K	L	M	N	O	P	Q	R	S	T	U	V	W	X	Y	Z	AA	AB
1	HAY-LEVEL	HAY-RANGE	HAY-MIDPOINT	FINANCE & ACCOUNTING		IT & TELECOMMUNICATIONS				HUMAN RESOURCES		LEGAL	MARKETING			SALES		CUSTOMER SERVICE		RESEARCH & DEVELOPMENT	ENGINEERING	LOGISTICS/SUPPLY CHAIN		PRODUCTION	ADMINISTRATION/SUPPORT/SERVICE			ENVIRONMENT/HEALTH/SAFETY
2				Accounting (FA)	Specialist (FB)	Design & Development (IA)	Infrastructure/
Support (IB)	Operations (IC)	Datamanagement (ID)	HR Generalist (HA)	HR Specialist (HB)	(L)	Market Research (MA)	Brand Management (MB)	Promotions (MC)	Support & Training (SA)	Individual Contributor & Sales Management (SB)	Technical (CA)	Non Technical (CB)	(R)	(E)	Acquisition (JA)	Internal Operations & Delivery (JB)	(P)	Clerical Services (AA)	Secretarial (AB)	Translation (AC)	(W)
3	21	878 - 1055	954			Head of Information Technology
(i9001)																						
4	20	735 - 879	805																					Superintendent III/Production Manager (P0349)				
5	19	614 - 734	677	Manager General Accounting
 (F0008M)	 Financial Sub-section Mgr.
(F7442)	Manager Systems & Programming 
(i7443)	Network Integrator (LAN/WAN) 
(i0079M)	Computer Services Manager II (i5153)				Senior legal Advisor (L0154)		Brand/Product
Manager IV
(M0178)			Regional Sales Manager (S0209M)	Manager Customer Service (C0223M)		Scientist/Researcher V (R0248)			Manager Logistics Operations (J0329M)	Plant Manager (P0350)                                            Superintendent II/Production Manager (P0348)				
6	18	519 - 613	571		Senior Financial Analyst (F0026)		Network Architect (i0080)                         Network Operations Manager 
(i0062M)		Manager Database (i0075M)                                       	Human Resources Manager
(H0106M)	Training & Development Manager (H0110L)                          Compensation & Benefits Manager (H7446)	Legal Advisor
(L0153)	Market Research Manager
(M0173M)	Brand/Product Manager III
(H0177)						Scientist/Researcher IV                                 (R0237)                                    Research & Development Supervisor II (R0240)	Engineer V (E0266)	Purchasing Manager (J0323L)	Manager Production Control (J0292M)	Superintendent I/Production Manager (P0347)				Environmental Health & Safety Manager (W7459)
7	17	439 - 518	479		 Financial Analyst II (F0025)
Controller (F00231)  	Senior Systems Analyst                          (i0048)                                             ERP Configurer (i0093)	Group Ware Specialist (i7445)	Computer Services Manager I (i5137)	Senior Data Security Specialist (i0082M)                                    Database Analyst III (i0074)                                      Database Architect
(i5237)	Personnel Manager II (H0104)	Recruitment Manager                (H0119 L)                                          Employee/Labour Relations Representative III (H0120)	Principal Legal Executive 
(L0162)	Market Analyst/Business Development Officer III (M4012)	Brand/Product Manager II
(M4009)	Market Communication Representative (M0175)                                Public Relations Representative (M0403)	Sales Training Manager (S6220) 	National Accounts/Key Accounts Manager
 (S0202)
Area/District Sales Manager 
(S0215)	Technical Customer Service Teamleader (C0224M)		Scientist/Researcher III                             (R0236)                                    Research & Development Supervisor I (R0239)	Engineer IV (E0265)			General Supervisor II (P0346)				Quality Assurance Manager (W7460)
8	16	371 - 438	406	Accounting Supervisor II/Chief Accountant II (F0007M)                          
	       Financial Analyst III
(F0025a)	Principal Analyst Programmer (i7444)                                                        Systems Analyst (i0047)	Network Planning Analyst (i0083)                         Network Administrator (multiple platform LAN/WAN) (i0078)      	Senior Information Center  (or End User Computing Support) Analyst (i0056)	Database Analyst II (i0073)                                     Database Administrator (i0053)	Personnel Manager I (H0103)	Training & Development Specialist II (H7447)                          Compensation & Benefits Specialist (H7448)	Senior Legal Executive (L4704)	Market Analyst/Business Development Officer II (M0172)	Brand/Product Manager I
(M0185)	Promotions Manager (M4013)		Sales Representative III (S0205)			Scientist/Researcher II (R0235)	Engineer III (E0264)	Purchasing Agent (J0322M)	Traffic Manager (L0295M)                                                  Warehouse Manager (J0294M)	Unit Supervisor IV (P7456)                                     General Supervisor I (P0345)                             				Environmental Health & Safety Professional (W7461)
9	15	314 - 370	342	Accounting Supervisor I (F0022)                 	 Financial Analyst I (F0024)	Analyst Programmer IV (i5119)	Network Administrator                       (single platform LAN/WAN) 
(i0077)      		Database Analyst I (i0072)		Recruitment Officer (H7449)	Legal Executive (L0163)	Market Analyst/Business Development Officer I (M4014)	Assistant Brand/Product Manager
(M4007)	Public Relations Assistant
(M0402)		Sales Representative II (S0204)	Technical Customer Service Rep. II (C0220M)	Customer Service Teamleader (C0222M)	Scientist/Researcher I (R0234)	Engineer II (E0263)		Production Planner (J0291M)	Unit Supervisor III (P0344) 	Office Manager III (A7458)			
10	14	269 - 313	291	Accountant III (F0004)		Analyst Programmer III (i5120)	Network Administrator (LAN) (i0061)      	Information Systems                (or End User Computing Support) Analyst (i0055)			Training & Development Specialist I (H0108)                          Compensation & Benefits Analyst (H7450)		Marketing Research Analyst II
(M7451)			Telesales Supervisor (S7453)
Sales Trainer
(S6222)	Sales Representative I (S0203)	Technical Customer Service Rep. I (C0221M)			Engineer I (E0262)	Buyer II (J0321)		Unit Supervisor II (P0343) 	Administrative Assistant II (A5010)                                         Office Manager II (A7055)     	Secretary VI (reports to CEO) (A5004)	Translator II (A7733)	
11	13	228 - 268	252	Accountant II (F0003)		Analyst Programmer II (i5121)				Human Resources Administrator 
(H0102)	Recruiter
(H0118)		Marketing Research Analyst I
(M7452)		Promotions Assistant (M4016)		Sales Representative (S7455)		Customer Service Rep. III 
(C0217M)	Researcher/Technician (R0232)	Design Drafter (E4120)	Buyer I (J0324)	Warehouse Supervisor (J0293M)	Unit Supervisor I (P0342) 	Administrative Assistant I (A7056)                             Office Manager I (A5009)     	Secretary V (A5005)	Translator I (A7734)	Industrial Nurse (W0124)
12	12	192 - 227	208	Accountant I (F0002)		Analyst Programmer I (i5122)		PC Maintenance Technician (i0095)								Telesales Operator (S1609)			Customer Service Rep. II 
(C0218M)	Laboratory Technician (R4107)	Drafter (E4122)                                    Electronic Technician II (E4123)			Maintenance Technician (P7457)	General Clerk V (A1087)	Secretary IV (A7054)		
13	11	161 - 191	173	Accounts Clerk IV (F1040)			Help Desk Analyst (i5150)												Customer Service Rep. I (C0219M)		Electronic Technician I (E4124)			Production/Process Operator V (P4204)	General Clerk IV (A1088)	Secretary III (A5006)		
14	10	135 - 160	151	Accounts Clerk III (F1039)												Merchandiser
(S7454)									General Clerk III (A1089)                                       Receptionist/Telephonist II (A7736)	Secretary II (A5007)		
15	9	114 - 134 	125	Accounts Clerk II (F1038)																				Production/Process Operator IV (P4212)	General Clerk II (A1090)                                       Chauffeur II (A5011)	Secretary I (A5008)		
16	8	98 - 113	104						Data Entry Operator II
(i9002)														Stock Clerk (J7752)	Production/Process Operator III (P4216)	General Clerk I (A1091)                                       Receptionist/
Switchboard
 Operator (A7057)                                                   Chauffeur I (A5012)			
17	7	85 - 97	90																				Forklift Operator (J7756)
```


## Лист Validation TSV

```tsv
row	A	B	C	D	E	F	G	H	I	J	K	L	M	N	O	P	Q	R	S	T	U	V	W	X	Y	Z	AA	AB	AC	AD	AE	AF	AG	AH	AI	AJ	AK	AL	AM	AN	AO	AP	AQ	AR	AS	AT	AU	AV	AW	AX	AY	AZ	BA	BB	BC	BD	BE	BF	BG	BH
1																																																					KH			PS		ACC		
2																																																						Khb	KhHrs	PSF	PSC	AcF	AcM	AcI
3	D =C_Khd																																																				A-	T-	1	A-	1-	A-	N-	I-
4	V =C_Khb																																																				A	T	2	A	1	A	N	I
5	1 =C_KhHrs	0 =OFFSET(Validation!$A$8,VLOOKUP(UPPER(LEFT(A3,1)),Validation!$A$9:$U$16,21),HLOOKUP(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(A4),"+",""),"-",""),"N","T"),Validation!$B$7:$S$18,12,FALSE)*3+VALUE(LEFT(A5,1)))																																																			A+	T+	3	A+	1+	A+	N+	I+
6																																																					B-	I-		B-	2-	B-	1-	II-
7		T			I			II			III			IV			V																																				B	I		B	2	B	1	II
8		1	2	3	1	2	3	1	2	3	1	2	3	1	2	3	1	2	3																																		B+	I+		B+	2+	B+	1+	II+
9	A	2	1	0	1	0	0	0	0	0	0	0	0	0	0	0	0	0	0		1																																C-	II-		C-	3-	C-	2-	III-
10	B	2	2	0	2	2	1	0	0	0	0	0	0	0	0	0	0	0	0		2																																C	II		C	3	C	2	III
11	C	2	2	0	2	2	2	0	0	0	0	0	0	0	0	0	0	0	0		3																																C+	II+		C+	3+	C+	2+	III+
12	D	1	2	0	2	2	2	0	1	1	0	0	0	0	0	0	0	0	0		4																																D-	III-		D-	4-	D-	3-	IV-
13	E	0	0	0	2	2	2	1	2	2	0	0		0	0	0	0	0	0		5																																D	III		D	4	D	3	IV
14	F	0	0	0	2	2	2	1	2	2	0	1	2	0	0	1	0	0	0		6																																D+	III+		D+	4+	D+	3+	IV+
15	G	0	0	0	2	2	2	1	2	2	0	1	2	0	0	2	0	0			7																																E-	IV-		E-	5-	E-	4-	V-
16	H	0	0	0	2	2	1	1	2	2	0	1	2	0	0	0	0	0	0		8																																E	IV		E	5	E	4	V
17																																																					E+	IV+		E+	5+	E+	4+	V+
18		0	0	0	1	1	1	2	2	2	3	3	3	4	4	4	5	5	5																																		F-	V-		F-		F-	5-	VI-
19																																																					F	V		F		F	5	VI
20																																																					F+	V+		F+		F+	5+	VI+
21		1	+	2	+	3	+	4	+	5	+																																										G-	VI-		G-		G-	6-	≡≡≡
22	A	2	2	1	0	0	0	0	0	0	0	1																																									G	VI		G		G	6	R-
23	B	1	2	2	2	0	0	0	0	0	0	2																																									G+	VI+		G+		G+	6+	R
24	C	0	0	2	2	2	2	0	0	0	0	3																																									H-	VII-		H-		H-		R+
25	D	0	0	0	1	2	2	2	1	0	0	4																																									H	VII		H		H		C-
26	E	0	0	0	0	2	2	2	2	0	0	5																																									H+	VII+		H+		H+		C
27	F	0	0	0	0	0	1	2	2	1	0	6																																									I-					I-		C+
28	G	0	0	0	0	0	0	2	2	2	0	7																																									I					I		S-
29	H	0	0	0	0	0	0	1	1	2	0	8																																									I+					I+		S
30												9																																																S+
31		0				1				2				3				4				5																																						P-
32		A	B	C	D	E	F	V	B	G	P	V	B	G	P	V	B	G	P	V	B	G	P	V	B	G	P																																	P
33	A	2	2	1	0	0	0	2	1	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0		1																															P+
34	B	2	2	2	1	0	0	2	2	2	2	2	1	0	0	0	0	0	0	0	0	0	0	0	0	0	0		2																															
35	C	1	2	2	2	1	0	2	2	2	2	2	2	2	1	2	2	0	0	2	1	0	0	0	0	0	0		3																															
36	D	0	1	2	2	2	1	1	2	2	2	2	2	2	2	2	2	2	2	2	2	0	0	1	1	0	0		4																															
37	E	0	0	0	0	2	2	0	1	2	2	1	2	2	2	1	2	2	2	2	2	2	2	2	2	0	0		5																															
38	F	0	0	0	0	0	1	0	0	1	2	0	1	1	2	0	1	2	2	1	2	2	2	1	2	1	1		6																															
39	G	0	0	0	0	0	0	0	0	0	0	0	0	0	1	0	0	1	2	0	0	2	2	0	1	2	2		7																															
40	H	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	2	2		8																															
41					UK			NL																																																				
42				Minimal	A	1		A	1																																																			
43				Limited	B	2		B	2																																																			
44				Important	C	3		C	2																																																			
45				Critical	D	4		D	4																																																			
46					N	1		N	1																																																			
47				Contribut.	C	2																																																						
48				Prime	P	4		P	4																																																			
49				Remote	R	1		V	1																																																			
50				Shared	S	3		G	3																																																			
51				38 =D53	43 =E53	50	57	66	76	87	100	115	132	152	175	200	230	264	304	350	400	460	528	608	700	800	920	1056	1216	1400																														
52				1	2	3	4	5	6	7	8	9	10	11	12	13	14	15	16	17	18	19	20	21	22	23	24	25	26	27																														
53				38	43	50	57	66	76	87	100	115	132	152	175	200	230	264	304	350	400	460	528	608	700	800	920	1056	1216	1400																														
54	10	16	87	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	1	1																														
55	12	15	76	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	1	1	2	2	2	2																														
56	14	14	66	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	1	2	2	2	2	2	2																														
57	16	13	57	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	1	2	2	2	2	2	2	2	1	1																														
58	19	12	50	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	1	2	2	2	2	2	1	0	0	0	0	0																														
59	22	11	43	0	0	0	0	0	0	0	0	0	0	0	0	0	1	2	2	2	2	2	1	0	0	0	0	0	0	0																														
60	25	10	38	0	0	0	0	0	0	0	0	0	0	0	0	1	2	2	2	2	1	0	0	0	0	0	0	0	0	0																														
61	29	9	33	0	0	0	0	0	0	0	0	0	0	1	2	2	2	2	2	1	0	0	0	0	0	0	0	0	0	0																														
62	33	8	29	0	0	0	0	0	0	0	0	1	2	2	2	2	1	0	0	0	0	0	0	0	0	0	0	0	0	0																														
63	38	7	25	0	0	0	0	0	0	0	1	2	2	2	1	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0																														
64	43	6	22	0	0	0	0	0	0	1	2	2	2	1	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0																														
65	50	5	19	0	0	0	0	0	1	2	2	2	1	1	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0																														
66	57	4	16	0	0	0	1	2	2	2	2	1	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0																														
67	66	3	14	0	1	2	2	2	2	1	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0																														
68	76	2	12	1	2	2	2	1	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0																														
69	87	1	10	2	2	1	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0
```


## Лист Matrix TSV

```tsv
row
```
