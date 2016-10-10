# Asynchronous Programming in Python

## Model

### Coroutines

Python's model of asynchronous programming is centered around coroutines.
Coroutines are functions marked with explicit execution breakpoints.
Generator-based coroutines are marked using the `@asyncio.coroutine` decorator
and implement execution breakpoints using `yield from` expressions.
Native coroutines are marked using `async` and implement execution breakpoints
using `await` expressions.

Coroutines cannot be executed via direct call. Direct calls to coroutines
create coroutine objects, which are a closure of the coroutine invocation
and its parameters. Coroutines must be scheduled and run in the context of an
event loop. The asyncio package provides the framework for event loops.

Coroutines can call into other coroutines and Futures by awaiting on them.
This is also the same mechanism coroutines use to implement breakpoints.
Coroutines can return values and raise exceptions like normal functions.

### Futures

In a sense, event loops do not execute coroutines directly. Event loops need
mechanisms for cancelling coroutine execution, storing coroutine results, and
storing exception information. Futures wrap coroutines to provide this
functionality. In essence, Futures are closures. When the asyncio package
accepts a coroutine directly, it wraps the coroutine in a Future or Task.

### Tasks

Tasks are special types of Futures. Whereas cancellation of a Future yields
instant gratification, cancellation of a Task may take time or not occur at
all if the Task prevents its own cancellation.

### Concurrent Execution

Asynchronous programming in Python simply means code may run in arbitrary
order. Futures and Tasks are not thread-safe by default. The event loop
interface provides explicitly marked methods for scheduling and interacting
with  Futures and Tasks in a manner that is thread-safe.

If concurrency is employed via processes, the event loop must run in the main
thread. Furthermore, a child watcher must run in the main thread if processes
are executed from worker threads.

## Django Channels

Channels provides asynchronous execution through message passing. Channels
separates Django into a communications process and consumer/worker processes.
Channels uses multiple independent worker processes in an event-oriented
execution model. Channels processes communicate using Asynchronous Server
Gateway Interface (ASGI).

Django cannot use Channels by itself. It requires:
 - an ASGI server such as Daphne.
 - Django workers started with `runworker`.
 - an ASGI router such as Redis.

Django primarily uses two types of channels: work dispatch channels and reply
channels. To ensure the reply is received by the correct server, the reply
channel is a process-specific channel.

### Asynchronous Server Gateway Interface

ASGI includes protocol servers, a channel layer, and application code. The
channel layer provides at-most-once delivery, which precludes broadcast.
Channels support multiple sources and multiple sinks.

Channels are implemented as FIFO queues. Normal channels operate independently
and message ordering is not guaranteed. Single-reader channels are denoted by
a main channel name and a sub-channel name separated by a `?`. Single-reader
channels preserve message ordering within the main channel. Process-specific
channels are denoted by a main channel name and a sub-channel name separated
by a `!`. Process-specific channels are guaranteed to only deliver messages to
the process that created it.

There are many extensions to the ASGI protocol:
 - groups provides mechanisms for implementing multicast and broadcast.
 - flush provides a method for resetting the channel.
 - asyncio provides an asynchronous receive mechanism.

## Celery

Celery provides asynchronous execution through message passing. Celery supports
multiple message brokers. For example, RabbitMQ in contrast to Django Channels
can provide guaranteed message delivery.

