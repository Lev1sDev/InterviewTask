import datetime as dt

from dummy_server.server import get_random_request

# Dummy server generates random requests,
# your goal is to process them as per task requirements (see README.md)


def text_handler(request):
    date = request.get('ts')

    if date.weekday() in (5, 6):
        if date.weekday() == 5:
            return "\U00000035"
        return "\U00000036"

    else:
        text = request.get('content')
        return len(list(set(text.split())))


def image_handler(request):
    image = request.get('content')
    ext = None

    for i in range(len(image)):
        if image[i] == '.':
            ext = (image[i + 1:len(image)], i)
            break

    if ext[0] == 'jpg':
        return image[:ext[1]]
    return request.get('ts') - dt.timedelta(hours=24)


def video_handler(request):
    date = request.get('ts')
    ext = None
    video = request.get('content')

    for i in range(len(video)):
        if video[i] == '.':
            ext = video[i + 1:len(video)]
            break

    if date.weekday() in (5, 6):
        if len(ext) == 4:
            return 'OK'
        return 'REJECT'

    else:
        if len(ext) == 3:
            return 'OK'
        return 'REJECT'


def sound_handler(request):
    sound = request.get('content')

    for symbol in sound:
        if sound.count(symbol) == 1:
            return symbol
    return None


if __name__ == "__main__":
    text, image, video, sound = 0, 0, 0, 0
    # Don't stop processing requests until we received at least 2 requests
    # of each type.
    while text < 2 or image < 2 or video < 2 or sound < 2:
        request = get_random_request()
        # Ignore image and video requests
        # if they were sent more than 4 days ago
        if (request.get('type') in ('image', 'video') and
                request.get('ts') < dt.datetime.now() - dt.timedelta(days=4)):
            continue
        print(request)
        if request.get('type') == 'text':
            print(text_handler(request))
            text += 1
        elif request.get('type') == 'image':
            print(image_handler(request))
            image += 1
        elif request.get('type') == 'video':
            print(video_handler(request))
            video += 1
        elif request.get('type') == 'sound':
            print(sound_handler(request))
            sound += 1
    # Print amount of all received requests by types
    print(
        f'Requests count: {text + image + video + sound}\n'
        f'text = {text}\n'
        f'image = {image}\n'
        f'video = {video}\n'
        f'sound = {sound}\n'
    )
