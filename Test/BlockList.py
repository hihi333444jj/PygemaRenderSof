from HelperScripts.Manage.Scene import *
import HelperScripts.Create_Shape as shape
BlockArrya = ["dirt","grass","air","Wire_TB_Off","Wire_LR_Off","Wire_BR_Off","Wire_BL_Off","Wire_TR_Off","Wire_TL_Off","PowerBlock"]
TS = 100 # TileSize
LT = 25 #Wire Thicknes
TSD2 = TS/2
LTD2 = LT/2
LTSD2 = TSD2-LTD2
def PlaceBlock(x,y,block):
    global TS,LT,TSD2,LTD2
    OffWireColor = (175,0,0)
    OnWireColor = (255,0,0)
    XPos,YPos = x*TS,y*TS
    XPos2,YPos2 = XPos+LTSD2,YPos+LTSD2
    # region Off wires
    if block == "Wire_TB_Off":
        AddObject([
            Group(
                shape.Rect(XPos, YPos, TS, TS, (0,0,0)),
                shape.Rect(XPos+LTSD2, YPos, LT, TS, OffWireColor)
            )
            , f"Block{x},{y}"])
    elif block == "Wire_LR_Off":
        AddObject([
            Group(
                shape.Rect(XPos, YPos, TS, TS, (0,0,0)),
                shape.Rect(XPos, YPos+LTSD2, TS, LT, OffWireColor)
            )
            , f"Block{x},{y}"])
    elif block == "Wire_BR_Off":
        AddObject([
            Group(
                shape.Rect(XPos, YPos, TS, TS, (0,0,0)),
                shape.Rect(XPos2, YPos2, TSD2+LTD2, LT, OffWireColor),
                shape.Rect(XPos2, YPos2, LT, TSD2+LTD2, OffWireColor)
            )
            , f"Block{x},{y}"])
    elif block == "Wire_BL_Off":
        AddObject([
            Group(
                shape.Rect(XPos, YPos, TS, TS, (0,0,0)),
                shape.Rect(XPos, YPos2, TSD2+LTD2, LT, OffWireColor),
                shape.Rect(XPos2, YPos2, LT, TSD2+LTD2, OffWireColor)
            )
            , f"Block{x},{y}"])
    elif block == "Wire_TR_Off":
        AddObject([
            Group(
                shape.Rect(XPos, YPos, TS, TS, (0,0,0)),
                shape.Rect(XPos2, YPos2, TSD2+LTD2, LT, OffWireColor),
                shape.Rect(XPos2, YPos, LT, TSD2+LTD2, OffWireColor)
            )
            , f"Block{x},{y}"])
    elif block == "Wire_TL_Off":
        AddObject([
            Group(
                shape.Rect(XPos, YPos, TS, TS, (0,0,0)),
                shape.Rect(XPos, YPos2, TSD2+LTD2, LT, OffWireColor),
                shape.Rect(XPos2, YPos, LT, TSD2+LTD2, OffWireColor)
            )
            , f"Block{x},{y}"])
    # endregion
    
    # region On wires
    elif block == "Wire_TB_On":
        AddObject([
            Group(
                shape.Rect(XPos, YPos, TS, TS, (0,0,0)),
                shape.Rect(XPos+LTSD2, YPos, LT, TS, OnWireColor)
            )
            , f"Block{x},{y}"])
    elif block == "Wire_LR_On":
        AddObject([
            Group(
                shape.Rect(XPos, YPos, TS, TS, (0,0,0)),
                shape.Rect(XPos, YPos+LTSD2, TS, LT, OnWireColor)
            )
            , f"Block{x},{y}"])
    elif block == "Wire_BR_On":
        AddObject([
            Group(
                shape.Rect(XPos, YPos, TS, TS, (0,0,0)),
                shape.Rect(XPos2, YPos2, TSD2+LTD2, LT, OnWireColor),
                shape.Rect(XPos2, YPos2, LT, TSD2+LTD2, OnWireColor)
            )
            , f"Block{x},{y}"])
    elif block == "Wire_BL_On":
        AddObject([
            Group(
                shape.Rect(XPos, YPos, TS, TS, (0,0,0)),
                shape.Rect(XPos, YPos2, TSD2+LTD2, LT, OnWireColor),
                shape.Rect(XPos2, YPos2, LT, TSD2+LTD2, OnWireColor)
            )
            , f"Block{x},{y}"])
    elif block == "Wire_TR_On":
        AddObject([
            Group(
                shape.Rect(XPos, YPos, TS, TS, (0,0,0)),
                shape.Rect(XPos2, YPos2, TSD2+LTD2, LT, OnWireColor),
                shape.Rect(XPos2, YPos, LT, TSD2+LTD2, OnWireColor)
            )
            , f"Block{x},{y}"])
    elif block == "Wire_TL_On":
        AddObject([
            Group(
                shape.Rect(XPos, YPos, TS, TS, (0,0,0)),
                shape.Rect(XPos, YPos2, TSD2+LTD2, LT, OnWireColor),
                shape.Rect(XPos2, YPos, LT, TSD2+LTD2, OnWireColor)
            )
            , f"Block{x},{y}"])
    # endregion
    
    
    #solid color blocks
    else:
        Color = (135, 206, 235)
        if block == "grass":
            Color = (0, 200, 0)
        elif block == "dirt":
            Color = (139, 69, 19)
        elif block == "PowerBlock":
            Color = (255, 0, 0)
        AddObject([shape.Rect(
            x*TS, y*TS, TS,TS, Color
            ), f"Block{x},{y}"])
