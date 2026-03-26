import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

NAVY = '#1a1a4e'
GOLD = '#D4AF37'
RED = '#C0392B'
GREEN = '#27AE60'
BLUE = '#2980B9'
ORANGE = '#E67E22'
GRAY = '#7F8C8D'
BG = '#FAFAFA'

plt.rcParams.update({
    'figure.facecolor': 'white', 'axes.facecolor': BG,
    'font.family': 'serif', 'font.size': 11,
    'figure.dpi': 150, 'savefig.dpi': 300,
})

FIG = 'figures'
os.makedirs(FIG, exist_ok=True)

# Fig 1: Differential Spectrum
curves =  ['15a1','11a1','27a1','32a1','14a1','43a1','58a1','61a1','53a1','37a1','389a1','433a1','5077a1']
ranks =   [0,0,0,0,0,1,1,1,1,1,2,2,3]
max_sh =  [0.002,0.011,0.021,0.021,0.038,0.006,0.006,0.006,0.020,0.246,0.029,0.029,0.029]
shifted = [0,1,15,11,23,0,0,0,10,122,19,19,19]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
fig.suptitle('Differential Spectrum: spec(H_D^E) - spec(H_D)', fontsize=15, fontweight='bold', color=NAVY)
colors = [GREEN if r==0 else (BLUE if r==1 else (ORANGE if r==2 else RED)) for r in ranks]
x = np.arange(len(curves))
ax1.bar(x, max_sh, color=colors, edgecolor=NAVY, linewidth=0.5, alpha=0.85)
ax1.set_xticks(x); ax1.set_xticklabels(curves, rotation=45, ha='right', fontsize=8)
ax1.set_ylabel('Max eigenvalue shift'); ax1.set_title('Maximum Spectral Shift per Curve')
ax1.annotate('37a1: 0.246\n(10x outlier)', xy=(9, 0.246), xytext=(6, 0.20),
            fontsize=10, fontweight='bold', color=NAVY,
            arrowprops=dict(arrowstyle='->', color=NAVY),
            bbox=dict(boxstyle='round', facecolor=GOLD, alpha=0.2))
ax2.bar(x, shifted, color=colors, edgecolor=NAVY, linewidth=0.5, alpha=0.85)
ax2.set_xticks(x); ax2.set_xticklabels(curves, rotation=45, ha='right', fontsize=8)
ax2.set_ylabel('Eigenvalues shifted > 0.01'); ax2.set_title('Count of Shifted Eigenvalues')
ax2.annotate('122', xy=(9, 122), xytext=(7, 100), fontsize=11, fontweight='bold', color=NAVY,
            arrowprops=dict(arrowstyle='->', color=NAVY))
legend_items = [mpatches.Patch(color=GREEN, label='Rank 0'), mpatches.Patch(color=BLUE, label='Rank 1'),
                mpatches.Patch(color=ORANGE, label='Rank 2'), mpatches.Patch(color=RED, label='Rank 3')]
ax1.legend(handles=legend_items, fontsize=9, loc='upper left')
plt.tight_layout(); plt.savefig(f'{FIG}/differential_spectrum.png', bbox_inches='tight'); plt.close()
print('[OK] differential_spectrum.png')

# Fig 2: Eigenvalue Comparison
fig, ax = plt.subplots(figsize=(9, 5))
eigs_32 = [-1.33793,-1.10090,-0.98997,-0.74393,-0.63673]
eigs_37 = [-1.33831,-1.10096,-0.99037,-0.74624,-0.64037]
eigs_389 = [-1.33794,-1.10090,-0.98998,-0.74399,-0.63682]
x_pos = np.arange(5); w = 0.25
ax.bar(x_pos-w, eigs_32, w, color=GREEN, edgecolor=NAVY, linewidth=0.5, label='32a1 (rank 0)')
ax.bar(x_pos, eigs_37, w, color=BLUE, edgecolor=NAVY, linewidth=0.5, label='37a1 (rank 1)')
ax.bar(x_pos+w, eigs_389, w, color=ORANGE, edgecolor=NAVY, linewidth=0.5, label='389a1 (rank 2)')
ax.set_xticks(x_pos); ax.set_xticklabels(['l0','l1','l2','l3','l4'], fontsize=12)
ax.set_ylabel('Eigenvalue'); ax.set_title('Low-Lying Eigenvalues of H_D^E at N=500 (dim 11,500)', fontsize=13, fontweight='bold', color=NAVY)
ax.legend(fontsize=10)
plt.tight_layout(); plt.savefig(f'{FIG}/eigenvalue_comparison.png', bbox_inches='tight'); plt.close()
print('[OK] eigenvalue_comparison.png')

