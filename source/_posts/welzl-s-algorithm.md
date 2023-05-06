---
title: Collision, Randomization and Welzl's Algorithm
tags: algorithm
thumbnail: https://i.ibb.co/nftPWTt/Screenshot-2023-05-06-at-9-45-45-AM.png
categories:
  - Algorithms
date: 2023-05-06 10:10:20
---


<center>
<img src="https://i.ibb.co/nftPWTt/Screenshot-2023-05-06-at-9-45-45-AM.png" alt="3D Car racing" border="0" height="200px" width="400px">
</center>

Have you ever played a 3D video game and wondered how the game engine detects collisions between objects? I recently found myself thinking about this while playing a popular racing game. As I was racing my car around the track, I couldn't help but wonder how the game engine was able to detect collisions between my car and the other cars on the track.
<!--more-->

After doing some research, I learned that one of the ways that game engines detect collisions is by using the minimum enclosing sphere algorithm. This algorithm is used to find the smallest sphere that encloses a set of points in 3D space, which is useful in detecting collisions between objects.

In the game I was playing, each car was represented by a 3D model, which was made up of a large number of points in 3D space. The game engine used the minimum enclosing sphere algorithm to calculate the minimum enclosing sphere of each car's 3D model. By doing this, the game engine was able to determine if the minimum enclosing spheres of two cars intersected, indicating a collision.

I was fascinated by this and started thinking about other applications of the minimum enclosing sphere algorithm. I realized that it could be used in various real-life simulations, such as simulations of fluid dynamics and molecular dynamics. In these simulations, the algorithm could be used to detect collisions between particles or fluid elements, which could help to simulate the behavior of fluids or molecules in real-world applications.

## Minimum Enclosing Circle:

<center>
<a title="Claudio Rocchini, CC BY-SA 3.0 &lt;https://creativecommons.org/licenses/by-sa/3.0&gt;, via Wikimedia Commons" href="https://commons.wikimedia.org/wiki/File:Smallest_circle_problem.svg"><img width="512" alt="Smallest circle problem" src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Smallest_circle_problem.svg/512px-Smallest_circle_problem.svg.png"></a>
</center>

The minimum enclosing circle problem involves finding the smallest circle that encloses a set of points in a 2D plane. This problem can be solved using a similar approach to the minimum enclosing sphere algorithm, but with some modifications to account for the reduced dimensionality.

Feeling inspired by the idea of the minimum enclosing circle problem, I decided to try and solve it myself. I thought to myself, "how hard could it be to find the smallest circle that encloses a set of points in a 2D plane?"

I started by sketching out some points on a piece of paper and drawing circles around them. I quickly realized that this was not going to work, as it was difficult to determine which circle was the smallest. I needed a more systematic approach.

Next, I tried to come up with a naive solution. I thought about selecting two points from the set of points and finding the distance between them. I could then draw a circle with a radius equal to half the distance between the two points. This circle would definitely enclose the two points, but it may not enclose all the other points in the set.

I then thought about selecting a third point and finding the circle that passes through all three points. This circle would definitely enclose the three points, but it may not be the smallest circle that encloses all the points in the set.

I decided to try a brute force algorithm to solve the minimum enclosing circle problem. While brute force algorithms are not always the most efficient, they can be useful in certain situations, especially when dealing with small sets of points.

My brute force algorithm involved checking every possible circle that could be drawn around the set of points. I started by selecting three points from the set and finding the smallest circle that encloses them. I then added one point at a time and checked if the circle still enclosed all the points. If it did, then I continued adding points until all the points in the set were included. If not, then I discarded the circle and started again with a different set of three points.

While this algorithm was not the most efficient, it was a valid solution to the problem. It guaranteed that the smallest possible circle that encloses all the points in the set would be found. However, it was not practical for larger sets of points, as the number of possible circles to check would become prohibitively large.

## Welzl's algorithm:
Since my brute force algorithm was not practical for larger sets of points, I did some research to see if there were more efficient algorithms available for solving the minimum enclosing circle problem. To my surprise, I discovered that the problem had once been a hot research topic and that many algorithms had been developed to solve it.

