# ### 1st Stop Repository Highway (2014) - By TheHighway ### #
# ########################################################## #

import xbmc,xbmcgui,urllib2,os,sys,logging,array,re,time,datetime,random,string,StringIO,xbmcplugin,xbmcaddon,shutil
from config import Config as Config
import common as Common
from common import *
import common
import downloader,extract ## Included Modules ##

try: from sqlite3 import dbapi2 as orm
except: from pysqlite2 import dbapi2 as orm
DB='sqlite'; DB_Located=''; yy=['20','19','18','17','16','15','14','13','12','11','10','9','8','7','6','5','4','3','2','1','']; 
for z in yy:
	if len(DB_Located)==0:
		testZ=os.path.join(xbmc.translatePath("special://database"),'Addons'+z+'.db')
		if    os.path.isfile(testZ)==True: print "Database Found: "+testZ;  DB_Located=testZ; 
if len(DB_Located)==0: print "Unable to locate Database"
def getITEMS(table='repo',where='',what='*',default=[]):
	if os.path.isfile(DB_Located)==True: 
		db=orm.connect(DB_Located); dbc=db.cursor(); 
		s='SELECT '+what+' FROM '+table+where; debob(s); 
		dbc.execute(s); 
		r=dbc.fetchall()
		db.close(); 
		#debob(r); 
		return r
	return default
def getITEM(table='repo',where='',what='*',default=[]):
	if os.path.isfile(DB_Located)==True: 
		db=orm.connect(DB_Located); dbc=db.cursor(); 
		s='SELECT '+what+' FROM '+table+where; debob(s); 
		dbc.execute(s); 
		r=dbc.fetchone()
		db.close(); 
		return r
	return default

XBMCversion={}
XBMCversion['All']=xbmc.getInfoLabel("System.BuildVersion"); 
XBMCversion['Ver']=XBMCversion['All']; XBMCversion['Release']=''; XBMCversion['Date']=''; 
if ('Git:' in XBMCversion['All']) and ('-' in XBMCversion['All']): XBMCversion['Date']=XBMCversion['All'].split('Git:')[1].split('-')[0]
if ' ' in XBMCversion['Ver']: XBMCversion['Ver']=XBMCversion['Ver'].split(' ')[0]
if '-' in XBMCversion['Ver']: XBMCversion['Release']=XBMCversion['Ver'].split('-')[1]; XBMCversion['Ver']=XBMCversion['Ver'].split('-')[0]
deb('Version All',XBMCversion['All']); deb('Version Number',XBMCversion['Ver']); deb('Version Release Name',XBMCversion['Release']); deb('Version Date',XBMCversion['Date']); 

