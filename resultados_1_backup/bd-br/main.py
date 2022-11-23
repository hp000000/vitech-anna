from bjontegaard_metric import *

def readBitratePSNR(root, folders, files, qps=["22/","27/","32/","37/"]):
	file_saida = open(root+"resultados.csv","a")
	file_saida.write("Video;Time Saving;BD-BR;Model Time\n")
	time_savings = []
	BD_BRs = []
	t_models = []
	for folder in folders:
		R1 = []
		PSNR1 = []
		R2 = []
		PSNR2 = []
		T1 = []
		T2 = []
		T_model = []
		for qp in qps:
			file_original   = open(root+folder+qp+files[0],"r")
			file_modificado = open(root+folder+qp+files[1],"r")
			pular_linhas_original = True
			pular_linhas_modificado = True
			while pular_linhas_original or pular_linhas_modificado:
				if pular_linhas_original:
					linha_original = file_original.readline()
					if 'Total Frames' in linha_original:
						linha_original = file_original.readline()
						pular_linhas_original = False
				if pular_linhas_modificado:
					linha_modificado = file_modificado.readline()
					if 'Total Frames' in linha_modificado:
						linha_modificado = file_modificado.readline()
						pular_linhas_modificado = False
			eficiencia_original = list(filter(("").__ne__,linha_original.lstrip().rstrip().split(" ")))
			eficiencia_modificado = list(filter(("").__ne__,linha_modificado.lstrip().rstrip().split(" ")))

			tempo_modelo = file_modificado.readline()
			for i in range(3):
				linha_original = file_original.readline()
				linha_modificado = file_modificado.readline()
			tempo_original = list(filter(("").__ne__,linha_original.lstrip().rstrip().split(" "))) #linha_original.rstrip("\n").split(" ")   
			tempo_modificado = list(filter(("").__ne__,linha_modificado.lstrip().rstrip().split(" ")))

			R1.append(float(eficiencia_original[2])) #Bitrate original
			R2.append(float(eficiencia_modificado[2])) #Bitrate modificado
			PSNR1.append(float(eficiencia_original[-1].replace("\n",""))) #PSNR original
			PSNR2.append(float(eficiencia_modificado[-1].replace("\n",""))) #PSNR modificado
			T1.append(float(tempo_original[5])) #Tempo original
			T2.append(float(tempo_modificado[5])) #Tempo modificado
			T_model.append(float(tempo_modelo.split(":")[1].lstrip().rstrip())) #Tempo modelo
			file_original.close()
			file_modificado.close()
		R1 = np.array(R1) #Bitrate original
		R2 = np.array(R2) #Bitrate modificado
		PSNR1 = np.array(PSNR1) #PSNR original
		PSNR2 = np.array(PSNR2) #PSNR modificado
		BD_BRs.append(round(BD_RATE(R1, PSNR1, R2, PSNR2),2))
		BD_BR = str(BD_BRs[-1]).replace(".",",") #BD-BR
		TS = [100-(T2[i]*100/T1[i]) for i in range(4)] #Time saving para cada QP
		time_savings.append(round(sum(TS)/len(TS),2))
		TS = str(time_savings[-1]).replace(".",",") #Média de Time Saving considerando todos os QPs
		TM = [T_model[i]*100/T2[i] for i in range(4)] #Tempo do modelo em cada QP
		t_models.append(round(sum(TM)/len(TM),2))
		TM = str(t_models[-1]).replace(".",",") #Média do tempo do modelo considerando todos os QPs
		file_saida.write(folder[:-1]+";"+TS+";"+BD_BR+";"+TM+"\n")
	file_saida.write("Average;"+str(round(sum(time_savings)/len(time_savings),2)).replace(".",",")+";"+str(round(sum(BD_BRs)/len(BD_BRs),2)).replace(".",",")+";"+str(round(sum(t_models)/len(t_models),2)).replace(".",","))
	file_saida.close()

#Anna: deves trocar o caminho raiz para onde está a pasta contendo os arquivos com os resultados no seu computador
readBitratePSNR("/home/pc-lacan/Downloads/vitech-anna-main/xgb/resultados/", ["720p/FourPeople/","1080p/BasketballDrive/","4k/FoodMarket4/"], ["original.txt","anna.txt"])