As I delved deeper into the research, I discovered that one of the most popular algorithms for solving the minimum enclosing circle problem was the Welzl's algorithm. This algorithm involved selecting points one at a time and finding the minimum enclosing circle that included all the previously selected points.

The Welzl's algorithm was much more efficient than my brute force algorithm and could handle larger sets of points. It was also more accurate, as it guaranteed that the smallest possible circle that encloses all the points in the set would be found.

The algorithm goes as follows:

```
Algorithm: Welzl's Algorithm for Minimum Enclosing Circle

Input: A set of n points P in a 2D plane
Output: The minimum enclosing circle that encloses all the points in P

1. if |P| = 1, return a circle with radius 0 centered at the only point in P.
2. if |P| = 2, return the circle with diameter defined by the two points in P.
3. Randomly shuffle the points in P.
4. Let R be the set of points chosen so far.
5. Let D be the minimum enclosing circle that encloses the points in R.
6. For each point p in P \ R:
    a. If p is inside D, continue to the next point.
    b. Add p to R.
    c. Recursively call the algorithm on the set of points R and update D.
7. Return the minimum enclosing circle D that encloses all the points in P.
```

## Randomization:
Before diving into the implementation of the Welzl's algorithm, it's worth noting the importance of random shuffling in the algorithm. The algorithm shuffles the points randomly before selecting them, which makes the algorithm randomized.

Randomness is a pretty cool concept, don't you think? It's like the universe is playing dice with us and we're just trying to figure out the rules of the game. But did you know that randomness can actually help us optimize problems? It's true!

By shuffling the points randomly, the Welzl's algorithm is able to explore different orders of points and find the one that leads to the most efficient and accurate solution. This is especially important when dealing with large sets of points, where the number of possible orders is large and the algorithm can benefit from the added randomness.

Did you also know that randomness can be used to optimize other algorithms too? For example, Monte Carlo simulations use random numbers to simulate the behavior of a system and estimate the probability of certain outcomes. This is super useful in fields like finance, engineering, and physics, where it's hard to simulate a system using deterministic algorithms.

Randomness is even used in sorting algorithms, like randomized quicksort, to avoid worst-case scenarios. And in cryptography, randomized primality testing is used to determine whether a given number is prime or composite.

It's amazing how randomness can be applied in so many different ways to make algorithms more efficient and accurate. It just goes to show that sometimes we need to embrace the chaos to find the best solutions.

## Implementation:
After learning about the Welzl's algorithm for minimum enclosing circle, I was excited to implement it and see it in action. I decided to create a mini project to demonstrate the algorithm and its various applications.

Despite the challenges, I was determined to implement the Welzl's algorithm and see it in action. I started by writing the pseudo code in paper and then translated it into JavaScript code. I created a simple GUI that allowed the user to input a set of points and see the minimum enclosing circle that encloses all the points.

After an hour of coding and debugging, I finally had a working implementation of the Welzl's algorithm. I was amazed at how quickly the algorithm was able to find the minimum enclosing circle for even large sets of points.

## Midpoint and circumcenter:
In addition to the algorithm, we may need to revisit our high school math. Let's revisit some high school math concepts and discuss how to find a circle that passes through two points and three points.

Finding a circle that passes through two points is a relatively simple process. We can use the midpoint of the line segment connecting the two points as the center of the circle, and the distance between the two points as the radius of the circle. This circle will pass through both points.

To find the midpoint of the line segment connecting two points, we can use the following formula:

$$ \text{midpoint} = \left(\frac{x_1 + x_2}{2}, \frac{y_1 + y_2}{2}\right) $$

where $(x_1, y_1)$ and $(x_2, y_2)$ are the coordinates of the two points that define the line segment.

Once we have the midpoint, we can find the distance between the two points using the distance formula:

$$ \text{distance} = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2} $$

where $(x_1, y_1)$ and $(x_2, y_2)$ are the coordinates of the two points.

