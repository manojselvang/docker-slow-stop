Here’s a simple README that feels more like a real GitHub project than AI-generated documentation:

# Docker Slow Stop

A small Docker project to understand **why some containers take several seconds to stop** and how using the correct `CMD` form can fix it.

## What this project shows

The project compares two Dockerfiles:

* `Dockerfile.slow` – uses the shell form of `CMD`
* `Dockerfile.fast` – uses the exec form of `CMD`

The slow version starts the application through `/bin/sh`, while the fast version starts Python directly as **PID 1**.

This matters when Docker sends a `SIGTERM` during `docker stop`.

## Project Structure

```text
.
├── Dockerfile.slow
├── Dockerfile.fast
├── app.py
└── README.md
```

## Run the slow version

Build the image:

```bash
docker build -f Dockerfile.slow -t slow-app .
```

Run the container:

```bash
docker run -d --name slow-container slow-app
```

Check the processes:

```bash
docker top slow-container
```

Then test the stop time:

```bash
time docker stop slow-container
```

The container should take around **10 seconds** to stop.

## Run the fast version

Build the image:

```bash
docker build -f Dockerfile.fast -t fast-app .
```

Run it:

```bash
docker run -d --name fast-container fast-app
```

Check the processes:

```bash
docker top fast-container
```

Then:

```bash
time docker stop fast-container
```

The container should stop almost immediately.

## What was the problem?

The slow Dockerfile uses:

```dockerfile
CMD python app.py
```

This starts the application through a shell:

```text
PID 1
└── /bin/sh
    └── python app.py
```

The fixed Dockerfile uses:

```dockerfile
CMD ["python", "app.py"]
```

Now Python runs directly as PID 1:

```text
PID 1
└── python app.py
```

This allows the application to receive the termination signal directly.

## Graceful Shutdown

The Python application also handles `SIGTERM` so it can shut down cleanly instead of being killed abruptly.

The main takeaway from this project is simple:

> **In containers, how you start your application matters.**

Using the exec form of `CMD` helps ensure your application runs as PID 1 and receives Docker's signals correctly.

## Things I learned

* What PID 1 means inside a container
* Difference between shell form and exec form of `CMD`
* How `SIGTERM` works with `docker stop`
* Why containers sometimes take several seconds to stop
* How to investigate container processes using `docker top`
* How to implement graceful shutdown in Python

## Author

Manoj Selvan G
Gmail: manojselvang@gmail.com
GitHub: github.com/manojselvang
LinkedIn: https://www.linkedin.com/in/manojselvang/
