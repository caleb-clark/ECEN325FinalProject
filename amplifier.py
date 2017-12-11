import math
import cmd

def get_parallel_r(r1, r2):
	return ((r1*r2)/(r1+r2))

def get_inverse_r(req, r1):
	return ((req*r1)/(r1-req))

def get_rg1_rg2(req, vg, Vdd):
	a = []
	a.append((Vdd*req)/(vg))
	a.append(get_inverse_r(req,a[0]))
	return a

def get_gm_1(Id, Vgs, Vth):
	return (2*Id/(Vgs-Vth))
def get_gm_2(beta, Id):
	return math.sqrt(2*beta*Id)

def get_vgs_1(Id, Vth, gm):
	return (2*Id)/gm + Vth
def in_sat(vd,vg,vt):
	if vd-vg > vt:
		return True
	else:
		return False

def gain_(req, rin, gm, rd):

	return (req/(req+rin))*(-1*gm*rd)

def first_two_stages(fileName,gain,input_impedance,s_resistance,vdd,beta,vt,vs):
	'''
	gain = float(input('What is the desired gain? [V/V] '))

	input_impedance = float(input('What is the desired input impedance? '))

	s_resistance = float(input('What is the resistance before the first capacitor (if any)? '))

	vdd = float(input('What is Vdd? '))

	beta = float(input('What is beta? '))
	'''
	# W = 9.7m L = 2u Vto = 2, Kp=20.78u


	rd_gm_vals = []

	increment = 5000/50

	gain_factor = (input_impedance)/(input_impedance+s_resistance)

	for i in range(1,50):
		rd = increment*i
		gm = (gain/gain_factor)/rd

		rd_gm_vals.append([rd, gm])
	Ids = []
	for q in rd_gm_vals:
		Id = (q[1]**2)/(beta*2)
		Ids.append(Id)
	vd = []

	for i in range(0, len(rd_gm_vals)):
		vd.append(vdd-Ids[i]*rd_gm_vals[i][0])



	VGSs = []

	for i in Ids:
		blah = []
		for j in rd_gm_vals:

			blah.append(get_vgs_1(i, vt, j[1]))
		VGSs.append(blah)

	

	rs = []

	for i in Ids:
		rs.append(vs/i)

	VGs = []

	for i in VGSs:
		blah = []
		for j in i:
			blah.append(j+vs)
		VGs.append(blah)
	print(VGs)
	print(len(vd))
	print(len(VGs))
	for i in range(0,len(VGs)):
		j = len(VGs[i])	-1

		while j >= 0:
			#print(vd[i])
			#print(VGs[i][j])
			if not in_sat(vd[i],VGs[i][j],vt):
				VGs[i].pop(j)
				VGSs[i].pop(j)
			j -= 1

	rgs = []

	for q in VGs:
		blah = []
		for a in q:
			qq = get_rg1_rg2(input_impedance, a, vdd)
			blah.append(qq)
		rgs.append(blah)

	for i in range(0, len(rd_gm_vals)):
		if Ids[i] < 1e-3:
			continue
		print('------------------------------------------------------')
		print('OPTION ' + str(i))
		print('gm: ' + str(rd_gm_vals[i][1]))
		print('Id: ' + str(Ids[i]))
		print('Rd: ' + str(rd_gm_vals[i][0]))
		print('Rs: ' + str(rs[i]))
		print('Vs: ' + str(vs))
		print('Vd: ' + str(vd[i]))


	option = int(input ('Take a look at one of the options in more detail? (Choose an option) '))



	print('------------------------------------------------------')
	print('OPTION ' + str(option))
	print('gm: ' + str(rd_gm_vals[option][1]))
	print('Id: ' + str(Ids[option]))
	print('Rd: ' + str(rd_gm_vals[option][0]))
	print('Rs: ' + str(rs[option]))
	print('Vs: ' + str(vs))

	for i in range(0, len(VGSs[option])):
		print('------------------------------------------------------')
		print('Suboption: ' + str(i))
		
		print('VGS: ' + str(VGSs[option][i]))
		print('VG: ' + str(VGs[option][i]))
		print('Rg1: ' + str(rgs[option][i][0]))
		print('Rg2: ' + str(rgs[option][i][1]))

	option2 =  int(input ('Which suboption? '))


	print('gm: ' + str(rd_gm_vals[option][1]))
	print('Id: ' + str(Ids[option]))
	print('Rd: ' + str(rd_gm_vals[option][0]))
	print('Rs: ' + str(rs[option]))
	print('Vs: ' + str(vs))
	print('VGS: ' + str(VGSs[option][option2]))
	print('VG: ' + str(VGs[option][option2]))
	print('Rg1: ' + str(rgs[option][option2][0]))
	print('Rg2: ' + str(rgs[option][option2][1]))

	with open(fileName,'w+') as outfile:
		outfile.write('Vt: ' + str(vt))
		outfile.write('\n')
		outfile.write('Beta: ' + str(beta))
		outfile.write('\n')
		outfile.write('gm: ' + str(rd_gm_vals[option][1]))
		outfile.write('\n')
		outfile.write('Id: ' + str(Ids[option]))
		outfile.write('\n')
		
		outfile.write('Vd: ' + str(vd[option]))
		outfile.write('\n')
		outfile.write('Vg: ' + str(VGs[option][option2]))
		outfile.write('\n')
		outfile.write('Vs: ' + str(vs))
		outfile.write('\n')
		outfile.write('Vgs: ' + str(VGSs[option][option2]))
		outfile.write('\n')
		outfile.write('Vds: ' + str(vd[option] - vs))
		outfile.write('\n')

		outfile.write('Rg1: ' + str(rgs[option][option2][0]))
		outfile.write('\n')
		outfile.write('Rg2: ' + str(rgs[option][option2][1]))
		outfile.write('\n')
		outfile.write('Rd: ' + str(rd_gm_vals[option][0]))
		outfile.write('\n')
		outfile.write('Rs: ' + str(rs[option]))
		outfile.write('\n')
		av = gain_(get_parallel_r(rgs[option][option2][0], rgs[option][option2][1]), s_resistance, rd_gm_vals[option][1], rd_gm_vals[option][0])

		outfile.write('Gain: ' + str(av))
		outfile.write('\n')
		if in_sat(vd[option], VGs[option][option2], vt):
			outfile.write('IN SAT MODE\n')

		outfile.write('Vdg: ' + str(-1*(VGs[option][option2]-vd[option])))
		outfile.write('\n')

		outfile.write('\n')


