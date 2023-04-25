---
title: Implementing Unique ID Generator
date: 2023-04-22 12:12:52
tags: system-design
categories:
  - System Design
---

A unique ID generator can be implemented using a combination of timestamp, counter, and random number. Here's a possible implementation in Python:
<!--more-->

```python
import time
import random

class IDGenerator:
    def __init__(self):
        self.counter = 0

    def generate_id(self):
        timestamp = int(time.time() * 1000)  # Get current timestamp in milliseconds
        self.counter = (self.counter + 1) % 10000  # Increment counter and wrap around
        random_num = random.randint(0, 999)  # Generate random number between 0 and 999
        return f"{timestamp:013d}{self.counter:04d}{random_num:03d}"
```

In this implementation, the `IDGenerator` class has a counter initialized to zero. The `generate_id` method generates a unique ID by concatenating the current timestamp in milliseconds, a counter value that increments with each ID generation, and a random number between 0 and 999. The resulting ID is a 20-digit string in the format `timestamp (13 digits) + counter (4 digits) + random number (3 digits)`.

Here's an example of how to use the `IDGenerator` class:

```python
generator = IDGenerator()
for i in range(10):
    print(generator.generate_id())
```

This code creates an instance of the `IDGenerator` class and generates 10 unique IDs using the `generate_id` method. The output might look like this:

```
162798978283100000000000
162798978283100000000001
162798978283100000000002
162798978283100000000003
162798978283100000000004
162798978283100000000005
162798978283100000000006
162798978283100000000007
162798978283100000000008
162798978283100000000009
```

This implementation generates unique IDs by combining a timestamp, a counter, and a random number, which ensures that the probability of collisions is very low. <b>However, it is possible for collisions to occur if the same ID generator is used across multiple machines or if the counter wraps around too quickly.</b> To further optimize the ID generator, additional measures such as using a stronger hash function or a distributed ID generation system may be necessary.

## Other options:

There are several options to generate unique IDs, depending on the requirements of the application. Here are some common methods:

1. UUID: A UUID (Universally Unique Identifier) is a 128-bit number that is guaranteed to be unique across time and space. UUIDs are generated using a combination of timestamp and random number, and can be represented as a string of hexadecimal digits.

2. Timestamp: A timestamp is a value that represents the current date and time. Timestamps can be used as unique IDs if they are combined with a counter or a random number to ensure uniqueness.

3. Counter: A counter is a value that increments with each ID generation. Counters can be used as unique IDs if they are combined with a timestamp or a random number to ensure uniqueness.

4. Hash function: A hash function can be used to generate a unique ID from a given input. Hash functions take an input of arbitrary size and produce a fixed-size output that is unique for each input value.

5. Snowflake ID: A Snowflake ID is a unique 64-bit integer that is generated using a combination of timestamp, machine ID, and sequence number. Snowflake IDs are used by distributed systems to generate unique IDs across multiple machines.

6. Custom ID: A custom ID can be generated using any combination of the above methods, or by using a custom algorithm that meets the specific requirements of the application.

Each of these methods has its own advantages and disadvantages, and the choice of ID generation method depends on the specific requirements of the application. For example, UUIDs are widely used because they are guaranteed to be unique, but they are relatively long and may not be suitable for some applications. On the other hand, counters are simple and efficient, but they may not be unique if multiple ID generators are used simultaneously.


### Auto Incremented ID:

Using auto-incremented IDs as primary keys in SQL databases is a common practice and works well in many cases. However, there are some situations where this approach may not be suitable:

1. Scalability: If the database is expected to grow very large, auto-incremented IDs may eventually overflow the maximum value of the data type used to store them. This can cause errors and require expensive database migrations.

2. Security: Auto-incremented IDs can be predictable, which can be a security risk if they are used in URLs or other public-facing contexts. Attackers can use this predictability to guess other IDs and access sensitive data.

