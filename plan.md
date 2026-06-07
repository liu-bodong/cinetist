USE THIS AS A REFERENCE, NOT STRICT GUIDELINES.

# System Architecture & Technical Specification: Interactive Movie Analyzer

## 1. Project Goal
The objective is to develop a lightweight, user-friendly, and open-source desktop/web application that treats video files as structured datasets. The system automates the extraction of structural, cinematic, colorimetric, and narrative features from feature-length films, compiling them into a highly portable metadata format (JSON/SQLite). A rich, interactive, hardware-accelerated dashboard then synchronizes these quantitative metrics back to a frame-accurate video stream, allowing researchers, editors, and film enthusiasts to easily share, aggregate, and visualize cinematic trends without re-processing raw media.

---

## 2. Benchmark Reference Architecture
To inform development, the system builds on and refines paradigms from established professional and academic tools:
* **Cinemetrics (cinemetrics.lv):** Replicates the calculation of Average Shot Length (ASL) and editing frequency distributions, shifting from manual logging to automated computer-vision processing.
* **VIAN (Visual Annotator):** Emulates its core philosophy of colorimetric data visualization over sequential timelines, optimizing pixel segregation using lightweight clustering techniques.
* **CineScale Framework:** Utilizes established shot-scale ontologies (Extreme Close-Up to Extreme Long Shot) verified by automated CNN feature extraction.

---

## 3. Core Technical Features

### 1. Temporal Segmentation (Shot Detection)
* **Mechanism:** Programmatic boundary tracking via pixel-difference analysis and frame edge-intensity shifts.
* **Execution:** Automated identification of hard cuts, fades, and cross-dissolves.
* **Output:** Continuous array of precise millisecond-level timecodes defining discrete shot intervals ($S_1, S_2, \dots, S_n$).

### 2. Compositional & Framing Classifiers (Scale & Angle)
* **Spatial Metrics:** Spatial categorization of framing layout mapped against the primary human subject.
* **Shot Scale:** Classification into discrete categories: *Extreme Close-Up (ECU), Close-Up (CU), Medium Shot (MS), Long Shot (LS), Extreme Long Shot (ELS)*.
* **Shot Angle:** Geometric classification of camera placement relative to the subject's horizon: *Overhead, High-Angle, Eye-Level, Low-Angle, Dutch Angle*.

### 3. Spatial Colorimetry (Color Palette Extraction)
* **Color-Space Processing:** Downsampling of uniform shot keyframes and conversion from standard sRGB to a perceptually uniform color space (CIE $L^*a^*b^*$ or HSV).
* **Clustering:** Vector quantization to isolate dominant spatial colors per individual shot.
* **Output:** Multi-hex array mapped alongside proportional pixel coverage values per shot.

### 4. Semantic Parsing (Character & Theme Detection)
* **Identity Tracking:** Frame-level facial recognition clustering and bounding-box object grouping to trace unique character presence timelines without external model training.
* **Narrative/Thematic Modeling:** Extraction of time-stamped audio/subtitle tracks, parsed through lightweight natural language embedding pipelines to output cluster tags reflecting narrative sentiment or theme (e.g., *conflict, intimacy, tension*).

### 5. Multi-Tier Hardware-Accelerated Dashboards
* **Movie Barcode Canvas:** A continuous, single-strip canvas rendering chronological keyframe slices or localized color blocks.
* **Pacing Scatterplots:** Two-dimensional scatterplot tracking runtime duration ($X$-axis) against discrete shot length ($Y$-axis) to trace micro and macro editing variations.
* **Bi-Directional Video Bridge:** Synchronized state engine binding interactive chart vectors directly to a custom video transport controller; selecting data intervals instantly adjusts the media player state to that exact frame sequence.

---

## 4. Technical Stack

```
                     ┌──────────────────────────────────────────────┐
                     │          React (Vite / TypeScript)           │
                     │  - State Engine: Zustand / Context API       │
                     │  - Charting: Apache ECharts (Canvas Core)     │
                     │  - Video Transport: Vidstack Player          │
                     └──────────────────────┬───────────────────────┘
                                            │
                                            ▼  [ HTTP REST / JSON ]
                     ┌──────────────────────────────────────────────┐
                     │               Python Backend                 │
                     │  - API Layer: FastAPI (Asynchronous AsyncIO) │
                     └──────────────────────┬───────────────────────┘
                                            │
                ┌───────────────────────────┴───────────────────────────┐
                ▼                                                       ▼
┌───────────────────────────────┐                       ┌───────────────────────────────┐
│     Processing Engine         │                       │         Storage Layer         │
│ - Video I/O: OpenCV / FFmpeg  │                       │ - Relational: SQLite          │
│ - Segmentation: PySceneDetect │                       │ - Portability: Pydantic JSON  │
│ - ML Core: PyTorch (ResNet)   │                       └───────────────────────────────┘
│ - Audio/Text: Faster-Whisper  │
└───────────────────────────────┘
```

### Frontend Platform
* **Framework Architecture:** **React (Vite + TypeScript)** — Selected for compile-time safety and high-performance DOM reconciliation.
* **Component Architecture:** **Tailwind CSS + shadcn/ui** — Strict utility-first rendering layer for clean design standards.
* **Data Visualization Kernel:** **Apache ECharts** (via `echarts-for-react`) — Employs native HTML5 Canvas/WebGL rendering pipelines to remain fully performant while rendering multi-thousand node data series.
* **Media Transport Layer:** **Vidstack Engine** — Highly configurable framework offering precise programmatic state hooks directly over HTML5 audio/video objects.

### Backend Infrastructure
* **Application Server:** **FastAPI (Python)** — Asynchronous ASGI server optimizing multi-threaded execution loops.
* **Segmentation Subsystem:** **`pyscenedetect`** — Leverages content-aware threshold analysis over sequential HSV channels.
* **Deep Learning Pipeline:** **PyTorch** — Deep-learning runtime loading lightweight pre-trained classifiers (`ResNet-50` / `EfficientNet-B0`) optimized via ONNX/TensorRT for processing local frames.
* **Color Processing Pipeline:** **OpenCV + Scikit-Learn** — Custom execution pipelines running vector clustering (K-Means) directly across downsampled arrays.
* **Transcription/Audio Engine:** **`faster-whisper`** — Quantized execution of OpenAI's Whisper engine to maximize local processing efficiency.

### Storage & Serialization Model
* **Local Persistence Engine:** **SQLite** — Serverless engine mapping nested shot structures directly into indexed local database tables.
* **Interoperable Schema Layout:** **Pydantic Serialization Models** — Validates strict typing boundaries to compile complete movie profiles into modular, platform-agnostic, easily shareable `.json` text objects.