def gain_src_follower(rs, vgs,vth, id_):
	return (rs/(rs+((vgs-vth)/(2*id_))))
def get_rs_buffer(vdd,vgs,id_):
	return (vdd-vgs)/(id_)
def get_rs_buffer2(gain,vdd,vth,id_):
	return(gain*(vdd-vth)/(id_*(2-gain)))
def equal_(gain_,gain__):
	if (gain_/gain__) < 1.000001 and (gain_/gain__) > 0.999999:
		return True
	else:
		return False
def buffer_stage(fileName, gain, dc_voltage, vth=2, Vdd=10, Beta=0.100783):

	increment=0.0005 #Amps

	Ids = []

	index = 1
	while index*increment <= 0.1:
		Ids.append(increment*index)
		index += 1
	'''
	Rs = []
	for i in range(0, len(Ids)):
		Rs.append(get_rs_buffer2(gain,Vdd,vth,Ids[i]))
	'''
	for id__ in Ids:
		for rs in range(0,500000):
			rs_act = rs/100
			vgs = Vdd - id__*rs_act
			gain__ = gain_src_follower(rs_act,vgs,vth,id__)
			if equal_(gain__, gain):
				print('ID: ' +str(id__))
				print('Gain: ' +str(gain__))
				return rs_act


	for i in range(0, len(Ids)):

		print('Option' + str(i))
		print('Id: ' + str(Ids[i]))
		print('Rs: ' + str(Rs[i]))
		print('Gain: ' + str(gain_src_follower(Rs[i],(Vdd-Ids[i]*Rs[i]), vth,Ids[i])))




#print(buffer_stage('buffer_stage.txt', 0.625, 6.12))
first_two_stages('first_stage.txt',8,5e6,100000,10,0.100783,2,0.4)
first_two_stages('second_stage.txt',6,1.1e6,0,10,0.100783,2,0.4)
