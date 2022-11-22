#!/usr/bin/env python

import re,os,time,datetime,glob,subprocess,numpy,sys
from obspy.core import read
from pylab import *
#numero minimo de estaciones que se leeran por evento.
nstamin = 4


#Comienza el loop por los directorios

path = os.getcwd()+'/'
loc = path+'LOC'

#CREANDO DIRECTORIOS NECESARIOS
try: 
    os.makedirs(path+'Leidos')
except OSError:
    if not os.path.isdir(path+'Leidos'):
        raise

try: 
    os.makedirs(loc+'/finalDEF')
except OSError:
    if not os.path.isdir(loc+'/finalDEF'):
        raise

leidos =  path+'Leidos'
finaldef = loc+'/finalDEF'
final = loc+'/final'

#BORRAR CONTENIDO DIRECTORIO FINAL
cmd = 'rm '+loc+'/final/*'
os.system(cmd)

k=0

#CAMBIAR AQUI DEPENDIENDO EL TIPO DE CARPETAS
#listdir = sorted(glob.glob('???????_????/'))
listdir = sorted(glob.glob('????-??-??-????/'))

for dire in listdir:	
	#MOVER DIRECTORIO YA LEIDO
	if k != 0:
#CAMBIAR SI IQUIQUE NO ES LA PALABRA CLAVE			
	   	try:		
#			cmd = 'cp '+final+'/Iquique.'+dire.split('_')[0][0:4]+'* '+finaldef
#CAMBIAR		
			cmd = 'cp '+final+'/Iquique.'+dire.split('-')[0][0:4]+'* '+finaldef
			os.system(cmd)
	   	except OSError:
			raise

		dirpre = listdir[k-1]
		cmd = 'mv '+path+dirpre+' '+leidos
		os.system(cmd)

		r = raw_input('\nSalir del programa? [s/n]\n')
		while r != 's' and r != 'n':
			r = raw_input('\nIncorrecto, intente otra vez. Salir? [s/n]?:\n')
			if r == 's' or r == 'n':
				break
		if r == 's':
			if k != 1:
				print '\n****Hasta la proxima!****\n'
				sys.exit(0)
			else:
				try:
#					cmd = 'cp '+final+'/Iquique.'+dire.split('_')[0][0:4]+'* '+finaldef
#CAMBIAR				
					cmd = 'cp '+final+'/Iquique.'+dire.split('-')[0][0:4]+'* '+finaldef

					os.system(cmd)
				except OSError:
					raise
				print '\n****Hasta la proxima!****\n'
				sys.exit(0)

				

	k += 1
        os.chdir(path+dire)
#CAMBIAR AQUI SEGUN EL TIPO DE ARCHIVOS 	
#	listfiles = sorted(glob.glob('*.SAC'))
	listfiles = sorted(glob.glob('????-??-??-????*..H*'))

        sta = [] 
	for file in listfiles:
		st = read(file)
	        tr = st[0]
                stac = tr.stats.station

		sta.append(stac)
	
	uniq = []
	for staelem in sta:
		if staelem not in uniq:
			uniq.append(staelem)
                largo = len(uniq)
	
	if largo >= nstamin:
	   print '\n\nTrabajando en el directorio '+dire+'\n'
   	   print '\nLA ULTIMA ESTACION PARA ESTE EVENTO ES '+uniq[largo-1]+'\n'
	   print 'EL NUMERO DE ESTACIONES ES: '+str(largo)+'\n'
	   time.sleep(2)
#CAMBIAR AQUI SEGUN EL TIPO DE ARCHIVOS 		
	   for stuni in uniq:
#	      filez = glob.glob('*'+stuni+'..*HZ*SAC')
	      filez = glob.glob('*'+stuni+'..*HZ')
       	      if not filez:
			filez = ' '
	      else:
			filez = filez[0]
#	      filen = glob.glob('*'+stuni+'..*HN*SAC')
	      filen = glob.glob('*'+stuni+'..*HN')
     	      if not filen:
			filen = ' '
	      else:
			filen = filen[0]

