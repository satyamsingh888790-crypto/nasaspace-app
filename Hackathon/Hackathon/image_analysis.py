"""Image Analysis Module using YOLO (Ultralytics)

This module provides a thin wrapper around the Ultralytics YOLO model for:
- Loading a pretrained model (default: yolov8n.pt)
- Running object detection on an uploaded image
- Returning structured detections (class name, confidence, bbox)
- Rendering an annotated image
- Generating a simple textual summary / pseudo-caption from detections

Notes:
- For space-domain specific imagery you would fine-tune a model on spacecraft, debris, etc.
- Here we use the generic COCO-pretrained model for demonstration.
- Heavy downloads happen on first model load; we cache the model in memory.
"""
from __future__ import annotations
import io
from dataclasses import dataclass
from typing import List, Dict, Any

try:
    from ultralytics import YOLO  # type: ignore
except Exception as e:  # pragma: no cover
    YOLO = None  # Fallback if not installed yet

from PIL import Image

@dataclass
class Detection:
    label: str
    confidence: float
    box: Dict[str, float]

class ImageAnalyzer:
    def __init__(self, model_name: str = "yolov8n.pt"):
        if YOLO is None:
            raise RuntimeError("Ultralytics YOLO not available. Install 'ultralytics' first.")
        self.model = YOLO(model_name)

    def detect(self, image: Image.Image, conf: float = 0.25) -> List[Detection]:
        results = self.model.predict(source=image, conf=conf, verbose=False)
        detections: List[Detection] = []
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls.item())
                label = r.names.get(cls_id, str(cls_id))
                confidence = float(box.conf.item())
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                detections.append(Detection(label=label, confidence=confidence, box={
                    "x1": x1, "y1": y1, "x2": x2, "y2": y2
                }))
        return detections

    def annotate(self, image: Image.Image, detections: List[Detection]) -> Image.Image:
        from PIL import ImageDraw, ImageFont
        annotated = image.copy().convert("RGB")
        draw = ImageDraw.Draw(annotated)
        try:
            font = ImageFont.load_default()
        except Exception:
            font = None
        for det in detections:
            b = det.box
            draw.rectangle([(b['x1'], b['y1']), (b['x2'], b['y2'])], outline="lime", width=2)
            text = f"{det.label} {det.confidence*100:.1f}%"
            tw, th = draw.textsize(text, font=font)
            draw.rectangle([(b['x1'], b['y1']-th-4), (b['x1']+tw+4, b['y1'])], fill="black")
            draw.text((b['x1']+2, b['y1']-th-2), text, fill="white", font=font)
        return annotated

    def summarize(self, detections: List[Detection], max_items: int = 5) -> str:
        if not detections:
            return "No objects confidently detected."
        # Aggregate counts by label
        counts: Dict[str, int] = {}
        for d in detections:
            counts[d.label] = counts.get(d.label, 0) + 1
        parts = [f"{cnt} {label}{'s' if cnt>1 else ''}" for label, cnt in sorted(counts.items(), key=lambda x: -x[1])[:max_items]]
        return "Detected: " + ", ".join(parts)


def load_image_analyzer(model_name: str = "yolov8n.pt") -> ImageAnalyzer:
    """Lazy loader with simple exception wrapping."""
    return ImageAnalyzer(model_name=model_name)
