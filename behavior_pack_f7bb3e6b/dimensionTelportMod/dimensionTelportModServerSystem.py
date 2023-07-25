# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
ServerSystem = serverApi.GetServerSystemCls()
Factory = serverApi.GetEngineCompFactory()


class dimensionTelportModServerSystem(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.ListenEvent()
        self.playerPointDict = {}
        print("加载监听ing")
        print("加载监听ok")

    def ListenEvent(self):
        #获取levelId
        self.levelId = serverApi.GetLevelId()
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'ServerBlockUseEvent', self, self.OnServerBlockUseEvent)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'AddServerPlayerEvent', self, self.OnAddServerPlayerEvent)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'DimensionChangeServerEvent', self, self.OnDimensionChangeServerEvent)   
        print("ListenEvent,OK")

    def OnAddServerPlayerEvent(self, args):
        playerId = args["id"]

        #读取数据看看有没有数据在，否则默认
        compByCreateExtraData = Factory.CreateExtraData(playerId)
        playerPos = compByCreateExtraData.GetExtraData(playerId)
        print("我的pos：")
        print(playerPos)

        if playerPos != None:
            self.playerPointDict[playerId] = playerPos
            return

        #0 玩家主世界坐标
        #1 玩家地狱坐标
        #2 玩家末地坐标
        self.playerPointDict[playerId] = [(0,128,0),(0,64,0),(0,128,0)]
        compByCreateGame = Factory.CreateGame(self.levelId)
        compByCreateGame.NotifyOneMessage(playerId, "你已加载维度传送石模组，第一次传送时可能会发生卡墙（记得开保留物品栏），属于正常现象，第二次就没事了", "§7")

    def OnDimensionChangeServerEvent(self, args):
        playerId = args["playerId"]
        print("OnDimensionChangeServerEvent")
        print(args["fromDimensionId"])
        if args["fromDimensionId"] == 0:
            #玩家传送坐标字典改主世界传送前坐标
            self.playerPointDict[playerId][0] = (args["fromX"],args["fromY"],args["fromZ"])
        elif args["fromDimensionId"] == 1:
            #玩家传送坐标字典改地狱传送前坐标
            self.playerPointDict[playerId][1] = (args["fromX"],args["fromY"],args["fromZ"])
        elif args["fromDimensionId"] == 2:
            #玩家传送坐标字典改末地传送前坐标
            self.playerPointDict[playerId][2] = (args["fromX"],args["fromY"],args["fromZ"])

        #保存数据
        entitycompByCreateExtraData = Factory.CreateExtraData(playerId)
        entitycompByCreateExtraData.SetExtraData(playerId, self.playerPointDict[playerId])
        entitycompByCreateExtraData.SaveExtraData()

    def OnServerBlockUseEvent(self, args):
        playerId = args["playerId"]
        print("OnServerBlockUseEvent ok")
        print(self.playerPointDict[playerId])
        compByCreateBlockUseEventWhiteList = Factory.CreateBlockUseEventWhiteList(self.levelId)
        compByCreateBlockUseEventWhiteList.AddBlockItemListenForUseEvent("qiemm:dimension_block:0")

        compByCreateItem = Factory.CreateItem(playerId)
        playerBagDict = compByCreateItem.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
        print(playerBagDict["newItemName"])

        #主世界
        if playerBagDict["newItemName"] == "qiemm:main_stone":      
            compByCreateDimension = Factory.CreateDimension(playerId)
            compByCreateDimension.ChangePlayerDimension(0, self.playerPointDict[playerId][0])
        #地狱
        elif playerBagDict["newItemName"] == "qiemm:hell_stone":
            compByCreateDimension = Factory.CreateDimension(playerId)
            compByCreateDimension.ChangePlayerDimension(1, self.playerPointDict[playerId][1])
        #末地
        elif playerBagDict["newItemName"] == "qiemm:ender_stone":
            compByCreateDimension = Factory.CreateDimension(playerId)
            compByCreateDimension.ChangePlayerDimension(2, self.playerPointDict[playerId][2])

    def UnListenEvent(self):
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'ServerBlockUseEvent', self, self.OnServerBlockUseEvent)
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'AddServerPlayerEvent', self, self.OnAddServerPlayerEvent)
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'DimensionChangeServerEvent', self, self.OnDimensionChangeServerEvent)   

    def Destroy(self):
        self.UnListenEvent()
