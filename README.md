# AI CCTV Detection Extension (Local Surveillance Prototype)

## Overview

AI-powered local surveillance system built on top of an existing CCTV stream accessed through **Bluestacks + ezyKam+**.

The system captures CCTV frames locally, performs real-time computer vision analysis, identifies suspicious activity, and stores evidence without requiring cloud-based CCTV subscriptions.

---

## High-Level Pipeline

```text
CCTV Camera
      ↓
ezyKam+
      ↓
Bluestacks
      ↓
Background Frame Capture
      ↓
Person Detection (YOLO)
      ↓
Person Tracking (ByteTrack)
      ↓
Zone Mapping / Virtual Fence
      ↓
Face Recognition
      ↓
Risk Assessment Engine
      ↓
Evidence Generation
      ↓
Local Storage & Alerts
```

---

## Architecture

```text
Capture
↓
Detection
↓
Tracking
↓
Zone Mapping
↓
Face Recognition
↓
Risk Engine
↓
Recording & Alerts
```

---

## Core Concepts

### Background Window Capture

Capture CCTV frames directly from Bluestacks even when the application is running in the background.

### Person Detection

Detect human presence in CCTV footage using a lightweight YOLO model optimized for CPU inference.

### Multi-Object Tracking

Assign persistent IDs to detected individuals and track their movement across frames using ByteTrack.

### Face Recognition

Identify known individuals and distinguish them from unknown visitors using facial embeddings.

### Zone Mapping

Define custom zones such as:

* Public Area
* Entry Gate
* Boundary Wall
* Restricted Area
* House Entrance

and monitor movement between them.

### Virtual Fence Detection

Detect intrusion events such as:

* Crossing restricted boundaries
* Entering prohibited zones
* Jumping walls
* Unauthorized access attempts

### Risk Engine

Generate risk scores based on multiple factors:

* Known vs Unknown Person
* Restricted Area Access
* Time of Day
* Face Visibility
* Movement Pattern
* Zone Violations

### Event-Based Recording

Automatically save evidence clips only when meaningful events occur.

### Local Evidence Storage

Store:

* Snapshots
* Detection Events
* Annotated Videos
* Face Data
* Tracking Information

locally on the machine.

---

## Planned Features

* Human Detection
* Multi-Person Tracking
* Known vs Unknown Face Recognition
* Visitor Logging
* Virtual Fence Detection
* Zone-Based Monitoring
* Suspicious Activity Detection
* Event-Based Video Recording
* Evidence Management
* Local Database Integration
* Alert System
* Dashboard & Analytics
* Adaptive Learning Enhancements (Future)

---

## Technologies

### Computer Vision

* OpenCV
* YOLOv8
* ByteTrack
* InsightFace / ArcFace
* NumPy

### Capture Layer

* pywin32
* Windows PrintWindow API
* Bluestacks
* ezyKam+

### Storage

* MongoDB
* MongoDB Compass
* Local Filesystem Storage

### Backend

* Python

### Future Extensions

* Reinforcement Learning
* Risk Scoring Engine
* Notification Services
* Web Dashboard

---

## Project Goals

* Eliminate dependency on cloud CCTV subscriptions
* Perform all processing locally
* Detect and track people in real time
* Identify unknown visitors
* Detect intrusion events
* Preserve only relevant evidence
* Build an intelligent surveillance system capable of understanding activity rather than simply recording footage

```
```