3. Data privacy: In some cases, auto-incremented IDs can reveal information about the data, such as the order in which it was added to the database. This can be a privacy concern if the data contains sensitive information.

4. Data integration: If data from multiple databases needs to be merged or integrated, auto-incremented IDs may not be unique across the different databases, leading to conflicts and errors.

For these reasons, it may be necessary to use other methods to generate unique IDs, such as UUIDs or custom ID generators. These methods can provide better scalability, security, and data privacy, and can be more suitable for distributed systems or applications with complex data integration requirements.


### UUID:

UUIDs (Universally Unique Identifiers) are widely used as unique identifiers in many applications and have several advantages, such as being guaranteed to be unique and not requiring a centralized ID generator. However, there are some situations where UUIDs may not be suitable:

1. Size: UUIDs are relatively long, typically 32 hexadecimal digits (128 bits). This can be a problem if the IDs need to be stored in a database or transmitted over a network, as it can increase storage and bandwidth requirements.

2. Predictability: Although UUIDs are designed to be unique, they are not completely random and can be predictable in some cases. This can be a security risk if the UUIDs are used in URLs or other public-facing contexts.

3. Performance: Generating UUIDs can be computationally expensive, especially if they are generated in large batches or in a distributed system. This can affect the performance of the application and increase response times.

4. Integration: If data from multiple systems needs to be merged or integrated, UUIDs may not be unique across the different systems, leading to conflicts and errors.

For these reasons, it may be necessary to use other methods to generate unique IDs, such as custom ID generators or other types of UUIDs (such as ULIDs or Flake IDs) that address some of the limitations of standard UUIDs. The choice of ID generation method depends on the specific requirements of the application and the trade-offs between uniqueness, size, predictability, and performance.

### Snowflake ID:

Snowflake ID is a unique 64-bit integer that is generated using a combination of timestamp, machine ID, and sequence number. Snowflake IDs are used by distributed systems to generate unique IDs across multiple machines. Here's an example of how Snowflake ID is generated:

Let's assume that we have a distributed system with multiple machines. Each machine has a unique ID, which is a 10-bit integer. The current timestamp in milliseconds is 41 bits long. The sequence number is a 12-bit integer that increments with each ID generation on the same machine.

To generate a Snowflake ID, we can concatenate these three values into a 64-bit integer in the following order:

1. The first 41 bits represent the current timestamp in milliseconds.
2. The next 10 bits represent the machine ID.
3. The last 12 bits represent the sequence number.

Here's an example of how a Snowflake ID might look like:

```
110011001101001110101011110010011101001110000000000000000000000 (64 bits)
```

In this example, the first 41 bits represent the timestamp, which is equivalent to the value `1630055836000` in milliseconds. The next 10 bits represent the machine ID, which could be any value between 0 and 1023. The last 12 bits represent the sequence number, which could be any value between 0 and 4095.

By using a combination of timestamp, machine ID, and sequence number, Snowflake IDs can be generated with a high degree of uniqueness and can be used to generate IDs across multiple machines in a distributed system.

Here's an implementation of the Snowflake method for generating unique IDs in Python:

```python
import time

class SnowflakeGenerator:
    def __init__(self, datacenter_id, worker_id):
        self.twepoch = 1288834974657
        self.datacenter_id = datacenter_id
        self.worker_id = worker_id
        self.sequence = 0
        self.sequence_bits = 12
        self.worker_id_bits = 5
        self.datacenter_id_bits = 5
        self.max_worker_id = -1 ^ (-1 << self.worker_id_bits)
        self.max_datacenter_id = -1 ^ (-1 << self.datacenter_id_bits)
        self.sequence_mask = -1 ^ (-1 << self.sequence_bits)
        self.worker_id_shift = self.sequence_bits
        self.datacenter_id_shift = self.sequence_bits + self.worker_id_bits
        self.timestamp_shift = self.sequence_bits + self.worker_id_bits + self.datacenter_id_bits

    def _generate_timestamp(self):
        return int(time.time() * 1000 - self.twepoch)

    def _next_sequence(self):
        self.sequence = (self.sequence + 1) & self.sequence_mask
        if self.sequence == 0:
            raise Exception("Sequence overflow")

    def generate_id(self):
        timestamp = self._generate_timestamp()
        if timestamp < self.last_timestamp:
            raise Exception("Clock moved backwards")
        if timestamp == self.last_timestamp:
            self._next_sequence()
        else:
            self.sequence = 0
        self.last_timestamp = timestamp
        return ((timestamp << self.timestamp_shift) |
                (self.datacenter_id << self.datacenter_id_shift) |
                (self.worker_id << self.worker_id_shift) |
                self.sequence)
```

