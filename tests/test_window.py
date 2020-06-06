import ahk


def test_windows(child_ahk):
    def windows():
        import ahk
        import sys

        ahk.hotkey("F24", sys.exit)

        @ahk.set_timer(countdown=0.1)
        def win1():
            ahk.message_box("win1", title="win1")

        @ahk.set_timer(countdown=0.2)
        def win2():
            ahk.message_box("win2", title="win2")

        ahk.sleep(1)
        sys.exit()

    child_ahk.popen_code(windows)

    assert repr(ahk.windows) == "Windows()"
    msg_boxes = ahk.windows.filter(exe="AutoHotkey.exe")
    assert repr(msg_boxes) == "Windows(exe='AutoHotkey.exe')"
    assert msg_boxes.wait(timeout=1) is True
    assert len(msg_boxes) == 2
    ahk_window_list = list(msg_boxes)
    assert ahk_window_list != []
    top = msg_boxes.first()
    assert ahk_window_list[0] == top
    assert ahk_window_list[-1] == msg_boxes.last()
    assert repr(top) == f"Window(id={top.id})"

    assert len(msg_boxes.filter(title="win2")) == 1
    assert msg_boxes.filter(title="win2").first().title == "win2"
    assert len(msg_boxes.exclude(title="win2")) == 1
    assert msg_boxes.exclude(title="win2").first().title == "win1"

    assert all(not mb.minimized and not mb.maximized for mb in msg_boxes)
    msg_boxes.minimize_all()
    assert all(mb.minimized for mb in msg_boxes)
    msg_boxes.maximize_all()
    assert all(mb.maximized for mb in msg_boxes)
    msg_boxes.restore_all()
    assert all(not mb.minimized and not mb.maximized for mb in msg_boxes)

    ahk.windows.close_all(exe="AutoHotkey.exe")
    assert ahk.windows.first(exe="AutoHotkey.exe") is None

    ahk.send("{F24}")