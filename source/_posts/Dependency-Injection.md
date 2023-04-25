---
title: Dependency Injection
date: 2023-04-22 12:07:05
tags: design-patterns
highlight: true
categories:
  - Design Patterns
---

Dependency injection is a design pattern used in software engineering that allows objects to be created with their dependencies supplied from outside sources. In other words, instead of an object creating its dependencies itself, the dependencies are "injected" into the object from an external source.
<!--more-->

The main benefits of dependency injection are:

1. Decoupling: By injecting dependencies, objects are not tightly coupled to their dependencies, which makes them more modular and easier to test.

2. Testability: Because dependencies can be easily replaced with mock objects, unit testing becomes easier and more effective.

3. Reusability: Injected dependencies can be reused across multiple objects, reducing code duplication and improving maintainability.

There are three main types of dependency injection:

1. Constructor Injection: Dependencies are passed to an object's constructor when it is created.

2. Setter Injection: Dependencies are set on an object using setter methods.

3. Interface Injection: Objects are required to implement a specific interface that defines the dependencies they require.

Dependency injection frameworks are available in many programming languages to help automate the process of injecting dependencies. These frameworks use a combination of reflection and configuration files to automatically inject dependencies into objects at runtime. Examples of dependency injection frameworks include Spring Framework for Java and AngularJS for JavaScript.

Here are some examples of dependency injection in Java:

## Constructor Injection:

```java
public class UserService {
    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public User getUserById(int id) {
        return userRepository.findById(id);
    }
}
```

In this example, the `UserService` class has a dependency on the `UserRepository` class, which is passed to its constructor. The `UserRepository` object is injected into the `UserService` object when it is created. This allows the `UserService` object to use the methods of the `UserRepository` object without creating it itself.

## Setter Injection:


```java
public class OrderService {
    private PaymentService paymentService;

    public void setPaymentService(PaymentService paymentService) {
        this.paymentService = paymentService;
    }

    public void processOrder(Order order) {
        paymentService.processPayment(order.getPayment());
        // process order logic
    }
}
```

In this example, the `OrderService` class has a dependency on the `PaymentService` class, which is set using a setter method. The `PaymentService` object is injected into the `OrderService` object after it is created. This allows the `OrderService` object to use the methods of the `PaymentService` object without creating it itself.

## Interface Injection:

```java
public interface Logger {
    void log(String message);
}

public class ConsoleLogger implements Logger {
    public void log(String message) {
        System.out.println(message);
    }
}

public class UserService {
    private Logger logger;

    public void setLogger(Logger logger) {
        this.logger = logger;
    }

    public User getUserById(int id) {
        logger.log("Getting user by id: " + id);
        // get user logic
    }
}
```

In this example, the `UserService` class has a dependency on the `Logger` interface, which is required to be implemented by any object that wants to be injected into the `UserService` object. The `ConsoleLogger` class implements the `Logger` interface and is injected into the `UserService` object using a setter method. This allows the `UserService` object to use the methods of the `Logger` object without creating it itself.

These are just a few examples of how dependency injection can be used in Java. There are many other ways to use dependency injection, and the specific implementation depends on the needs of the application.

Let's say we have a class called "UserService" that is responsible for managing user data. This class has a dependency on a database connection to retrieve and store user data.

Without dependency injection, the UserService class would have to create its own database connection object, which would tightly couple the UserService class to the database connection implementation.

With dependency injection, we can pass in the database connection object as a dependency to the UserService class. This allows us to easily swap out different database connection implementations without having to modify the UserService class.

For example, we could create a `MySQLDatabaseConnection` class and a `PostgreSQLDatabaseConnection` class, both implementing the same interface. We can then pass in either of these objects to the UserService class depending on which database we want to use.

This makes our code more flexible and easier to maintain, as we can easily swap out dependencies without having to modify the code that uses them.