class MyWindow(xbmcgui.Window):
	#
	#
	InstallToPath=xbmc.validatePath(xbmc.translatePath(os.path.join("special://home","addons")))
	DownloadToPath=xbmc.validatePath(xbmc.translatePath(os.path.join("special://home","addons","packages")))
	DotOrgRepo_XML='http://mirrors.xbmc.org/addons/frodo/addons.xml'
	DotOrgRepo_XMLInfoCompressed=True
	DotOrgRepo_Checksum='http://mirrors.xbmc.org/addons/frodo/addons.xml.md5'
	DotOrgRepo_DataDirPath='http://mirrors.xbmc.org/addons/frodo'
	DotOrgRepo_DataDirZIP=True
	##
	button={}
	def __init__(self):
		self.background=(xbmc.translatePath(Config.fanart)); self.background=artp("XBMCHUB_D5T"); 
		self.backgroundB=artp("XBMCHUB_D5T"); self.b1=artp("black1"); 
		#deb("BG",self.background)
		self.show_graphics_behind_list=tfalse(SettingG('show_graphics_behind_list'))
		self.BGB=xbmcgui.ControlImage(0,0,1280,720,self.b1,aspectRatio=0); self.addControl(self.BGB)
		self.TVSBGB=xbmcgui.ControlImage(800,12,280,190,self.b1,aspectRatio=0); self.addControl(self.TVSBGB)
		self.TVS=xbmcgui.ControlImage(800,12,280,190,self.b1,aspectRatio=0); self.addControl(self.TVS)
		self.TVSBGB.setAnimations([('WindowOpen','effect=rotatey time=0 end=10 center=1040,120')])
		self.TVS.setAnimations([('WindowOpen','effect=rotatey time=0 end=10 center=1040,120')])
		self.BG=xbmcgui.ControlImage(0,0,1280,720,self.backgroundB,aspectRatio=0); self.addControl(self.BG)
		focus=artp("button-focus2"); nofocus=artp("button-nofocus"); 
		self.RepoFanart2=xbmcgui.ControlImage(30,120,400,520,self.b1,aspectRatio=0); self.addControl(self.RepoFanart2); 
		self.RepoFanart=xbmcgui.ControlImage(30,120,330,460,self.b1,aspectRatio=0); self.addControl(self.RepoFanart); 
		self.RepoThumbnail=xbmcgui.ControlImage(330,120,100,100,self.b1,aspectRatio=0); self.addControl(self.RepoThumbnail); 
		##
		self.LabTitle=xbmcgui.ControlLabel(30,20,1000,50,'','font30','0xFFFF0000'); self.addControl(self.LabTitle)
		self.LabTitleText=Config.name
		zz=["XBMCHUB","Your","1st Stop"]
		for z in zz:
			if z+" " in self.LabTitleText: self.LabTitleText=self.LabTitleText.replace(z+" ","[COLOR deepskyblue][B][I]"+z+"[/I][/B][/COLOR]  ")
		if "Highway" in self.LabTitleText: self.LabTitleText=self.LabTitleText.replace("Highway","[COLOR tan]Highway[/COLOR]")
		self.LabTitle.setLabel(self.LabTitleText)
		#time.sleep(2); 
		self.CtrlList=xbmcgui.ControlList(30,120,400,500,font='font12',textColor="0xFFFF0000",selectedColor="0xFF00FF00",buttonFocusTexture=focus,buttonTexture=nofocus); self.CtrlList.setSpace(2); self.addControl(self.CtrlList); 
		self.CtrlList.setImageDimensions(100,100)
		#self.CtrlList.setItemHeight(100)
		#self.CtrlList.setItemWidth(100)
		#self.CtrlList.
		zz=[self.CtrlList,self.RepoFanart2,self.RepoFanart,self.RepoThumbnail]
		for z in zz: z.setAnimations([('WindowOpen','effect=slide delay=1000 time=1000 start=-500')])
		##
		self.LabCurrentRepo=xbmcgui.ControlLabel(180,80,220,30,'','font12','0xFF00BFFF',alignment=1); self.addControl(self.LabCurrentRepo)
		self.button[0]=xbmcgui.ControlButton(30, 70, 135, 30, "Exit",textColor="0xFFB22222",focusedColor="0xFF00BFFF",alignment=2,focusTexture=focus,noFocusTexture=nofocus); self.addControl(self.button[0])
		self.button[0].controlDown(self.CtrlList); self.button[0].controlUp(self.CtrlList); 
		self.CtrlList.controlDown(self.button[0]); self.CtrlList.controlUp(self.button[0]); 
		self.CtrlList.controlLeft(self.button[0]); self.CtrlList.controlRight(self.button[0]); 
		##
		self.ItemsA=getITEMS(table='addon',where=' WHERE addonID NOT IN (SELECT addonID FROM disabled)',what='addonID'); #debob(self.ItemsA); 
		self.ItemsR=getITEMS(table='repo',where=' WHERE addonID NOT IN (SELECT addonID FROM disabled)',what='addonID'); #debob(self.ItemsR); 
		##
		#Items=getITEMS(table='repo',where=' WHERE addonID NOT IN (SELECT addonID FROM disabled)'); debob(Items); 
		if tfalse(SettingG('show_disabled'))==True: Items=getITEMS(table='repo',where=''); debob('Displaying Enabled and Disabled Addons.'); 
		else: Items=getITEMS(table='repo',where=' WHERE addonID NOT IN (SELECT addonID FROM disabled)'); debob('Displaying Enabled Addons.'); 
		debob(Items); 
		try: Items=sorted(Items, key=lambda item: item[1], reverse=False); 
		except: pass
		self.RepoListData=[]; 
		try: self.parseRepositories(Items); 
		except: pass
		##
		if tfalse(SettingG('show_repo_thehighway'))==True: 
			if "repository.thehighway" not in self.CurRepoListings: self.AddRepo(RepoID="repository.thehighway",RepoName="TheHighway's Repository",RepoVersion="0.0.4",RepoNumber="",RepoLastCheck="",RepoChecksum="",RepoSummary="",RepoDescription="",RepoDisclaimer="",RepoAuthor="The[COLOR tan]Highway[/COLOR]",InstalledPath="special://home",RepoURL="http://raw.github.com/HIGHWAY99/repository.thehighway/master/addons.xml",RepoURLMD5="http://raw.github.com/HIGHWAY99/repository.thehighway/master/addons.xml.md5",RepoURLPath="http://raw.github.com/HIGHWAY99/repository.thehighway/master/repo/")
		if tfalse(SettingG('show_repo_xbmchub'))==True: 
			if "repository.xbmchub" not in self.CurRepoListings: self.AddRepo(RepoID="repository.xbmchub",RepoName="XBMCHUB.com's Repository",RepoVersion="1.0.2",RepoNumber="",RepoLastCheck="",RepoChecksum="",RepoSummary="",RepoDescription="",RepoDisclaimer="",RepoAuthor="",InstalledPath="special://home",RepoURL="http://xbmc-hub-repo.googlecode.com/svn/addons/addons.xml",RepoURLMD5="http://xbmc-hub-repo.googlecode.com/svn/addons/addons.xml.md5",RepoURLPath="http://xbmc-hub-repo.googlecode.com/svn/addons")
		if tfalse(SettingG('show_repo_superrepo'))==True: 
			if "repository.superrepo.org.gotham.all" not in self.CurRepoListings: self.AddRepo(RepoID="repository.superrepo.org.gotham.all",RepoName="SuperRepo.org Repository - All (Gotham)",RepoVersion="0.5.1",RepoNumber="",RepoLastCheck="",RepoChecksum="",RepoSummary="",RepoDescription="",RepoDisclaimer="",RepoAuthor="Bart Otten",InstalledPath="special://home",RepoURL="http://mirrors.superrepo.org/addons/gotham/.xml/all/addons.xml",RepoURLMD5="http://mirrors.superrepo.org/addons/gotham/.xml/all/addons.xml.md5",RepoURLPath="http://mirrors.superrepo.org/addons/gotham/")
			if "repository.superrepo.org.frodo.all" not in self.CurRepoListings: self.AddRepo(RepoID="repository.superrepo.org.frodo.all",RepoName="SuperRepo.org Repository - All (Frodo)",RepoVersion="0.5.1",RepoNumber="",RepoLastCheck="",RepoChecksum="",RepoSummary="",RepoDescription="",RepoDisclaimer="",RepoAuthor="Bart Otten",InstalledPath="special://home",RepoURL="http://mirrors.superrepo.org/addons/frodo/.xml/all/addons.xml",RepoURLMD5="http://mirrors.superrepo.org/addons/frodo/.xml/all/addons.xml.md5",RepoURLPath="http://mirrors.superrepo.org/addons/frodo/")
		if tfalse(SettingG('show_repo_xbmc'))==True: 
			#if "repository.xbmc.org" not in self.CurRepoListings: 
			self.AddRepo(RepoID="repository.xbmc.org",RepoName="XBMC.org Add-ons (Eden)",RepoVersion="0.0.1",RepoNumber="",RepoLastCheck="",RepoChecksum="",RepoSummary="",RepoDescription="",RepoDisclaimer="",RepoAuthor="Team XBMC",InstalledPath="special://home",RepoURL="http://mirrors.xbmc.org/addons/eden/addons.xml",RepoURLMD5="http://mirrors.xbmc.org/addons/eden/addons.xml.md5",RepoURLPath="http://mirrors.xbmc.org/addons/eden")
			self.AddRepo(RepoID="repository.xbmc.org",RepoName="XBMC.org Add-ons (Frodo)",RepoVersion="2.0.10",RepoNumber="",RepoLastCheck="",RepoChecksum="",RepoSummary="",RepoDescription="",RepoDisclaimer="",RepoAuthor="Team XBMC",InstalledPath="special://home",RepoURL="http://mirrors.xbmc.org/addons/frodo/addons.xml",RepoURLMD5="http://mirrors.xbmc.org/addons/frodo/addons.xml.md5",RepoURLPath="http://mirrors.xbmc.org/addons/frodo")
			self.AddRepo(RepoID="repository.xbmc.org",RepoName="XBMC.org Add-ons (Gotham)",RepoVersion="0.0.1",RepoNumber="",RepoLastCheck="",RepoChecksum="",RepoSummary="",RepoDescription="",RepoDisclaimer="",RepoAuthor="Team XBMC",InstalledPath="special://home",RepoURL="http://mirrors.xbmc.org/addons/gotham/addons.xml",RepoURLMD5="http://mirrors.xbmc.org/addons/gotham/addons.xml.md5",RepoURLPath="http://mirrors.xbmc.org/addons/gotham")
		if tfalse(SettingG('show_repo_divingmule'))==True: 
			if "repository.divingmule.addons" not in self.CurRepoListings: self.AddRepo(RepoID="repository.divingmule.addons",RepoName="divingmule's Unofficial Repository",RepoVersion="1.0.0",RepoNumber="",RepoLastCheck="",RepoChecksum="",RepoSummary="",RepoDescription="",RepoDisclaimer="",RepoAuthor="divingmule",InstalledPath="special://home",RepoURL="http://divingmules-repo.googlecode.com/svn/trunk/addons.xml",RepoURLMD5="http://divingmules-repo.googlecode.com/svn/trunk/addons.xml.md5",RepoURLPath="http://divingmules-repo.googlecode.com/svn/trunk/")
		if tfalse(SettingG('show_repo_coremodule_betas'))==True: 
			if "repository.coremodule.betas" not in self.CurRepoListings: self.AddRepo(RepoID="repository.coremodule.betas",RepoName="Core Module Beta Testing Repo",RepoVersion="1.0.0",RepoNumber="",RepoLastCheck="",RepoChecksum="",RepoSummary="",RepoDescription="",RepoDisclaimer="",RepoAuthor="eldorado",InstalledPath="special://home",RepoURL="http://raw.github.com/Eldorados/Core-Module-Beta-Repo/master/addons.xml",RepoURLMD5="http://raw.github.com/Eldorados/Core-Module-Beta-Repo/master/addons.xml.md5",RepoURLPath="http://raw.github.com/Eldorados/Core-Module-Beta-Repo/master/repo/")
		if tfalse(SettingG('show_repo_eldorado'))==True: 
			if "repository.eldorado" not in self.CurRepoListings: self.AddRepo(RepoID="repository.eldorado",RepoName="Eldorado's XBMC Addons",RepoVersion="1.0.2",RepoNumber="",RepoLastCheck="",RepoChecksum="",RepoSummary="",RepoDescription="",RepoDisclaimer="",RepoAuthor="eldorado",InstalledPath="special://home",RepoURL="http://raw.github.com/Eldorados/eldorado-xbmc-addons/master/addons.xml",RepoURLMD5="http://raw.github.com/Eldorados/eldorado-xbmc-addons/master/addons.xml.md5",RepoURLPath="http://raw.github.com/Eldorados/eldorado-xbmc-addons/master/repo/")
		#self.AddRepo(RepoID="",RepoName="",RepoVersion="",RepoNumber="",RepoLastCheck="",RepoChecksum="",RepoSummary="",RepoDescription="",RepoDisclaimer="",RepoAuthor="",InstalledPath="special://home",RepoURL="",RepoURLMD5="",RepoURLPath="")
		#self.AddRepo(RepoID="",RepoName="",RepoVersion="",RepoNumber="",RepoLastCheck="",RepoChecksum="",RepoSummary="",RepoDescription="",RepoDisclaimer="",RepoAuthor="",InstalledPath="special://home",RepoURL="",RepoURLMD5="",RepoURLPath="")
		
		self.setFocus(self.button[0])
		##
		#self.DotOrgREPO=getURL(self.DotOrgRepo_XML)
		#if len(self.DotOrgREPO) > 0: self.DotOrgREPO_Addons=re.compile('<addon\s+(.+?)>(.+?)</addon',re.IGNORECASE).findall(self.DotOrgREPO)
		#else: self.DotOrgREPO=[]
		##
	def parseRepositories(self,Items):
		self.CtrlList.reset()
		self.CurRepoListings=[]
		for (i_id,i_addonID,i_checksumb,i_lastcheck) in Items:
			try: self.CurRepoListings.append(i_addonID)
			except: pass
			try:
				debob((i_id,i_addonID))
				addon_path="special://home"; addon_file=repo(i_addonID,"addon.xml")
				if os.path.isfile(addon_file)==False: addon_path="special://xbmc"; addon_file=repox(i_addonID,"addon.xml"); 
				if os.path.isfile(addon_file)==True:
					pleaseSkip=False
					try: addon_xml=nolines(Common._OpenFile(addon_file))
					except: addon_xml=''; pleaseSkip=True
					if len(addon_xml) > 0:
						#addon_xml_addon=addon_xml.split("<addon",re.IGNORECASE)[1].split(">")[0]
						try: addon_xml_addon=re.compile("<addon(.*?)>",re.IGNORECASE).findall(addon_xml)[0]
						except: addon_xml_addon=''; pleaseSkip=True
						try: addon_xml_addon_inner=re.compile("<addon.*?>(.*?)</addon>",re.IGNORECASE).findall(addon_xml)[0]
						except: addon_xml_addon_inner=''; pleaseSkip=True
						try: addon_xml_addon_name=re.compile('\s+name="(.*?)"',re.IGNORECASE).findall(addon_xml_addon)[0]
						except: pleaseSkip=True
						try: addon_xml_addon_version=re.compile('\s+version="(.*?)"',re.IGNORECASE).findall(addon_xml_addon)[0]
						except: pleaseSkip=True
						try: addon_xml_addon_author=re.compile('\s+provider-name="(.*?)"',re.IGNORECASE).findall(addon_xml_addon)[0]
						except:
							try: addon_xml_addon_author=re.compile("\s+provider-name='(.*?)'",re.IGNORECASE).findall(addon_xml_addon)[0]
							except: addon_xml_addon_author="[UNKNOWN]"
						try: addon_xml_addon_url=re.compile('<info.*?>(.*?)</info>',re.IGNORECASE).findall(' '+addon_xml_addon_inner)[0]
						except: pleaseSkip=True
						try: addon_xml_addon_urlmd5=re.compile('<checksum.*?>(.*?)</checksum>',re.IGNORECASE).findall(addon_xml_addon_inner)[0]
						except: pleaseSkip=True
						try: addon_xml_addon_urlpath=re.compile('<datadir.*?>(.*?)</datadir>',re.IGNORECASE).findall(addon_xml_addon_inner)[0]
						except: pleaseSkip=True
						try: debob((i_addonID)); 
						except: pass
						try: debob((i_addonID,addon_xml_addon_url,addon_xml_addon_urlmd5,addon_xml_addon_urlpath))
						except: pass
						if pleaseSkip==False:
							self.RepoListData.append({'RepoID':str(i_addonID),'RepoName':str(addon_xml_addon_name),'RepoVersion':str(addon_xml_addon_version),'RepoNumber':str(i_id),'RepoLastCheck':str(i_lastcheck),'RepoChecksum':str(i_checksumb),'RepoSummary':"",'RepoDescription':"",'RepoDisclaimer':"",'RepoAuthor':str(addon_xml_addon_author),'InstalledPath':addon_path,'RepoURL':addon_xml_addon_url,'RepoURLMD5':addon_xml_addon_urlmd5,'RepoURLPath':addon_xml_addon_urlpath})
							self.AddRepo(RepoID=str(i_addonID),RepoName=str(addon_xml_addon_name),RepoVersion=str(addon_xml_addon_version),RepoNumber=str(i_id),RepoLastCheck=str(i_lastcheck),RepoChecksum=str(i_checksumb),RepoSummary="",RepoDescription="",RepoDisclaimer="",RepoAuthor=str(addon_xml_addon_author),InstalledPath=addon_path,RepoURL=addon_xml_addon_url,RepoURLMD5=addon_xml_addon_urlmd5,RepoURLPath=addon_xml_addon_urlpath)
						#self.AddRepo(RepoID=str(i_addonID),RepoName=str(i_addonID),RepoVersion="0.0.4",RepoNumber=str(i_id),RepoLastCheck=str(i_lastcheck),RepoChecksum=str(i_checksumb))
				##
			except: pass
			##
		##
		
	def AddRepo(self,RepoID="",RepoName="",RepoVersion="",RepoNumber="",RepoLastCheck="",RepoChecksum="",RepoSummary="",RepoDescription="",RepoDisclaimer="",RepoAuthor="",InstalledPath="special://home",RepoURL="",RepoURLMD5="",RepoURLPath=""):
		r1=repo(RepoID,"icon.png",h=InstalledPath)
		r2=repo(RepoID,"fanart.jpg",h=InstalledPath)
		if tfalse(SettingG('repofix_github'))==True:
			if ("http://github.com/" in RepoURLPath) and ("/raw/" in RepoURLPath): RepoURLPath=RepoURLPath.replace("/raw/","").replace("http://github.com/","http://raw.github.com/")
			if ("http://www.github.com/" in RepoURLPath) and ("/raw/" in RepoURLPath): RepoURLPath=RepoURLPath.replace("/raw/","").replace("http://www.github.com/","http://raw.github.com/")
		#deb("icon",r1)
		c1=xbmcgui.ListItem(RepoName,RepoVersion,iconImage=r1,thumbnailImage=r1)
		c1.setProperty("repository.id",RepoID)
		c1.setProperty("repository.number",RepoNumber)
		c1.setProperty("repository.lastcheck",RepoLastCheck)
		c1.setProperty("repository.checksum",RepoChecksum)
		c1.setProperty("repository.icon",r1)
		c1.setProperty("repository.fanart",r2)
		c1.setProperty("repository.summary",RepoSummary)
		c1.setProperty("repository.description",RepoDescription)
		c1.setProperty("repository.disclaimer",RepoDisclaimer)
		c1.setProperty("repository.version",RepoVersion)
		c1.setProperty("repository.name",RepoName)
		c1.setProperty("repository.author",RepoAuthor)
		c1.setProperty("repository.installedpath",InstalledPath)
		c1.setProperty("repository.url",RepoURL)
		c1.setProperty("repository.urlmd5",RepoURLMD5)
		c1.setProperty("repository.urlpath",RepoURLPath)
		c1.setProperty("repository.category","")
		self.CtrlList.addItem(c1)
		
	def AddRepoCat(self,RepoID="",RepoName="",RepoVersion="",RepoCategory="",RepoSummary="",RepoDescription="",RepoDisclaimer="",RepoAuthor="",InstalledPath="special://home"):
		r1=repo(RepoID,"icon.png",h=InstalledPath)
		r2=repo(RepoID,"fanart.jpg",h=InstalledPath)
		#deb("icon",r1)
		c1=xbmcgui.ListItem(RepoCategory,"",iconImage=r1,thumbnailImage=r1)
		c1.setProperty("repository.id",RepoID)
		c1.setProperty("repository.icon",r1)
		c1.setProperty("repository.fanart",r2)
		c1.setProperty("repository.summary",RepoSummary)
		c1.setProperty("repository.description",RepoDescription)
		c1.setProperty("repository.disclaimer",RepoDisclaimer)
		c1.setProperty("repository.version",RepoVersion)
		c1.setProperty("repository.name",RepoName)
		c1.setProperty("repository.category","")
		#cMI=[]; 
		#cMI.append(( 'Show Info','XBMC.Action(Info)' ))
		#c1.addContextMenuItems(cMI)
		
		self.RepoCatList.addItem(c1)
		##
	def FillInRepoCatList(self,SelectedRepo):
		#SelectedRepo.getProperty("repository.icon")
		RepoID=SelectedRepo.getProperty("repository.id")
		RepoName=SelectedRepo.getProperty("repository.name")
		RepoVersion=SelectedRepo.getProperty("repository.version")
		RepoURL=SelectedRepo.getProperty("repository.url")
		RepoURLMD5=SelectedRepo.getProperty("repository.urlmd5")
		RepoURLPath=SelectedRepo.getProperty("repository.urlpath")
		self.LabCurrentRepo.setLabel(RepoName)
		self.RepoCatList.reset()
		RepoDATA=getURL(RepoURL)
		#AddRepoCat(RepoID,RepoName,RepoVersion,"")
		setContent("repositories"); 
		
		zz=["Video Addons","Music Addons","Program Addons",str(len(RepoDATA))]
		for z in zz:
			self.AddRepoCat(RepoID,RepoName,RepoVersion,z)
		
		self.setFocus(self.RepoCatList)
	def onAction(self,action):
		#non Display Button control
		if   action == Config.ACTION_PREVIOUS_MENU: self.CloseWindow1st()
		elif action == Config.ACTION_NAV_BACK: self.CloseWindow1st()
		try:
			#try: 
			rpI=str(self.CtrlList.getSelectedItem().getProperty("repository.icon"))
			rpF=str(self.CtrlList.getSelectedItem().getProperty("repository.fanart"))
			if (len(rpI) > 0) and (os.path.isfile(rpI)==True):
					if self.show_graphics_behind_list==True: self.RepoThumbnail.setImage(rpI); self.RepoThumbnail.setVisible(True)
					else: self.TVS.setImage(rpI); self.TVS.setVisible(True)
			#elif (len(rpI) > 0):
			#		self.RepoThumbnail.setImage(rpI); self.RepoThumbnail.setVisible(True)
			else: self.TVS.setImage(self.b1); self.RepoThumbnail.setImage(self.b1); self.RepoThumbnail.setVisible(False)
			if (len(rpF) > 0) and (os.path.isfile(rpF)==True):
					if self.show_graphics_behind_list==True: self.RepoFanart.setImage(rpF); self.RepoFanart.setVisible(True)
					else: self.BGB.setImage(rpF); self.BGB.setVisible(True)
					#self.LabTitle.setLabel(rpF)
			#elif (len(rpF) > 0):
			#		self.RepoFanart.setImage(rpF); self.RepoFanart.setVisible(True)
			else: self.BGB.setImage(self.b1); self.RepoFanart.setImage(self.b1); #self.RepoFanart.setVisible(False)
			#except: self.RepoThumbnail.setImage(self.background)
			#debob(self.CtrlList.getSelectedItem().getProperty("repository.icon"))
		except: pass
		try:
			addonI=str(self.AddonsList.getSelectedItem().getProperty("addon.icon"))
			#if (len(addonI) > 0) and (os.path.isfile(addonI)==True):
			if (len(addonI) > 0):
					self.AddonThumbnail.setImage(addonI); self.AddonThumbnail.setVisible(True)
			else: self.AddonThumbnail.setImage(self.b1); self.AddonThumbnail.setVisible(False)
			addonF=str(self.AddonsList.getSelectedItem().getProperty("addon.fanart"))
			if (len(addonF) > 0):
					self.AddonFanart.setImage(addonF); self.AddonFanart.setVisible(True)
					#self.LabTitle.setLabel(rpF)
			else: self.AddonFanart.setImage(self.b1); #self.RepoFanart.setVisible(False)
		except: pass
		#if addonI==addonI:
		try:
			addonFsi=self.AddonsList.getSelectedItem()
			#debob(addonFsi.getLabel())
			#debob(addonFsi.getProperty("addon.id"))
			try: self.AddonsId.setLabel("[COLOR mediumpurple]ID: [/COLOR]"+str(addonFsi.getProperty("addon.id")))
			except: self.AddonsId.setLabel('')
			aLatestVersion=str(addonFsi.getProperty("addon.version")); 
			try: self.AddonsVer.setLabel("[COLOR mediumpurple]ver: [/COLOR]"+aLatestVersion)
			except: self.AddonsVer.setLabel('')
			try: self.AddonsTitle.setLabel("[COLOR mediumpurple]Name: [/COLOR]"+str(addonFsi.getProperty("addon.name")))
			except: self.AddonsTitle.setLabel('')
			try: self.AddonsRepoName.setLabel("[COLOR mediumpurple]Repo: [/COLOR]"+str(addonFsi.getProperty("repository.name")))
			except: self.AddonsRepoName.setLabel('')
			try: self.AddonsAuthor.setLabel("[COLOR mediumpurple]Author(s): [/COLOR]"+str(addonFsi.getProperty("addon.provider-name")))
			except: self.AddonsAuthor.setLabel('')
			try: self.AddonsProvides.setLabel("[COLOR mediumpurple]Type: [/COLOR]"+str(addonFsi.getProperty("addon.provides")))
			except: self.AddonsProvides.setLabel('')
			try: self.AddonsSummary.setText("[COLOR mediumpurple]Summary: [/COLOR]"+str(addonFsi.getProperty("addon.summary")))
			except: self.AddonsSummary.setText('')
			try: self.AddonsDescription.setText("[COLOR mediumpurple]Description: [/COLOR]"+str(addonFsi.getProperty("addon.description")))
			except: self.AddonsDescription.setText('')
			try: self.AddonsRequirements.setText("[COLOR mediumpurple]Requires: [/COLOR][CR]"+str(addonFsi.getProperty("addon.requires").replace('addon=','').replace('version=','').replace('/>','>').replace(' <','<')))
			except: self.AddonsRequirements.setText('')
			try: 
				if len(str(addonFsi.getProperty("addon.language"))) > 0:
					self.AddonsLanguage.setLabel("[COLOR mediumpurple]Language: [/COLOR]"+str(addonFsi.getProperty("addon.language")))
				else: self.AddonsLanguage.setLabel('')
			except: self.AddonsLanguage.setLabel('')
			try: 
				if len(str(addonFsi.getProperty("addon.platform"))) > 0:
					self.AddonsPlatform.setLabel("[COLOR mediumpurple]Platform: [/COLOR]"+str(addonFsi.getProperty("addon.platform")))
				else: self.AddonsPlatform.setLabel('')
			except: self.AddonsPlatform.setLabel('')
			try: 
				if len(str(addonFsi.getProperty("addon.broken"))) > 0:
					self.AddonsBroken.setText("[COLOR mediumpurple]Broken: [/COLOR]"+str(addonFsi.getProperty("addon.broken")))
				else: self.AddonsBroken.setText('')
			except: self.AddonsBroken.setText('')
			##
			#addon.currentinstalledversion
			#addon.installed
			try: 
				if 'tru' in addonFsi.getProperty("addon.installed"):
					try: 		AciVerA=str(addonFsi.getProperty("addon.currentinstalledversion")); AciVer=' ['+AciVerA+']'
					except: AciVerA=''; AciVer=''
					#debob((AciVerA,aLatestVersion)); 
					#try: 
					AciE=str(addonFsi.getProperty("addon.ebabled")); 
					#except: AciE='false'
					deb('AciE',AciE); 
					if AciE=='true':
						if AciVerA==aLatestVersion:
							self.btnInstall.setLabel('['+AciVerA+']'); 
							self.btnInstall.setVisible(True); 
							self.btnInstall.setEnabled(False); 
						else:
							self.btnInstall.setLabel('Update'+AciVer); 
							self.btnInstall.setVisible(True); 
							self.btnInstall.setEnabled(True); 
					else:
							self.btnInstall.setLabel('Disabled'+AciVer); 
							self.btnInstall.setVisible(True); 
							self.btnInstall.setEnabled(False); 
				else: 
					self.btnInstall.setLabel('Install'); 
					self.btnInstall.setVisible(True); 
					self.btnInstall.setEnabled(True); 
			except: self.btnInstall.setEnabled(False); self.btnInstall.setLabel('')
			try: 
				if 'tru' in addonFsi.getProperty("addon.installed"):
					self.btnUninstall.setLabel('Uninstall'); 
					self.btnUninstall.setVisible(True); 
					self.btnUninstall.setEnabled(True); 
				#else: self.btnUninstall.setEnabled(False); self.btnUninstall.setLabel(''); 
				else: self.btnUninstall.setVisible(False); self.btnUninstall.setEnabled(False); self.btnUninstall.setLabel(''); 
			#except: self.btnUninstall.setEnabled(False); self.btnUninstall.setLabel(''); 
			except: self.btnUninstall.setVisible(False); self.btnUninstall.setEnabled(False); self.btnUninstall.setLabel(''); 
			##
		except: pass
	def StartWindow2nd(self):
		#BusyAnimationShow()
		self.TempWindow2=MyWindowAddons(owner=self); self.TempWindow2.doModal(); 
		del self.TempWindow2; 
	def RestartWindow2nd(self):
		try: 
			#self.TempWindow3.close()
			self.TempWindow2.CloseWindow2nd()
		except: pass
		del self.TempWindow2; 
		self.StartWindow2nd()
	def onControl(self,control):
		#Display Button control
		if   control==self.button[0]: self.CloseWindow1st()
		#elif control==self.button0: freeze_install(Main)
		#elif control==self.button1: freeze_uninstall(Main)
		#elif control==self.button3: xml_mod(Main)
		#elif control==self.button2: self.close()
		elif control==self.CtrlList: 
			#t2=self.CtrlList.getSelectedItem().getPath()
			t1=self.CtrlList.getSelectedItem()
			t2=str(t1.getProperty("repository.id"))
			#note("Repository's ID",t2)
			#deb("path",t2)
			#self.FillInRepoCatList(self.CtrlList.getSelectedItem())
			#self.FillInAddonsList(self.CtrlList.getSelectedItem())
			self.CurrentRepoSelected=self.CtrlList.getSelectedItem()
			#self.CtrlList.setEnabled(False); 
			self.StartWindow2nd()
			#self.CtrlList.setEnabled(True); 
			##
		
		##
	def CloseWindow1st(self):
		try: zz=[self.CtrlList,self.RepoThumbnail,self.RepoFanart2,self.RepoFanart,self.LabCurrentRepo,self.LabTitle,self.button[0],self.TVS,self.TVSBGB,self.BGB]
		except: zz=[]
		for z in zz:
			try: self.removeControl(z); del z
			except: pass
		self.close()
	##
