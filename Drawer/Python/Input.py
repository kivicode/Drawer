r11 = Rect([10,10],50,50, color=(0,0,255))
r12 = Rect([36,36],50,50, color=(0,0,255))

r21 = Rect([110,10],50,50, color=(0,0,255))
r22 = Rect([136,36],50,50, color=(0,0,255))

r31 = Rect([10,110],50,50, color=(0,0,255))
r32 = Rect([36,136],50,50, color=(0,0,255))

r41 = Rect([110,110],50,50, color=(0,0,255))
r42 = Rect([136,136],50,50, color=(0,0,255))

r1 = Rect([10,10],50,50)
r2 = Rect([36,36],50,50)
r1.CONCAT(r2)

r3 = Rect([110,10],50,50)
r4 = Rect([136,36],50,50)
r3.AND(r4)

r5 = Rect([10,110],50,50)
r6 = Rect([36,136],50,50)
r5.CUTA(r6)

r7 = Rect([110,110],50,50)
r8 = Rect([136,136],50,50)
r7.CUTB(r8)