---
title: Using Threading to Print Odd and Even Numbers in Order
date: 2023-04-22 11:31:22
tags: multi-threading
categories:
  - Operating System
---
In this blog post, we'll explore how to use threading in Java to print odd and even numbers in order. Threading is a powerful technique that allows us to execute multiple threads of code concurrently, which can be useful for a wide variety of applications, including parallel processing, network programming, and more.
<!--more-->

In this example, we'll use threading to print a sequence of odd and even numbers in order. We'll start by creating two threads, one for printing odd numbers and one for printing even numbers. Each thread will execute a loop that prints the appropriate numbers, and we'll use a synchronization primitive called a semaphore to ensure that the threads execute in the correct order.

By the end of this blog post, you'll have a better understanding of how to use threading in Java to execute concurrent tasks.

We're going to discuss about two major methods to implement this.

## Using <code>synchronized</code> method:

In Java, the synchronized keyword is used to create synchronized methods, which are methods that can be accessed by only one thread at a time. When a thread invokes a synchronized method, it acquires a lock on the object that the method is called on, and no other thread can access the synchronized method on that object until the lock is released.

Here's a sample Java code that creates two separate threads to print odd and even numbers:

``` java
public class OddEvenPrinter {
    private final int MAX_VALUE = 10;
    private int currentValue = 1;

    public static void main(String[] args) {
        OddEvenPrinter printer = new OddEvenPrinter();
        Thread oddThread = new Thread(printer::printOdd, "Odd");
        Thread evenThread = new Thread(printer::printEven, "Even");
        oddThread.start();
        evenThread.start();
    }

    public synchronized void printOdd() {
        while (currentValue <= MAX_VALUE) {
            if (currentValue % 2 != 0) {
                System.out.println(Thread.currentThread().getName() + ": " + currentValue);
                currentValue++;
                notify();
            } else {
                try {
                    wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    public synchronized void printEven() {
        while (currentValue <= MAX_VALUE) {
            if (currentValue % 2 == 0) {
                System.out.println(Thread.currentThread().getName() + ": " + currentValue);
                currentValue++;
                notify();
            } else {
                try {
                    wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }
}
```

This code should print the following output:

```
Odd: 1
Even: 2
Odd: 3
Even: 4
Odd: 5
Even: 6
Odd: 7
Even: 8
Odd: 9
Even: 10
```

In this code, we define a `OddEvenPrinter` class that has a `MAX_VALUE` constant that specifies the maximum number to print, and a `currentValue` variable that keeps track of the current number to print.

We create two separate threads, one for printing odd numbers and one for printing even numbers, using the `Thread` class and lambda expressions.

The `printOdd()` and `printEven()` methods use a `synchronized` block to ensure that only one thread can access the shared `currentValue` variable at a time.

Within each method, we use a `while` loop to print odd and even numbers, respectively. If the current value is odd and the current thread is the odd thread, we print the current value and increment the `currentValue` variable, and then notify the other thread to wake up. If the current value is even and the current thread is the even thread, we print the current value and increment the `currentValue` variable, and then notify the other thread to wake up. Otherwise, we wait for the other thread to notify us.

By the end of this code, you should have two separate threads that print odd and even numbers in order.

## Using Semaphores:

Semaphores are a synchronization mechanism that is used to control access to a shared resource in a concurrent system. They were first introduced by Edsger Dijkstra in 1965.

A semaphore is essentially a counter that is associated with a shared resource. The counter can be incremented or decremented by threads that wish to access the shared resource. When the counter is greater than zero, the resource is available for use. When the counter is zero, the resource is unavailable and threads that wish to access it must wait until it becomes available.

In Java, the Semaphore class is provided as part of the java.util.concurrent package. It provides methods for acquiring and releasing permits, which are equivalent to incrementing and decrementing the counter associated with the semaphore. Semaphores can be used in conjunction with other synchronization mechanisms such as locks and condition variables to implement more complex synchronization patterns.

Here's a sample Java code that uses Semaphores to print odd and even numbers in order:

``` java
import java.util.concurrent.Semaphore;

public class OddEvenPrinter {
    private final int MAX_VALUE = 10;
    private int currentValue = 1;
    private Semaphore oddSemaphore = new Semaphore(1);
    private Semaphore evenSemaphore = new Semaphore(0);

    public static void main(String[] args) {
        OddEvenPrinter printer = new OddEvenPrinter();
        Thread oddThread = new Thread(printer::printOdd, "Odd");
        Thread evenThread = new Thread(printer::printEven, "Even");
        oddThread.start();
        evenThread.start();
    }

    public void printOdd() {
        while (currentValue <= MAX_VALUE) {
            try {
                oddSemaphore.acquire();
                System.out.println(Thread.currentThread().getName() + ": " + currentValue);
                currentValue++;
                evenSemaphore.release();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    public void printEven() {
        while (currentValue <= MAX_VALUE) {
            try {
                evenSemaphore.acquire();
                System.out.println(Thread.currentThread().getName() + ": " + currentValue);
                currentValue++;
                oddSemaphore.release();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
```

In this code, we define a `OddEvenPrinter` class that has a `MAX_VALUE` constant that specifies the maximum number to print, and a `currentValue` variable that keeps track of the current number to print.

We create two `Semaphore` objects, `oddSemaphore` and `evenSemaphore`, that are used to synchronize access to the shared `currentValue` variable. The `oddSemaphore` is initialized with a permit count of 1, and the `evenSemaphore` is initialized with a permit count of 0.

We create two separate threads, one for printing odd numbers and one for printing even numbers, using the `Thread` class and lambda expressions.

The `printOdd()` and `printEven()` methods use the `acquire()` and `release()` methods of the `Semaphore` class to ensure that only one thread can access the shared `currentValue` variable at a time.

Within each method, we use a `while` loop to print odd and even numbers, respectively. If the current value is odd and the current thread is the odd thread, we acquire a permit from the `oddSemaphore`, print the current value, increment the `currentValue` variable, and release a permit to the `evenSemaphore`. If the current value is even and the current thread is the even thread, we acquire a permit from the `evenSemaphore`, print the current value, increment the `currentValue` variable, and release a permit to the `oddSemaphore`.

By the end of this code, you should have two separate threads that print odd and even numbers in order using Semaphores.


## `synchronized` vs `Semaphore`:

In terms of performance, Semaphores are generally faster and more efficient than synchronized methods for managing concurrency in Java. This is because Semaphores involve less overhead than synchronized methods, and they allow for more fine-grained control over access to shared resources.

For this problem, both approaches (synchronized methods and Semaphores) are viable solutions and will produce correct results. However, since Semaphores are more efficient than synchronized methods, using Semaphores would be the better choice for this problem in terms of performance.

In the Semaphore implementation of the Odd Even problem, we use two Semaphores to control access to the shared `currentValue` variable. The `oddSemaphore` is initialized with a permit count of 1, and the `evenSemaphore` is initialized with a permit count of 0. This allows us to ensure that only one thread can access the shared `currentValue` variable at a time, and that the threads take turns printing odd and even numbers.

Overall, using Semaphores is a good choice for managing concurrency in Java applications, especially when performance is a concern. However, it's important to note that Semaphores can be more difficult to use correctly than synchronized methods, and they require more careful design and testing to ensure that they work as intended.