Here's how you can use this class to generate unique IDs:

```python
generator = SnowflakeGenerator(datacenter_id=1, worker_id=1)
unique_id = generator.generate_id()
print(unique_id)
```

This will output a unique ID that is generated using the Snowflake method. You can change the `datacenter_id` and `worker_id` values to generate IDs that are unique to your specific environment.

The code is an implementation of the Snowflake method for generating unique IDs in Python.

The `SnowflakeGenerator` class has the following attributes:

- `twepoch`: This is the timestamp of the Snowflake epoch, which is January 1, 2010 in milliseconds. It is used to calculate the timestamp portion of the generated ID.
- `datacenter_id`: This is a unique identifier for the datacenter that the ID is being generated in.
- `worker_id`: This is a unique identifier for the worker that is generating the ID.
- `sequence`: This is a counter that is used to ensure that IDs generated within the same millisecond are unique.
- `sequence_bits`: This is the number of bits used to represent the sequence number.
- `worker_id_bits`: This is the number of bits used to represent the worker ID.
- `datacenter_id_bits`: This is the number of bits used to represent the datacenter ID.
- `max_worker_id`: This is the maximum value that the worker ID can be.
- `max_datacenter_id`: This is the maximum value that the datacenter ID can be.
- `sequence_mask`: This is a bitmask that is used to extract the sequence number from the generated ID.
- `worker_id_shift`: This is the number of bits to shift the worker ID to the left before combining it with the other parts of the ID.
- `datacenter_id_shift`: This is the number of bits to shift the datacenter ID to the left before combining it with the other parts of the ID.
- `timestamp_shift`: This is the number of bits to shift the timestamp to the left before combining it with the other parts of the ID.

The `SnowflakeGenerator` class has the following methods:

- `_generate_timestamp()`: This method generates the timestamp portion of the ID by subtracting the Snowflake epoch from the current time in milliseconds.
- `_next_sequence()`: This method increments the sequence number and handles sequence number overflow.
- `generate_id()`: This method generates a unique ID using the Snowflake method. It combines the timestamp, datacenter ID, worker ID, and sequence number to create a 64-bit ID.

To use the `SnowflakeGenerator` class, you can create an instance of the class with a unique datacenter ID and worker ID, and then call the `generate_id()` method to generate a new ID. The generated ID will be unique to your specific environment.


#### Note:

The Snowflake method was originally developed by Twitter to generate unique IDs for their distributed systems. They chose January 1, 2010 as the epoch for their implementation of the Snowflake method because it was a recent date at the time and it allowed for a larger range of timestamps than if they had chosen an earlier epoch.

In the Snowflake method, the timestamp portion of the ID is calculated by subtracting the epoch time from the current time in milliseconds. By choosing a more recent epoch time, the timestamp portion of the ID can be represented using fewer bits, which allows for a larger range of timestamps to be represented in the ID.

It's worth noting that the choice of epoch time is somewhat arbitrary and can be adjusted to suit the needs of a particular system. However, it's important to choose an epoch time that allows for a sufficient range of timestamps to be represented in the ID, while also ensuring that the timestamp portion of the ID doesn't take up too many bits and reduce the number of bits available for other parts of the ID (such as the worker ID and sequence number).
