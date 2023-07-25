# -*- coding: utf-8 -*-

from mod.common.mod import Mod


@Mod.Binding(name="Script_NeteaseModAPM81lJk", version="0.0.1")
class Script_NeteaseModAPM81lJk(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def Script_NeteaseModAPM81lJkServerInit(self):
        pass

    @Mod.DestroyServer()
    def Script_NeteaseModAPM81lJkServerDestroy(self):
        pass

    @Mod.InitClient()
    def Script_NeteaseModAPM81lJkClientInit(self):
        pass

    @Mod.DestroyClient()
    def Script_NeteaseModAPM81lJkClientDestroy(self):
        pass