## ################################################## ##
## ################################################## ##

class MyWindowAddons(xbmcgui.Window):
	#
	#
	InstallToPath=xbmc.validatePath(xbmc.translatePath(os.path.join("special://home","addons")))
	DownloadToPath=xbmc.validatePath(xbmc.translatePath(os.path.join("special://home","addons","packages")))
	DotOrgRepo_XML='http://mirrors.xbmc.org/addons/frodo/addons.xml'
	DotOrgRepo_XMLInfoCompressed=True
	DotOrgRepo_Checksum='http://mirrors.xbmc.org/addons/frodo/addons.xml.md5'
	DotOrgRepo_DataDirPath='http://mirrors.xbmc.org/addons/frodo'
	DotOrgRepo_DataDirZIP=True
	##
	CurrentRestrictToType=''; 
	button={}
	def __init__(self,owner):
		self.ow=owner; self.CurrentRestrictToType=''; 
		self.BGB=xbmcgui.ControlImage(0,0,1280,720,self.ow.b1,aspectRatio=0); self.addControl(self.BGB)
		self.TVSBGB=xbmcgui.ControlImage(800,12,280,190,self.ow.b1,aspectRatio=0); self.addControl(self.TVSBGB)
		self.TVS=xbmcgui.ControlImage(800,12,280,190,self.ow.b1,aspectRatio=0); self.addControl(self.TVS)
		#self.TVS.setAnimations([('WindowOpen','effect=rotatex time=0 end=30'),('WindowOpen','effect=rotatey time=0 end=60')])
		self.TVSBGB.setAnimations([('WindowOpen','effect=rotatey time=0 end=10 center=1040,120')])
		self.TVS.setAnimations([('WindowOpen','effect=rotatey time=0 end=10 center=1040,120')])
		BG=xbmcgui.ControlImage(0,0,1280,720,self.ow.backgroundB,aspectRatio=0); self.addControl(BG)
		focus=artp("button-focus2"); nofocus=artp("button-nofocus"); 
		self.AddonFanart2=xbmcgui.ControlImage(30,120,400,460,self.ow.b1,aspectRatio=0); self.addControl(self.AddonFanart2); 
		self.AddonFanart=xbmcgui.ControlImage(30,120,330,460,self.ow.b1,aspectRatio=0); self.addControl(self.AddonFanart); 
		self.AddonThumbnail=xbmcgui.ControlImage(330,120,100,100,self.ow.b1,aspectRatio=0); self.addControl(self.AddonThumbnail); 
		
		self.LabTitle=xbmcgui.ControlLabel(30,20,1000,50,'','font30','0xFFFF0000'); self.addControl(self.LabTitle)
		self.LabTitle.setLabel(self.ow.LabTitleText)
		#time.sleep(2); 
		self.LabCurrentRepo=xbmcgui.ControlLabel(180,80,220,30,'','font12','0xFF00BFFF',alignment=1); self.addControl(self.LabCurrentRepo)
		self.TypeListFanart=xbmcgui.ControlImage(1070,10,180,190,self.ow.b1,aspectRatio=0); self.addControl(self.TypeListFanart); 
		self.TypeList=xbmcgui.ControlList(1070,10,180,190,font='font12',textColor="0xFF8A2BE2",selectedColor="0xFF00FF00",buttonFocusTexture=focus,buttonTexture=nofocus); self.TypeList.setSpace(2); self.TypeList.setImageDimensions(0,0); self.TypeList.setItemHeight(25); self.addControl(self.TypeList); 
		zz=[self.TypeList,self.TypeListFanart]
		for z in zz: z.setAnimations([('WindowOpen','effect=slide delay=100 time=1000 start=1500')])
		self.AddonsList=xbmcgui.ControlList(30,120,400,480,font='font12',textColor="0xFFFF0000",selectedColor="0xFF00FF00",buttonFocusTexture=focus,buttonTexture=nofocus); self.AddonsList.setSpace(5); self.addControl(self.AddonsList); 
		zz=[self.AddonsList,self.AddonFanart2,self.AddonFanart,self.AddonThumbnail]
		for z in zz: z.setAnimations([('WindowOpen','effect=slide delay=100 time=1000 start=-500')])
		
		leftA=760; widA=235; hiB=30; topA=4; 
		self.btnInstall=xbmcgui.ControlButton(leftA-5-widA,topA,widA,hiB, "Install",textColor="0xFFB22222",focusedColor="0xFF00BFFF",alignment=2,focusTexture=focus,noFocusTexture=nofocus); self.addControl(self.btnInstall)
		self.btnUninstall=xbmcgui.ControlButton(leftA-5-widA,topA+2+hiB,widA,hiB, "Uninstall",textColor="0xFFB22222",focusedColor="0xFF00BFFF",alignment=2,focusTexture=focus,noFocusTexture=nofocus); self.addControl(self.btnUninstall)
		self.btnInstall.setVisible(False); self.btnUninstall.setVisible(False); 
		leftA=435; widA=235; hiB=30; 
		topA=75; 		hiA=200-topA+5; self.AddonFanart3=xbmcgui.ControlImage(leftA-10,topA,300+20,hiA,self.ow.b1,aspectRatio=0); self.addControl(self.AddonFanart3); 
		topA=topA+0; 		 hiA= 20; self.AddonsTitle=xbmcgui.ControlLabel(leftA,topA,300,hiA,'',font='font12',textColor="0xFF00BFFF"); self.addControl(self.AddonsTitle); 
		topA=topA+2+hiA; hiA= 20; self.AddonsId=xbmcgui.ControlLabel(leftA,topA,200,hiA,'',font='font12',textColor="0xFFFF0000"); self.addControl(self.AddonsId); 
		topA=			 topA; hiA= 20; self.AddonsVer=xbmcgui.ControlLabel(leftA+200,topA,100,hiA,'',font='font12',textColor="0xFFFFFFFF",alignment=1); self.addControl(self.AddonsVer); 
		topA=topA+2+hiA; hiA= 20; self.AddonsAuthor=xbmcgui.ControlLabel(leftA,topA,300,hiA,'',font='font12',textColor="0xFFFFFFFF"); self.addControl(self.AddonsAuthor); 
		topA=topA+2+hiA; hiA= 20; self.AddonsPlatform=xbmcgui.ControlLabel(leftA,topA,200,hiA,'',font='font12',textColor="0xFFFFFFFF"); self.addControl(self.AddonsPlatform); 
		topA=			 topA; hiA= 20; self.AddonsLanguage=xbmcgui.ControlLabel(leftA+100,topA,200,hiA,'',font='font12',textColor="0xFFFFFFFF",alignment=1); self.addControl(self.AddonsLanguage); 
		topA=topA+2+hiA; hiA= 20; self.AddonsProvides=xbmcgui.ControlLabel(leftA,topA,300,hiA,'',font='font12',textColor="0xFFFF00FF"); self.addControl(self.AddonsProvides); 
		topA=topA+2+hiA; hiA= 20; self.AddonsRepoName=xbmcgui.ControlLabel(leftA,topA,300,hiA,'',font='font12',textColor="0xFFFFFFFF"); self.addControl(self.AddonsRepoName); 
		
		#topA=topA+2+hiA; hiA= 60; self.AddonsSummary=xbmcgui.ControlTextBox(leftA,topA,400,hiA,font='font12',textColor="0xFFFFFFFF"); self.addControl(self.AddonsSummary); 
		widA=400; 
		leftA=30; topA=580; hiA= 120; self.bgSummary=xbmcgui.ControlImage(leftA-2,topA,widA+4,hiA,self.ow.b1,aspectRatio=0); self.addControl(self.bgSummary); self.AddonsSummary=xbmcgui.ControlTextBox(leftA,topA,widA,hiA,font='font12',textColor="0xFFFFFFFF"); self.addControl(self.AddonsSummary); 
		leftA=leftA+2+400; topA=520; hiA=180; self.bgDescription=xbmcgui.ControlImage(leftA-2,topA,widA+4,hiA,self.ow.b1,aspectRatio=0); self.addControl(self.bgDescription); self.AddonsDescription=xbmcgui.ControlTextBox(leftA,topA,widA,hiA,font='font12',textColor="0xFFFFFFFF"); self.addControl(self.AddonsDescription); 
		leftA=leftA+2+400; topA=topA; hiA=180; self.bgRequirements=xbmcgui.ControlImage(leftA-2,topA,widA+4,hiA,self.ow.b1,aspectRatio=0); self.addControl(self.bgRequirements); self.AddonsRequirements=xbmcgui.ControlTextBox(leftA,topA,widA,hiA,font='font12',textColor="0xFFFFFFFF"); self.addControl(self.AddonsRequirements); 
		widA=290; leftA=770; topA=4; hiA= 120; self.bgBroken=xbmcgui.ControlImage(leftA-2,topA,widA+4,hiA,self.ow.b1,aspectRatio=0); self.addControl(self.bgBroken); self.AddonsBroken=xbmcgui.ControlTextBox(leftA,topA,widA,hiA,font='font12',textColor="0xFFFFFFFF"); self.addControl(self.AddonsBroken); self.bgBroken.setVisible(False); self.AddonsBroken.setVisible(False); 
		self.button[0]=xbmcgui.ControlButton(30, 70, 135, 30, "Back",textColor="0xFFB22222",focusedColor="0xFF00BFFF",alignment=2,focusTexture=focus,noFocusTexture=nofocus); self.addControl(self.button[0])
		self.ItemsA=getITEMS(table='addon',where=' WHERE addonID NOT IN (SELECT addonID FROM disabled)',what='addonID'); #debob(self.ItemsA); 
		self.ItemsR=getITEMS(table='repo',where=' WHERE addonID NOT IN (SELECT addonID FROM disabled)',what='addonID'); #debob(self.ItemsR); 
		#Items=getITEMS(table='repo',where=' WHERE addonID NOT IN (SELECT addonID FROM disabled)'); debob(Items); 
		#Items=sorted(Items, key=lambda item: item[1], reverse=False)
		##
		self.button[0].controlDown(self.AddonsList); self.button[0].controlUp(self.AddonsList); 
		self.button[0].controlLeft(self.AddonsList); self.button[0].controlRight(self.TypeList); 
		self.AddonsList.controlRight(self.TypeList); self.AddonsList.controlLeft(self.TypeList); 
		self.AddonsList.controlUp(self.button[0]); self.AddonsList.controlDown(self.button[0]); 
		self.btnInstall.controlRight(self.AddonsList); self.btnInstall.controlLeft(self.AddonsList); 
		self.btnInstall.controlUp(self.AddonsList); self.btnInstall.controlDown(self.btnUninstall); 
		self.btnUninstall.controlRight(self.AddonsList); self.btnUninstall.controlLeft(self.AddonsList); 
		self.btnUninstall.controlUp(self.btnInstall); self.btnUninstall.controlDown(self.AddonsList); 
		self.TypeList.controlRight(self.AddonsList); self.TypeList.controlLeft(self.AddonsList); 
		self.TypeList.controlUp(self.button[0]); self.TypeList.controlDown(self.AddonsList); 
		self.btnInstall.setEnabled(False); self.btnUninstall.setEnabled(False); 
		self.setFocus(self.button[0])
		##
		#self.DotOrgREPO=getURL(self.DotOrgRepo_XML)
		#if len(self.DotOrgREPO) > 0: self.DotOrgREPO_Addons=re.compile('<addon\s+(.+?)>(.+?)</addon',re.IGNORECASE).findall(self.DotOrgREPO)
		#else: self.DotOrgREPO=[]
		##
		zz=[self.AddonsBroken,self.bgBroken,self.AddonFanart3,self.bgSummary,self.bgDescription,self.bgRequirements,self.AddonsId,self.AddonsVer,self.AddonsTitle,self.AddonsRepoName,self.AddonsAuthor,self.AddonsProvides,self.AddonsLanguage,self.AddonsPlatform,self.AddonsDescription,self.AddonsSummary,self.AddonsRequirements]
		for z in zz: z.setVisible(False)
		self.FillInAddonsList(self.ow.CurrentRepoSelected)
		##
	def getCurrentVerOfAddon(self,TheAddonXmlFile):
		if os.path.isfile(TheAddonXmlFile)==False: return ''
		try: addon_xml=nolines(Common._OpenFile(TheAddonXmlFile))
		except: return ''
		try: addon_xml_addon=re.compile("<addon(.*?)>",re.IGNORECASE).findall(' '+addon_xml)[0]
		except: return ''
		#try: addon_xml_addon_name=re.compile('\s+name="(.*?)"',re.IGNORECASE).findall(addon_xml_addon)[0]
		#except: return ''
		try: addon_xml_addon_version=re.compile('\s+version="(.*?)"',re.IGNORECASE).findall(' '+addon_xml_addon)[0]
		except: return ''
		try: return addon_xml_addon_version
		except: return ''
	def FillInAddonsList(self,SelectedRepo):
		##
		self.RepoID=SelectedRepo.getProperty("repository.id")
		self.RepoName=SelectedRepo.getProperty("repository.name")
		self.RepoVersion=SelectedRepo.getProperty("repository.version")
		self.RepoURL=SelectedRepo.getProperty("repository.url")
		self.RepoURLMD5=SelectedRepo.getProperty("repository.urlmd5")
		self.RepoURLPath=SelectedRepo.getProperty("repository.urlpath")
		self.LabCurrentRepo.setLabel(self.RepoName)
		self.AddonsList.reset()
		self.CurrentREPO=nolines(getURL(self.RepoURL)); 
		deb("Current Repository's URL",self.RepoURL); 
		if len(self.CurrentREPO)==0: note("Repo Error","Problem catching the Respository's .xml list of addons."); deb("Repo Error","Problem catching the Respository's .xml list of addons."); return
		try: 		self.CurrentREPO_Addons=re.compile('<addon(\s*.*?\s+name="(.+?)"\s*.*?)>(.+?)</addon',re.IGNORECASE).findall(self.CurrentREPO)
		except: self.CurrentREPO_Addons=[]
		try: self.CurrentREPO_Addons=sorted(self.CurrentREPO_Addons, key=lambda item: item[1], reverse=False)
		except: pass
		if (len(self.CurrentREPO_Addons)==0): note("Repo Error","No addons found in the current Respository's .xml list of addons."); deb("Repo Error","No addons found in the current Respository's .xml list of addons."); return
		deb("number of addons found",str(len(self.CurrentREPO_Addons))); 
		#try: setContent("addons"); 
		#except: pass
		self.ItemsA=getITEMS(table='addon',where=' WHERE addonID NOT IN (SELECT addonID FROM disabled)',what='addonID'); #debob(self.ItemsA); 
		#self.ItemsR=getITEMS(table='repo',where=' WHERE addonID NOT IN (SELECT addonID FROM disabled)',what='addonID'); #debob(self.ItemsR); 
		self.TypeListData=[]; self.TypeListData.append('All')
		self.TypeList.reset()
		for Zi,ZiSortBy,Zo in self.CurrentREPO_Addons: self.AddAddon(self.ItemsA,Zi,Zo,self.RepoID,self.RepoName,self.RepoVersion,self.RepoURLPath)
		self.TypeList.addItems(self.TypeListData)
		#for z in self.TypeListData: self.TypeList.addItem(z)
		self.setFocus(self.AddonsList)
		##
		#self.DotOrgREPO=getURL(self.DotOrgRepo_XML)
		#if len(self.DotOrgREPO) > 0: self.DotOrgREPO_Addons=re.compile('<addon\s+(.+?)>(*+?)</addon',re.IGNORECASE).findall(self.DotOrgREPO)
		##
		#try: BusyAnimationHide()
		#except: pass
	def RestrictList(self,RestrictToType=""):
		if RestrictToType=="All": RestrictToType=""
		self.AddonsList.reset(); self.CurrentRestrictToType=RestrictToType; 
		for Zi,ZiSortBy,Zo in self.CurrentREPO_Addons: self.AddAddon(self.ItemsA,Zi,Zo,self.RepoID,self.RepoName,self.RepoVersion,self.RepoURLPath,RestrictToType=RestrictToType)
		
		
		##
	def AddAddon(self,ItemsD,AddonInner,AddonOutter,RepoID="",RepoName="",RepoVersion="",RepoURLPath="",RepoCategory="",RepoSummary="",RepoDescription="",RepoDisclaimer="",RepoAuthor="",InstalledPath="special://home",RestrictToType=""):
		m={}; m2={}; AddonInner=" "+AddonInner; AddonOutter=" "+AddonOutter; KindOfAddon=""; 
		zz=['id','version','name','provider-name']
		for z in zz:
			mv=''+z; mu=''+z; #debob(z); debob(AddonInner); 
			try:			m[mv]=re.compile('\s+'+mu+'="(.+?)"',re.IGNORECASE).findall(' '+AddonInner)[0]
			except:		
				try: 		m[mv]=re.compile("\s+"+mu+"='(.+?)'",re.IGNORECASE).findall(' '+AddonInner)[0]
				except: m[mv]=''; deb(RepoID,"failed to parse: "+z); 
			#m[mv]=re.compile('\s+'+mu+'="(.+?)"',re.IGNORECASE).findall(' '+AddonInner)[0]
		zz2=['provides','requires','extension point="xbmc.addon.metadata"','language','platform','forum','website','source','broken','email']
		for z in zz2:
			mv=''+z; mu=''+z;
			try:			m2[mv]=re.compile('<'+mu+'\s*>(.+?)</'+mu+'',re.IGNORECASE).findall(' '+AddonOutter)[0]
			except:		m2[mv]=''
		m2['requires']=m2['requires'].replace('	',' ').replace('  ',' ').replace('  ',' ').replace('  ',' ').replace('  ',' ').replace('> <','>[CR]<').replace('><','>[CR]<')
		zz3=['summary','description','disclaimer']
		for z in zz3:
			mv=''+z; mu=''+z;
			try:			m2[mv]=re.compile('<'+mu+'\s+lang="en"\s*>(.+?)</'+mu+'',re.IGNORECASE).findall(' '+AddonOutter)[0]
			except:		
				try:		m2[mv]=re.compile('<'+mu+'\s*>(.+?)</'+mu+'',re.IGNORECASE).findall(' '+AddonOutter)[0]
				except:	m2[mv]=''
		##
		if (len(RepoURLPath) > 4):
			if (RepoURLPath[0:1:-1] not in '/'): 
				RepoURLPath+='/'
		r1=RepoURLPath+"/"+m['id']+"/icon.png"
		r2=RepoURLPath+"/"+m['id']+"/fanart.jpg"
		#deb("icon",r1)
		c1NameTag=''; c1VerTag=''; 
		if len(m2['broken']) > 0: c1NameTag=' [COLOR grey][Broken][/COLOR]'
		inst1=str(repo(m['id'],"addon.xml")); inst2=str(repox(m['id'],"addon.xml")); debob(inst1); 
		if   os.path.isfile(inst1)==True: 
			CurInstVer=self.getCurrentVerOfAddon(inst1)
			if m['version']==CurInstVer: c1VerTag+='[COLOR blue] *[/COLOR]'
			else: c1VerTag+='[COLOR blue] +[/COLOR]'
		elif os.path.isfile(inst2)==True: 
			CurInstVer=self.getCurrentVerOfAddon(inst2); 
			if m['version']==CurInstVer: c1VerTag+='[COLOR grey] *[/COLOR]'
			else: c1VerTag+='[COLOR grey] +[/COLOR]'
		else: c1VerTag+='[COLOR black]   [/COLOR]'
		##
		if   ('point="xbmc.addon.repository"' in AddonOutter) or ("point='xbmc.addon.repository'" in AddonOutter): KindOfAddon='Repository'; 
		elif ('point="xbmc.gui.skin"' in AddonOutter) or ("point='xbmc.gui.skin'" in AddonOutter): KindOfAddon='Skin'; 
		elif ('point="xbmc.gui.webinterface"' in AddonOutter) or ("point='xbmc.gui.webinterface'" in AddonOutter): KindOfAddon='Web interface'; 
		elif ('point="xbmc.ui.screensaver"' in AddonOutter) or ("point='xbmc.ui.screensaver'" in AddonOutter): KindOfAddon='Screensaver'; 
		elif ('point="xbmc.python.weather"' in AddonOutter) or ("point='xbmc.python.weather'" in AddonOutter): KindOfAddon='Weather'; 
		elif ('point="xbmc.python.lyrics"' in AddonOutter) or ("point='xbmc.python.lyrics'" in AddonOutter): KindOfAddon='Lyrics'; 
		elif ('point="xbmc.python.subtitles"' in AddonOutter) or ("point='xbmc.python.subtitles'" in AddonOutter): KindOfAddon='Subtitles'; 
		elif ('point="xbmc.python.pluginsource"' in AddonOutter) or ("point='xbmc.python.pluginsource'" in AddonOutter): KindOfAddon='Addons'; 
		elif ('point="xbmc.python.script"' in AddonOutter) or ("point='xbmc.python.script'" in AddonOutter): KindOfAddon='Programs'; 
		elif ('point="xbmc.python.module"' in AddonOutter) or ("point='xbmc.python.module'" in AddonOutter): KindOfAddon='Script Modules'; 
		elif ('point="xbmc.metadata.scraper.tvshows"' in AddonOutter) or ("point='xbmc.metadata.scraper.tvshows'" in AddonOutter): KindOfAddon='TV information'; 
		elif ('point="xbmc.metadata.scraper.movies"' in AddonOutter) or ("point='xbmc.metadata.scraper.movies'" in AddonOutter): KindOfAddon='Movie information'; 
		elif ('point="xbmc.metadata.scraper.artists"' in AddonOutter) or ("point='xbmc.metadata.scraper.artists'" in AddonOutter): KindOfAddon='Artist information'; 
		elif ('point="xbmc.metadata.scraper.albums"' in AddonOutter) or ("point='xbmc.metadata.scraper.albums'" in AddonOutter): KindOfAddon='Album information'; 
		elif ('point="xbmc.service"' in AddonOutter) or ("point='xbmc.service'" in AddonOutter): KindOfAddon='Services'; 
		else: KindOfAddon='Addons'; 
		#KindOfAddon=" [COLOR blueviolet][I]"+KindOfAddon+"[/I][/COLOR]"
		##
		if KindOfAddon not in self.TypeListData: self.TypeListData.append(KindOfAddon)
		
		c1=xbmcgui.ListItem(m['name']+c1NameTag+" [COLOR blueviolet][I]"+KindOfAddon+"[/I][/COLOR]",m['version']+c1VerTag,iconImage=r1,thumbnailImage=r1)
		if   os.path.isfile(inst1)==True: c1.setProperty("addon.installed",'true'); CurInstVer=self.getCurrentVerOfAddon(inst1); c1.setProperty("addon.installedpath",inst1); 
		elif os.path.isfile(inst2)==True: c1.setProperty("addon.installed",'trux'); CurInstVer=self.getCurrentVerOfAddon(inst2); c1.setProperty("addon.installedpath",inst2); 
		else: c1.setProperty("addon.installed",'false'); CurInstVer=''; 
		c1.setProperty("addon.currentinstalledversion",str(CurInstVer)); 
		c1.setProperty("addon.kindofaddon",str(KindOfAddon)); 
		##
		for z in zz: 
			#c1.setProperty("addon."+z,m[z])
			try: c1.setProperty("addon."+z,m[z])
			except: pass
		for z in zz2: 
			#c1.setProperty("addon."+z,m2[z])
			try: c1.setProperty("addon."+z,m2[z])
			except: pass
		for z in zz3: 
			try: c1.setProperty("addon."+z,m2[z])
			except: pass
		##
		c1.setProperty("repository.id",RepoID)
		c1.setProperty("addon.icon",r1)
		c1.setProperty("addon.fanart",r2)
		#c1.setProperty("repository.icon",r1)
		#c1.setProperty("repository.fanart",r2)
		c1.setProperty("repository.summary",RepoSummary)
		c1.setProperty("repository.description",RepoDescription)
		c1.setProperty("repository.disclaimer",RepoDisclaimer)
		c1.setProperty("repository.version",RepoVersion)
		c1.setProperty("repository.name",RepoName)
		c1.setProperty("repository.urlpath",RepoURLPath)
		##
		#c1.setProperty("repository.categories",RepoCategory)
		#c1.setProperty("repository.category",RepoCategory)
		#ItemsD=getITEMS(table='addon',where=' WHERE addonID NOT IN (SELECT addonID FROM disabled)',what='addonID'); debob(ItemsD); 
		isE=False
		ZrZ=[self.ItemsA,self.ItemsR]
		for zZ in ZrZ:
			for z in zZ:
				if m['id'] in z: isE=True
		if isE==True: c1.setProperty("addon.ebabled",'true')
		#if m['id'] in ItemsD: c1.setProperty("addon.ebabled",'true')
		else: c1.setProperty("addon.ebabled",'false')
		if (len(RestrictToType)==0) or (RestrictToType.lower()==KindOfAddon.lower()):
			self.AddonsList.addItem(c1)
		##
	def onAction(self,action):
		#non Display Button control
		if   action == Config.ACTION_PREVIOUS_MENU: self.CloseWindow2nd()
		elif action == Config.ACTION_NAV_BACK: self.CloseWindow2nd()
		try:
			addonI=str(self.AddonsList.getSelectedItem().getProperty("addon.icon")); #debob(addonI); 
			addonF=str(self.AddonsList.getSelectedItem().getProperty("addon.fanart"))
			if self.ow.show_graphics_behind_list==True:
   				if (len(addonI) > 0):
					self.AddonThumbnail.setImage(addonI); self.AddonThumbnail.setVisible(True)
				else: self.AddonThumbnail.setImage(self.ow.b1); self.AddonThumbnail.setVisible(False)
				if (len(addonF) > 0):
					self.AddonFanart.setImage(addonF); self.AddonFanart.setVisible(True)
					#self.LabTitle.setLabel(rpF)
				else: self.AddonFanart.setImage(self.ow.b1); #self.RepoFanart.setVisible(False)
			else:
				self.TVS.setImage(addonI); self.TVS.setVisible(True)
				self.BGB.setImage(addonF); self.BGB.setVisible(True)
		except: pass
		#if addonI==addonI:
		try:
			addonFsi=self.AddonsList.getSelectedItem()
			#debob(addonFsi.getLabel())
			#debob(addonFsi.getProperty("addon.id"))
			zz=[self.AddonFanart3,self.bgSummary,self.bgDescription,self.bgRequirements,self.AddonsId,self.AddonsVer,self.AddonsTitle,self.AddonsRepoName,self.AddonsAuthor,self.AddonsProvides,self.AddonsLanguage,self.AddonsPlatform,self.AddonsDescription,self.AddonsSummary,self.AddonsRequirements]
			for z in zz: z.setVisible(True); 
			try: self.AddonsId.setLabel("[COLOR mediumpurple]ID: [/COLOR]"+str(addonFsi.getProperty("addon.id")))
			except: self.AddonsId.setLabel('')
			aLatestVersion=str(addonFsi.getProperty("addon.version")); 
			try: self.AddonsVer.setLabel("[COLOR mediumpurple]ver: [/COLOR]"+aLatestVersion)
			except: self.AddonsVer.setLabel('')
			try: self.AddonsTitle.setLabel("[COLOR mediumpurple]Name: [/COLOR]"+str(addonFsi.getProperty("addon.name")))
			except: self.AddonsTitle.setLabel('')
			try: self.AddonsRepoName.setLabel("[COLOR mediumpurple]Repo: [/COLOR]"+str(addonFsi.getProperty("repository.name")))
			except: self.AddonsRepoName.setLabel('')
			try: self.AddonsAuthor.setLabel("[COLOR mediumpurple]Author(s): [/COLOR]"+str(addonFsi.getProperty("addon.provider-name")))
			except: self.AddonsAuthor.setLabel('')
			try: self.AddonsProvides.setLabel("[COLOR mediumpurple]Type: [/COLOR]"+"[COLOR blueviolet][I]"+str(addonFsi.getProperty("addon.kindofaddon"))+"[/I][/COLOR]  "+str(addonFsi.getProperty("addon.provides")))
			except: self.AddonsProvides.setLabel('')
			try: self.AddonsSummary.setText("[COLOR mediumpurple]Summary: [/COLOR]"+str(addonFsi.getProperty("addon.summary"))); self.bgSummary.setVisible(True); 
			except: self.AddonsSummary.setText(''); self.bgSummary.setVisible(False); 
			try: self.AddonsDescription.setText("[COLOR mediumpurple]Description: [/COLOR]"+str(addonFsi.getProperty("addon.description")))
			except: self.AddonsDescription.setText('')
			try: self.AddonsRequirements.setText("[COLOR mediumpurple]Requires: [/COLOR][CR]"+str(addonFsi.getProperty("addon.requires").replace('addon=','').replace('version=','').replace('/>','>').replace(' <','<')))
			except: self.AddonsRequirements.setText('')
			try: 
				if len(str(addonFsi.getProperty("addon.language"))) > 0:
					self.AddonsLanguage.setLabel("[COLOR mediumpurple]Language: [/COLOR]"+str(addonFsi.getProperty("addon.language"))); self.AddonsLanguage.setVisible(True); 
				else: self.AddonsLanguage.setLabel('')
			except: self.AddonsLanguage.setLabel('')
			try: 
				if len(str(addonFsi.getProperty("addon.platform"))) > 0:
					self.AddonsPlatform.setLabel("[COLOR mediumpurple]Platform: [/COLOR]"+str(addonFsi.getProperty("addon.platform"))); self.AddonsPlatform.setVisible(True); 
				else: self.AddonsPlatform.setLabel('')
			except: self.AddonsPlatform.setLabel('')
			try: 
				if len(str(addonFsi.getProperty("addon.broken"))) > 0:
					self.AddonsBroken.setText("[COLOR mediumpurple]Broken: [/COLOR]"+str(addonFsi.getProperty("addon.broken"))); self.bgBroken.setVisible(True); self.AddonsBroken.setVisible(True); 
				else: self.AddonsBroken.setText(''); self.bgBroken.setVisible(False); self.AddonsBroken.setVisible(False); 
			except: self.AddonsBroken.setText(''); self.bgBroken.setVisible(False); self.AddonsBroken.setVisible(False); 
			##
			#addon.currentinstalledversion
			#addon.installed
			try: 
				if 'tru' in addonFsi.getProperty("addon.installed"):
					try: 		AciVerA=str(addonFsi.getProperty("addon.currentinstalledversion")); AciVer=' ['+AciVerA+']'
					except: AciVerA=''; AciVer=''
					#debob((AciVerA,aLatestVersion)); 
					#try: 
					AciE=str(addonFsi.getProperty("addon.ebabled")); 
					#except: AciE='false'
					#deb('AciE',AciE); 
					if AciE=='true':
						if AciVerA==aLatestVersion:
							self.btnInstall.setLabel('['+AciVerA+']'); 
							self.btnInstall.setVisible(True); 
							self.btnInstall.setEnabled(False); 
						else:
							self.btnInstall.setLabel('Update'+AciVer); 
							self.btnInstall.setVisible(True); 
							self.btnInstall.setEnabled(True); 
					else:
							self.btnInstall.setLabel('Disabled'+AciVer); 
							self.btnInstall.setVisible(True); 
							self.btnInstall.setEnabled(False); 
				else: 
					self.btnInstall.setLabel('Install'); 
					self.btnInstall.setVisible(True); 
					self.btnInstall.setEnabled(True); 
			except: self.btnInstall.setEnabled(False); self.btnInstall.setLabel('')
			#self.btnInstall.setEnabled(False); 
			try: 
				if 'tru' in addonFsi.getProperty("addon.installed"):
					self.btnUninstall.setLabel('Uninstall'); 
					self.btnUninstall.setVisible(True); 
					self.btnUninstall.setEnabled(True); 
				#else: self.btnUninstall.setEnabled(False); self.btnUninstall.setLabel(''); 
				else: self.btnUninstall.setVisible(False); self.btnUninstall.setEnabled(False); self.btnUninstall.setLabel(''); 
			#except: self.btnUninstall.setEnabled(False); self.btnUninstall.setLabel(''); 
			except: self.btnUninstall.setVisible(False); self.btnUninstall.setEnabled(False); self.btnUninstall.setLabel(''); 
			#self.btnUninstall.setEnabled(False); 
			##
		except: pass
		self.btnInstall.setEnabled(False); 
		self.btnUninstall.setEnabled(False); 
	def ReDo2ndWindow(self):
		try: self.TempWindow3.CloseWindow3rd(); #self.TempWindow3.close()
		except: pass
		try: del self.TempWindow3; 
		except: pass
		self.FillInAddonsList(self.ow.CurrentRepoSelected)
	def StartWindow3rd(self):
		#BusyAnimationShow()
		self.TempWindow3=MyWindowWorks(owner=self); self.TempWindow3.doModal(); 
		try: del self.TempWindow3; 
		except: pass
	def RestartWindow3rd(self):
		try: 
			#self.TempWindow3.close()
			self.TempWindow3.CloseWindow3rd()
		except: pass
		try: del self.TempWindow3; 
		except: pass
		self.StartWindow3rd()
	def onControl(self,control):
		#Display Button control
		if   control==self.button[0]: self.CloseWindow2nd()
		elif control==self.AddonsList:
			self.CurSelAddon=self.AddonsList.getSelectedItem(); 
			self.StartWindow3rd(); 
			return
		elif control==self.TypeList:
			#try:
			RestrictToType=str(self.TypeList.getSelectedItem().getLabel()); 
			if not RestrictToType==self.CurrentRestrictToType: 
				self.RestrictList(RestrictToType)
			#except: pass
		##
	def CloseWindow2nd(self):
		try: zz=[self.TypeList,self.TypeListFanart,self.AddonsTitle,self.AddonsId,self.AddonsVer,self.AddonsAuthor,self.AddonsPlatform,self.AddonsLanguage,self.AddonsProvides,self.AddonsRepoName,self.LabCurrentRepo,self.btnInstall,self.btnUninstall,self.AddonsList,self.AddonThumbnail,self.AddonFanart3,self.AddonFanart2,self.AddonFanart,self.LabTitle,self.button[0],self.TVS,self.TVSBGB,self.BGB]
		except: zz=[]
		for z in zz:
			try: self.removeControl(z); del z
			except: pass
		self.close()
	##
