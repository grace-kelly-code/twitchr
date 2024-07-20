from sense_hat import SenseHat
import time

# COLORS
r = (255, 0, 0)
blu = (90, 250, 250)
w = (213, 214, 219)
blk = (26, 32, 48)
y = (255, 222, 85)
o = (255, 169, 65)

# IMAGES
CLOUD_BASE = [
    blk, blk, blk, w, w, blk, blk, blk,
    blk, blk, w, w, w, w, blk, blk,
    blk, w, w, w, w, w, w, blk,
    w, w, w, w, w, w, w, w,
]

CLOUD = CLOUD_BASE + [blk for i in range(0, 32)]

DRIZZLE = CLOUD_BASE + [
    blk, blk, blu, blk, blk, blu, blk, blk,
    blk, blk, blk, blk, blk, blk, blk, blk,
    blk, blu, blk, blk, blu, blk, blk, blk,
    blk, blk, blk, blk, blk, blk, blk, blk,
]

RAIN = CLOUD_BASE + [
    blk, blu, blk, blk, blu, blk, blu, blk,
    blu, blk, blk, blu, blk, blu, blk, blk,
    blk, blu, blk, blu, blk, blu, blk, blk,
    blk, blk, blk, blk, blk, blk, blk, blk
]

THUNDERSTORM = CLOUD_BASE + [
    blk, blk, blk, blk, y, blk, blk, blk,
    blk, blu, blk, y, blk, blk, blu, blk,
    blk, blk, blk, blk, y, blk, blk, blk,
    blk, blu, blk, y, blk, blk, blu, blk
]

CLEAR = [
    blk, blk, y, y, y, y, blk, blk,
    blk, y, o, o, o, o, y, blk,
    y, o, o, o, o, o, o, y,
    y, o, o, o, o, o, o, y,
    y, o, o, o, o, o, o, y,
    y, o, o, o, o, o, o, y,
    blk, y, o, o, o, o, y, blk,
    blk, blk, y, y, y, y, blk, blk,
]

MIST = [
    w, w, w, w, w, w, w, w,
    blk, blk, blk, blk, blk, blk, blk, blk,
    w, w, w, w, w, w, w, w,
    blk, blk, blk, blk, blk, blk, blk, blk,
    w, w, w, w, w, w, w, w,
    blk, blk, blk, blk, blk, blk, blk, blk,
    w, w, w, w, w, w, w, w,
    blk, blk, blk, blk, blk, blk, blk, blk,
]

UNKNOWN = [
    blk, blk, blk, blk, blk, blk, blk, blk,
    blk, blk, o, o, o, o, blk, blk,
    blk, blk, o, blk, blk, o, blk, blk,
    blk, blk, blk, blk, blk, o, blk, blk,
    blk, blk, blk, o, o, o, blk, blk,
    blk, blk, blk, o, blk, blk, blk, blk,
    blk, blk, blk, blk, blk, blk, blk, blk,
    blk, blk, blk, o, blk, blk, blk, blk,
]

BIRD = [
    blk, blk, blu, blu, blk, blk, blk, blk,
    blk, blu, blu, blu, blu, blk, blk, blk,
    o, blu, w, blu, blu, blk, blk, w,
    blk, blu, blu, blu, w, w, w, w,
    blk, blu, blu, blu, w, w, w, w,
    blk, blk, blu, blu, blu, blu, blu, blk,
    blk, blk, blu, blu, blu, blk, blk, blk,
    blk, blk, o, blk, o, blk, blk, blk
]

CAT = [
    blk, blk, blk, blk, blk, blk, blk, blk,
    blk, blk, blk, o, blk, blk, o, blk,
    blk, blk, blk, o, o, o, o, blk,
    o, o, blk, o, r, o, r, blk,
    o, blk, blk, o, o, o, o, blk,
    o, o, o, o, o, o, blk, blk,
    blk, o, o, o, o, o, blk, blk,
    blk, o, o, blk, o, o, blk, blk
]

IMAGE_MAP = {
    "thunderstorm": THUNDERSTORM,
    "clear": CLEAR,
    "mist": MIST,
    "rain": RAIN,
    "clouds": CLOUD,
    "drizzle": DRIZZLE,
    "bird": BIRD,
    "cat": CAT
}


def draw_message(sense: SenseHat, msg: str) -> None:
    sense.show_message(msg, text_colour=w, back_colour=blk, scroll_speed=.065)
    sense.clear()


def draw_image(sense: SenseHat, image_choice: str) -> None:
    image = IMAGE_MAP[image_choice] if image_choice in IMAGE_MAP else UNKNOWN
    sense.set_pixels(image)


def draw_alert(sense: SenseHat, image_choice: str, msg: str) -> None:
    sense.clear()
    now = time.time()
    future = now + 15
    while time.time() < future:
        draw_message(sense, msg)
        draw_image(sense, image_choice)
        time.sleep(5)
    sense.clear()
