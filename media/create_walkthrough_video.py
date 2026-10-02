"""Render a short narrated walkthrough of the NINR AI workshop repository."""

from __future__ import annotations

import asyncio
import csv
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont
from moviepy import AudioFileClip
import edge_tts
import imageio_ffmpeg


ROOT = Path(__file__).resolve().parents[1]
MEDIA = Path(__file__).resolve().parent
BUILD = MEDIA / "walkthrough_build"
OUTPUT = MEDIA / "ninr_ai_bootcamp_walkthrough.mp4"
THUMBNAIL = MEDIA / "ninr_ai_bootcamp_walkthrough_thumbnail.png"

WIDTH, HEIGHT = 1280, 720
FPS = 24

NAVY = "#14213D"
NAVY_2 = "#1E3158"
PURPLE = "#6554C0"
LAVENDER = "#EDE9FE"
TEAL = "#1F9D8A"
PALE_TEAL = "#DDF5EF"
GOLD = "#F6C85F"
PALE_GOLD = "#FFF4CF"
CORAL = "#E56B6F"
WHITE = "#FFFFFF"
INK = "#172033"
MUTED = "#5D6678"
PAPER = "#F7F8FC"


SCENES = [
    {
        "eyebrow": "NINR AI SUMMER RESEARCH INTENSIVE",
        "title": "A beginner-friendly home for learning responsible AI with health data",
        "subtitle": "A two-minute tour of the workshop repository",
        "narration": (
            "This is the NINR AI Summer Research Intensive repository: a beginner-friendly home for nursing scientists "
            "to learn responsible artificial intelligence with real health data. No previous coding, statistics, or machine-learning experience is required."
        ),
        "kind": "title",
    },
    {
        "eyebrow": "ONE REPOSITORY · MANY NURSING QUESTIONS",
        "title": "20 participant-ready public datasets",
        "subtitle": "Organized around questions nursing scientists actually study",
        "narration": (
            "The repository offers twenty public datasets organized around questions nursing scientists actually study. "
            "Participants can explore clinical outcomes, symptoms and monitoring, health behavior and workforce, or environment and care quality."
        ),
        "kind": "portfolio",
    },
    {
        "eyebrow": "TRUSTWORTHY BY DESIGN",
        "title": "From official source to workshop-ready data",
        "subtitle": "Every transformation can be inspected and reproduced",
        "narration": (
            "Each dataset starts with an official or original source. The repository preserves provenance, creates an approachable participant file, "
            "and supplies a data dictionary, research questions, risk flags, and automated validation. This lets learners ask not only what a model can predict, but whether the data and design support the claim."
        ),
        "kind": "pipeline",
    },
    {
        "eyebrow": "GUIDED DAY 1 LAB",
        "title": "Learning with a real diabetes readmission dataset",
        "subtitle": "A supported first experience with clinical data",
        "narration": (
            "The guided Day One lab uses real diabetes hospitalization data. Learners open a prepared notebook, examine patient and health-services variables, "
            "create simple summaries and visualizations, and discuss what thirty-day readmission can and cannot tell us."
        ),
        "kind": "diabetes",
    },
    {
        "eyebrow": "INTERACTIVE ACTIVITY 2",
        "title": "Can today's data predict tomorrow's fatigue?",
        "subtitle": "Patient reports + wearable signals + time context",
        "narration": (
            "A second interactive activity asks whether today's patient reports, wearable signals, and time context can predict tomorrow's fatigue. "
            "It uses an openly available repeated-measures dataset and clearly identifies that electronic health record data are not present."
        ),
        "kind": "fatigue",
    },
    {
        "eyebrow": "DESIGNED FOR FIRST-TIME LEARNERS",
        "title": "Learn → Do → Notice → Explain",
        "subtitle": "Concepts come before algorithms",
        "narration": (
            "The activity teaches one idea at a time. Participants learn plain-language vocabulary, make a prediction themselves, explore one person's trajectory, "
            "and compare a simple rule with a basic machine-learning model. Prompts help them notice patterns, explain results, and avoid confusing prediction with causation."
        ),
        "kind": "learning",
    },
    {
        "eyebrow": "READY TO TEACH",
        "title": "Participant materials and an instructor guide",
        "subtitle": "Notebook · walkthrough · teaching guide · answer key",
        "narration": (
            "The finished package includes interactive notebooks, a step-by-step participant walkthrough, and an instructor guide with timing, discussion prompts, answer keys, and optional extensions. "
            "Together, the materials make responsible AI concrete, approachable, and relevant to nursing research. Explore the repository at github dot com slash sonya dash j slash N I N R dash A I dash bootcamp."
        ),
        "kind": "close",
    },
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    names = [
        "C:/Windows/Fonts/seguisb.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for name in names:
        if Path(name).exists():
            return ImageFont.truetype(name, size)
    return ImageFont.load_default()


def wrap(draw: ImageDraw.ImageDraw, text: str, face: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textbbox((0, 0), candidate, font=face)[2] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill: str, radius: int = 24, outline: str | None = None, width: int = 1) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def base_canvas(scene: dict, index: int) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(image)
    # Header band and small visual anchors.
    draw.rectangle((0, 0, WIDTH, 98), fill=NAVY)
    draw.rounded_rectangle((54, 30, 84, 60), radius=8, fill=TEAL)
    draw.text((99, 33), "NINR AI SUMMER RESEARCH INTENSIVE", font=font(20, True), fill=WHITE)
    draw.text((1218, 34), f"{index + 1:02d} / {len(SCENES):02d}", font=font(18, True), fill="#C9D2E3", anchor="ra")
    draw.text((62, 130), scene["eyebrow"], font=font(18, True), fill=PURPLE)

    title_face = font(45, True)
    y = 165
    for line in wrap(draw, scene["title"], title_face, 1120):
        draw.text((62, y), line, font=title_face, fill=INK)
        y += 56
    draw.text((64, y + 4), scene["subtitle"], font=font(24), fill=MUTED)

    draw.rectangle((0, 655, WIDTH, HEIGHT), fill=NAVY)
    caption = short_caption(scene["narration"])
    caption_lines = wrap(draw, caption, font(21), 1130)
    cy = 668 if len(caption_lines) == 1 else 660
    for line in caption_lines[:2]:
        draw.text((64, cy), line, font=font(21), fill=WHITE)
        cy += 28
    return image, draw


def short_caption(text: str) -> str:
    replacements = {
        "The repository ": "This repository ",
        "The activity ": "The activity ",
    }
    first = text.split(". ")[0].strip() + "."
    for source, target in replacements.items():
        first = first.replace(source, target)
    return first


def card(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, title: str, body: str, color: str, number: str | None = None) -> None:
    rounded(draw, (x, y, x + w, y + h), WHITE, 22, "#DFE4ED")
    draw.rectangle((x, y, x + 9, y + h), fill=color)
    if number:
        rounded(draw, (x + 24, y + 20, x + 72, y + 68), color, 14)
        draw.text((x + 38, y + 29), number, font=font(20, True), fill=WHITE, anchor="mm")
        text_x = x + 90
    else:
        text_x = x + 28
    draw.text((text_x, y + 21), title, font=font(23, True), fill=INK)
    body_size = 16 if h < 90 else 18
    body_y = y + 50 if h < 90 else y + 57
    lines = wrap(draw, body, font(body_size), w - (text_x - x) - 24)
    for i, line in enumerate(lines[:3]):
        draw.text((text_x, body_y + i * 23), line, font=font(body_size), fill=MUTED)


def draw_title(image: Image.Image, draw: ImageDraw.ImageDraw) -> None:
    # Replace standard content area with a bold hero composition.
    draw.rounded_rectangle((62, 324, 1218, 606), radius=32, fill=WHITE, outline="#DFE4ED", width=2)
    draw.text((108, 365), "20", font=font(82, True), fill=PURPLE)
    draw.text((108, 455), "documented datasets", font=font(25, True), fill=INK)
    draw.line((390, 365, 390, 556), fill="#E2E6EE", width=3)
    items = [
        ("Official sources", TEAL),
        ("Beginner notebooks", PURPLE),
        ("Responsible-AI guidance", CORAL),
    ]
    for i, (label, color) in enumerate(items):
        y = 366 + i * 65
        rounded(draw, (440, y, 478, y + 38), color, 11)
        draw.text((501, y + 4), label, font=font(27, True), fill=INK)


def draw_portfolio(image: Image.Image, draw: ImageDraw.ImageDraw) -> None:
    cards = [
        ("Clinical care & outcomes", "Readmission, serious illness, acute care", TEAL),
        ("Symptoms & monitoring", "Parkinson symptoms, fetal monitoring, fatigue", PURPLE),
        ("Health behavior & workforce", "Sleep, aging, caregiving, absenteeism", GOLD),
        ("Environment & care quality", "Air quality, communication, patient experience", CORAL),
    ]
    for i, (title, body, color) in enumerate(cards):
        x = 62 + (i % 2) * 584
        y = 310 + (i // 2) * 152
        card(draw, x, y, 548, 126, title, body, color)


def draw_pipeline(image: Image.Image, draw: ImageDraw.ImageDraw) -> None:
    steps = [
        ("1", "Official source", "Original public data", TEAL),
        ("2", "Prepare", "Reproducible Python", PURPLE),
        ("3", "Teach", "CSV + dictionary", GOLD),
        ("4", "Question", "Risks + validation", CORAL),
    ]
    for i, (num, title, body, color) in enumerate(steps):
        x = 62 + i * 295
        y = 345
        rounded(draw, (x, y, x + 245, y + 155), WHITE, 24, "#DFE4ED")
        rounded(draw, (x + 20, y + 20, x + 66, y + 66), color, 14)
        draw.text((x + 43, y + 43), num, font=font(21, True), fill=WHITE, anchor="mm")
        draw.text((x + 20, y + 82), title, font=font(23, True), fill=INK)
        draw.text((x + 20, y + 117), body, font=font(18), fill=MUTED)
        if i < len(steps) - 1:
            draw.line((x + 251, y + 76, x + 281, y + 76), fill="#AEB7C7", width=4)
            draw.polygon([(x + 281, y + 76), (x + 269, y + 69), (x + 269, y + 83)], fill="#AEB7C7")
    rounded(draw, (244, 535, 1036, 595), PALE_TEAL, 18)
    draw.text((640, 565), "Every step is documented, inspectable, and repeatable", font=font(24, True), fill="#166456", anchor="mm")


def draw_diabetes(image: Image.Image, draw: ImageDraw.ImageDraw) -> None:
    rounded(draw, (62, 320, 743, 600), WHITE, 26, "#DFE4ED")
    draw.rectangle((62, 320, 743, 370), fill=NAVY_2)
    draw.text((88, 333), "01_day1_python_and_clinical_data.ipynb", font=font(21, True), fill=WHITE)
    draw.text((92, 398), "Research question", font=font(18, True), fill=PURPLE)
    question = "Which patient and care characteristics are associated with 30-day readmission?"
    for i, line in enumerate(wrap(draw, question, font(28, True), 595)):
        draw.text((92, 431 + i * 36), line, font=font(28, True), fill=INK)
    draw.text((92, 535), "5,000 encounters  ·  26 core variables  ·  guided analysis", font=font(19), fill=MUTED)

    checklist = [("Explore the data", True), ("Create a visualization", True), ("Interpret carefully", True)]
    for i, (label, _) in enumerate(checklist):
        y = 350 + i * 75
        rounded(draw, (795, y, 1200, y + 56), PALE_TEAL if i != 1 else LAVENDER, 17)
        draw.ellipse((816, y + 14, 844, y + 42), fill=TEAL if i != 1 else PURPLE)
        draw.text((830, y + 27), "✓", font=font(18, True), fill=WHITE, anchor="mm")
        draw.text((862, y + 14), label, font=font(22, True), fill=INK)


def load_fatigue_series() -> list[float]:
    path = ROOT / "data/processed/multimodal_symptom_trajectories/participant_day.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        rows = [row for row in csv.DictReader(handle) if row["participant_id"] == "1" and row["fatigue_today"]]
    return [float(row["fatigue_today"]) for row in rows[:12]]


def draw_fatigue(image: Image.Image, draw: ImageDraw.ImageDraw) -> None:
    labels = [("Patient reports", TEAL), ("Wearable signals", PURPLE), ("Time context", GOLD)]
    for i, (label, color) in enumerate(labels):
        x = 62 + i * 243
        rounded(draw, (x, 314, x + 218, 367), color, 16)
        draw.text((x + 109, 340), label, font=font(20, True), fill=WHITE if color != GOLD else INK, anchor="mm")
    rounded(draw, (807, 314, 1218, 367), "#FBE7E8", 16)
    draw.text((1012, 340), "EHR data: not present", font=font(20, True), fill="#9B3539", anchor="mm")

    chart = (92, 408, 1180, 595)
    rounded(draw, (62, 390, 1218, 617), WHITE, 24, "#DFE4ED")
    x0, y0, x1, y1 = chart
    draw.line((x0, y1, x1, y1), fill="#AEB7C7", width=2)
    draw.line((x0, y0, x0, y1), fill="#AEB7C7", width=2)
    for score in [1, 5, 10]:
        y = y1 - (score - 1) / 9 * (y1 - y0)
        draw.line((x0, y, x1, y), fill="#E8EBF1", width=1)
        draw.text((70, y - 10), str(score), font=font(15), fill=MUTED)
    values = load_fatigue_series()
    points = []
    for i, value in enumerate(values):
        x = x0 + i / max(1, len(values) - 1) * (x1 - x0)
        y = y1 - (value - 1) / 9 * (y1 - y0)
        points.append((x, y))
    draw.line(points, fill=PURPLE, width=5, joint="curve")
    for x, y in points:
        draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill=PURPLE, outline=WHITE, width=2)
    draw.text((108, 417), "A real participant's daily fatigue trajectory", font=font(17, True), fill=MUTED)


def draw_learning(image: Image.Image, draw: ImageDraw.ImageDraw) -> None:
    stages = [
        ("1", "Learn", "Plain-language terms", TEAL),
        ("2", "Do", "Make a prediction", PURPLE),
        ("3", "Notice", "Explore the pattern", GOLD),
        ("4", "Explain", "State the evidence", CORAL),
    ]
    for i, (num, title, body, color) in enumerate(stages):
        x = 62 + i * 294
        y = 337
        draw.ellipse((x + 72, y, x + 170, y + 98), fill=color)
        draw.text((x + 121, y + 49), num, font=font(34, True), fill=WHITE if color != GOLD else INK, anchor="mm")
        draw.text((x + 121, y + 119), title, font=font(28, True), fill=INK, anchor="mm")
        lines = wrap(draw, body, font(18), 230)
        for j, line in enumerate(lines):
            draw.text((x + 121, y + 160 + j * 24), line, font=font(18), fill=MUTED, anchor="mm")
        if i < 3:
            draw.line((x + 184, y + 48, x + 275, y + 48), fill="#AEB7C7", width=4)
            draw.polygon([(x + 275, y + 48), (x + 261, y + 39), (x + 261, y + 57)], fill="#AEB7C7")
    rounded(draw, (235, 558, 1045, 610), LAVENDER, 16)
    draw.text((640, 584), "No coding required · a simple rule comes before machine learning", font=font(21, True), fill="#493A99", anchor="mm")


def draw_close(image: Image.Image, draw: ImageDraw.ImageDraw) -> None:
    items = [
        ("Interactive notebooks", "Run prepared steps in Google Colab", TEAL),
        ("Participant walkthrough", "Learn, reflect, and explain", PURPLE),
        ("Instructor guide", "Timing, prompts, answers, and extensions", CORAL),
    ]
    for i, (title, body, color) in enumerate(items):
        card(draw, 62, 316 + i * 94, 688, 76, title, body, color)
    rounded(draw, (792, 316, 1218, 576), NAVY, 28)
    draw.text((1005, 357), "EXPLORE THE REPOSITORY", font=font(17, True), fill="#A9B8D1", anchor="mm")
    draw.text((1005, 410), "github.com", font=font(28, True), fill=WHITE, anchor="mm")
    draw.text((1005, 453), "sonya-j /", font=font(31, True), fill=GOLD, anchor="mm")
    draw.text((1005, 494), "ninr-ai-bootcamp", font=font(31, True), fill=GOLD, anchor="mm")
    draw.text((1005, 545), "Open · reproducible · ready to teach", font=font(17), fill="#D7DEEB", anchor="mm")


DRAWERS = {
    "title": draw_title,
    "portfolio": draw_portfolio,
    "pipeline": draw_pipeline,
    "diabetes": draw_diabetes,
    "fatigue": draw_fatigue,
    "learning": draw_learning,
    "close": draw_close,
}


async def synthesize(text: str, output: Path) -> None:
    speech = edge_tts.Communicate(text, voice="en-US-JennyNeural", rate="-5%")
    await speech.save(str(output))


def main() -> None:
    BUILD.mkdir(parents=True, exist_ok=True)
    image_paths: list[Path] = []
    audio_paths: list[Path] = []

    for index, scene in enumerate(SCENES):
        image, draw = base_canvas(scene, index)
        DRAWERS[scene["kind"]](image, draw)
        image_path = BUILD / f"scene_{index + 1:02d}.png"
        image.save(image_path, quality=95)
        image_paths.append(image_path)

        audio_path = BUILD / f"scene_{index + 1:02d}.mp3"
        asyncio.run(synthesize(scene["narration"], audio_path))
        audio_paths.append(audio_path)

    audio_clips = [AudioFileClip(str(path)) for path in audio_paths]
    durations = [clip.duration + 0.55 for clip in audio_clips]
    for audio in audio_clips:
        audio.close()

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    segment_paths: list[Path] = []
    for index, (image_path, audio_path, duration) in enumerate(zip(image_paths, audio_paths, durations)):
        segment = BUILD / f"segment_{index + 1:02d}.mp4"
        subprocess.run(
            [
                ffmpeg,
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-loop",
                "1",
                "-framerate",
                str(FPS),
                "-i",
                str(image_path),
                "-i",
                str(audio_path),
                "-af",
                "apad=pad_dur=0.55",
                "-t",
                f"{duration:.3f}",
                "-c:v",
                "libx264",
                "-preset",
                "medium",
                "-tune",
                "stillimage",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-b:a",
                "128k",
                str(segment),
            ],
            check=True,
        )
        segment_paths.append(segment)

    concat_file = BUILD / "segments.txt"
    concat_file.write_text(
        "".join(f"file '{path.as_posix()}'\n" for path in segment_paths),
        encoding="utf-8",
    )
    subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c",
            "copy",
            "-movflags",
            "+faststart",
            str(OUTPUT),
        ],
        check=True,
    )

    Image.open(image_paths[0]).save(THUMBNAIL)
    print(f"Created {OUTPUT}")
    print(f"Duration: {sum(durations):.1f} seconds")
    print(f"Size: {OUTPUT.stat().st_size / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    main()