## ################################################## ##
## ################################################## ##
class MyWindowWorks(xbmcgui.Window):
	InstallToPath=xbmc.validatePath(xbmc.translatePath(os.path.join("special://home","addons")))
	DownloadToPath=xbmc.validatePath(xbmc.translatePath(os.path.join("special://home","addons","packages")))
	DotOrgRepo_XML='http://mirrors.xbmc.org/addons/frodo/addons.xml'
	DotOrgRepo_XMLInfoCompressed=True
	DotOrgRepo_Checksum='http://mirrors.xbmc.org/addons/frodo/addons.xml.md5'
	DotOrgRepo_DataDirPath='http://mirrors.xbmc.org/addons/frodo'
	DotOrgRepo_DataDirZIP=True
	##
	button={}
	def __init__(self,owner):
		self.ow=owner.ow; self.ow2=owner; 
		self.BGB=xbmcgui.ControlImage(0,0,1280,720,self.ow.b1,aspectRatio=0); self.addControl(self.BGB)
		self.TVSBGB=xbmcgui.ControlImage(800,12,280,190,self.ow.b1,aspectRatio=0); self.addControl(self.TVSBGB)
		self.TVS=xbmcgui.ControlImage(800,12,280,190,self.ow.b1,aspectRatio=0); self.addControl(self.TVS)
		#self.TVS.setAnimations([('WindowOpen','effect=rotatex time=0 end=30'),('WindowOpen','effect=rotatey time=0 end=60')])
		self.TVSBGB.setAnimations([('WindowOpen','effect=rotatey time=0 end=10 center=1040,120')])
		self.TVS.setAnimations([('WindowOpen','effect=rotatey time=0 end=10 center=1040,120')])
		self.BG=xbmcgui.ControlImage(0,0,1280,720,self.ow.backgroundB,aspectRatio=0); self.addControl(self.BG)
		focus=artp("button-focus2"); nofocus=artp("button-nofocus"); 
		#self.AddonFanart2=xbmcgui.ControlImage(30,120,400,460,self.ow.b1,aspectRatio=0); self.addControl(self.AddonFanart2); 
		#self.AddonFanart=xbmcgui.ControlImage(30,120,330,460,self.ow.b1,aspectRatio=0); self.addControl(self.AddonFanart); 
		#self.AddonThumbnail=xbmcgui.ControlImage(740,120,100,100,self.ow.b1,aspectRatio=0); self.addControl(self.AddonThumbnail); 
		self.LabTitle=xbmcgui.ControlLabel(30,20,1000,50,'','font30','0xFFFF0000'); self.addControl(self.LabTitle)
		self.LabTitle.setLabel(self.ow.LabTitleText)
		#time.sleep(2); 
		self.LabCurrentRepo=xbmcgui.ControlLabel(180,80,220,30,'','font12','0xFF00BFFF',alignment=1); self.addControl(self.LabCurrentRepo)
		#self.AddonsList=xbmcgui.ControlList(30,120,400,480,font='font12',textColor="0xFFFF0000",selectedColor="0xFF00FF00",buttonFocusTexture=focus,buttonTexture=nofocus); self.AddonsList.setSpace(5); self.addControl(self.AddonsList); 
		leftA=760; widA=235; hiB=30; topA=4; 
		self.btnInstall=xbmcgui.ControlButton(leftA-5-widA,topA,widA,hiB, "Install",textColor="0xFFB22222",focusedColor="0xFF00BFFF",alignment=2,focusTexture=focus,noFocusTexture=nofocus); self.addControl(self.btnInstall)
		self.btnUninstall=xbmcgui.ControlButton(leftA-5-widA,topA+2+hiB,widA,hiB, "Uninstall",textColor="0xFFB22222",focusedColor="0xFF00BFFF",alignment=2,focusTexture=focus,noFocusTexture=nofocus); self.addControl(self.btnUninstall)
		self.btnInstall.setVisible(False); self.btnUninstall.setVisible(False); 
		leftA=435; widA=235; hiB=30; 
		topA=75; 		hiA=200-topA+5; self.AddonFanart3=xbmcgui.ControlImage(leftA-10,topA,300+20,hiA,self.ow.b1,aspectRatio=0); self.addControl(self.AddonFanart3); 
		topA=topA+0; 		 hiA= 20; self.AddonsTitle=xbmcgui.ControlLabel(leftA,topA,300,hiA,'',font='font12',textColor="0xFF00BFFF"); self.addControl(self.AddonsTitle); 
		topA=topA+2+hiA; hiA= 20; self.AddonsId=xbmcgui.ControlLabel(leftA,topA,200,hiA,'',font='font12',textColor="0xFFFF0000"); self.addControl(self.AddonsId); 
		topA=			 topA; hiA= 20; self.AddonsVer=xbmcgui.ControlLabel(leftA+200,topA,100,hiA,'',font='font12',textColor="0xFFFFFFFF",alignment=1); self.addControl(self.AddonsVer); 
		topA=topA+2+hiA; hiA= 20; self.AddonsAuthor=xbmcgui.ControlLabel(leftA,topA,300,hiA,'',font='font12',textColor="0xFFFFFFFF"); self.addControl(self.AddonsAuthor); 
		topA=topA+2+hiA; hiA= 20; self.AddonsPlatform=xbmcgui.ControlLabel(leftA,topA,200,hiA,'',font='font12',textColor="0xFFFFFFFF"); self.addControl(self.AddonsPlatform); 
		topA=			 topA; hiA= 20; self.AddonsLanguage=xbmcgui.ControlLabel(leftA+100,topA,200,hiA,'',font='font12',textColor="0xFFFFFFFF",alignment=1); self.addControl(self.AddonsLanguage); 
		topA=topA+2+hiA; hiA= 20; self.AddonsProvides=xbmcgui.ControlLabel(leftA,topA,300,hiA,'',font='font12',textColor="0xFFFF00FF"); self.addControl(self.AddonsProvides); 
		topA=topA+2+hiA; hiA= 20; self.AddonsRepoName=xbmcgui.ControlLabel(leftA,topA,300,hiA,'',font='font12',textColor="0xFFFFFFFF"); self.addControl(self.AddonsRepoName); 
		#topA=topA+2+hiA; hiA= 60; self.AddonsSummary=xbmcgui.ControlTextBox(leftA,topA,400,hiA,font='font12',textColor="0xFFFFFFFF"); self.addControl(self.AddonsSummary); 
		widA=400; 
		leftA=30; topA=580; hiA= 120; self.bgSummary=xbmcgui.ControlImage(leftA,topA,widA,hiA,self.ow.b1,aspectRatio=0); self.addControl(self.bgSummary); self.AddonsSummary=xbmcgui.ControlTextBox(leftA,topA,widA,hiA,font='font12',textColor="0xFFFFFFFF"); self.addControl(self.AddonsSummary); 
		leftA=leftA+2+400; topA=520; hiA=180; self.bgDescription=xbmcgui.ControlImage(leftA-2,topA,widA+4,hiA,self.ow.b1,aspectRatio=0); self.addControl(self.bgDescription); self.AddonsDescription=xbmcgui.ControlTextBox(leftA,topA,widA,hiA,font='font12',textColor="0xFFFFFFFF"); self.addControl(self.AddonsDescription); 
		leftA=leftA+2+400; topA=topA; hiA=180; self.bgRequirements=xbmcgui.ControlImage(leftA-2,topA,widA+4,hiA,self.ow.b1,aspectRatio=0); self.addControl(self.bgRequirements); self.AddonsRequirements=xbmcgui.ControlTextBox(leftA,topA,widA,hiA,font='font12',textColor="0xFFFFFFFF"); self.addControl(self.AddonsRequirements); 
		widA=440; leftA=770; topA=4; hiA= 60; self.bgBroken=xbmcgui.ControlImage(leftA-2,topA,widA+4,hiA,self.ow.b1,aspectRatio=0); self.addControl(self.bgBroken); self.AddonsBroken=xbmcgui.ControlTextBox(leftA,topA,widA,hiA,font='font12',textColor="0xFFFFFFFF"); self.addControl(self.AddonsBroken); 
		##
		self.button[0]=xbmcgui.ControlButton(30, 70, 135, 30, "Back",textColor="0xFFB22222",focusedColor="0xFF00BFFF",alignment=2,focusTexture=focus,noFocusTexture=nofocus); self.addControl(self.button[0])
		self.ItemsA=getITEMS(table='addon',where=' WHERE addonID NOT IN (SELECT addonID FROM disabled)',what='addonID'); #debob(self.ItemsA); 
		self.ItemsR=getITEMS(table='repo',where=' WHERE addonID NOT IN (SELECT addonID FROM disabled)',what='addonID'); #debob(self.ItemsR); 
		#Items=getITEMS(table='repo',where=' WHERE addonID NOT IN (SELECT addonID FROM disabled)'); debob(Items); 
		#Items=sorted(Items, key=lambda item: item[1], reverse=False)
		##
		self.button[0].controlDown(self.btnInstall); self.button[0].controlUp(self.btnUninstall); 
		self.button[0].controlLeft(self.btnInstall); self.button[0].controlRight(self.btnUninstall); 
		self.btnInstall.controlRight(self.button[0]); self.btnInstall.controlLeft(self.button[0]); 
		self.btnInstall.controlUp(self.btnUninstall); self.btnInstall.controlDown(self.btnUninstall); 
		self.btnUninstall.controlRight(self.button[0]); self.btnUninstall.controlLeft(self.button[0]); 
		self.btnUninstall.controlUp(self.btnInstall); self.btnUninstall.controlDown(self.btnInstall); 
		self.setFocus(self.button[0])
		##
		#self.DotOrgREPO=getURL(self.DotOrgRepo_XML)
		#if len(self.DotOrgREPO) > 0: self.DotOrgREPO_Addons=re.compile('<addon\s+(.+?)>(.+?)</addon',re.IGNORECASE).findall(self.DotOrgREPO)
		#else: self.DotOrgREPO=[]
		##
		#self.FillInAddonsList(self.ow.CurrentRepoSelected)
		self.CurSelAddon=self.ow2.CurSelAddon
		self.WindowStarted(self.ow2.CurSelAddon)
		##
	def WindowStarted(self,c):
		try:
			addonFsi=c
			#addonFsi=self.ow2.AddonsList.getSelectedItem()
			#debob(addonFsi.getLabel())
			#debob(addonFsi.getProperty("addon.id"))
			self.BGB.setImage(str(addonFsi.getProperty("addon.fanart"))); self.BGB.setVisible(True)
			self.TVS.setImage(str(addonFsi.getProperty("addon.icon"))); self.TVS.setVisible(True)
			try: self.AddonsId.setLabel("[COLOR mediumpurple]ID: [/COLOR]"+str(addonFsi.getProperty("addon.id")))
			except: self.AddonsId.setLabel('')
			aLatestVersion=str(addonFsi.getProperty("addon.version")); 
			try: self.AddonsVer.setLabel("[COLOR mediumpurple]ver: [/COLOR]"+aLatestVersion)
			except: self.AddonsVer.setLabel('')
			try: self.AddonsTitle.setLabel("[COLOR mediumpurple]Name: [/COLOR]"+str(addonFsi.getProperty("addon.name")))
			except: self.AddonsTitle.setLabel('')
			try: self.AddonsRepoName.setLabel("[COLOR mediumpurple]Repo: [/COLOR]"+str(addonFsi.getProperty("repository.name")))
			except: self.AddonsRepoName.setLabel('')
			try: self.AddonsAuthor.setLabel("[COLOR mediumpurple]Author(s): [/COLOR]"+str(addonFsi.getProperty("addon.provider-name")))
			except: self.AddonsAuthor.setLabel('')
			try: self.AddonsProvides.setLabel("[COLOR mediumpurple]Type: [/COLOR]"+"[COLOR blueviolet][I]"+str(addonFsi.getProperty("addon.kindofaddon"))+"[/I][/COLOR]  "+str(addonFsi.getProperty("addon.provides")))
			except: self.AddonsProvides.setLabel('')
			try: self.AddonsSummary.setText("[COLOR mediumpurple]Summary: [/COLOR]"+str(addonFsi.getProperty("addon.summary"))); self.bgSummary.setVisible(True); 
			except: self.AddonsSummary.setText(''); self.bgSummary.setVisible(False); 
			try: self.AddonsDescription.setText("[COLOR mediumpurple]Description: [/COLOR]"+str(addonFsi.getProperty("addon.description")))
			except: self.AddonsDescription.setText('')
			try: self.AddonsRequirements.setText("[COLOR mediumpurple]Requires: [/COLOR][CR]"+str(addonFsi.getProperty("addon.requires").replace('addon=','').replace('version=','').replace('/>','>').replace(' <','<')))
			except: self.AddonsRequirements.setText('')
			try: 
				if len(str(addonFsi.getProperty("addon.language"))) > 0:
					self.AddonsLanguage.setLabel("[COLOR mediumpurple]Language: [/COLOR]"+str(addonFsi.getProperty("addon.language")))
				else: self.AddonsLanguage.setLabel('')
			except: self.AddonsLanguage.setLabel('')
			try: 
				if len(str(addonFsi.getProperty("addon.platform"))) > 0:
					self.AddonsPlatform.setLabel("[COLOR mediumpurple]Platform: [/COLOR]"+str(addonFsi.getProperty("addon.platform")))
				else: self.AddonsPlatform.setLabel('')
			except: self.AddonsPlatform.setLabel('')
			try: 
				if len(str(addonFsi.getProperty("addon.broken"))) > 0:
					self.AddonsBroken.setText("[COLOR mediumpurple]Broken: [/COLOR]"+str(addonFsi.getProperty("addon.broken"))); self.bgBroken.setVisible(True); 
				else: self.AddonsBroken.setText(''); self.bgBroken.setVisible(False); 
			except: self.AddonsBroken.setText(''); self.bgBroken.setVisible(False); 
			try: 
				if 'tru' in addonFsi.getProperty("addon.installed"):
					try: 		AciVerA=str(addonFsi.getProperty("addon.currentinstalledversion")); AciVer=' ['+AciVerA+']'
					except: AciVerA=''; AciVer=''
					#debob((AciVerA,aLatestVersion)); 
					#try: 
					AciE=str(addonFsi.getProperty("addon.ebabled")); 
					#except: AciE='false'
					#deb('AciE',AciE); 
					if AciE=='true':
						if AciVerA==aLatestVersion:
							self.btnInstall.setLabel('['+AciVerA+']'); self.btnInstall.setVisible(True); self.btnInstall.setEnabled(False); 
						else: self.btnInstall.setLabel('Update'+AciVer); self.btnInstall.setVisible(True); self.btnInstall.setEnabled(True); 
					else: self.btnInstall.setLabel('Disabled'+AciVer); self.btnInstall.setVisible(True); self.btnInstall.setEnabled(False); 
				else: self.btnInstall.setLabel('Install'); self.btnInstall.setVisible(True); self.btnInstall.setEnabled(True); 
			except: self.btnInstall.setEnabled(False); self.btnInstall.setLabel('')
			try: 
				if 'tru' in addonFsi.getProperty("addon.installed"):
					self.btnUninstall.setLabel('Uninstall'); self.btnUninstall.setVisible(True); self.btnUninstall.setEnabled(True); 
				else: self.btnUninstall.setVisible(False); self.btnUninstall.setEnabled(False); self.btnUninstall.setLabel(''); 
			except: self.btnUninstall.setVisible(False); self.btnUninstall.setEnabled(False); self.btnUninstall.setLabel(''); 
			##
		except: pass
		##
		self.setFocus(self.btnInstall)
		try: bTxt=self.btnInstall.getLabel()
		except: bTxt=''
		#deb("Install-Button's Text",bTxt); 
		if len(bTxt) > 0:
			if   ('Install' in bTxt): self.btnInstall.setVisible(True); self.btnInstall.setEnabled(True); self.setFocus(self.btnInstall)
			elif ('Update' in bTxt): self.btnInstall.setVisible(True); self.btnInstall.setEnabled(True); self.setFocus(self.btnInstall)
			elif ('Disabled [' in bTxt): self.setFocus(self.btnUninstall)
			elif ('[' in bTxt) and (']' in bTxt): self.setFocus(self.btnUninstall)
			else: self.setFocus(self.btnUninstall)
	def getCurrentVerOfAddon(self,TheAddonXmlFile):
		if os.path.isfile(TheAddonXmlFile)==False: return ''
		try: addon_xml=nolines(Common._OpenFile(TheAddonXmlFile))
		except: return ''
		try: addon_xml_addon=re.compile("<addon(.*?)>",re.IGNORECASE).findall(addon_xml)[0]
		except: return ''
		#try: addon_xml_addon_name=re.compile('\s+name="(.*?)"',re.IGNORECASE).findall(addon_xml_addon)[0]
		#except: return ''
		try: addon_xml_addon_version=re.compile('\s+version="(.*?)"',re.IGNORECASE).findall(addon_xml_addon)[0]
		except: return ''
		try: return addon_xml_addon_version
		except: return ''
	def onAction(self,action):
		#non Display Button control
		if   action == Config.ACTION_PREVIOUS_MENU: self.CloseWindow3rd()
		elif action == Config.ACTION_NAV_BACK: self.CloseWindow3rd()
	def onControl(self,control):
		#Display Button control
		if   control==self.button[0]: self.CloseWindow3rd()
		elif control==self.btnInstall: self.doAddonInstall(control); 
		elif control==self.btnUninstall: self.doAddonUninstall(control); 
		##
	def CloseWindow3rd(self):
		try: zz=[self.AddonsTitle,self.AddonsId,self.AddonsVer,self.AddonsAuthor,self.AddonsPlatform,self.AddonsLanguage,self.AddonsProvides,self.AddonsRepoName,self.LabCurrentRepo,self.btnInstall,self.btnUninstall,self.AddonFanart3,self.LabTitle,self.button[0],self.TVS,self.TVSBGB,self.BGB]
		except: zz=[]
		for z in zz:
			try: self.removeControl(z); del z
			except: pass
		self.close()
	def doAddonActualInstall(self,control):
		bTxt=control.getLabel()
		#addonFsi=self.AddonsList.getSelectedItem()
		addonFsi=self.CurSelAddon
		aId=str(addonFsi.getProperty("addon.id"))
		aVer=str(addonFsi.getProperty("addon.version"))
		aUrlpath=str(addonFsi.getProperty("repository.urlpath"))
		if len(bTxt) > 0:
			msg="Do you want to install this?"; 
			ansr=popYN(title=aId,line1=msg); deb("answer",str(ansr)); 
			if ansr==True:
				msg="Prepairing to install..."; deb(aId,msg); #note(aId,msg); 
				dp=xbmcgui.DialogProgress(); dp.create(Config.name,"Downloading ",'','Please Wait')
				lib=xbmc.validatePath(xbmc.translatePath(os.path.join(self.DownloadToPath,aId+"-"+aVer+".zip"))); deb("downloaded file location",lib); 
				url=aUrlpath+"/"+aId+"/"+aId+"-"+aVer+".zip"; 
				url=url.replace("//"+aId,"/"+aId); 
				deb("url",url); 
				try: downloader.download(url,lib,dp,title=Config.name)
				except: deb(aId,"error on download"); return
				time.sleep(2); 
				dp.update(0,"","Extracting Zip Please Wait")
				try: extract.all(lib,self.InstallToPath,dp)
				except Exception, e: deb(aId,"error on extraction"); debob(e); return
				except: deb(aId,"error on extraction"); return
				
				self.doAddonPythonFix(control,os.path.join(self.InstallToPath,aId,'addon.xml'),aId); 
				
				self.UpdateLocalAddons(); 
				msg="Install Completed."; deb(aId,msg); 
				popOK(msg=msg,title=aId); 
				#return
			else: msg="Install canceled."; deb(aId,msg); note(aId,msg); 
			##
		##
	def UpdateLocalAddons(self):
		xbmc.executebuiltin("XBMC.UpdateLocalAddons()"); 
	def doAddonPythonFix(self,control,AddonXmlFile,AddonIdN):
		if tfalse(SettingG('pythonfix'))==True:
			note("AutoFixing Python Version",AddonIdN); 
			try: XVer2=int(XBMCversion['Ver'][0:2]); 
			except:
				try: XVer2=int(XBMCversion['Ver'][0:1]); 
				except: XVer2=0
			deb('XBMC Version', XVer2); 
			if XVer2==0: debob('problem finding xbmc version number.'); return
			elif XVer2 < 10: pver="1.0"
			elif XVer2==10: pver="1.0"
			elif XVer2==11: pver="1.0"
			elif XVer2==12: pver="2.1.0"
			elif XVer2==13: pver="2.1.0"
			elif XVer2==14: pver="2.1.0"
			else: debob('problem matching xbmc version number.'); return
			s=Common._OpenFile(AddonXmlFile); 
			try: s2=re.compile('<import\s+addon="xbmc.python"\s+version="[0-9\.]+"').findall(s)[0]; deb('current python version',s2); 
			except:
				try: s2=re.compile("<import\s+addon='xbmc.python'\s+version='[0-9\.]+'").findall(s)[0]; debob(s2); 
				except: s2=''
			if len(s2) > 0:
				s3='<import addon="xbmc.python" version="'+pver+'"'; deb('new     python version',s3); s=s.replace(s2,s3); 
				Common._SaveFile(AddonXmlFile,s); deb('addon.xml file has been updated',AddonXmlFile); 
			##
	def doAddonInstall(self,control):
		bTxt=control.getLabel()
		#addonFsi=self.AddonsList.getSelectedItem()
		addonFsi=self.CurSelAddon
		aId=str(addonFsi.getProperty("addon.id"))
		if len(bTxt) > 0:
			if   ('Install' in bTxt):
				msg="Attempting to Install Addon/Repository."; deb(aId,msg); 
				self.doAddonActualInstall(control); 
			elif ('Update [' in bTxt):
				msg="Attempting to Update Addon/Repository."; deb(aId,msg); 
				self.doAddonActualInstall(control); 
			elif ('Disabled [' in bTxt): 
				msg="The addon / repository is currently disabled."; deb(aId,msg); 
				popOK(msg=msg,title=aId)
				#ansr=popYN(title=aId,line1=msg); 
				#note(aId,msg); 
				return
			elif ('[' in bTxt) and (']' in bTxt): 
				msg="The current version is already installed."; deb(aId,msg); 
				popOK(msg=msg,title=aId)
				#ansr=popYN(title=aId,line1=msg); 
				#note(aId,msg); 
				return
			else: return
			self.ow2.ReDo2ndWindow()
		return
		##
	def doAddonUninstall(self,control):
		addonFsi=self.CurSelAddon
		aId=str(addonFsi.getProperty("addon.id"))
		aVer=str(addonFsi.getProperty("addon.version"))
		aUrlpath=str(addonFsi.getProperty("repository.urlpath"))
		debob([aId,aVer]); msg="Attempting to Uninstall Addon/Repository."; deb(aId,msg); 
		if len(aId)==0: msg="Addon ID -NOT- Found!"; deb(aId,msg); popOK(msg=msg,title=aId); return
		inst1=str(repo(aId)); inst2=str(repox(aId)); debob(inst1); 
		if os.path.exists(inst1)==False: msg="Path not found in[CR]special://home/addons/[CR]"+inst1; deb(aId,msg); popOK(msg=msg,title=aId); return
		deb("Path Found",inst1); 
		#msg="This Function is not currently available."; deb(aId,msg); popOK(msg=msg,title=aId); return
		msg="Do you want to [I]uninstall[/I]  this?"; ansr=popYN(title=aId,line1=msg); deb("answer",str(ansr)); 
		if ansr==True:
			try:
				shutil.rmtree(inst1)
			except Exception, e: deb(aId,"error on extraction"); debob(e); msg="* Problem while attempting to remove Addon!"; deb(aId,msg); popOK(msg=msg,title=aId); return
			except: msg="Problem while attempting to remove Addon!"; deb(aId,msg); popOK(msg=msg,title=aId); return
			msg="The addon should now be removed."; deb(aId,msg); popOK(msg=msg,title=aId); 
			self.UpdateLocalAddons(); 
			self.ow2.ReDo2ndWindow(); 
			return
		##
	def doAddonEnable(self,control):
		
		return
 		##
	def doAddonDisable(self,control):
		
		return
		##
	##


## ################################################## ##
## ################################################## ##



## Start of program
TempWindow=MyWindow()
TempWindow.doModal()
del TempWindow


