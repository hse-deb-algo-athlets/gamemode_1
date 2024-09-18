# Getting Started with the Dev Environment

This guide will walk you through the initial steps to power on your NVIDIA Jetson Nano, log in, and set up the development environment to start working on the "Build Your Own Chatbot" project.

## Steps to Get Started

### 1. Power On the NVIDIA Jetson Nano

Turn on your NVIDIA Jetson Nano by plugging it into a power source and connecting it to your monitor and keyboard.

### 2. Log In

Use the following credentials to log into your Nano:

- **Username**: `<your_username>` 
- **Password**: `<your_password>`


### 3. Launch Visual Studio Code

After logging in, open the terminal and navigate to the project directory. Then, launch Visual Studio Code.

#### Terminal Commands:

```bash
cd /ssd/build-your-own-chatbot   # Navigate to the project folder
code .                           # Launch VSCode in the project directory
```

### 4. Check Docker Installation

To ensure Docker is running and properly installed, use the following command:

```bash
docker --version
```

If Docker is installed, this command will return the installed version. If it's not installed, you may need to set it up before continuing.

---