# Fig 3: Hasse Bound
fig, ax = plt.subplots(figsize=(8, 5))
primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]
ap_37 = [0,-3,-2,-4,2,-5,4,-2,1,-7,-3,2,-9,-8,9]
ratios = [abs(a)/(2*p**0.5) if p > 0 else 0 for p,a in zip(primes, ap_37)]
ax.bar(range(len(primes)), ratios, color=NAVY, alpha=0.7, edgecolor=NAVY)
ax.axhline(y=1.0, color=RED, linewidth=2, linestyle='--', label='Hasse bound')
ax.set_xticks(range(len(primes))); ax.set_xticklabels([str(p) for p in primes], fontsize=9)
ax.set_xlabel('Prime p'); ax.set_ylabel('|a_p| / (2 sqrt(p))')
ax.set_title('Hasse Bound Verification: 37a1', fontsize=13, fontweight='bold', color=NAVY)
ax.set_ylim(0, 1.2); ax.legend(fontsize=11)
ax.annotate('ALL below bound\n(unconditional)', xy=(0.5, 0.5), xycoords='axes fraction',
           ha='center', fontsize=12, fontweight='bold', color=GREEN,
           bbox=dict(boxstyle='round', facecolor=GREEN, alpha=0.15))
plt.tight_layout(); plt.savefig(f'{FIG}/hasse_bound.png', bbox_inches='tight'); plt.close()
print('[OK] hasse_bound.png')

# Fig 4: Gap Analysis
fig, ax = plt.subplots(figsize=(8, 5))
gap_names = ['32a1 (r=0)', '37a1 (r=1)', '389a1 (r=2)']
gaps = [0.24604, 0.24413, 0.24599]
colors_gap = [GREEN, BLUE, ORANGE]
bars = ax.bar(gap_names, gaps, color=colors_gap, edgecolor=NAVY, linewidth=1.5, width=0.5)
ax.set_ylabel('gap_23'); ax.set_title('Spectral Gap Between 3rd and 4th Eigenvalues', fontsize=13, fontweight='bold', color=NAVY)
ax.set_ylim(0.243, 0.247)
for bar, val in zip(bars, gaps):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.0002, f'{val:.5f}', ha='center', fontsize=11, fontweight='bold', color=NAVY)
ax.annotate('Rank-1 has SMALLER gap\n(eigenvalue clustering)', xy=(1, 0.24413), xytext=(1.8, 0.2445),
           fontsize=10, color=NAVY, arrowprops=dict(arrowstyle='->', color=NAVY),
           bbox=dict(boxstyle='round', facecolor=GOLD, alpha=0.2))
plt.tight_layout(); plt.savefig(f'{FIG}/gap_analysis.png', bbox_inches='tight'); plt.close()
print('[OK] gap_analysis.png')

