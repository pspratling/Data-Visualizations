import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


#constant that defines how many pairs of random numbers to generate
iterations = 1000
#initializing random seed
np.random.seed(15)

#generating random points (x,y) sampled from U(-1,1)
rand_pts = np.random.rand(iterations, 2)*2 - 1
#finding points in the unit circle (must satisfy x^2 + y^2 < 1)
is_in_circle = np.square(rand_pts[:,0]) + np.square(rand_pts[:,1]) <= 1
pts_inside = rand_pts[is_in_circle]
pts_outside = rand_pts[is_in_circle == False]


#-------------------------- creating initial chart ----------------------------
fig = plt.figure(figsize=(10,5))
plt.suptitle("Estimating Pi via Monte Carlo Simulation")

#axis to be used for plotting iteration number vs pi estimate
ax1 = plt.axes([.07,.1,.9,.85])
ax1.spines['right'].set_visible(False), ax1.spines['top'].set_visible(False)
ax1.set_xlabel('N'), ax1.set_ylabel('Pi Estimate')
ax1.set_xlim(0, iterations), ax1.set_ylim(2, 4)
ax1.axhline(np.pi, color='r', alpha=0.2)

#axis to be used for plotting points in/around circle
ax2 = plt.axes([.74,.13, .3, .3])
ax2.set_xlim(-1,1), ax2.set_ylim(-1,1)
ax2.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
#plotting unit circle using polar coordinates
theta = np.linspace(0, 2*np.pi)
x = np.cos(theta)
y = np.sin(theta)
ax2.plot(x, y, color='black', alpha=0.7)
ax2.set_aspect('equal')
#------------------------------------------------------------------------------

#initializing lines and scatter plots to animate
line, = ax1.plot([])
scat1, = ax2.plot([], [], marker='o', markersize=2, ls='', color='blue')
scat2, = ax2.plot([], [], marker='o', markersize=2, ls='', color='gray')

#initializing variables used for animation
pi_estimates = []

def animate(i):
    #updating circle chart
    in_count = np.sum(is_in_circle[:i+1])
    out_count = i+1 - in_count
    
    if is_in_circle[i]:
        scat1.set_xdata(pts_inside[:in_count+1, 0])
        scat1.set_ydata(pts_inside[:in_count+1, 1])        
    else:
        scat2.set_xdata(pts_outside[:out_count+1, 0])
        scat2.set_ydata(pts_outside[:out_count+1, 1])
    
    #updating pi estimate and adding to pi_list    
    in_circle_ratio = in_count/(in_count+out_count)
    pi_estimates.append(in_circle_ratio*4)
    
    #updating line chart
    line.set_xdata(np.arange(i+1))
    line.set_ydata(pi_estimates[:i+1])
    return line, scat1, scat2,
    
#creating animation
anim = animation.FuncAnimation(fig, animate, frames=iterations,
                               interval=10, blit=True, repeat=False)

plt.show()

##for saving to mp4
#Writer = animation.writers['ffmpeg']
#writer = Writer(fps=60, metadata=dict(artist='pspratling'), bitrate=1800)
#anim.save('monte_carlo.mp4', writer=writer)