#	      filee = glob.glob('*'+stuni+'..*HE*SAC')
	      filee = glob.glob('*'+stuni+'..*HE')

	      if not filee:
			filee = ' '
	      else:
			filee = filee[0]

	      subprocess.call(['java net.alomax.seisgram2k.SeisGram2K -binarytype=SUN_UNIX '+filez+' '+filen+' '+filee+' -pick.file='+dire[0:len(dire)-1]+'.pick'],close_fds=True,shell=True)
	   #TERMINA EL LOOP
	   print '\n\nSE HAN TERMINADO DE REVISAR LAS ESTACIONES DISPONIBLES PARA EL EVENTO '+dire+'\n\n'
	   time.sleep(2)

	   with open(dire[0:len(dire)-1]+'.pick','r') as fichero:
				stapickfile = [] 
			
				for lin in fichero:
					if lin:
						stapickfile.append(lin.split()[0])

				stapickfileuniq = []
				for st in stapickfile:
					if st not in stapickfileuniq:
						stapickfileuniq.append(st)

	   if len(stapickfileuniq) >= nstamin:
		#MOSTRAR PICKFILE EN PANTALLA
		print '\n\nARCHIVO PEAKS:\n\n'
		cmd = 'more '+dire[0:len(dire)-1]+'.pick'
		os.system(cmd)
		time.sleep(2)
		#COMIENZA LA LOCALIZACION INDIVIDUAL
		print '\nCOMIENZO DE LOCALIZACION NLLOC PARA EL EVENTO '+dire+'...\n'
		time.sleep(2)
		cmd = 'cp '+dire[0:len(dire)-1]+'.pick '+loc
		os.system(cmd)
		os.chdir(loc)
		cmd = 'mv '+dire[0:len(dire)-1]+'.pick gatherpickfiles.dat'
		os.system(cmd)
		cmd = 'rm '+loc+'/final/*'
		os.system(cmd)

	
		subprocess.call(['NLLoc nlloc.in'],close_fds=True,shell=True)
				




#CAMBIAR "Iquique" SI ES NECESARIO
		os.chdir(loc+'/final')
				
		try:
#			hypfile = glob.glob('Iquique.'+dire.split('_')[0][0:4]+'*.hyp')[0]
#CAMBIAR		
			hypfile = glob.glob('Iquique.'+dire.split('-')[0][0:4]+'*.hyp')[0]

		except IndexError:
			hypfile = ''

	
		if hypfile:
#		   hypfile = glob.glob('Iquique.'+dire.split('_')[0][0:4]+'*.hyp')[0]
#CAMBIAR	   
		   hypfile = glob.glob('Iquique.'+dire.split('-')[0][0:4]+'*.hyp')[0]

		   time.sleep(3)
		   print '\n\nRESULTADOS DE LA LOCALIZACION:\n\n'
		   i = 1
		   with open(hypfile,'r') as hyp:	
			infoxsta = []
			for lin in hyp:
				   line = lin.rstrip()	
				   if line:
					if lin.split()[0] == 'GEOGRAPHIC':
						fechahora = lin.split()[2]+' '+ lin.split()[3] +' '+lin.split()[4]+' ' +lin.split()[5] +' ' + lin.split()[6] +' '+lin.split()[7]
						hipo = lin.split()[9]+' '+ lin.split()[11] +' '+lin.split()[13]
					if lin.split()[0] == 'QUALITY':
						rms = lin.split()[8]
					if lin.split()[0] == 'STATISTICS':
						err = str(sqrt(3.53*float(lin.split()[8]))) + ' '+str(sqrt(3.53*float(lin.split()[14]))) + ' '+ str(sqrt(3.53*float(lin.split()[18]))) 
					if i > 16 and len(lin.split()) > 1:
						infoxsta.append(lin.split()[0]+'    '+lin.split()[2]+'    '+lin.split()[4]+'    '+lin.split()[6]+' '+lin.split()[7]+' '+lin.split()[8]+' '+lin.split()[16])
					i = i+1		
		else:
			
		   	fechahora = '***'
			hipo = ' no hay '
			rms = 'localizacion '
			err = '***'
			infoxsta = ['*** Lecturas insuficientes ***']

		print 'yyyy mm dd hh mm ss.ssss    lat   long   depth        RMS          Dx         Dy        Dz'
		print fechahora+' '+hipo+' '+rms+' '+err+'\n'
		print 'sta   comp   fase  yyyymmdd  hhmm  ss  rms'
		for info in infoxsta:
			print info
				
		faltan = []
		for lin in uniq:
			if lin not in stapickfileuniq:
				faltan.append(lin)
		if len(faltan) > 0:
			print'\nLas siguientes estaciones no han sido leidas:\n'
			print faltan
		else:
			print'\nTodas las estaciones disponibles han sido leidas\n'
		
		if k == len(listdir):
			defi = raw_input('\nEste es el ultimo evento. Es esta la localizacion definitiva? [s/n]\n')
			while defi != 's' and defi != 'n':
				defi = raw_input('\nIncorrecto, intente otra vez.\nModificar una estacion [s/n]?:\n')
				if defi == 's' or defi == 'n':
					break
			if defi == 's':
				try:
#					hypfile = glob.glob('Iquique.'+dire.split('_')[0][0:4]+'*.hyp')[0]
#CAMBIAR				
					hypfile = glob.glob('Iquique.'+dire.split('_')[0][0:4]+'*.hyp')[0]

				except IndexError:
					hypfile = ''
				if hypfile:	
#				   cmd = 'cp '+final+'/Iquique.'+dire.split('_')[0][0:4]+'* '+finaldef
				   cmd = 'cp '+final+'/Iquique.'+dire.split('-')[0][0:4]+'* '+finaldef

				   os.system(cmd)
			  

				cmd = 'mv '+path+dire+' '+leidos
				os.system(cmd)
				print '*****************Fin******************'
				sys.exit(0)



#ACA COMIENZA LA MODIFICACION DE ESTACIONES


		resp = raw_input('\nModificar una estacion [s/n]?:\n')
		while resp != 's' and resp != 'n':
			resp = raw_input('\nIncorrecto, intente otra vez.\nModificar una estacion [s/n]?:\n')
			if resp == 's' or resp == 'n':
				break


					
		while resp == 's':
			#corrsta = raw_input('\nNombre de la estacion?:\n')
			#while corrsta not in sta:
			#	corrsta = raw_input('\nIncorrecto. Ingrese nuevamente.\nNombre de la estacion?:\n')

			cobo = raw_input('\nCorregir o borrar [c/b]?:\n')
			while cobo != 'c' and cobo != 'b':
				cobo = raw_input('\nIncorrecto, intente otra vez.\nCorregir o borrar [c/b]?:\n')
				if cobo == 'c' or cobo == 'b':
					break
			if cobo == 'b':
			   borrar = raw_input('\nEscriba la o las estaciones que quiere borrar separadas por un espacio:\n')
			   os.chdir(path+dire)
			   borr = borrar.split()
			   for st in borr:
				   #BORRAR EN EL PICK FILE
				   cmd = 'awk \'!/'+st+'/\' '+dire[0:len(dire)-1]+'.pick > temp && mv temp '+dire[0:len(dire)-1]+'.pick'
			           os.system(cmd)

									
			   with open(dire[0:len(dire)-1]+'.pick','r') as fichero:
					stapickfile = [] 
					arreglo = []
		
					for lin in fichero:
						if lin:
							arreglo.append(lin)
							stapickfile.append(lin.split()[0])

					stapickfileuniq = []
					for st in stapickfile:
						if st not in stapickfileuniq:
							stapickfileuniq.append(st)
			   if len(stapickfileuniq) >= nstamin:			
	
			
				cmd = 'cp '+dire[0:len(dire)-1]+'.pick '+loc
    			      	os.system(cmd)
			        os.chdir(loc)
				cmd = 'mv '+dire[0:len(dire)-1]+'.pick gatherpickfiles.dat'
				os.system(cmd)
				cmd = 'rm '+loc+'/final/*'
				os.system(cmd)

				subprocess.call(['NLLoc nlloc.in'],close_fds=True,shell=True)
						

				os.chdir(loc+'/final')
#CAMBIAR AQUI SEGUN LA CONFIGURACION DE LA CARPETA
				try:
#					hypfile = glob.glob('Iquique.'+dire.split('_')[0][0:4]+'*.hyp')[0]
					hypfile = glob.glob('Iquique.'+dire.split('-')[0][0:4]+'*.hyp')[0]

				except IndexError:
					hypfile = ''

	
				if hypfile:
#		   		  hypfile = glob.glob('Iquique.'+dire.split('_')[0][0:4]+'*.hyp')[0]
  		   		  hypfile = glob.glob('Iquique.'+dire.split('-')[0][0:4]+'*.hyp')[0]

		   		  time.sleep(3)
		   		  print '\n\nRESULTADOS DE LA LOCALIZACION:\n\n'
				  i = 1
       				  with open(hypfile,'r') as hyp:
				   infoxsta = []
				   for lin in hyp:
				    line = lin.rstrip()	
				    if line:
					if lin.split()[0] == 'GEOGRAPHIC':
						fechahorap = fechahora
						fechahora = lin.split()[2]+' '+ lin.split()[3] +' '+lin.split()[4]+' ' +lin.split()[5] +' ' + lin.split()[6] +' '+lin.split()[7]
						hipop = hipo
						hipo = lin.split()[9]+' '+ lin.split()[11] +' '+lin.split()[13]
					if lin.split()[0] == 'QUALITY':
						rmsp = rms
						rms = lin.split()[8]
					if lin.split()[0] == 'STATISTICS':
						errp = err
						err = str(sqrt(3.53*float(lin.split()[8]))) + ' '+str(sqrt(3.53*float(lin.split()[14]))) + ' '+ str(sqrt(3.53*float(lin.split()[18]))) 
					if i > 16 and len(lin.split()) > 1:
						infoxsta.append(lin.split()[0]+'    '+lin.split()[2]+'    '+lin.split()[4]+'  '+lin.split()[6]+'  '+lin.split()[7]+'  '+lin.split()[8]+'  '+lin.split()[16])
					

					i = i+1
				else:
					
					fechahorap = fechahora
		   			fechahora = '***'
					hipop = hipo
					hipo = ' no hay '
					rmsp = rms
					rms = 'localizacion '
					errp = err
					err = '***'
					infoxsta = ['*** Lecturas insuficientes ***']


				print '\nRESULTADO PREVIO'	
				print 'yyyy mm dd hh mm ss.ssss    lat   long   depth        RMS          Dx         Dy        Dz'
				print fechahorap+' '+hipop+' '+rmsp+' '+errp
	
				print 'RESULTADO ACTUAL'
				print 'yyyy mm dd hh mm ss.ssss    lat   long   depth        RMS          Dx         Dy        Dz'
				print fechahora+' '+hipo+' '+rms+' '+err+'\n'
				print 'sta  comp  fase  fecha        hora    rms'
				for info in infoxsta:
					print info
				faltan = []
				for lin in uniq:
					if lin not in stapickfileuniq:
						faltan.append(lin)
				if len(faltan) > 0:
					print'\nLas siguientes estaciones no han sido leidas\n'
					print faltan
				else:
					print'\nTodas las estaciones disponibles han sido leidas\n'
	
						
				if k == len(listdir):
					defi = raw_input('\nEste es el ultimo evento. Es esta la localizacion definitiva? [s/n]\n')
					while defi != 's' and defi != 'n':
						defi = raw_input('\nIncorrecto, intente otra vez.\nModificar una estacion [s/n]?:\n')
						if defi == 's' or defi == 'n':
							break
					if defi == 's':
#CAMBIAR						
						try:
#							hypfile = glob.glob('Iquique.'+dire.split('_')[0][0:4]+'*.hyp')[0]
							hypfile = glob.glob('Iquique.'+dire.split('-')[0][0:4]+'*.hyp')[0]

						except IndexError:
							hypfile = ''
						if hypfile:	
#				   		   cmd = 'cp '+final+'/Iquique.'+dire.split('_')[0][0:4]+'* '+finaldef
  				   		   cmd = 'cp '+final+'/Iquique.'+dire.split('-')[0][0:4]+'* '+finaldef

				                   os.system(cmd)

						cmd = 'mv '+path+dire+' '+leidos
						os.system(cmd)
						print '*****************Fin******************'
						sys.exit(0)



				resp = raw_input('\nModificar una estacion [s/n]?:\n')
				while resp != 's' and resp != 'n':
					resp = raw_input('\nIncorrecto, intente otra vez.\nModificar una estacion [s/n]?:\n')
					if resp == 's' or resp == 'n':
						break

			   else:

				   resp = raw_input('\nLecturas insuficientes. Modificar alguna estacion [s/n]?:\n')
				   while resp != 's' and resp != 'n':
					resp = raw_input('\nIncorrecto, intente otra vez.\nModificar una estacion [s/n]?:\n')
					if resp == 's' or resp == 'n':
						break
				   if resp == 'n':
					   print '\nArchivo pick tiene insuficientes lecturas y sera borrado...\n'
					   cmd = 'rm '+path+dire+dire[0:len(dire)-1]+'.pick'
					   os.system(cmd)
					   time.sleep(2)
					   if len(listdir) == 1 or k == len(listdir):
						   cmd = 'mv '+path+dire+' '+leidos
						   os.system(cmd)
						   print '*****************Fin******************'
						   sys.exit(0)

	




			if cobo == 'c':
			   corrsta = raw_input('\nNombre de la estacion?:\n')
			   while corrsta not in sta:
				corrsta = raw_input('\nIncorrecto. Ingrese nuevamente.\nNombre de la estacion?:\n')
	
								
