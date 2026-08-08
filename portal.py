import cv2
import numpy as np


class Portal:

    #updated Contructor
    def __init__(self, radius=120):
        def __init__(self, radius=120):
        self.x = 320
        self.y = 240
        self.radius = radius
        # Available portal shapes
        self.shapes = ["circle", "square", "hexagon", "heart"]
        self.current_shape = 0
        
        # NEW: Color Themes (Border BGR, Glow BGR)
        self.themes = [
            {"border": (0, 255, 255), "glow": (255, 180, 0)},   # Default Yellow/Orange
            {"border": (255, 0, 255), "glow": (255, 0, 255)},   # Magenta
            {"border": (0, 255, 0), "glow": (0, 255, 0)},       # Green
            {"border": (255, 0, 0), "glow": (255, 0, 0)}        # Blue
        ]
        self.current_theme = 0

    def next_color(self):
        """Switch to the next portal color theme."""
        self.current_theme = (self.current_theme + 1) % len(self.themes)
        
    def get_theme(self):
        return self.themes[self.current_theme]

        

    # -------------------------
    # Smooth Position Update
    # -------------------------
    def update(self, x, y):

        speed = 0.18

        self.x = int(self.x + (x - self.x) * speed)
        self.y = int(self.y + (y - self.y) * speed)

    # -------------------------
    # Smooth Radius Update
    # -------------------------
    def set_radius(self, radius):

        radius = max(60, min(180, radius))

        speed = 0.20

        self.radius = int(
            self.radius + (radius - self.radius) * speed
        )

    # -------------------------
    #Shape Switcher
    # -------------------------
    def next_shape(self):
        """
        Switch to the next portal shape.
        """
        self.current_shape = (self.current_shape + 1) % len(self.shapes)

    def get_shape(self):
        return self.shapes[self.current_shape]

    # -------------------------
    # Draw Portal
    # -------------------------
    def draw_mask(self, mask):

        shape = self.get_shape()

        if shape == "circle":

            cv2.circle(
                mask,
                (self.x, self.y),
                self.radius,
                255,
                -1
            )

        elif shape == "square":

            cv2.rectangle(
                mask,
                (self.x - self.radius, self.y - self.radius),
                (self.x + self.radius, self.y + self.radius),
                255,
                -1
            )

        elif shape == "hexagon":

            pts = []

            for i in range(6):

                angle = np.deg2rad(60 * i)

                px = int(self.x + self.radius * np.cos(angle))
                py = int(self.y + self.radius * np.sin(angle))

                pts.append([px, py])

            pts = np.array([pts], dtype=np.int32)

            cv2.fillPoly(mask, pts, 255)

        elif shape == "heart":

            pts = []

            for t in np.linspace(0, 2 * np.pi, 300):

                x = 16 * (np.sin(t) ** 3)
                y = (
                    13 * np.cos(t)
                    - 5 * np.cos(2 * t)
                    - 2 * np.cos(3 * t)
                    - np.cos(4 * t)
                )

                px = int(self.x + x * self.radius / 18)
                py = int(self.y - y * self.radius / 18)

                pts.append([px, py])

            pts = np.array([pts], dtype=np.int32)

            cv2.fillPoly(mask, pts, 255)

    # -------------------------
    # Draw Portal Glow
    # -------------------------
    def draw_glow(self, frame):

        glow = frame.copy()

        shape = self.get_shape()

        if shape == "circle":

            for r in range(self.radius + 8, self.radius + 36, 8):

                cv2.circle(
                    glow,
                    (self.x, self.y),
                    r,
                    (255, 180, 0),
                    2,
                    cv2.LINE_AA
                )

        elif shape == "square":

            for offset in range(8, 36, 8):

                cv2.rectangle(
                    glow,
                    (self.x - self.radius - offset,
                    self.y - self.radius - offset),

                    (self.x + self.radius + offset,
                    self.y + self.radius + offset),

                    (255, 180, 0),
                    2,
                    cv2.LINE_AA
                )

        elif shape == "hexagon":

            for offset in range(8, 36, 8):

                pts = []

                r = self.radius + offset

                for i in range(6):

                    angle = np.deg2rad(60 * i)

                    px = int(self.x + r * np.cos(angle))
                    py = int(self.y + r * np.sin(angle))

                    pts.append([px, py])

                pts = np.array([pts], dtype=np.int32)

                cv2.polylines(
                    glow,
                    pts,
                    True,
                    (255, 180, 0),
                    2,
                    cv2.LINE_AA
                )

        elif shape == "heart":

            for offset in range(8, 36, 8):

                pts = []

                scale = (self.radius + offset) / 18

                for t in np.linspace(0, 2 * np.pi, 300):

                    x = 16 * (np.sin(t) ** 3)
                    y = (
                        13 * np.cos(t)
                        - 5 * np.cos(2 * t)
                        - 2 * np.cos(3 * t)
                        - np.cos(4 * t)
                    )

                    px = int(self.x + x * scale)
                    py = int(self.y - y * scale)

                    pts.append([px, py])

                pts = np.array([pts], dtype=np.int32)

                cv2.polylines(
                    glow,
                    pts,
                    True,
                    (255, 180, 0),
                    2,
                    cv2.LINE_AA
                )

        return cv2.addWeighted(
            glow,
            0.30,
            frame,
            0.70,
            0
        )

    def draw_border(self, frame):

        shape = self.get_shape()

        if shape == "circle":

            cv2.circle(
                frame,
                (self.x, self.y),
                self.radius,
                (0,255,255),
                3,
                cv2.LINE_AA
            )

            cv2.circle(
                frame,
                (self.x, self.y),
                self.radius-4,
                (255,255,255),
                2,
                cv2.LINE_AA
            )

        elif shape == "square":

            cv2.rectangle(
                frame,
                (self.x-self.radius,self.y-self.radius),
                (self.x+self.radius,self.y+self.radius),
                (0,255,255),
                3, cv2.LINE_AA
            )
            cv2.rectangle(
                frame,
                (self.x-self.radius+4,
                self.y-self.radius+4),

                (self.x+self.radius-4,
                self.y+self.radius-4),

                (255,255,255),
                2,
                cv2.LINE_AA
            )

        elif shape == "hexagon":

            pts=[]

            for i in range(6):

                angle=np.deg2rad(60*i)

                pts.append([
                    int(self.x+self.radius*np.cos(angle)),
                    int(self.y+self.radius*np.sin(angle))
                ])

            pts=np.array([pts],dtype=np.int32)

            cv2.polylines(
                frame,
                pts,
                True,
                (0,255,255),
                3
            )
            pts=[]

            for i in range(6):

                angle=np.deg2rad(60*i)

                px=int(self.x+(self.radius-4)*np.cos(angle))
                py=int(self.y+(self.radius-4)*np.sin(angle))

                pts.append([px,py])

            pts=np.array([pts],dtype=np.int32)

            cv2.polylines(
                frame,
                pts,
                True,
                (255,255,255),
                2,
                cv2.LINE_AA
            )

        elif shape == "heart":

            pts = []

            scale = self.radius / 18

            for t in np.linspace(0, 2 * np.pi, 300):

                x = 16 * (np.sin(t) ** 3)
                y = (
                    13 * np.cos(t)
                    - 5 * np.cos(2 * t)
                    - 2 * np.cos(3 * t)
                    - np.cos(4 * t)
                )

                px = int(self.x + x * scale)
                py = int(self.y - y * scale)

                pts.append([px, py])

            pts = np.array([pts], dtype=np.int32)

            cv2.polylines(
                frame,
                pts,
                True,
                (0, 255, 255),
                3,
                cv2.LINE_AA
            )

            # Inner Border
            pts = []

            scale = (self.radius - 4) / 18

            for t in np.linspace(0, 2 * np.pi, 300):

                x = 16 * (np.sin(t) ** 3)
                y = (
                    13 * np.cos(t)
                    - 5 * np.cos(2 * t)
                    - 2 * np.cos(3 * t)
                    - np.cos(4 * t)
                )

                px = int(self.x + x * scale)
                py = int(self.y - y * scale)

                pts.append([px, py])

            pts = np.array([pts], dtype=np.int32)

            cv2.polylines(
                frame,
                pts,
                True,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )

    def draw(self, frame, background):

        h, w = frame.shape[:2]

        # Create Portal Mask
        mask = np.zeros((h, w), dtype=np.uint8)

        self.draw_mask(mask)
        

        # Soft Edge
        mask = cv2.GaussianBlur(mask, (15, 15), 4)

        alpha = mask.astype(np.float32) / 255.0
        alpha = cv2.merge([alpha, alpha, alpha])

    # Match brightness of captured background to current frame
        bg = background.copy()

        result = (
            frame.astype(np.float32) * (1 - alpha)
            + bg.astype(np.float32) * alpha
        )

        result = result.astype(np.uint8)

        # Glow
        self.draw_glow(result)

        # Border
        self.draw_border(result)
        
        # Center Crosshair
        cv2.line(
            result,
            (self.x - 10, self.y),
            (self.x + 10, self.y),
            (0, 255, 255),
            2,
            cv2.LINE_AA
        )

        cv2.line(
            result,
            (self.x, self.y - 10),
            (self.x, self.y + 10),
            (0, 255, 255),
            2,
            cv2.LINE_AA
        )

        return result