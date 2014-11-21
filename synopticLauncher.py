__author__ = 'andrew.willis'

#SYNOPTIC LAUNCHER

import maya.cmds as cmds
import os, imp, asiist

#windows root
winRoot = os.environ['ProgramFiles'][:2]+'/'

#determining root path
rootPath = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')

#fetch data from projInfo
enviFetch=asiist.getEnvi()
for chk in enviFetch:
    if chk[0] == 'projName': curProj = chk[1]
    if chk[0] == 'resWidth': resWidth = chk[1]
    if chk[0] == 'resHeight': resHeight = chk[1]
    if chk[0] == 'playblastCodec': codec = chk[1]
    if chk[0] == 'playblastFormat': playblastFormat = chk[1]

class synopticLauncherCLS:
    def __init__(self):
        global SCRIPTlis, PROJECTtxt
        if cmds.window('synopticLauncher',exists=True): cmds.deleteUI('synopticLauncher',wnd=True)

        cmds.window('synopticLauncher',t='Synoptic Launcher',s=False,w=200)
        cmas=cmds.columnLayout(adj=True,w=200)

        f2=cmds.frameLayout(l='Synoptic',p=cmas)
        SCRIPTlis=cmds.textScrollList(w=200,h=300,dcc=self.RUNSYNfn)
        cmds.popupMenu(p=SCRIPTlis)
        cmds.menuItem(l='Run Synoptic',c=self.RUNSYNfn)
        cmds.menuItem(l='Delete Synoptic',c=self.DELETEfn)
        cmds.menuItem(divider=True)
        cmds.menuItem(l='Refresh',c=self.REFRESHfn)

        cmds.showWindow()

        self.REFRESHfn()
        return

    def DELETEfn(self,*args):
        global SCRIPTlis, PROJECTtxt
        REPvar=cmds.confirmDialog(icn='question',\
                               t='Delete',\
                               m='Are you sure you want to delete this synoptic?',\
                               button=['Yes','No'])
        if REPvar=='No':
            cmds.error('error : cancelled by user')

        SELvar=cmds.textScrollList(SCRIPTlis,q=True,si=True)
        if SELvar==None:
            cmds.confirmDialog(icn='warning',\
                               t='Error',\
                               m='No item selected from list.',\
                               button=['Ok'])
            cmds.error('error : no item selected from list')
        else:
            SELvar=SELvar[0]
        os.remove(rootPath+'/synopticLibrary/'+curProj+'/'+SELvar+'.pyc')
        self.REFRESHfn()
        return

    def RUNSYNfn(self,*args):
        global SCRIPTlis, PROJECTtxt
        SELvar=cmds.textScrollList(SCRIPTlis,q=True,si=True)
        if SELvar==None:
            cmds.confirmDialog(icn='warning',\
                               t='Error',\
                               m='No item selected from list.',\
                               button=['Ok'])
            cmds.error('error : no item selected from list')
        else:
            SELvar=SELvar[0]
        try:
            imp.load_compiled(SELvar,rootPath+'/synopticLibrary/'+curProj+'/'+SELvar+'.pyc')
        except Exception as e:
            cmds.confirmDialog(icn='warning',\
                               t='Error',\
                               m='Error running synoptic script\n'+str(e),\
                               button=['Ok'])
            cmds.error('error : no item selected from list')
        return

    def REFRESHfn(self,*args):
        global SCRIPTlis, PROJECTtxt
        SYNlis=os.listdir(rootPath+'/synopticLibrary/'+curProj)

        cmds.textScrollList(SCRIPTlis,e=True,ra=True)

        for chk in SYNlis:cmds.textScrollList(SCRIPTlis,e=True,a=chk.replace('.pyc',''))
        return


synopticLauncherCLS()