import math, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from geo import OBST, SPOTS, NORMAL
from model import exposure, local_wind_factor
fig = plt.figure(figsize=(13,6.2)); fig.patch.set_facecolor("white")
ax = fig.add_subplot(1,2,1)
for n,g in OBST.items():
    xs,ys = zip(*g.coords); ax.plot(xs,ys,color="#333" if "Costa" in n else "#b5651d",lw=1.5 if "Costa" in n else 3)
cols={"Biologia":"#1f77b4","Yacht":"#d62728"}
for s,p in SPOTS.items():
    ax.plot(*p,"o",color=cols[s],ms=10); ax.annotate(s,p,xytext=(8,6),textcoords="offset points",color=cols[s],fontsize=11,weight="bold")
    for az in range(0,360,3):
        e = exposure(s,az,30)
        if e>0.05:
            L=350*e; ax.plot([p[0],p[0]+L*math.sin(math.radians(az))],[p[1],p[1]+L*math.cos(math.radians(az))],color=cols[s],alpha=.25,lw=1)
ax.annotate("Escollera Norte",(700,-760),fontsize=9,color="#b5651d"); ax.annotate("Biología",(200,300),fontsize=9,color="#b5651d")
ax.arrow(-900,700,0,180,head_width=50,color="k"); ax.text(-925,920,"N")
ax.set_xlim(-1000,1400); ax.set_ylim(-1100,1000); ax.set_aspect("equal"); ax.set_title("Playa Grande (geometría OSM)\nabanicos = cuánto swell le llega a cada pico por dirección",fontsize=10)
ax.set_xticks([]); ax.set_yticks([])
ax2 = fig.add_subplot(2,2,2); ax3 = fig.add_subplot(2,2,4)
dirs=list(range(0,225,5))
for s in SPOTS: ax2.plot(dirs,[exposure(s,d,30) for d in dirs],color=cols[s],lw=2.5,label=s)
ax2.set_xticks(range(0,225,45)); ax2.set_xticklabels(["N","NE","E","SE","S"]); ax2.set_ylabel("factor de altura"); ax2.set_title("SWELL: quién recibe más ola según dirección",fontsize=10); ax2.legend(); ax2.grid(alpha=.3)
wd=list(range(0,361,5))
for s in SPOTS: ax3.plot(wd,[local_wind_factor(s,d) for d in wd],color=cols[s],lw=2.5)
ax3.axvspan(215,345,color="green",alpha=.08); ax3.text(250,0.85,"offshore\n(limpio)",color="green",fontsize=9)
ax3.set_xticks(range(0,361,45)); ax3.set_xticklabels(["N","NE","E","SE","S","SO","O","NO","N"]); ax3.set_ylabel("viento que ensucia"); ax3.set_title("VIENTO: más bajo = más reparado",fontsize=10); ax3.grid(alpha=.3)
plt.tight_layout(); plt.savefig("geometria.png",dpi=130); print("geometria.png")
