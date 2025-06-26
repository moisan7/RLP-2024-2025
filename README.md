# Compa-Compra 🛒🤖

An autonomous shopping assistant that makes your shopping experience easier and smarter.

## What is it?

Compa-Compra is a general-purpose autonomous shopping assistant that guides and assists store users to complete their shopping easily and simply. Users communicate with ComCom through a dedicated application where they can specify products, and the system provides intelligent assistance throughout their shopping journey.

## Table of Contents

- [Hardware](#hardware)
  - [Components](#components)
  - [Connection Diagram](#connection-diagram)
  - [Assembly Instructions](#assembly-instructions)
- [Software](#software)
  - [Software Architecture](#software-architecture)
  - [Requirements and Languages](#requirements-and-languages)
  - [Algorithms](#algorithms)
- [Results](#results)
  - [Videos](#videos)
  - [Contributions](#contributions)
- [Authors](#authors)

## Hardware

### Components

The Compa-Compra system consists of the following hardware components:

<table>
  <tr>
    <td align="center">
      <img src="docs/report/compacompra_logo.jpg" alt="Microcontroller Unit" width="150"/>
      <p><strong>Microcontroller Unit</strong><br/>
      <a href="LINK_1">Component Details</a></p>
    </td>
    <td align="center">
      <img src="docs/report/compacompra_logo.jpg" alt="Navigation Sensors" width="150"/>
      <p><strong>Navigation Sensors</strong><br/>
      <a href="LINK_2">Component Details</a></p>
    </td>
    <td align="center">
      <img src="docs/report/compacompra_logo.jpg" alt="Communication Module" width="150"/>
      <p><strong>Communication Module</strong><br/>
      <a href="LINK_3">Component Details</a></p>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="docs/report/compacompra_logo.jpg" alt="Chassis Base" width="150"/>
      <p><strong>Chassis Base</strong><br/>
      <a href="LINK_4">3D Model Download</a></p>
    </td>
    <td align="center">
      <img src="docs/report/compacompra_logo.jpg" alt="Sensor Mount" width="150"/>
      <p><strong>Sensor Mount</strong><br/>
      <a href="LINK_5">3D Model Download</a></p>
    </td>
    <td align="center">
      <img src="docs/report/compacompra_logo.jpg" alt="Component Housing" width="150"/>
      <p><strong>Component Housing</strong><br/>
      <a href="LINK_6">3D Model Download</a></p>
    </td>
  </tr>
</table>

### Connection Diagram

```
[Connection diagram will be inserted here]
```

*Add your system's wiring diagram, showing how all electronic components connect to the main controller.*

### Assembly Instructions

1. **Step 1**: Assemble the 3D printed chassis components
2. **Step 2**: Mount the electronic components according to the connection diagram
3. **Step 3**: Install sensors and calibrate the system
4. **Step 4**: Test all connections and functionality

*[Add detailed assembly instructions with photos]*

## Software

### Software Architecture

The Compa-Compra system follows a modular architecture:

```
┌──────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Mobile App     │    │   Robot System  │    │   Backend API   │
│                  │◄──►│                 │◄──►│                 │
│  - User Interface│    │ - Navigation    │    │ - Product DB    │
│  - Product Lists │    │ - Communication │    │ - Store Maps    │
│  - Preferences   │    │ - Sensors       │    │ - Analytics     │
└──────────────────┘    └─────────────────┘    └─────────────────┘
```

### Requirements and Languages

#### Hardware Requirements
- **Microcontroller**: [Specify your microcontroller]
- **Memory**: [RAM/Storage requirements]
- **Sensors**: [List required sensors]
- **Power**: [Battery/power requirements]

#### Software Requirements
- **Mobile App**: 
  - iOS 12+ / Android 8+
  - [List any specific mobile requirements]
- **Robot System**:
  - [Operating system/firmware requirements]
  - [Any specific libraries or frameworks]

#### Programming Languages
- **Mobile Application**: [e.g., Flutter/Dart, React Native/JavaScript, or Native iOS/Android]
- **Robot Control**: [e.g., C++, Python, Arduino IDE]
- **Backend Services**: [e.g., Node.js, Python, Java]
- **Database**: [e.g., SQLite, PostgreSQL, MongoDB]

### Algorithms

The system implements several key algorithms:

#### 1. Path Planning Algorithm
- **Purpose**: Optimal route calculation through store layout
- **Method**: [e.g., A*, Dijkstra's algorithm, or custom implementation]
- **Input**: Store map, current position, target products
- **Output**: Optimized shopping route

#### 2. Product Recognition
- **Purpose**: Identify products and their locations
- **Method**: [e.g., Computer vision, barcode scanning, RFID]
- **Accuracy**: [Performance metrics if available]

#### 3. Navigation Control
- **Purpose**: Autonomous movement and obstacle avoidance
- **Method**: [e.g., PID control, sensor fusion, mapping]
- **Features**: Real-time obstacle detection and avoidance

## Results

### Videos

| Demo Type | Description | Link |
|-----------|-------------|------|
| Navigation + APP Demo | Autonomous navigation in store | [Watch Video](https://youtu.be/27P_5_Zp0pg) |

### Contributions

This project demonstrates:

- ✅ **Autonomous Navigation**: Successfully navigates store environments
- ✅ **User-Friendly Interface**: Intuitive mobile application
- ✅ **Real-time Communication**: Seamless robot-app integration
- ✅ **Efficient Path Planning**: Optimized shopping routes
- ✅ **Scalable Architecture**: Modular system design

#### Performance Metrics
- **Navigation Accuracy**: [Add your results]
- **Response Time**: [Add your results]
- **Battery Life**: [Add your results]
- **User Satisfaction**: [Add your results if available]

## Authors

**Development Team:**
- [Author Name 1] - [Role/Contribution] - [Email/GitHub]
- [Author Name 2] - [Role/Contribution] - [Email/GitHub]
- [Author Name 3] - [Role/Contribution] - [Email/GitHub]

---

## Getting Started

### Quick Setup
1. Clone this repository
2. Follow the [Hardware Assembly](#assembly-instructions) guide
3. Install the mobile application
4. Upload firmware to the robot system
5. Configure your store layout
6. Start shopping with ComCom! 🛒

### Documentation
- [Hardware Setup Guide](docs/hardware-setup.md)
- [Software Installation](docs/software-installation.md)
- [User Manual](docs/user-manual.md)
- [API Documentation](docs/api-docs.md)

### Support
- **Issues**: Please report bugs and feature requests through GitHub Issues
- **Wiki**: Check our [project wiki](LINK_TO_WIKI) for detailed documentation
- **Contact**: [your-email@example.com]

---

*Made with ❤️ by the Compa-Compra team*