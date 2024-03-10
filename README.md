# Vehicle Routing Problem (VRP)

Find the optimal driver schedule for a set of loads to be completed.

### Requirements

- Unbound number of drivers
- Drivers have a maximum shift driving time of 12 hours
- Driver starts at (0,0) and must return within maximum shift
- The Euclidean distance between 2 points gives the drive time in minutes
- Optimal driver schedule should try to minimize cost

### Formulas

Eucledian Distance - $\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}$

Cost Calculation - $500*drivers_{count}+time_{total}$

### Usage

Developed using `Python=3.12` - but should be compatible with early versions of `Python=3.*`.

To run:

``` shell
# 'path_to_problem' is a file path to problem text file
> python3 vrp.py [path_to_problem]
```

### Approach

The VRP problem can be generalized into the traveling salesman problem - find the
optimal path for a traveling salesman so that they visit each required location.
We can think of this VRP problem as a set of traveling salesman problems for each
potential driver.

First, we can consider each driver's schedule to be a constrained traveling salesman
problem. The driver can only travel a maximum Eucledian distance of ``12 * 60``
(12 hour maximum shifts) and must start and end at the same location.

Next for each driver we try to solve the traveling salesman problem with the
constraints applied. We implement a solution using the [nearest neighbor algorithm](https://en.wikipedia.org/wiki/Nearest_neighbour_algorithm). In this approach we attempt to
create a schedule for each driver by considering the nearest next load location.

We generate schedules for each driver but per driver iteration, we must make sure
that the constraints respected - the driver cannot drive beyond the 12 hour shift
limit and the driver must return to the starting location within the 12 hour shift.

And we just repeat this process, adding new drivers as needed until all the loads
have been completed.

### Improvements

This solution only provides an approximate solution to the VRP. A shortcoming of
this particular implementation of nearest neighbor is that it does not try to
optimize the schedule for returning to the starting location. In fact, regarding
nearest neighbor as a solution for traveling salesman:

> The nearest neighbour algorithm may not find a feasible tour at all, even when one exists.