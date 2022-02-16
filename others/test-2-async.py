import asyncio
import tkinter as tk


class TkAsyncWindow(tk.Tk):
    def __init__(self, loop, update_interval=1 / 20):
        super(TkAsyncWindow, self).__init__()
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.geometry('400x100')
        self.loop = loop
        self.tasks = []

        self.status = 'working'
        self.status_label = tk.Label(self, text=self.status)
        self.status_label.pack(padx=10, pady=10)

        self.after(0, self.__update_asyncio, update_interval)
        self.close_event = asyncio.Event()

    def close(self):
        self.close_event.set()

    def __update_asyncio(self, interval):
        self.loop.call_soon(self.loop.stop)
        self.loop.run_forever()
        if self.close_event.is_set():
            self.quit()
        self.after(int(interval * 1000), self.__update_asyncio, interval)

    async def status_label_task(self):
        """
        This keeps the Status label updated with an alternating number of dots so that you know the UI isn't
        frozen even when it's not doing anything.
        """
        dots = ''
        while True:
            self.status_label['text'] = 'Status: %s%s' % (self.status, dots)
            await asyncio.sleep(0.5)
            dots += '.'
            if len(dots) >= 4:
                dots = ''

    def initialize(self):
        coros = (
            self.status_label_task(),
            # additional network-bound tasks
        )
        for coro in coros:
            self.tasks.append(self.loop.create_task(coro))


if __name__ == '__main__':
    gui = TkAsyncWindow(asyncio.get_event_loop())
    gui.initialize()
    gui.mainloop()
    gui.destroy()
