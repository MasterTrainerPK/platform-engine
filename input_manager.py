import pygame
import collections
# This is a lot of repeated code... maybe make it one thing with a simple parameter?
_key_down_events = [collections.defaultdict(list)]
_key_up_events = [collections.defaultdict(list)]
_mouse_down_events = [collections.defaultdict(list)]
_mouse_up_events = [collections.defaultdict(list)]
events_lists = [_key_up_events, _key_down_events,
                _mouse_up_events, _mouse_down_events]
keys = set()
m_buttons = set()


def event(e):
    match e.type:
        case pygame.MOUSEBUTTONDOWN:
            if e.button in m_buttons:
                print("Something weird is happening")
            else:
                m_buttons.add(e.button)
            for x in _mouse_down_events[-1][e.button]:
                x(e)
        case pygame.MOUSEBUTTONUP:
            if e.button not in m_buttons:
                print("Something weird is happening")
            else:
                m_buttons.remove(e.button)
            for x in _mouse_up_events[-1][e.button]:
                x(e)
        case pygame.KEYDOWN:
            if e.key in keys:
                print("Something weird is happening")
            else:
                keys.add(e.key)
            for x in _key_down_events[-1][e.key]:
                x(e)
        case pygame.KEYUP:
            if e.key not in keys:
                print("Something weird is happening")
            else:
                keys.remove(e.key)
            for x in _key_up_events[-1][e.key]:
                x(e)
        case _:
            pass
            # print("Don't know how to receive", e.type, "Event")


def input_handler_push():
    for events_list in events_lists:
        events_list.append(collections.defaultdict(list))


def input_handler_pop():
    for events_list in events_lists:
        events_list.pop()


def register(event, key, event_list):
    print("registering event")
    event_list[-1][key].append(event)
    print(key)


def on_key_down(key):
    if isinstance(key, str):
        key = ord(key)

    def inner(event):
        register(event, key, _key_down_events)
        return event
    return inner


def on_key_up(key):
    if isinstance(key, str):
        key = ord(key)

    def inner(event):
        register(event, key, _key_up_events)
        return event
    return inner


def on_m_button_down(key):
    def inner(event):
        register(event, key, _mouse_down_events)
        return event
    return inner


def on_m_button_up(key):
    def inner(event):
        register(event, key, _mouse_up_events)
        return event
    return inner