The radius of the circle will be equal to half the distance between the two points, and the center of the circle will be the midpoint of the line segment connecting the two points.

<center><img src="https://i.ibb.co/HrCQGYv/Screenshot-2023-05-06-at-10-02-57-AM.png" alt="Circumcenter" width="300px" border="0"></center>

To begin with, finding a circle that passes through three points is a bit more involved than finding a circle that passes through two points. One way to do this is to use the fact that the perpendicular bisectors of the three line segments connecting the three points will intersect at the center of the circle. We can then use the distance between the center and any one of the points as the radius of the circle.

Another approach to finding the circle that passes through three points is to use the inverse determinant and edge length approach. This method involves finding the circumcenter of the triangle formed by the three points and then using the distance between the circumcenter and any one of the points as the radius of the circle.

To find the circumcenter of the triangle formed by the three points, we can use the following formula:

$$
x = \frac{a^2(b^2 + c^2 - a^2)x_1 + b^2(a^2 + c^2 - b^2)x_2 + c^2(a^2 + b^2 - c^2)x_3}{2(a^2(b^2 + c^2 - a^2) + b^2(a^2 + c^2 - b^2) + c^2(a^2 + b^2 - c^2))}
$$

$$
y = \frac{a^2(b^2 + c^2 - a^2)y_1 + b^2(a^2 + c^2 - b^2)y_2 + c^2(a^2 + b^2 - c^2)y_3}{2(a^2(b^2 + c^2 - a^2) + b^2(a^2 + c^2 - b^2) + c^2(a^2 + b^2 - c^2))}
$$

where $(x_1, y_1)$, $(x_2, y_2)$, and $(x_3, y_3)$ are the coordinates of the three points, and $a$, $b$, and $c$ are the lengths of the sides of the triangle opposite the three points, respectively.

Once we have the coordinates of the circumcenter, we can use the distance formula to find the radius of the circle. The distance formula is:

$$
distance = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}
$$

where $(x_1, y_1)$ and $(x_2, y_2)$ are the coordinates of the two points.

Using the inverse determinant and edge length approach we can find the circle that passes through three points.


## Implementation:
Here is my version of Welzl's algorithm's implementation:

```JavaScript
export function createWelZelCircle(points) {
  let minCircle = null;
  let supportSet = [];
  if (points.length > 1) {
    shuffleArray(points);
    let p = points[0];
    let totalPoints = points.length;
    minCircle = new Circle(p);
    let index = 1;
    supportSet.push(p);
    while (index < totalPoints) {
      let pi = points[index];
      if (!supportSet.some((p) => p === pi) && !minCircle.contains(pi)) {
        let newCircle = updateCircle(supportSet, pi);
        if (newCircle && newCircle.radius > minCircle.radius) {
          minCircle = newCircle;
          index = 0;
          continue;
        }
      }
      index++;
    }
  }
  return minCircle;
}

function updateCircle(supportSet, point) {
  let updatedCircle = null;
  const supportSetSize = supportSet.length;
  switch (supportSetSize) {
    case 1:
      updatedCircle = updateCircleWithOnePoint(supportSet, point);
      break;
    case 2:
      updatedCircle = updateCircleWithTwoPoints(supportSet, point);
      break;
    case 3:
      updatedCircle = updateCircleWithThreePoints(supportSet, point);
      break;
    default:
      break;
  }
  return updatedCircle;
}
```

Here is the output:
<iframe src="https://codesandbox.io/embed/welzels-algorithm-0mz7bk?fontsize=14&hidenavigation=1&theme=dark&view=preview" style="width:100%; height:700px; border:0; border-radius: 4px; overflow:hidden;" title="welzels-algorithm" allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking" sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"></iframe>

$~$

Overall, my curiosity about how collisions are detected in 3D games led me to discover the minimum enclosing sphere algorithm and its various applications in simulations and other fields. It's amazing how video games can inspire us to learn and explore new concepts and technologies.

To learn about this algorithm more: https://people.inf.ethz.ch/emo/PublFiles/SmallEnclDisk_LNCS555_91.pdf
