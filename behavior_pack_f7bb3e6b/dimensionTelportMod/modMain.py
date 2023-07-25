# -*- coding: utf-8 -*-

from mod.common.mod import Mod
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi


@Mod.Binding(name="dimensionTelportMod", version="0.0.1")
class dimensionTelportMod(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def dimensionTelportModServerInit(self):
        serverApi.RegisterSystem("dimensionTelportMod","dimensionTelportModServerSystem","dimensionTelportMod.dimensionTelportModServerSystem.dimensionTelportModServerSystem")
        print("===服务端注册完毕===")

    @Mod.DestroyServer()
    def dimensionTelportModServerDestroy(self):
        print("===服务端销毁完毕===")

    @Mod.InitClient()
    def dimensionTelportModClientInit(self):
        clientApi.RegisterSystem("dimensionTelportMod","dimensionTelportModClientSystem","dimensionTelportMod.dimensionTelportModClientSystem.dimensionTelportModClientSystem")
        print("===客户端注册完毕===")

    @Mod.DestroyClient()
    def dimensionTelportModClientDestroy(self):
        print("===客户端销毁完毕===")