# Fig 5: Proof Chain
fig, ax = plt.subplots(figsize=(12, 5))
ax.set_xlim(0, 12); ax.set_ylim(0, 5); ax.axis('off')
ax.set_title('BSD Proof Architecture: (A*) => BSD', fontsize=15, fontweight='bold', color=NAVY)
boxes = [
    (1.5, 3.5, 'Kato-Rellich\n+ Hasse', GREEN, 'PROVED'),
    (4.5, 3.5, 'Self-adjoint\nH_D^E', GREEN, 'PROVED'),
    (7.5, 3.5, '(A*) GUE\nuniversality', ORANGE, 'CONDITIONAL'),
    (10.5, 3.5, 'D^E(s)=e^b xi(E,s)', ORANGE, 'CONDITIONAL'),
    (4.5, 1.2, 'Kolyvagin+GZ\nrank <= 1', GREEN, 'PROVED'),
    (7.5, 1.2, 'rank = spec rank', ORANGE, 'CONDITIONAL'),
    (10.5, 1.2, 'BSD', GOLD, 'RESULT'),
]
for bx, by, text, color, status in boxes:
    w, h = 2.5, 1.2
    rect = mpatches.FancyBboxPatch((bx-w/2, by-h/2), w, h, boxstyle='round,pad=0.15',
                                   facecolor=color, alpha=0.25, edgecolor=color, linewidth=2)
    ax.add_patch(rect)
    ax.text(bx, by+0.05, text, ha='center', va='center', fontsize=8, fontweight='bold', color=NAVY)
    ax.text(bx, by-h/2-0.12, status, ha='center', va='top', fontsize=6, color=color, fontstyle='italic')
akw = dict(arrowstyle='->', color=NAVY, lw=1.5)
ax.annotate('', xy=(3.25,3.5), xytext=(2.75,3.5), arrowprops=akw)
ax.annotate('', xy=(6.25,3.5), xytext=(5.75,3.5), arrowprops=akw)
ax.annotate('', xy=(9.25,3.5), xytext=(8.75,3.5), arrowprops=akw)
ax.annotate('', xy=(9.25,1.2), xytext=(8.75,1.2), arrowprops=akw)
ax.annotate('', xy=(7.5,2.8), xytext=(7.5,1.8), arrowprops=dict(arrowstyle='->',color=ORANGE,lw=1,linestyle='--'))
legend_items = [mpatches.Patch(color=GREEN, alpha=0.4, label='Proved'), mpatches.Patch(color=ORANGE, alpha=0.4, label='Conditional'), mpatches.Patch(color=GOLD, alpha=0.4, label='Result')]
ax.legend(handles=legend_items, loc='lower left', fontsize=9)
plt.tight_layout(); plt.savefig(f'{FIG}/bsd_proof_chain.png', bbox_inches='tight'); plt.close()
print('[OK] bsd_proof_chain.png')

# Fig 6: Rank-2/3 Saturation
fig, ax = plt.subplots(figsize=(8, 5))
rank_labels = ['Rank 0\n(5 curves)', 'Rank 1\n(5 curves)', 'Rank 2\n(2 curves)', 'Rank 3\n(1 curve)']
mean_shifts = [np.mean([0.002,0.011,0.021,0.021,0.038]), np.mean([0.006,0.006,0.006,0.020,0.246]),
               np.mean([0.029,0.029]), np.mean([0.029])]
max_shifts = [0.038, 0.246, 0.029, 0.029]
x_r = np.arange(4); w = 0.3
ax.bar(x_r-w/2, mean_shifts, w, color=[GREEN,BLUE,ORANGE,RED], edgecolor=NAVY, linewidth=0.5, alpha=0.6, label='Mean shift')
ax.bar(x_r+w/2, max_shifts, w, color=[GREEN,BLUE,ORANGE,RED], edgecolor=NAVY, linewidth=1.5, alpha=0.9, label='Max shift')
ax.set_xticks(x_r); ax.set_xticklabels(rank_labels, fontsize=10)
ax.set_ylabel('Eigenvalue Shift Magnitude'); ax.set_title('Perturbation Magnitude vs Algebraic Rank', fontsize=13, fontweight='bold', color=NAVY)
ax.legend(fontsize=10)
ax.annotate('Saturation at\nrank >= 2', xy=(2.5, 0.029), xytext=(2.5, 0.10),
           fontsize=10, fontweight='bold', color=NAVY, ha='center',
           arrowprops=dict(arrowstyle='->', color=NAVY),
           bbox=dict(boxstyle='round', facecolor=GOLD, alpha=0.2))
plt.tight_layout(); plt.savefig(f'{FIG}/rank_saturation.png', bbox_inches='tight'); plt.close()
print('[OK] rank_saturation.png')

print(f'\nDone! {len(os.listdir(FIG))} figures generated.')