#CAMBIAR AQUI SEGUN TIPO DE ARCHIVOS


			   os.chdir(path+dire)
#			   filez = glob.glob('*'+corrsta+'..*HZ*SAC')
			   filez = glob.glob('*'+corrsta+'..*HZ')

			   if not filez:
					filez = ' '
			   else:
					filez = filez[0]
#			   filen = glob.glob('*'+corrsta+'..*HN*SAC')
			   filen = glob.glob('*'+corrsta+'..*HN')
			   
			   if not filen:
					filen = ' '
			   else:
					filen = filen[0]
		
#			   filee = glob.glob('*'+corrsta+'..*HE*SAC')
			   filee = glob.glob('*'+corrsta+'..*HE')

			   if not filee:
					filee = ' '
			   else:
					filee = filee[0]
		
			
			   subprocess.call(['java net.alomax.seisgram2k.SeisGram2K -binarytype=SUN_UNIX '+filez+' '+filen+' '+filee+' -pick.file='+dire[0:len(dire)-1]+'.pick'],close_fds=True,shell=True)
			   with open(dire[0:len(dire)-1]+'.pick','r') as fichero:
					stapickfile = [] 
					arreglo = []
		
					for lin in fichero:
						if lin:
							arreglo.append(lin)
							stapickfile.append(lin.split()[0])

					stapickfileuniq = []
					for st in stapickfile:
						if st not in stapickfileuniq:
							stapickfileuniq.append(st)

                           if len(stapickfileuniq) >= nstamin:
				cmd = 'cp '+dire[0:len(dire)-1]+'.pick '+loc
    			      	os.system(cmd)
			        os.chdir(loc)
				cmd = 'mv '+dire[0:len(dire)-1]+'.pick gatherpickfiles.dat'
				os.system(cmd)
				cmd = 'rm '+loc+'/final/*'
				os.system(cmd)
				subprocess.call(['NLLoc nlloc.in'],close_fds=True,shell=True)
						


				os.chdir(loc+'/final')
				#CAMBIAR AQUI SEGUN LA CONFIGURACION DE LA CARPETA
				try:
#					hypfile = glob.glob('Iquique.'+dire.split('_')[0][0:4]+'*.hyp')[0]
#CAMBIAR				
					hypfile = glob.glob('Iquique.'+dire.split('-')[0][0:4]+'*.hyp')[0]

				except IndexError:
					hypfile = ''

	
				if hypfile:
#		   		  hypfile = glob.glob('Iquique.'+dire.split('_')[0][0:4]+'*.hyp')[0]
#CAMBIAR			  
				  hypfile = glob.glob('Iquique.'+dire.split('-')[0][0:4]+'*.hyp')[0]

		   		  time.sleep(3)
		   		  print '\n\nRESULTADOS DE LA LOCALIZACION:\n\n'
				  i = 1

       				  with open(hypfile,'r') as hyp:
				   infoxsta = []
				   for lin in hyp:
				    line = lin.rstrip()	
				    if line:
					if lin.split()[0] == 'GEOGRAPHIC':
						fechahorap = fechahora
						fechahora = lin.split()[2]+' '+ lin.split()[3] +' '+lin.split()[4]+' ' +lin.split()[5] +' ' + lin.split()[6] +' '+lin.split()[7]
						hipop = hipo
						hipo = lin.split()[9]+' '+ lin.split()[11] +' '+lin.split()[13]
					if lin.split()[0] == 'QUALITY':
						rmsp = rms
						rms = lin.split()[8]
					if lin.split()[0] == 'STATISTICS':
						errp = err
						err = str(sqrt(3.53*float(lin.split()[8]))) + ' '+str(sqrt(3.53*float(lin.split()[14]))) + ' '+ str(sqrt(3.53*float(lin.split()[18]))) 
					if i > 16 and len(lin.split()) > 1:
						infoxsta.append(lin.split()[0]+'    '+lin.split()[2]+'    '+lin.split()[4]+'  '+lin.split()[6]+'  '+lin.split()[7]+'  '+lin.split()[8]+'  '+lin.split()[16])
							

					i = i+1
				else:
					fechahorap = fechahora
		   			fechahora = '***'
					hipop = hipo
					hipo = ' no hay '
					rmsp = rms
					rms = 'localizacion '
					errp = err
					err = '***'
					infoxsta = ['*** Lecturas insuficientes ***']

	
				print '\nRESULTADO PREVIO'	
				print 'yyyy mm dd hh mm ss.ssss    lat   long   depth        RMS          Dx         Dy        Dz'
				print fechahorap+' '+hipop+' '+rmsp+' '+errp
			
				print 'RESULTADO ACTUAL'
				print 'yyyy mm dd hh mm ss.ssss    lat   long   depth        RMS          Dx         Dy        Dz'
				print fechahora+' '+hipo+' '+rms+' '+err+'\n'
				print 'sta  comp  fase  fecha        hora    rms'
				for info in infoxsta:
					print info

				faltan = []
				for lin in uniq:
					if lin not in stapickfileuniq:
						faltan.append(lin)
				if len(faltan) > 0:
					print'\nLas siguientes estaciones no han sido leidas\n'
					print faltan
				else:
					print'\nTodas las estaciones disponibles han sido leidas\n'
	
						
				if k == len(listdir):
					defi = raw_input('\nEste es el ultimo evento. Es esta la localizacion definitiva? [s/n]\n')
					while defi != 's' and defi != 'n':
						defi = raw_input('\nIncorrecto, intente otra vez.\nModificar una estacion [s/n]?:\n')
						if defi == 's' or defi == 'n':
							break
					if defi == 's':
#						cmd = 'cp '+final+'/Iquique.'+dire.split('_')[0][0:4]+'* '+finaldef
#CAMBIAR					
						cmd = 'cp '+final+'/Iquique.'+dire.split('-')[0][0:4]+'* '+finaldef

						os.system(cmd)
						cmd = 'mv '+path+dire+' '+leidos
						os.system(cmd)
						print '*****************Fin******************'
						sys.exit(0)


				resp = raw_input('\nModificar una estacion [s/n]?:\n')
				while resp != 's' and resp != 'n':
					resp = raw_input('\nIncorrecto, intente otra vez.\nModificar una estacion [s/n]?:\n')
					if resp == 's' or resp == 'n':
						break

			   else:

				   resp = raw_input('\nLecturas insuficientes. Modificar alguna estacion [s/n]?:\n')
				   while resp != 's' and resp != 'n':
					resp = raw_input('\nIncorrecto, intente otra vez.\nModificar una estacion [s/n]?:\n')
					if resp == 's' or resp == 'n':
						break
				   if resp == 'n':
					   print '\nArchivo pick tiene insuficientes lecturas y sera borrado...\n'
					   cmd = 'rm '+path+dire+dire[0:len(dire)-1]+'.pick'
					   os.system(cmd)
					   time.sleep(2)
					   if len(listdir) == 1 or k == len(listdir):
						   cmd = 'mv '+path+dire+' '+leidos
						   os.system(cmd)
						   print '*****************Fin******************'
						   sys.exit(0)



					
		
 	   else:
		cmd = 'rm '+path+dire+dire[0:len(dire)-1]+'.pick'
		os.system(cmd)
		print '\nArchivo pick tiene insuficientes lecturas y serA borrado. El evento no sera localizado.\n'
		time.sleep(2)
		if len(listdir) == 1 or k == len(listdir):
			cmd = 'mv '+path+dire+' '+leidos
			os.system(cmd)



	else:
		print '\nMuy pocas estaciones en el directorio '+dire+'. El evento no sera localizado.\n'
		time.sleep(2)
		if len(listdir) == 1 or k == len(listdir):
			cmd = 'mv '+path+dire+' '+leidos
			os.system(cmd)


		
			
		
	



