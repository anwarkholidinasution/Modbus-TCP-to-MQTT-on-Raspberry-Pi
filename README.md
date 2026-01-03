# Modbus-TCP-to-MQTT-on-Raspberry-Pi

# Project Overview
This project transforms a Raspberry Pi into an edge computing device and gateway. The Raspberry Pi connects to field devices via Modbus TCP/IP as a master, polling data from sensors and transmitters. It also connects northbound through a wireless connection to send data to a website monitoring system using MQTT (Message Queuing Telemetry Transport). All applications run within Docker containers for better isolation and deployment.

## Docker Installation on Raspberry Pi

**Update the Linux operating system:**

```
sudo apt update && sudo apt upgrade -y
```

![image.png](attachment:36cce6b1-62d0-4bf3-ae2a-9db11a7e8858:image.png)

**Install Dependencies**

Dependencies for Docker refer to the software packages, libraries, or tools that are required for Docker to function correctly on a specific system or platform. These dependencies ensure that Docker can run containers, manage network configurations, and interact with the underlying operating system.

```
sudo apt install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

**`-y`**

- **Purpose**: Automatically answers "yes" to any prompts that might appear during installation.
- **Why it's useful**: Prevents the need for manual confirmation during installation, making the process non-interactive (especially useful in scripts).

### **`ca-certificates`**

- **Purpose**: Provides a collection of trusted Certificate Authority (CA) certificates.
- **Why it's needed**:
    - Ensures secure HTTPS communication by verifying SSL/TLS certificates.
    - Required for downloading packages or files from secure sources (e.g., Docker's repository).

### **`url`**

- **Purpose**: A command-line tool for transferring data using protocols like HTTP, HTTPS, FTP, etc.
- **Why it's needed**:
    - Often used to download files or perform HTTP requests.
    - In this case, it is commonly used to fetch installation scripts or keys from external sources (e.g., Docker's GPG key or installation script).

### **`gnupg`**

- **Purpose**: A tool for secure communication and data storage, which includes managing GPG keys.
- **Why it's needed**:
    - Used to verify the authenticity of downloaded packages by checking their digital signatures.
    - In this case, it will likely be used to add and verify GPG keys for external repositories (e.g., Docker's repository).

### **`lsb-release`**

- **Purpose**: A utility that provides information about the Linux distribution.
- **Why it's needed**:
    - Outputs details such as the distribution's codename, release version, and ID.
    - Often used in scripts to dynamically detect the Linux distribution and version (e.g., `lsb_release -cs` outputs the codename of the OS, like `focal` for Ubuntu 20.04).

### **`\` (Backslash)**

- **Purpose**: Used as a line continuation character in the command.
- **Why it's needed**:
    - Allows the command to be split over multiple lines for better readability.
    - Without the `\`, the command would need to be written on a single line.

**Add Docker GPG key**

```
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

what are these command for?
These commands are part of the **Docker installation process on Debian/Ubuntu**. Their purpose is to securely set up Docker’s official repository.

**Add repository Docker**

```
echo \
  "deb [arch=armhf signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

**Update & install Docker Engine**

```
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io -y
```

**Check if Docker is Running**
sudo systemctl status docker
