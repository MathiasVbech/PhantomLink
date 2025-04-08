## Steganographic Command & Control System
This repository contains a proof-of-concept command and control system using steganography for educational purposes only. The system consists of three main components:

### Components
- C2/: Command & Control server components for generating commands
- RAT/LocalTesting/: Local testing environment for development
- RAT/Trojan/: Main payload component (Warning: Contains potentially harmful code)

# Steganographic Command & Control System

This repository contains a proof-of-concept command and control system that utilizes steganography for communication. It is intended for **educational purposes only** and should be used responsibly.

**WARNING:** This project contains code that can be harmful if misused. It should only be executed in a controlled environment, such as a virtual machine.

## Project Overview

This system demonstrates how malicious commands can be hidden within seemingly innocent images using Least Significant Bit (LSB) steganography. This technique allows malware to receive instructions through channels that are less likely to be scrutinized by security tools.

The project is divided into five main components:

* C2:  Tools for generating and embedding commands into images.
* RAT/LocalTesting: A local testing environment for development and experimentation.
* RAT/Trojan: The main payload component (**WARNING:** Contains potentially harmful code).
* Thesis.pdf written research and development report
* Video_live_Demo video demo of the RAT working

## Features

* Steganographic Command Hiding:  Conceals commands within PNG images using LSB steganography.
* Keylogging: Captures keystrokes and strategically exfiltrates data.
* Cloud-Based C2: Utilizes cloud storage (Dropbox in this implementation) for command delivery and data exfiltration.
* Persistence:  Establishes persistence on the infected system.
* Modular Design:  Components are separated for easier understanding and modification.

### Warning
This code is for educational purposes only. The components can be harmful if misused. Only run in controlled environments like virtual machines.

### Requirements
 -Python 3.10+
 -PowerShell 5.1+
 -Windows OS
 -Virtual Machine (strongly recommended for testing)

See individual component READMEs for specific setup and usage instructions.